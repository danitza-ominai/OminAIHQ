"""Pruebas exhaustivas para la Exportacion y Verificacion Canonica de VBP (PZ-013C).

Valida precondiciones de exportacion, verificacion de huellas de integridad SHA-256,
existencia de las 18 secciones obligatorias, referencia a aprobacion humana,
idempotencia de bytes y generacion de archivos .md descargables.
Cumple estrictamente con CONTRATO-MVP-v1.md secciones 6.1-6.6, 9.6, RF-018, RF-030 y FICHA-PZ-013C.md.
"""

import copy
import json
import tempfile
import unittest
from pathlib import Path

import app.demo_intake as demo_intake
import app.demo_plan_review as demo_plan_review
import app.mission_engine as mission_engine
import app.runtime_contracts as runtime_contracts
import app.vbp_document as vbp_document
import app.vbp_export as vbp_export

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FIXTURE_PATH = PROJECT_ROOT / "examples" / "demo_mission.json"


class TestVBPExport(unittest.TestCase):
    """Suite de pruebas unitarias para PZ-013C (VBP Export)."""

    def setUp(self) -> None:
        from test_human_approvals import fixture
        runtime,self.repo,ctx,request=fixture(stage="approved")
        self.addCleanup(self.repo.close)
        self.vbp_approved=self.repo.get_object("candidate","MSN-SIM:GATE_2_VBP")
        self.vbp_draft=copy.deepcopy(self.vbp_approved)
        self.vbp_draft.update(approval_status="BORRADOR",human_approval_ref=None)

    def test_ac01_rejection_of_unapproved_vbp(self) -> None:
        """AC-01 & AC-03: Rechazar exportacion si el VBP esta en estado BORRADOR sin aprobacion humana."""
        # 1. VBP en BORRADOR sin aprobacion humana
        ok, err = vbp_export.validate_vbp_export_preconditions(self.vbp_draft)
        self.assertFalse(ok)
        self.assertIn("NOT_APPROVED", err)

        # Intento de exportar bytes falla con codigo no aprobado
        ok_bytes, raw_bytes, meta, err_b = vbp_export.export_canonical_vbp_bytes(self.vbp_draft)
        self.assertFalse(ok_bytes)
        self.assertIsNone(raw_bytes)
        self.assertIn("NOT_APPROVED", err_b)

    def test_ac02_successful_export_of_approved_vbp(self) -> None:
        """AC-02: Exportacion exitosa de VBP aprobado genera Markdown canonico y metadatos correctos."""
        ok, md_text, meta = vbp_export.export_canonical_vbp_markdown(self.vbp_approved, repository=self.repo)
        self.assertTrue(ok)
        self.assertIsNotNone(md_text)
        self.assertIn("Venture Build Package", md_text)
        self.assertIn("## 1. Mision", md_text)
        self.assertIn("## 18. Historial de trazabilidad", md_text)

        self.assertEqual(meta["vbp_id"], self.vbp_approved["vbp_id"])
        self.assertEqual(meta["manifest_fingerprint"], self.vbp_approved["fingerprint"])
        self.assertEqual(meta["filename"], f"{self.vbp_approved['vbp_id']}.md")
        self.assertEqual(meta["mime_type"], "text/markdown; charset=utf-8")

    def test_ac03_fingerprint_integrity_and_tampering_detection(self) -> None:
        """AC-03: Si el contenido del VBP es manipulado sin recalcular huella, la exportacion es rechazada."""
        tampered_vbp = copy.deepcopy(self.vbp_approved)
        tampered_vbp["title"] = "Titulo Manipulado Silenciosamente"
        # Dejamos la huella antigua
        ok, err = vbp_export.validate_vbp_export_preconditions(tampered_vbp)
        self.assertFalse(ok)
        self.assertIn("INTEGRITY_FINGERPRINT_MISMATCH", err)

    def test_ac04_missing_or_invalid_sections_rejection(self) -> None:
        """AC-04: Si falta alguna de las 18 secciones obligatorias, la exportacion falla."""
        # VBP con solo 17 secciones
        bad_sections_vbp = copy.deepcopy(self.vbp_approved)
        bad_sections_vbp["sections"] = bad_sections_vbp["sections"][:17]
        bad_sections_vbp["fingerprint"] = runtime_contracts.compute_vbp_manifest_fingerprint(bad_sections_vbp)

        ok, err = vbp_export.validate_vbp_export_preconditions(bad_sections_vbp)
        self.assertFalse(ok)
        self.assertIn("SECTION_COUNT_INVALID", err)

    def test_ac05_idempotency_of_export_bytes_and_file_write(self) -> None:
        """AC-05: La exportacion es estrictamente idempotente; escribir a archivo es atomico."""
        ok1, bytes1, meta1, _ = vbp_export.export_canonical_vbp_bytes(self.vbp_approved, repository=self.repo)
        ok2, bytes2, meta2, _ = vbp_export.export_canonical_vbp_bytes(self.vbp_approved, repository=self.repo)
        self.assertTrue(ok1 and ok2)
        self.assertEqual(bytes1, bytes2)
        self.assertEqual(meta1["markdown_fingerprint"], meta2["markdown_fingerprint"])

        # Probar escritura atomica a archivo
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            out_file = Path(tmp_dir) / "test_vbp_download.md"
            ok_w, err_w = vbp_export.export_vbp_to_file(self.vbp_approved, out_file, repository=self.repo)
            self.assertTrue(ok_w)
            self.assertIsNone(err_w)
            self.assertTrue(out_file.exists())
            self.assertEqual(out_file.read_bytes(), bytes1)


class TestForgedExport(unittest.TestCase):
    def test_approval_label_must_match_exact_persisted_decision(self):
        from test_human_approvals import fixture
        for stage, label in (("approved", "APROBADO_CON_EXCEPCION"), ("exception", "APROBADO")):
            runtime,repo,ctx,request=fixture(stage=stage)
            try:
                vbp=repo.get_object("candidate","MSN-SIM:GATE_2_VBP")
                original=vbp_export.export_canonical_vbp_bytes(vbp,repository=repo)
                self.assertTrue(original[0],original[3])
                before=list(repo._conn.iterdump())
                bad=copy.deepcopy(vbp);bad["approval_status"]=label
                self.assertEqual(runtime_contracts.compute_vbp_manifest_fingerprint(bad),vbp["fingerprint"])
                result=vbp_export.export_canonical_vbp_bytes(bad,repository=repo)
                self.assertFalse(result[0]);self.assertIsNone(result[1])
                self.assertEqual(list(repo._conn.iterdump()),before)
                self.assertEqual(vbp_export.export_canonical_vbp_bytes(vbp,repository=repo)[1],original[1])
            finally: repo.close()
    def test_fake_reference_rehashed_content_and_lost_original(self):
        from test_human_approvals import fixture
        runtime,repo,ctx,request=fixture(stage="approved")
        self.addCleanup(repo.close)
        vbp=repo.get_object("candidate","MSN-SIM:GATE_2_VBP")
        for field,value in (("human_approval_ref","APP-INVENTADA"),("title","Alterado")):
            bad=copy.deepcopy(vbp);bad[field]=value
            bad["fingerprint"]=runtime_contracts.compute_vbp_manifest_fingerprint(bad)
            ok,raw,_,_=vbp_export.export_canonical_vbp_bytes(bad,repository=repo,mission_status="FINALIZADA")
            self.assertFalse(ok);self.assertIsNone(raw)
        self.assertFalse(vbp_export.export_canonical_vbp_bytes(vbp)[0])
        eid=repo.get_mission("MSN-SIM")["evidence_ids"][0];repo.put_object("evidence_original",eid,{})
        result=vbp_export.export_canonical_vbp_bytes(vbp,repository=repo)
        self.assertFalse(result[0]);self.assertIn("EVIDENCIA_NO_DISPONIBLE",result[3])

if __name__ == "__main__":
    unittest.main()
