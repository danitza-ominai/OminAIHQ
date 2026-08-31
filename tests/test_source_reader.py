
"""Pruebas exhaustivas para el lector de fuentes y prevencion de SSRF (PZ-005A, H06)."""
import unittest

import app.source_reader as source_reader


class TestSourceReader(unittest.TestCase):
    def test_empty_allowed_domains_denies_all_external_urls(self):
        reader = source_reader.SourceReader(allowed_domains=set())
        ok, err = reader.validate_locator("https://wikipedia.org/wiki/Test")
        self.assertFalse(ok)
        self.assertIn("no esta en la lista blanca", err)

    def test_ssrf_blocking_for_private_and_metadata_ips(self):
        reader = source_reader.SourceReader(allowed_domains={"wikipedia.org", "google.com", "example.com"})
        ssrf_targets = [
            "http://127.0.0.1/admin",
            "http://localhost:8080",
            "http://169.254.169.254/latest/meta-data",
            "http://metadata.google.internal/computeMetadata/v1",
            "http://10.0.0.1/secret",
            "http://192.168.1.1/config",
            "http://172.16.0.1/status",
            "http://[::1]/debug",
        ]
        for url in ssrf_targets:
            with self.subTest(url=url):
                ok, err = reader.validate_locator(url)
                self.assertFalse(ok)
                self.assertIn("bloqueado", err.lower())

    def test_byte_level_truncation(self):
        reader = source_reader.SourceReader(allowed_domains={"example.com"}, max_bytes=10)
        mock = {"https://example.com/data": "abcdefghijklmnopqrstuvwxyz"}
        ok, content, err = reader.read_source("https://example.com/data", mock_sources=mock)
        self.assertTrue(ok)
        self.assertEqual(len(content.encode("utf-8")), 10)
        self.assertEqual(content, "abcdefghij")

    def test_internal_doc_and_fixture_schemes_allowed(self):
        reader = source_reader.SourceReader(allowed_domains=set())
        ok, err = reader.validate_locator("doc://intake/document1")
        self.assertTrue(ok)
        self.assertIsNone(err)
        ok2, err2 = reader.validate_locator("fixture://demo/source1")
        self.assertTrue(ok2)
        self.assertIsNone(err2)


if __name__ == "_main__":
    unittest.main()
