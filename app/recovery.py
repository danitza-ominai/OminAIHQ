"""OminAI HQ - Recuperacion ante Fallos e Idempotencia Durable (PZ-010B).

Implementa la reanudacion segura de misiones desde checkpoints transaccionales,
preservando limites acumulados de costo/intentos y bloqueando la duplicacion de tareas
conforme a CONTRATO-MVP-v1.md seccion 11.3-11.5 y RF-021.
"""

import copy
import json
from typing import Any, Dict, List, Optional, Tuple

import app.local_repository as local_repository
import app.runtime_config as runtime_config


class RecoveryError(Exception):
    """Excepcion controlada en el proceso de recuperacion."""
    pass


class RecoveryManager:
    """Gestiona la recuperacion de estado y preservacion de limites tras interrupcion."""

    def __init__(
        self,
        repository: Optional[local_repository.LocalRepository] = None,
        config: Optional[runtime_config.RuntimeConfig] = None,
    ) -> None:
        self.repository = repository or local_repository.LocalRepository()
        self.config = config or runtime_config.RuntimeConfig()

    def recover_mission(self, mission_id: str) -> Tuple[bool, Optional[dict], Optional[str]]:
        """Recupera el estado exacto de una mision desde SQLite preservando contadores y autorizaciones."""
        mission_record = self.repository.get_mission(mission_id)
        if not mission_record:
            return False, None, f"Mision {mission_id} no encontrada en repositorio durable."

        checkpoints = self.repository.list_checkpoints(mission_id)
        approvals = self.repository.list_approvals(mission_id)

        # 1. Comprobar integridad de checkpoints
        latest_checkpoint = None
        if not checkpoints:
            return False, None, "CHECKPOINT_CORRUPTO: No hay checkpoint verificable; recuperacion bloqueada."
        if checkpoints:
            try:
                # El ultimo checkpoint ordenado cronologicamente
                last_chk = checkpoints[-1]
                snapshot_data = json.loads(last_chk["state_snapshot_json"]) if isinstance(last_chk["state_snapshot_json"], str) else last_chk["state_snapshot_json"]
                self.repository.validate_core("checkpoint", snapshot_data)
                self.repository.validate_core("mission", mission_record["nuclear"])
                integrity = self.repository.get_object("checkpoint_integrity", last_chk["checkpoint_id"])
                expected = self.repository.build_checkpoint(mission_record, last_chk["checkpoint_id"], last_chk["created_at"])
                if (snapshot_data != expected or snapshot_data["mission_id"] != mission_id
                    or mission_record["nuclear"]["last_checkpoint_id"] != last_chk["checkpoint_id"]
                    or not integrity or integrity["mission_hash"] != self.repository.payload_hash(mission_record)):
                    raise ValueError("Integridad o pertenencia incompatible")
                for ref in snapshot_data["authorizations"]:
                    wrapper = self.repository.get_object("approval_request", ref)
                    record = self.repository.get_object("approval_record", ref)
                    if not wrapper or not record or wrapper["record"] != record:
                        raise ValueError("Autorizacion inexistente")
                    self.repository.validate_core("approval", record)
                    request = wrapper["request"]
                    if (request["mission_id"] != mission_id or request["version"] > mission_record["version"]
                        or record["user_id"] != mission_record["user_id"] or record["status"] != "CONSUMIDA"
                        or record["decision"] not in ("APROBAR", "APROBAR_CON_EXCEPCION")):
                        raise ValueError("Autorizacion cruzada u obsoleta")
                    from app.human_approvals import document_fingerprint
                    candidate = self.repository.get_object("candidate", mission_id + ":" + request["gate_type"])
                    if not candidate or document_fingerprint(candidate, request["gate_type"]) != record["version_or_fingerprint"]:
                        raise ValueError("Contenido autorizado alterado")
                latest_checkpoint = {
                    "checkpoint_id": last_chk["checkpoint_id"],
                    "milestone": last_chk["milestone"],
                    "snapshot": snapshot_data,
                    "created_at": last_chk["created_at"],
                }
            except Exception:
                return False, None, "CHECKPOINT_CORRUPTO: Estructura, huella, version o referencias invalidas."

        # 2. Comprobar integridad de aprobaciones
        valid_approvals = []
        for app in approvals:
            if not app.get("fingerprint") or not app.get("idempotency_key"):
                return False, None, "APROBACION_INVALIDA: Registro de aprobacion carece de huella o clave de idempotencia."
            valid_approvals.append(app)

        # 3. Reconstruir estado recuperado
        recovered_state = copy.deepcopy(mission_record)
        recovered_state["recovered"] = True
        recovered_state["latest_checkpoint"] = latest_checkpoint
        recovered_state["approvals_count"] = len(valid_approvals)

        # Preservar contadores de gasto e intentos acumulados
        recovered_state["cost_usd"] = recovered_state.get("cost_usd", 0.0)
        recovered_state["attempts_count"] = recovered_state.get("attempts_count", 0)

        # Detectar tareas en curso interrumpidas
        tasks = recovered_state.get("tasks", [])
        for task in tasks:
            if task.get("status") in ("EN_CURSO", "EN_EJECUCION"):
                # Estado indeterminado: pausar y requerir confirmacion humana, no reintentar a ciegas
                task["status"] = "BLOQUEADA"
                task["requires_human_decision"] = True
                if recovered_state["status"] != "CANCELADA":
                    recovered_state["resumable_state"] = recovered_state.get("resumable_state") or "EN_EJECUCION"
                    recovered_state["status"] = "PAUSADA"
                    recovered_state["current_state"] = "PAUSADA"
                recovered_state["pause_reason"] = "ESTADO_INDETERMINADO_EN_INTERRUPCION"

        if recovered_state.get("inflight") and recovered_state["status"] != "CANCELADA":
            recovered_state["status"] = "PAUSADA"
            recovered_state["current_state"] = "PAUSADA"
            recovered_state["pause_reason"] = "ESTADO_INDETERMINADO_EN_INTERRUPCION"
        recovered_state["budget"] = self.repository.budget_snapshot()
        return True, recovered_state, None
