"""Security regression tests for the Cloud Run HTTP adapter (PZ-016A)."""

import base64
import json
import time
import unittest

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from google.auth import crypt, jwt

import app.cloud_http_api as cloud_http_api
from app import hq_runtime, local_repository
from test_human_approvals import fixture


class TestCloudHTTPApi(unittest.TestCase):
    audience = "/projects/123456789/global/backendServices/987654321"
    host = "hq.example.run.app"
    origin = "https://hq.example.run.app"

    @classmethod
    def setUpClass(cls):
        key = ec.generate_private_key(ec.SECP256R1())
        private_pem = key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
        cls.public_pem = key.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        cls.signer = crypt.ES256Signer.from_string(private_pem, key_id="test-key")

    def setUp(self):
        self.runtime,self.repo,self.ctx,self.req=fixture()
        ok,error=self.repo.save_profile({
            "user_id":"USR-SIM",
            "display_name":"SIMULADA",
            "email":"niko@ominai.ai",
            "actor_role":"usuario_humano",
        })
        self.assertTrue(ok,error)
        self.router=cloud_http_api.CloudAPIRouter(
            runtime=self.runtime,
            iap_audience=self.audience,
            allowed_hosts={self.host},
            allowed_origins={self.origin},
            operator_subject="USR-SIM",
            operator_email="niko@ominai.ai",
            token_verifier=self.verify_test_token,
        )
        self.base="/api/v1/missions/MSN-SIM"

    def tearDown(self):
        self.repo.close()

    def verify_test_token(self, token, audience):
        return jwt.decode(token, certs={"test-key":self.public_pem}, audience=audience)

    def token(self, **overrides):
        now=int(time.time())
        claims={
            "iss":cloud_http_api.IAP_ISSUER,
            "aud":self.audience,
            "sub":"USR-SIM",
            "email":"niko@ominai.ai",
            "iat":now-1,
            "exp":now+300,
        }
        claims.update(overrides)
        return jwt.encode(self.signer,claims).decode("ascii")

    def headers(self, token=None, origin=None):
        values={"Host":self.host,"X-Goog-IAP-JWT-Assertion":token or self.token()}
        if origin is not None:
            values["Origin"]=origin
        return values

    def test_signed_iap_identity_success_and_legacy_headers_have_no_authority(self):
        token=self.token()
        encoded_header=token.split(".")[0]
        encoded_header += "=" * (-len(encoded_header) % 4)
        self.assertEqual(json.loads(base64.urlsafe_b64decode(encoded_header))["alg"],"ES256")
        ok,email,subject,error=cloud_http_api.extract_google_identity(
            self.headers(token),self.audience,self.verify_test_token
        )
        self.assertTrue(ok,error)
        self.assertEqual(email,"niko@ominai.ai")
        self.assertEqual(subject,"USR-SIM")
        legacy={
            "Host":self.host,
            "X-Goog-Authenticated-User-Email":"accounts.google.com:attacker@example.test",
            "X-Goog-Authenticated-User-Id":"accounts.google.com:attacker",
        }
        before=list(self.repo._conn.iterdump())
        self.assertEqual(self.router.dispatch("GET","/api/v1/profile",legacy)[0],401)
        self.assertEqual(list(self.repo._conn.iterdump()),before)

    def test_missing_forged_expired_and_wrong_audience_jwts_have_no_effect(self):
        valid=self.token()
        head,payload,signature=valid.split(".")
        pivot=len(signature)//2
        forged=".".join((head,payload,signature[:pivot]+("A" if signature[pivot] != "A" else "B")+signature[pivot+1:]))
        cases=(
            {"Host":self.host},
            self.headers(forged),
            self.headers(self.token(exp=int(time.time())-1)),
            self.headers(self.token(aud="wrong-audience")),
        )
        before=list(self.repo._conn.iterdump())
        for headers in cases:
            response=self.router.dispatch("POST",self.base+"/decisions",headers,b"{}")
            self.assertEqual(response[0],401,response[2])
            self.assertEqual(list(self.repo._conn.iterdump()),before)

    def test_issuer_subject_and_email_claims_are_required(self):
        for claims in (
            {"iss":"https://issuer.invalid"},
            {"sub":""},
            {"email":"not-an-email"},
        ):
            self.assertFalse(cloud_http_api.extract_google_identity(
                self.headers(self.token(**claims)),self.audience,self.verify_test_token
            )[0])

    def test_cloud_host_origin_and_configuration_fail_closed_without_effect(self):
        before=list(self.repo._conn.iterdump())
        for headers in (
            {**self.headers(),"Host":"arbitrary.run.app"},
            self.headers(origin="https://evil.example"),
        ):
            self.assertEqual(self.router.dispatch("POST",self.base+"/decisions",headers,b"{}")[0],403)
            self.assertEqual(list(self.repo._conn.iterdump()),before)
        unconfigured=cloud_http_api.CloudAPIRouter(runtime=self.runtime,token_verifier=self.verify_test_token)
        self.assertEqual(unconfigured.dispatch("GET","/health",{"Host":self.host})[0],403)
        missing_audience=cloud_http_api.CloudAPIRouter(
            runtime=self.runtime,allowed_hosts={self.host},
            operator_subject="USR-SIM",operator_email="niko@ominai.ai",
            token_verifier=self.verify_test_token
        )
        self.assertEqual(missing_audience.dispatch("GET","/api/v1/profile",self.headers())[0],401)
        self.assertEqual(list(self.repo._conn.iterdump()),before)

    def test_authenticated_identity_must_match_explicit_operator_without_effects(self):
        before=list(self.repo._conn.iterdump())
        for token in (
            self.token(sub="OTHER"),
            self.token(email="other@example.test"),
        ):
            self.assertEqual(self.router.dispatch("GET","/api/v1/profile",self.headers(token))[0],403)
            self.assertEqual(list(self.repo._conn.iterdump()),before)
        no_operator=cloud_http_api.CloudAPIRouter(
            runtime=self.runtime,iap_audience=self.audience,allowed_hosts={self.host},
            allowed_origins={self.origin},token_verifier=self.verify_test_token,
        )
        self.assertEqual(no_operator.dispatch("GET","/api/v1/profile",self.headers())[0],403)
        self.assertEqual(list(self.repo._conn.iterdump()),before)

    def test_origin_and_csrf_remain_required_for_state_changes(self):
        before=list(self.repo._conn.iterdump())
        no_origin={**self.headers(),"X-Ominai-CSRF":self.router.csrf_token,"Content-Type":"application/json"}
        self.assertEqual(self.router.dispatch("POST",self.base+"/decisions",no_origin,b"{}")[0],403)
        bad_csrf={**self.headers(origin=self.origin),"X-Ominai-CSRF":"wrong","Content-Type":"application/json"}
        self.assertEqual(self.router.dispatch("POST",self.base+"/decisions",bad_csrf,b"{}")[0],403)
        self.assertEqual(list(self.repo._conn.iterdump()),before)

    def test_empty_repository_valid_jwt_and_wrong_csrf_creates_no_profile(self):
        repo=local_repository.LocalRepository(":memory:")
        runtime=hq_runtime.HQRuntime(repository=repo)
        router=cloud_http_api.CloudAPIRouter(
            runtime=runtime,
            iap_audience=self.audience,
            allowed_hosts={self.host},
            allowed_origins={self.origin},
            operator_subject="USR-SIM",
            operator_email="niko@ominai.ai",
            token_verifier=self.verify_test_token,
        )
        headers={
            **self.headers(origin=self.origin),
            "X-Ominai-CSRF":"wrong",
            "Content-Type":"application/json",
        }
        before=list(repo._conn.iterdump())
        try:
            self.assertEqual(router.dispatch("POST","/api/v1/missions",headers,b"{}")[0],403)
            self.assertEqual(repo._conn.execute("SELECT COUNT(*) FROM profiles").fetchone()[0],0)
            self.assertEqual(list(repo._conn.iterdump()),before)
            headers["X-Ominai-CSRF"]=router.csrf_token
            self.assertEqual(router.dispatch("POST","/api/v1/missions",headers,b"{}")[0],403)
            self.assertEqual(repo._conn.execute("SELECT COUNT(*) FROM profiles").fetchone()[0],0)
            self.assertEqual(list(repo._conn.iterdump()),before)
        finally:
            repo.close()

    def test_valid_signed_identity_origin_and_csrf_allow_the_scoped_decision(self):
        headers={
            **self.headers(origin=self.origin),
            "X-Ominai-CSRF":self.router.csrf_token,
            "Content-Type":"application/json",
        }
        body=json.dumps({"approval_request":self.req,"decision":"APROBAR"}).encode()
        code,_,response=self.router.dispatch("POST",self.base+"/decisions",headers,body)
        self.assertEqual(code,200,response)
        self.assertEqual(self.repo.get_mission("MSN-SIM")["status"],"AUTORIZADA_PARA_EJECUTAR")

    def test_request_identity_is_restored_and_not_contaminated(self):
        original_context=self.runtime.approvals.local_context
        headers={
            **self.headers(),
            "X-Goog-Authenticated-User-Email":"accounts.google.com:other@example.test",
            "X-Goog-Authenticated-User-Id":"accounts.google.com:other",
        }
        code,_,body=self.router.dispatch("GET","/api/v1/profile",headers)
        self.assertEqual(code,200,body)
        self.assertEqual(json.loads(body)["data"]["user_id"],"USR-SIM")
        self.assertIs(self.runtime.approvals.local_context,original_context)
        other=self.headers(self.token(sub="OTHER",email="other@example.test"))
        self.assertEqual(self.router.dispatch("GET","/api/v1/profile",other)[0],403)
        self.assertIs(self.runtime.approvals.local_context,original_context)

    def test_health_is_effect_free_and_reports_actual_bound_port(self):
        before=list(self.repo._conn.iterdump())
        server=cloud_http_api.create_cloud_server("localhost",0,router=self.router)
        try:
            code,_,body=self.router.dispatch("GET","/health",{"Host":self.host})
            self.assertEqual(code,200)
            health=json.loads(body)["data"]
            self.assertEqual(health["port"],server.server_port)
            self.assertEqual(health["mode"],"DEMO_SIMULADA")
            self.assertEqual(list(self.repo._conn.iterdump()),before)
        finally:
            server.server_close()


if __name__ == "__main__":
    unittest.main()
