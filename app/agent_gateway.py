"""Gateway acotado para ejecucion simulada o ADK real explicitamente autorizada."""

import copy
from dataclasses import dataclass
import json
import re
import uuid
from typing import Any, Dict, List, Optional, Tuple

import app.demo_intake as demo_intake
from app.local_repository import LocalRepository
from app.runtime_config import REAL_MODE, SIMULATED_MODE, RuntimeConfig


class ModelCallResponse:
    """Respuesta normalizada; ``usage_confirmed`` gobierna la reconciliacion."""

    def __init__(
        self,
        content: str,
        input_tokens: int,
        output_tokens: int,
        status_code: int = 200,
        error_message: Optional[str] = None,
        is_transient: bool = False,
        usage_confirmed: bool = True,
    ) -> None:
        self.content = content
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.status_code = status_code
        self.error_message = error_message
        self.is_transient = is_transient
        self.usage_confirmed = usage_confirmed


class ModelClientProvider:
    def call_model(
        self,
        model_name: str,
        system_instruction: str,
        prompt: str,
        timeout_seconds: int,
        *,
        max_output_tokens: int = 4096,
        response_schema: Optional[Dict[str, Any]] = None,
    ) -> ModelCallResponse:
        raise NotImplementedError


@dataclass(frozen=True)
class ValidatedRealExecutionMandate:
    """Mandato devuelto solo tras validar la decision humana persistida."""

    mission_id: str
    task_id: str
    owner_id: str
    approval_id: str
    decision: str
    persisted: bool
    is_current: bool


class RealExecutionAuthorizationValidator:
    """Puerto confiable hacia aprobaciones persistidas; no acepta prompts ni HTTP."""

    def validate(
        self, *, mission_id: str, task_id: str, owner_id: str, approval_id: str
    ) -> Optional[ValidatedRealExecutionMandate]:
        raise NotImplementedError


@dataclass(frozen=True)
class PersistedCallOutcome:
    """Resultado terminal recuperable por una clave logica durable."""

    ok: bool
    result: Optional[Dict[str, Any]]
    error: Optional[Dict[str, Any]]


class DurableCallIdempotencyStore:
    """Puerto durable y atomico; el gateway no implementa una cache volatil."""

    def begin(
        self, *, mission_id: str, task_id: str
    ) -> Tuple[str, Optional[PersistedCallOutcome]]:
        """Devuelve NEW, IN_PROGRESS o REPLAY junto al resultado persistido."""
        raise NotImplementedError

    def complete(
        self, *, mission_id: str, task_id: str, outcome: PersistedCallOutcome
    ) -> None:
        raise NotImplementedError


class MockModelClientProvider(ModelClientProvider):
    """Proveedor determinista; siempre representa evidencia SIMULADA."""

    provider_kind = "MOCK_SIMULADA"

    def __init__(self, responses: Optional[List[ModelCallResponse]] = None) -> None:
        self.responses = responses or []
        self.call_history: List[dict] = []

    def add_response(self, response: ModelCallResponse) -> None:
        self.responses.append(response)

    def call_model(
        self,
        model_name: str,
        system_instruction: str,
        prompt: str,
        timeout_seconds: int,
        *,
        max_output_tokens: int = 4096,
        response_schema: Optional[Dict[str, Any]] = None,
    ) -> ModelCallResponse:
        self.call_history.append(
            {
                "model_name": model_name,
                "system_instruction": system_instruction,
                "prompt": prompt,
                "timeout_seconds": timeout_seconds,
                "max_output_tokens": max_output_tokens,
                "response_schema": response_schema,
            }
        )
        if self.responses:
            return self.responses.pop(0)
        return ModelCallResponse(
            '{"summary": "Respuesta simulada exitosa", '
            '"findings": ["Hallazgo simulado"]}',
            input_tokens=150,
            output_tokens=80,
        )


class AgentGateway:
    """Reserva antes de invocar y falla cerrado ante estado incierto."""

    def __init__(
        self,
        config: Optional[RuntimeConfig] = None,
        provider: Optional[ModelClientProvider] = None,
        repository=None,
        mission_id: str = "MSN-SIM-GATEWAY",
        *,
        real_execution_authorized: bool = False,
        real_authorization_validator: Optional[RealExecutionAuthorizationValidator] = None,
        idempotency_store: Optional[DurableCallIdempotencyStore] = None,
    ) -> None:
        self.config = config or RuntimeConfig()
        self.provider = provider or MockModelClientProvider()
        self.repository = repository or LocalRepository()
        self.mission_id = mission_id
        # Compatibilidad de firma: este booleano queda deliberadamente sin autoridad.
        self.real_execution_authorized = real_execution_authorized
        self.real_authorization_validator = real_authorization_validator
        self.idempotency_store = idempotency_store
        self.total_spent_usd = 0.0
        self.agent_requests_count = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.alerts_emitted: List[float] = []

    @staticmethod
    def _fail(code: str, message: str):
        return False, None, demo_intake.make_error_payload(code, message)

    def sanitize_outbound_data(
        self, system_prompt: str, user_prompt: str
    ) -> Tuple[bool, Optional[str]]:
        if not isinstance(system_prompt, str) or not isinstance(user_prompt, str):
            return False, "Instruccion y prompt deben ser texto."
        combined = f"{system_prompt}\n{user_prompt}"
        patterns = [
            r"AIza[0-9A-Za-z-_]{30,}",
            r"(?i)api[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]",
            r"(?i)secret[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]",
            r"(?i)private[_-]?key",
        ]
        if any(re.search(pattern, combined) for pattern in patterns):
            return False, "Deteccion de secreto o clave privada en contenido saliente."
        if len(combined.encode("utf-8")) > self.config.max_input_tokens:
            return False, "Entrada excede la cota conservadora previa a tokenizacion."
        return True, None

    def sanitize_inbound_content(
        self, raw_content: str
    ) -> Tuple[bool, str, Optional[str]]:
        if not isinstance(raw_content, str):
            return False, "", "Respuesta del proveedor no textual."
        lowered = raw_content.lower()
        forbidden = (
            "<thought>",
            "</thought>",
            "<reasoning>",
            "</reasoning>",
            "chain_of_thought",
            "internal_reasoning",
        )
        if any(item in lowered for item in forbidden):
            return False, "", "Respuesta rechazada: contiene razonamiento interno o Chain-of-Thought."
        if re.search(r"AIza[0-9A-Za-z-_]{30,}", raw_content):
            return False, "", "Respuesta rechazada: contiene material sensible."
        return True, raw_content.strip(), None

    @staticmethod
    def _validate_schema(value: dict, schema: Dict[str, Any]) -> Optional[str]:
        try:
            from jsonschema import Draft202012Validator

            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(value)
        except Exception:
            return "La salida no cumple el esquema JSON autorizado."
        return None

    @staticmethod
    def _declares_tool_action(value: Any) -> bool:
        if isinstance(value, dict):
            for key, nested in value.items():
                if key.lower() in {
                    "tool_call",
                    "tool_calls",
                    "function_call",
                    "function_calls",
                }:
                    return True
                if AgentGateway._declares_tool_action(nested):
                    return True
        elif isinstance(value, list):
            return any(AgentGateway._declares_tool_action(item) for item in value)
        return False

    def _validate_mode(
        self,
        model: str,
        *,
        mission_id: str,
        task_id: Optional[str],
        owner_id: Optional[str],
        approval_id: Optional[str],
    ) -> Optional[str]:
        if self.config.execution_mode == SIMULATED_MODE:
            if not isinstance(self.provider, MockModelClientProvider):
                return "El modo SIMULADA solo admite el proveedor mock."
            return None
        if self.config.execution_mode != REAL_MODE:
            return "Modo de ejecucion no permitido."
        if getattr(self.provider, "provider_kind", None) != "ADK_REAL":
            return "El modo REAL requiere el proveedor ADK permitido."
        valid, error = self.config.validate_real_profile()
        if not valid:
            return error
        if model != self.config.model_id:
            return "El modelo solicitado no coincide con el perfil real permitido."
        if not bool(getattr(self.provider, "has_credentials", lambda: False)()):
            return "Credencial real ausente."
        ready, reason = getattr(self.provider, "preflight", lambda: (False, "ADK no verificado."))()
        if not ready:
            return reason
        references = (mission_id, task_id, owner_id, approval_id)
        if any(not isinstance(value, str) or not value.strip() for value in references):
            return "Faltan referencias del mandato real concreto."
        validator = self.real_authorization_validator
        if validator is None:
            return "La ejecucion real carece de un validador confiable."
        try:
            mandate = validator.validate(
                mission_id=mission_id,
                task_id=task_id,
                owner_id=owner_id,
                approval_id=approval_id,
            )
        except Exception:
            return "No fue posible validar el mandato real de forma confiable."
        if not isinstance(mandate, ValidatedRealExecutionMandate):
            return "El mandato real no fue validado."
        if (
            mandate.mission_id != mission_id
            or mandate.task_id != task_id
            or mandate.owner_id != owner_id
            or mandate.approval_id != approval_id
            or mandate.decision not in ("APROBAR", "APROBAR_CON_EXCEPCION")
            or mandate.persisted is not True
            or mandate.is_current is not True
        ):
            return "El mandato real no coincide o ya no esta vigente."
        if self.idempotency_store is None:
            return "La ejecucion real carece de idempotencia durable."
        return None

    def _begin_real_call(self, mission_id: str, task_id: str):
        try:
            state, persisted = self.idempotency_store.begin(
                mission_id=mission_id, task_id=task_id
            )
        except Exception:
            return "ERROR", None
        if state == "NEW" and persisted is None:
            return state, None
        if state == "IN_PROGRESS" and persisted is None:
            return state, None
        if state == "REPLAY" and isinstance(persisted, PersistedCallOutcome):
            return state, persisted
        return "ERROR", None

    def _complete_real_call(
        self,
        mission_id: str,
        task_id: str,
        outcome: PersistedCallOutcome,
    ):
        try:
            self.idempotency_store.complete(
                mission_id=mission_id, task_id=task_id, outcome=outcome
            )
        except Exception:
            return self._fail(
                "SYSTEM_ERROR",
                "El resultado terminal no pudo persistirse; replay bloqueado.",
            )
        return copy.deepcopy((outcome.ok, outcome.result, outcome.error))

    def execute_agent_call(
        self,
        system_instruction,
        prompt,
        preferred_model=None,
        *,
        mission_id=None,
        task_id=None,
        owner_id=None,
        approval_id=None,
        response_schema: Optional[Dict[str, Any]] = None,
    ):
        ok, message = self.sanitize_outbound_data(system_instruction, prompt)
        if not ok:
            return self._fail("PERMISSION_DENIED", message or "Entrada rechazada.")
        schema = {"type": "object"} if response_schema is None else response_schema
        if not isinstance(schema, dict):
            return self._fail("INVALID_INPUT", "Esquema JSON requerido e invalido.")
        try:
            from jsonschema import Draft202012Validator

            Draft202012Validator.check_schema(schema)
        except Exception:
            return self._fail("INVALID_INPUT", "Esquema JSON requerido e invalido.")
        bounded_input = (
            system_instruction
            + "\n"
            + prompt
            + "\n"
            + json.dumps(schema, sort_keys=True, separators=(",", ":"))
        )
        if len(bounded_input.encode("utf-8")) > self.config.max_input_tokens:
            return self._fail(
                "INVALID_INPUT",
                "Entrada y esquema exceden la cota conservadora previa a tokenizacion.",
            )

        model = preferred_model or self.config.model_id
        mid = mission_id or self.mission_id
        tid = task_id or (
            None if self.config.execution_mode == REAL_MODE else "TSK-" + uuid.uuid4().hex
        )
        mode_error = self._validate_mode(
            model,
            mission_id=mid,
            task_id=tid,
            owner_id=owner_id,
            approval_id=approval_id,
        )
        if mode_error:
            return self._fail("PERMISSION_DENIED", mode_error)
        try:
            reservation_cost = self.config.calculate_call_cost(
                model, self.config.max_input_tokens, self.config.max_output_tokens
            )
        except (KeyError, ValueError):
            return self._fail("INVALID_INPUT", "Tarifa permitida no definida.")

        is_real = self.config.execution_mode == REAL_MODE
        if is_real:
            idempotency_state, persisted = self._begin_real_call(mid, tid)
            if idempotency_state == "REPLAY":
                return copy.deepcopy((persisted.ok, persisted.result, persisted.error))
            if idempotency_state == "IN_PROGRESS":
                return self._fail(
                    "SYSTEM_ERROR",
                    "La llamada real ya esta registrada sin resultado terminal; no reintentar.",
                )
            if idempotency_state != "NEW":
                return self._fail(
                    "SYSTEM_ERROR", "No fue posible adquirir la clave idempotente durable."
                )

        def finish(outcome):
            if is_real:
                return self._complete_real_call(mid, tid, PersistedCallOutcome(*outcome))
            return outcome

        max_attempts = min(2, self.config.max_retries + 1)
        for attempt in range(1, max_attempts + 1):
            try:
                key = self.repository.reserve_call(
                    mid,
                    tid,
                    reservation_cost,
                    max_budget_usd=self.config.max_budget_usd,
                    max_requests=self.config.max_agent_requests,
                )
            except ValueError as exc:
                code = "SYSTEM_ERROR" if "indeterminada" in str(exc).lower() else "BUDGET_EXHAUSTED"
                return finish(self._fail(code, str(exc)))
            usage = self.repository.get_object("usage", mid) or {"requests": 0}
            self.agent_requests_count = usage["requests"]
            try:
                response = self.provider.call_model(
                    model,
                    system_instruction,
                    prompt,
                    self.config.timeout_seconds,
                    max_output_tokens=self.config.max_output_tokens,
                    response_schema=schema,
                )
            except Exception:
                return self._fail(
                    "SYSTEM_ERROR",
                    "Resultado del proveedor indeterminado; reserva retenida y sin reintento.",
                )
            if not isinstance(response, ModelCallResponse):
                return self._fail(
                    "SYSTEM_ERROR",
                    "Uso del proveedor indeterminado; reserva retenida y sin reintento.",
                )
            if response.status_code in (401, 403) and not response.usage_confirmed:
                return self._fail(
                    "PERMISSION_DENIED",
                    "Proveedor rechazo autorizacion; uso indeterminado, reserva retenida y sin reintento.",
                )
            if not response.usage_confirmed:
                return self._fail(
                    "SYSTEM_ERROR",
                    "Uso del proveedor indeterminado; reserva retenida y sin reintento.",
                )
            if (
                type(response.input_tokens) is not int
                or type(response.output_tokens) is not int
                or not 0 <= response.input_tokens <= self.config.max_input_tokens
                or not 0 <= response.output_tokens <= self.config.max_output_tokens
            ):
                return self._fail(
                    "SYSTEM_ERROR",
                    "Consumo fuera de reserva; llamada retenida para revision.",
                )
            cost = self.config.calculate_call_cost(
                model, response.input_tokens, response.output_tokens
            )
            try:
                self.repository.reconcile_call(key, cost)
            except ValueError:
                return self._fail(
                    "SYSTEM_ERROR", "No fue posible reconciliar la reserva exactamente una vez."
                )

            snapshot = self.repository.budget_snapshot()
            self.total_spent_usd = snapshot["spent_usd"]
            self.total_input_tokens += response.input_tokens
            self.total_output_tokens += response.output_tokens
            threshold = self.config.check_threshold_alert(snapshot["committed_usd"])
            if threshold is not None and threshold not in self.alerts_emitted:
                self.alerts_emitted.append(threshold)

            if response.status_code == 200:
                valid, clean, error = self.sanitize_inbound_content(response.content)
                if not valid:
                    return finish(self._fail("SCHEMA_INVALID", error or "Respuesta rechazada."))
                try:
                    result = json.loads(clean)
                    if not isinstance(result, dict):
                        raise ValueError
                except (TypeError, ValueError):
                    return finish(self._fail("SCHEMA_INVALID", "La salida no es un objeto JSON valido."))
                schema_error = self._validate_schema(result, schema)
                if schema_error or self._declares_tool_action(result):
                    return finish(self._fail(
                        "SCHEMA_INVALID",
                        schema_error or "La salida declara una herramienta no autorizada.",
                    ))
                return finish((
                    True,
                    {
                        "content": result,
                        "model": model,
                        "input_tokens": response.input_tokens,
                        "output_tokens": response.output_tokens,
                        "cost_usd": cost,
                        "cost_kind": "REAL_ESTIMADA" if is_real else "SIMULADA",
                        "execution_evidence": "REAL_NO_VERIFICADA" if is_real else "SIMULADA",
                        "attempts": attempt,
                    },
                    None,
                ))
            if response.status_code in (401, 403):
                return finish(self._fail("PERMISSION_DENIED", "Proveedor rechazo autorizacion."))
            if response.status_code in (408, 429, 500, 502, 503, 504) and response.is_transient:
                if attempt < max_attempts:
                    continue
                return finish(self._fail("TRANSIENT_FAILURE", "Unico reintento transitorio agotado."))
            return finish(self._fail("SYSTEM_ERROR", "Fallo controlado del proveedor."))
        return finish(self._fail("TRANSIENT_FAILURE", "Intentos agotados."))
