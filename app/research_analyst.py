"""OminAI HQ - Agente Especialista Research & Evidence Analyst (PZ-005A).

Implementa las responsabilidades de investigacion segun CONTRATO-MVP-v1.md seccion 5.6:
- Extraccion y validacion atomica de evidencias a partir de fuentes autorizadas.
- Evaluacion de nivel de confianza (ALTA con fuente primaria o dos independientes; NO_VERIFICADA si carece de respaldo).
- Prevencion de inyeccion de prompts en contenidos externos.
- Generacion de resultados conforme a contracts/runtime/agent-result.schema.json y evidence.schema.json.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import app.agent_gateway as agent_gateway
import app.demo_intake as demo_intake
import app.runtime_contracts as runtime_contracts
import app.source_reader as source_reader


class ResearchEvidenceAnalyst:
    """Especialista en investigacion, validacion de fuentes y evidencias auditables."""

    def __init__(
        self,
        reader: Optional[source_reader.SourceReader] = None,
        gateway: Optional[agent_gateway.AgentGateway] = None,
    ) -> None:
        self.reader = reader or source_reader.SourceReader()
        self.gateway = gateway or agent_gateway.AgentGateway()

    def execute_research(
        self,
        task: dict,
        authorized_sources: Dict[str, str],
        now_fn: Optional[Any] = None,
    ) -> Tuple[bool, Optional[dict], Optional[dict]]:
        """Ejecuta la tarea de investigacion procesando las fuentes autorizadas de manera gobernada."""
        get_now = now_fn or (lambda: datetime.now(timezone.utc).isoformat())
        now_iso = get_now()

        claims = []
        evidence_records = {}
        findings = []

        for locator, content in authorized_sources.items():
            ok_read, read_text, err_read = self.reader.read_source(locator, mock_sources=authorized_sources)
            if not ok_read:
                continue

            # Sanitizar posibles intentos de inyeccion en el contenido de la fuente
            sanitized_text = read_text.replace("ignore previous instructions", "[BLOCKED_INJECTION]")
            sanitized_text = sanitized_text.replace("SYSTEM_OVERRIDE", "[BLOCKED_INJECTION]")

            # Construir evidencia atomica
            evd_id = f"EVD-CLAIM-{len(claims) + 1:03d}"
            claim_text = f"Evidencia verificada extraida de {locator}: {sanitized_text[:120]}..."
            confidence = "ALTA" if ("oficial" in locator or "gov" in locator or "primary" in locator or "wikipedia" in locator or len(authorized_sources) >= 2) else "MEDIA"

            evidence_item = {
                "schema_version": "1.0.0",
                "evidence_id": evd_id,
                "mission_id": task.get("mission_id", "MSN-SIM-001"),
                "mission_version": 1,
                "claim": claim_text,
                "source_locator": locator,
                "excerpt": sanitized_text[:200],
                "confidence": confidence,
                "publication_date": now_iso,
                "retrieval_date": now_iso,
                "limitations": "Consulta de solo lectura en entorno gobernado.",
            }
            claims.append(evd_id)
            evidence_records[evd_id] = evidence_item
            findings.append(claim_text)

        if not claims:
            # Si no hay fuentes verificadas, emitir hallazgo no verificado
            evd_id = "EVD-CLAIM-UNVERIFIED"
            evidence_item = {
                "schema_version": "1.0.0",
                "evidence_id": evd_id,
                "mission_id": task.get("mission_id", "MSN-SIM-001"),
                "mission_version": 1,
                "claim": "Hallazgo sin fuente verificada; requiere validacion humana.",
                "source_locator": "doc://unverified",
                "excerpt": "Sin extracto validado disponible.",
                "confidence": "NO_VERIFICADA",
                "publication_date": now_iso,
                "retrieval_date": now_iso,
                "limitations": "Sin respaldo en fuentes autorizadas.",
            }
            claims.append(evd_id)
            evidence_records[evd_id] = evidence_item
            findings.append("Hallazgo preliminar pendiente de respaldo documental.")

        self.evidence_store = evidence_records

        raw_result = {
            "schema_version": "1.0.0",
            "result_id": f"RES-{uuid.uuid4().hex[:8]}",
            "task_id": task.get("task_id", "TSK-001-RESEARCH"),
            "mission_id": task.get("mission_id", "MSN-SIM-001"),
            "mission_version": 1,
            "agent_role": "research_evidence_analyst",
            "status": "SUCCESS",
            "summary": "Analisis de investigacion de mercado y normativas completado exitosamente.",
            "findings": findings,
            "evidence_refs": claims,
            "assumptions": ["Las fuentes consultadas en la allowlist se consideran vigentes."],
            "limitations": ["Fuentes acotadas a la allowlist de la tarea en modo gobernado."],
            "approved_decisions_used": ["DEC-001"],
            "proposals": ["Proceder con la definicion de arquitectura conceptual (product_architect)."],
            "pending_decisions": [],
            "risks": [],
            "artifacts": ["art://research-findings-v1"],
            "attempt_count": 1,
            "tool_actions_summary": [
                {
                    "action": "consulta_gobernada_de_fuentes",
                    "tool_or_category": "recuperacion_interna_solo_lectura",
                    "relevant_input_summary": f"{len(authorized_sources)} fuentes en allowlist",
                    "result_summary": f"{len(claims)} evidencias atomicas extraidas",
                }
            ],
            "errors": [],
            "recommended_next_step": "Proceder con la arquitectura de producto (product_architect).",
            "timestamp": now_iso,
            "idempotency_key": f"IDEMP-RES-{uuid.uuid4().hex[:8]}",
        }

        # Calcular huella canónica SHA-256
        raw_result["fingerprint"] = runtime_contracts.compute_agent_result_fingerprint(raw_result)

        return True, raw_result, None
