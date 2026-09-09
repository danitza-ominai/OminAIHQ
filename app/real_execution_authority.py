"""REAL-01 – Validador de autorizacion persistida para ejecucion real.

Componente de producto: RealExecutionAuthorizationValidator.

Verifica que existe una decision humana real, persistida y vigente en el
repositorio antes de permitir que AgentGateway ejecute una llamada real.

Contratos aplicados:
- CONTRATO-MVP-v1.md ss4.4 (decisiones humanas), ss6.4 (aprobaciones),
  RF-006, RF-007, RF-025, RNF-002, RNF-006.
- AGENTS.md: no crea aprobaciones ni perfiles al validar; no confunde
  vencimiento de solicitud pendiente con vigencia de decision tomada.

Restricciones:
- Solo lectura durante la validacion: cero escrituras si la validacion falla.
- Recibe el repositorio explicitamente; compatible con SQLite en pruebas.
- No declarado compatible con Firestore hasta contar con evidencia ejecutable.
- No es una cache volatil; lee del repositorio en cada llamada.
"""

from __future__ import annotations

import copy
import re
from typing import Optional

from app.agent_gateway import RealExecutionAuthorizationValidator, ValidatedRealExecutionMandate
from app.human_approvals import document_fingerprint

# ---------------------------------------------------------------------------
# Constantes internas
# ---------------------------------------------------------------------------

# Solo la aprobacion ordinaria del plan autoriza ejecutar especialistas.
_APPROVING_DECISION = "APROBAR"
_PLAN_GATE = "GATE_1_PLAN"
_TERMINAL_STATUS = "CONSUMIDA"
_EXECUTABLE_MISSION_STATES = frozenset({
    "AUTORIZADA_PARA_EJECUTAR",
    "EN_EJECUCION",
})
_SHA256_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")


def _valid_identity(value: object) -> bool:
    """Acepta solo identificadores no vacios y sin espacios marginales."""
    return isinstance(value, str) and bool(value) and value == value.strip()


def _valid_fingerprint(value: object) -> bool:
    return isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None


def _single_task(tasks: object, task_id: str) -> Optional[dict]:
    if not isinstance(tasks, list):
        return None
    matches = [task for task in tasks if isinstance(task, dict) and task.get("task_id") == task_id]
    return matches[0] if len(matches) == 1 else None


def _runtime_task_matches_plan(runtime_task: dict, plan_task: dict, mission: dict) -> bool:
    """Comprueba la identidad y los campos derivados del contenido aprobado."""
    if runtime_task.get("mission_id") != mission.get("mission_id"):
        return False
    if runtime_task.get("mission_version") != mission.get("version"):
        return False
    direct_fields = (
        "task_id",
        "agent_role",
        "objective",
        "allowed_tool_categories",
        "dependencies",
    )
    if any(runtime_task.get(field) != plan_task.get(field) for field in direct_fields):
        return False
    if runtime_task.get("question") != plan_task.get("objective"):
        return False
    if runtime_task.get("authorized_context", {}).get("input_refs") != plan_task.get("input_refs"):
        return False
    expected_output = runtime_task.get("expected_output")
    if not isinstance(expected_output, dict):
        return False
    if expected_output.get("description") != plan_task.get("expected_output"):
        return False
    if expected_output.get("acceptance_criteria") != plan_task.get("acceptance_criteria"):
        return False
    runtime_limits = runtime_task.get("limits")
    plan_limits = plan_task.get("limits")
    if not isinstance(runtime_limits, dict) or not isinstance(plan_limits, dict):
        return False
    expected_limits = {**plan_limits, "max_depth": 0, "max_breadth": 1}
    return runtime_limits == expected_limits


class LocalApprovalRecordValidator(RealExecutionAuthorizationValidator):
    """Valida la autorizacion de ejecucion real contra registros persistidos.

    Lee unicamente de los objetos 'approval_record' y 'approval_request'
    persistidos por HumanApprovalEngine. No escribe nada durante la
    validacion, sea esta exitosa o fallida.

    Parametros
    ----------
    repository:
        Instancia de LocalRepository ya inicializada y abierta.
        Inyeccion explicita obligatoria; no se crea internamente.
        El validador consulta en cada llamada la mision, su propietario, el
        plan vigente, la tarea runtime, la solicitud y la decision persistida.
        No admite conjuntos de tareas ni huellas proporcionados por el llamador.
    """

    def __init__(
        self,
        repository,
    ) -> None:
        if repository is None:
            raise ValueError("INVALID_INPUT: El repositorio es obligatorio.")
        self._repo = repository

    # ------------------------------------------------------------------
    # Interfaz publica (contrato RealExecutionAuthorizationValidator)
    # ------------------------------------------------------------------

    def validate(
        self,
        *,
        mission_id: str,
        task_id: str,
        owner_id: str,
        approval_id: str,
    ) -> Optional[ValidatedRealExecutionMandate]:
        """Devuelve un mandato validado o None si cualquier verificacion falla.

        No lanza excepciones controladas; cualquier error de lectura o
        inconsistencia produce None (fallo cerrado). El llamador (AgentGateway)
        trata None como rechazo de autorizacion.

        La pertenencia al plan y la igualdad del contenido vigente con el
        aprobado son obligatorias. Solo GATE_1_PLAN con decision APROBAR
        puede producir un mandato; VBP y excepciones fallan cerrado.
        """
        if not all(_valid_identity(value) for value in (
            mission_id, task_id, owner_id, approval_id
        )):
            return None

        try:
            mission = self._repo.get_mission(mission_id)
            profile = self._repo.get_profile(owner_id)
            envelope = self._repo.get_object("approval_request", approval_id)
            record = self._repo.get_object("approval_record", approval_id)
            candidate = self._repo.get_object("candidate", mission_id + ":" + _PLAN_GATE)
            approvals = self._repo.list_approvals(mission_id)
        except Exception:
            return None

        if not all(isinstance(item, dict) for item in (
            mission, profile, envelope, record, candidate
        )):
            return None
        if mission.get("mission_id") != mission_id:
            return None
        if mission.get("user_id") != owner_id:
            return None
        if profile.get("user_id") != owner_id or profile.get("actor_role") != "usuario_humano":
            return None
        if mission.get("status") not in _EXECUTABLE_MISSION_STATES:
            return None
        if mission.get("current_state") != mission.get("status"):
            return None
        if mission.get("approval_id") != approval_id:
            return None
        if mission.get("pending_" + _PLAN_GATE) != approval_id:
            return None
        nuclear = mission.get("nuclear")
        if not isinstance(nuclear, dict):
            return None
        if nuclear.get("mission_id") != mission_id or nuclear.get("user_id") != owner_id:
            return None
        if nuclear.get("record_version") != mission.get("version"):
            return None
        if approval_id not in nuclear.get("approval_refs", []):
            return None

        request = envelope.get("request")
        embedded_record = envelope.get("record")
        if not isinstance(request, dict) or embedded_record != record:
            return None
        if (
            request.get("approval_id") != approval_id
            or request.get("mission_id") != mission_id
            or request.get("gate_type") != _PLAN_GATE
            or request.get("status") != _TERMINAL_STATUS
            or not _valid_fingerprint(request.get("fingerprint"))
            or not _valid_identity(request.get("idempotency_key"))
            or type(request.get("version")) is not int
            or request["version"] < 1
            or request["version"] > mission.get("version", 0)
        ):
            return None

        fingerprint = request["fingerprint"]
        if (
            record.get("approval_id") != approval_id
            or record.get("user_id") != owner_id
            or record.get("actor") != owner_id
            or record.get("actor_role") != "usuario_humano"
            or record.get("decision") != _APPROVING_DECISION
            or record.get("status") != _TERMINAL_STATUS
            or record.get("idempotency_key") != request["idempotency_key"]
            or record.get("version_or_fingerprint") != fingerprint
        ):
            return None

        matching_approvals = [
            approval for approval in approvals
            if isinstance(approval, dict) and approval.get("approval_id") == approval_id
        ]
        if len(matching_approvals) != 1:
            return None
        approval = matching_approvals[0]
        if (
            approval.get("mission_id") != mission_id
            or approval.get("approval_type") != _PLAN_GATE
            or approval.get("status") != _TERMINAL_STATUS
            or approval.get("decision") != _APPROVING_DECISION
            or approval.get("idempotency_key") != request["idempotency_key"]
            or approval.get("fingerprint") != fingerprint
            or approval.get("actor") != owner_id
        ):
            return None

        current_document = {
            "brief": copy.deepcopy(mission.get("brief")),
            "plan": copy.deepcopy(mission.get("plan")),
        }
        if candidate != current_document:
            return None
        try:
            if document_fingerprint(candidate, _PLAN_GATE) != fingerprint:
                return None
            if document_fingerprint(current_document, _PLAN_GATE) != fingerprint:
                return None
        except Exception:
            return None
        if mission.get("plan_fingerprint") != fingerprint:
            return None

        approved_task = _single_task(candidate.get("plan", {}).get("tasks"), task_id)
        current_plan_task = _single_task(mission.get("plan", {}).get("tasks"), task_id)
        runtime_task = _single_task(mission.get("tasks"), task_id)
        if approved_task is None or current_plan_task is None or runtime_task is None:
            return None
        if approved_task != current_plan_task:
            return None
        if not _runtime_task_matches_plan(runtime_task, approved_task, mission):
            return None

        return ValidatedRealExecutionMandate(
            mission_id=mission_id,
            task_id=task_id,
            owner_id=owner_id,
            approval_id=approval_id,
            decision=_APPROVING_DECISION,
            persisted=True,
            is_current=True,
        )
