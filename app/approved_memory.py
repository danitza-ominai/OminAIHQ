"""Persistent, version-bound approved memory. Never infer consent from VBP approval."""
import copy
import json
import uuid
from datetime import datetime, timezone
from app.local_repository import LocalRepository

VALID_CATEGORIES = {"PREFERENCIA", "RESTRICCION", "DECISION_ARQUITECTURA", "HECHO_VALIDADO"}

class MemoryAccessError(Exception):
    pass

class ApprovedMemoryManager:
    def __init__(self, repository=None, authority=None, now_fn=None):
        self.repository = repository or LocalRepository()
        self.authority = authority
        self.now_fn = now_fn or (lambda: datetime.now(timezone.utc))

    @property
    def memories(self):
        rows = self.repository._conn.execute("SELECT object_key,payload FROM durable_objects WHERE kind='memory'").fetchall()
        return {r[0]: json.loads(r[1]) for r in rows}

    def _authorized(self, context, record=None, version=None):
        return (self.authority is not None and self.authority.check_context(context)
                and (record is None or (record.get("user_id") == context.user_id
                     and type(version) is int and record.get("version") == version and "deleted_at" not in record)))

    def propose_memory(self, category, content, origin_mission_id, human_approved=False,
                       *, context=None, review_at=None, review_required=False,
                       conflict=False, material_impact=False):
        if human_approved or not self._authorized(context):
            return False, None, "PERMISSION_DENIED: La propuesta no concede aprobacion humana."
        origin = self.repository.get_mission(origin_mission_id)
        if not origin or origin.get("user_id") != context.user_id:
            return False, None, "PERMISSION_DENIED: Origen o propietario invalido."
        if category not in VALID_CATEGORIES or not isinstance(content, str) or not content.strip():
            return False, None, "INVALID_INPUT: Categoria o contenido invalido."
        if not all(type(x) is bool for x in (review_required, conflict, material_impact)):
            return False, None, "INVALID_INPUT: Condiciones invalidas."
        if review_at is not None:
            try:
                if datetime.fromisoformat(review_at).tzinfo is None:
                    raise ValueError()
            except (ValueError, TypeError):
                return False, None, "INVALID_INPUT: Fecha de revision con zona requerida."
        now = self.now_fn().isoformat()
        record = {"memory_id": "MEM-" + uuid.uuid4().hex, "category": category, "content": content.strip(),
                  "origin_mission_id": origin_mission_id, "user_id": context.user_id, "version": 1,
                  "status": "PROPUESTA_PENDIENTE_APROBACION", "human_approved": False,
                  "approved_version": None, "review_at": review_at, "review_required": review_required,
                  "conflict": conflict, "material_impact": material_impact, "created_at": now, "updated_at": now}
        self.repository.put_object("memory", record["memory_id"], record)
        return True, copy.deepcopy(record), None

    def approve_memory(self, memory_id, *, context=None, version=None, resolve_blockers=False, review_at=None):
        with self.repository.transaction():
            record = self.repository.get_object("memory", memory_id)
            if not record or not self._authorized(context, record, version):
                return False
            if review_at is not None:
                try:
                    if datetime.fromisoformat(review_at).tzinfo is None:
                        return False
                except (ValueError, TypeError):
                    return False
                record["review_at"] = review_at
            if self._blocked(record) and resolve_blockers is not True:
                return False
            if record["review_required"] and not record["review_at"]:
                return False
            if record["review_at"] and datetime.fromisoformat(record["review_at"]) <= self.now_fn():
                return False
            record.update(human_approved=True, approved_version=version, status="ACTIVA",
                          conflict=False, material_impact=False, updated_at=self.now_fn().isoformat())
            self.repository.put_object("memory", memory_id, record)
            return True

    def _blocked(self, record):
        return (record.get("conflict") or record.get("material_impact")
                or (record.get("review_required") and not record.get("review_at"))
                or (record.get("review_at") and datetime.fromisoformat(record["review_at"]) <= self.now_fn()))

    def query_memories_for_role(self, role, category=None, *, context=None, fragments=None):
        if role not in ("chief_of_staff", "product_architect", "research_evidence_analyst", "delivery_planner", "governance_risk"):
            raise MemoryAccessError("PERMISSION_DENIED: Rol no autorizado.")
        if not self._authorized(context):
            raise MemoryAccessError("PERMISSION_DENIED: Contexto local ausente.")
        results = []
        for record in self.memories.values():
            if (record.get("user_id") != context.user_id or record.get("status") != "ACTIVA"
                or not record.get("human_approved") or record.get("approved_version") != record.get("version")
                or self._blocked(record) or (category and record["category"] != category)):
                continue
            if role == "chief_of_staff":
                results.append(copy.deepcopy(record))
            elif role == "governance_risk":
                results.append({k: record[k] for k in ("memory_id", "version", "approved_version", "human_approved", "origin_mission_id")})
            elif fragments and record["memory_id"] in fragments:
                start, end = fragments[record["memory_id"]]
                if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(record["content"]):
                    raise MemoryAccessError("INVALID_INPUT: Fragmento fuera de limites.")
                results.append({"memory_id": record["memory_id"], "version": record["version"], "content": record["content"][start:end]})
        return results

    def update_memory(self, memory_id, new_content, *, context=None, version=None):
        with self.repository.transaction():
            record = self.repository.get_object("memory", memory_id)
            if not record or not self._authorized(context, record, version):
                return False, None, "PERMISSION_DENIED: Propietario, contexto o version invalida."
            if not isinstance(new_content, str) or not new_content.strip():
                return False, None, "INVALID_INPUT: Contenido vacio."
            record.setdefault('version_history', []).append({'version':version, 'status':'INACTIVA',
                                                            'retired_at':self.now_fn().isoformat()})
            record.update(version=version + 1, content=new_content.strip(), human_approved=False,
                          approved_version=None, status="PROPUESTA_PENDIENTE_APROBACION",
                          updated_at=self.now_fn().isoformat())
            self.repository.put_object("memory", memory_id, record)
            return True, copy.deepcopy(record), None

    def delete_memory(self, memory_id, *, context=None, version=None):
        with self.repository.transaction():
            record = self.repository.get_object("memory", memory_id)
            if not record or not self._authorized(context, record, version):
                return False
            tombstone = {k: record[k] for k in ("memory_id", "user_id", "origin_mission_id")}
            tombstone["deleted_at"] = self.now_fn().isoformat()
            self.repository._conn.execute("PRAGMA secure_delete=ON")
            self.repository.put_object("memory", memory_id, tombstone)
            return True
