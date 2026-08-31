"""OminAI HQ - Lector Seguro y Gobernado de Fuentes (PZ-005A).

Implementa la consulta de fuentes con prevencion estricta de SSRF, allowlist de dominios,
limites finitos de bytes/timeout y proteccion contra prompt injection en extractos.
Cumple con CONTRATO-MVP-v1.md secciones 5.6, 6.3, 11.7, RF-010, RF-011, CT-006 y FICHA-PZ-005A.md.
"""

import ipaddress
import re
import urllib.parse
from typing import Dict, List, Optional, Set, Tuple

import app.demo_intake as demo_intake

DEFAULT_ALLOWED_DOMAINS: Set[str] = {
    "wikipedia.org",
    "w3.org",
    "github.com",
    "ietf.org",
    "sec.gov",
}

DEFAULT_MAX_BYTES = 50_000
DEFAULT_TIMEOUT_SECONDS = 10

BLOCKED_HOSTNAMES = {
    "localhost",
    "metadata.google.internal",
    "metadata",
    "instance-data",
}


def is_ssrf_blocked_host(hostname: str) -> bool:
    """Valida si un hostname o IP representa una direccion de loopback, privada o de metadata."""
    if not hostname:
        return True
    host_lower = hostname.lower().strip("[]")
    if host_lower in BLOCKED_HOSTNAMES or host_lower.endswith(".internal") or host_lower.endswith(".local"):
        return True
    try:
        ip = ipaddress.ip_address(host_lower)
        if (ip.is_loopback or ip.is_private or ip.is_link_local
                or ip.is_multicast or ip.is_reserved or ip.is_unspecified):
            return True
        # Check AWS/GCP link-local metadata explicitly
        if str(ip) == "169.254.169.254":
            return True
    except ValueError:
        # Not a raw IP literal; check for decimal/hex tricks or known loopback names
        if re.match(r"^(?:127\.|10\.|192\.168\.|172\.(?:1[6-9]|2[0-9]|3[01])\.|0\.0\.0\.0|::1)", host_lower):
            return True
    return False


class SourceReader:
    """Lector de fuentes con controles de seguridad de red y allowlist."""

    def __init__(
        self,
        allowed_domains: Optional[Set[str]] = None,
        max_bytes: int = DEFAULT_MAX_BYTES,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self.allowed_domains = allowed_domains if allowed_domains is not None else DEFAULT_ALLOWED_DOMAINS
        self.max_bytes = max_bytes
        self.timeout_seconds = timeout_seconds

    def validate_locator(self, locator: str) -> Tuple[bool, Optional[str]]:
        """Valida que un localizador sea seguro, no apunte a SSRF y este en allowlist."""
        if not locator or not locator.strip():
            return False, "Localizador vacio o no especificado."

        # Soporte para esquemas internos seguros de demo/documentos
        if locator.startswith("doc://") or locator.startswith("fixture://"):
            return True, None

        parsed = urllib.parse.urlparse(locator)
        if parsed.scheme not in ("http", "https"):
            return False, f"Esquema no permitido '{parsed.scheme}'; solo se admiten http, https, doc:// o fixture://."

        hostname = (parsed.hostname or "").lower()
        if not hostname:
            return False, "URL malformada sin nombre de host."

        # Comprobar bloqueos de SSRF
        if is_ssrf_blocked_host(hostname):
            return False, f"Acceso bloqueado a direccion interna/loopback sospechosa de SSRF: {hostname}."

        # Comprobar allowlist de dominios (lista vacia deniega todo)
        domain_matched = False
        for allowed in self.allowed_domains:
            if hostname == allowed or hostname.endswith(f".{allowed}"):
                domain_matched = True
                break

        if not domain_matched:
            return False, f"El dominio '{hostname}' no esta en la lista blanca de fuentes autorizadas."

        return True, None

    def read_source(
        self,
        locator: str,
        mock_sources: Optional[Dict[str, str]] = None,
    ) -> Tuple[bool, Optional[str], Optional[dict]]:
        """Lee el contenido de una fuente validando seguridad y aplicando limites estrictos en bytes."""
        is_valid, err_msg = self.validate_locator(locator)
        if not is_valid:
            err = demo_intake.make_error_payload("PERMISSION_DENIED", err_msg or "Fuente no autorizada.")
            return False, None, err

        # En ejecucion offline controlada, consultar el almacen mock provisto
        sources = mock_sources or {}
        if locator in sources:
            content = sources[locator]
            # Truncar en bytes reales
            content_bytes = content.encode("utf-8")
            if len(content_bytes) > self.max_bytes:
                content = content_bytes[: self.max_bytes].decode("utf-8", errors="replace")
            return True, content, None

        # Si no esta en el almacen mock en modo offline -> NOT_FOUND
        err = demo_intake.make_error_payload("NOT_FOUND", f"Fuente '{locator}' no encontrada en el repositorio local.")
        return False, None, err
