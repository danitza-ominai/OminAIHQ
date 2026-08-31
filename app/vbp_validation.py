"""OminAI HQ - Motor determinista de validacion y evaluacion de VBP (PZ-003E).

Implementa la evaluacion determinista de las 5 dimensiones ponderadas (30/25/20/15/10),
la deteccion de bloqueadores absolutos y la emision de dictamenes conformes a CONTRATO-MVP-v1.md seccion 11.8:
- PASA (>= 80 sin bloqueadores)
- PASA_CON_CONDICIONES (70 a 79 sin bloqueadores)
- NO_PASA (< 70 o cualquier bloqueador activo).
"""

import copy
from typing import Any, Dict, List, Optional, Tuple

import app.demo_intake as demo_intake
import app.runtime_contracts as runtime_contracts
import app.vbp_document as vbp_document

WEIGHTS = {
    "cobertura_secciones": 0.30,
    "evidencia_trazabilidad": 0.25,
    "coherencia_requisitos_alcance": 0.20,
    "riesgos_gobernanza": 0.15,
    "calidad_formal_manifest": 0.10,
}


def build_evaluation_context(envelope):
    """Project existing records to the exact closed validator interface.

    Originals are explicit records, not references inferred from citation text.
    Missing records remain missing so the validator rejects their references.
    """
    mission = copy.deepcopy(envelope["mission"])
    mid, version = mission["mission_id"], mission["record_version"]
    descriptor = lambda ref: {"ref_id": ref, "mission_id": mid, "mission_version": version}
    artifacts = {key: envelope[key] for key in ("brief", "plan") if envelope.get(key)}
    artifacts.update(envelope.get("task_results", {}))
    evidence = list(envelope.get("evidence_store", {}).values())
    artifacts.update({ev["evidence_id"]: ev for ev in evidence})
    inputs = dict(artifacts)
    claims = {}
    for ev in evidence:
        original = envelope.get("evidence_originals", {}).get(ev["evidence_id"])
        if original and original.get("fingerprint") == ev["fingerprint"]:
            inputs[ev["source_locator"]] = original
            claims[ev["claim_id"]] = ev["excerpt_or_summary"]
    tasks = copy.deepcopy(envelope.get("tasks", []))
    for t in tasks:
        t["mission_version"] = version
    evidence_list = []
    for ev in evidence:
        ev_copy = copy.deepcopy(ev)
        ev_copy["mission_version"] = version
        ev_copy["fingerprint"] = runtime_contracts.compute_evidence_fingerprint(ev_copy)
        evidence_list.append(ev_copy)
    return {"mission": mission, "tasks": tasks,
            "evidence": evidence_list, "approvals": copy.deepcopy(envelope.get("approvals", [])),
            "inputs": [descriptor(key) for key in inputs], "decisions": copy.deepcopy(envelope.get("decisions", [])),
            "claims": [descriptor(key) for key in claims], "artifacts": [descriptor(key) for key in artifacts]}


def task_from_plan(task, mission):
    """Canonical runtime task from the actual approved plan; no new authority."""
    return {"schema_version": "1.0.0", "task_id": task["task_id"], "mission_id": mission["mission_id"],
            "mission_version": mission["record_version"], "agent_role": task["agent_role"],
            "objective": task["objective"], "question": task["objective"],
            "authorized_context": {"brief_version": mission["brief_version"], "input_refs": task["input_refs"], "evidence_refs": []},
            "approved_decisions": [], "structured_inputs": {},
            "expected_output": {"description": task["expected_output"], "acceptance_criteria": task["acceptance_criteria"]},
            "allowed_tool_categories": task["allowed_tool_categories"], "prohibitions": ["Sin acciones externas"],
            "limits": {**task["limits"], "max_depth": 0, "max_breadth": 1},
            "escalation_rules": ["Detener ante limites o autorizacion ausente"], "category": "razonamiento",
            "dependencies": task["dependencies"], "status": task["status"], "attempt": task.get("attempt", 0)}


class VBPValidator:
    """Validador y evaluador determinista para el Venture Build Package."""

    def __init__(self) -> None:
        self.contracts_validator = runtime_contracts.RuntimeContractsValidator()

    def evaluate_vbp(
        self,
        vbp_data: dict,
        evidence_store: Optional[Dict[str, dict]] = None,
        injected_blockers: Optional[List[str]] = None,
        *, context=None,
    ) -> dict:
        """Evalua el VBP deterministamente y genera dictamen, desglose de puntaje y hallazgos."""
        evidence_store = evidence_store or {}
        injected_blockers = injected_blockers or []

        findings = []
        blockers = list(injected_blockers)
        scores: Dict[str, float] = {}

        # 1. Validar esquema general
        schema_valid, schema_errors = self.contracts_validator.validate_vbp_assembly(vbp_data, context=context)
        if not schema_valid:
            blockers.append("INTEGRIDAD_REFERENCIAL_INVALIDA")
            for err in schema_errors:
                findings.append(err["message"])

        # 2. Dimension 1: Cobertura de secciones (30%)
        sections = vbp_data.get("sections", [])
        sec_dict = {s.get("section_number"): s for s in sections if isinstance(s, dict)}

        missing_sections = []
        pending_sections = []
        for num in range(1, 19):
            sec = sec_dict.get(num)
            if not sec:
                missing_sections.append(num)
            elif sec.get("status") == "PENDIENTE":
                pending_sections.append(num)

        if missing_sections:
            scores["cobertura_secciones"] = 0.0
            blockers.append("SECCION_OBLIGATORIA_FALTANTE")
            findings.append(f"Secciones obligatorias faltantes: {missing_sections}")
        else:
            # 100 base, penalizacion por secciones pendientes justificadas
            score_cob = 100.0 - (len(pending_sections) * 10.0)
            scores["cobertura_secciones"] = max(0.0, score_cob)

        # 3. Dimension 2: Evidencia y trazabilidad (25%)
        sec_evd = sec_dict.get(5, {})
        evd_content = sec_evd.get("content", "")
        if "falsa" in evd_content.lower() or "inventada" in evd_content.lower():
            blockers.append("EVIDENCIA_FALSA_O_INEXISTENTE")
            findings.append("Deteccion de cita a fuente falsa o inexistente.")
            scores["evidencia_trazabilidad"] = 0.0
        elif evidence_store:
            scores["evidencia_trazabilidad"] = 100.0
        else:
            scores["evidencia_trazabilidad"] = 60.0
            findings.append("Sin registros de evidencia enlazados directamente en la sesion.")

        # 4. Dimension 3: Coherencia de requisitos y alcance (20%)
        sec_rf = sec_dict.get(9, {})
        sec_rnf = sec_dict.get(10, {})
        if sec_rf.get("content") and sec_rnf.get("content"):
            scores["coherencia_requisitos_alcance"] = 100.0
        else:
            scores["coherencia_requisitos_alcance"] = 50.0
            findings.append("Requisitos funcionales o no funcionales incompletos.")

        # 5. Dimension 4: Riesgos y gobernanza (15%)
        sec_risk = sec_dict.get(13, {})
        risk_content = sec_risk.get("content", "")
        if "sin mitigar" in risk_content.lower() or "critico sin tratar" in risk_content.lower():
            blockers.append("RIESGO_CRITICO_SIN_TRATAR")
            findings.append("Riesgo critico identificado sin plan de mitigacion.")
            scores["riesgos_gobernanza"] = 20.0
        else:
            scores["riesgos_gobernanza"] = 100.0

        # 6. Dimension 5: Calidad formal y manifest (10%)
        if vbp_data.get("language") == "es" and vbp_data.get("contract_version") == "1.2-aprobada" and vbp_data.get("fingerprint"):
            scores["calidad_formal_manifest"] = 100.0
        else:
            scores["calidad_formal_manifest"] = 50.0
            findings.append("Metadatos del manifest incompletos o idioma no conforme.")

        # Calculo de puntaje ponderado
        total_score = sum(scores[dim] * WEIGHTS[dim] for dim in WEIGHTS)
        total_score = round(total_score, 1)

        # Emision de dictamen
        unique_blockers = sorted(list(set(blockers)))
        if unique_blockers:
            verdict = "NO_PASA"
            reason = f"Dictamen bloqueado por: {', '.join(unique_blockers)}."
        elif total_score >= 80.0:
            verdict = "PASA"
            reason = "Comprobaciones deterministas satisfechas; no demuestra calidad real ni veracidad de una simulacion."
        elif total_score >= 70.0:
            verdict = "PASA_CON_CONDICIONES"
            reason = "El VBP es utilizable pero conserva advertencias no criticas identificadas."
        else:
            verdict = "NO_PASA"
            reason = f"Puntaje total ({total_score}) inferior al umbral minimo de 70.0."

        return {
            "verdict": verdict,
            "total_score": total_score,
            "dimension_scores": scores,
            "weights": WEIGHTS,
            "blockers": unique_blockers,
            "findings": findings,
            "reason": reason,
            "integrity": {"valid": schema_valid, "errors": schema_errors},
            "quality_scope": "Comprobaciones estructurales y referenciales; calidad real no demostrada.",
        }
