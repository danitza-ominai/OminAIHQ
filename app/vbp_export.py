"""OminAI HQ - Exportador y Verificador Canonico de VBP (PZ-013C).

Implementa la exportacion determinista del Venture Build Package (VBP) canónico en Markdown (.md),
verificacion estricta de precondiciones de aprobacion humana, comprobacion de huellas SHA-256,
integridad de las 18 secciones y generacion de carga util para descarga en la interfaz web.
Cumple estrictamente con CONTRATO-MVP-v1.md secciones 6.1-6.6, 9.6, RF-018, RF-030 y FICHA-PZ-013C.md.
"""

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import app.runtime_contracts as runtime_contracts
import app.vbp_document as vbp_document


class VBPExportError(Exception):
    """Excepcion generica para fallos de exportacion de VBP."""
    pass


class VBPExportNotApprovedError(VBPExportError):
    """El VBP no cuenta con una aprobacion humana formal registrada."""
    pass


class VBPExportIntegrityError(VBPExportError):
    """La huella o las secciones del VBP no coinciden con el contrato canonico."""
    pass


def validate_vbp_export_preconditions(
    vbp_data: Dict[str, Any],
    mission_status: Optional[str] = None,
    repository=None,
) -> Tuple[bool, Optional[str]]:
    """Verifica que el VBP cumpla todas las condiciones previas para poder ser exportado y descargado.
    
    Reglas contractuales (CONTRATO-MVP-v1.md 6.6, 9.6, RF-018, RF-030):
    1. El VBP debe tener estado de aprobacion 'APROBADO' (o la mision debe estar en 'VBP_APROBADO' o 'FINALIZADA').
    2. Debe existir una referencia formal a la aprobacion humana ('human_approval_ref' no nulo).
    3. Debe contener exactamente las 18 secciones obligatorias.
    4. La huella digital del manifest debe coincidir exactamente con el calculo sobre el contenido.
    """
    if not isinstance(vbp_data, dict):
        return False, "INVALID_INPUT: El objeto VBP debe ser un diccionario valido."

    serialized = json.dumps(vbp_data, ensure_ascii=False)
    if re.search(r"(?i)(?:javascript\s*:|data\s*:\s*text/html|file\s*://|(?:api[_-]?key|password|secret|token)\s*[:=]\s*[^\s,]+|-----BEGIN.*PRIVATE KEY)", serialized):
        return False, "PERMISSION_DENIED: Contenido sensible o enlace peligroso; requiere saneamiento antes de aprobar."
    # 1. Validar estado de aprobacion
    approval_status = vbp_data.get("approval_status")
    allowed_vbp_statuses = {"APROBADO", "APROBADO_CON_EXCEPCION"}
    allowed_mission_statuses = {"VBP_APROBADO", "FINALIZADA"}

    if approval_status not in allowed_vbp_statuses:
        return False, f"NOT_APPROVED: El VBP tiene estado '{approval_status}'. Solo un VBP aprobado puede exportarse."

    # 2. Validar referencia de aprobacion humana
    approval_ref = vbp_data.get("human_approval_ref")
    if not approval_ref or not str(approval_ref).strip():
        return False, "MISSING_HUMAN_APPROVAL: Falta la referencia obligatoria a la aprobacion humana ('human_approval_ref')."

    # 3. Validar las 18 secciones obligatorias
    sections = vbp_data.get("sections", [])
    if len(sections) != 18:
        return False, f"SECTION_COUNT_INVALID: Se requieren exactamente 18 secciones, encontradas {len(sections)}."

    for idx, expected_name in enumerate(runtime_contracts.VBP_SECTION_NAMES, start=1):
        sec = sections[idx - 1]
        if sec.get("section_number") != idx:
            return False, f"SECTION_ORDER_INVALID: Seccion {idx} tiene numero invalido {sec.get('section_number')}."
        if sec.get("section_name") != expected_name:
            return False, f"SECTION_NAME_INVALID: Seccion {idx} esperaba '{expected_name}', encontrada '{sec.get('section_name')}'."

    # 4. Validar huella de integridad del manifest
    stored_fp = vbp_data.get("fingerprint")
    calc_fp = runtime_contracts.compute_vbp_manifest_fingerprint(vbp_data)
    if stored_fp != calc_fp:
        return False, f"INTEGRITY_FINGERPRINT_MISMATCH: La huella registrada '{stored_fp}' no coincide con el calculo canonico '{calc_fp}'."

    if repository is None:
        return False, "NOT_APPROVED: Registro persistido requerido."
    mission = repository.get_mission(vbp_data.get("mission_id", ""))
    wrapper = repository.get_object("approval_request", approval_ref)
    if not mission or not wrapper:
        return False, "NOT_APPROVED: Aprobacion persistida inexistente."
    request, record = wrapper["request"], wrapper["record"]
    if (mission.get("status") not in allowed_mission_statuses
        or request.get("gate_type") != "GATE_2_VBP"
        or request.get("mission_id") != vbp_data["mission_id"]
        or request.get("version") != vbp_data.get("mission_version")
        or vbp_data.get("mission_version") > mission["version"]
        or record.get("status") != "CONSUMIDA"
        or record.get("decision") != {"APROBADO": "APROBAR", "APROBADO_CON_EXCEPCION": "APROBAR_CON_EXCEPCION"}[approval_status]
        or request.get("approval_id") != approval_ref
        or record.get("approval_id") != approval_ref
        or request.get("fingerprint") != stored_fp
        or record.get("actor") != mission.get("user_id")
        or record.get("actor_role") != "usuario_humano"
        or record.get("action_approved") != f"Aprobacion del VBP {vbp_data['vbp_id']} v{vbp_data['version']} de la mision {vbp_data['mission_id']}"
        or record.get("version_or_fingerprint") != stored_fp
        or record.get("user_id") != mission.get("user_id")):
        return False, "NOT_APPROVED: Aprobacion no corresponde al contenido y version."
    from app.human_approvals import evidence_available
    if not evidence_available(repository, mission):
        return False, "EVIDENCIA_NO_DISPONIBLE"
    stored = repository.get_object("candidate", vbp_data["mission_id"] + ":GATE_2_VBP")
    if not stored or stored != vbp_data or runtime_contracts.compute_vbp_manifest_fingerprint(stored) != stored_fp:
        return False, "INTEGRITY_FINGERPRINT_MISMATCH: Candidato aprobado diferente."
    valid, errors = runtime_contracts.RuntimeContractsValidator().validate_structure("vbp", vbp_data)
    if not valid:
        return False, "SCHEMA_INVALID: VBP fuera de contrato."
    return True, None


def export_canonical_vbp_markdown(
    vbp_data: Dict[str, Any],
    mission_status: Optional[str] = None,
    repository=None,
    include_bilingual_blocks: bool = False,
) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    """Genera el texto Markdown canonico y metadatos de exportacion tras validar integridad.
    
    Devuelve: (exito, markdown_text_o_error, metadata)
    """
    ok, err = validate_vbp_export_preconditions(vbp_data, mission_status=mission_status, repository=repository)
    if not ok:
        return False, err, None

    # Renderizar Markdown canonico
    markdown_text = vbp_document.render_canonical_markdown(vbp_data, include_bilingual_blocks=include_bilingual_blocks)
    md_fingerprint = vbp_document.compute_markdown_content_fingerprint(markdown_text)

    metadata = {
        "vbp_id": vbp_data.get("vbp_id"),
        "mission_id": vbp_data.get("mission_id"),
        "version": vbp_data.get("version", 1),
        "manifest_fingerprint": vbp_data.get("fingerprint"),
        "markdown_fingerprint": md_fingerprint,
        "content_length_bytes": len(markdown_text.encode("utf-8")),
        "filename": f"{vbp_data.get('vbp_id', 'VBP')}.md",
        "mime_type": "text/markdown; charset=utf-8",
        "human_approval_ref": vbp_data.get("human_approval_ref"),
        "language": vbp_data.get("language", "es"),
    }

    return True, markdown_text, metadata


def export_canonical_vbp_bytes(
    vbp_data: Dict[str, Any],
    mission_status: Optional[str] = None,
    repository=None,
    include_bilingual_blocks: bool = False,
) -> Tuple[bool, Optional[bytes], Optional[Dict[str, Any]], Optional[str]]:
    """Genera los bytes UTF-8 del VBP Markdown para descarga HTTP directa.
    
    Devuelve: (exito, raw_bytes, metadata, error_message)
    """
    ok, md_or_err, meta = export_canonical_vbp_markdown(
        vbp_data,
        mission_status=mission_status,
        repository=repository,
        include_bilingual_blocks=include_bilingual_blocks,
    )
    if not ok:
        return False, None, None, md_or_err

    raw_bytes = md_or_err.encode("utf-8")
    return True, raw_bytes, meta, None


def export_vbp_to_file(
    vbp_data: Dict[str, Any],
    destination_path: Path,
    mission_status: Optional[str] = None,
    repository=None,
    include_bilingual_blocks: bool = False,
) -> Tuple[bool, Optional[str]]:
    """Escribe de forma atomica el VBP Markdown canonico a un archivo local."""
    ok, raw_bytes, meta, err = export_canonical_vbp_bytes(
        vbp_data,
        mission_status=mission_status,
        repository=repository,
        include_bilingual_blocks=include_bilingual_blocks,
    )
    if not ok:
        return False, err

    try:
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dest = destination_path.with_suffix(".tmp_export")
        temp_dest.write_bytes(raw_bytes)
        temp_dest.replace(destination_path)
        return True, None
    except Exception as e:
        return False, f"IO_ERROR: Fallo al escribir archivo de exportacion: {str(e)}"
