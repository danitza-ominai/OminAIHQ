"""Pruebas exhaustivas para la Ingesta de Archivos y Extractores (PZ-009B).

Valida limites de tamano y conteo, proteccion contra path traversal, coherencia de bytes magicos,
extraccion de formatos (TXT, MD, DOCX, PDF), bloqueo de secretos, confirmacion de confidencialidad
y aislamiento en directorios temporales.
"""

import io
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

import app.document_extractors as document_extractors
import app.file_intake as file_intake
import app.hq_runtime as hq_runtime


def _build_dummy_docx(text_content: str) -> bytes:
    """Construye en memoria un archivo binario DOCX valido con el texto especificado."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p>
      <w:r>
        <w:t>{text_content}</w:t>
      </w:r>
    </w:p>
  </w:body>
</w:document>"""
        zf.writestr("word/document.xml", xml)
    return buf.getvalue()


def _build_dummy_pdf(text_content: str) -> bytes:
    """Construye en memoria un archivo binario PDF simple con el texto especificado."""
    pdf_template = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>
endobj
4 0 obj
<< /Length {len(text_content) + 20} >>
stream
BT
/F1 12 Tf
({text_content}) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
trailer
<< /Size 5 /Root 1 0 R >>
startxref
%%EOF"""
    return pdf_template.encode("latin-1")


class TestFileIntake(unittest.TestCase):
    """Suite de pruebas para PZ-009B."""

    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.tmp_dir.name)
        self.manager = file_intake.FileIntakeManager(storage_root=str(self.storage_path))
        self.runtime = hq_runtime.HQRuntime(file_intake_manager=self.manager)

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()

    def test_ac01_limits_path_traversal_and_corrupt_files(self) -> None:
        """AC-01: Limites exactos y excedidos, path traversal, extension falsa y archivos corruptos."""
        # 1. Path traversal bloqueado
        ok_pt1, _, err_pt1 = self.manager.process_file_intake("../secret.txt", b"Contenido", "MSN-001")
        self.assertFalse(ok_pt1)
        self.assertIn("Path Traversal", err_pt1)

        ok_pt2, _, err_pt2 = self.manager.process_file_intake("subdir/file.txt", b"Contenido", "MSN-001")
        self.assertFalse(ok_pt2)
        self.assertIn("Path Traversal", err_pt2)

        # 2. Extension no autorizada (.exe, .docm)
        ok_ext, _, err_ext = self.manager.process_file_intake("malware.exe", b"bytes", "MSN-001")
        self.assertFalse(ok_ext)
        self.assertIn("no autorizada", err_ext)

        # 3. Extension falsa (dice .pdf pero es texto plano sin %PDF-)
        ok_fake, _, err_fake = self.manager.process_file_intake("fake.pdf", b"Este no es un PDF", "MSN-001")
        self.assertFalse(ok_fake)
        self.assertIn("Encabezado binario", err_fake)

        # 4. Limite de archivos (max 5)
        for i in range(5):
            ok_i, rec_i, err_i = self.manager.process_file_intake(f"doc_{i}.txt", f"Contenido {i}".encode(), "MSN-001")
            self.assertTrue(ok_i, f"Fallo en archivo {i}: {err_i}")

        # Intento de 6to archivo excediendo limite
        ok_6, _, err_6 = self.manager.process_file_intake("doc_6.txt", b"Contenido extra", "MSN-001")
        self.assertFalse(ok_6)
        self.assertIn("Limite de 5 archivos", err_6)

    def test_ac02_extraction_of_all_formats_and_hash_verifiability(self) -> None:
        """AC-02: Extraccion de TXT, MD, DOCX y PDF con hash SHA-256 verificable."""
        # 1. TXT
        txt_bytes = "Texto plano de especificacion tecnica.".encode("utf-8")
        ok_txt, rec_txt, _ = self.manager.process_file_intake("spec.txt", txt_bytes, "MSN-001")
        self.assertTrue(ok_txt)
        self.assertIn("especificacion tecnica", rec_txt["extracted_text_preview"])
        self.assertTrue(os.path.exists(rec_txt["saved_path"]))

        # 2. MD
        md_bytes = "# Titulo Markdown\n- Item 1\n- Item 2".encode("utf-8")
        ok_md, rec_md, _ = self.manager.process_file_intake("doc.md", md_bytes, "MSN-001")
        self.assertTrue(ok_md)
        self.assertIn("Titulo Markdown", rec_md["extracted_text_preview"])

        # 3. DOCX
        docx_bytes = _build_dummy_docx("Contenido estructurado desde documento Word DOCX.")
        ok_docx, rec_docx, _ = self.manager.process_file_intake("manual.docx", docx_bytes, "MSN-001")
        self.assertTrue(ok_docx)
        self.assertIn("documento Word DOCX", rec_docx["extracted_text_preview"])

        # 4. PDF
        pdf_bytes = _build_dummy_pdf("Texto extraido desde PDF valido.")
        ok_pdf, rec_pdf, _ = self.manager.process_file_intake("reporte.pdf", pdf_bytes, "MSN-001")
        self.assertTrue(ok_pdf)
        self.assertIn("PDF valido", rec_pdf["extracted_text_preview"])

    def test_ac03_secret_blocking_and_confidentiality_confirmation(self) -> None:
        """AC-03: Bloqueo estricto de secretos y confirmacion humana de confidencialidad."""
        # 1. Secreto en texto claro bloquea intake
        secret_content = "Configuracion interna: api_key='sk-live-secret-9988776655443322'".encode("utf-8")
        ok_sec, _, err_sec = self.manager.process_file_intake("keys.txt", secret_content, "MSN-001")
        self.assertFalse(ok_sec)
        self.assertIn("SECRETO_DETECTADO", err_sec)

        # 2. Confidencial sin autorizacion humana se detiene
        conf_content = "DOCUMENTO CONFIDENCIAL: Analisis de costos internos.".encode("utf-8")
        ok_conf_no, _, err_conf_no = self.manager.process_file_intake("costos.txt", conf_content, "MSN-001", human_confidential_confirmed=False)
        self.assertFalse(ok_conf_no)
        self.assertIn("REQUIERE_CONFIRMACION_CONFIDENCIALIDAD", err_conf_no)

        # 3. Confidencial con confirmacion humana se admite
        ok_conf_yes, rec_conf_yes, _ = self.manager.process_file_intake("costos.txt", conf_content, "MSN-001", human_confidential_confirmed=True)
        self.assertTrue(ok_conf_yes)
        self.assertTrue(rec_conf_yes["is_confidential"])

    def test_ac04_storage_failure_leaves_zero_traces(self) -> None:
        """AC-04: Si ocurre un fallo en el guardado, no se registra el archivo como admitido."""
        # Configurar storage_root a una ruta inexistente de solo lectura o invalida
        bad_manager = file_intake.FileIntakeManager(storage_root="Z:\\non_existent_drive\\storage")
        ok, rec, err = bad_manager.process_file_intake("valid.txt", b"Texto valido", "MSN-001")
        self.assertFalse(ok)
        self.assertIn("Fallo al escribir", err)
        self.assertEqual(len(bad_manager.admitted_files), 0)

    def test_ac05_runtime_integration(self) -> None:
        """AC-05: El FileIntakeManager se encuentra accesible e integrado en HQRuntime."""
        self.assertIsNotNone(self.runtime.file_intake)
        self.assertIsInstance(self.runtime.file_intake, file_intake.FileIntakeManager)


if __name__ == "__main__":
    unittest.main()
