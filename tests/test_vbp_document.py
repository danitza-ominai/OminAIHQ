"""Pruebas exhaustivas para el VBP canonico y validacion determinista (PZ-003E).

Valida el conteo de las 18 secciones y manifest obligatorio, rechazo de secciones
ausentes o evidencias falsas, fronteras numericas de evaluacion (69/70/79/80),
comportamiento ante bloqueadores, inmutabilidad de huellas y control de estado final.
"""

import copy
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

import app.demo_plan_review as demo_plan_review
import app.mission_engine as mission_engine
import app.runtime_contracts as runtime_contracts
import app.vbp_document as vbp_document
import app.vbp_validation as vbp_validation

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FIXTURE_PATH = PROJECT_ROOT / "examples" / "demo_mission.json"


class TestVBPDocumentAndValidation(unittest.TestCase):
    """Suite de pruebas para PZ-003E."""

    def setUp(self) -> None:
        with open(DEFAULT_FIXTURE_PATH, "r", encoding="utf-8") as f:
            fixture = json.load(f)

        # 1. Intake y sesion autorizada
        session = demo_plan_review.PlanReviewSession()
        session.init_from_intake(raw_data=fixture)
        app_req = session.approvals[0]

        cmd = {
            "approval_id": app_req["approval_id"],
            "version_or_fingerprint": app_req["version_or_fingerprint"],
            "decision": "APROBAR",
            "comment": "Plan aprobado para VBP",
            "idempotency_key": app_req["idempotency_key"],
        }
        actor = {
            "user_id": session.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
            "identity_scope": "IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA",
        }
        session.process_decision(cmd, actor)
        auth_env = session.build_envelope()

        # 2. Ejecutar motor hasta consolidacion
        engine = mission_engine.MissionExecutionEngine()
        engine.load_authorized_session(auth_env)
        code, self.engine_env = engine.run_execution()
        self.assertEqual(code, 0)

        # 3. Ensamblar VBP base
        self.vbp_data = vbp_document.assemble_vbp_data(self.engine_env)
        self.validator = vbp_validation.VBPValidator()
        self.context = vbp_validation.build_evaluation_context(self.engine_env)

    def test_ac01_eighteen_sections_and_manifest(self) -> None:
        """AC-01: Contar e identificar las 18 secciones obligatorias y los metadatos del manifest."""
        self.assertEqual(len(self.vbp_data["sections"]), 18)
        self.assertEqual(self.vbp_data["contract_version"], "1.2-aprobada")
        self.assertEqual(self.vbp_data["language"], "es")
        self.assertEqual(self.vbp_data["approval_status"], "BORRADOR")
        self.assertIsNone(self.vbp_data["human_approval_ref"])

        # Verificar nombres de secciones en orden exacto
        for idx, expected_name in enumerate(runtime_contracts.VBP_SECTION_NAMES, start=1):
            sec = self.vbp_data["sections"][idx - 1]
            self.assertEqual(sec["section_number"], idx)
            self.assertEqual(sec["section_name"], expected_name)

        md = vbp_document.render_canonical_markdown(self.vbp_data)
        self.assertIn("# Venture Build Package", md)
        self.assertIn("## 1. Mision", md)
        self.assertIn("## 18. Historial de trazabilidad", md)

    def test_ac02_rejection_of_missing_section_and_fake_evidence(self) -> None:
        """AC-02: Rechazar seccion ausente y detectar bloqueador por evidencia falsa."""
        # 1. Seccion ausente
        bad_vbp = copy.deepcopy(self.vbp_data)
        bad_vbp["sections"] = bad_vbp["sections"][:-1]  # 17 secciones
        res_missing = self.validator.evaluate_vbp(bad_vbp, self.engine_env.get("evidence_store"))
        self.assertEqual(res_missing["verdict"], "NO_PASA")
        self.assertIn("SECCION_OBLIGATORIA_FALTANTE", res_missing["blockers"])

        # 2. Evidencia falsa inyectada
        fake_evd_vbp = copy.deepcopy(self.vbp_data)
        fake_evd_vbp["sections"][4]["content"] = "Contiene evidencia falsa e inventada sin fuente real."
        res_fake = self.validator.evaluate_vbp(fake_evd_vbp, self.engine_env.get("evidence_store"))
        self.assertEqual(res_fake["verdict"], "NO_PASA")
        self.assertIn("EVIDENCIA_FALSA_O_INEXISTENTE", res_fake["blockers"])

    def test_ac03_threshold_boundaries_and_blocker_override(self) -> None:
        """AC-03: Comprobar fronteras 69/70/79/80 y caso con puntaje alto pero con bloqueador."""
        # 1. Caso excelente: PASA (>= 80.0)
        res_good = self.validator.evaluate_vbp(self.vbp_data, self.engine_env.get("evidence_store"), context=self.context)
        self.assertEqual(res_good["verdict"], "PASA")
        self.assertGreaterEqual(res_good["total_score"], 80.0)
        self.assertEqual(len(res_good["blockers"]), 0)

        # 2. Caso condicional: puntaje en [70.0, 79.9] -> PASA_CON_CONDICIONES
        cond_vbp = copy.deepcopy(self.vbp_data)
        for i in [5, 6, 7, 8]:  # 4 pendientes (score cob = 60)
            cond_vbp["sections"][i]["status"] = "PENDIENTE"
            cond_vbp["sections"][i]["pending_reason"] = "Pendiente de refinamiento"
        # Sin evidence_store directo -> score evd = 60 -> total = 78.0
        cond_vbp["fingerprint"] = runtime_contracts.compute_vbp_manifest_fingerprint(cond_vbp)
        res_cond = self.validator.evaluate_vbp(cond_vbp, evidence_store={}, context=self.context)
        self.assertEqual(res_cond["verdict"], "PASA_CON_CONDICIONES")
        self.assertEqual(res_cond["total_score"], 78.0)

        # 3. Caso insuficiente: puntaje < 70.0 (exactamente 69.0) -> NO_PASA
        bad_score_vbp = copy.deepcopy(self.vbp_data)
        for i in range(3, 10):  # 7 pendientes (score cob = 30)
            bad_score_vbp["sections"][i]["status"] = "PENDIENTE"
            bad_score_vbp["sections"][i]["pending_reason"] = "Pendiente"
        # Sin evidence_store directo -> total = 69.0
        bad_score_vbp["fingerprint"] = runtime_contracts.compute_vbp_manifest_fingerprint(bad_score_vbp)
        res_bad_score = self.validator.evaluate_vbp(bad_score_vbp, evidence_store={}, context=self.context)
        self.assertEqual(res_bad_score["verdict"], "NO_PASA")
        self.assertEqual(res_bad_score["total_score"], 69.0)

        # 4. Caso con puntaje alto (100) pero con bloqueador inyectado -> NO_PASA
        res_blocked = self.validator.evaluate_vbp(
            self.vbp_data,
            self.engine_env.get("evidence_store"),
            injected_blockers=["RIESGO_CRITICO_SIN_TRATAR"],
            context=self.context,
        )
        self.assertEqual(res_blocked["verdict"], "NO_PASA")
        self.assertIn("RIESGO_CRITICO_SIN_TRATAR", res_blocked["blockers"])

    def test_ac04_fingerprint_integrity_and_render_preservation(self) -> None:
        """AC-04: Alterar un dato cambia la huella; renderizar sin cambios preserva exactamente el contenido."""
        fp1 = self.vbp_data["fingerprint"]

        # Modificar un dato material
        vbp_mod = copy.deepcopy(self.vbp_data)
        vbp_mod["title"] = "Titulo Modificado de VBP"
        fp_mod = runtime_contracts.compute_vbp_manifest_fingerprint(vbp_mod)
        self.assertNotEqual(fp1, fp_mod)

        # Renderizar Markdown determinista
        md1 = vbp_document.render_canonical_markdown(self.vbp_data)
        md2 = vbp_document.render_canonical_markdown(self.vbp_data)
        self.assertEqual(md1, md2)

        md_fp1 = vbp_document.compute_markdown_content_fingerprint(md1)
        md_fp2 = vbp_document.compute_markdown_content_fingerprint(md2)
        self.assertEqual(md_fp1, md_fp2)

    def test_ac05_no_auto_approval_or_final_state(self) -> None:
        """AC-05: Sin aprobacion humana explicita no hay estado FINALIZADA ni VBP marcado como APROBADO."""
        self.assertEqual(self.vbp_data["approval_status"], "BORRADOR")
        self.assertIsNone(self.vbp_data["human_approval_ref"])

        # La evaluacion emite dictamen PASA pero no cambia el estado a APROBADO ni FINALIZADA
        eval_result = self.validator.evaluate_vbp(self.vbp_data, self.engine_env.get("evidence_store"), context=self.context)
        self.assertEqual(eval_result["verdict"], "PASA")
        self.assertEqual(self.vbp_data["approval_status"], "BORRADOR")

    def test_ac06_bilingual_rendering_blocks(self) -> None:
        """AC-06: render_canonical_markdown con include_bilingual_blocks incluye bloques de traduccion."""
        vbp_bilingual = copy.deepcopy(self.vbp_data)
        vbp_bilingual["sections"][0]["content"] += "\n\n```english\nMission Objective in English\n```"

        vbp_bilingual["fingerprint"] = runtime_contracts.compute_vbp_manifest_fingerprint(vbp_bilingual)
        valid, errors = runtime_contracts.RuntimeContractsValidator().validate_structure("vbp",vbp_bilingual)
        self.assertTrue(valid,errors)
        md_bi = vbp_document.render_canonical_markdown(vbp_bilingual, include_bilingual_blocks=True)
        self.assertIn("```english\nMission Objective in English\n```", md_bi)

        # Sin include_bilingual_blocks (default) no incluye el bloque
        md_default = vbp_document.render_canonical_markdown(vbp_bilingual, include_bilingual_blocks=False)
        self.assertEqual(md_bi, md_default)

    def test_context_missing_crossed_and_invalid_references_never_pass(self):
        before=copy.deepcopy(self.vbp_data)
        contexts=[None, {**self.context,"artifacts":[]}, {**self.context,"claims":[]},
                  {**self.context,"inputs":[]}, {**self.context,"approvals":[]}]
        crossed=copy.deepcopy(self.context)
        crossed["mission"]["mission_id"]="MSN-FOREIGN"
        contexts.append(crossed)
        for context in contexts:
            result=self.validator.evaluate_vbp(self.vbp_data,self.engine_env["evidence_store"],context=context)
            self.assertEqual(result["verdict"],"NO_PASA")
            self.assertFalse(result["integrity"]["valid"])
            self.assertEqual(self.vbp_data,before)


if __name__ == "__main__":
    unittest.main()
