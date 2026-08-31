
"""Pruebas exhaustivas para el Adaptador HTTP de Cloud Run (PZ-014A, H12)."""
import unittest

import app.cloud_http_api as cloud_http_api


class TestCloudHTTPApi(unittest.TestCase):
    def test_google_identity_extraction_success(self):
        headers = {
            "X-Goog-Authenticated-User-Email": "accounts.google.com:niko@ominai.ai",
            "X-Goog-Authenticated-User-Id": "accounts.google.com:109928234567",
        }
        ok, email, user_id, err = cloud_http_api.extract_google_identity(headers)
        self.assertTrue(ok)
        self.assertEqual(email, "niko@ominai.ai")
        self.assertEqual(user_id, "109928234567")
        self.assertIsNone(err)


    def test_google_identity_missing_or_invalid_email(self):
        ok_m, _, _, err_m = cloud_http_api.extract_google_identity({})
        self.assertFalse(ok_m)
        self.assertIn("Ausencia de encabezados", err_m)

        bad_hdrs = {"X-Goog-Authenticated-User-Email": "no_email_string"}
        ok_b, _, _, err_b = cloud_http_api.extract_google_identity(bad_hdrs)
        self.assertFalse(ok_b)
        self.assertIn("invalido", err_b)


    def test_cloud_server_instantiation_port_binding(self):
        router = cloud_http_api.CloudAPIRouter()
        server = cloud_http_api.create_cloud_server("localhost", 9991, router=router)
        self.assertEqual(server.server_port, 9991)
        server.server_close()


if __name__ == "__main__":
    unittest.main()
