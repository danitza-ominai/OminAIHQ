"""OminAI HQ - Registro de Evidencias y Validacion de Procedencia (PZ-009A).

Implementa las responsabilidades de trazabilidad de evidencia y procedencia segun CONTRATO-MVP-v1.md seccion 6.3 y 11.7:
- Registro indexado de evidencias atomicas por claim, version y localizador de fuente.
- Soporte de multiples afirmaciones sobre una misma fuente documental.
- Deteccion de contradicciones entre fuentes con registro de decision humana pendiente.
- Revalidacion estricta de disponibilidad de evidencias previas a decisiones y puertas de aprobacion.
- Mapeo de fallos de disponibilidad a estados nucleares existentes (PAUSADA/BLOQUEADA) con motivo funcional EVIDENCIA_REQUERIDA.
- Preservacion de VBPs historicos tras eliminacion de originales marcando VERIFICABILIDAD_INCOMPLETA.
"""

import copy
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

import app.runtime_contracts as runtime_contracts
from jsonschema import Draft202012Validator


def create_evidence_record(
    evidence_id: str,
    mission_id: str,
    claim_id: str,
    title: str,
    source_locator: str,
    excerpt_or_summary: str,
    author_or_organization: str = "",
    source_type: str = "ENLACE_WEB",
    location_in_source: str = "",
    publication_date: Optional[str] = None,
    retrieval_date: Optional[str] = None,
    collector: str = "research_evidence_analyst",
    confidence: str = "ALTA",
    confidence_justification: str = "Fuente primaria validada",
    limitations: Optional[List[str]] = None,
    contradictions: Optional[List[str]] = None,
    verification_status: str = "VALIDADA",
    mission_version: int = 1,
) -> dict:
    """Construye un registro de evidencia canonico con huella SHA-256 calculada conforme a evidence.schema.json."""
    ret_dt = retrieval_date or datetime.now(timezone.utc).isoformat()
    record = {
        "schema_version": "1.0.0",
        "evidence_id": evidence_id,
        "mission_id": mission_id,
        "claim_id": claim_id,
        "title": title,
        "author_or_organization": author_or_organization,
        "source_type": source_type,
        "source_locator": source_locator,
        "location_in_source": location_in_source,
        "publication_date": publication_date,
        "retrieval_date": ret_dt,
        "excerpt_or_summary": excerpt_or_summary,
        "collector": collector,
        "confidence": confidence,
        "confidence_justification": confidence_justification,
        "limitations": limitations or [],
        "contradictions": contradictions or [],
        "verification_status": verification_status,
        "mission_version": mission_version,
    }
    record["fingerprint"] = runtime_contracts.compute_evidence_fingerprint(record)
    return record


class EvidenceRegistry:
    """Registro inmutable y verificador de procedencia de evidencias para misiones de OminAI HQ."""

    def __init__(
        self,
        initial_records: Optional[Dict[str, dict]] = None,
        source_contents: Optional[Dict[str, str]] = None,
    ) -> None:
        self.records: Dict[str, dict] = dict(initial_records or {})
        self.source_contents: Dict[str, str] = dict(source_contents or {})
        self.source_fingerprints: Dict[str, str] = {}
        self.contradictions: List[dict] = []

        # Inicializar huellas de contenido
        for loc, content in self.source_contents.items():
            self.source_fingerprints[loc] = hashlib.sha256(content.encode("utf-8")).hexdigest()

        # Cargar validador de contrato de evidencia
        _, _, self.evidence_schema, _ = runtime_contracts.load_runtime_contracts()
        self.validator = Draft202012Validator(self.evidence_schema)

    def register_evidence(
        self,
        evidence: dict,
        source_content: Optional[str] = None,
        expected_mission_id: Optional[str] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Registra y valida una evidencia atomica contra evidence.schema.json y politicas de integridad."""
        # 1. Validacion estructural de schema
        try:
            self.validator.validate(evidence)
        except Exception as e:
            return False, f"Fallo de validacion de esquema de evidencia: {str(e)}"

        evd_id = evidence["evidence_id"]
        mission_id = evidence["mission_id"]

        # 2. Rechazar referencias cruzadas entre misiones no vinculadas
        if expected_mission_id and mission_id != expected_mission_id:
            return False, f"Referencia cruzada rechazada: mision {mission_id} no coincide con mision esperada {expected_mission_id}."

        # 3. Validacion de coherencia temporal (retrieval_date >= publication_date)
        pub_dt = evidence.get("publication_date")
        ret_dt = evidence.get("retrieval_date")
        if pub_dt and ret_dt:
            try:
                if ret_dt < pub_dt:
                    return False, f"Incoherencia temporal: fecha de consulta {ret_dt} previa a publicacion {pub_dt}."
            except Exception:
                pass

        # 4. Registrar contenido y huella de fuente si se provee
        source_loc = evidence["source_locator"]
        if source_content is not None:
            self.source_contents[source_loc] = source_content
            self.source_fingerprints[source_loc] = hashlib.sha256(source_content.encode("utf-8")).hexdigest()

        self.records[evd_id] = copy.deepcopy(evidence)
        return True, None

    def get_evidence(self, evidence_id: str) -> Optional[dict]:
        """Recupera una evidencia por su identificador unico."""
        item = self.records.get(evidence_id)
        return copy.deepcopy(item) if item else None

    def get_evidences_for_source(self, source_locator: str) -> List[dict]:
        """Obtiene todas las evidencias asociadas a un localizador de fuente especifico."""
        return [
            copy.deepcopy(rec)
            for rec in self.records.values()
            if rec.get("source_locator") == source_locator
        ]

    def record_contradiction(
        self,
        evidence_id_a: str,
        evidence_id_b: str,
        topic: str,
        description: str,
    ) -> dict:
        """Registra una contradiccion formal entre dos evidencias conservando ambas fuentes."""
        evd_a = self.records.get(evidence_id_a)
        evd_b = self.records.get(evidence_id_b)
        contradiction_record = {
            "contradiction_id": f"CONTRA-{len(self.contradictions) + 1:03d}",
            "evidence_a": evidence_id_a,
            "source_a": evd_a.get("source_locator") if evd_a else "desconocido",
            "evidence_b": evidence_id_b,
            "source_b": evd_b.get("source_locator") if evd_b else "desconocido",
            "topic": topic,
            "description": description,
            "status": "PENDIENTE_DECISION_HUMANA",
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }
        self.contradictions.append(contradiction_record)
        return contradiction_record

    def withdraw_source(self, source_locator: str) -> None:
        """Simula o aplica el retiro/desaparicion de un original de fuente."""
        if source_locator in self.source_contents:
            del self.source_contents[source_locator]

    def validate_availability_before_gate(
        self,
        required_evidence_ids: List[str],
    ) -> Tuple[bool, List[str], Optional[dict]]:
        """Revalida la disponibilidad de evidencias y fuentes originales antes de una puerta de aprobacion."""
        missing: List[str] = []
        for evd_id in required_evidence_ids:
            rec = self.records.get(evd_id)
            if not rec:
                missing.append(evd_id)
                continue
            loc = rec.get("source_locator")
            if loc and (loc.startswith("http") or loc.startswith("doc://")) and loc not in self.source_contents:
                missing.append(evd_id)

        if missing:
            error_envelope = {
                "error_code": "RESOURCE_UNAVAILABLE",
                "functional_reason": "EVIDENCIA_REQUERIDA",
                "message": "EVIDENCIA_NO_DISPONIBLE",
                "suggested_state": "PAUSADA",
                "missing_evidences": missing,
            }
            return False, missing, error_envelope

        return True, [], None

    def assess_post_approval_verifiability(
        self,
        vbp_data: dict,
    ) -> dict:
        """Evalua la verificabilidad de un VBP aprobado ante la eventual perdida posterior de fuentes."""
        vbp_copy = copy.deepcopy(vbp_data)
        missing_count = 0
        total_evidences = 0

        manifest = vbp_copy.get("manifest", {})
        evidence_ids = manifest.get("evidence_items_covered", [])

        for evd_id in evidence_ids:
            total_evidences += 1
            rec = self.records.get(evd_id)
            if not rec or (rec.get("source_locator") and rec.get("source_locator") not in self.source_contents):
                missing_count += 1

        if missing_count > 0:
            vbp_copy["verifiability_status"] = "VERIFICABILIDAD_INCOMPLETA"
            vbp_copy["verifiability_details"] = f"{missing_count} de {total_evidences} fuentes originales no se encuentran disponibles; el documento VBP historico se conserva intacto."
        else:
            vbp_copy["verifiability_status"] = "COMPLETA"

        return vbp_copy
