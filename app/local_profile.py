"""OminAI HQ - Perfil Humano Unico Local (PZ-010A).

Implementa la gestion del perfil de usuario unico conforme a CONTRATO-MVP-v1.md seccion 11.2 y RF-002:
- Unico usuario humano operador/propietario (A0).
- Sin almacenamiento de passwords, autenticacion multi-usuario ni estructuras de equipos.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

DEFAULT_USER_ID = "usr_local_admin"
DEFAULT_DISPLAY_NAME = "Niko (A0)"


class LocalProfileError(Exception):
    """Excepcion controlada en la gestion del perfil local."""
    pass


class LocalProfileManager:
    """Administra el perfil unico del operador humano en el entorno local."""

    def __init__(self, initial_profile: Optional[dict] = None) -> None:
        self.profile = initial_profile or {
            "user_id": DEFAULT_USER_ID,
            "display_name": DEFAULT_DISPLAY_NAME,
            "email": "niko@ominai.dev",
            "actor_role": "usuario_humano",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_profile(self) -> dict:
        """Obtiene el perfil humano activo."""
        return dict(self.profile)

    def update_profile(
        self,
        display_name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Tuple[bool, dict, Optional[str]]:
        """Actualiza metadatos basicos del perfil sin admitir passwords ni multi-tenancy."""
        if display_name:
            if not display_name.strip():
                return False, self.profile, "El nombre no puede estar vacio."
            self.profile["display_name"] = display_name.strip()

        if email:
            if "@" not in email or "." not in email:
                return False, self.profile, "Formato de correo electronico invalido."
            self.profile["email"] = email.strip()

        self.profile["updated_at"] = datetime.now(timezone.utc).isoformat()
        return True, dict(self.profile), None
