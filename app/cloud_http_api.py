"""Cloud Run HTTP adapter with explicit host/origin policy and signed IAP identity."""

import http.server
import os
import re
import secrets
import threading
from pathlib import Path
from typing import Callable, Dict, Mapping, Optional, Tuple

from google.auth.transport.requests import Request
from google.oauth2 import id_token

from app import __version__
import app.api_contracts as api_contracts
import app.hq_runtime as hq_runtime
import app.http_api as http_api
from app.human_approvals import LocalHumanContext

IAP_CERTS_URL = "https://www.gstatic.com/iap/verify/public_key"
IAP_ISSUER = "https://cloud.google.com/iap"
DEFAULT_CLOUD_PORT = 8080
_EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def _verify_signed_iap_token(assertion: str, audience: str) -> Mapping[str, object]:
    """Verify the IAP signature and temporal/audience claims with Google's keys."""
    return id_token.verify_token(
        assertion,
        Request(),
        audience=audience,
        certs_url=IAP_CERTS_URL,
    )


def extract_google_identity(
    headers: Dict[str, str],
    audience: Optional[str],
    verifier: Optional[Callable[[str, str], Mapping[str, object]]] = None,
) -> Tuple[bool, Optional[str], Optional[str], Optional[str]]:
    """Authenticate one request exclusively from its signed IAP assertion."""
    hdrs = {k.lower(): v for k, v in headers.items()}
    assertion = hdrs.get("x-goog-iap-jwt-assertion")
    if not isinstance(audience, str) or not audience.strip():
        return False, None, None, "Configuracion IAP incompleta: falta audiencia explicita."
    if not isinstance(assertion, str) or not assertion.strip():
        return False, None, None, "Ausencia de X-Goog-IAP-JWT-Assertion firmado."
    try:
        claims = (verifier or _verify_signed_iap_token)(assertion, audience)
    except Exception:
        return False, None, None, "JWT IAP invalido o no verificable."
    issuer = claims.get("iss")
    claim_audience = claims.get("aud")
    subject = claims.get("sub")
    email = claims.get("email")
    if issuer != IAP_ISSUER:
        return False, None, None, "JWT IAP con emisor invalido."
    if claim_audience != audience:
        return False, None, None, "JWT IAP con audiencia invalida."
    if not isinstance(subject, str) or not subject.strip():
        return False, None, None, "JWT IAP sin sujeto valido."
    if not isinstance(email, str) or not _EMAIL_RE.fullmatch(email):
        return False, None, None, "JWT IAP sin correo valido."
    return True, email, subject, None


def _configured_values(environment_name: str) -> set[str]:
    raw = os.environ.get(environment_name, "")
    return {value.strip() for value in raw.split(",") if value.strip()}


class CloudAPIRouter(http_api.LocalAPIRouter):
    """Cloud adapter; every non-health request gets an isolated verified identity."""

    def __init__(
        self,
        runtime: Optional[hq_runtime.HQRuntime] = None,
        web_dir: Optional[Path] = None,
        *,
        iap_audience: Optional[str] = None,
        allowed_hosts: Optional[set[str]] = None,
        allowed_origins: Optional[set[str]] = None,
        operator_subject: Optional[str] = None,
        operator_email: Optional[str] = None,
        token_verifier: Optional[Callable[[str, str], Mapping[str, object]]] = None,
        listen_port: int = DEFAULT_CLOUD_PORT,
    ) -> None:
        cloud_origins = set(allowed_origins or ())
        super().__init__(
            runtime=runtime,
            web_dir=web_dir,
            listen_port=listen_port,
            allowed_origins=cloud_origins,
        )
        self.iap_audience = iap_audience
        self.allowed_hosts = set(allowed_hosts or ())
        self.operator_subject = operator_subject
        self.operator_email = operator_email
        self.token_verifier = token_verifier
        self._identity_lock = threading.RLock()

    def _operator_is_configured(self) -> bool:
        return (
            isinstance(self.operator_subject, str)
            and bool(self.operator_subject)
            and isinstance(self.operator_email, str)
            and bool(_EMAIL_RE.fullmatch(self.operator_email))
        )

    def dispatch(self, method, path, headers, body_bytes=b""):
        ok, error = api_contracts.validate_cloud_request_security(
            headers, self.allowed_hosts, self.allowed_origins
        )
        if not ok:
            return self.response(403, error=error)
        ok, error = api_contracts.validate_request_body_size(body_bytes)
        if not ok:
            return self.response(413, error=error)
        normalized = {k.lower(): v for k, v in headers.items()}
        if method == "GET" and path == "/health":
            return self.response(
                200,
                {"status": "UP", "mode": "DEMO_SIMULADA", "version": __version__, "port": self.listen_port},
            )
        if not self._operator_is_configured():
            return self.response(403, error="PERMISSION_DENIED: Operador A0 cloud no configurado.")
        ok, email, subject, error = extract_google_identity(
            normalized, self.iap_audience, self.token_verifier
        )
        if not ok:
            return self.response(401, error="PERMISSION_DENIED: " + str(error))
        if not (
            secrets.compare_digest(subject, self.operator_subject)
            and secrets.compare_digest(email, self.operator_email)
        ):
            return self.response(403, error="PERMISSION_DENIED: Identidad IAP distinta del operador A0 configurado.")
        if method in ("POST", "DELETE", "PUT", "PATCH") and (
            normalized.get("origin") not in self.allowed_origins
            or not secrets.compare_digest(normalized.get("x-ominai-csrf", ""), self.csrf_token)
        ):
            return self.response(403, error="PERMISSION_DENIED: Proteccion CSRF requerida.")
        return self._dispatch_with_identity(method, path, normalized, body_bytes, email, subject)

    def _dispatch_with_identity(self, method, path, headers, body_bytes, email, subject):
        """Scope the approval capability to this request and restore it before return."""
        approvals = self.runtime.approvals
        with self._identity_lock:
            previous_context = approvals.local_context
            try:
                profile = self.runtime.repository.get_profile(subject)
                if (
                    profile is None
                    or profile.get("user_id") != self.operator_subject
                    or profile.get("email") != self.operator_email
                    or profile.get("actor_role") != "usuario_humano"
                ):
                    return self.response(403, error="PERMISSION_DENIED: Perfil A0 preexistente no coincide.")
                request_context = LocalHumanContext(subject)
                approvals.local_context = request_context
                return self._dispatch_validated(method, path, headers, body_bytes, request_context)
            except Exception:
                return self.response(500, error="SYSTEM_ERROR: No se pudo verificar el perfil A0.")
            finally:
                approvals.local_context = previous_context


def create_cloud_server(
    host: str = "0.0.0.0",
    port: int = DEFAULT_CLOUD_PORT,
    router: Optional[CloudAPIRouter] = None,
):
    """Create the Cloud Run listener without inventing security configuration."""
    if host not in ("0.0.0.0", "127.0.0.1", "localhost"):
        raise ValueError("Direccion de escucha cloud no autorizada.")
    if type(port) is not int or not 0 <= port <= 65535:
        raise ValueError("Puerto cloud invalido.")
    if router is None:
        raise ValueError("Configure explicitamente el router cloud.")
    handler = type("IsolatedCloudHandler", (http_api.OminAIHTTPRequestHandler,), {"router": router})
    server = http.server.ThreadingHTTPServer((host, port), handler)
    router.listen_port = server.server_port
    return server


def run_cloud_server(override_port: Optional[int] = None, block: bool = True):
    raw_port = str(override_port) if override_port is not None else os.environ.get("PORT", str(DEFAULT_CLOUD_PORT))
    if not raw_port.isdigit() or not 1 <= int(raw_port) <= 65535:
        raise ValueError("PORT debe ser un entero entre 1 y 65535.")
    router = CloudAPIRouter(
        iap_audience=os.environ.get("OMINAI_IAP_AUDIENCE"),
        allowed_hosts=_configured_values("OMINAI_CLOUD_ALLOWED_HOSTS"),
        allowed_origins=_configured_values("OMINAI_CLOUD_ALLOWED_ORIGINS"),
        operator_subject=os.environ.get("OMINAI_A0_SUBJECT"),
        operator_email=os.environ.get("OMINAI_A0_EMAIL"),
        listen_port=int(raw_port),
    )
    server = create_cloud_server("0.0.0.0", int(raw_port), router=router)
    if block:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
    return server


if __name__ == "__main__":
    run_cloud_server()
