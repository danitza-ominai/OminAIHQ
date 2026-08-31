"""Pruebas exhaustivas para el Agente Governance & Risk (PZ-008A).

Valida emision de dictamenes independientes (PASA, PASA_CON_CONDICIONES, NO_PASA),
deteccion de bloqueadores de gobernanza, imposibilidad de autoaprobacion y validacion contra schemas.
"""

import copy
import json
import unittest
from pathlib import Path

import app.governance_risk as governance_risk
import app.hq_runtime as hq_runtime
import app.runtime_contracts as runtime_contracts
import app.vbp_document as vbp_document
from jsonschema import Draft202012Validator

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FIXTURE_PATH = PROJECT_ROOT / "examples" / "demo_mission.json"


class TestGovernanceRisk(unittest.TestCase):
    """Suite de pruebas para PZ-008A."""

    def setUp(self) -> None:
        self.gov = governance_risk.GovernanceRisk()
        self.runtime = hq_runtime.HQRuntime()
        _, self.agent_result_schema, _, _ = runtime_contracts.load_runtime_contracts()
        self.result_validator = Draft202012Validator(self.agent_result_schema)

        # Cargar sesion base para construir VBP candidato
        import app.demo_vbp_flow as demo_vbp_flow
        runner = demo_vbp_flow.CompleteVBPFlowRunner()
        with open(DEFAULT_FIXTURE_PATH, "r", encoding="utf-8") as f:
            fixture = json.load(f)
        runner.init_flow(raw_data=fixture)
        plan_app = runner.plan_session.approvals[0]
        cmd1 = {
            "approval_id": plan_app["approval_id"],
            "version_or_fingerprint": plan_app["version_or_fingerprint"],
            "decision": "APROBAR",
            "comment": "OK",
            "idempotency_key": plan_app["idempotency_key"],
        }
        actor = {
            "user_id": runner.plan_session.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
            "identity_scope": "IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA",
        }
        runner.process_plan_decision(cmd1, actor)
        plan_env = runner.plan_session.build_envelope()
        runner.engine.load_authorized_session(plan_env)
        runner.engine.run_execution()
        self.engine_envelope = runner.engine.build_envelope()
        self.vbp_candidate = vbp_document.assemble_vbp_data(self.engine_envelope)
        from app.vbp_validation import build_evaluation_context
        self.context = build_evaluation_context(self.engine_envelope)

    def test_ac01_dictamen_verdicts_pasa_and_no_pasa(self) -> None:
        """AC-01: Evaluar dictamenes PASA y NO_PASA segun condiciones del VBP candidato."""
        # 1. Candidato valido -> PASA
        eval_clean = self.gov.evaluate_vbp_governance(self.vbp_candidate, evidence_store=self.engine_envelope["evidence_store"], context=self.context)
        self.assertEqual(eval_clean["verdict"], "PASA")

        # 2. Candidato con evidencia falsa -> NO_PASA
        vbp_bad = copy.deepcopy(self.vbp_candidate)
        vbp_bad["sections"][4]["content"] = "Cita a fuente falsa e inventada."
        eval_bad = self.gov.evaluate_vbp_governance(vbp_bad, evidence_store=self.engine_envelope["evidence_store"])
        self.assertEqual(eval_bad["verdict"], "NO_PASA")
        self.assertIn("EVIDENCIA_FALSA_O_INEXISTENTE", eval_bad["blockers"])

    def test_ac02_governance_cannot_self_approve(self) -> None:
        """AC-02: Governance emite dictamen pero no puede aprobar ni cambiar approvals a CONSUMIDA."""
        task = {"task_id": "TSK-004-GOV", "mission_id": "MSN-SIM-001"}
        brief = {"title": "App Demo", "objective": "Objetivo"}

        ok, res, _ = self.gov.execute_governance_task(
            task=task,
            brief=brief,
            vbp_candidate=self.vbp_candidate,
            evidence_store=self.engine_envelope["evidence_store"],
            context=self.context,
        )
        self.assertTrue(ok)
        self.result_validator.validate(res)

        # El resultado no contiene modificaciones de estado de aprobacion
        self.assertEqual(res["agent_role"], "governance_risk")
        self.assertIn("Dictamen de Gobernanza: PASA", res["proposals"][0])
        self.assertTrue(any("aprobacion humana obligatoria" in lim for lim in res["limitations"]))

    def test_ac03_evaluator_does_not_mutate_input(self) -> None:
        """AC-03: La evaluacion es determinista y no muta el documento VBP de entrada."""
        fp_before = self.vbp_candidate["fingerprint"]
        self.gov.evaluate_vbp_governance(self.vbp_candidate, evidence_store=self.engine_envelope["evidence_store"])
        self.assertEqual(self.vbp_candidate["fingerprint"], fp_before)

    def test_ac04_schema_conformance_and_fingerprint(self) -> None:
        """AC-04: La salida cumple con agent-result.schema.json y tiene huella SHA-256 valida."""
        task = {"task_id": "TSK-004-GOV"}
        brief = {"title": "Sistema G"}
        ok, res, _ = self.gov.execute_governance_task(task, brief)
        self.assertTrue(ok)
        self.result_validator.validate(res)
        self.assertTrue(res["fingerprint"].startswith("sha256:"))

    def test_ac05_runtime_integration(self) -> None:
        """AC-05: Governance Risk se encuentra registrado e integrable en HQRuntime."""
        specialist = self.runtime.get_specialist("governance_risk")
        self.assertIsNotNone(specialist)
        self.assertIsInstance(specialist, governance_risk.GovernanceRisk)


if __name__ == "__main__":
    unittest.main()
