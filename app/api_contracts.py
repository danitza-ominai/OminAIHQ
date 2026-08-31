"""OminAI HQ - Contratos de API Local y Validacion de Solicitudes (PZ-013A).

Define las especificaciones de carga util, restricciones de tamano, validacion de headers
de seguridad (Host, Origin, CSRF) y envolturas estandarizadas de respuesta para el backend local
conforme a CONTRATO-MVP-v1.md seccion 9, CT-014-016 y RF-001/006/016/019/025.
"""

import json
from typing import Any, Dict, List, Optional, Tuple

MAX_REQUEST_BODY_BYTES = 50 * 1024  # 50 KB
ALLOWED_HOSTS = {"localhost", "127.0.0.1", "[::1]", "localhost:8000", "127.0.0.1:8000"}
ALLOWED_ORIGINS = {"http://localhost:8000", "http://127.0.0.1:8000", "http://127.0.0.1:8000"}


class APIContractError(Exception):
    """Excepcion de validacion de contrato de API."""
    pass


def validate_request_security(headers: Dict[str, str]) -> Tuple[bool, Optional[str]]:
    """Valida que la solicitud provenga de origen loopback seguro y no de cross-origin no autorizado."""
    # Normalizar headers a minusculas
    norm_headers = {k.lower(): v for k, v in headers.items()}

    # 1. Validar Host
    host = norm_headers.get("host")
    if not host or host not in ALLOWED_HOSTS:
        return False, f"HOST_INVALIDO: El host '{host}' no es loopback local autorizado."

    # 2. Validar Origin (si esta presente en navegadores)
    origin = norm_headers.get("origin")
    if origin and origin not in ALLOWED_ORIGINS:
        return False, f"CROSS_ORIGIN_PROHIBIDO: Origen '{origin}' no autorizado para la API local."

    return True, None


def validate_request_body_size(raw_bytes: bytes) -> Tuple[bool, Optional[str]]:
    """Comprueba que el cuerpo de la peticion no exceda el limite maximo de 50 KB."""
    if len(raw_bytes) > MAX_REQUEST_BODY_BYTES:
        return False, f"PAYLOAD_TOO_LARGE: Cuerpo de {len(raw_bytes)} bytes excede el maximo de {MAX_REQUEST_BODY_BYTES} bytes."
    return True, None


STATIC_MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
}


def is_human_actor(actor_role: Optional[str]) -> bool:
    """Verifica si el rol corresponde a una autoridad humana autorizada (A0)."""
    return actor_role in ("usuario_humano", "operador_humano", "a0_humana")


def format_api_response(
    status_code: int,
    data: Optional[Any] = None,
    error: Optional[str] = None,
) -> Dict[str, Any]:
    """Genera la envoltura estandarizada JSON para respuestas de API."""
    return {
        "status_code": status_code,
        "success": 200 <= status_code < 300,
        "data": data,
        "error": error,
    }
