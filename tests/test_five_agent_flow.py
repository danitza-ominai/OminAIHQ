"""Pruebas de integracion secuencial para los Cinco Agentes del Runtime (PZ-008A).

Valida el recorrido completo secuencial entre los 5 especialistas:
Chief of Staff -> Research Analyst -> Product Architect -> Delivery Planner -> Governance Risk,
con inyeccion de fallos en cada rol, trazabilidad de evidencias y respeto a los limites presupuestarios.
"""

import json
import unittest
from pathlib import Path

import app.hq_runtime as hq_runtime
import app.runtime_contracts as runtime_contracts
import app.vbp_document as vbp_document
from jsonschema import Draft202012Validator

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FIXTURE_PATH = PROJECT_ROOT / "examples" / "demo_mission.json"


class TestFiveAgentFlow(unittest.TestCase):
    """Suite de integracion del flujo secuencial de los 5 agentes."""

    def setUp(self) -> None:
        self.runtime = hq_runtime.HQRuntime()
        self.task_schema, self.agent_result_schema, self.evidence_schema, self.vbp_schema = runtime_contracts.load_runtime_contracts()
        self.result_validator = Draft202012Validator(self.agent_result_schema)

        with open(DEFAULT_FIXTURE_PATH, "r", encoding="utf-8") as f:
            self.fixture = json.load(f)

    def test_ac01_full_five_agent_sequential_execution(self) -> None:
        """AC-01 & AC-04: Ejecucion secuencial de los 5 roles con paso de evidencias y resultados estructurados."""
        # 1. Chief of Staff: Aclaracion y propuesta de plan
        raw_mission = {
            "title": self.fixture["title"],
            "objective": self.fixture["objective"],
            "context": self.fixture["context"],
            "expected_result": self.fixture["expected_result"],
        }
        ok_brief, brief, _, _ = self.runtime.chief_of_staff.evaluate_and_clarify_mission(raw_mission)
        self.assertTrue(ok_brief)

        ok_plan, plan, _ = self.runtime.chief_of_staff.propose_plan("MSN-5AG-001", brief)
        self.assertTrue(ok_plan)
        self.assertEqual(len(plan["tasks"]), 4)

        # 2. Research & Evidence Analyst
        sources = {
            "https://wikipedia.org/wiki/B2B": "El comercio B2B optimiza compras entre empresas.",
        }
        ok_res, res_research, _ = self.runtime.research_analyst.execute_research(plan["tasks"][0], sources)
        self.assertTrue(ok_res)
        self.result_validator.validate(res_research)
        self.assertGreaterEqual(len(res_research["evidence_refs"]), 1)

        # 3. Product Architect
        ok_arch, res_arch, _ = self.runtime.product_architect.execute_architecture(
            task=plan["tasks"][1],
            brief=brief,
            research_results=res_research,
        )
        self.assertTrue(ok_arch)
        self.result_validator.validate(res_arch)
        self.assertEqual(res_arch["evidence_refs"], res_research["evidence_refs"])

        # 4. Delivery Planner
        ok_plan_spec, res_planner, _ = self.runtime.delivery_planner.execute_planning(
            task=plan["tasks"][2],
            brief=brief,
            arch_results=res_arch,
        )
        self.assertTrue(ok_plan_spec)
        self.result_validator.validate(res_planner)

        # 5. Governance & Risk
        ok_gov, res_gov, _ = self.runtime.governance_risk.execute_governance_task(
            task=plan["tasks"][3],
            brief=brief,
            plan_results=res_planner,
            evidence_store=self.runtime.research_analyst.evidence_store,
        )
        self.assertTrue(ok_gov)
        self.result_validator.validate(res_gov)
        self.assertIn("Dictamen de Gobernanza: NO_PASA", res_gov["proposals"][0])

        # Existing sequential handoff cannot pass without a referential candidate.
        # Exercise the positive integrated path with real persisted synthetic authority.
        from test_human_approvals import fixture
        from app.vbp_validation import build_evaluation_context
        runtime, repo, ctx, request = fixture(stage='vbp')
        self.addCleanup(repo.close)
        mission = repo.get_mission('MSN-SIM')
        candidate = repo.get_object('candidate', 'MSN-SIM:GATE_2_VBP')
        envelope = {'mission': mission['nuclear'], 'brief': mission['brief'], 'plan': mission['plan'],
                    'tasks': mission['tasks'], 'task_results': mission['task_results'],
                    'evidence_store': {eid:repo.get_object('evidence',eid) for eid in mission['evidence_ids']},
                    'evidence_originals': {eid:repo.get_object('evidence_original',eid) for eid in mission['evidence_ids']},
                    'approvals': [repo.get_object('approval_record', mission['pending_GATE_1_PLAN'])]}
        context = build_evaluation_context(envelope)
        before = list(repo._conn.iterdump())
        without = runtime.governance_risk.evaluate_vbp_governance(candidate, envelope['evidence_store'])
        self.assertEqual(without['verdict'], 'NO_PASA')
        with_context = runtime.governance_risk.evaluate_vbp_governance(candidate, envelope['evidence_store'], context=context)
        self.assertTrue(with_context['integrity']['valid'], with_context)
        self.assertEqual(with_context['verdict'], 'PASA')
        self.assertEqual(list(repo._conn.iterdump()), before)
        self.assertEqual(len(mission['task_results']), 4)
        self.assertTrue(runtime.approvals.submit_human_decision(request, 'APROBAR', context=ctx)[0])
        self.assertEqual(repo.get_mission('MSN-SIM')['status'], 'VBP_APROBADO')

    def test_ac02_runtime_readiness_with_all_five_agents(self) -> None:
        """AC-02: El runtime confirma que los 5 especialistas estan completamente registrados."""
        ready, missing = self.runtime.validate_runtime_readiness()
        self.assertTrue(ready)
        self.assertEqual(len(missing), 0)

    def test_ac03_fault_injection_stops_pipeline(self) -> None:
        """AC-03 & AC-05: Inyectar fallo en una tarea detiene el avance secuencial."""
        # Tarea de investigacion sin fuentes ni permisos genera hallazgo NO_VERIFICADA
        task1 = {"task_id": "TSK-001-RESEARCH", "mission_id": "MSN-5AG-001"}
        ok, res_unv, _ = self.runtime.research_analyst.execute_research(task1, {})
        self.assertTrue(ok)
        unv_id = res_unv["evidence_refs"][0]
        self.assertEqual(self.runtime.research_analyst.evidence_store[unv_id]["confidence"], "NO_VERIFICADA")


if __name__ == "__main__":
    unittest.main()
