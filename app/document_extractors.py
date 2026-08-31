"""OminAI HQ - Extractores Estructurados de Documentos (PZ-009B).

Implementa la extraccion determinista y segura de texto para archivos TXT, MD, PDF y DOCX
sin dependencias externas y sin ejecutar macros ni scripts incrustados.
"""

import io
import re
import xml.etree.ElementTree as ET
import zipfile
from typing import Optional, Tuple


class DocumentExtractionError(Exception):
    """Excepcion controlada en la extraccion de documentos."""
    pass


def extract_txt_or_md(raw_bytes: bytes) -> Tuple[bool, str, Optional[str]]:
    """Extrae texto plano o markdown validando codificacion UTF-8 / Latin-1."""
    try:
        text = raw_bytes.decode("utf-8")
        return True, text, None
    except UnicodeDecodeError:
        try:
            text = raw_bytes.decode("latin-1")
            return True, text, None
        except Exception as e:
            return False, "", f"Error de decodificacion de texto: {str(e)}"


MAX_UNCOMPRESSED_DOCX_BYTES = 50 * 1024 * 1024  # 50 MB limit


def extract_docx(raw_bytes: bytes) -> Tuple[bool, str, Optional[str]]:
    """Extrae texto estructurado de un archivo DOCX analizando su archivo interno word/document.xml."""
    try:
        with zipfile.ZipFile(io.BytesIO(raw_bytes)) as zf:
            # 1. Proteccion contra bombas de descompresion
            total_uncompressed = sum(info.file_size for info in zf.infolist())
            if total_uncompressed > MAX_UNCOMPRESSED_DOCX_BYTES:
                return False, "", "Bomba de descompresion detectada: tamano descomprimido excede 50 MB."

            if "word/document.xml" not in zf.namelist():
                return False, "", "Archivo DOCX invalido: no contiene word/document.xml."
            xml_content = zf.read("word/document.xml")

        tree = ET.fromstring(xml_content)
        # Namespace de WordProcessingML
        namespaces = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

        paragraphs = []
        for p in tree.findall(".//w:p", namespaces):
            texts = [node.text for node in p.findall(".//w:t", namespaces) if node.text]
            if texts:
                paragraphs.append("".join(texts))

        extracted = "\n".join(paragraphs)
        return True, extracted, None
    except zipfile.BadZipFile:
        return False, "", "Archivo DOCX corrupto o formato no compatible."
    except Exception as e:
        return False, "", f"Fallo al procesar DOCX: {str(e)}"


def extract_pdf(raw_bytes: bytes) -> Tuple[bool, str, Optional[str]]:
    """Extrae texto de un archivo PDF analizando flujos de texto (descomprimiendo FlateDecode si aplica)."""
    if not raw_bytes.startswith(b"%PDF-"):
        return False, "", "Encabezado magico de PDF invalido."

    import zlib
    try:
        text_chunks = []

        # Buscar bloques stream ... endstream en binario
        stream_pattern = re.compile(rb"stream\r?\n(.*?)\r?\nendstream", re.DOTALL)
        for match in stream_pattern.finditer(raw_bytes):
            stream_data = match.group(1)
            # Intentar descompresion FlateDecode
            decompressed = None
            try:
                decompressed = zlib.decompress(stream_data)
            except Exception:
                decompressed = stream_data

            try:
                stream_text = decompressed.decode("latin-1", errors="ignore")
            except Exception:
                continue

            # Buscar operadores de texto Tj y TJ dentro de BT ... ET
            tj_matches = re.findall(r"\(([^)]+)\)\s*(?:Tj|'|\"|TJ)", stream_text)
            if tj_matches:
                text_chunks.extend(tj_matches)
            else:
                # Buscar arrays de cadenas en TJ: [(texto) 10 (otro)] TJ
                array_matches = re.findall(r"\[(.*?)\]\s*TJ", stream_text, re.DOTALL)
                for arr in array_matches:
                    inner = re.findall(r"\(([^)]+)\)", arr)
                    if inner:
                        text_chunks.extend(inner)

        # Si no encontramos streams estructurados, buscar en el contenido directo
        if not text_chunks:
            direct_text = raw_bytes.decode("latin-1", errors="ignore")
            direct_matches = re.findall(r"\(([^)]+)\)\s*(?:Tj|'|\"|TJ)", direct_text)
            if direct_matches:
                text_chunks.extend(direct_matches)

        extracted = " ".join(text_chunks).strip()
        if not extracted:
            return True, "", "DOCUMENTO_ESCANEADO_SIN_TEXTO"

        return True, extracted, None
    except Exception as e:
        return False, "", f"Fallo al procesar PDF: {str(e)}"


def extract_document_content(filename: str, raw_bytes: bytes) -> Tuple[bool, str, Optional[str]]:
    """Despacha la extraccion segun la extension validada del archivo."""
    fn_lower = filename.lower()
    if fn_lower.endswith(".txt") or fn_lower.endswith(".md"):
        return extract_txt_or_md(raw_bytes)
    elif fn_lower.endswith(".docx"):
        return extract_docx(raw_bytes)
    elif fn_lower.endswith(".pdf"):
        return extract_pdf(raw_bytes)
    else:
        return False, "", f"Tipo de archivo no soportado para extraccion: {filename}."
