"""Durable human gates for the integrated SIMULADA runtime; no network authority."""
import copy
import hashlib
import json
import uuid
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from typing import Optional

import app.audit_query as audit_query
import app.local_profile as local_profile
import app.local_repository as local_repository
import app.runtime_contracts as runtime_contracts

VALID_GATES = {"GATE_1_PLAN", "GATE_2_VBP"}
VALID_DECISIONS = {"APROBAR", "RECHAZAR", "SOLICITAR_CAMBIOS", "APROBAR_CON_EXCEPCION"}
DEFAULT_EXPIRATION_SECONDS = 300


class HumanApprovalError(Exception):
    pass


@dataclass(frozen=True)
class LocalHumanContext:
    """Process-local capability issued explicitly by the trusted local adapter."""
    user_id: str
    actor_role: str = "usuario_humano"


def json_dumps_canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def document_fingerprint(document, gate):
    if gate == "GATE_2_VBP":
        return runtime_contracts.compute_vbp_manifest_fingerprint(document)
    return "sha256:" + hashlib.sha256(json_dumps_canonical(document).encode()).hexdigest()


def evidence_available(repository, mission):
    ids = mission.get("evidence_ids", [])
    if not ids:
        return False
    for eid in ids:
        evidence = repository.get_object("evidence", eid)
        original = repository.get_object("evidence_original", eid)
        if not evidence or not original or evidence.get("mission_id") != mission["mission_id"]:
            return False
        if original.get("fingerprint") != evidence.get("fingerprint"):
            return False
        if runtime_contracts.compute_evidence_fingerprint(evidence) != evidence["fingerprint"]:
            return False
    return True


class HumanApprovalEngine:
    def __init__(self, repository=None, audit_engine=None, profile_manager=None, now_fn=None):
        self.repository = repository or local_repository.LocalRepository()
        self.audit_engine = audit_engine or audit_query.AuditQueryEngine()
        self.profile_manager = profile_manager or local_profile.LocalProfileManager()
        self.now_fn = now_fn or (lambda: datetime.now(timezone.utc))
        self.local_context = None

    def bind_local_profile(self, profile):
        """Only startup/test code calls this; never invoked from request data."""
        if not isinstance(profile, dict) or not profile.get("user_id") or profile.get("actor_role") != "usuario_humano":
            raise HumanApprovalError("PERMISSION_DENIED: Perfil local invalido.")
        rows = self.repository._conn.execute("SELECT user_id FROM profiles").fetchall()
        if rows and any(row[0] != profile["user_id"] for row in rows):
            raise HumanApprovalError("PERMISSION_DENIED: Solo un perfil local.")
        ok, error = self.repository.save_profile(profile)
        if not ok:
            raise HumanApprovalError("SYSTEM_ERROR: No se pudo persistir el perfil.")
        self.local_context = LocalHumanContext(profile["user_id"])
        return self.local_context

    def check_context(self, context):
        return (context is not None and context is self.local_context
                and context.actor_role == "usuario_humano"
                and self.repository.get_profile(context.user_id) is not None)

    def create_approval_request(self, mission_id, gate_type, candidate_document,
                                expiration_seconds=300):
        if gate_type not in VALID_GATES or expiration_seconds != 300:
            return False, None, "INVALID_INPUT: Puerta o plazo invalido; plazo fijo 300 segundos."
        try:
            with self.repository.transaction():
                mission = self.repository.get_mission(mission_id)
                if not mission:
                    return False, None, "NOT_FOUND: Mision inexistente."
                expected = "PLAN_EN_REVISION" if gate_type == "GATE_1_PLAN" else "VBP_EN_REVISION"
                if mission.get("status") != expected or not mission.get("user_id"):
                    return False, None, "PERMISSION_DENIED: Estado o propietario invalido."
                fingerprint = document_fingerprint(candidate_document, gate_type)
                now = self.now_fn()
                approval_id = "APP-" + uuid.uuid4().hex
                request = {
                    "approval_id": approval_id, "mission_id": mission_id,
                    "gate_type": gate_type, "fingerprint": fingerprint,
                    "version": mission.get("version", 1), "status": "PENDIENTE",
                    "idempotency_key": "IDEMP-" + uuid.uuid4().hex,
                    "created_at": now.isoformat(), "expiration": (now + timedelta(seconds=300)).isoformat(),
                }
                record = {
                    "schema_version": "1.0.0", "approval_id": approval_id,
                    "user_id": mission["user_id"], "actor": mission["user_id"],
                    "actor_role": "usuario_humano", "action_approved": (f"Aprobacion del VBP {candidate_document['vbp_id']} v{candidate_document['version']} de la mision {mission_id}"
                        if gate_type == "GATE_2_VBP" and "vbp_id" in candidate_document else gate_type + ":" + mission_id),
                    "version_or_fingerprint": fingerprint, "timestamp": now.isoformat(),
                    "decision": None, "comment": "", "conditions": [],
                    "expiration": request["expiration"], "status": "PENDIENTE",
                    "idempotency_key": request["idempotency_key"],
                }
                self.repository.put_object("candidate", mission_id + ":" + gate_type, candidate_document)
                self.repository.put_object("approval_request", approval_id, {"request": request, "record": record})
                mission["pending_" + gate_type] = approval_id
                ok, err = self.repository.save_mission(mission)
                if not ok:
                    raise HumanApprovalError(err)
                return True, copy.deepcopy(request), None
        except Exception:
            return False, None, "SYSTEM_ERROR: No se pudo persistir la solicitud."

    def submit_human_decision(self, approval_request, decision, actor_role=None,
                              actor_user_id=None, comment="", conditions=None,
                              check_expiration=True, *, context=None, risks=None):
        # Identity is checked BEFORE replay. Wire fields never grant authority.
        if not self.check_context(context):
            return False, None, "PERMISSION_DENIED: Falta contexto humano local valido."
        if actor_role not in (None, context.actor_role) or actor_user_id not in (None, context.user_id):
            return False, None, "PERMISSION_DENIED: Identidad o rol no coincidente."
        if not isinstance(approval_request, dict) or decision not in VALID_DECISIONS:
            return False, None, "INVALID_INPUT: Solicitud o decision invalida."
        if not isinstance(comment, str) or len(comment) > 4000:
            return False, None, "INVALID_INPUT: Comentario invalido."
        conditions = [] if conditions is None else conditions
        risks = [] if risks is None else risks
        if any(not isinstance(items, list) or any(not isinstance(x, str) or not x.strip() for x in items)
               for items in (conditions, risks)):
            return False, None, "INVALID_INPUT: Condiciones o riesgos invalidos."
        if decision in ("RECHAZAR", "SOLICITAR_CAMBIOS", "APROBAR_CON_EXCEPCION") and not comment.strip():
            return False, None, "INVALID_INPUT: MOTIVO_REQUERIDO."
        if decision == "APROBAR_CON_EXCEPCION" and (not conditions or not risks):
            return False, None, "INVALID_INPUT: CONDICIONES_Y_RIESGOS_REQUERIDOS."
        try:
            with self.repository.transaction():
                stored = self.repository.get_object("approval_request", approval_request.get("approval_id", ""))
                if not stored:
                    return False, None, "NOT_FOUND: Solicitud inexistente."
                request, record = stored["request"], stored["record"]
                mission = self.repository.get_mission(request["mission_id"])
                if not mission:
                    return False, None, "NOT_FOUND: Mision inexistente."
                if mission.get("user_id") != context.user_id or record["user_id"] != context.user_id:
                    return False, None, "PERMISSION_DENIED: Propietario distinto."
                required = ("approval_id", "mission_id", "gate_type", "fingerprint", "idempotency_key")
                if any(approval_request.get(k) != request[k] for k in required):
                    if not (record["status"] == "CONSUMIDA"
                            and approval_request.get("fingerprint") == request.get("original_fingerprint")
                            and all(approval_request.get(k) == request[k]
                                    for k in required if k != "fingerprint")):
                        return False, None, "INVALID_INPUT: Solicitud cruzada o manipulada."
                for k in ("version", "expiration", "created_at"):
                    if k in approval_request and approval_request[k] != request[k]:
                        if (k == "version" and record["status"] == "CONSUMIDA"
                                and approval_request[k] == request.get("original_version")):
                            continue
                        return False, None, "INVALID_INPUT: Version o plazo manipulado."
                command = {k: (approval_request[k]
                              if k == "fingerprint" and approval_request.get(k) == request.get("original_fingerprint")
                              else request[k]) for k in required}
                command.update(decision=decision, actor=context.user_id, comment=comment,
                               conditions=conditions, risks=risks)
                ledger = self.repository.get_object("ledger", request["idempotency_key"])
                if ledger:
                    if ledger["command"] != command:
                        return False, None, "INVALID_INPUT: Conflicto de idempotencia."
                    return True, ledger["response"], None
                gate = request["gate_type"]
                expected = "PLAN_EN_REVISION" if gate == "GATE_1_PLAN" else "VBP_EN_REVISION"
                if record["status"] != "PENDIENTE" or mission.get("pending_" + gate) != request["approval_id"]:
                    return False, None, "INVALID_INPUT: Solicitud consumida u obsoleta."
                if self.now_fn() >= datetime.fromisoformat(request["expiration"]):
                    stored["record"]["status"] = "EXPIRADA"
                    stored["request"]["status"] = "EXPIRADA"
                    self.repository.put_object("approval_request", request["approval_id"], stored)
                    return False, None, "INVALID_INPUT: SOLICITUD_EXPIRADA."
                if mission.get("status") != expected or mission.get("version", 1) != request["version"]:
                    return False, None, "INVALID_INPUT: Estado o version obsoleta."
                candidate = self.repository.get_object("candidate", mission["mission_id"] + ":" + gate)
                if not candidate or document_fingerprint(candidate, gate) != request["fingerprint"]:
                    return False, None, "INVALID_INPUT: Huella de la version vigente distinta."
                approved = decision in ("APROBAR", "APROBAR_CON_EXCEPCION")
                if gate == "GATE_1_PLAN" and decision == "APROBAR_CON_EXCEPCION":
                    return False, None, "INVALID_INPUT: El Plan no admite excepcion."
                if gate == "GATE_2_VBP" and approved:
                    valid, errors = runtime_contracts.RuntimeContractsValidator().validate_structure("vbp", candidate)
                    if not valid or candidate.get("mission_id") != mission["mission_id"] or candidate.get("mission_version") != mission["version"]:
                        return False, None, "SCHEMA_INVALID: VBP candidato fuera de contrato o de version."
                    if not evidence_available(self.repository, mission):
                        return False, None, "NOT_FOUND: EVIDENCIA_NO_DISPONIBLE."
                    report = mission.get("evaluation_report", {})
                    if report.get("verdict") not in ("PASA", "PASA_CON_CONDICIONES", "NO_PASA"):
                        return False, None, "INVALID_INPUT: Evaluacion no disponible."
                    if report["verdict"] == "NO_PASA" and decision == "APROBAR":
                        return False, None, "PERMISSION_DENIED: NO_PASA bloquea aprobacion ordinaria."
                    if report["verdict"] == "PASA_CON_CONDICIONES" and not conditions:
                        return False, None, "INVALID_INPUT: CONDICIONES_REQUERIDAS."
                now = self.now_fn().isoformat()
                new_status = ("AUTORIZADA_PARA_EJECUTAR" if approved else "PLAN_EN_REVISION") if gate == "GATE_1_PLAN" else ("VBP_APROBADO" if approved else "VBP_RECHAZADO")
                mission.update(status=new_status, current_state=new_status)
                record.update(status="CONSUMIDA", decision=decision, comment=comment,
                              conditions=conditions, timestamp=now)
                response = {
                    "approval_id": request["approval_id"], "mission_id": mission["mission_id"],
                    "gate_type": gate, "decision": decision, "status": "CONSUMIDA",
                    "new_mission_status": new_status, "actor": context.user_id, "decided_at": now,
                }
                approval = {
                    "approval_id": request["approval_id"], "mission_id": mission["mission_id"],
                    "approval_type": gate, "status": "CONSUMIDA", "decision": decision,
                    "idempotency_key": request["idempotency_key"], "fingerprint": request["fingerprint"],
                    "comment": comment, "actor": context.user_id, "decided_at": now,
                }
                if gate == "GATE_2_VBP" and approved:
                    candidate["approval_status"] = "APROBADO" if decision == "APROBAR" else "APROBADO_CON_EXCEPCION"
                    candidate["human_approval_ref"] = request["approval_id"]
                    candidate["fingerprint"] = request["fingerprint"]
                    self.repository.put_object("candidate", mission["mission_id"] + ":" + gate, candidate)
                ok, err = self.repository.save_approval_atomic(approval, mission)
                if not ok:
                    raise HumanApprovalError(err)
                mission = self.repository.get_mission(mission["mission_id"])
                stored["record"] = record
                stored["request"]["status"] = "CONSUMIDA"
                stored["request"]["version"] = request["version"]
                stored["request"]["fingerprint"] = request["fingerprint"]
                self.repository.put_object("approval_request", request["approval_id"], stored)
                self.repository.put_object("approval_record", request["approval_id"], record)
                self.repository.save_event(self.repository.build_event(
                    mission, "decision_humana_" + gate + ":" + decision,
                    event_id="EVT-" + request["approval_id"], timestamp=now,
                    actor=context.user_id, actor_role="usuario_humano",
                    previous_state=expected, approval_id=request["approval_id"]))
                self.repository.save_runtime_checkpoint(mission, "CHK-" + request["approval_id"], now)
                self.repository.save_ledger(request["idempotency_key"], {"command": command, "response": response})
                return True, response, None
        except Exception:
            return False, None, "SYSTEM_ERROR: La decision no se confirmo; transaccion revertida."
