"""Adaptador real ADK 2.8.0 para una sola generacion Gemini sin herramientas."""

from importlib import metadata, util
import os
from typing import Any, Callable, Dict, Iterable, Optional
import uuid

import app.agent_gateway as agent_gateway


ADK_VERSION = "2.8.0"
REAL_MODEL = "gemini-3.5-flash"


def _field(value: Any, name: str, default=None):
    if isinstance(value, dict):
        return value.get(name, default)
    return getattr(value, name, default)


def _exception_status(exc: Exception) -> int:
    """Extrae solo un estado HTTP seguro sin propagar texto del proveedor."""
    candidates = (
        getattr(exc, "status_code", None),
        getattr(exc, "code", None),
        getattr(getattr(exc, "response", None), "status_code", None),
    )
    for candidate in candidates:
        try:
            candidate = candidate() if callable(candidate) else candidate
            status = int(candidate)
        except (TypeError, ValueError):
            continue
        if 400 <= status <= 599:
            return status
    return 500


class ADKModelClientProvider(agent_gateway.ModelClientProvider):
    """Ejecuta un ``Agent`` mediante ``InMemoryRunner`` de Google ADK."""

    provider_kind = "ADK_REAL"

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_model: str = REAL_MODEL,
        mode: str = "REAL",
        *,
        executor: Optional[Callable[..., Iterable[Any]]] = None,
    ) -> None:
        self.api_key = (
            api_key
            or os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
        )
        self.default_model = default_model
        self.mode = mode
        self._executor = executor
        if mode != "REAL":
            raise ValueError("ADKModelClientProvider solo admite modo REAL.")
        if not self.api_key:
            raise ValueError(
                "Credencial requerida para modo REAL; fallback a mock prohibido."
            )

    def has_credentials(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    def preflight(self):
        """Comprueba el paquete fijado sin importar ni iniciar el SDK."""
        if self._executor is not None:
            return True, None
        try:
            if util.find_spec("google.adk") is None:
                return False, "google-adk no esta disponible en el entorno."
            installed = metadata.version("google-adk")
        except (ImportError, ModuleNotFoundError, metadata.PackageNotFoundError):
            return False, "google-adk no esta disponible en el entorno."
        if installed != ADK_VERSION:
            return False, "La version instalada de google-adk no coincide con el pin."
        return True, None

    @staticmethod
    def _run_adk(
        *,
        api_key: str,
        model_name: str,
        system_instruction: str,
        prompt: str,
        timeout_seconds: int,
        max_output_tokens: int,
        response_schema: Dict[str, Any],
    ):
        """Construye el cliente y runtime ADK; no contiene fallback REST."""
        from google import genai
        from google.adk.agents import Agent, RunConfig
        from google.adk.models import Gemini
        from google.adk.runners import InMemoryRunner
        from google.genai import types

        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=timeout_seconds * 1000,
                retry_options=None,
            ),
        )
        model = Gemini(model=model_name, client=client, retry_options=None)
        agent = Agent(
            name="ominai_hq_single_call",
            model=model,
            instruction=system_instruction,
            tools=[],
            output_schema=response_schema,
            include_contents="none",
            mode="single_turn",
            generate_content_config=types.GenerateContentConfig(
                max_output_tokens=max_output_tokens,
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )
        app_name = "ominai_hq_adk"
        user_id = "runtime_user"
        session_id = "adk-" + uuid.uuid4().hex
        runner = InMemoryRunner(agent=agent, app_name=app_name)
        runner.session_service.create_session_sync(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
        )
        content = types.Content(
            role="user", parts=[types.Part.from_text(text=prompt)]
        )
        return runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
            run_config=RunConfig(max_llm_calls=1),
        )

    @staticmethod
    def _normalize_events(events: Iterable[Any]) -> agent_gateway.ModelCallResponse:
        final_text = None
        usage = None
        provider_error = False
        tool_action = False
        for event in events:
            event_usage = _field(event, "usage_metadata")
            if event_usage is not None:
                usage = event_usage
            if _field(event, "error_code"):
                provider_error = True
            get_calls = getattr(event, "get_function_calls", None)
            if callable(get_calls) and get_calls():
                tool_action = True
            is_final = getattr(event, "is_final_response", None)
            if callable(is_final) and not is_final():
                continue
            content = _field(event, "content")
            parts = _field(content, "parts", []) if content is not None else []
            texts = []
            for part in parts or []:
                if _field(part, "function_call") is not None:
                    tool_action = True
                if not _field(part, "thought", False) and _field(part, "text"):
                    texts.append(_field(part, "text"))
            if texts:
                final_text = "".join(texts)

        if usage is None:
            return agent_gateway.ModelCallResponse(
                "", 0, 0, status_code=502, usage_confirmed=False
            )
        prompt_tokens = _field(usage, "prompt_token_count")
        candidate_tokens = _field(usage, "candidates_token_count")
        thought_tokens = _field(usage, "thoughts_token_count", 0) or 0
        tool_tokens = _field(usage, "tool_use_prompt_token_count", 0) or 0
        counts = (prompt_tokens, candidate_tokens, thought_tokens, tool_tokens)
        if any(type(value) is not int or value < 0 for value in counts):
            return agent_gateway.ModelCallResponse(
                "", 0, 0, status_code=502, usage_confirmed=False
            )
        if tool_action or tool_tokens:
            return agent_gateway.ModelCallResponse(
                "", prompt_tokens, candidate_tokens + thought_tokens, status_code=422
            )
        if provider_error or final_text is None:
            return agent_gateway.ModelCallResponse(
                "", prompt_tokens, candidate_tokens + thought_tokens, status_code=502
            )
        return agent_gateway.ModelCallResponse(
            final_text,
            prompt_tokens,
            candidate_tokens + thought_tokens,
            status_code=200,
        )

    def call_model(
        self,
        model_name: str,
        system_instruction: str,
        prompt: str,
        timeout_seconds: int = 45,
        *,
        max_output_tokens: int = 4096,
        response_schema: Optional[Dict[str, Any]] = None,
    ) -> agent_gateway.ModelCallResponse:
        if model_name != self.default_model or model_name != REAL_MODEL:
            return agent_gateway.ModelCallResponse(
                "", 0, 0, status_code=403, error_message="Modelo no permitido."
            )
        if not 1 <= timeout_seconds <= 45 or not 1 <= max_output_tokens <= 4096:
            return agent_gateway.ModelCallResponse(
                "", 0, 0, status_code=400, error_message="Limites invalidos."
            )
        if not isinstance(response_schema, dict):
            return agent_gateway.ModelCallResponse(
                "", 0, 0, status_code=400, error_message="Esquema requerido."
            )
        ready, _ = self.preflight()
        if not ready:
            return agent_gateway.ModelCallResponse(
                "", 0, 0, status_code=503, usage_confirmed=True
            )
        executor = self._executor or self._run_adk
        try:
            events = executor(
                api_key=self.api_key,
                model_name=model_name,
                system_instruction=system_instruction,
                prompt=prompt,
                timeout_seconds=timeout_seconds,
                max_output_tokens=max_output_tokens,
                response_schema=response_schema,
            )
            return self._normalize_events(events)
        except Exception as exc:
            status = _exception_status(exc)
            return agent_gateway.ModelCallResponse(
                "",
                0,
                0,
                status_code=status,
                is_transient=status in (408, 429, 500, 502, 503, 504),
                usage_confirmed=False,
            )
