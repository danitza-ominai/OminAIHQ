"""OminAI HQ - Controles de Mision: Pausa, Cancelacion, Reanudacion y Cambio de Alcance (PZ-012B).

Implementa los controles de ciclo de vida en estados no terminales conforme a state-machine.json,
validando autoridad humana exclusiva para cancelaciones, preservacion de resumable_state,
bloqueo de reanudacion ante limites agotados o evidencia faltante y versionado de cambios de alcance
conforme a CONTRATO-MVP-v1.md seccion 4, 11.3-11.5 y RF-021/024/029.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

import app.local_repository as local_repository
import app.recovery as recovery
import app.runtime_config as runtime_config

TERMINAL_STATES = {"FINALIZADA", "CANCELADA"}
ACTIVE_FLOW_STATES = {
    "BORRADOR",
    "PLAN_EN_REVISION",
    "AUTORIZADA_PARA_EJECUTAR",
    "EN_EJECUCION",
    "EN_CONSOLIDACION",
    "VBP_EN_REVISION",
}


class MissionControlError(Exception):
    """Excepcion controlada en los controles de estado de mision."""
    pass


class MissionControlManager:
    """Gestiona pausas de seguridad, cancelaciones humanas, reanudaciones y cambios de alcance."""

    def __init__(
        self,
        repository: Optional[local_repository.LocalRepository] = None,
        recovery_mgr: Optional[recovery.RecoveryManager] = None,
        config: Optional[runtime_config.RuntimeConfig] = None,
    ) -> None:
        self.repository = repository or local_repository.LocalRepository()
        self.recovery = recovery_mgr or recovery.RecoveryManager(repository=self.repository)
        self.config = config or runtime_config.RuntimeConfig()

    def pause_mission(
        self,
        mission_id: str,
        reason: str,
        actor_role: str = "usuario_humano",
    ) -> Tuple[bool, Optional[dict], Optional[str]]:
        """Pausa una mision activa conservando su resumable_state para reanudacion futura."""
        mission = self.repository.get_mission(mission_id)
        if not mission:
            return False, None, f"Mision {mission_id} no encontrada."

        curr_state = mission.get("status")
        if curr_state in TERMINAL_STATES:
            return False, None, f"ESTADO_TERMINAL_INMUTABLE: No se puede pausar una mision en estado {curr_state}."

        if curr_state == "PAUSADA":
            # Idempotente: ya esta pausada, no duplicar ni cambiar version
            return True, mission, None

        mission["resumable_state"] = curr_state
        mission["status"] = "PAUSADA"
        mission["current_state"] = "PAUSADA"
        mission["pause_reason"] = reason
        mission["paused_at"] = datetime.now(timezone.utc).isoformat()

        ok, err = self.repository.save_mission(mission)
        if not ok:
            return False, None, f"Fallo al pausar mision: {err}"

        return True, mission, None

    def cancel_mission(
        self,
        mission_id: str,
        reason: str,
        actor_role: str = "usuario_humano",
    ) -> Tuple[bool, Optional[dict], Optional[str]]:
        """Cancela definitivamente una mision exigiendo autorizacion humana expresa (A0)."""
        if actor_role != "usuario_humano":
            return False, None, f"PERMISSION_DENIED: Rol '{actor_role}' no autorizado para cancelar. Solo el usuario humano puede cancelar."

        mission = self.repository.get_mission(mission_id)
        if not mission:
            return False, None, f"Mision {mission_id} no encontrada."

        curr_state = mission.get("status")
        if curr_state in TERMINAL_STATES:
            return False, None, f"ESTADO_TERMINAL_INMUTABLE: La mision ya se encuentra en estado terminal {curr_state}."

        mission["status"] = "CANCELADA"
        mission["current_state"] = "CANCELADA"
        mission["cancel_reason"] = reason
        mission["cancelled_at"] = datetime.now(timezone.utc).isoformat()

        ok, err = self.repository.save_mission(mission)
        if not ok:
            return False, None, f"Fallo al cancelar mision: {err}"

        return True, mission, None

    def resume_mission(
        self,
        mission_id: str,
        actor_role: str = "usuario_humano",
        missing_evidence: bool = False,
    ) -> Tuple[bool, Optional[dict], Optional[str]]:
        """Reanuda una mision pausada revalidando limites acumulados y disponibilidad de evidencia."""
        mission = self.repository.get_mission(mission_id)
        if not mission:
            return False, None, f"Mision {mission_id} no encontrada."

        if mission.get("status") != "PAUSADA":
            return False, None, f"ESTADO_INVALIDO: Solo se pueden reanudar misiones en estado PAUSADA (actual: {mission.get('status')})."

        # Validar limites acumulados (USD 25 maximo)
        spent_usd = mission.get("cumulative_cost_usd", 0.0)
        if spent_usd >= self.config.max_budget_usd:
            return False, None, f"PRESUPUESTO_AGOTADO: El gasto acumulado (${spent_usd:.2f}) ha alcanzado el limite maximo permitido."

        # Validar disponibilidad de evidencia original
        if missing_evidence:
            return False, None, "EVIDENCIA_NO_DISPONIBLE: La evidencia requerida no esta disponible. Reanudacion bloqueada."

        target_state = mission.get("resumable_state", "BORRADOR")
        mission["status"] = target_state
        mission["current_state"] = target_state
        mission["resumed_at"] = datetime.now(timezone.utc).isoformat()

        ok, err = self.repository.save_mission(mission)
        if not ok:
            return False, None, f"Fallo al reanudar mision: {err}"

        return True, mission, None

    def request_scope_change(
        self,
        mission_id: str,
        change_summary: str,
        actor_role: str = "usuario_humano",
    ) -> Tuple[bool, Optional[dict], Optional[str]]:
        """Aplica un cambio material de alcance incrementando la version y obligando a nueva revision del plan."""
        if actor_role != "usuario_humano":
            return False, None, f"PERMISSION_DENIED: Solo el operador humano puede autorizar un cambio de alcance."

        mission = self.repository.get_mission(mission_id)
        if not mission:
            return False, None, f"Mision {mission_id} no encontrada."

        curr_state = mission.get("status")
        if curr_state in TERMINAL_STATES:
            return False, None, f"ESTADO_TERMINAL_INMUTABLE: No se puede modificar el alcance de una mision terminal ({curr_state})."

        # Incrementar version y transicionar a revision
        new_version = mission.get("version", 1) + 1
        mission["version"] = new_version
        mission["status"] = "PLAN_EN_REVISION"
        mission["current_state"] = "PLAN_EN_REVISION"
        mission["scope_change_summary"] = change_summary
        mission["scope_modified_at"] = datetime.now(timezone.utc).isoformat()

        ok, err = self.repository.save_mission(mission)
        if not ok:
            return False, None, f"Fallo al registrar cambio de alcance: {err}"

        return True, mission, None
