"""OminAI HQ - Repositorio Transaccional Local SQLite (PZ-010A).

Implementa la persistencia duradera, aislamiento por mision, atomicidad de aprobaciones
y regla de una sola mision activa conforme a CONTRATO-MVP-v1.md seccion 9.0, 11.2, 11.5 y RF-022.
"""

import json
import copy
import hashlib
import threading
import uuid
from contextlib import contextmanager
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ACTIVE_STATES = {
    "BORRADOR",
    "PLAN_EN_REVISION",
    "AUTORIZADA_PARA_EJECUTAR",
    "EN_EJECUCION",
    "EN_CONSOLIDACION",
    "VBP_EN_REVISION", "PAUSADA", "BLOQUEADA", "EN_EVALUACION", "VBP_APROBADO", "VBP_RECHAZADO",
}


class LocalRepository:
    """Repositorio SQLite transaccional local para el perfil, misiones, decisiones y eventos."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            from app.runtime_config import configured_repository_path
            db_path = configured_repository_path()
        self.db_path = db_path
        self._lock = threading.RLock()
        self._depth = 0
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_db()

    @contextmanager
    def transaction(self):
        """Nested savepoints never commit the caller's transaction."""
        with self._lock:
            outer = self._depth == 0
            savepoint = "sp_" + uuid.uuid4().hex
            self._conn.execute("BEGIN IMMEDIATE" if outer else "SAVEPOINT " + savepoint)
            self._depth += 1
            try:
                yield
                self._conn.execute("COMMIT" if outer else "RELEASE SAVEPOINT " + savepoint)
            except BaseException:
                if outer:
                    self._conn.rollback()
                else:
                    self._conn.execute("ROLLBACK TO SAVEPOINT " + savepoint)
                    self._conn.execute("RELEASE SAVEPOINT " + savepoint)
                raise
            finally:
                self._depth -= 1

    def get_object(self, kind, key):
        with self._lock:
            row = self._conn.execute(
                "SELECT payload FROM durable_objects WHERE kind=? AND object_key=?", (kind, key)
            ).fetchone()
            return json.loads(row[0]) if row else None

    def put_object(self, kind, key, payload):
        with self.transaction():
            self._conn.execute(
                "INSERT INTO durable_objects VALUES (?,?,?) ON CONFLICT(kind,object_key) "
                "DO UPDATE SET payload=excluded.payload",
                (kind, key, json.dumps(payload, allow_nan=False)),
            )

    def save_ledger(self, key, payload):
        if self.get_object("ledger", key) is not None:
            raise ValueError("INVALID_INPUT: Clave de idempotencia ya registrada.")
        self.put_object("ledger", key, payload)

    def save_event(self, event):
        from app.audit_query import AuditQueryEngine
        engine = AuditQueryEngine()
        event_to_save = copy.deepcopy(event)
        if "result_summary" in event_to_save and isinstance(event_to_save["result_summary"], str):
            event_to_save["result_summary"] = engine.sanitize_audit_text(event_to_save["result_summary"])
        if "action" in event_to_save and isinstance(event_to_save["action"], str):
            event_to_save["action"] = engine.sanitize_audit_text(event_to_save["action"])
        self.validate_core("event", event_to_save)
        with self.transaction():
            mission = self.get_mission(event_to_save["mission_id"])
            if not mission or event_to_save["version"] != mission["version"]:
                raise ValueError("INVALID_INPUT: Evento de mision/version inexistente.")
            if event_to_save['task_id'] is not None and not any(t['task_id'] == event_to_save['task_id'] for t in mission.get('tasks', [])):
                raise ValueError('INVALID_INPUT: Tarea del evento inexistente.')
            if event_to_save['related_approval_id'] is not None:
                approval = self.get_object('approval_request', event_to_save['related_approval_id'])
                if not approval or approval['request']['mission_id'] != mission['mission_id']:
                    raise ValueError('INVALID_INPUT: Aprobacion del evento cruzada o inexistente.')
            self._conn.execute(
                "INSERT INTO audit_events VALUES (?,?,?,?,?,?,?)",
                (event_to_save["event_id"], event_to_save["mission_id"], event_to_save.get("task_id"),
                 event_to_save["action"], event_to_save["result_summary"], event_to_save["timestamp"],
                 hashlib.sha256(json.dumps(event_to_save, sort_keys=True).encode()).hexdigest()),
            )
            self.put_object("event", event_to_save["event_id"], event_to_save)

    @staticmethod
    def validate_core(kind, value):
        from jsonschema import Draft202012Validator
        from app.demo_intake import get_format_checker
        schema = json.loads((Path(__file__).resolve().parent.parent / "contracts" / "core" / (kind + ".schema.json")).read_text(encoding="utf-8"))
        if not Draft202012Validator(schema, format_checker=get_format_checker()).is_valid(value):
            raise ValueError("SCHEMA_INVALID: Registro nuclear invalido: " + kind)

    def build_event(self, mission, action, *, event_id, timestamp, actor="sistema",
                    actor_role="sistema", previous_state=None, approval_id=None, task_id=None):
        task = next((t for t in mission.get('tasks', []) if t['task_id'] == task_id), None)
        if task_id is not None and task is None:
            raise ValueError('INVALID_INPUT: Tarea de evento inexistente.')
        return {"schema_version": "1.0.0", "event_id": event_id,
                "mission_id": mission["mission_id"], "task_id": task_id,
                "actor": actor, "actor_role": actor_role, "action": action,
                "timestamp": timestamp, "version": mission["version"],
                "previous_state": previous_state, "new_state": task['status'] if task else mission["status"],
                "tool_or_category": "transformacion_determinista",
                "source_or_artifact": task_id or mission["mission_id"],
                "result_summary": action + " (SIMULADA)", "typed_error": None,
                "attempt": task['attempt'] if task else 0, "budget_consumed": {'dimension':'usd','amount':0} if task else None,
                "related_approval_id": approval_id, "idempotency_key": event_id}

    def build_checkpoint(self, mission, checkpoint_id, timestamp):
        from app.demo_plan_review import compute_checkpoint_fingerprint
        nuclear = mission["nuclear"]
        tasks = mission.get("tasks", [])
        cp = {"schema_version": "1.0.0", "checkpoint_id": checkpoint_id,
              "mission_id": mission["mission_id"], "mission_version": mission["version"],
              "state": mission["status"], "resumable_state": nuclear.get("resumable_state"),
              "tasks": [{"task_id": t["task_id"], "state": t["status"], "attempts": t["attempt"]} for t in tasks],
              "dependencies": [{"from_task": dep, "to_task": t["task_id"],
                                "satisfied": any(x["task_id"] == dep and x["status"] == "COMPLETA" for x in tasks)}
                               for t in tasks for dep in t["dependencies"]],
              "attempts": copy.deepcopy(nuclear["counters"]),
              "budgets_consumed": {"elapsed_mission_seconds": mission.get("active_seconds", 0),
                                   "budget_usd_spent": mission.get("cost_usd", 0)},
              "artifacts": list(mission.get("task_results", {})),
              "authorizations": [a["approval_id"] for a in self.list_approvals(mission["mission_id"])
                                 if a["decision"] in ("APROBAR", "APROBAR_CON_EXCEPCION")],
              "timestamp": timestamp, "fingerprint": "", "idempotency_key": checkpoint_id}
        cp["fingerprint"] = compute_checkpoint_fingerprint(cp)
        return cp

    def save_runtime_checkpoint(self, mission, checkpoint_id, timestamp):
        with self.transaction():
            mission["nuclear"]["last_checkpoint_id"] = checkpoint_id
            ok, error = self.save_mission(mission)
            if not ok:
                raise ValueError(error)
            persisted = self.get_mission(mission["mission_id"])
            checkpoint = self.build_checkpoint(persisted, checkpoint_id, timestamp)
            ok, error = self.save_checkpoint(checkpoint)
            if not ok:
                raise ValueError(error)
            self.put_object("checkpoint_integrity", checkpoint_id,
                            {"mission_hash": self.payload_hash(persisted)})
            mission.update(persisted)

    @staticmethod
    def payload_hash(payload):
        return hashlib.sha256(json.dumps(payload, sort_keys=True, allow_nan=False).encode()).hexdigest()

    def list_events(self, mission_id):
        rows = self._conn.execute(
            "SELECT event_id FROM audit_events WHERE mission_id=? ORDER BY rowid", (mission_id,)
        ).fetchall()
        return [self.get_object("event", row[0]) for row in rows]

    def current_mission_for_owner(self, user_id):
        rows = self._conn.execute('SELECT payload_json FROM missions WHERE user_id=? ORDER BY rowid DESC', (user_id,)).fetchall()
        missions = [json.loads(row[0]) for row in rows]
        return next((m for m in missions if m['status'] in ACTIVE_STATES), missions[0] if missions else None)

    def _init_db(self) -> None:
        """Inicializa el esquema de tablas transaccionales."""
        with self.transaction():
            self._conn.execute("CREATE TABLE IF NOT EXISTS durable_objects (kind TEXT, object_key TEXT, payload TEXT NOT NULL, PRIMARY KEY(kind,object_key))")
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    user_id TEXT PRIMARY KEY,
                    display_name TEXT NOT NULL,
                    email TEXT,
                    actor_role TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT
                );
            """)
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS missions (
                    mission_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    status TEXT NOT NULL,
                    version INTEGER NOT NULL DEFAULT 1,
                    current_state TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
            """)
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS approvals (
                    approval_id TEXT PRIMARY KEY,
                    mission_id TEXT NOT NULL,
                    approval_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    idempotency_key TEXT UNIQUE NOT NULL,
                    fingerprint TEXT NOT NULL,
                    comment TEXT,
                    actor TEXT NOT NULL,
                    decided_at TEXT NOT NULL
                );
            """)
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    checkpoint_id TEXT PRIMARY KEY,
                    mission_id TEXT NOT NULL,
                    milestone TEXT NOT NULL,
                    state_snapshot_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
            """)
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS evidences (
                    evidence_id TEXT PRIMARY KEY,
                    mission_id TEXT NOT NULL,
                    claim_id TEXT,
                    title TEXT NOT NULL,
                    source_locator TEXT NOT NULL,
                    confidence TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    fingerprint TEXT NOT NULL
                );
            """)
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_events (
                    event_id TEXT PRIMARY KEY,
                    mission_id TEXT NOT NULL,
                    task_id TEXT,
                    action TEXT NOT NULL,
                    result_summary TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    fingerprint TEXT NOT NULL
                );
            """)

    def save_profile(self, profile_data: dict) -> Tuple[bool, Optional[str]]:
        """Guarda o actualiza el perfil humano unico."""
        now_iso = datetime.now(timezone.utc).isoformat()
        try:
            with self.transaction():
                self._conn.execute(
                    """
                    INSERT INTO profiles (user_id, display_name, email, actor_role, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        display_name = excluded.display_name,
                        email = excluded.email,
                        updated_at = excluded.updated_at;
                    """,
                    (
                        profile_data["user_id"],
                        profile_data["display_name"],
                        profile_data.get("email"),
                        profile_data.get("actor_role", "usuario_humano"),
                        profile_data.get("created_at", now_iso),
                        now_iso,
                    ),
                )
            return True, None
        except Exception as e:
            return False, f"Fallo al guardar perfil: {str(e)}"

    def get_profile(self, user_id: str) -> Optional[dict]:
        """Obtiene el perfil registrado."""
        cur = self._conn.execute("SELECT * FROM profiles WHERE user_id = ?;", (user_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def save_mission(self, mission_data: dict) -> Tuple[bool, Optional[str]]:
        """Guarda o actualiza una mision verificando la regla de una sola mision activa concurrente."""
        incoming = copy.deepcopy(mission_data)
        existing = self.get_mission(incoming["mission_id"])
        mission_data = {**(existing or {}), **incoming}
        m_id = mission_data["mission_id"]
        status = mission_data.get("status", "BORRADOR")
        user_id = mission_data.get("user_id", "")
        title = mission_data.get("title", "Mision")
        previous_status = existing.get("status") if existing else None
        previous_version = existing.get("version", 1) if existing else None
        state_changed = bool(existing and status != previous_status)
        if existing and "version" in incoming:
            accepted_versions = {previous_version, previous_version + 1} if state_changed else {previous_version}
            if incoming["version"] not in accepted_versions:
                return False, "INVALID_INPUT: Version de mision obsoleta."
        version = (previous_version + 1) if state_changed else mission_data.get("version", 1)
        if type(version) is not int or version < 1:
            return False, "INVALID_INPUT: Version de mision invalida."
        mission_data["version"] = version
        mission_data["current_state"] = status

        # Una transicion de estado es una sola operacion de versionado. Todas las
        # referencias activas al registro se mueven juntas dentro de la transaccion
        # que finalmente persiste la mision.
        if state_changed:
            mission_data["tasks"] = copy.deepcopy(mission_data.get("tasks", []))
            for task in mission_data["tasks"]:
                if task.get("mission_id") == m_id and "mission_version" in task:
                    task["mission_version"] = version
        now_iso = datetime.now(timezone.utc).isoformat()

        if "nuclear" in mission_data:
            nuclear = copy.deepcopy(mission_data["nuclear"])
            if nuclear["mission_id"] != m_id or nuclear["user_id"] != user_id:
                return False, "PERMISSION_DENIED: Identidad nuclear incompatible."
            nuclear.update(current_state=status, record_version=version,
                           resumable_state=mission_data.get("resumable_state") if status in ("PAUSADA", "BLOQUEADA") else None)
            nuclear["counters"]["agent_requests"] = mission_data.get("agent_requests", 0)
            nuclear["counters"]["task_reasoning_attempts"] = max((t.get("attempt", 0) for t in mission_data.get("tasks", [])), default=0)
            nuclear["approval_refs"] = [a["approval_id"] for a in self.list_approvals(m_id)]
            try:
                self.validate_core("mission", nuclear)
            except ValueError as exc:
                return False, str(exc)
            mission_data["nuclear"] = nuclear

        # Comprobar regla de 1 sola mision activa simultanea
        if status in ACTIVE_STATES:
            cur = self._conn.execute(
                "SELECT mission_id FROM missions WHERE status IN ('BORRADOR', 'PLAN_EN_REVISION', 'AUTORIZADA_PARA_EJECUTAR', 'EN_EJECUCION', 'EN_CONSOLIDACION', 'VBP_EN_REVISION', 'PAUSADA', 'BLOQUEADA', 'EN_EVALUACION', 'VBP_APROBADO', 'VBP_RECHAZADO') AND mission_id != ?;",
                (m_id,),
            )
            existing_active = cur.fetchone()
            if existing_active:
                return False, f"MAX_CONCURRENT_MISSIONS_EXCEEDED: Ya existe una mision activa en curso ({existing_active['mission_id']})."

        try:
            with self.transaction():
                self._conn.execute(
                    """
                    INSERT INTO missions (mission_id, user_id, title, status, version, current_state, payload_json, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(mission_id) DO UPDATE SET
                        title = excluded.title,
                        status = excluded.status,
                        version = excluded.version,
                        current_state = excluded.current_state,
                        payload_json = excluded.payload_json,
                        updated_at = excluded.updated_at;
                    """,
                    (
                        m_id,
                        user_id,
                        title,
                        status,
                        version,
                        status,
                        json.dumps(mission_data),
                        mission_data.get("created_at", now_iso),
                        now_iso,
                    ),
                )
            return True, None
        except Exception as e:
            return False, f"Fallo al guardar mision: {str(e)}"

    def get_mission(self, mission_id: str) -> Optional[dict]:
        """Recupera el payload completo de una mision."""
        cur = self._conn.execute("SELECT payload_json FROM missions WHERE mission_id = ?;", (mission_id,))
        row = cur.fetchone()
        if row:
            return json.loads(row["payload_json"])
        return None

    def save_approval_atomic(
        self,
        approval_data: dict,
        mission_update: Optional[dict] = None,
        simulated_fault: bool = False,
    ) -> Tuple[bool, Optional[str]]:
        """Registra una aprobacion e idempotencia de forma atomica con el estado de la mision."""
        if mission_update:
            current = self.get_mission(mission_update["mission_id"])
            if current is None:
                return False, "NOT_FOUND: Mision inexistente."
            mission_update = {**current, **mission_update}
        idemp_key = approval_data["idempotency_key"]

        # Verificar idempotencia duradera
        cur = self._conn.execute("SELECT * FROM approvals WHERE idempotency_key = ?;", (idemp_key,))
        existing = cur.fetchone()
        if existing:
            fields = ("approval_id", "mission_id", "decision", "fingerprint")
            if any(existing[k] != approval_data[k] for k in fields):
                return False, "INVALID_INPUT: Conflicto de idempotencia."
            if existing["actor"] != approval_data.get("actor", "usuario_humano"):
                return False, "PERMISSION_DENIED: Identidad distinta."
            return True, None

        try:
            with self.transaction():
                self._conn.execute(
                    """
                    INSERT INTO approvals (approval_id, mission_id, approval_type, status, decision, idempotency_key, fingerprint, comment, actor, decided_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        approval_data["approval_id"],
                        approval_data["mission_id"],
                        approval_data.get("approval_type", "PLAN_EXECUTION"),
                        approval_data.get("status", "CONSUMIDA"),
                        approval_data["decision"],
                        idemp_key,
                        approval_data["fingerprint"],
                        approval_data.get("comment", ""),
                        approval_data.get("actor", "usuario_humano"),
                        approval_data.get("decided_at", datetime.now(timezone.utc).isoformat()),
                    ),
                )

                if mission_update:
                    ok, error = self.save_mission(mission_update)
                    if not ok:
                        raise ValueError(error)

                if simulated_fault:
                    raise RuntimeError("Fallo simulado para comprobar rollback transaccional.")

            return True, None
        except Exception as e:
            return False, f"Fallo transaccional en aprobacion: {str(e)}"

    def save_checkpoint(self, checkpoint_data: dict) -> Tuple[bool, Optional[str]]:
        """Registra un snapshot de estado duradero en un hito de la mision."""
        try:
            with self.transaction():
                self.validate_core("checkpoint", checkpoint_data)
                mission = self.get_mission(checkpoint_data["mission_id"])
                from app.demo_plan_review import compute_checkpoint_fingerprint
                if (not mission or checkpoint_data["fingerprint"] != compute_checkpoint_fingerprint(checkpoint_data)
                    or checkpoint_data != self.build_checkpoint(mission, checkpoint_data["checkpoint_id"], checkpoint_data["timestamp"])):
                    raise ValueError("INVALID_INPUT: Checkpoint incoherente con registros persistidos.")
                self._conn.execute(
                    """
                    INSERT INTO checkpoints (checkpoint_id, mission_id, milestone, state_snapshot_json, created_at)
                    VALUES (?, ?, ?, ?, ?);
                    """,
                    (
                        checkpoint_data["checkpoint_id"],
                        checkpoint_data["mission_id"],
                        checkpoint_data["state"],
                        json.dumps(checkpoint_data, allow_nan=False),
                        checkpoint_data["timestamp"],
                    ),
                )
            return True, None
        except Exception as e:
            return False, f"Fallo al guardar checkpoint: {str(e)}"

    def list_approvals(self, mission_id: str) -> List[dict]:
        """Lista todas las decisiones de aprobacion registradas para una mision."""
        cur = self._conn.execute("SELECT * FROM approvals WHERE mission_id = ? ORDER BY decided_at ASC;", (mission_id,))
        return [dict(r) for r in cur.fetchall()]

    def list_checkpoints(self, mission_id: str) -> List[dict]:
        """Lista todos los checkpoints registrados para una mision."""
        cur = self._conn.execute("SELECT * FROM checkpoints WHERE mission_id = ? ORDER BY created_at ASC;", (mission_id,))
        return [dict(r) for r in cur.fetchall()]

    def close(self) -> None:
        """Cierra la conexion SQLite de forma segura."""
        try:
            self._conn.close()
        except Exception:
            pass

    def budget_snapshot(self):
        rows = self._conn.execute("SELECT payload FROM durable_objects WHERE kind='call'").fetchall()
        calls = [json.loads(r[0]) for r in rows]
        spent = sum(c.get("actual_micros", 0) for c in calls)
        reserved = sum(c["reserved_micros"] for c in calls if c["status"] != "CONFIRMADA")
        return {"spent_usd": spent / 1000000, "reserved_usd": reserved / 1000000,
                "committed_usd": (spent + reserved) / 1000000,
                "cost_kind": "SIMULADA", "requests": len(calls),
                "alert": "STOP_100" if spent + reserved >= 25000000 else "PAUSE_90" if spent + reserved >= 22500000 else "WARN_70" if spent + reserved >= 17500000 else None}

    def reserve_call(self, mission_id, task_id, estimated_usd, *, max_budget_usd=25, max_requests=15):
        from decimal import Decimal, ROUND_CEILING
        amount = Decimal(str(estimated_usd))
        if not amount.is_finite() or amount < 0:
            raise ValueError("INVALID_INPUT: Reserva invalida.")
        micros = int((amount * 1000000).to_integral_value(rounding=ROUND_CEILING))
        ceiling = min(25, max_budget_usd)
        with self.transaction():
            usage = self.budget_snapshot()
            if usage["committed_usd"] >= ceiling * 0.9 or usage["committed_usd"] + micros / 1000000 > ceiling:
                raise ValueError("BUDGET_EXHAUSTED: Presupuesto compartido reservado o agotado.")
            calls = self._conn.execute("SELECT payload FROM durable_objects WHERE kind='call'").fetchall()
            for row in calls:
                prior = json.loads(row[0])
                if prior["mission_id"] == mission_id and prior["task_id"] == task_id and prior["status"] == "INDETERMINADA":
                    raise ValueError("SYSTEM_ERROR: Llamada indeterminada; no reintentar.")
            counters = self.get_object("usage", mission_id) or {"requests": 0, "tasks": {}}
            if counters["requests"] >= min(15, max_requests) or counters["tasks"].get(task_id, 0) >= 2:
                raise ValueError("BUDGET_EXHAUSTED: Solicitudes o intentos agotados.")
            counters["requests"] += 1
            counters["tasks"][task_id] = counters["tasks"].get(task_id, 0) + 1
            key = "CALL-" + uuid.uuid4().hex
            self.put_object("usage", mission_id, counters)
            self.put_object("call", key, {
                "mission_id": mission_id, "task_id": task_id, "reserved_micros": micros,
                "status": "INDETERMINADA", "actual_micros": 0,
            })
            return key

    def reconcile_call(self, key, actual_usd):
        from decimal import Decimal, ROUND_CEILING
        actual = Decimal(str(actual_usd))
        if not actual.is_finite() or actual < 0:
            raise ValueError("INVALID_INPUT: Consumo invalido.")
        actual_micros = int((actual * 1000000).to_integral_value(rounding=ROUND_CEILING))
        with self.transaction():
            call = self.get_object("call", key)
            if not call or call["status"] != "INDETERMINADA":
                raise ValueError("INVALID_INPUT: Reserva inexistente o confirmada.")
            if actual_micros > call["reserved_micros"]:
                raise ValueError("SYSTEM_ERROR: Consumo excede reserva; mantener llamada incierta.")
            call.update(status="CONFIRMADA", actual_micros=actual_micros)
            self.put_object("call", key, call)
