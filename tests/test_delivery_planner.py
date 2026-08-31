"""Pruebas exhaustivas para el Agente Delivery Planner (PZ-007A).

Valida estructuracion de fases de entrega, trazabilidad de tareas a requisitos/riesgos,
deteccion de ciclos y autodependencias en el grafo, declaracion de supuestos de estimacion,
y validacion estricta contra agent-result.schema.json.
"""

import unittest

import app.delivery_planner as delivery_planner
import app.hq_runtime as hq_runtime
import app.runtime_contracts as runtime_contracts
from jsonschema import Draft202012Validator


class TestDeliveryPlanner(unittest.TestCase):
    """Suite de pruebas para PZ-007A."""

    def setUp(self) -> None:
        self.planner = delivery_planner.DeliveryPlanner()
        self.runtime = hq_runtime.HQRuntime()
        _, self.agent_result_schema, _, _ = runtime_contracts.load_runtime_contracts()
        self.result_validator = Draft202012Validator(self.agent_result_schema)

    def test_ac01_traceability_of_phases_to_requirements(self) -> None:
        """AC-01: Fases y tareas estan trazadas a requisitos y riesgos identificados."""
        brief = {"title": "Portal B2B", "objective": "Objetivo"}
        task = {"task_id": "TSK-003-PLAN", "mission_id": "MSN-SIM-001"}
        arch_results = {"evidence_refs": ["EVD-CLAIM-001"]}

        ok, res, err = self.planner.execute_planning(task, brief, arch_results)
        self.assertTrue(ok)
        self.assertIsNotNone(res)
        self.result_validator.validate(res)

        self.assertEqual(res["agent_role"], "delivery_planner")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertGreaterEqual(len(res["proposals"]), 4)
        self.assertGreaterEqual(len(res["risks"]), 1)

    def test_ac02_dependency_graph_cycle_and_fault_detection(self) -> None:
        """AC-02: Deteccion de ciclos, autodependencias y referencias inexistentes."""
        # 1. Autodependencia
        self_dep_tasks = [
            {"task_id": "T1", "dependencies": ["T1"]},
        ]
        ok_self, msg_self = self.planner.validate_dependency_graph(self_dep_tasks)
        self.assertFalse(ok_self)
        self.assertIn("Autodependencia", msg_self)

        # 2. Referencia rota / inexistente
        broken_tasks = [
            {"task_id": "T1", "dependencies": ["T_INEXISTENTE"]},
        ]
        ok_brk, msg_brk = self.planner.validate_dependency_graph(broken_tasks)
        self.assertFalse(ok_brk)
        self.assertIn("inexistente", msg_brk)

        # 3. Ciclo directo T1 -> T2 -> T1
        cyclic_tasks = [
            {"task_id": "T1", "dependencies": ["T2"]},
            {"task_id": "T2", "dependencies": ["T1"]},
        ]
        ok_cyc, msg_cyc = self.planner.validate_dependency_graph(cyclic_tasks)
        self.assertFalse(ok_cyc)
        self.assertIn("Ciclo", msg_cyc)

        # 4. Grafo aciclico valido
        valid_tasks = [
            {"task_id": "T1", "dependencies": []},
            {"task_id": "T2", "dependencies": ["T1"]},
            {"task_id": "T3", "dependencies": ["T2"]},
        ]
        ok_val, msg_val = self.planner.validate_dependency_graph(valid_tasks)
        self.assertTrue(ok_val)
        self.assertIsNone(msg_val)

    def test_ac03_estimates_declared_as_assumptions(self) -> None:
        """AC-03: Las estimaciones quedan formalmente como supuestos, no como hechos contractuales."""
        brief = {"title": "App X", "objective": "Obj X"}
        task = {"task_id": "TSK-003-PLAN"}

        ok, res, _ = self.planner.execute_planning(task, brief)
        self.assertTrue(ok)
        self.result_validator.validate(res)

        assumptions = res["assumptions"]
        self.assertTrue(any("SUPUESTO" in a for a in assumptions))
        self.assertTrue(any("supuestos tecnicos" in a.lower() for a in assumptions))

    def test_ac04_schema_conformance_and_fingerprint(self) -> None:
        """AC-04: La salida cumple con agent-result.schema.json y tiene huella SHA-256 valida."""
        brief = {"title": "Sistema Y", "objective": "Obj Y"}
        task = {"task_id": "TSK-003-PLAN"}
        ok, res, _ = self.planner.execute_planning(task, brief)
        self.assertTrue(ok)
        self.result_validator.validate(res)
        self.assertTrue(res["fingerprint"].startswith("sha256:"))
        self.assertEqual(len(res["fingerprint"]), 71)

    def test_ac05_runtime_integration(self) -> None:
        """AC-05: El Delivery Planner se encuentra registrado e integrable en HQRuntime."""
        specialist = self.runtime.get_specialist("delivery_planner")
        self.assertIsNotNone(specialist)
        self.assertIsInstance(specialist, delivery_planner.DeliveryPlanner)


if __name__ == "__main__":
    unittest.main()
