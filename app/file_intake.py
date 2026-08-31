"""OminAI HQ - Ingesta Segura de Archivos y Originales Privados (PZ-009B).

Implementa las politicas de admision, limites de tamano, proteccion contra path traversal,
deteccion de secretos y almacenamiento de originales conforme a CONTRATO-MVP-v1.md seccion 11.7.
"""

import hashlib
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import app.document_extractors as document_extractors

# Limites aprobados
MAX_FILES_PER_MISSION = 5
MAX_FILE_BYTES = 20 * 1024 * 1024  # 20 MB
MAX_TOTAL_BYTES = 50 * 1024 * 1024  # 50 MB
MAX_URL_LINKS = 10
ALLOWED_EXTENSIONS = {"txt", "md", "pdf", "docx"}

# Patrones de seguridad
SECRET_PATTERN = re.compile(
    r"(?:api[_-]?key|secret|password|bearer|private[_-]?key)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-]{16,})['\"]?",
    re.IGNORECASE,
)
CONFIDENTIAL_PATTERN = re.compile(
    r"\b(CONFIDENCIAL|ESTRICTAMENTE CONFIDENCIAL|SECRETO EMPRESARIAL)\b",
    re.IGNORECASE,
)


class FileIntakeError(Exception):
    """Excepcion controlada en la admision de archivos."""
    pass


class FileIntakeManager:
    """Gestiona la admision, validacion de limites, deteccion de secretos y guardado de originales."""

    def __init__(self, storage_root: Optional[str] = None) -> None:
        self.storage_root = Path(storage_root) if storage_root else None
        self.admitted_files: Dict[str, dict] = {}

    def sanitize_filename(self, filename: str) -> Tuple[bool, str, Optional[str]]:
        """Valida que el nombre de archivo no contenga secuencias de path traversal ni caracteres prohibidos."""
        if not filename or not isinstance(filename, str):
            return False, "", "Nombre de archivo invalido o vacio."

        # Detectar path traversal
        if ".." in filename or "/" in filename or "\\" in filename or "\x00" in filename:
            return False, "", "Intento de Path Traversal o caracteres prohibidos detectados."

        clean_name = Path(filename).name
        parts = clean_name.rsplit(".", 1)
        if len(parts) != 2:
            return False, "", "El archivo debe tener una extension valida."

        ext = parts[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return False, "", f"Extension '.{ext}' no autorizada. Extensiones permitidas: {sorted(ALLOWED_EXTENSIONS)}."

        return True, clean_name, None

    def validate_file_magic(self, filename: str, raw_bytes: bytes) -> Tuple[bool, Optional[str]]:
        """Verifica la coherencia entre la extension declarada y los bytes magicos del encabezado."""
        ext = filename.rsplit(".", 1)[1].lower()

        if ext == "pdf":
            if not raw_bytes.startswith(b"%PDF-"):
                return False, "Encabezado binario no coincide con formato PDF legitimo."
        elif ext == "docx":
            if not raw_bytes.startswith(b"PK\x03\x04"):
                return False, "Encabezado binario no coincide con formato DOCX (ZIP) legitimo."
        elif ext in ("txt", "md"):
            # Verificar ausencia de bytes nulos binarios
            if b"\x00" in raw_bytes[:1024]:
                return False, "El archivo de texto contiene bytes binarios no permitidos."

        return True, None

    def screen_content_security(
        self,
        text_content: str,
        human_confidential_confirmed: bool = False,
    ) -> Tuple[bool, Optional[str], bool]:
        """Analiza el texto en busca de secretos desprotegidos y marcas de confidencialidad."""
        # 1. Bloqueo de secretos en texto claro
        if SECRET_PATTERN.search(text_content):
            return False, "SECRETO_DETECTADO: Se detectaron posibles credenciales o claves de API sin sanear.", False

        # 2. Comprobacion de confidencialidad
        is_confidential = bool(CONFIDENTIAL_PATTERN.search(text_content))
        if is_confidential and not human_confidential_confirmed:
            return False, "REQUIERE_CONFIRMACION_CONFIDENCIALIDAD: Archivo marcado como confidencial; requiere autorizacion humana expresa.", True

        return True, None, is_confidential

    def process_file_intake(
        self,
        filename: str,
        raw_bytes: bytes,
        mission_id: str,
        mission_version: int = 1,
        human_confidential_confirmed: bool = False,
        links_count: int = 0,
    ) -> Tuple[bool, Optional[dict], Optional[str]]:
        """Ejecuta el ciclo completo de validacion, extraccion y almacenamiento seguro del archivo."""
        if not mission_id or not isinstance(mission_id, str) or ".." in mission_id or "/" in mission_id or "\\" in mission_id:
            return False, None, "Identificador de mision invalido o sospechoso de Path Traversal."

        # 1. Validar limites por mision
        mission_files = [f for f in self.admitted_files.values() if f.get("mission_id") == mission_id]
        if len(mission_files) >= MAX_FILES_PER_MISSION:
            return False, None, f"Limite de {MAX_FILES_PER_MISSION} archivos por mision alcanzado."

        if links_count > MAX_URL_LINKS:
            return False, None, f"Limite de {MAX_URL_LINKS} enlaces web excedido."

        file_len = len(raw_bytes)
        if file_len == 0:
            return False, None, "El archivo esta vacio (0 bytes)."

        if file_len > MAX_FILE_BYTES:
            return False, None, f"El archivo excede el limite de {MAX_FILE_BYTES // (1024*1024)} MB."

        total_current_bytes = sum(f["size_bytes"] for f in mission_files)
        if total_current_bytes + file_len > MAX_TOTAL_BYTES:
            return False, None, f"El lote de archivos excede el limite total de {MAX_TOTAL_BYTES // (1024*1024)} MB."

        # 2. Validar nombre y path traversal
        ok_name, clean_name, err_name = self.sanitize_filename(filename)
        if not ok_name:
            return False, None, err_name

        # 3. Validar encabezados magicos
        ok_magic, err_magic = self.validate_file_magic(clean_name, raw_bytes)
        if not ok_magic:
            return False, None, err_magic

        # 4. Extraer texto estructurado
        ok_ext, extracted_text, warning_ext = document_extractors.extract_document_content(clean_name, raw_bytes)
        if not ok_ext:
            return False, None, f"Fallo en extraccion de contenido: {warning_ext}"

        # 5. Analisis de seguridad y confidencialidad
        ok_sec, err_sec, is_confidential = self.screen_content_security(
            extracted_text,
            human_confidential_confirmed=human_confidential_confirmed,
        )
        if not ok_sec:
            return False, None, err_sec

        # 6. Calcular huella SHA-256 del archivo original
        sha256_hash = hashlib.sha256(raw_bytes).hexdigest()
        file_id = f"FILE-{sha256_hash[:8]}"

        # 7. Guardar en almacenamiento seguro si storage_root esta configurado
        saved_path = None
        if self.storage_root:
            try:
                root_resolved = self.storage_root.resolve()
                dest_dir = (self.storage_root / mission_id).resolve()
                if not str(dest_dir).startswith(str(root_resolved)):
                    return False, None, "Path traversal detectado en mission_id."
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest_file = dest_dir / f"{sha256_hash[:12]}_{clean_name}"
                with open(dest_file, "wb") as f:
                    f.write(raw_bytes)
                saved_path = str(dest_file.resolve())
            except Exception as e:
                # Si falla el guardado, NO registrar que el archivo fue admitido
                return False, None, f"Fallo al escribir original en almacenamiento seguro: {str(e)}"

        record = {
            "file_id": file_id,
            "filename": clean_name,
            "size_bytes": file_len,
            "sha256": sha256_hash,
            "mission_id": mission_id,
            "mission_version": mission_version,
            "saved_path": saved_path,
            "is_confidential": is_confidential,
            "extracted_text_preview": extracted_text[:200] if extracted_text else "",
            "extracted_text_length": len(extracted_text),
            "extraction_warning": warning_ext,
            "admitted_at": datetime.now(timezone.utc).isoformat(),
        }

        self.admitted_files[f"{mission_id}:{file_id}"] = record
        return True, record, None
