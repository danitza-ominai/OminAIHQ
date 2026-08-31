"""OminAI HQ - Auditoria Consultable y Trazas Minimizadas (PZ-009D).

Implementa la linea de tiempo consultable por mision, tarea, fuente y decision,
con proyecciones minimizadas sin Chain-of-Thought, aislamiento estricto entre misiones
y preservacion de la integridad historica conforme a CONTRATO-MVP-v1.md seccion 6.5 y 11.1.
"""

import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

# Patrones para sanitizacion de auditoria
SECRET_PATTERN = re.compile(r"(?:api[_-]?key|secret|password|bearer|private[_-]?key)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-]{16,})['\"]?", re.IGNORECASE)
PATH_PATTERN = re.compile(r"(?:[a-zA-Z]:\\[^\s'\"]+|/(?:home|Users|root|etc|var)/[^\s'\"]+)")
COT_PATTERN = re.compile(r"<thought>.*?</thought>", re.DOTALL | re.IGNORECASE)


class AuditQueryEngine:
    """Motor de consulta y agregacion de eventos de auditoria con aislamiento por mision."""

    def __init__(self, initial_events: Optional[List[dict]] = None, repository=None) -> None:
        self.repository = repository
        self.events: List[dict] = []
        self.event_ids: Set[str] = set()

        if initial_events:
            for ev in initial_events:
                self.record_event(ev)

    def sanitize_audit_text(self, text: str) -> str:
        """Elimina Chain-of-Thought, secretos y rutas absolutas privadas de las trazas de auditoria."""
        if not text or not isinstance(text, str):
            return ""

        sanitized = COT_PATTERN.sub("[COT_ELIMINADO]", text)
        sanitized = SECRET_PATTERN.sub("[REDACTED_SECRET]", sanitized)
        sanitized = PATH_PATTERN.sub("[RUTA_LOCAL_PROTEGIDA]", sanitized)
        return sanitized

    def record_event(self, event_data: dict) -> Tuple[bool, Optional[str]]:
        """Registra un evento de auditoria verificando unicidad de ID y sanitizacion previa."""
        ev_id = event_data.get("event_id")
        mission_id = event_data.get("mission_id")

        if not ev_id or not mission_id:
            return False, "Evento de auditoria debe incluir event_id y mission_id validos."

        if ev_id in self.event_ids:
            return False, f"Identificador de evento duplicado: {ev_id}."

        if event_data.get('schema_version'):
            from app.local_repository import LocalRepository
            try:
                LocalRepository.validate_core('event', event_data)
            except ValueError:
                return False, 'SCHEMA_INVALID: Evento nuclear invalido.'
        ev_copy = self._project(event_data)

        # Sanitizar campos de texto
        if "result_summary" in ev_copy:
            ev_copy["result_summary"] = self.sanitize_audit_text(ev_copy["result_summary"])
        if "action" in ev_copy:
            ev_copy["action"] = self.sanitize_audit_text(ev_copy["action"])

        if "timestamp" not in ev_copy:
            ev_copy["timestamp"] = datetime.now(timezone.utc).isoformat()

        # Calcular huella del evento
        hasher = hashlib.sha256()
        key_tuple = (
            ev_copy["event_id"],
            ev_copy["mission_id"],
            ev_copy.get("task_id", ""),
            ev_copy.get("action", ""),
            ev_copy.get("result_summary", ""),
            ev_copy["timestamp"],
        )
        hasher.update("|".join(str(value or '') for value in key_tuple).encode("utf-8"))
        ev_copy["fingerprint"] = f"sha256:{hasher.hexdigest()}"

        self.events.append(ev_copy)
        self.event_ids.add(ev_id)
        return True, None

    def _project(self, value):
        if isinstance(value, str):
            return self.sanitize_audit_text(value)
        if isinstance(value, list):
            return [self._project(item) for item in value]
        if isinstance(value, dict):
            return {key:self._project(item) for key,item in value.items()
                    if key.lower() not in {'chain_of_thought','scratchpad','internal_reasoning','reasoning_trace','prompt'}}
        return value

    def query_timeline(
        self,
        mission_id: str,
        task_id: Optional[str] = None,
        source_locator: Optional[str] = None,
        decision_id: Optional[str] = None,
        actor_role: Optional[str] = None,
    ) -> List[dict]:
        """Consulta la linea de tiempo filtrada con aislamiento estricto por mision."""
        results: List[dict] = []
        events = self.repository.list_events(mission_id) if self.repository else self.events
        for ev in events:
            # Aislamiento por mision
            if ev.get("mission_id") != mission_id:
                continue

            if task_id and ev.get("task_id") != task_id:
                continue
            if source_locator and ev.get("source_or_artifact", ev.get("source_locator")) != source_locator:
                continue
            if decision_id and ev.get("related_approval_id", ev.get("decision_id")) != decision_id:
                continue
            if actor_role and ev.get("actor_role") != actor_role:
                continue

            results.append(self._project(ev))

        return results

    def reconstruct_trajectory(self, mission_id: str) -> dict:
        """Reconstruye el recorrido de ejecucion completo de la mision agrupando etapas y checkpoints."""
        timeline = self.query_timeline(mission_id)

        approvals: List[dict] = []
        checkpoints: List[dict] = []
        errors: List[dict] = []
        stages_passed: List[str] = []

        for ev in timeline:
            action = ev.get("action", "")
            if "aprobacion" in action.lower() or ev.get("related_approval_id", ev.get("decision_id")):
                approvals.append({
                    "event_id": ev["event_id"],
                    "decision_id": ev.get("related_approval_id", ev.get("decision_id")),
                    "timestamp": ev["timestamp"],
                    "actor_role": ev.get("actor_role"),
                })
            if "checkpoint" in action.lower() or ev.get("checkpoint_id"):
                checkpoints.append({
                    "event_id": ev["event_id"],
                    "checkpoint_id": ev.get("checkpoint_id"),
                    "timestamp": ev["timestamp"],
                })
            if ev.get("typed_error") or ev.get("error_code"):
                errors.append({
                    "event_id": ev["event_id"],
                    "error_code": (ev.get("typed_error") or {}).get("error_code", ev.get("error_code")),
                    "summary": ev.get("result_summary"),
                })
            if action not in stages_passed:
                stages_passed.append(action)

        if self.repository:
            checkpoints = [self._project(json.loads(row['state_snapshot_json']))
                           for row in self.repository.list_checkpoints(mission_id)]
        return {
            "mission_id": mission_id,
            "total_events": len(timeline),
            "stages_passed": stages_passed,
            "approvals_recorded": approvals,
            "checkpoints_recorded": checkpoints,
            "errors_recorded": errors,
            "events": timeline,
        }
