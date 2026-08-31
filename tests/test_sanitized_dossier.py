"""Pruebas exhaustivas para el Expediente Saneado de Competencia (PZ-009C).

Valida separacion estricta entre original privado y copia publica, anonimizacion de rutas locales,
revocacion inmediata de autorizaciones y calculo de manifest con huella SHA-256.
"""

import unittest

import app.hq_runtime as hq_runtime
import app.sanitized_dossier as sanitized_dossier


class TestSanitizedDossier(unittest.TestCase):
    """Suite de pruebas para PZ-009C (Sanitized Dossier)."""

    def setUp(self) -> None:
        self.dossier = sanitized_dossier.SanitizedDossierManager()
        self.runtime = hq_runtime.HQRuntime(dossier_manager=self.dossier)

    def test_ac01_authorization_and_manifest_construction(self) -> None:
        """AC-01 & AC-03: Construccion del manifest publico con copias autorizadas y rutas anonimizadas."""
        # Autorizar 2 items en MSN-001 y 1 item en MSN-002
        self.dossier.authorize_item_for_dossier(
            mission_id="MSN-001",
            item_id="DOC-001",
            item_type="DOCUMENTO_TEXTO",
            public_filename="especificacion_publica.txt",
            sanitized_bytes=b"Texto saneado sin secretos",
            original_hash="sha256:orig_1111111111111111111111111111111111111111111111111111111111111111",
            description="Especificacion publica",
        )

        self.dossier.authorize_item_for_dossier(
            mission_id="MSN-001",
            item_id="IMG-001",
            item_type="IMAGEN_DIAGRAMA",
            public_filename="arquitectura_publica.png",
            sanitized_bytes=b"\x89PNG_saneado",
            original_hash="sha256:orig_2222222222222222222222222222222222222222222222222222222222222222",
            description="Diagrama de bloques saneado",
        )

        self.dossier.authorize_item_for_dossier(
            mission_id="MSN-002",
            item_id="DOC-002",
            item_type="DOCUMENTO_TEXTO",
            public_filename="especificacion_msn2.txt",
            sanitized_bytes=b"Texto MSN 2",
            original_hash="sha256:orig_3333333333333333333333333333333333333333333333333333333333333333",
            description="Especificacion MSN 2",
        )

        ok, manifest, err = self.dossier.build_public_dossier_manifest("MSN-001", "VBP Portal B2B")
        self.assertTrue(ok)
        self.assertEqual(manifest["total_items"], 2)
        self.assertTrue(manifest["dossier_fingerprint"].startswith("sha256:"))

        # Verificar que items de MSN-002 no aparecen en manifest de MSN-001
        self.assertFalse(any(it["item_id"] == "DOC-002" for it in manifest["items"]))

        # Verificar que no existen rutas absolutas locales privadas
        for it in manifest["items"]:
            self.assertNotIn("C:\\", it["public_filename"])
            self.assertNotIn("/home/", it["public_filename"])

    def test_ac04_revocation_excludes_item_from_future_dossiers(self) -> None:
        """AC-04: Revocar autorizacion de un item lo excluye inmediatamente del expediente publico."""
        self.dossier.authorize_item_for_dossier(
            mission_id="MSN-001",
            item_id="IMG-CONFIDENTIAL",
            item_type="IMAGEN",
            public_filename="captura_sensible.png",
            sanitized_bytes=b"bytes",
            original_hash="hash_orig",
        )

        # Antes de revocar
        ok1, man1, _ = self.dossier.build_public_dossier_manifest("MSN-001", "VBP Demo")
        self.assertEqual(man1["total_items"], 1)

        # Revocar
        revoked = self.dossier.revoke_item_authorization("IMG-CONFIDENTIAL", mission_id="MSN-001")
        self.assertTrue(revoked)

        # Despues de revocar -> expediente queda vacio
        ok2, man2, _ = self.dossier.build_public_dossier_manifest("MSN-001", "VBP Demo")
        self.assertEqual(man2["total_items"], 0)
        self.assertNotEqual(man1["dossier_fingerprint"], man2["dossier_fingerprint"])

    def test_ac05_runtime_integration(self) -> None:
        """AC-05: El SanitizedDossierManager se encuentra accesible en HQRuntime."""
        self.assertIsNotNone(self.runtime.dossier_manager)
        self.assertIsInstance(self.runtime.dossier_manager, sanitized_dossier.SanitizedDossierManager)


if __name__ == "__main__":
    unittest.main()
