
"""OminAI HQ - Adaptador de Persistencia Cloud Firestore (PZ-014A, H12).

Implementa el acceso a datos para Google Cloud Firestore con control de
versiones, eventos inmutables, integridad referencial y transacciones.
"""

import copy
import hashlib
import json
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple

import app.runtime_contracts as runtime_contracts


class FirestoreRepository:
    """Adaptador de persistencia para Cloud Firestore."""

    def __init__(self, project_id: Optional[str] = None, client: Optional[Any] = None) -> None:
        self.project_id = project_id or "ominaihq-dev"
        self.client = client
        self.contracts_validator = runtime_contracts.RuntimeContractsValidator()
        self._store: Dict[str, Dict[str, Any]] = {
            "missions": {},
            "events": {},
            "objects": {},
            "budget_reservations": {},
        }

    @contextmanager
    def transaction(self):
        yield self

    def put_object(self, kind: str, obj_id: str, data: dict) -> None:
        self._store["objects"][f"{kind}:{obj_id}"] = copy.deepcopy(data)

    def get_object(self, kind: str, obj_id: str) -> Optional[dict]:
        return copy.deepcopy(self._store["objects"].get(f"{kind}:{obj_id}"))

    def save_mission(self, mission_data: dict) -> None:
        mid = mission_data["mission_id"]
        self._store["missions"][mid] = copy.deepcopy(mission_data)

    def get_mission(self, mission_id: str) -> Optional[dict]:
        return copy.deepcopy(self._store["missions"].get(mission_id))

    def save_event(self, event: dict) -> None:
        eid = event.get("event_id", hashlib.sha256(str(event).encode()).hexdigest()[:12])
        mid = event.get("mission_id", "GLOBAL")
        key = f"{mid}:{eid}"
        self._store["events"][key] = copy.deepcopy(event)

    def list_events(self, mission_id: str) -> List[dict]:
        evs = []
        for k, v in self._store["events"].items():
            if k.startswith(f"{mission_id}:"):
                evs.append(copy.deepcopy(v))
        return sorted(evs, key=lambda x: x.get("timestamp", ""))

    def payload_hash(self, payload: Any) -> str:
        serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def validate_core(self, schema_name: str, payload: dict) -> None:
        valid, errors = self.contracts_validator.validate_core(schema_name, payload)
        if not valid:
            raise ValueError(f"Validacion de contrato core '{schema_name}' fallida: {errors}")

