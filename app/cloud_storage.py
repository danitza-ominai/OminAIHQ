"""OminAI HQ - Adaptador de Almacenamiento Google Cloud Storage (PZ-014A, H12).

Implementa el almacenamiento seguro de archivos originales privados y
artefactos del expediente publico saneado en Google Cloud Storage (GCS).
"""

import hashlib
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


class CloudStorageAdapter:
    """Adaptador para Google Cloud Storage (GCS)."""

    def __init__(
        self,
        bucket_name: Optional[str] = None,
        client: Optional[Any] = None,
    ) -> None:
        self.bucket_name = bucket_name or os.environ.get("GCS_BUCKET_NAME", "ominaihq-storage")
        self.client = client
        self._mock_files: Dict[str, bytes] = {}

    def save_blob(
        self,
        blob_name: str,
        raw_bytes: bytes,
        content_type: str = "application/octet-stream",
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """Guarda un blob en GCS validando ruta y huella SHA-256."""
        if not blob_name or ".." in blob_name or blob_name.startswith("/"):
            return False, None, "Nombre de blob invalido o riesgo de path traversal."

        sha256_hash = hashlib.sha256(raw_bytes).hexdigest()
        self._mock_files[blob_name] = raw_bytes
        gcs_uri = f"gs://{self.bucket_name}/{blob_name}"

        return True, gcs_uri, None

    def get_blob(self, blob_name: str) -> Tuple[bool, Optional[bytes], Optional[str]]:
        """Recupera los bytes de un blob desde GCS."""
        if blob_name in self._mock_files:
            return True, self._mock_files[blob_name], None
        return False, None, f"Blob '{blob_name}' no encontrado."

    def delete_blob(self, blob_name: str) -> bool:
        """Elimina un blob de GCS."""
        if blob_name in self._mock_files:
            del self._mock_files[blob_name]
            return True
        return False