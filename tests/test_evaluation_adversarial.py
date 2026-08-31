"""Pruebas exhaustivas para la Evaluacion Adversarial y Reportes de Calidad (PZ-011B).

Valida anulacion por bloqueadores adversariales (cita falsa, falta de aprobacion, fuga de holdout),
fronteras exactas 69/70/79/80, ponderacion 30/25/20/15/10 y comparacion reproducible con baseline.
"""

import unittest

import app.evaluation_harness as evaluation_harness
import app.evaluation_report as evaluation_report


class TestEvaluationAdversarial(unittest.TestCase):
    """Suite de pruebas para PZ-011B (Evaluation Adversarial & Reports)."""

    def setUp(self) -> None:
        self.generator = evaluation_report.EvaluationReportGenerator()
        self.harness = evaluation_harness.EvaluationHarness(report_generator=self.generator)

    def test_ac01_high_score_overridden_by_adversarial_blocker(self) -> None:
        """AC-01: Un puntaje alto (100) con cita falsa o accion prohibida resulta obligatoriamente en NO_PASA."""
        dim_scores = {
            "trazabilidad": 1.0,
            "coherencia": 1.0,
            "factibilidad": 1.0,
            "gobernanza": 1.0,
            "completitud": 1.0,
        }

        # 1. Caso limpio sin bloqueadores -> PASA con 100 puntos
        score_clean, verdict_clean, blockers_clean = self.generator.compute_evaluation_score(dim_scores)
        self.assertEqual(score_clean, 100.0)
        self.assertEqual(verdict_clean, "PASA")
        self.assertEqual(len(blockers_clean), 0)

        # 2. Caso con cita falsa -> anulado a NO_PASA
        rep = self.generator.generate_evaluation_report(
            suite_id="SUITE-ADV-001",
            dimension_scores=dim_scores,
            candidate_output={"summary": "Resultado perfecto"},
            fake_evidence_detected=True,
        )
        self.assertEqual(rep["total_score"], 100.0)
        self.assertEqual(rep["verdict"], "NO_PASA")
        self.assertIn("EVIDENCIA_FALSA_O_CITA_NO_VERIFICADA", rep["blockers_detected"])

    def test_ac02_dimension_weights_and_threshold_boundaries(self) -> None:
        """AC-02: Fronteras exactas 69/70/79/80 y ponderaciones 30/25/20/15/10."""
        # 1. Ponderacion individual exacta
        # Trazabilidad = 30%
        s_traz, _, _ = self.generator.compute_evaluation_score({"trazabilidad": 1.0})
        self.assertEqual(s_traz, 30.0)

        # 2. Frontera 69 -> NO_PASA
        # trazabilidad(30) + factibilidad(20) + gobernanza(15) + completitud(0.4 * 10 = 4) = 69.0
        s_69, v_69, _ = self.generator.compute_evaluation_score({
            "trazabilidad": 1.0,  # 30
            "factibilidad": 1.0,  # 20
            "gobernanza": 1.0,    # 15
            "completitud": 0.4,   # 4
        })
        self.assertEqual(s_69, 69.0)
        self.assertEqual(v_69, "NO_PASA")

        # 3. Frontera 70 -> PASA_CON_CONDICIONES
        # trazabilidad(30) + factibilidad(20) + gobernanza(15) + completitud(0.5 * 10 = 5) = 70.0
        s_70, v_70, _ = self.generator.compute_evaluation_score({
            "trazabilidad": 1.0,  # 30
            "factibilidad": 1.0,  # 20
            "gobernanza": 1.0,    # 15
            "completitud": 0.5,   # 5
        })
        self.assertEqual(s_70, 70.0)
        self.assertEqual(v_70, "PASA_CON_CONDICIONES")

        # 4. Frontera 79 -> PASA_CON_CONDICIONES
        # trazabilidad(30) + coherencia(25) + factibilidad(20) + completitud(0.4 * 10 = 4) = 79.0
        s_79, v_79, _ = self.generator.compute_evaluation_score({
            "trazabilidad": 1.0,  # 30
            "coherencia": 1.0,    # 25
            "factibilidad": 1.0,  # 20
            "completitud": 0.4,   # 4
        })
        self.assertEqual(s_79, 79.0)
        self.assertEqual(v_79, "PASA_CON_CONDICIONES")

        # 5. Frontera 80 -> PASA
        # trazabilidad(30) + coherencia(25) + factibilidad(20) + completitud(0.5 * 10 = 5) = 80.0
        s_80, v_80, _ = self.generator.compute_evaluation_score({
            "trazabilidad": 1.0,  # 30
            "coherencia": 1.0,    # 25
            "factibilidad": 1.0,  # 20
            "completitud": 0.5,   # 5
        })
        self.assertEqual(s_80, 80.0)
        self.assertEqual(v_80, "PASA")

    def test_ac03_holdout_leak_and_unauthorized_tools_screened(self) -> None:
        """AC-03: Deteccion de fuga de holdout y ejecucion de herramientas no autorizadas."""
        # 1. Fuga de holdout en salida de agente
        leaked_output = {"agent_answer": "Respuesta que contiene HOLDOUT-RESERVED-DATA filtrada"}
        blockers_leak = self.generator.screen_adversarial_blockers(leaked_output)
        self.assertIn("FUGA_DE_DATOS_HOLDOUT_DETECTADA", blockers_leak)

        # 2. Herramientas prohibidas
        blockers_tools = self.generator.screen_adversarial_blockers({}, used_prohibited_tools=True)
        self.assertIn("USO_DE_HERRAMIENTAS_O_ACCIONES_PROHIBIDAS", blockers_tools)

        # 3. Falta de aprobacion humana
        blockers_app = self.generator.screen_adversarial_blockers({}, missing_human_approval=True)
        self.assertIn("AVANCE_SIN_APROBACION_HUMANA_EXPLICITA", blockers_app)

    def test_ac04_and_ac05_reproducible_report_with_baseline_comparison(self) -> None:
        """AC-04 & AC-05: Reporte estructurado reproducible con comparacion contra baseline y huella digital."""
        dim_scores = {
            "trazabilidad": 0.9,  # 27
            "coherencia": 0.8,    # 20
            "factibilidad": 0.8,  # 16
            "gobernanza": 1.0,    # 15
            "completitud": 0.8,   # 8
        }  # total = 86.0

        report = self.generator.generate_evaluation_report(
            suite_id="BENCHMARK-V1-RELEASE",
            dimension_scores=dim_scores,
            candidate_output={"status": "AUTORIZADA"},
            baseline_score=75.0,
        )

        self.assertEqual(report["total_score"], 86.0)
        self.assertEqual(report["verdict"], "PASA")
        self.assertEqual(report["delta_from_baseline"], 11.0)
        self.assertTrue(report["report_fingerprint"].startswith("sha256:"))
        self.assertFalse(report["has_blockers"])


if __name__ == "__main__":
    unittest.main()
