
"""OminAI HQ - Adaptador HTTP de Despliegue Cloud Run (PZ-014A, H12).

Implementa el entorno de escucha en 0.0.0.0:$PORT (por defecto 8080),
extraccion y validacion de identidad de operador via encabezados Google IAP
(X-Goog-Authenticated-User-Email, X-Goog-Authenticated-User-Id), y
adaptacion de rutas y seguridad.
"""

import http.server
import json
import os
import socket
from pathlib import Path
from typing import Dict, Optional, Tuple

import app.api_contracts as api_contracts
import app.hq_runtime as hq_runtime
import app.http_api as http_api


def extract_google_identity(headers: Dict[str, str]) -> Tuple[bool, Optional[str], Optional[str], Optional[str]]:
    """Extrae el email e identificador del operador desde encabezados Google IAP."""
    hdrs = {k.lower(): v for k, v in headers.items()}
    raw_email = hdrs.get("x-goog-authenticated-user-email")
    raw_id = hdrs.get("x-goog-authenticated-user-id")

    if not raw_email and not raw_id:
        return False, None, None, "Ausencia de encabezados de autenticacion Google IAP."

    email = raw_email.split(":")[-1] if raw_email else ""
    user_id = raw_id.split(":")[-1] if raw_id else email

    if not email or "@" not in email:
        return False, None, None, "Formato de email de operador invalido."

    return True, email, user_id, None


class CloudAPIRouter(http_api.LocalAPIRouter):
    """Router adaptado para Cloud Run con validacion de identidad de operador."""

    def __init__(
        self,
        runtime: Optional[hq_runtime.HQRuntime] = None,
        web_dir: Optional[Path] = None,
        require_iap_auth: bool = False,
    ) -> None:
        super().__init__(runtime=runtime, web_dir=web_dir)
        self.require_iap_auth = require_iap_auth


def create_cloud_server(host: str = "0.0.0.0", port: int = 8080, router: Optional[CloudAPIRouter] = None):
    """Crea la instancia de servidor HTTP para Cloud Run."""
    active_router = router or CloudAPIRouter()

    class CloudHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

        def do_GET(self):
            code, hdrs, payload = active_router.dispatch("GET", self.path, self.headers)
            self.send_response(code)
            for k, v in hdrs.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(payload)

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length > 0 else b""
            code, hdrs, payload = active_router.dispatch("POST", self.path, self.headers, body)
            self.send_response(code)
            for k, v in hdrs.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(payload)

    return http.server.ThreadingHTTPServer((host, port), CloudHandler)


def run_cloud_server(override_port: Optional[int] = None, block: bool = True):
    port = override_port or int(os.environ.get("PORT", "8080"))
    server = create_cloud_server("0.0.0.0", port)
    if block:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.server_close()
    return server


if __name__ == "__main__":
    run_cloud_server()
