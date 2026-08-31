"""Pruebas de Entrega e Integración de la Interfaz Local de OminAI HQ (PZ-UI-014A).

Valida la entrega de la interfaz con el lenguaje visual de marca, la disponibilidad
de los activos estáticos y los 8 bloques funcionales de la oficina digital agéntica.
"""

import unittest
from pathlib import Path

import app.http_api as http_api


class TestMVPInterfaceDelivery(unittest.TestCase):
    """Pruebas de entrega de interfaz de usuario de OminAI HQ."""

    def setUp(self) -> None:
        self.router = http_api.LocalAPIRouter()
        self.base_dir = Path(__file__).resolve().parent.parent

    def test_ac01_brand_assets_exist(self) -> None:
        """Verifica que los activos de marca oficiales estén presentes en el directorio web/assets/brand/."""
        logo_path = self.base_dir / "web" / "assets" / "brand" / "ominai-logo.png"
        emblem_path = self.base_dir / "web" / "assets" / "brand" / "ominai-emblem.png"

        self.assertTrue(logo_path.exists(), f"El archivo {logo_path} debe existir.")
        self.assertTrue(logo_path.stat().st_size > 0, "El logo no debe estar vacío.")
        self.assertTrue(emblem_path.exists(), f"El archivo {emblem_path} debe existir.")
        self.assertTrue(emblem_path.stat().st_size > 0, "El emblema no debe estar vacío.")

    def test_ac02_all_eight_management_sections_rendered(self) -> None:
        """Comprueba que los 8 bloques del Centro de Gestión estén definidos con IDs estables."""
        _, _, body_html = self.router.dispatch("GET", "/", {"Host": "localhost:8000"})
        content = body_html.decode("utf-8")

        sections = [
            "operator-section",
            "intake-section",
            "gate1-section",
            "execution-section",
            "evidence-memory-section",
            "gate2-section",
            "vbp-view-section",
            "audit-section",
        ]
        for sec in sections:
            self.assertIn(f'id="{sec}"', content, f"La sección {sec} debe estar presente en el HTML.")

    def test_ac03_human_approval_controls_preserved(self) -> None:
        """Comprueba que los botones de decisión humana mantengan sus identificadores requeridos."""
        _, _, body_html = self.router.dispatch("GET", "/", {"Host": "localhost:8000"})
        content = body_html.decode("utf-8")

        control_ids = [
            "btn-submit-mission",
            "btn-approve-plan",
            "btn-reject-plan",
            "btn-pause-mission",
            "btn-resume-mission",
            "btn-cancel-mission",
            "btn-execute-step",
            "btn-memory-propose",
            "btn-memory-approve",
            "btn-memory-update",
            "btn-memory-delete",
            "btn-approve-vbp",
            "btn-reject-vbp",
            "btn-approve-exception",
            "btn-download-vbp",
            "btn-refresh-audit",
            "btn-lang-toggle",
        ]
        for cid in control_ids:
            self.assertIn(f'id="{cid}"', content, f"El control {cid} debe estar presente.")

    def test_ac04_bilingual_dictionary_coverage(self) -> None:
        """Verifica que el archivo i18n.js defina los diccionarios es y en con claves completas."""
        _, _, body_js = self.router.dispatch("GET", "/i18n.js", {"Host": "localhost:8000"})
        js_code = body_js.decode("utf-8")

        required_keys = [
            "app_title",
            "badge_simulated",
            "section_operator",
            "section_intake",
            "section_gate1",
            "section_specialists",
            "section_evidence_memory",
            "section_gate2",
            "section_vbp",
            "section_audit",
            "nav_title",
            "nav_operator",
            "nav_intake",
            "nav_gate1",
            "nav_execution",
            "nav_evidence",
            "nav_gate2",
            "nav_export",
            "nav_audit",
        ]
        for key in required_keys:
            self.assertIn(key, js_code, f"La clave de traducción {key} debe estar presente en i18n.js.")


if __name__ == "__main__":
    unittest.main()
