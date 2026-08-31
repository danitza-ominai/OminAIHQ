"""OminAI HQ - Punto de composicion del Runtime de Agentes (PZ-004B).

Gestiona el registro explicito de especialistas, composicion de pasarela de modelos,
Chief of Staff y validacion de dependencias sin fallback silencioso.
Cumple estrictamente con CONTRATO-MVP-v1.md seccion 5 y FICHA-PZ-004B.md.
"""

from typing import Any, Dict, List, Optional, Tuple

import app.agent_gateway as agent_gateway
import app.approved_memory as approved_memory
import app.audit_query as audit_query
import app.chief_of_staff as chief_of_staff
import app.data_lifecycle as data_lifecycle
import app.delivery_planner as delivery_planner
import app.demo_intake as demo_intake
import app.evidence_registry as evidence_registry
import app.file_intake as file_intake
import app.governance_risk as governance_risk
import app.human_approvals as human_approvals
import app.image_intake as image_intake
import app.local_profile as local_profile
import app.local_repository as local_repository
import app.mission_controls as mission_controls
import app.product_architect as product_architect
import app.recovery as recovery
import app.research_analyst as research_analyst
import app.runtime_config as runtime_config
import app.runtime_contracts as runtime_contracts
import app.sanitized_dossier as sanitized_dossier
import app.source_reader as source_reader

REQUIRED_ROLES = [
    "chief_of_staff",
    "research_evidence_analyst",
    "product_architect",
    "delivery_planner",
    "governance_risk",
]


class HQRuntime:
    """Contenedor de composicion y resolucion de agentes para OminAI HQ."""

    def __init__(
        self,
        config: Optional[runtime_config.RuntimeConfig] = None,
        gateway: Optional[agent_gateway.AgentGateway] = None,
        reader: Optional[source_reader.SourceReader] = None,
        registry: Optional[evidence_registry.EvidenceRegistry] = None,
        file_intake_manager: Optional[file_intake.FileIntakeManager] = None,
        image_intake_manager: Optional[image_intake.ImageIntakeManager] = None,
        dossier_manager: Optional[sanitized_dossier.SanitizedDossierManager] = None,
        audit_engine: Optional[audit_query.AuditQueryEngine] = None,
        repository: Optional[local_repository.LocalRepository] = None,
        profile_manager: Optional[local_profile.LocalProfileManager] = None,
        recovery_manager: Optional[recovery.RecoveryManager] = None,
        memory_manager: Optional[approved_memory.ApprovedMemoryManager] = None,
        lifecycle_manager: Optional[data_lifecycle.DataLifecycleManager] = None,
        approvals_engine: Optional[human_approvals.HumanApprovalEngine] = None,
        controls_manager: Optional[mission_controls.MissionControlManager] = None,
    ) -> None:
        self.config = config or runtime_config.RuntimeConfig()
        self.repository = repository or local_repository.LocalRepository()
        self.gateway = gateway or agent_gateway.AgentGateway(config=self.config, repository=self.repository)
        if self.gateway.repository is not self.repository:
            if self.repository.db_path == ':memory:' or self.gateway.repository.db_path != self.repository.db_path:
                raise ValueError('INVALID_INPUT: Gateway y runtime deben compartir repositorio.')
        self.reader = reader or source_reader.SourceReader()
        self.evidence_registry = registry or evidence_registry.EvidenceRegistry()
        self.file_intake = file_intake_manager or file_intake.FileIntakeManager()
        self.image_intake = image_intake_manager or image_intake.ImageIntakeManager()
        self.dossier_manager = dossier_manager or sanitized_dossier.SanitizedDossierManager()
        self.audit_engine = audit_engine or audit_query.AuditQueryEngine(repository=self.repository)
        self.profile_manager = profile_manager or local_profile.LocalProfileManager()
        self.recovery = recovery_manager or recovery.RecoveryManager(repository=self.repository, config=self.config)
        self.memory = memory_manager or approved_memory.ApprovedMemoryManager(repository=self.repository)
        self.lifecycle = lifecycle_manager or data_lifecycle.DataLifecycleManager(
            repository=self.repository,
            memory_manager=self.memory,
            evidence_reg=self.evidence_registry,
        )
        self.approvals = approvals_engine or human_approvals.HumanApprovalEngine(
            repository=self.repository,
            audit_engine=self.audit_engine,
            profile_manager=self.profile_manager,
        )
        self.memory.authority = self.approvals
        self.memory.repository = self.repository
        self.controls = controls_manager or mission_controls.MissionControlManager(
            repository=self.repository,
            recovery_mgr=self.recovery,
            config=self.config,
        )
        self.chief_of_staff = chief_of_staff.ChiefOfStaff(gateway=self.gateway, memory_manager=self.memory)
        self.research_analyst = research_analyst.ResearchEvidenceAnalyst(
            reader=self.reader,
            gateway=self.gateway,
        )
        self.product_architect = product_architect.ProductArchitect(
            gateway=self.gateway,
        )
        self.delivery_planner = delivery_planner.DeliveryPlanner(
            gateway=self.gateway,
        )
        self.governance_risk = governance_risk.GovernanceRisk(
            gateway=self.gateway,
        )
        self.specialists: Dict[str, Any] = {
            "research_evidence_analyst": self.research_analyst,
            "product_architect": self.product_architect,
            "delivery_planner": self.delivery_planner,
            "governance_risk": self.governance_risk,
        }

    def register_specialist(self, role: str, agent_instance: Any) -> None:
        """Registra un agente especialista en la composicion del runtime."""
        self.specialists[role] = agent_instance

    def get_specialist(self, role: str) -> Optional[Any]:
        """Obtiene un agente especialista por su rol."""
        if role == "chief_of_staff":
            return self.chief_of_staff
        return self.specialists.get(role)

    def validate_runtime_readiness(self) -> Tuple[bool, List[str]]:
        """Verifica que todos los roles requeridos esten registrados. Falla si alguno falta."""
        missing = []
        for role in REQUIRED_ROLES:
            if role == "chief_of_staff":
                if not self.chief_of_staff:
                    missing.append(role)
            else:
                if role not in self.specialists or self.specialists[role] is None:
                    missing.append(role)

        return len(missing) == 0, missing

    def create_local_mission(self, fields, context):
        """Adapt the existing synthetic intake; SQLite owns the subsequent lifecycle."""
        import copy
        import json
        import uuid
        from pathlib import Path
        from app.demo_plan_review import PlanReviewSession
        if not self.approvals.check_context(context):
            return False, None, "PERMISSION_DENIED: Falta contexto humano local."
        allowed = {"mission_id", "title", "objective", "context", "expected_result"}
        if not isinstance(fields, dict) or set(fields) - allowed:
            return False, None, "INVALID_INPUT: Campos no admitidos."
        if any(not isinstance(fields.get(k), str) or not fields[k].strip()
               for k in ("title", "objective", "context", "expected_result")):
            return False, None, "INVALID_INPUT: Complete titulo, objetivo, contexto y resultado esperado."
        mid = fields.get("mission_id") or "MSN-" + uuid.uuid4().hex
        import re
        if not re.fullmatch(r"MSN-[A-Za-z0-9_-]{1,100}", mid):
            return False, None, "INVALID_INPUT: mission_id invalido."
        try:
            with self.repository.transaction():
                if self.repository.get_mission(mid):
                    return False, None, "INVALID_INPUT: La mision ya existe."
                raw = json.loads((Path(__file__).resolve().parent.parent / "examples/demo_mission.json").read_text(encoding="utf-8"))
                raw.update({k: fields[k] for k in ("title", "objective", "context", "expected_result")})
                raw["user_id"] = context.user_id
                raw["simulation_status"] = "SIMULADA"
                session = PlanReviewSession(id_generator=lambda prefix: mid if prefix.startswith("MSN") else prefix + "-" + uuid.uuid4().hex)
                code, env = session.init_from_intake(raw_data=raw)
                if code not in (0, 3) or not env.get("plan"):
                    return False, None, "INVALID_INPUT: El intake no produjo un plan revisable."
                # The intake's draft request is not a durable human decision.
                nuclear = copy.deepcopy(env["mission"])
                nuclear["approval_refs"] = []
                memories = self.memory.query_memories_for_role("chief_of_staff", context=context)
                env["plan"]["memory_refs"] = [{"memory_id": mem["memory_id"], "version": mem["version"]} for mem in memories]
                mission = {
                    **fields, "mission_id": mid, "user_id": context.user_id, "version": nuclear["record_version"],
                    "status": "PLAN_EN_REVISION", "current_state": "PLAN_EN_REVISION",
                    "simulation_status": "SIMULADA", "nuclear": nuclear,
                    "brief": env["brief"], "plan": env["plan"], "tasks": [],
                    "task_results": {}, "evidence_ids": [], "agent_requests": 0,
                    "active_seconds": 0.0, "cost_usd": 0.0, "cost_kind": "SIMULADA",
                }
                for t in mission["plan"]["tasks"]:
                    from app.vbp_validation import task_from_plan
                    task = task_from_plan(t, nuclear)
                    mission["tasks"].append(task)
                ok, err = self.repository.save_mission(mission)
                if not ok:
                    raise ValueError(err)
                ok, req, err = self.approvals.create_approval_request(
                    mid, "GATE_1_PLAN", {"brief": mission["brief"], "plan": mission["plan"]})
                if not ok:
                    raise ValueError(err)
                mission = self.repository.get_mission(mid)
                mission.update(plan_fingerprint=req["fingerprint"], approval_id=req["approval_id"],
                               idempotency_key=req["idempotency_key"])
                self._save_runtime_milestone(mission, "PLAN_EN_REVISION")
                return True, mission, None
        except Exception as exc:
            code = "INVALID_INPUT" if "MAX_CONCURRENT" in str(exc) else "SYSTEM_ERROR"
            return False, None, code + ": No se pudo guardar la mision."

    def _save_runtime_milestone(self, mission, milestone, *, task_id=None):
        import uuid
        from datetime import datetime, timezone
        with self.repository.transaction():
            previous = self.repository.get_mission(mission["mission_id"])
            ok, err = self.repository.save_mission(mission)
            if not ok:
                raise RuntimeError(err)
            key = uuid.uuid4().hex
            now = datetime.now(timezone.utc).isoformat()
            mission.update(self.repository.get_mission(mission["mission_id"]))
            previous_state = previous['status'] if previous else None
            if task_id and previous:
                previous_state = next(t['status'] for t in previous['tasks'] if t['task_id'] == task_id)
            self.repository.save_event(self.repository.build_event(
                mission, milestone, event_id="EVT-" + key, timestamp=now,
                previous_state=previous_state, task_id=task_id,
                approval_id=mission.get('pending_GATE_1_PLAN') if task_id else None))
            self.repository.save_runtime_checkpoint(mission, "CHK-" + key, now)

    def check_execution_authority(self, mission):
        from app.human_approvals import document_fingerprint
        for ref in mission.get('plan', {}).get('memory_refs', []):
            memory = self.repository.get_object('memory', ref['memory_id'])
            if (not memory or memory.get('user_id') != mission.get('user_id')
                or memory.get('version') != ref['version'] or memory.get('approved_version') != ref['version']
                or not memory.get('human_approved') or memory.get('status') != 'ACTIVA'
                or self.memory._blocked(memory)):
                return False
        request_id = mission.get("pending_GATE_1_PLAN")
        stored = self.repository.get_object("approval_request", request_id or "")
        if (not stored or stored["record"].get("decision") != "APROBAR"
                or stored["request"].get("status") != "CONSUMIDA"
                or stored["record"].get("status") != "CONSUMIDA"):
            return False
        candidate = {"brief": mission.get("brief"), "plan": mission.get("plan")}
        return (stored["request"]["version"] <= mission["version"]
                and stored["record"]["version_or_fingerprint"] == document_fingerprint(candidate, "GATE_1_PLAN"))

    def execute_local_simulation(self, mission_id, context, *, one_step=False):
        """Commit intent before each synthetic call and each confirmed result separately."""
        import copy
        import time
        from app.simulated_specialists import SimulatedSpecialistRunner
        from app import vbp_document, vbp_validation, runtime_contracts
        if not self.approvals.check_context(context):
            return False, None, "PERMISSION_DENIED: Falta contexto humano local."
        for _ in range(4):
            try:
                with self.repository.transaction():
                    mission = self.repository.get_mission(mission_id)
                    if not mission:
                        return False, None, "NOT_FOUND: Mision inexistente."
                    if mission.get("user_id") != context.user_id:
                        return False, None, "PERMISSION_DENIED: Propietario distinto."
                    if mission["status"] not in ("AUTORIZADA_PARA_EJECUTAR", "EN_EJECUCION"):
                        return False, None, "PERMISSION_DENIED: Estado no ejecutable."
                    if not self.check_execution_authority(mission):
                        return False, None, "PERMISSION_DENIED: Plan no aprobado o modificado."
                    recovered, _, recovery_error = self.recovery.recover_mission(mission_id)
                    if not recovered:
                        return False, None, "INVALID_INPUT: " + recovery_error
                    if mission.get("evidence_ids") and not human_approvals.evidence_available(self.repository, mission):
                        return False, None, "NOT_FOUND: EVIDENCIA_NO_DISPONIBLE."
                    if mission.get("inflight"):
                        return False, None, "SYSTEM_ERROR: ESTADO_INDETERMINADO; requiere revision."
                    if mission.get("active_seconds", 0) >= 1200:
                        return False, None, "BUDGET_EXHAUSTED: Tiempo activo agotado."
                    task = next((t for t in mission["tasks"] if t["status"] != "COMPLETA"), None)
                    if task is None:
                        break
                    if any(not any(t["task_id"] == dep and t["status"] == "COMPLETA" for t in mission["tasks"])
                           for dep in task["dependencies"]):
                        return False, None, "DEPENDENCY_FAILED: Dependencia incompleta."
                    if task["attempt"] >= 2:
                        return False, None, "BUDGET_EXHAUSTED: Intentos agotados."
                    reservation = self.repository.reserve_call(mission_id, task["task_id"], 0)
                    task["attempt"] += 1
                    task["status"] = "EN_CURSO"
                    mission.update(status="EN_EJECUCION", current_state="EN_EJECUCION",
                                   inflight=reservation, agent_requests=mission["agent_requests"] + 1)
                    self._save_runtime_milestone(mission, "LLAMADA_INICIADA", task_id=task['task_id'])
                start = time.monotonic()
                runner = getattr(self, "simulation_provider", None) or SimulatedSpecialistRunner()
                evidence = {eid: self.repository.get_object("evidence", eid) for eid in mission["evidence_ids"]}
                nuclear = copy.deepcopy(mission["nuclear"])
                nuclear["current_state"] = "EN_EJECUCION"
                result, new_evidence = runner.execute_task(task, nuclear, evidence, mission["task_results"])
                elapsed = time.monotonic() - start
                validator = runtime_contracts.RuntimeContractsValidator()
                valid, errors = validator.validate_structure("agent-result", result)
                if not valid:
                    raise ValueError(errors)
                if result["mission_id"] != mission_id or result["task_id"] != task["task_id"]:
                    raise ValueError("Identidad de resultado distinta.")
                with self.repository.transaction():
                    current = self.repository.get_mission(mission_id)
                    if current["status"] != "EN_EJECUCION" or current.get("inflight") != reservation:
                        raise ValueError("Estado modificado durante llamada; resultado incierto.")
                    self.repository.reconcile_call(reservation, 0)
                    for ev in new_evidence:
                        # An explicitly synthetic original, not a claim that a real PDF was fetched.
                        ev["title"] = "[SIMULADA] " + ev["title"]
                        ev["limitations"].append("Original sintetico persistido; fuente real NO_VERIFICADA.")
                        ev["fingerprint"] = runtime_contracts.compute_evidence_fingerprint(ev)
                        valid, errors = validator.validate_structure("evidence", ev)
                        if not valid:
                            raise ValueError(errors)
                        self.repository.put_object("evidence", ev["evidence_id"], ev)
                        self.repository.put_object("evidence_original", ev["evidence_id"],
                                                   {"fingerprint": ev["fingerprint"], "mode": "SIMULADA"})
                        current["evidence_ids"].append(ev["evidence_id"])
                    current["inflight"] = None
                    current["active_seconds"] += elapsed
                    current["task_results"][task["task_id"]] = result
                    current_task = next(t for t in current["tasks"] if t["task_id"] == task["task_id"])
                    current_task["status"] = {"SUCCESS": "COMPLETA", "PARTIAL": "PARCIAL",
                                              "BLOCKED": "BLOQUEADA", "FAILED": "FALLIDA"}[result["status"]]
                    if result["status"] != "SUCCESS" or elapsed >= 300:
                        current.update(status="PAUSADA", current_state="PAUSADA",
                                       resumable_state="EN_EJECUCION", pause_reason="RESULTADO_NO_COMPLETO_O_TIEMPO")
                    self._save_runtime_milestone(current, "TAREA_CONFIRMADA", task_id=task['task_id'])
                if current["status"] == "PAUSADA":
                    return False, current, "DEPENDENCY_FAILED: Resultado no completo; ejecucion pausada."
                if one_step and any(t["status"] != "COMPLETA" for t in current["tasks"]):
                    return True, current, None
            except Exception:
                # A durable inflight reservation is intentionally NOT refunded.
                return False, None, "SYSTEM_ERROR: Estado incierto; no repetir la llamada automaticamente."
        try:
            with self.repository.transaction():
                mission = self.repository.get_mission(mission_id)
                if mission["status"] != "EN_EJECUCION" or any(t["status"] != "COMPLETA" for t in mission["tasks"]):
                    return False, None, "DEPENDENCY_FAILED: Tareas incompletas."
                mission.update(status="EN_CONSOLIDACION", current_state="EN_CONSOLIDACION")
                self._save_runtime_milestone(mission, "EN_CONSOLIDACION")
                envelope = {
                    "mission": mission["nuclear"], "brief": mission["brief"], "plan": mission["plan"],
                    "task_results": mission["task_results"],
                    "tasks": mission["tasks"],
                    "evidence_store": {eid: self.repository.get_object("evidence", eid) for eid in mission["evidence_ids"]},
                    "evidence_originals": {eid: self.repository.get_object("evidence_original", eid) for eid in mission["evidence_ids"]},
                    "events": self.repository.list_events(mission_id),
                    "approvals": [self.repository.get_object("approval_record", mission["pending_GATE_1_PLAN"])],
                }
                vbp = vbp_document.assemble_vbp_data(envelope)
                vbp_document.prepare_simulated_bilingual(vbp, envelope)
                mission['translation_status'] = 'PENDIENTE' if any('TRANSLATION PENDING' in s['content'] for s in vbp['sections']) else 'PREPARADA_ES_EN'
                mission.update(status="EN_EVALUACION", current_state="EN_EVALUACION")
                self._save_runtime_milestone(mission, "EN_EVALUACION")
                mission["evaluation_report"] = vbp_validation.VBPValidator().evaluate_vbp(
                    vbp, envelope["evidence_store"], context=vbp_validation.build_evaluation_context(envelope))
                mission["evaluation_report"]["simulation_status"] = "SIMULADA"

                mission.update(status="VBP_EN_REVISION", current_state="VBP_EN_REVISION")
                self._save_runtime_milestone(mission, "VBP_EN_REVISION")
                # Las transiciones de evaluacion/revision tambien versionan la
                # mision. El VBP se asocia a la version vigente antes de pedir la
                # Puerta 2; su huella debe cubrir ese cambio de referencia.
                mission = self.repository.get_mission(mission_id)
                vbp["mission_version"] = mission["version"]
                vbp["fingerprint"] = runtime_contracts.compute_vbp_manifest_fingerprint(vbp)
                ok, req, err = self.approvals.create_approval_request(mission_id, "GATE_2_VBP", vbp)
                if not ok:
                    raise RuntimeError(err)
                mission = self.repository.get_mission(mission_id)
                mission["approval_request"] = req
                self._save_runtime_milestone(mission, "SOLICITUD_VBP")
                return True, mission, None
        except Exception:
            return False, None, "SYSTEM_ERROR: Consolidacion no confirmada; conserve el checkpoint."

    def control_local_mission(self, mission_id, action, context, reason=""):
        if not self.approvals.check_context(context):
            return False, None, "PERMISSION_DENIED: Falta contexto humano local."
        try:
            with self.repository.transaction():
                mission = self.repository.get_mission(mission_id)
                if not mission:
                    return False, None, "NOT_FOUND: Mision inexistente."
                if mission.get("user_id") != context.user_id:
                    return False, None, "PERMISSION_DENIED: Propietario distinto."
                if action == "resume":
                    recovered, _, recovery_error = self.recovery.recover_mission(mission_id)
                    if not recovered:
                        return False, None, "INVALID_INPUT: " + recovery_error
                    if mission.get("inflight"):
                        return False, None, "SYSTEM_ERROR: ESTADO_INDETERMINADO."
                    if mission.get("active_seconds", 0) >= 1200 or self.repository.budget_snapshot()["committed_usd"] >= 22.5:
                        return False, None, "BUDGET_EXHAUSTED: Limite agotado."
                    if mission.get("agent_requests", 0) >= 15 or (mission.get("resumable_state") not in ("BORRADOR", "PLAN_EN_REVISION") and not self.check_execution_authority(mission)):
                        return False, None, "PERMISSION_DENIED: Autorizacion o limite no vigente."
                    if mission.get("evidence_ids") and not human_approvals.evidence_available(self.repository, mission):
                        return False, None, "NOT_FOUND: EVIDENCIA_NO_DISPONIBLE."
                    result = self.controls.resume_mission(mission_id, actor_role=context.actor_role)
                elif action == "pause":
                    result = self.controls.pause_mission(mission_id, reason or "Pausa de usuario", context.actor_role)
                else:
                    result = self.controls.cancel_mission(mission_id, reason or "Cancelacion de usuario", context.actor_role)
                if result[0]:
                    # Los controles persisten una transicion y el repositorio
                    # asigna la nueva version; el checkpoint/evento siguiente
                    # debe partir del registro ya versionado.
                    result = (True, self.repository.get_mission(mission_id), result[2])
                    self._save_runtime_milestone(result[1], action.upper())
                return result
        except Exception:
            return False, None, "SYSTEM_ERROR: Control no confirmado."
