"""OminAI HQ - Ciclo de Vida, Retencion, Archivo y Borrado Seguro (PZ-010D).

Implementa la distincion estricta entre cancelar, archivar y eliminar datos,
con confirmacion humana explicita, prevencion de path traversal y manejo de efectos
sobre la verificabilidad de evidencias conforme a CONTRATO-MVP-v1.md seccion 9.6, 11.6 y 11.7.
"""

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

import app.approved_memory as approved_memory
import app.evidence_registry as evidence_registry
import app.local_repository as local_repository


class DataLifecycleError(Exception):
    """Excepcion controlada en operaciones de ciclo de vida de datos."""
    pass


class DataLifecycleManager:
    """Gestiona el archivo, eliminacion segura y efectos de retencion en misiones y evidencias."""

    def __init__(
        self,
        repository: Optional[local_repository.LocalRepository] = None,
        memory_manager: Optional[approved_memory.ApprovedMemoryManager] = None,
        evidence_reg: Optional[evidence_registry.EvidenceRegistry] = None,
    ) -> None:
        self.repository = repository or local_repository.LocalRepository()
        self.memory_manager = memory_manager or approved_memory.ApprovedMemoryManager()
        self.evidence_registry = evidence_reg or evidence_registry.EvidenceRegistry()

    def archive_mission(self, mission_id: str) -> Tuple[bool, Optional[dict], Optional[str]]:
        """Archiva una mision ocultandola del estado activo y liberando el cupo de mision concurrente."""
        mis = self.repository.get_mission(mission_id)
        if not mis:
            return False, None, f"Mision {mission_id} no encontrada."

        mis["status"] = "ARCHIVADA"
        mis["current_state"] = "ARCHIVADA"
        mis["archived_at"] = datetime.now(timezone.utc).isoformat()

        ok, err = self.repository.save_mission(mis)
        if not ok:
            return False, None, f"Fallo al archivar mision: {err}"

        return True, mis, None

    def delete_mission(
        self,
        mission_id: str,
        target_version: int,
        human_confirmed: bool = False,
        confirmation_reason: str = "",
    ) -> Tuple[bool, Optional[str]]:
        """Elimina de forma segura una mision exigiendo confirmacion humana y prevencion de path traversal."""
        # 1. Validar proteccion contra path traversal
        if ".." in mission_id or "/" in mission_id or "\\" in mission_id:
            return False, "PATH_TRAVERSAL_DETECTADO: Identificador de mision invalido."

        # 2. Exigir confirmacion humana expresa
        if not human_confirmed:
            return False, "ELIMINACION_REQUIERE_CONFIRMACION_HUMANA: La eliminacion irreversible exige autorizacion expresa."

        # 3. Comprobar existencia y version
        mis = self.repository.get_mission(mission_id)
        if not mis:
            return False, f"Mision {mission_id} no encontrada."

        if mis.get("version", 1) != target_version:
            return False, f"VERSION_MISMATCH: La version indicada ({target_version}) no coincide con la version actual ({mis.get('version', 1)})."

        try:
            with self.repository._conn:
                self.repository._conn.execute("DELETE FROM missions WHERE mission_id = ?;", (mission_id,))
                self.repository._conn.execute("DELETE FROM checkpoints WHERE mission_id = ?;", (mission_id,))
                self.repository._conn.execute("DELETE FROM approvals WHERE mission_id = ?;", (mission_id,))
                self.repository._conn.execute("DELETE FROM evidences WHERE mission_id = ?;", (mission_id,))
                self.repository._conn.execute("DELETE FROM audit_events WHERE mission_id = ?;", (mission_id,))
            return True, None
        except Exception as e:
            return False, f"Fallo al eliminar registros de mision: {str(e)}"

    def handle_evidence_deletion_event(
        self,
        mission_id: str,
        evidence_id: str,
        is_post_approval: bool,
    ) -> Tuple[bool, dict, Optional[str]]:
        """Gestiona el impacto de la eliminacion de un original antes o despues de la aprobacion del VBP."""
        if not is_post_approval:
            # Preaprobacion: Detener y bloquear porque la evidencia requerida no esta disponible
            return False, {
                "evidence_id": evidence_id,
                "status": "EVIDENCIA_NO_DISPONIBLE",
                "gate_blocked": True,
            }, "EVIDENCIA_NO_DISPONIBLE: Archivo original eliminado previo a la aprobacion. Se requiere decision humana."
        else:
            # Postaprobacion: Preservar el VBP historico, marcar evidencia eliminada y degradar verificabilidad
            record = {
                "evidence_id": evidence_id,
                "mission_id": mission_id,
                "status": "ELIMINADA_POR_EL_USUARIO",
                "verifiability": "VERIFICABILIDAD_INCOMPLETA",
                "historical_vbp_preserved": True,
                "deleted_at": datetime.now(timezone.utc).isoformat(),
            }
            return True, record, None
