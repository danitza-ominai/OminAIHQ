
"""Pruebas exhaustivas para el Adaptador de Cloud Storage (PZ-014A, H12)."""
import unittest

import app.cloud_storage as cloud_storage


class TestCloudStorage(unittest.TestCase):
    def setUp(self):
        self.storage = cloud_storage.CloudStorageAdapter(bucket_name="test-bucket")

    def test_save_and_get_blob_success(self):
        raw_data = b"Expediente Saneado de Competencia OminAI HQ"
        ok, uri, err = self.storage.save_blob("dossiers/MSN-01/manifest.json", raw_data)
        self.assertTrue(ok)
        self.assertEqual(uri, "gs://test-bucket/dossiers/MSN-01/manifest.json")

        ok_g, content, err_g = self.storage.get_blob("dossiers/MSN-01/manifest.json")
        self.assertTrue(ok_g)
        self.assertEqual(content, raw_data)


    def test_path_traversal_rejected(self):
        ok, uri, err = self.storage.save_blob("../secrets/keys.txt", b"secrets")
        self.assertFalse(ok)
        self.assertIn("path traversal", err)


if __name__ == "_main__":
    unittest.main()
