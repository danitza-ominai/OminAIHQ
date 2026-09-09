"""REAL-02 – Composicion segura de ejecucion real para OminAI HQ.

Componente de producto: RealExecutionComposition.

Construye y mantiene la conexion entre los cuatro componentes requeridos
para ejecutar una llamada real vinculada a una mision y tarea aprobadas:
  - AgentGateway (con modo REAL y perfil validado)
  - ADKModelClientProvider (sin fallback simulado)
  - LocalApprovalRecordValidator (autoridad persistida de REAL-01)
  - RepositoryDurableCallStore (idempotencia persistida de REAL-01)

Responsabilidades de este modulo:
  1. Exigir repositorio explicito en archivo (no :memory:), perfil REAL
     validado y contexto humano verificado por HumanApprovalEngine.
  2. Derivar propietario y aprobacion de los registros persistidos de la
     mision; nunca aceptarlos como autoridad desde parametros libres.
  3. Componer los cuatro componentes con el mismo repositorio.
  4. Ofrecer execute_task() para que futuros especialistas de confianza
     puedan solicitar una llamada sin reconstruir estos controles.
  5. Revalidar el contexto y la autoridad en cada llamada, aunque la
     instancia se haya creado antes de una cancelacion del plan.
  6. Delegar adquisicion, reservas y resultado terminal a los componentes
     existentes de REAL-01 y AgentGateway; no anadir contadores paralelos.
  7. Configurar cero reintentos automaticos.
  8. Devolver resultado o error estructurado sin alterar estados de mision,
     API ni pantalla.
  9. Ante resultado incierto, conservar el bloqueo; no limpiar registros.
 10. No mantener una transaccion SQLite abierta durante la llamada al proveedor.
 11. Documentar aqui como el futuro runtime consumira resultado/error.

Consumo del resultado por el runtime futuro (doc obligatorio):
  La tupla (ok, result, error) sigue el mismo protocolo que AgentGateway:
  - ok=True, result contiene el dict del modelo mas 'execution_evidence',
    'cost_kind' y 'cost_usd'. Nunca interpreta el result como tarea
    completada, evidencia validada ni VBP aprobado.
  - ok=False, error contiene 'error_code', 'message', 'retry_allowed'.
    Si error_code es SYSTEM_ERROR o PERMISSION_DENIED con result incierto,
    el runtime no debe reintentar ni limpiar el registro; debe conservar el
    bloqueo y la reserva para auditoria posterior.
  El runtime futuro actualizara el estado de la mision y la tarea solo
  despues de validar el mandato de resultado con el CoordinatorAgent; esa
  logica esta fuera del alcance de REAL-02.

Restricciones:
  - Requiere db_path != ':memory:' y que el archivo exista o pueda crearse.
  - No crea la base, el perfil, las aprobaciones ni el plan.
  - No declara compatibilidad con Firestore ni con cloud.
  - ADKModelClientProvider es el unico proveedor de producto aceptado;
    los dobles solo pueden inyectarse mediante _provider_override en pruebas
    y no hay opcion HTTP, ambiental ni de configuracion que los active.
  - max_retries=0 fijo; no se pueden ampliar los limites de REAL-01.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from app.agent_gateway import AgentGateway, ValidatedRealExecutionMandate
from app.adk_provider import ADKModelClientProvider, REAL_MODEL
from app.durable_call_store import RepositoryDurableCallStore
from app.real_execution_authority import LocalApprovalRecordValidator
from app.runtime_config import REAL_MODE, RuntimeConfig, REAL_MODEL_PRICING, REAL_PRICE_SOURCE, REAL_PRICE_CHECKED_ON


# Clave de fingerprint del plan en la mision persistida.
_PLAN_GATE = "GATE_1_PLAN"

# Regex de sha256 valido para huellas de plan.
_SHA256_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")

# Estados de mision que permiten ejecucion de especialistas.
_EXECUTABLE_MISSION_STATES = frozenset({"AUTORIZADA_PARA_EJECUTAR", "EN_EJECUCION"})


def _valid_identity(value: object) -> bool:
    return isinstance(value, str) and bool(value) and value == value.strip()


def _valid_fingerprint(value: object) -> bool:
    return isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None


def _require_persistent_repo(repository) -> None:
    """Lanza ValueError si el repositorio usa :memory: o no tiene ruta de archivo."""
    db_path = getattr(repository, "db_path", None)
    if not isinstance(db_path, str) or db_path == ":memory:" or not db_path.strip():
        raise ValueError(
            "INVALID_INPUT: La ejecucion real requiere un repositorio persistente "
            "en archivo; ':memory:' no esta permitido."
        )


def _real_config() -> RuntimeConfig:
    """Construye el perfil REAL con cero reintentos automaticos."""
    return RuntimeConfig(
        execution_mode=REAL_MODE,
        max_retries=0,
        pricing_table=REAL_MODEL_PRICING,
    )


class RealExecutionComposition:
    """Composicion segura de los componentes de ejecucion real.

    Cada instancia encapsula la composicion para una mision y tarea
    especificas. El contexto humano y la autoridad de ejecucion se
    revalidan en cada llamada a execute_task().

    No implementa especialistas, endpoints ni interfaz. No autoriza
    prompts arbitrarios desde el navegador.

    Parametros
    ----------
    repository:
        LocalRepository ya abierto apuntando a un archivo persistente.
        No se acepta ':memory:'.
    mission_id : str
        Identificador de la mision cuyos registros persistidos se usaran
        para derivar propietario, aprobacion y huella.
    task_id : str
        Identificador de la tarea del plan aprobado a ejecutar.
    approvals:
        HumanApprovalEngine activo cuyo contexto local valida la identidad
        del solicitante. Requerido; no se construye internamente.
    human_context:
        LocalHumanContext devuelto por approvals.bind_local_profile().
        Verificado con approvals.check_context() en cada llamada.
    api_key : str | None
        Clave de API de Gemini. Si es None se lee de GEMINI_API_KEY o
        GOOGLE_API_KEY. Nunca se persiste ni se imprime.
    _provider_override:
        Solo para pruebas internas. Proveedor que sustituye al ADK real.
        No hay opcion HTTP, ambiental ni de configuracion que lo active
        en produccion; este parametro no existe en la interfaz publica.

    Uso esperado por futuros especialistas:
        comp = RealExecutionComposition(repo, mission_id, task_id, approvals, ctx)
        ok, result, error = comp.execute_task(
            system_instruction="...",
            prompt="...",
            response_schema={...},
        )
        # result y error tienen el formato de AgentGateway.execute_agent_call.
        # Ver docstring del modulo para el protocolo de consumo.
    """

    def __init__(
        self,
        repository,
        mission_id: str,
        task_id: str,
        approvals,
        human_context,
        *,
        api_key: Optional[str] = None,
        _provider_override=None,
    ) -> None:
        # --- Validaciones de construccion ---
        if repository is None:
            raise ValueError("INVALID_INPUT: El repositorio es obligatorio.")
        _require_persistent_repo(repository)
        if not _valid_identity(mission_id):
            raise ValueError("INVALID_INPUT: mission_id invalido.")
        if not _valid_identity(task_id):
            raise ValueError("INVALID_INPUT: task_id invalido.")
        if approvals is None:
            raise ValueError("INVALID_INPUT: approvals (HumanApprovalEngine) es obligatorio.")
        if human_context is None:
            raise ValueError("INVALID_INPUT: human_context es obligatorio.")
        if not approvals.check_context(human_context):
            raise ValueError(
                "PERMISSION_DENIED: El contexto humano no es valido para el motor de aprobaciones."
            )

        self._repo = repository
        self._mission_id = mission_id
        self._task_id = task_id
        self._approvals = approvals
        self._human_context = human_context

        # Proveedor: ADKModelClientProvider en produccion; _provider_override
        # solo disponible como parametro de prueba controlado.
        if _provider_override is not None:
            self._provider = _provider_override
        else:
            self._provider = ADKModelClientProvider(api_key=api_key, mode=REAL_MODE)

        self._config = _real_config()

    # ------------------------------------------------------------------
    # Interfaz publica
    # ------------------------------------------------------------------

    def execute_task(
        self,
        *,
        system_instruction: str,
        prompt: str,
        response_schema: Dict[str, Any],
    ) -> Tuple[bool, Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        """Ejecuta una llamada real vinculada a la mision y tarea de esta instancia.

        Revalida el contexto y la autoridad antes de cada invocacion.
        Delega adquisicion, reservas y resultado terminal al gateway y a
        los componentes de REAL-01. No abre una transaccion durante la
        llamada al proveedor.

        Parametros
        ----------
        system_instruction : str
            Instruccion de sistema proporcionada por el especialista de confianza.
        prompt : str
            Entrada del especialista de confianza.
        response_schema : dict
            Esquema JSON del resultado esperado; obligatorio en modo REAL.

        Devuelve
        --------
        (ok, result, error) con el mismo protocolo que AgentGateway.execute_agent_call.
        Ver docstring del modulo para el protocolo de consumo por el runtime futuro.
        """
        # 1. Revalidar el contexto humano en cada llamada.
        if not self._approvals.check_context(self._human_context):
            return False, None, {
                "schema_version": "1.0.0",
                "error_code": "PERMISSION_DENIED",
                "message": "El contexto humano ya no es valido.",
                "retry_allowed": False, "max_retries": 0,
                "current_attempt": 0, "recoverable": False,
                "required_action": "renovar_contexto",
            }

        # 2. Leer la mision y derivar identidad de los registros persistidos.
        #    Ningun parametro libre concede autoridad.
        mission_identity = self._read_mission_identity()
        if mission_identity is None:
            return False, None, {
                "schema_version": "1.0.0",
                "error_code": "PERMISSION_DENIED",
                "message": "La mision, el propietario o la aprobacion no son validos o el plan cambio.",
                "retry_allowed": False, "max_retries": 0,
                "current_attempt": 0, "recoverable": False,
                "required_action": "revisar_mision",
            }

        owner_id, approval_id, plan_fingerprint = mission_identity

        # 3. Componer los componentes con el mismo repositorio y la huella derivada.
        validator = LocalApprovalRecordValidator(self._repo)
        store = RepositoryDurableCallStore(
            self._repo,
            authorized_content_fingerprint=plan_fingerprint,
            authorization_validator=validator,
        )

        # 4. Componer el gateway con cero reintentos y modo REAL.
        gateway = AgentGateway(
            config=self._config,
            provider=self._provider,
            repository=self._repo,
            real_execution_authorized=True,
            real_authorization_validator=validator,
            idempotency_store=store,
        )

        # 5. Delegar la ejecucion al gateway. La transaccion SQLite de adquisicion
        #    se cierra antes de que el gateway llame al proveedor.
        return gateway.execute_agent_call(
            system_instruction,
            prompt,
            mission_id=self._mission_id,
            task_id=self._task_id,
            owner_id=owner_id,
            approval_id=approval_id,
            response_schema=response_schema,
        )

    # ------------------------------------------------------------------
    # Metodos internos
    # ------------------------------------------------------------------

    def _read_mission_identity(
        self,
    ) -> Optional[Tuple[str, str, str]]:
        """Lee propietario, approval_id y fingerprint de la mision persistida.

        Devuelve (owner_id, approval_id, plan_fingerprint) o None si
        cualquier verificacion falla. No escribe nada.

        Verificaciones:
        - La mision existe y su mission_id coincide.
        - El propietario es identidad valida y coincide con el contexto.
        - El estado de la mision permite ejecucion de especialistas.
        - approval_id y plan_fingerprint son validos y coherentes.
        """
        try:
            mission = self._repo.get_mission(self._mission_id)
        except Exception:
            return None

        if not isinstance(mission, dict):
            return None
        if mission.get("mission_id") != self._mission_id:
            return None

        owner_id = mission.get("user_id")
        if not _valid_identity(owner_id):
            return None

        # El propietario de la mision debe coincidir con el contexto humano.
        if owner_id != self._human_context.user_id:
            return None

        if mission.get("status") not in _EXECUTABLE_MISSION_STATES:
            return None

        approval_id = mission.get("approval_id")
        if not _valid_identity(approval_id):
            return None

        plan_fingerprint = mission.get("plan_fingerprint")
        if not _valid_fingerprint(plan_fingerprint):
            return None

        return owner_id, approval_id, plan_fingerprint
