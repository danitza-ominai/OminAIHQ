"""Pruebas exhaustivas para el Agente Product Architect (PZ-006A).

Valida definicion de producto, propuestas, decisiones pendientes humanas,
enlace de evidencias y validacion estricta contra agent-result.schema.json.
"""

import unittest

import app.hq_runtime as hq_runtime
import app.product_architect as product_architect
import app.runtime_contracts as runtime_contracts
from jsonschema import Draft202012Validator


class TestProductArchitect(unittest.TestCase):
    """Suite de pruebas para PZ-006A."""

    def setUp(self) -> None:
        self.architect = product_architect.ProductArchitect()
        self.runtime = hq_runtime.HQRuntime()
        _, self.agent_result_schema, _, _ = runtime_contracts.load_runtime_contracts()
        self.result_validator = Draft202012Validator(self.agent_result_schema)

    def test_ac01_coherent_case_generates_traceable_requirements(self) -> None:
        """AC-01: Caso coherente produce resultados trazables enlazados a claims de investigacion."""
        brief = {
            "title": "Portal Autoservicio B2B",
            "objective": "Permitir compras mayoristas directas integradas con ERP",
            "context": "Empresa de distribucion",
        }
        task = {"task_id": "TSK-002-ARCH", "mission_id": "MSN-SIM-001"}
        research_results = {
            "claims": ["EVD-CLAIM-001", "EVD-CLAIM-002"],
        }

        ok, res, err = self.architect.execute_architecture(task, brief, research_results)
        self.assertTrue(ok)
        self.assertIsNotNone(res)
        self.result_validator.validate(res)

        self.assertEqual(res["agent_role"], "product_architect")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("EVD-CLAIM-001", res["evidence_refs"])
        self.assertGreaterEqual(len(res["proposals"]), 1)
        self.assertGreaterEqual(len(res["findings"]), 1)

    def test_ac02_tech_decisions_remain_pending_human_decisions(self) -> None:
        """AC-02: Decisiones de proveedor de nube/infraestructura no son impuestas, sino declaradas pendientes."""
        brief = {"title": "App Cliente", "objective": "Construir app"}
        task = {"task_id": "TSK-002-ARCH"}

        ok, res, _ = self.architect.execute_architecture(task, brief)
        self.assertTrue(ok)
        self.result_validator.validate(res)

        decisions = res["pending_decisions"]
        self.assertGreaterEqual(len(decisions), 1)
        self.assertTrue(any("proveedor" in d.lower() or "infraestructura" in d.lower() for d in decisions))

    def test_ac03_missing_research_claims_handled_gracefully(self) -> None:
        """AC-03: Cuando no hay claims previos, el resultado se genera sin romper el schema."""
        brief = {"title": "App Demo", "objective": "Demo"}
        task = {"task_id": "TSK-002-ARCH"}

        ok, res, err = self.architect.execute_architecture(task, brief, research_results=None)
        self.assertTrue(ok)
        self.result_validator.validate(res)
        self.assertEqual(res["evidence_refs"], [])

    def test_ac04_schema_conformance(self) -> None:
        """AC-04: La salida cumple estrictamente con agent-result.schema.json y tiene huella valida."""
        brief = {"title": "Sistema X", "objective": "Obj X"}
        task = {"task_id": "TSK-002-ARCH"}
        ok, res, _ = self.architect.execute_architecture(task, brief)
        self.assertTrue(ok)
        self.result_validator.validate(res)
        self.assertTrue(res["fingerprint"].startswith("sha256:"))
        self.assertEqual(len(res["fingerprint"]), 71)

    def test_ac05_runtime_integration(self) -> None:
        """AC-05: El Product Architect se encuentra registrado e integrable en HQRuntime."""
        specialist = self.runtime.get_specialist("product_architect")
        self.assertIsNotNone(specialist)
        self.assertIsInstance(specialist, product_architect.ProductArchitect)


if __name__ == "__main__":
    unittest.main()
