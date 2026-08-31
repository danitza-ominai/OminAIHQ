"""OminAI HQ - Recorrido completo Mision a VBP SIMULADA (PZ-003F).

Integra de extremo a extremo el flujo simulado desde intake, revision de plan (Puerta 1),
ejecucion secuencial de tareas, ensamblaje y evaluacion de VBP, y decision humana sobre VBP (Puerta 2)
hasta la transicion a FINALIZADA y exportacion del Markdown canonico en memoria.
Cumple estrictamente con CONTRATO-MVP-v1.md y FICHA-PZ-003F.md.
"""

import copy
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from jsonschema import Draft202012Validator

import app.demo_intake as demo_intake
import app.demo_plan_review as demo_plan_review
import app.mission_engine as mission_engine
import app.runtime_contracts as runtime_contracts
import app.vbp_document as vbp_document
import app.vbp_validation as vbp_validation

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FIXTURE_PATH = PROJECT_ROOT / "examples" / "demo_mission.json"


class CompleteVBPFlowRunner:
    """Ejecutor de extremo a extremo del flujo simulado con soporte para dos puertas humanas."""

    def __init__(
        self,
        now_fn: Optional[Callable[[], datetime]] = None,
        id_generator: Optional[Callable[[str], str]] = None,
        monotonic_time_fn: Optional[Callable[[], float]] = None,
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
        self.vbp_validator = Draft202012Validator(self.vbp_schema, format_checker=self.format_checker)

        self.plan_session = demo_plan_review.PlanReviewSession(
            now_fn=self.now_fn,
            id_generator=self.id_generator,
            monotonic_time_fn=self.monotonic_time_fn,
        )
        self.engine = mission_engine.MissionExecutionEngine(
            now_fn=self.now_fn,
            id_generator=self.id_generator,
            monotonic_time_fn=self.monotonic_time_fn,
        )
        self.evaluator = vbp_validation.VBPValidator()

        self.vbp_data: Optional[dict] = None
        self.canonical_markdown: str = ""
        self.evaluation_report: Optional[dict] = None
        self.vbp_approval_req: Optional[dict] = None
        self.errors: List[dict] = []
        self.engine_envelope: Optional[dict] = None

    def gen_id(self, prefix: str) -> str:
        return self.id_generator(prefix)

    def init_flow(self, raw_data: Optional[dict] = None) -> Tuple[int, dict]:
        """Paso 1: Inicializa el intake y prepara la Puerta 1 (Plan Review)."""
        code, env = self.plan_session.init_from_intake(raw_data=raw_data)
        return code, env

    def process_plan_decision(self, command: dict, actor_context: dict) -> Tuple[int, dict]:
        """Paso 2 (Puerta 1): Procesa la decision humana sobre el plan."""
        return self.plan_session.process_decision(command, actor_context)

    def execute_tasks_and_assemble_vbp(self) -> Tuple[int, dict]:
        """Paso 3 y 4: Ejecuta tareas secuenciales y ensambla el VBP para evaluacion y Puerta 2."""
        plan_env = self.plan_session.build_envelope()
        ok, errs = self.engine.load_authorized_session(plan_env)
        if not ok:
            self.errors.extend(errs)
            return 1, self.build_envelope()

        code, self.engine_envelope = self.engine.run_execution()
        if code != 0:
            self.errors.extend(self.engine_envelope.get("errors", []))
            return code, self.build_envelope()

        # Ensamblar VBP data
        now_iso = self.now_fn().isoformat()
        self.vbp_data = vbp_document.assemble_vbp_data(self.engine_envelope, now_iso=now_iso)
        self.vbp_validator.validate(self.vbp_data)
        self.canonical_markdown = vbp_document.render_canonical_markdown(self.vbp_data)

        # Evaluar VBP deterministamente
        self.evaluation_report = self.evaluator.evaluate_vbp(
            self.vbp_data,
            evidence_store=self.engine_envelope.get("evidence_store"),
            context=vbp_validation.build_evaluation_context(self.engine_envelope),
        )

        mission = self.engine.mission

        # Transicion MT-009: EN_CONSOLIDACION -> EN_EVALUACION
        mission["current_state"] = "EN_EVALUACION"
        mission["record_version"] += 1
        mission["updated_at"] = now_iso
        self.mission_validator.validate(mission)

        evt_eval = demo_intake.make_event(
            event_id=self.gen_id("EVT-EVALUATION"),
            mission_id=mission["mission_id"],
            actor="governance_risk_simulado",
            actor_role="governance_risk",
            action="evaluacion_de_vbp",
            timestamp=now_iso,
            version=mission["record_version"],
            previous_state="EN_CONSOLIDACION",
            new_state="EN_EVALUACION",
            result_summary=f"Evaluacion determinista completada: Dictamen {self.evaluation_report['verdict']} (SIMULADA)",
            idempotency_key=self.gen_id("IDEMP-EVT-EVAL"),
            source_or_artifact=self.vbp_data["fingerprint"],
        )
        self.event_validator.validate(evt_eval)
        self.engine.events.append(evt_eval)

        # Transicion MT-010: EN_EVALUACION -> VBP_EN_REVISION
        mission["current_state"] = "VBP_EN_REVISION"
        mission["record_version"] += 1
        mission["updated_at"] = now_iso
        self.mission_validator.validate(mission)

        # Generar solicitud de aprobacion de VBP (Puerta 2)
        app_vbp_id = self.gen_id("APP-VBP")
        app_vbp_req = {
            "schema_version": "1.0.0",
            "approval_id": app_vbp_id,
            "user_id": mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "action_approved": f"Aprobacion final del VBP v{self.vbp_data['version']} de la mision {mission['mission_id']}",
            "version_or_fingerprint": self.vbp_data["fingerprint"],
            "timestamp": now_iso,
            "decision": None,
            "comment": "",
            "conditions": [],
            "expiration": now_iso,
            "status": "PENDIENTE",
            "idempotency_key": self.gen_id("IDEMP-APP-VBP-REQ"),
        }
        self.approval_validator.validate(app_vbp_req)
        self.vbp_approval_req = app_vbp_req
        self.engine.approvals.append(app_vbp_req)

        mission["approval_refs"].append(app_vbp_id)
        self.mission_validator.validate(mission)

        evt_vbp_req = demo_intake.make_event(
            event_id=self.gen_id("EVT-VBP-APP-REQ"),
            mission_id=mission["mission_id"],
            actor="sistema",
            actor_role="sistema",
            action="solicitud_de_aprobacion_vbp",
            timestamp=now_iso,
            version=mission["record_version"],
            previous_state="EN_EVALUACION",
            new_state="VBP_EN_REVISION",
            result_summary="Solicitud de aprobacion del VBP registrada (SIMULADA)",
            idempotency_key=self.gen_id("IDEMP-EVT-VBP-REQ"),
            related_approval_id=app_vbp_id,
            source_or_artifact=self.vbp_data["fingerprint"],
        )
        self.event_validator.validate(evt_vbp_req)
        self.engine.events.append(evt_vbp_req)

        # Retorna codigo 3 (solicitud PENDIENTE de decision humana sobre VBP)
        return 3, self.build_envelope()

    def process_vbp_decision(self, command: dict, actor_context: dict) -> Tuple[int, dict]:
        """Paso 5 (Puerta 2): Procesa la decision humana sobre el VBP."""
        if not self.vbp_approval_req or not self.engine or not self.engine.mission:
            err = demo_intake.make_error_payload("NOT_FOUND", "No hay solicitud de VBP pendiente de decision.")
            self.errors.append(err)
            return 1, self.build_envelope()

        decision = command.get("decision")
        comment = command.get("comment", "")
        now_iso = self.now_fn().isoformat()
        mission = self.engine.mission

        if actor_context.get("actor_role") != "usuario_humano" or actor_context.get("user_id") != mission["user_id"]:
            err = demo_intake.make_error_payload("PERMISSION_DENIED", "Solo el usuario humano propietario puede decidir.")
            self.errors.append(err)
            return 1, self.build_envelope()

        # Comprobar huella
        if command.get("version_or_fingerprint") != self.vbp_data["fingerprint"]:
            err = demo_intake.make_error_payload("INVALID_INPUT", "La huella no coincide con el VBP vigente.")
            self.errors.append(err)
            return 1, self.build_envelope()

        if decision == "APROBAR":
            if not self.evaluation_report or self.evaluation_report["verdict"] != "PASA":
                self.errors.append(demo_intake.make_error_payload("PERMISSION_DENIED", "Evaluacion no permite aprobacion ordinaria."))
                return 1, self.build_envelope()
            # Consumir aprobacion de VBP
            self.vbp_approval_req["status"] = "CONSUMIDA"
            self.vbp_approval_req["decision"] = "APROBAR"
            self.vbp_approval_req["comment"] = comment
            self.vbp_approval_req["timestamp"] = now_iso
            self.approval_validator.validate(self.vbp_approval_req)

            self.vbp_data["approval_status"] = "APROBADO"
            self.vbp_data["human_approval_ref"] = self.vbp_approval_req["approval_id"]
            self.vbp_data["fingerprint"] = runtime_contracts.compute_vbp_manifest_fingerprint(self.vbp_data)
            self.canonical_markdown = vbp_document.render_canonical_markdown(self.vbp_data)

            # Transicion MT-014: VBP_EN_REVISION -> VBP_APROBADO
            mission["current_state"] = "VBP_APROBADO"
            mission["record_version"] += 1
            mission["updated_at"] = now_iso
            self.mission_validator.validate(mission)

            evt_app = demo_intake.make_event(
                event_id=self.gen_id("EVT-VBP-APPROVED"),
                mission_id=mission["mission_id"],
                actor="usuario_local_demo",
                actor_role="usuario_humano",
                action="aprobacion_de_vbp",
                timestamp=now_iso,
                version=mission["record_version"],
                previous_state="VBP_EN_REVISION",
                new_state="VBP_APROBADO",
                result_summary="VBP formalmente aprobado por el usuario humano (SIMULADA)",
                idempotency_key=self.gen_id("IDEMP-EVT-VBP-APPROVED"),
                related_approval_id=self.vbp_approval_req["approval_id"],
                source_or_artifact=self.vbp_data["fingerprint"],
            )
            self.event_validator.validate(evt_app)
            self.engine.events.append(evt_app)

            # Transicion MT-016: VBP_APROBADO -> FINALIZADA
            mission["current_state"] = "FINALIZADA"
            mission["record_version"] += 1
            mission["updated_at"] = now_iso
            self.mission_validator.validate(mission)

            evt_fin = demo_intake.make_event(
                event_id=self.gen_id("EVT-MISSION-FINALIZED"),
                mission_id=mission["mission_id"],
                actor="sistema",
                actor_role="sistema",
                action="finalizacion_de_mision",
                timestamp=now_iso,
                version=mission["record_version"],
                previous_state="VBP_APROBADO",
                new_state="FINALIZADA",
                result_summary="Mision completada y finalizada exitosamente (SIMULADA)",
                idempotency_key=self.gen_id("IDEMP-EVT-FIN"),
                source_or_artifact=self.vbp_data["fingerprint"],
            )
            self.event_validator.validate(evt_fin)
            self.engine.events.append(evt_fin)

            return 0, self.build_envelope()

        elif decision == "RECHAZAR":
            if not comment.strip():
                err = demo_intake.make_error_payload("INVALID_INPUT", "Rechazar exige motivo no vacio.")
                self.errors.append(err)
                return 1, self.build_envelope()

            self.vbp_approval_req["status"] = "CONSUMIDA"
            self.vbp_approval_req["decision"] = "RECHAZAR"
            self.vbp_approval_req["comment"] = comment
            self.approval_validator.validate(self.vbp_approval_req)

            self.vbp_data["approval_status"] = "RECHAZADO"

            # Transicion MT-015: VBP_EN_REVISION -> VBP_RECHAZADO
            mission["current_state"] = "VBP_RECHAZADO"
            mission["record_version"] += 1
            mission["updated_at"] = now_iso
            self.mission_validator.validate(mission)

            evt_rej = demo_intake.make_event(
                event_id=self.gen_id("EVT-VBP-REJECTED"),
                mission_id=mission["mission_id"],
                actor="usuario_local_demo",
                actor_role="usuario_humano",
                action="rechazo_de_vbp",
                timestamp=now_iso,
                version=mission["record_version"],
                previous_state="VBP_EN_REVISION",
                new_state="VBP_RECHAZADO",
                result_summary=f"VBP rechazado: {comment} (SIMULADA)",
                idempotency_key=self.gen_id("IDEMP-EVT-VBP-REJECTED"),
                related_approval_id=self.vbp_approval_req["approval_id"],
            )
            self.event_validator.validate(evt_rej)
            self.engine.events.append(evt_rej)

            return 0, self.build_envelope()

        else:
            err = demo_intake.make_error_payload("INVALID_INPUT", f"Decision '{decision}' no soportada en demo_vbp_flow.")
            self.errors.append(err)
            return 1, self.build_envelope()

    def build_envelope(self) -> dict:
        """Construye el sobre consolidado de salida del flujo completo."""
        mission = self.engine.mission if self.engine and self.engine.mission else self.plan_session.mission
        brief = self.engine.brief if self.engine and self.engine.brief else self.plan_session.brief
        plan = self.engine.plan if self.engine and self.engine.plan else self.plan_session.plan
        events = self.engine.events if self.engine and self.engine.events else self.plan_session.events
        approvals = self.engine.approvals if self.engine and self.engine.approvals else self.plan_session.approvals
        checkpoints = self.engine.checkpoints if self.engine and self.engine.checkpoints else self.plan_session.checkpoints

        return {
            "simulation_status": "SIMULADA",
            "mission": copy.deepcopy(mission),
            "brief": copy.deepcopy(brief),
            "plan": copy.deepcopy(plan),
            "events": copy.deepcopy(events),
            "tasks": copy.deepcopy(self.engine.runtime_tasks if self.engine else []),
            "task_results": copy.deepcopy(self.engine.task_results if self.engine else {}),
            "evidence_store": copy.deepcopy(self.engine.evidence_store if self.engine else {}),
            "approvals": copy.deepcopy(approvals),
            "checkpoints": copy.deepcopy(checkpoints),
            "vbp_data": copy.deepcopy(self.vbp_data),
            "canonical_markdown": self.canonical_markdown,
            "evaluation_report": copy.deepcopy(self.evaluation_report),
            "errors": copy.deepcopy(self.errors),
        }


def main(argv: Optional[List[str]] = None) -> int:
    """Punto de entrada CLI para el recorrido completo SIMULADA."""
    args = argv if argv is not None else sys.argv[1:]

    fixture_path = DEFAULT_FIXTURE_PATH
    if "--fixture" in args:
        idx = args.index("--fixture")
        if idx + 1 < len(args):
            fixture_path = Path(args[idx + 1])

    with open(fixture_path, "r", encoding="utf-8") as f:
        fixture_data = json.load(f)

    runner = CompleteVBPFlowRunner()
    code, env = runner.init_flow(raw_data=fixture_data)

    # Por defecto se detiene en la Puerta 1 con solicitud pendiente
    sys.stderr.write("[INFO] Flujo SIMULADA iniciado. Puerta 1 (Plan) PENDIENTE.\n")
    print(json.dumps(env, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
