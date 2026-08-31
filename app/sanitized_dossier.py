"""OminAI HQ - Expediente Saneado de Competencia (PZ-009C).

Implementa la separacion estricta entre el espacio de trabajo privado y el expediente publico
de competencia, garantizando anonimizacion de rutas, stripping de metadatos y revocabilidad de permisos.
"""

import copy
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple


class SanitizedDossierManager:
    """Gestiona la construccion, autorizacion y exportacion del expediente publico saneado."""

    def __init__(self) -> None:
        self.authorized_items: Dict[str, Dict[str, dict]] = {}

    def authorize_item_for_dossier(
        self,
        mission_id: str,
        item_id: str,
        item_type: str,
        public_filename: str,
        sanitized_bytes: bytes,
        original_hash: str,
        description: str = "",
        *,
        context=None,
        mission_version: int = 1,
    ) -> dict:
        """Registra una autorizacion expresa humana para incluir un artefacto en el expediente publico."""
        sanitized_hash = hashlib.sha256(sanitized_bytes).hexdigest()
        entry = {
            "mission_id": mission_id,
            "mission_version": mission_version,
            "item_id": item_id,
            "item_type": item_type,
            "public_filename": public_filename,
            "sha256_sanitized": sanitized_hash,
            "sha256_original": original_hash,
            "size_bytes": len(sanitized_bytes),
            "description": description,
            "status": "AUTORIZADO_PUBLICO",
            "sanitized_bytes": sanitized_bytes,
            "authorized_at": datetime.now(timezone.utc).isoformat(),
        }
        if mission_id not in self.authorized_items:
            self.authorized_items[mission_id] = {}
        self.authorized_items[mission_id][item_id] = entry
        return entry

    def revoke_item_authorization(self, item_id: str, mission_id: Optional[str] = None) -> bool:
        """Revoca inmediatamente la autorizacion publica de un artefacto."""
        if mission_id:
            if mission_id in self.authorized_items and item_id in self.authorized_items[mission_id]:
                del self.authorized_items[mission_id][item_id]
                return True
            return False
        revoked = False
        for m_id in list(self.authorized_items.keys()):
            if item_id in self.authorized_items[m_id]:
                del self.authorized_items[m_id][item_id]
                revoked = True
        return revoked

    def build_public_dossier_manifest(
        self,
        mission_id: str,
        vbp_title: str,
    ) -> Tuple[bool, Optional[dict], Optional[str]]:
        """Construye el manifest anonimizado del expediente publico excluyendo rutas privadas."""
        active_items = []
        mission_items = self.authorized_items.get(mission_id, {})
        for item in mission_items.values():
            if item.get("status") == "AUTORIZADO_PUBLICO":
                active_items.append({
                    "item_id": item["item_id"],
                    "public_filename": item["public_filename"],
                    "item_type": item["item_type"],
                    "sha256_sanitized": item["sha256_sanitized"],
                    "size_bytes": item["size_bytes"],
                    "description": item["description"],
                })

        manifest = {
            "dossier_version": "1.0.0",
            "mission_id": mission_id,
            "vbp_title": vbp_title,
            "sanitization_policy": "ANONYMIZED_EXIF_STRIPPED_NO_PRIVATE_PATHS",
            "total_items": len(active_items),
            "items": sorted(active_items, key=lambda x: x["item_id"]),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

        # Calcular huella del manifest
        hasher = hashlib.sha256()
        hasher.update(f"{mission_id}:{vbp_title}".encode("utf-8"))
        for it in manifest["items"]:
            hasher.update(f"{it['item_id']}:{it['sha256_sanitized']}:{it['public_filename']}:{it['size_bytes']}".encode("utf-8"))
        manifest["dossier_fingerprint"] = f"sha256:{hasher.hexdigest()}"

        return True, manifest, None
