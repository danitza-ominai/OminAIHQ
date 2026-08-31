"""OminAI HQ - Motor secuencial de tareas SIMULADA (PZ-003D).

Implementa la ejecucion secuencial y determinista de las tareas del plan aprobado,
aplicando las transiciones MT-006 y MT-008 de la maquina de estados de mision,
y las transiciones TT-001 a TT-006 de la maquina de estados de tareas.
Detiene el recorrido en EN_CONSOLIDACION sin autoaprobar el VBP ni pasar a estados terminales.
Cumple estrictamente con CONTRATO-MVP-v1.md y FICHA-PZ-003D.md.
"""

import copy
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import jsonschema
from jsonschema import Draft202012Validator

import app.demo_intake as demo_intake
import app.demo_plan_review as demo_plan_review
import app.runtime_contracts as runtime_contracts
from app.simulated_specialists import SimulatedSpecialistRunner


class MissionExecutionEngine:
    """Motor de ejecucion secuencial de tareas en memoria con control estricto de limites y estados."""

    def __init__(
        self,
        now_fn: Optional[Callable[[], datetime]] = None,
        id_generator: Optional[Callable[[str], str]] = None,
        monotonic_time_fn: Optional[Callable[[], float]] = None,
        fault_config: Optional[Dict[str, dict]] = None,
    ) -> None:
        self.now_fn = now_fn or (lambda: datetime.now(timezone.utc))
        self.id_generator = id_generator or (lambda prefix: f"{prefix}-{uuid.uuid4().hex[:8]}")
        self.monotonic_time_fn = monotonic_time_fn or (lambda: 0.0)

        (
            self.mission_schema,
            self.event_schema,
            self.error_schema,
            self.approval_schema,
            self.checkpoint_schema,
            self.state_machine,
        ) = demo_plan_review.load_all_contracts()

        (
            self.task_schema,
            self.agent_result_schema,
            self.evidence_schema,
            self.vbp_schema,
        ) = runtime_contracts.load_runtime_contracts()

        self.format_checker = demo_intake.get_format_checker()
        self.mission_validator = Draft202012Validator(self.mission_schema, format_checker=self.format_checker)
        self.event_validator = Draft202012Validator(self.event_schema, format_checker=self.format_checker)
        self.error_validator = Draft202012Validator(self.error_schema, format_checker=self.format_checker)
        self.approval_validator = Draft202012Validator(self.approval_schema, format_checker=self.format_checker)
        self.checkpoint_validator = Draft202012Validator(self.checkpoint_schema, format_checker=self.format_checker)
        self.task_validator = Draft202012Validator(self.task_schema, format_checker=self.format_checker)
        self.agent_result_validator = Draft202012Validator(self.agent_result_schema, format_checker=self.format_checker)
        self.evidence_validator = Draft202012Validator(self.evidence_schema, format_checker=self.format_checker)

        self.specialist_runner = SimulatedSpecialistRunner(
            now_fn=self.now_fn,
            id_generator=self.id_generator,
            fault_config=fault_config,
        )

        self.mission: Optional[dict] = None
        self.brief: Optional[dict] = None
        self.plan: Optional[dict] = None
        self.events: List[dict] = []
        self.approvals: List[dict] = []
        self.checkpoints: List[dict] = []
        self.errors: List[dict] = []
        self.evidence_store: Dict[str, dict] = {}
        self.task_results: Dict[str, dict] = {}
        self.runtime_tasks: List[dict] = []
        self.next_action: str = ""

        self.start_monotonic = self.monotonic_time_fn()

    def gen_id(self, prefix: str) -> str:
        return self.id_generator(prefix)

    def load_authorized_session(self, session_envelope: dict) -> Tuple[bool, List[dict]]:
        """Carga y valida los datos de una sesion autorizada previa (PZ-003B) sin modificar el original."""
        if not isinstance(session_envelope, dict):
            err = demo_intake.make_error_payload("INVALID_INPUT", "El sobre de sesion debe ser un objeto JSON.")
            return False, [err]

        mission = copy.deepcopy(session_envelope.get("mission"))
        brief = copy.deepcopy(session_envelope.get("brief"))
        plan = copy.deepcopy(session_envelope.get("plan"))
        approvals = copy.deepcopy(session_envelope.get("approvals") or [])
        events = copy.deepcopy(session_envelope.get("events") or [])
        checkpoints = copy.deepcopy(session_envelope.get("checkpoints") or [])

        errors = []
        if not mission or not plan or not brief:
            errors.append(demo_intake.make_error_payload("INVALID_INPUT", "Mision, brief o plan ausentes en la sesion."))
            return False, errors

        # 1. Comprobar que la mision este exactamente en AUTORIZADA_PARA_EJECUTAR
        if mission.get("current_state") != "AUTORIZADA_PARA_EJECUTAR":
            errors.append(
                demo_intake.make_error_payload(
                    "PERMISSION_DENIED",
                    f"La mision debe estar en estado 'AUTORIZADA_PARA_EJECUTAR', recibido: '{mission.get('current_state')}'.",
                )
            )

        # 2. Comprobar que exista aprobacion CONSUMIDA con decision APROBAR
        if not approvals:
            errors.append(demo_intake.make_error_payload("PERMISSION_DENIED", "No existe aprobacion registrada en la sesion."))
        else:
            app_req = approvals[0]
            if app_req.get("status") != "CONSUMIDA" or app_req.get("decision") != "APROBAR":
                errors.append(
                    demo_intake.make_error_payload(
                        "PERMISSION_DENIED",
                        f"La solicitud de aprobacion debe estar 'CONSUMIDA' con decision 'APROBAR', recibido status='{app_req.get('status')}', decision='{app_req.get('decision')}'.",
                    )
                )

            # Verificar huella exacta
            expected_fp = demo_plan_review.compute_plan_fingerprint(
                mission_id=mission["mission_id"],
                user_id=mission["user_id"],
                brief_version=mission["brief_version"],
                plan_version=plan["plan_version"],
                brief=brief,
                plan=plan,
            )
            if app_req.get("version_or_fingerprint") != expected_fp:
                errors.append(
                    demo_intake.make_error_payload(
                        "INVALID_INPUT",
                        f"La huella de aprobacion '{app_req.get('version_or_fingerprint')}' no coincide con la huella computada del plan '{expected_fp}'.",
                    )
                )

        if errors:
            return False, errors

        self.mission = mission
        self.brief = brief
        self.plan = plan
        self.approvals = approvals
        self.events = events
        self.checkpoints = checkpoints
        self.errors = []
        self.evidence_store = {}
        self.task_results = {}

        # Construir objetos de runtime task iniciales
        self.runtime_tasks = []
        for idx, t in enumerate(self.plan.get("tasks", [])):
            rt_task = {
                "schema_version": "1.0.0",
                "task_id": t["task_id"],
                "mission_id": self.mission["mission_id"],
                "mission_version": self.mission["record_version"],
                "agent_role": t["agent_role"],
                "objective": t["objective"],
                "question": f"Resolver tarea {t['task_id']}",
                "authorized_context": {
                    "brief_version": self.mission["brief_version"],
                    "input_refs": t.get("input_refs", ["brief"]),
                    "evidence_refs": [],
                },
                "approved_decisions": ["DEC-ALCANCE-PLAN"],
                "structured_inputs": {"focus": t["task_id"]},
                "expected_output": {
                    "description": t.get("expected_output", ""),
                    "acceptance_criteria": t.get("acceptance_criteria", ["Completar tarea"]),
                },
                "allowed_tool_categories": t.get("allowed_tool_categories", []),
                "prohibitions": ["No ejecutar acciones sensibles externas"],
                "limits": {
                    "max_attempts": t.get("limits", {}).get("max_attempts", 2),
                    "max_seconds": t.get("limits", {}).get("max_seconds", 300),
                    "max_budget_usd": float(t.get("limits", {}).get("max_budget_usd", 0.0)),
                    "max_depth": 0,
                    "max_breadth": 1,
                },
                "escalation_rules": ["Escalar si se supera limite de intentos"],
                "category": "razonamiento",
                "dependencies": copy.deepcopy(t.get("dependencies", [])),
                "status": "PENDIENTE",
                "attempt": 0,
            }
            self.task_validator.validate(rt_task)
            self.runtime_tasks.append(rt_task)

        return True, []

    def run_execution(self) -> Tuple[int, dict]:
        """Ejecuta secuencialmente las tareas del plan autorizado."""
        if not self.mission or self.mission.get("current_state") != "AUTORIZADA_PARA_EJECUTAR":
            err = demo_intake.make_error_payload("PERMISSION_DENIED", "No hay una sesion autorizada lista para ejecucion.")
            self.errors.append(err)
            return 1, self.build_envelope()

        now_iso = self.now_fn().isoformat()

        # 1. Transicion MT-006: AUTORIZADA_PARA_EJECUTAR -> EN_EJECUCION
        self.mission["current_state"] = "EN_EJECUCION"
        self.mission["record_version"] += 1
        self.mission["updated_at"] = now_iso
        self.mission_validator.validate(self.mission)

        evt_start = demo_intake.make_event(
            event_id=self.gen_id("EVT-EXEC-START"),
            mission_id=self.mission["mission_id"],
            actor="chief_of_staff_simulado",
            actor_role="chief_of_staff",
            action="inicio_de_ejecucion",
            timestamp=now_iso,
            version=self.mission["record_version"],
            previous_state="AUTORIZADA_PARA_EJECUTAR",
            new_state="EN_EJECUCION",
            result_summary="Mision inicia ejecucion secuencial de tareas autorizadas (SIMULADA)",
            idempotency_key=self.gen_id("IDEMP-EXEC-START"),
        )
        self.event_validator.validate(evt_start)
        self.events.append(evt_start)

        # 2. Ejecutar cada tarea en secuencia fija
        for idx, task in enumerate(self.runtime_tasks):
            task_id = task["task_id"]

            # Verificar dependencias
            for dep_id in task["dependencies"]:
                dep_task = next((t for t in self.runtime_tasks if t["task_id"] == dep_id), None)
                if not dep_task or dep_task["status"] != "COMPLETA":
                    err = demo_intake.make_error_payload(
                        "SYSTEM_ERROR",
                        f"Dependencia '{dep_id}' insatisfecha para tarea '{task_id}'.",
                    )
                    self.errors.append(err)
                    task["status"] = "BLOQUEADA"
                    self._pause_mission(task_id, f"Dependencia {dep_id} no satisfecha")
                    return 1, self.build_envelope()

            # Verificar limites de la mision antes de ejecutar tarea
            limits = self.mission["limits"]
            counters = self.mission["counters"]

            if counters["agent_requests"] >= limits["max_agent_requests_per_mission"]:
                err = demo_intake.make_error_payload(
                    "BUDGET_EXHAUSTED",
                    f"Limite de solicitudes de agente ({limits['max_agent_requests_per_mission']}) excedido.",
                )
                self.errors.append(err)
                self._pause_mission(task_id, "Limite de solicitudes de agente agotado")
                return 1, self.build_envelope()

            # Transicion TT-001: PENDIENTE -> LISTA
            task["status"] = "LISTA"
            self.task_validator.validate(task)

            # Transicion TT-002: LISTA -> EN_CURSO
            task["status"] = "EN_CURSO"
            task["attempt"] += 1
            counters["agent_requests"] += 1
            counters["task_reasoning_attempts"] = task["attempt"]
            self.mission["active_task"] = task_id
            self.mission["updated_at"] = self.now_fn().isoformat()
            self.task_validator.validate(task)
            self.mission_validator.validate(self.mission)

            evt_task_start = demo_intake.make_event(
                event_id=self.gen_id(f"EVT-TSK-START-{task_id}"),
                mission_id=self.mission["mission_id"],
                task_id=task_id,
                actor="chief_of_staff_simulado",
                actor_role="chief_of_staff",
                action="asignacion_de_tarea",
                timestamp=self.now_fn().isoformat(),
                version=self.mission["record_version"],
                previous_state=None,
                new_state="EN_CURSO",
                result_summary=f"Tarea {task_id} asignada a {task['agent_role']} (SIMULADA)",
                idempotency_key=self.gen_id(f"IDEMP-TSK-START-{task_id}"),
                attempt=task["attempt"],
            )
            self.event_validator.validate(evt_task_start)
            self.events.append(evt_task_start)

            # Ejecutar especialista simulado
            agent_res, new_evidences = self.specialist_runner.execute_task(
                task=task,
                mission=self.mission,
                evidence_store=self.evidence_store,
                previous_results=self.task_results,
            )

            # Almacenar evidencias generadas
            for ev in new_evidences:
                self.evidence_store[ev["evidence_id"]] = ev

            self.task_results[task_id] = agent_res

            # Evaluar estado de salida del especialista
            res_status = agent_res["status"]
            if res_status == "SUCCESS":
                # Transicion TT-003: EN_CURSO -> COMPLETA
                task["status"] = "COMPLETA"
                self.task_validator.validate(task)
                self.mission["active_task"] = None
                self.mission["updated_at"] = self.now_fn().isoformat()
                self.mission_validator.validate(self.mission)

                evt_task_end = demo_intake.make_event(
                    event_id=self.gen_id(f"EVT-TSK-END-{task_id}"),
                    mission_id=self.mission["mission_id"],
                    task_id=task_id,
                    actor=task["agent_role"],
                    actor_role=task["agent_role"],
                    action="finalizacion_de_tarea",
                    timestamp=self.now_fn().isoformat(),
                    version=self.mission["record_version"],
                    previous_state="EN_CURSO",
                    new_state="COMPLETA",
                    result_summary=f"Tarea {task_id} completada exitosamente: {agent_res['summary']}",
                    idempotency_key=self.gen_id(f"IDEMP-TSK-END-{task_id}"),
                    attempt=task["attempt"],
                    source_or_artifact=agent_res["fingerprint"],
                )
                self.event_validator.validate(evt_task_end)
                self.events.append(evt_task_end)

            else:
                # Fallo o bloqueo en tarea
                if res_status == "FAILED":
                    task["status"] = "FALLIDA"  # TT-005
                elif res_status == "BLOCKED":
                    task["status"] = "BLOQUEADA"  # TT-006
                elif res_status == "PARTIAL":
                    task["status"] = "PARCIAL"  # TT-004

                self.task_validator.validate(task)
                self.mission["active_task"] = None
                self._pause_mission(task_id, f"Fallo en especialista: {agent_res['summary']}")
                return 1, self.build_envelope()

        # 3. Transicion MT-008: EN_EJECUCION -> EN_CONSOLIDACION
        now_end_iso = self.now_fn().isoformat()
        self.mission["current_state"] = "EN_CONSOLIDACION"
        self.mission["record_version"] += 1
        self.mission["updated_at"] = now_end_iso
        self.mission_validator.validate(self.mission)

        evt_consolidation = demo_intake.make_event(
            event_id=self.gen_id("EVT-CONSOLIDATION"),
            mission_id=self.mission["mission_id"],
            actor="chief_of_staff_simulado",
            actor_role="chief_of_staff",
            action="consolidacion_de_resultados",
            timestamp=now_end_iso,
            version=self.mission["record_version"],
            previous_state="EN_EJECUCION",
            new_state="EN_CONSOLIDACION",
            result_summary="Todas las tareas completadas. Mision avanza a EN_CONSOLIDACION (SIMULADA)",
            idempotency_key=self.gen_id("IDEMP-CONSOLIDATION"),
        )
        self.event_validator.validate(evt_consolidation)
        self.events.append(evt_consolidation)

        # Current, still-unapproved assembly records are versioned together.
        # Earlier event/approval/checkpoint objects are not rewritten.
        for task in self.runtime_tasks:
            task["mission_version"] = self.mission["record_version"]
        for evidence in self.evidence_store.values():
            evidence["mission_version"] = self.mission["record_version"]
            evidence["fingerprint"] = runtime_contracts.compute_evidence_fingerprint(evidence)

        # Crear Checkpoint de consolidacion en memoria
        self._create_checkpoint("EN_CONSOLIDACION")

        self.next_action = "Mision en EN_CONSOLIDACION. Tareas completadas. Esperando consolidacion de VBP."
        return 0, self.build_envelope()

    def _pause_mission(self, active_task_id: str, reason: str) -> None:
        """Pasa la mision a PAUSADA (MT-012) con resumable_state y crea checkpoint en memoria."""
        now_iso = self.now_fn().isoformat()
        self.mission["current_state"] = "PAUSADA"
        self.mission["resumable_state"] = "EN_EJECUCION"
        self.mission["record_version"] += 1
        self.mission["updated_at"] = now_iso
        self.mission_validator.validate(self.mission)

        evt_pause = demo_intake.make_event(
            event_id=self.gen_id("EVT-MISSION-PAUSED"),
            mission_id=self.mission["mission_id"],
            task_id=active_task_id,
            actor="sistema",
            actor_role="sistema",
            action="pausa_de_mision",
            timestamp=now_iso,
            version=self.mission["record_version"],
            previous_state="EN_EJECUCION",
            new_state="PAUSADA",
            result_summary=f"Mision PAUSADA por tarea {active_task_id}: {reason} (SIMULADA)",
            idempotency_key=self.gen_id("IDEMP-MISSION-PAUSED"),
        )
        self.event_validator.validate(evt_pause)
        self.events.append(evt_pause)

        self._create_checkpoint("PAUSADA", resumable_state="EN_EJECUCION")
        self.next_action = f"Mision PAUSADA en tarea {active_task_id}. Requiere intervencion o reanudacion."

    def _create_checkpoint(self, state: str, resumable_state: Optional[str] = None) -> None:
        """Genera un checkpoint en memoria conforme a contracts/core/checkpoint.schema.json."""
        now_iso = self.now_fn().isoformat()
        elapsed = max(0.0, self.monotonic_time_fn() - self.start_monotonic)
        chk_id = self.gen_id("CHK")

        dep_graph = []
        for idx, t in enumerate(self.runtime_tasks):
            if idx > 0:
                prev_id = self.runtime_tasks[idx - 1]["task_id"]
                curr_id = t["task_id"]
                dep_graph.append({
                    "from_task": prev_id,
                    "to_task": curr_id,
                    "satisfied": self.runtime_tasks[idx - 1]["status"] == "COMPLETA",
                })

        checkpoint_data = {
            "schema_version": "1.0.0",
            "checkpoint_id": chk_id,
            "mission_id": self.mission["mission_id"],
            "mission_version": self.mission["record_version"],
            "state": state,
            "resumable_state": resumable_state,
            "tasks": [
                {
                    "task_id": t["task_id"],
                    "state": t["status"],
                    "attempts": t["attempt"],
                }
                for t in self.runtime_tasks
            ],
            "dependencies": dep_graph,
            "attempts": {
                "clarification_cycles": self.mission["counters"]["clarification_cycles"],
                "task_reasoning_attempts": self.mission["counters"]["task_reasoning_attempts"],
                "transient_retries": self.mission["counters"]["transient_retries"],
                "vbp_correction_rounds": self.mission["counters"]["vbp_correction_rounds"],
                "agent_requests": self.mission["counters"]["agent_requests"],
            },
            "budgets_consumed": {
                "elapsed_mission_seconds": float(round(elapsed, 2)),
                "budget_usd_spent": 0.0,
            },
            "artifacts": list(self.task_results.keys()),
            "authorizations": [a["approval_id"] for a in self.approvals],
            "timestamp": now_iso,
            "idempotency_key": self.gen_id("IDEMP-CHK"),
        }
        checkpoint_data["fingerprint"] = demo_plan_review.compute_checkpoint_fingerprint(checkpoint_data)
        self.checkpoint_validator.validate(checkpoint_data)

        self.mission["last_checkpoint_id"] = chk_id
        self.mission_validator.validate(self.mission)
        self.checkpoints.append(checkpoint_data)

    def build_envelope(self) -> dict:
        """Construye el sobre de salida estructurado del motor."""
        return {
            "simulation_status": "SIMULADA",
            "mission": copy.deepcopy(self.mission),
            "brief": copy.deepcopy(self.brief),
            "plan": copy.deepcopy(self.plan),
            "events": copy.deepcopy(self.events),
            "tasks": copy.deepcopy(self.runtime_tasks),
            "task_results": copy.deepcopy(self.task_results),
            "evidence_store": copy.deepcopy(self.evidence_store),
            "evidence_originals": {eid: {"fingerprint": ev["fingerprint"], "mode": "SIMULADA",
                                         "excerpt": ev["excerpt_or_summary"]}
                                   for eid, ev in self.evidence_store.items()},
            "decisions": [{"ref_id": "DEC-ALCANCE-PLAN", "mission_id": self.mission["mission_id"],
                           "mission_version": self.mission["record_version"], "approval_ref": self.approvals[0]["approval_id"]}]
                          if self.mission and self.approvals else [],
            "approvals": copy.deepcopy(self.approvals),
            "checkpoints": copy.deepcopy(self.checkpoints),
            "errors": copy.deepcopy(self.errors),
            "next_action": self.next_action,
        }
