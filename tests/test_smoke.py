"""Pruebas basicas (smoke tests) para la estructura minima ejecutable."""

import io
import json
import unittest
from contextlib import redirect_stdout

import app
import app.__main__


class TestSmoke(unittest.TestCase):
    """Verifica la importacion, version y ejecucion minima del paquete."""

    def test_app_imports_cleanly(self) -> None:
        """Verifica que el paquete se importa y expone sus metadatos sin efectos."""
        self.assertEqual(app.__application__, "OminAI HQ")
        self.assertEqual(app.__version__, "0.1.0")

    def test_main_execution_output(self) -> None:
        """Verifica que main() devuelve codigo 0 y JSON con la estructura esperada."""
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = app.__main__.main()

        self.assertEqual(exit_code, 0)
        output = buffer.getvalue().strip()
        data = json.loads(output)

        self.assertEqual(data.get("application"), "OminAI HQ")
        self.assertEqual(data.get("status"), "STRUCTURE_READY")
        self.assertEqual(data.get("implemented_capabilities"), [])
        self.assertIsInstance(data.get("implemented_capabilities"), list)
        self.assertEqual(len(data.get("implemented_capabilities")), 0)


if __name__ == "__main__":
    unittest.main()
