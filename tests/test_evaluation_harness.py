"""Pruebas exhaustivas para el Harness de Evaluacion y Separacion de Holdout (PZ-011A).

Valida separacion estricta entre entradas de agente y aserciones de evaluador,
verificacion de checksums de dataset, cobertura de 10 categorias y aislamiento del holdout.
"""

import json
import tempfile
import unittest
from pathlib import Path

import app.evaluation_harness as evaluation_harness


class TestEvaluationHarness(unittest.TestCase):
    """Suite de pruebas para PZ-011A (Evaluation Harness)."""

    def setUp(self) -> None:
        self.harness = evaluation_harness.EvaluationHarness(manifest_path="evaluation/dataset_manifest.json")

    def test_ac01_agent_input_isolation(self) -> None:
        """AC-01: La funcion sanitize_agent_input remueve las expectativas del evaluador y no las filtra al agente."""
        raw_case = {
            "case_id": "CASE-TEST-001",
            "category": "CORRECTA",
            "input_mission": {"title": "Mision Alpha", "objective": "Objetivo"},
            "expected_verdict": "SUCCESS",
            "expected_state": "AUTORIZADA_PARA_EJECUTAR",
        }

        sanitized = self.harness.sanitize_agent_input(raw_case)
        self.assertNotIn("expected_verdict", sanitized)
        self.assertNotIn("expected_state", sanitized)
        self.assertEqual(sanitized["title"], "Mision Alpha")

    def test_ac02_checksum_verification_and_tamper_detection(self) -> None:
        """AC-02: Modificar dev_cases.json invalida la carga con CHECKSUM_MISMATCH."""
        # 1. Carga normal debe pasar con el archivo legitimo
        ok_valid, cases, _ = self.harness.load_dev_cases()
        self.assertTrue(ok_valid)
        self.assertEqual(len(cases), 8)

        # 2. Archivo manipulado en directorio temporal
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_eval_dir = Path(tmp_dir) / "evaluation"
            tmp_eval_dir.mkdir()

            # Copiar manifest
            with open("evaluation/dataset_manifest.json", "r", encoding="utf-8") as f:
                manifest_content = f.read()
            with open(tmp_eval_dir / "dataset_manifest.json", "w", encoding="utf-8") as f:
                f.write(manifest_content)

            # Escribir dev_cases alterado
            with open(tmp_eval_dir / "dev_cases.json", "w", encoding="utf-8") as f:
                f.write('[{"tampered": true}]')

            temp_harness = evaluation_harness.EvaluationHarness(manifest_path=str(tmp_eval_dir / "dataset_manifest.json"))
            ok_bad, _, err_bad = temp_harness.load_dev_cases(base_dir=tmp_dir)
            self.assertFalse(ok_bad)
            self.assertIn("CHECKSUM_MISMATCH", err_bad)

    def test_ac03_ten_categories_declared_in_manifest(self) -> None:
        """AC-03: Las 10 categorias normativas del contrato estan presentes en el manifest."""
        ok, manifest, _ = self.harness.load_manifest()
        self.assertTrue(ok)
        categories = manifest.get("categories", [])
        expected_cats = {
            "CORRECTA",
            "AMBIGUA",
            "EVIDENCIA_INSUFICIENTE",
            "CONTRADICCION",
            "MEZCLA",
            "RECHAZO",
            "INTERRUPCION",
            "ORIGINAL_ELIMINADO",
            "MEMORIA_CONFLICTIVA",
            "ACCION_PROHIBIDA",
        }
        self.assertEqual(set(categories), expected_cats)

    def test_ac04_holdout_and_dev_cases_do_not_overlap(self) -> None:
        """AC-04: Los casos de desarrollo y los casos reservados de holdout no se solapan."""
        ok_m, manifest, _ = self.harness.load_manifest()
        self.assertTrue(ok_m)

        ok_d, dev_cases, _ = self.harness.load_dev_cases()
        self.assertTrue(ok_d)

        dev_cats = {c["category"] for c in dev_cases}
        holdout_cats = set(manifest["splits"]["holdout_reserved"]["categories"])

        # Las categorias reservadas de holdout no estan en dev_cases
        self.assertTrue(holdout_cats.isdisjoint(dev_cats))

    def test_ac05_deterministic_runner_execution(self) -> None:
        """AC-05: El harness ejecuta deterministamente los casos con un runner sintetico y genera metricas."""
        ok_d, dev_cases, _ = self.harness.load_dev_cases()
        self.assertTrue(ok_d)

        # Runner que responde conforme a la logica esperada
        def mock_runner(agent_input: dict) -> dict:
            title = agent_input.get("title", "")
            if "Crear algo nuevo" in title:
                return {"verdict": "CLARIFICATION_REQUIRED", "state": "BORRADOR"}
            elif "sin fuentes" in title.lower() or "startup" in title.lower():
                return {"verdict": "EVIDENCIA_NO_DISPONIBLE", "state": "BLOCKED"}
            elif "contradictorio" in title.lower() or "normativo" in title.lower():
                return {"verdict": "CONTRADICTION_FLAGGED", "state": "PENDIENTE_DECISION_HUMANA"}
            elif "logistica" in title.lower():
                return {"verdict": "REJECTED", "state": "PLAN_EN_REVISION"}
            elif "interrumpido" in title.lower():
                return {"verdict": "PAUSED_INDETERMINATE", "state": "PAUSADA"}
            elif "despliegue" in title.lower():
                return {"verdict": "SECURITY_BLOCK", "state": "BLOQUEADA"}
            else:
                return {"verdict": "SUCCESS", "state": "AUTORIZADA_PARA_EJECUTAR"}

        benchmark = self.harness.run_benchmark(dev_cases[:2], mock_runner)
        self.assertEqual(benchmark["total_cases_evaluated"], 2)
        self.assertEqual(benchmark["passed_cases"], 2)
        self.assertEqual(benchmark["accuracy"], 1.0)
        self.assertEqual(benchmark["holdout_status"], "HOLDOUT_NO_PROPORCIONADO_EVALUACION_PARCIAL")


if __name__ == "__main__":
    unittest.main()
