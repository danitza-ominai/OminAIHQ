"""OminAI HQ - Contratos de API Local y Validacion de Solicitudes (PZ-013A).

Define las especificaciones de carga util, restricciones de tamano, validacion de headers
de seguridad (Host, Origin, CSRF) y envolturas estandarizadas de respuesta para el backend local
conforme a CONTRATO-MVP-v1.md seccion 9, CT-014-016 y RF-001/006/016/019/025.
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlsplit

MAX_REQUEST_BODY_BYTES = 50 * 1024  # 50 KB
_LOCAL_AUTHORITY_RE = re.compile(
    r"(?:localhost|127\.0\.0\.1|\[::1\])(?::([0-9]{1,5}))?",
    re.IGNORECASE,
)


class APIContractError(Exception):
    """Excepcion de validacion de contrato de API."""
    pass


def _valid_port(raw_port: Optional[str]) -> bool:
    return raw_port is None or 1 <= int(raw_port) <= 65535


def is_loopback_authority(authority: Optional[str]) -> bool:
    """Acepta solo localhost/IPv4/IPv6 loopback y un puerto TCP valido opcional."""
    if not isinstance(authority, str):
        return False
    match = _LOCAL_AUTHORITY_RE.fullmatch(authority)
    return bool(match and _valid_port(match.group(1)))


def is_loopback_origin(origin: Optional[str]) -> bool:
    """Valida un Origin HTTP serializado, sin ruta, credenciales ni partes extra."""
    if not isinstance(origin, str) or not origin:
        return False
    try:
        parsed = urlsplit(origin)
        parsed_port = parsed.port
    except ValueError:
        return False
    return (
        parsed.scheme.lower() == "http"
        and parsed.username is None
        and parsed.password is None
        and parsed.path == ""
        and not parsed.query
        and not parsed.fragment
        and is_loopback_authority(parsed.netloc)
        and (parsed_port is None or 1 <= parsed_port <= 65535)
    )


def validate_local_request_security(headers: Dict[str, str]) -> Tuple[bool, Optional[str]]:
    """Valida Host y Origin para el adaptador local exclusivamente loopback."""
    norm_headers = {k.lower(): v for k, v in headers.items()}
    host = norm_headers.get("host")
    if not is_loopback_authority(host):
        return False, f"HOST_INVALIDO: El host '{host}' no es loopback local autorizado."
    origin = norm_headers.get("origin")
    if origin and not is_loopback_origin(origin):
        return False, f"CROSS_ORIGIN_PROHIBIDO: Origen '{origin}' no autorizado para la API local."
    return True, None


def validate_cloud_request_security(
    headers: Dict[str, str],
    allowed_hosts: set[str],
    allowed_origins: set[str],
) -> Tuple[bool, Optional[str]]:
    """Valida allowlists cloud exactas; una configuracion vacia falla cerrado."""
    norm_headers = {k.lower(): v for k, v in headers.items()}
    host = norm_headers.get("host")
    configured_hosts = {value.casefold() for value in allowed_hosts if value}
    if not isinstance(host, str) or host.casefold() not in configured_hosts:
        return False, f"HOST_INVALIDO: El host '{host}' no esta configurado para Cloud Run."
    origin = norm_headers.get("origin")
    configured_origins = {value.casefold() for value in allowed_origins if value}
    if origin and origin.casefold() not in configured_origins:
        return False, f"CROSS_ORIGIN_PROHIBIDO: Origen '{origin}' no autorizado para Cloud Run."
    return True, None


# Compatibilidad interna: el validador sin calificador siempre conserva semantica local.
validate_request_security = validate_local_request_security


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
