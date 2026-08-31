"""Pruebas exhaustivas para el Chief of Staff y composicion del Runtime (PZ-004B).

Valida ciclos de aclaracion (limite 3), propuesta de plan, invalidacion de aprobacion
ante cambios de brief, aislamiento de secretos, y deteccion de especialistas faltantes en el runtime.
"""

import copy
import unittest

import app.chief_of_staff as chief_of_staff
import app.demo_plan_review as demo_plan_review
import app.hq_runtime as hq_runtime


class TestChiefOfStaffAndRuntime(unittest.TestCase):
    """Suite de pruebas para PZ-004B."""

    def setUp(self) -> None:
        self.chief = chief_of_staff.ChiefOfStaff()
        self.runtime = hq_runtime.HQRuntime()

    def test_ac01_mission_clarification_cycles_and_limit(self) -> None:
        """AC-01: Validar mision completa, formular aclaraciones y detenerse en el ciclo 3/4."""
        # 1. Mision completa
        complete_mission = {
            "title": "Portal B2B",
            "objective": "Desarrollar portal de autoservicio",
            "context": "Empresa distribuidora con ERP heredado",
            "expected_result": "VBP para implementar el portal en 90 dias",
        }
        ok, brief, questions, err = self.chief.evaluate_and_clarify_mission(complete_mission, clarification_cycle=0)
        self.assertTrue(ok)
        self.assertIsNotNone(brief)
        self.assertIsNone(questions)
        self.assertIsNone(err)

        # 2. Mision incompleta (falta objective y context)
        incomplete_mission = {
            "title": "Portal B2B",
            "objective": "",
            "context": "",
            "expected_result": "VBP",
        }
        ok_inc, brief_inc, questions_inc, err_inc = self.chief.evaluate_and_clarify_mission(incomplete_mission, clarification_cycle=1)
        self.assertFalse(ok_inc)
        self.assertIsNone(brief_inc)
        self.assertEqual(len(questions_inc), 2)
        self.assertIn("objective", questions_inc[0])

        # 3. Superar limite de 3 ciclos de aclaracion (ciclo 3 solicita cuarto intento)
        ok_lim, _, _, err_lim = self.chief.evaluate_and_clarify_mission(incomplete_mission, clarification_cycle=3)
        self.assertFalse(ok_lim)
        self.assertIsNotNone(err_lim)
        self.assertEqual(err_lim["error_code"], "BUDGET_EXHAUSTED")

    def test_ac02_brief_modification_invalidates_plan_fingerprint(self) -> None:
        """AC-02: Modificar el brief invalida la huella exacta de aprobacion previa."""
        brief1 = {
            "user_id": "USR-001",
            "title": "Titulo Original",
            "objective": "Objetivo 1",
            "context": "Contexto 1",
            "expected_result": "Resultado 1",
            "constraints": ["C1"],
            "assumptions": [],
            "pending_decisions": [],
            "simulation_status": "SIMULADA",
        }
        ok, plan, _ = self.chief.propose_plan("MSN-001", brief1, plan_version=1)
        self.assertTrue(ok)

        fp1 = demo_plan_review.compute_plan_fingerprint("MSN-001", "USR-001", 1, 1, brief1, plan)

        # Modificar brief
        brief2 = copy.deepcopy(brief1)
        brief2["objective"] = "Objetivo Modificado que cambia el alcance"
        fp2 = demo_plan_review.compute_plan_fingerprint("MSN-001", "USR-001", 2, 1, brief2, plan)

        self.assertNotEqual(fp1, fp2)

    def test_ac03_sanitized_invocation_context(self) -> None:
        """AC-03: La invocacion del Chief no incluye secretos ni datos no autorizados."""
        ok_clean, msg = self.chief.gateway.sanitize_outbound_data("Eres Chief", "Analiza la mision")
        self.assertTrue(ok_clean)
        self.assertIsNone(msg)

        ok_bad, msg_bad = self.chief.gateway.sanitize_outbound_data("Eres Chief", "api_key = 'AIzaSyD982347289347289347293472934'")
        self.assertFalse(ok_bad)
        self.assertIsNotNone(msg_bad)

    def test_ac04_missing_specialist_blocks_runtime(self) -> None:
        """AC-04: Si falta un especialista requerido en el runtime, este reporta no listo y bloquea."""
        empty_runtime = hq_runtime.HQRuntime()
        empty_runtime.specialists.clear()
        ready_empty, missing_empty = empty_runtime.validate_runtime_readiness()
        self.assertFalse(ready_empty)
        self.assertIn("research_evidence_analyst", missing_empty)
        self.assertIn("product_architect", missing_empty)
        self.assertIn("delivery_planner", missing_empty)
        self.assertIn("governance_risk", missing_empty)

        # En runtime por defecto todos los 5 roles requeridos estan registrados
        ready, missing = self.runtime.validate_runtime_readiness()
        self.assertTrue(ready)
        self.assertEqual(len(missing), 0)

    def test_ac05_all_outputs_in_spanish(self) -> None:
        """AC-05: El Chief genera planes y tareas con descripciones en espanol."""
        brief = {
            "title": "Mision Demo",
            "objective": "Objetivo",
            "context": "Contexto",
            "expected_result": "Resultado",
            "simulation_status": "SIMULADA",
        }
        ok, plan, _ = self.chief.propose_plan("MSN-001", brief)
        self.assertTrue(ok)
        self.assertEqual(len(plan["tasks"]), 4)
        for t in plan["tasks"]:
            self.assertTrue(any(c in "áéíóúñÁÉÍÓÚÑ" or "de" in t["objective"] for c in t["objective"]))


if __name__ == "__main__":
    unittest.main()
