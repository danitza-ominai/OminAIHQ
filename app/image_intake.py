"""OminAI HQ - Ingesta y Saneamiento de Imagenes (PZ-009C).

Implementa la validacion de encabezados PNG/JPEG, proteccion contra bombas de descompresion,
eliminacion de metadatos EXIF/privados y distincion entre observacion e interpretacion visual.
"""

import hashlib
import struct
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

MAX_IMAGE_DIMENSION = 4096
MAX_IMAGE_PIXELS = 16_000_000  # 16 Megapixeles


class ImageIntakeError(Exception):
    """Excepcion controlada en la admision de imagenes."""
    pass


def parse_png_dimensions(raw_bytes: bytes) -> Tuple[bool, int, int, Optional[str]]:
    """Extrae ancho y alto de un archivo PNG desde su chunk IHDR."""
    if len(raw_bytes) < 24 or not raw_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return False, 0, 0, "Encabezado magico PNG invalido o truncado."

    try:
        width, height = struct.unpack(">II", raw_bytes[16:24])
        if width <= 0 or height <= 0:
            return False, 0, 0, "Dimensiones PNG no positivas."
        return True, width, height, None
    except Exception as e:
        return False, 0, 0, f"Error al parsear IHDR de PNG: {str(e)}"


def parse_jpeg_dimensions(raw_bytes: bytes) -> Tuple[bool, int, int, Optional[str]]:
    """Extrae ancho y alto de un archivo JPEG analizando los marcadores SOF0/SOF2."""
    if len(raw_bytes) < 4 or not raw_bytes.startswith(b"\xff\xd8"):
        return False, 0, 0, "Encabezado magico JPEG invalido."

    idx = 2
    length = len(raw_bytes)
    while idx < length - 8:
        if raw_bytes[idx] != 0xFF:
            idx += 1
            continue
        marker = raw_bytes[idx + 1]
        # Marcadores SOF0 (0xC0), SOF1 (0xC1), SOF2 (0xC2)
        if marker in (0xC0, 0xC1, 0xC2):
            try:
                # [idx+2, idx+4] es la longitud del segmento; [idx+5, idx+7] es alto, [idx+7, idx+9] es ancho
                height, width = struct.unpack(">HH", raw_bytes[idx + 5 : idx + 9])
                if width <= 0 or height <= 0:
                    return False, 0, 0, "Dimensiones JPEG no positivas."
                return True, width, height, None
            except Exception as e:
                return False, 0, 0, f"Error al parsear SOF de JPEG: {str(e)}"
        else:
            # Saltar segmento
            if idx + 4 > length:
                break
            seg_len = struct.unpack(">H", raw_bytes[idx + 2 : idx + 4])[0]
            idx += 2 + seg_len

    return False, 0, 0, "No se encontro marcador SOF valido en JPEG; archivo corrupto o truncado."


def sanitize_png_metadata(raw_bytes: bytes) -> bytes:
    """Elimina chunks no esenciales de metadatos (eXIf, tEXt, zTXt, iTXt) preservando IHDR, PLTE, IDAT, IEND."""
    if not raw_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return raw_bytes

    out = bytearray(raw_bytes[:8])
    idx = 8
    length = len(raw_bytes)

    while idx < length - 12:
        chunk_len = struct.unpack(">I", raw_bytes[idx : idx + 4])[0]
        chunk_type = raw_bytes[idx + 4 : idx + 8]
        end_chunk = idx + 12 + chunk_len

        # Filtrar metadatos sensibles y de texto
        if chunk_type not in (b"eXIf", b"tEXt", b"zTXt", b"iTXt", b"tIME"):
            out.extend(raw_bytes[idx:end_chunk])

        idx = end_chunk

    return bytes(out)


def sanitize_jpeg_metadata(raw_bytes: bytes) -> bytes:
    """Elimina marcadores APP1 (EXIF) preservando la estructura fundamental de la imagen JPEG."""
    if not raw_bytes.startswith(b"\xff\xd8"):
        return raw_bytes

    out = bytearray(b"\xff\xd8")
    idx = 2
    length = len(raw_bytes)

    while idx < length:
        if raw_bytes[idx] != 0xFF:
            out.append(raw_bytes[idx])
            idx += 1
            continue
        if idx + 1 >= length:
            out.append(raw_bytes[idx])
            break

        marker = raw_bytes[idx + 1]
        # APP1 marker (EXIF / GPS) es 0xE1
        if marker == 0xE1:
            if idx + 4 <= length:
                seg_len = struct.unpack(">H", raw_bytes[idx + 2 : idx + 4])[0]
                idx += 2 + seg_len
                continue
        out.extend(raw_bytes[idx : idx + 2])
        idx += 2

    return bytes(out)


class ImageIntakeManager:
    """Administrador de admision, analisis de dimensiones y saneamiento de imagenes."""

    def __init__(self) -> None:
        self.admitted_images: Dict[str, dict] = {}

    def process_image(
        self,
        filename: str,
        raw_bytes: bytes,
        mission_id: str,
        observed_caption: str = "",
    ) -> Tuple[bool, Optional[dict], Optional[str]]:
        """Valida, analiza dimensiones, detecta bombas de descompresion y genera copia saneada."""
        fn_lower = filename.lower()
        if not (fn_lower.endswith(".png") or fn_lower.endswith(".jpg") or fn_lower.endswith(".jpeg")):
            return False, None, "Formato de imagen no soportado. Formatos permitidos: PNG, JPG, JPEG."

        if len(raw_bytes) == 0:
            return False, None, "Archivo de imagen vacio (0 bytes)."

        # 1. Extraer dimensiones
        if fn_lower.endswith(".png"):
            ok_dim, width, height, err_dim = parse_png_dimensions(raw_bytes)
        else:
            ok_dim, width, height, err_dim = parse_jpeg_dimensions(raw_bytes)

        if not ok_dim:
            return False, None, f"Archivo de imagen corrupto o encabezado invalido: {err_dim}"

        # 2. Proteccion contra bombas de descompresion
        if width > MAX_IMAGE_DIMENSION or height > MAX_IMAGE_DIMENSION or (width * height) > MAX_IMAGE_PIXELS:
            return False, None, f"Bomba de descompresion detectada: dimensiones {width}x{height} exceden el umbral de seguridad."

        # 3. Saneamiento de metadatos EXIF
        if fn_lower.endswith(".png"):
            sanitized_bytes = sanitize_png_metadata(raw_bytes)
        else:
            sanitized_bytes = sanitize_jpeg_metadata(raw_bytes)

        sha256_orig = hashlib.sha256(raw_bytes).hexdigest()
        sha256_san = hashlib.sha256(sanitized_bytes).hexdigest()
        image_id = f"IMG-{sha256_orig[:8]}"

        record = {
            "image_id": image_id,
            "filename": filename,
            "mission_id": mission_id,
            "width": width,
            "height": height,
            "pixel_count": width * height,
            "original_size_bytes": len(raw_bytes),
            "sanitized_size_bytes": len(sanitized_bytes),
            "sha256_original": sha256_orig,
            "sha256_sanitized": sha256_san,
            "observed_caption": observed_caption,
            "visual_uncertainty_flag": "OBSERVACION_PRELIMINAR_NO_CONFIRMADA",
            "sanitized_bytes": sanitized_bytes,
            "admitted_at": datetime.now(timezone.utc).isoformat(),
        }

        self.admitted_images[image_id] = record
        return True, record, None
