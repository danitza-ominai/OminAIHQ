"""OminAI HQ - Modulo de decision humana del plan en ensayo local (PZ-003B SIMULADA).

Implementa la puerta local determinista de decision sobre el plan propuesto:
solicitud pendiente por defecto, decision interactiva vinculada a huella exacta,
validez de 300 segundos, idempotencia, prevencion de doble respuesta,
transicion MT-005 hacia AUTORIZADA_PARA_EJECUTAR al aprobar, y checkpoint efimero en memoria.
Cumple estrictamente con CONTRATO-MVP-v1.md y FICHA-PZ-003B-DECISION-HUMANA-DEL-PLAN.md.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re
import sys
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None

import app.demo_intake as demo_intake

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTRACTS_CORE_DIR = PROJECT_ROOT / "contracts" / "core"

MAX_LINE_LENGTH = 4096
APPROVAL_VALIDITY_SECONDS = 300

ALLOWED_COMMAND_KEYS = {
    "approval_id",
    "version_or_fingerprint",
    "decision",
    "comment",
    "idempotency_key",
}

VALID_DECISIONS = {"APROBAR", "RECHAZAR", "SOLICITAR_CAMBIOS"}
_UNSET = object()


class ReviewError(Exception):
    """Rechazo controlado con mensaje propio, sin datos de la entrada."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message


def failure_result(code: str, message: str) -> Tuple[int, dict]:
    """No publica registros cuya integridad no se pudo comprobar."""
    envelope = demo_intake._empty_envelope()
    envelope.update(approvals=[], approval_history=[], checkpoints=[], review=None)
    envelope["errors"] = [demo_intake.make_error_payload(code, message)]
    envelope["next_action"] = "Ensayo SIMULADA detenido sin aplicar la operacion; sesion no persistida."
    return (2 if code == "NOT_FOUND" else 1), envelope


def load_all_contracts() -> Tuple[dict, dict, dict, dict, dict, dict]:
    """Carga los cinco schemas nucleares y la maquina de estados."""
    mission_schema, event_schema, error_schema, state_machine = demo_intake.load_core_contracts()
    approval_schema_path = CONTRACTS_CORE_DIR / "approval.schema.json"
    checkpoint_schema_path = CONTRACTS_CORE_DIR / "checkpoint.schema.json"

    with open(approval_schema_path, "r", encoding="utf-8") as f:
        approval_schema = json.load(f)
    with open(checkpoint_schema_path, "r", encoding="utf-8") as f:
        checkpoint_schema = json.load(f)

    return mission_schema, event_schema, error_schema, approval_schema, checkpoint_schema, state_machine


def compute_plan_fingerprint(
    mission_id: str,
    user_id: str,
    brief_version: int,
    plan_version: int,
    brief: dict,
    plan: dict,
) -> str:
    """Calcula la huella SHA-256 exacta y canonica del contenido del brief y plan."""
    payload = {
        "mission_id": mission_id,
        "user_id": user_id,
        "brief_version": brief_version,
        "plan_version": plan_version,
        "brief": brief,
        "plan": plan,
    }
    canonical_json = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    digest = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest().lower()
    return f"sha256:{digest}"


def compute_checkpoint_fingerprint(checkpoint_data: dict) -> str:
    """Calcula la huella canonica del checkpoint excluyendo el campo 'fingerprint'."""
    data_to_hash = {k: v for k, v in checkpoint_data.items() if k != "fingerprint"}
    canonical_json = json.dumps(
        data_to_hash,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    digest = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest().lower()
    return f"sha256:{digest}"


class PlanReviewSession:
    """Gestiona el estado en memoria de la sesion de revision y decision del plan."""

    def __init__(
        self,
        now_fn: Optional[Callable[[], datetime]] = None,
        id_generator: Optional[Callable[[str], str]] = None,
        monotonic_time_fn: Optional[Callable[[], float]] = None,
        contracts_override: Optional[Tuple] = None,
    ) -> None:
        self.now_fn = now_fn or (lambda: datetime.now(timezone.utc))
        self.id_generator = id_generator or (lambda prefix: f"{prefix}-{uuid.uuid4().hex[:8]}")
        self.monotonic_time_fn = monotonic_time_fn or time.monotonic
        self.mission = self.brief = self.plan = self.review_metadata = None
        self.events, self.pending_fields, self.errors = [], [], []
        self.approvals, self.approval_history, self.checkpoints = [], [], []
        self.processed_idempotency_keys = {}
        self.next_action = ""
        self._startup_error = None
        try:
            if Draft202012Validator is None or demo_intake.Draft202012Validator is None:
                raise ReviewError("SYSTEM_ERROR", "jsonschema no disponible; no se realizo validacion ni decision.")
            self._load_validators(contracts_override)
            self.start_monotonic = self.monotonic_time_fn()
        except ReviewError as exc:
            self._startup_error = (exc.code, exc.message)
        except FileNotFoundError:
            self._startup_error = ("NOT_FOUND", "Archivo de contrato no encontrado; ensayo detenido.")
        except Exception:
            self._startup_error = ("SYSTEM_ERROR", "No se pudo inicializar o validar los contratos del ensayo.")

    def _load_validators(self, contracts_override):
        if contracts_override is not None:
            (
                self.mission_schema,
                self.event_schema,
                self.error_schema,
                self.approval_schema,
                self.checkpoint_schema,
                self.state_machine,
            ) = copy.deepcopy(contracts_override)
        else:
            (
                self.mission_schema,
                self.event_schema,
                self.error_schema,
                self.approval_schema,
                self.checkpoint_schema,
                self.state_machine,
            ) = load_all_contracts()

        self.format_checker = demo_intake.get_format_checker()
        self.mission_validator = Draft202012Validator(self.mission_schema, format_checker=self.format_checker)
        self.event_validator = Draft202012Validator(self.event_schema, format_checker=self.format_checker)
        self.error_validator = Draft202012Validator(self.error_schema, format_checker=self.format_checker)
        self.approval_validator = Draft202012Validator(self.approval_schema, format_checker=self.format_checker)
        self.checkpoint_validator = Draft202012Validator(self.checkpoint_schema, format_checker=self.format_checker)

        for schema in (self.mission_schema, self.event_schema, self.error_schema,
                       self.approval_schema, self.checkpoint_schema):
            Draft202012Validator.check_schema(schema)

    def _transaction(self, operation, *args, **kwargs):
        if self._startup_error:
            return failure_result(*self._startup_error)
        try:
            draft = copy.copy(self)
            for name in ("mission", "brief", "plan", "events", "pending_fields", "errors",
                         "approvals", "approval_history", "checkpoints", "review_metadata",
                         "processed_idempotency_keys"):
                setattr(draft, name, copy.deepcopy(getattr(self, name)))
            result = getattr(draft, operation)(*args, **kwargs)
            # Preparar incluso la copia de salida antes del unico reemplazo.
            result = copy.deepcopy(result)
            self.__dict__ = draft.__dict__
            return result
        except ReviewError as exc:
            return failure_result(exc.code, exc.message)
        except Exception:
            return failure_result("SYSTEM_ERROR", "Fallo interno o de validacion; operacion no aplicada.")

    def gen_id(self, prefix: str) -> str:
        return self.id_generator(prefix)

    def init_from_intake(
        self,
        fixture_path: Optional[Path | str] = None,
        raw_data: Any = _UNSET,
    ) -> Tuple[int, dict]:
        return self._transaction("_init_from_intake", fixture_path, raw_data)

    def _init_from_intake(self, fixture_path=None, raw_data=_UNSET):
        """Ejecuta el intake inicial y, si es valido en PLAN_EN_REVISION, crea la solicitud de aprobacion."""
        if self.mission is not None or self.approvals:
            raise ReviewError("INVALID_INPUT", "La sesion ya fue inicializada; no admite reapertura.")
        if raw_data is not _UNSET:
            exit_code, intake_env = demo_intake.run_demo_intake(
                fixture_path=fixture_path,
                raw_data=raw_data,
                now_fn=self.now_fn,
                id_generator=self.id_generator,
            )
        else:
            exit_code, intake_env = demo_intake.run_demo_intake(
                fixture_path=fixture_path,
                now_fn=self.now_fn,
                id_generator=self.id_generator,
            )

        self.simulation_status = intake_env.get("simulation_status", "SIMULADA")
        self.mission = copy.deepcopy(intake_env.get("mission"))
        self.brief = copy.deepcopy(intake_env.get("brief"))
        self.plan = copy.deepcopy(intake_env.get("plan"))
        self.events = copy.deepcopy(intake_env.get("events") or [])
        self.pending_fields = copy.deepcopy(intake_env.get("pending_fields") or [])
        self.errors = copy.deepcopy(intake_env.get("errors") or [])
        self.next_action = intake_env.get("next_action", "")

        if exit_code != 0 or not self.mission or self.mission.get("current_state") != "PLAN_EN_REVISION" or not self.plan:
            if exit_code == 0:
                raise ReviewError("SYSTEM_ERROR", "El intake no produjo un plan valido para revision.")
            return exit_code, self.build_envelope()

        self._validate_content()
        self._validate_references()
        if self.errors or self.approvals or self.mission["record_version"] != 3:
            raise ReviewError("INVALID_INPUT", "El intake no corresponde a una solicitud nueva.")

        # Construir y registrar solicitud de aprobacion PENDIENTE
        now_dt = self.now_fn()
        now_iso = now_dt.isoformat()
        expiration_dt = now_dt + timedelta(seconds=APPROVAL_VALIDITY_SECONDS)
        expiration_iso = expiration_dt.isoformat()

        fingerprint = compute_plan_fingerprint(
            mission_id=self.mission["mission_id"],
            user_id=self.mission["user_id"],
            brief_version=self.mission["brief_version"],
            plan_version=self.plan["plan_version"],
            brief=self.brief,
            plan=self.plan,
        )

        approval_id = self.gen_id("APP")
        approval_req = {
            "schema_version": "1.0.0",
            "approval_id": approval_id,
            "user_id": self.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "action_approved": f"Aprobacion del plan v{self.plan['plan_version']} de la mision {self.mission['mission_id']}",
            "version_or_fingerprint": fingerprint,
            "timestamp": now_iso,
            "decision": None,
            "comment": "",
            "conditions": [],
            "expiration": expiration_iso,
            "status": "PENDIENTE",
            "idempotency_key": self.gen_id("IDEMP-APP-REQ"),
        }

        self.approval_validator.validate(approval_req)
        self.approvals = [copy.deepcopy(approval_req)]
        self.approval_history = [copy.deepcopy(approval_req)]

        # Actualizar mision a record_version 4 vinculando approval_ref
        self.mission["approval_refs"].append(approval_id)
        self.mission["record_version"] = 4
        self.mission["updated_at"] = now_iso
        self.mission_validator.validate(self.mission)

        # Evento 4: Registro de solicitud de aprobacion
        req_event = demo_intake.make_event(
            event_id=self.gen_id("EVT-APP-REQ"),
            mission_id=self.mission["mission_id"],
            actor="sistema",
            actor_role="sistema",
            action="solicitud_de_aprobacion",
            timestamp=now_iso,
            version=4,
            previous_state="PLAN_EN_REVISION",
            new_state="PLAN_EN_REVISION",
            result_summary="Solicitud de aprobacion del plan registrada (SIMULADA)",
            idempotency_key=self.gen_id("IDEMP-EVT-REQ"),
            related_approval_id=approval_id,
            source_or_artifact=fingerprint,
        )
        self.event_validator.validate(req_event)
        self.events.append(req_event)

        self.review_metadata = {
            "simulation_status": "SIMULADA",
            "approval_id": approval_id,
            "version_or_fingerprint": fingerprint,
            "identity_scope": "IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA",
            "durable": False,
        }

        self.next_action = "Solicitud de aprobacion PENDIENTE. Esperando decision humana local."
        self._validate_session()
        return 3, self.build_envelope()

    def _validate_policy(self):
        """Politicas declarativas del tramo, con unicidad y booleanos estrictos."""
        def require(ok):
            if not ok:
                raise ReviewError("SYSTEM_ERROR", "Contrato incompatible con la puerta local de decision.")

        def transition(rows, ident, source, target, authority):
            require(isinstance(rows, list))
            matches = [r for r in rows if isinstance(r, dict) and r.get("id") == ident]
            require(len(matches) == 1)
            row = matches[0]
            require(row.get("from") == source and row.get("to") == target and row.get("authority") == authority)
            return row

        lifecycle = self.state_machine["approval_lifecycle"]
        transition(lifecycle["transitions"], "AT-001", "PENDIENTE", "CONSUMIDA", "solo_usuario_humano")
        transition(lifecycle["transitions"], "AT-002", "PENDIENTE", "EXPIRADA", "accion_determinista")
        mt = transition(self.state_machine["mission_transitions"], "MT-005", "PLAN_EN_REVISION",
                        "AUTORIZADA_PARA_EJECUTAR", "solo_usuario_humano")
        require(mt.get("requires_human_approval") is True)
        for state, terminal in (("PENDIENTE", False), ("CONSUMIDA", True), ("EXPIRADA", True)):
            require(lifecycle["states"][state].get("terminal") is terminal)
        require(not any(t.get("from") in ("CONSUMIDA", "EXPIRADA") for t in lifecycle["transitions"]))
        idem = self.state_machine["idempotency_rules"]
        require(idem["same_key_same_content"].get("action") == "no_second_effect")
        require(idem["same_key_different_content"].get("action") == "conflict_rejection")
        require(idem["same_key_different_content"].get("error_code") == "INVALID_INPUT")
        rules = self.state_machine["approval_rules"]
        require(rules.get("actor_role_required") == "usuario_humano")
        require(set(rules["terminal_statuses"]) == {"CONSUMIDA", "EXPIRADA"})
        require(VALID_DECISIONS <= set(rules["valid_decisions"]))
        for decision in ("RECHAZAR", "SOLICITAR_CAMBIOS"):
            require(rules["decision_constraints"][decision].get("comment_required") is True)

    def _validate_content(self):
        """Validacion real del brief, plan y su pertenencia a la misma mision."""
        if any(obj is None for obj in (self.mission, self.brief, self.plan)):
            raise ReviewError("NOT_FOUND", "Falta mision, brief o plan de la sesion.")
        self.mission_validator.validate(self.mission)
        m, b, p = self.mission, self.brief, self.plan
        if not isinstance(b, dict) or not isinstance(p, dict):
            raise ReviewError("INVALID_INPUT", "Brief o plan invalido.")
        if (set(b) != {"simulation_status", "user_id", "title", "objective", "context",
                      "expected_result", "constraints", "assumptions", "pending_decisions"} or
                set(p) != {"simulation_status", "mission_id", "brief_version", "plan_version", "title", "tasks", "risks"}):
            raise ReviewError("INVALID_INPUT", "Campos incompatibles en brief o plan.")
        if b["user_id"] != m["user_id"]:
            raise ReviewError("PERMISSION_DENIED", "El brief pertenece a otro usuario.")
        if (p["mission_id"] != m["mission_id"] or type(m["brief_version"]) is not int or
                m["brief_version"] != 1 or type(p["brief_version"]) is not int or p["brief_version"] != 1 or
                type(p["plan_version"]) is not int or p["plan_version"] != 1 or
                b["simulation_status"] != "SIMULADA" or p["simulation_status"] != "SIMULADA"):
            raise ReviewError("INVALID_INPUT", "IDs, versiones o etiquetas de simulacion incompatibles.")
        template = {k: p[k] for k in ("title", "tasks", "risks")}
        raw = dict(b, plan_template=template)
        valid, errors = demo_intake.validate_raw_fixture_data(raw)
        if errors or valid is None or any(demo_intake.evaluate_brief_fields(valid)):
            raise ReviewError("INVALID_INPUT", "El brief no es valido y completo para decidir.")
        valid_plan, errors = demo_intake.validate_plan_template(template)
        if errors or valid_plan is None:
            raise ReviewError("INVALID_INPUT", "La estructura del plan vigente no es valida.")
        title = b["title"] if b["title"].startswith("[SIMULADA]") else "[SIMULADA] " + b["title"]
        if (m["title"] != title or self.pending_fields or m["active_task"] is not None or
                m["resumable_state"] is not None or any(m["counters"].values())):
            raise ReviewError("INVALID_INPUT", "La mision no corresponde al ensayo pendiente sin ejecucion.")

    def _validate_references(self):
        """RI-001, RI-002 y RI-003 se resuelven contra los registros de esta sesion."""
        m = self.mission
        for app in self.approvals:
            self.approval_validator.validate(app)
        for cp in self.checkpoints:
            self.checkpoint_validator.validate(cp)
        approvals = {a["approval_id"]: a for a in self.approvals}
        checkpoints = {c["checkpoint_id"]: c for c in self.checkpoints}
        if len(approvals) != len(self.approvals) or len(checkpoints) != len(self.checkpoints):
            raise ReviewError("INVALID_INPUT", "Identificadores de registros duplicados.")
        if any(ref not in approvals for ref in m["approval_refs"]):
            raise ReviewError("NOT_FOUND", "RI-001: referencia de aprobacion inexistente.")
        if m["last_checkpoint_id"] is not None and m["last_checkpoint_id"] not in checkpoints:
            raise ReviewError("NOT_FOUND", "RI-002: referencia de checkpoint inexistente.")
        for app in self.approvals:
            if app["user_id"] != m["user_id"]:
                raise ReviewError("PERMISSION_DENIED", "La solicitud pertenece a otro usuario.")
        for cp in self.checkpoints:
            if any(ref not in approvals for ref in cp["authorizations"]):
                raise ReviewError("NOT_FOUND", "RI-003: autorizacion del checkpoint inexistente.")
            if (cp["mission_id"] != m["mission_id"] or cp["checkpoint_id"] != m["last_checkpoint_id"] or
                    cp["mission_version"] != m["record_version"] or cp["state"] != m["current_state"]):
                raise ReviewError("INVALID_INPUT", "Checkpoint cruzado o incompatible con la mision.")
            if cp["artifacts"] != ["brief", "plan"] or self.brief is None or self.plan is None:
                raise ReviewError("NOT_FOUND", "Artefactos del checkpoint no resolubles.")
            if cp["authorizations"] != m["approval_refs"] or not cp["authorizations"]:
                raise ReviewError("INVALID_INPUT", "Checkpoint sin autorizacion correspondiente.")
            for ref in cp["authorizations"]:
                if approvals[ref]["status"] != "CONSUMIDA" or approvals[ref]["decision"] != "APROBAR":
                    raise ReviewError("INVALID_INPUT", "Checkpoint sin aprobacion consumida valida.")
            expected_tasks = [{"task_id": t["task_id"], "state": "PENDIENTE", "attempts": 0} for t in self.plan["tasks"]]
            expected_deps = [{"from_task": ref, "to_task": t["task_id"], "satisfied": False}
                             for t in self.plan["tasks"] for ref in t["dependencies"]]
            if (cp["tasks"] != expected_tasks or cp["dependencies"] != expected_deps or
                    cp["attempts"] != m["counters"] or cp["budgets_consumed"]["budget_usd_spent"] != 0 or
                    not math.isfinite(cp["budgets_consumed"]["elapsed_mission_seconds"]) or
                    cp["resumable_state"] is not None or cp["fingerprint"] != compute_checkpoint_fingerprint(cp)):
                raise ReviewError("INVALID_INPUT", "Contenido o huella del checkpoint incompatible.")

    def _validate_session(self):
        self._validate_content()
        self._validate_references()
        m = self.mission
        if len(self.approvals) != 1:
            raise ReviewError("NOT_FOUND", "No existe una solicitud unica vigente.")
        app = self.approvals[0]
        if m["approval_refs"] != [app["approval_id"]]:
            raise ReviewError("NOT_FOUND", "La solicitud no esta vinculada a la mision.")
        for old in self.approval_history:
            self.approval_validator.validate(old)
        if not self.approval_history:
            raise ReviewError("NOT_FOUND", "Falta el registro original de la solicitud.")
        original = self.approval_history[0]
        fingerprint = compute_plan_fingerprint(m["mission_id"], m["user_id"], m["brief_version"],
                                               self.plan["plan_version"], self.brief, self.plan)
        expected_metadata = {"simulation_status": "SIMULADA", "approval_id": app["approval_id"],
                             "version_or_fingerprint": fingerprint,
                             "identity_scope": "IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA", "durable": False}
        if (self.review_metadata != expected_metadata or app["version_or_fingerprint"] != fingerprint or
                app["actor"] != "usuario_local_demo" or app["actor_role"] != "usuario_humano" or
                app["action_approved"] != f"Aprobacion del plan v1 de la mision {m['mission_id']}"):
            raise ReviewError("INVALID_INPUT", "Solicitud, huella o metadatos no corresponden al contenido vigente.")
        immutable = set(app) - {"timestamp", "status", "decision", "comment"}
        if (any(app[k] != original[k] for k in immutable) or original["status"] != "PENDIENTE" or
                original["decision"] is not None or original["comment"] != "" or original["conditions"] != [] or
                datetime.fromisoformat(original["expiration"]) - datetime.fromisoformat(original["timestamp"]) !=
                timedelta(seconds=APPROVAL_VALIDITY_SECONDS)):
            raise ReviewError("INVALID_INPUT", "La identidad o vigencia de la solicitud original fue alterada.")
        pending = app["status"] == "PENDIENTE"
        approved = app["status"] == "CONSUMIDA" and app["decision"] == "APROBAR"
        expected_state = "AUTORIZADA_PARA_EJECUTAR" if approved else "PLAN_EN_REVISION"
        expected_history = [original] if pending else [original, app]
        if (m["current_state"] != expected_state or m["record_version"] != (4 if pending else 5) or
                self.approval_history != expected_history or (pending and app != original) or
                len(self.checkpoints) != (1 if approved else 0) or
                (not approved and m["last_checkpoint_id"] is not None)):
            raise ReviewError("INVALID_INPUT", "Estado, version o historia incompatible con la solicitud.")
        if len(self.events) != m["record_version"]:
            raise ReviewError("INVALID_INPUT", "Historia de eventos incompleta.")
        seen = set()
        previous = None
        for version, event in enumerate(self.events, 1):
            self.event_validator.validate(event)
            if (event["event_id"] in seen or event["mission_id"] != m["mission_id"] or
                    event["version"] != version or event["previous_state"] != previous or event["task_id"] is not None):
                raise ReviewError("INVALID_INPUT", "Evento duplicado o cruzado con otra mision.")
            if event["related_approval_id"] is not None and event["related_approval_id"] != app["approval_id"]:
                raise ReviewError("NOT_FOUND", "Referencia de aprobacion de evento no resoluble.")
            if version >= 4 and (event["related_approval_id"] != app["approval_id"] or event["source_or_artifact"] != fingerprint):
                raise ReviewError("INVALID_INPUT", "Evento sin correspondencia con la solicitud y su huella.")
            seen.add(event["event_id"])
            previous = event["new_state"]
        if previous != expected_state:
            raise ReviewError("INVALID_INPUT", "Estado final sin evento correspondiente.")

    def process_decision(self, command: Any, actor_context: Any) -> Tuple[int, dict]:
        return self._transaction("_process_decision", command, actor_context)

    def _process_decision(
        self,
        command: Any,
        actor_context: Any,
    ) -> Tuple[int, dict]:
        """Procesa una decision humana sobre la solicitud de aprobacion en memoria."""
        if not isinstance(command, dict) or set(command) != ALLOWED_COMMAND_KEYS:
            raise ReviewError("INVALID_INPUT", "El comando debe contener exactamente los cinco campos obligatorios.")
        for key, value in command.items():
            if not isinstance(value, str) or len(value) > 4000 or (key != "comment" and not value.strip()):
                raise ReviewError("INVALID_INPUT", "Los campos del comando deben ser cadenas validas de hasta 4000 caracteres.")
        decision, comment = command["decision"], command["comment"]
        if decision not in VALID_DECISIONS or (decision != "APROBAR" and not comment.strip()):
            raise ReviewError("INVALID_INPUT", "Decision no admitida o motivo obligatorio ausente.")
        if (not isinstance(actor_context, dict) or actor_context.get("actor_role") != "usuario_humano" or
                actor_context.get("actor") != "usuario_local_demo" or
                actor_context.get("source") != "terminal_local_autorizada" or
                not self.mission or actor_context.get("user_id") != self.mission.get("user_id")):
            raise ReviewError("PERMISSION_DENIED", "Contexto local no autorizado o usuario ajeno a la mision.")
        self._validate_policy()
        self._validate_session()
        current_app = self.approvals[0]
        if command["approval_id"] != current_app["approval_id"]:
            raise ReviewError("NOT_FOUND", "La solicitud indicada no pertenece a esta sesion.")
        idemp_key = command["idempotency_key"]
        if command["version_or_fingerprint"] != current_app["version_or_fingerprint"]:
            raise ReviewError("INVALID_INPUT", "La huella del comando no coincide con el contenido vigente.")
        current_fingerprint = current_app["version_or_fingerprint"]
        if idemp_key != current_app["idempotency_key"]:
            code = "PERMISSION_DENIED" if current_app["status"] != "PENDIENTE" else "INVALID_INPUT"
            raise ReviewError(code, "La clave no corresponde a la solicitud de esta sesion.")
        if idemp_key in self.processed_idempotency_keys:
            recorded = self.processed_idempotency_keys[idemp_key]
            if recorded["command"] != command or recorded["actor_context"] != actor_context:
                raise ReviewError("INVALID_INPUT", "Conflicto de idempotencia: contenido o contexto diferente.")
            if recorded["envelope"] != self.build_envelope() or current_app["status"] != "CONSUMIDA":
                raise ReviewError("INVALID_INPUT", "El resultado previo no corresponde al estado vigente.")
            return recorded["exit_code"], copy.deepcopy(recorded["envelope"])
        if current_app["status"] != "PENDIENTE":
            raise ReviewError("PERMISSION_DENIED", "La solicitud es terminal; no admite otra respuesta.")

        now_dt = self.now_fn()
        now_iso = now_dt.isoformat()

        # 8. Verificar expiracion (AT-002)
        exp_dt = datetime.fromisoformat(current_app["expiration"])
        if now_dt >= exp_dt:
            # Transicion AT-002: PENDIENTE -> EXPIRADA
            current_app["status"] = "EXPIRADA"
            current_app["decision"] = None
            current_app["timestamp"] = now_iso
            self.approval_validator.validate(current_app)
            self.approval_history.append(copy.deepcopy(current_app))

            self.mission["record_version"] = 5
            self.mission["updated_at"] = now_iso
            self.mission_validator.validate(self.mission)

            exp_event = demo_intake.make_event(
                event_id=self.gen_id("EVT-APP-EXP"),
                mission_id=self.mission["mission_id"],
                actor="sistema",
                actor_role="sistema",
                action="expiracion_de_solicitud",
                timestamp=now_iso,
                version=5,
                previous_state="PLAN_EN_REVISION",
                new_state="PLAN_EN_REVISION",
                result_summary="Solicitud de aprobacion expirada tras superar plazo de validez (SIMULADA)",
                idempotency_key=self.gen_id("IDEMP-EVT-EXP"),
                related_approval_id=current_app["approval_id"],
                source_or_artifact=current_fingerprint,
            )
            self.event_validator.validate(exp_event)
            self.events.append(exp_event)

            err = demo_intake.make_error_payload(
                "PERMISSION_DENIED",
                f"La solicitud '{current_app['approval_id']}' expiro en {current_app['expiration']}.",
            )
            self.error_validator.validate(err)
            self.errors.append(err)
            self.next_action = "Solicitud expirada. No se autoriza el plan."
            self._validate_session()
            return 1, self.build_envelope()

        # Preparar copias para actualizacion atomica
        new_app = copy.deepcopy(current_app)
        new_mission = copy.deepcopy(self.mission)
        new_events = copy.deepcopy(self.events)

        new_app["status"] = "CONSUMIDA"
        new_app["decision"] = decision
        new_app["comment"] = comment
        new_app["timestamp"] = now_iso
        self.approval_validator.validate(new_app)

        if decision == "APROBAR":
            new_mission["current_state"] = "AUTORIZADA_PARA_EJECUTAR"
            new_mission["record_version"] = 5
            new_mission["updated_at"] = now_iso

            # Evento 5: Decision de aprobacion
            decision_event = demo_intake.make_event(
                event_id=self.gen_id("EVT-APP-DECISION"),
                mission_id=new_mission["mission_id"],
                actor=actor_context.get("actor", "usuario_local_demo"),
                actor_role="usuario_humano",
                action="aprobacion_del_plan",
                timestamp=now_iso,
                version=5,
                previous_state="PLAN_EN_REVISION",
                new_state="AUTORIZADA_PARA_EJECUTAR",
                result_summary="Plan SIMULADA autorizado por decision local explicita. No ejecutado; sesion no persistida.",
                idempotency_key=idemp_key,
                related_approval_id=new_app["approval_id"],
                source_or_artifact=current_fingerprint,
            )
            self.event_validator.validate(decision_event)
            new_events.append(decision_event)

            # Construir grafo de dependencias de tareas
            dep_graph = []
            for idx, t in enumerate(self.plan["tasks"]):
                if idx > 0:
                    prev_id = self.plan["tasks"][idx - 1]["task_id"]
                    curr_id = t["task_id"]
                    dep_graph.append({
                        "from_task": prev_id,
                        "to_task": curr_id,
                        "satisfied": False,
                    })

            # Construir Checkpoint efimero en memoria
            elapsed = self.monotonic_time_fn() - self.start_monotonic
            if not math.isfinite(elapsed) or elapsed < 0:
                raise ReviewError("SYSTEM_ERROR", "Duracion monotona invalida; operacion no aplicada.")
            checkpoint_id = self.gen_id("CHK")
            checkpoint_data = {
                "schema_version": "1.0.0",
                "checkpoint_id": checkpoint_id,
                "mission_id": new_mission["mission_id"],
                "mission_version": 5,
                "state": "AUTORIZADA_PARA_EJECUTAR",
                "resumable_state": None,
                "tasks": [
                    {
                        "task_id": t["task_id"],
                        "state": "PENDIENTE",
                        "attempts": 0,
                    }
                    for t in self.plan["tasks"]
                ],
                "dependencies": dep_graph,
                "attempts": {
                    "clarification_cycles": new_mission["counters"]["clarification_cycles"],
                    "task_reasoning_attempts": new_mission["counters"]["task_reasoning_attempts"],
                    "transient_retries": new_mission["counters"]["transient_retries"],
                    "vbp_correction_rounds": new_mission["counters"]["vbp_correction_rounds"],
                    "agent_requests": new_mission["counters"]["agent_requests"],
                },
                "budgets_consumed": {
                    "elapsed_mission_seconds": float(elapsed),
                    "budget_usd_spent": 0.0,
                },
                "artifacts": ["brief", "plan"],
                "authorizations": [new_app["approval_id"]],
                "timestamp": now_iso,
                "idempotency_key": self.gen_id("IDEMP-CHK"),
            }
            chk_fingerprint = compute_checkpoint_fingerprint(checkpoint_data)
            checkpoint_data["fingerprint"] = chk_fingerprint

            self.checkpoint_validator.validate(checkpoint_data)

            # Vincular checkpoint en mision
            new_mission["last_checkpoint_id"] = checkpoint_id
            self.mission_validator.validate(new_mission)

            # Commit atomico
            self.approvals = [new_app]
            self.approval_history.append(copy.deepcopy(new_app))
            self.mission = new_mission
            self.events = new_events
            self.checkpoints = [checkpoint_data]
            self.next_action = "Plan SIMULADA autorizado por decision local explicita. No ejecutado; sesion no persistida."
            exit_code = 0

        else:
            # RECHAZAR o SOLICITAR_CAMBIOS: la mision permanece en PLAN_EN_REVISION
            new_mission["record_version"] = 5
            new_mission["updated_at"] = now_iso
            self.mission_validator.validate(new_mission)

            action_name = "rechazo_del_plan" if decision == "RECHAZAR" else "solicitud_de_cambios_al_plan"
            summary_text = (
                f"Decision {decision} registrada con motivo: '{comment}'. Plan no autorizado (SIMULADA)."
            )

            decision_event = demo_intake.make_event(
                event_id=self.gen_id("EVT-APP-DECISION"),
                mission_id=new_mission["mission_id"],
                actor=actor_context.get("actor", "usuario_local_demo"),
                actor_role="usuario_humano",
                action=action_name,
                timestamp=now_iso,
                version=5,
                previous_state="PLAN_EN_REVISION",
                new_state="PLAN_EN_REVISION",
                result_summary=summary_text,
                idempotency_key=idemp_key,
                related_approval_id=new_app["approval_id"],
                source_or_artifact=current_fingerprint,
            )
            self.event_validator.validate(decision_event)
            new_events.append(decision_event)

            # Commit atomico
            self.approvals = [new_app]
            self.approval_history.append(copy.deepcopy(new_app))
            self.mission = new_mission
            self.events = new_events
            self.checkpoints = []
            self.next_action = f"Plan no autorizado (decision: {decision}). Revision fuera de alcance de este ensayo."
            exit_code = 3

        self._validate_session()
        final_env = self.build_envelope()
        self.processed_idempotency_keys[idemp_key] = {
            "command": copy.deepcopy(command),
            "actor_context": copy.deepcopy(actor_context),
            "exit_code": exit_code,
            "envelope": copy.deepcopy(final_env),
        }
        return exit_code, final_env

    def build_envelope(self) -> dict:
        """Construye el sobre de salida completo de la sesion."""
        return {
            "simulation_status": "SIMULADA",
            "mission": copy.deepcopy(self.mission),
            "brief": copy.deepcopy(self.brief),
            "plan": copy.deepcopy(self.plan),
            "events": copy.deepcopy(self.events),
            "pending_fields": copy.deepcopy(self.pending_fields),
            "errors": copy.deepcopy(self.errors),
            "next_action": self.next_action,
            "approvals": copy.deepcopy(self.approvals),
            "approval_history": copy.deepcopy(self.approval_history),
            "checkpoints": copy.deepcopy(self.checkpoints),
            "review": copy.deepcopy(self.review_metadata),
        }


def _sanitize_for_terminal(text: str) -> str:
    """Escapa caracteres de control de terminal para impresion segura en stderr."""
    return re.sub(r"[\x00-\x1f\x7f-\x9f]", lambda m: f"\\x{ord(m.group(0)):02x}", text)


def run_interactive_cli(session: PlanReviewSession) -> Tuple[int, dict]:
    """Frontera controlada de terminal; no publica un resultado parcial."""
    if session._startup_error:
        return failure_result(*session._startup_error)
    try:
        session._validate_session()
        return _run_interactive_cli(session)
    except ReviewError as exc:
        return failure_result(exc.code, exc.message)
    except Exception:
        return failure_result("SYSTEM_ERROR", "Fallo de terminal; no se aplico una decision.")


def _run_interactive_cli(session: PlanReviewSession) -> Tuple[int, dict]:
    """Maneja el flujo interactivo de decision en terminal de forma segura."""
    if not sys.stdin.isatty() or not sys.stderr.isatty():
        err = demo_intake.make_error_payload(
            "PERMISSION_DENIED",
            "El modo interactivo requiere una terminal interactiva TTY en stdin y stderr.",
        )
        session.error_validator.validate(err)
        session.errors.append(err)
        session.next_action = "Ejecutar en una terminal interactiva TTY para responder."
        return 1, session.build_envelope()

    app_req = session.approvals[0]
    fp = app_req["version_or_fingerprint"]
    app_id = app_req["approval_id"]

    # Mostrar contexto completo en stderr
    sys.stderr.write("=" * 70 + "\n")
    sys.stderr.write("[SIMULADA] OminAI HQ - REVISION LOCAL DE PLAN DE MISION\n")
    sys.stderr.write("ADVERTENCIA: Este es un ensayo SIMULADA. Ninguna tarea sera ejecutada.\n")
    sys.stderr.write(f"IDENTIDAD: {session.review_metadata['identity_scope']} (usuario_local_demo)\n")
    sys.stderr.write("=" * 70 + "\n")
    for label, record in (("Mision", session.mission), ("Brief completo", session.brief), ("Plan completo", session.plan)):
        sys.stderr.write(label + ":\n")
        sys.stderr.write(_sanitize_for_terminal(json.dumps(record, ensure_ascii=True, allow_nan=False)) + "\n")
    sys.stderr.write("-" * 70 + "\n")
    sys.stderr.write(f"Solicitud ID:   {_sanitize_for_terminal(app_id)}\n")
    sys.stderr.write(f"Huella exacta:  {_sanitize_for_terminal(fp)}\n")
    sys.stderr.write(f"Expiracion:     {_sanitize_for_terminal(app_req['expiration'])}\n")
    sys.stderr.write("=" * 70 + "\n")
    sys.stderr.write("Opciones admitidas:\n")
    sys.stderr.write(f"  APROBAR {fp}\n")
    sys.stderr.write(f"  RECHAZAR {fp}\n")
    sys.stderr.write(f"  SOLICITAR_CAMBIOS {fp}\n")
    sys.stderr.write("  SALIR\n")
    sys.stderr.write("=" * 70 + "\n")
    sys.stderr.write("Ingrese su decision > ")
    sys.stderr.flush()

    try:
        raw_line = sys.stdin.readline(MAX_LINE_LENGTH + 1)
    except (KeyboardInterrupt, EOFError):
        sys.stderr.write("\nInterrupcion recibida. Saliendo sin decision.\n")
        session.next_action = "Interrupcion de usuario. Solicitud permanece PENDIENTE."
        return 3, session.build_envelope()

    if not raw_line:
        # EOF
        session.next_action = "Fin de entrada (EOF). Solicitud permanece PENDIENTE."
        return 3, session.build_envelope()

    if len(raw_line) > MAX_LINE_LENGTH:
        err = demo_intake.make_error_payload(
            "INVALID_INPUT",
            f"Linea de entrada excede el limite maximo de {MAX_LINE_LENGTH} caracteres.",
        )
        session.error_validator.validate(err)
        session.errors.append(err)
        return 1, session.build_envelope()

    line = raw_line.strip()
    if line == "SALIR":
        sys.stderr.write("Saliendo sin emitir decision.\n")
        session.next_action = "Operacion cancelada por usuario. Solicitud permanece PENDIENTE."
        return 3, session.build_envelope()

    parts = line.split(maxsplit=1)
    decision_verb = parts[0] if parts else ""
    provided_fp = parts[1].strip() if len(parts) > 1 else ""

    if decision_verb not in VALID_DECISIONS:
        err = demo_intake.make_error_payload(
            "INVALID_INPUT",
            "Comando no reconocido. Debe ser APROBAR, RECHAZAR, SOLICITAR_CAMBIOS o SALIR.",
        )
        session.error_validator.validate(err)
        session.errors.append(err)
        return 1, session.build_envelope()

    comment = ""
    if decision_verb in ["RECHAZAR", "SOLICITAR_CAMBIOS"]:
        sys.stderr.write(f"Ingrese motivo para {decision_verb} > ")
        sys.stderr.flush()
        try:
            raw_comment = sys.stdin.readline(MAX_LINE_LENGTH + 1)
        except (KeyboardInterrupt, EOFError):
            session.next_action = "Interrupcion al solicitar motivo. Solicitud permanece PENDIENTE."
            return 3, session.build_envelope()

        if not raw_comment:
            session.next_action = "Fin de entrada al solicitar motivo. Solicitud permanece PENDIENTE."
            return 3, session.build_envelope()
        if len(raw_comment) > MAX_LINE_LENGTH:
            err = demo_intake.make_error_payload(
                "INVALID_INPUT",
                f"Linea de motivo excede el limite de {MAX_LINE_LENGTH} caracteres.",
            )
            session.error_validator.validate(err)
            session.errors.append(err)
            return 1, session.build_envelope()
        comment = raw_comment.rstrip("\r\n")

    command = {
        "approval_id": app_id,
        "version_or_fingerprint": provided_fp,
        "decision": decision_verb,
        "comment": comment,
        "idempotency_key": app_req["idempotency_key"],
    }

    actor_context = {
        "user_id": session.mission["user_id"],
        "actor": "usuario_local_demo",
        "actor_role": "usuario_humano",
        "source": "terminal_local_autorizada",
        "identity_scope": "IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA",
    }

    return session.process_decision(command, actor_context)


def main(argv: Optional[List[str]] = None) -> int:
    """Punto de entrada CLI para la revision y decision del plan."""
    args = argv if argv is not None else sys.argv[1:]
    try:
        if args not in ([], ["--interactive"]):
            raise ReviewError("INVALID_INPUT", "Argumentos no admitidos; solo se permite --interactive.")
        session = PlanReviewSession()
        exit_code, envelope = session.init_from_intake()
        if args and exit_code == 3 and session.approvals:
            exit_code, envelope = run_interactive_cli(session)
        output = json.dumps(envelope, indent=2, ensure_ascii=True, allow_nan=False)
    except ReviewError as exc:
        exit_code, envelope = failure_result(exc.code, exc.message)
        output = json.dumps(envelope, ensure_ascii=True)
    except Exception:
        exit_code, envelope = failure_result("SYSTEM_ERROR", "Fallo interno del ensayo; no se publico resultado valido.")
        output = json.dumps(envelope, ensure_ascii=True)
    sys.stdout.write(output + "\n")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
