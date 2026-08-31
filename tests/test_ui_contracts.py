"""Pruebas exhaustivas para la Interfaz de Mision, Trabajo y Decisiones (PZ-013B, PZ-013C & PZ-UI-014A).

Valida entrega de recursos estáticos (HTML/CSS/JS/i18n), estructura semántica y accesible,
protección contra inyecciones XSS en el frontend, visualización y descarga de VBP (PZ-013C),
seguimiento visual de los 5 roles especialistas autorizados y cumplimiento del lenguaje visual
del Centro de Gestión y Memoria de OminAI (PZ-UI-014A).
"""

import re
import unittest
from pathlib import Path

import app.http_api as http_api


class TestUIContracts(unittest.TestCase):
    """Suite de pruebas para PZ-013B, PZ-013C y PZ-UI-014A (UI Contracts)."""

    def setUp(self) -> None:
        self.router = http_api.LocalAPIRouter()

    def test_ac01_static_assets_serving(self) -> None:
        """AC-01: GET / devuelve HTML, GET /styles.css devuelve CSS, GET /app.js y /i18n.js devuelven JS."""
        # 1. HTML principal
        code_html, h_html, body_html = self.router.dispatch("GET", "/", {"Host": "localhost:8000"})
        self.assertEqual(code_html, 200)
        self.assertIn("text/html", h_html["Content-Type"])
        content_html = body_html.decode("utf-8")
        self.assertIn('<html lang="es">', content_html)
        self.assertIn("OminAI HQ", content_html)

        # 2. CSS
        code_css, h_css, body_css = self.router.dispatch("GET", "/styles.css", {"Host": "localhost:8000"})
        self.assertEqual(code_css, 200)
        self.assertIn("text/css", h_css["Content-Type"])

        # 3. JS app
        code_js, h_js, body_js = self.router.dispatch("GET", "/app.js", {"Host": "localhost:8000"})
        self.assertEqual(code_js, 200)
        self.assertIn("application/javascript", h_js["Content-Type"])
        self.assertIn("function escapeHTML", body_js.decode("utf-8"))

        # 4. JS i18n
        code_i18n, h_i18n, body_i18n = self.router.dispatch("GET", "/i18n.js", {"Host": "localhost:8000"})
        self.assertEqual(code_i18n, 200)
        self.assertIn("application/javascript", h_i18n["Content-Type"])
        self.assertIn("OminaiI18N", body_i18n.decode("utf-8"))

    def test_ac02_accessibility_and_semantic_structure(self) -> None:
        """AC-02: El HTML contiene encabezados, atributos aria y botones con tipo explicito."""
        _, _, body_html = self.router.dispatch("GET", "/", {"Host": "localhost:8000"})
        content = body_html.decode("utf-8")

        # Verificar etiquetas aria y encabezados
        self.assertIn('aria-labelledby="op-heading"', content)
        self.assertIn('aria-labelledby="intake-heading"', content)
        self.assertIn('aria-labelledby="gate1-heading"', content)
        self.assertIn('aria-labelledby="exec-heading"', content)
        self.assertIn('aria-labelledby="ev-heading"', content)
        self.assertIn('aria-labelledby="gate2-heading"', content)
        self.assertIn('aria-labelledby="vbp-view-heading"', content)
        self.assertIn('aria-labelledby="audit-heading"', content)

        # Verificar botones con type explícito
        self.assertIn('type="submit"', content)
        self.assertIn('type="button"', content)

    def test_ac03_xss_protection_in_js_helper(self) -> None:
        """AC-03: El modulo app.js incluye logica probada de neutralizacion de caracteres XSS."""
        _, _, body_js = self.router.dispatch("GET", "/app.js", {"Host": "localhost:8000"})
        js_code = body_js.decode("utf-8")

        # La funcion escapeHTML reemplaza los caracteres peligrosos
        self.assertIn(".replace(/&/g, '&amp;')", js_code)
        self.assertIn(".replace(/</g, '&lt;')", js_code)
        self.assertIn(".replace(/>/g, '&gt;')", js_code)
        self.assertIn(".replace(/\"/g, '&quot;')", js_code)

    def test_ac04_ui_displays_all_five_specialist_roles(self) -> None:
        """AC-04: La interfaz incluye el seguimiento visual de los 5 roles autorizados."""
        _, _, body_html = self.router.dispatch("GET", "/", {"Host": "localhost:8000"})
        content = body_html.decode("utf-8")

        roles = [
            "Chief of Staff",
            "Research Analyst",
            "Product Architect",
            "Delivery Planner",
            "Governance Risk",
        ]
        for r in roles:
            self.assertIn(r, content)

    def test_ac05_vbp_section_and_download_button(self) -> None:
        """AC-05: La interfaz incluye seccion de visualizacion de VBP y boton de descarga (PZ-013C)."""
        _, _, body_html = self.router.dispatch("GET", "/", {"Host": "localhost:8000"})
        content = body_html.decode("utf-8")

        self.assertIn('id="vbp-view-section"', content)
        self.assertIn('id="vbp-markdown-preview"', content)
        self.assertIn('id="btn-download-vbp"', content)
        self.assertIn('id="btn-lang-toggle"', content)
        self.assertIn('data-i18n="badge_simulated"', content)

    def test_ac06_visual_brand_tokens_and_layout(self) -> None:
        """AC-06: Verificación de los tokens de marca oficiales, franja cuatricolor y sidebar (PZ-UI-014A)."""
        _, _, body_css = self.router.dispatch("GET", "/styles.css", {"Host": "localhost:8000"})
        css_text = body_css.decode("utf-8")

        # Tokens de color exactos
        self.assertIn("#8E44AD", css_text.upper())  # Morado
        self.assertIn("#3498DB", css_text.upper())  # Azul
        self.assertIn("#16A085", css_text.upper())  # Cian
        self.assertIn("#F1C40F", css_text.upper())  # Amarillo
        self.assertIn("#E67E22", css_text.upper())  # Naranja
        self.assertIn("#000000", css_text.upper())  # Negro
        self.assertIn("#FFFFFF", css_text.upper())  # Blanco

        # Tipografía Roboto y accesibilidad 44px
        self.assertIn("Roboto", css_text)
        self.assertIn("44px", css_text)

        # Verificar HTML con sidebar y accent-rule
        _, _, body_html = self.router.dispatch("GET", "/", {"Host": "localhost:8000"})
        html_text = body_html.decode("utf-8")
        self.assertIn('class="accent-rule"', html_text)
        self.assertIn('class="side-panel"', html_text)
        self.assertIn('class="side-nav"', html_text)


if __name__ == "__main__":
    unittest.main()
