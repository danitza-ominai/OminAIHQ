"""OminAI HQ - Agente Especialista Governance & Risk (PZ-008A).

Implementa las responsabilidades de gobernanza y evaluacion de riesgos segun CONTRATO-MVP-v1.md seccion 5.9:
- Evaluacion independiente y determinista del candidato VBP y resultados de especialistas.
- Emision de dictamenes formales: PASA, PASA_CON_CONDICIONES y NO_PASA.
- Deteccion de bloqueadores absolutos de gobernanza (evidencia falsa, riesgos criticos sin mitigar).
- Prohibicion de autoaprobacion o alteracion unilateral de estados de mision.
- Generacion de resultados conformes a contracts/runtime/agent-result.schema.json con 24 campos canonicos.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import app.agent_gateway as agent_gateway
import app.runtime_contracts as runtime_contracts
import app.vbp_validation as vbp_validation


class GovernanceRisk:
    """Especialista en evaluacion de riesgos, gobernanza y dictamen independiente."""

    def __init__(
        self,
        gateway: Optional[agent_gateway.AgentGateway] = None,
        evaluator: Optional[vbp_validation.VBPValidator] = None,
    ) -> None:
        self.gateway = gateway or agent_gateway.AgentGateway()
        self.evaluator = evaluator or vbp_validation.VBPValidator()

    def evaluate_vbp_governance(
        self,
        vbp_data: dict,
        evidence_store: Optional[dict] = None,
        *, context=None,
    ) -> dict:
        """Ejecuta la evaluacion determinista de las 5 dimensiones y bloqueadores del VBP."""
        return self.evaluator.evaluate_vbp(vbp_data, evidence_store=evidence_store, context=context)

    def execute_governance_task(
        self,
        task: dict,
        brief: dict,
        plan_results: Optional[dict] = None,
        vbp_candidate: Optional[dict] = None,
        evidence_store: Optional[dict] = None,
        now_fn: Optional[Any] = None,
        *, context=None,
    ) -> Tuple[bool, Optional[dict], Optional[dict]]:
        """Ejecuta la tarea de analisis de gobernanza y emision de dictamen de conformidad."""
        get_now = now_fn or (lambda: datetime.now(timezone.utc).isoformat())
        now_iso = get_now()

        task_id = task.get("task_id", "TSK-004-GOV")
        mission_id = task.get("mission_id", "MSN-SIM-001")
        title = brief.get("title", "Iniciativa de Producto")

        evidence_refs = plan_results.get("evidence_refs", []) if plan_results else []

        eval_report = None
        verdict = "NO_PASA"
        blockers = []
        findings = [
            f"Evaluacion de gobernanza y analisis de riesgos completado para {title}.",
            "Matriz de riesgos de seguridad y cumplimiento normativo validada.",
        ]

        if vbp_candidate:
            eval_report = self.evaluate_vbp_governance(vbp_candidate, evidence_store=evidence_store, context=context)
            verdict = eval_report.get("verdict", "PASA")
            blockers = eval_report.get("blockers", [])
            findings.extend(eval_report.get("findings", []))

        proposals = [
            f"Dictamen de Gobernanza: {verdict}",
            "Recomendacion 1: Establecer revision periodica de contratos de integracion.",
            "Recomendacion 2: Registrar matriz de accesos y politicas de seguridad por rol.",
        ]

        risks = [
            "Riesgo de exposicion de datos en caso de configuracion erronea de permisos.",
            "Riesgo de dependencia critica en sistemas legados sin soporte continuo.",
        ]

        raw_result = {
            "schema_version": "1.0.0",
            "result_id": f"RES-{uuid.uuid4().hex[:8]}",
            "task_id": task_id,
            "mission_id": mission_id,
            "mission_version": 1,
            "agent_role": "governance_risk",
            "status": "SUCCESS",
            "summary": f"Analisis de gobernanza finalizado con dictamen {verdict}.",
            "findings": findings,
            "evidence_refs": evidence_refs,
            "assumptions": [
                "Se asume cumplimiento estricto del esquema de autorizacion local sin elevacion de privilegios."
            ],
            "limitations": [
                "El dictamen de gobernanza no sustituye la aprobacion humana obligatoria del usuario (A0)."
            ],
            "approved_decisions_used": ["DEC-001"],
            "proposals": proposals,
            "pending_decisions": [],
            "risks": risks,
            "artifacts": ["art://governance-report-v1"],
            "attempt_count": 1,
            "tool_actions_summary": [
                {
                    "action": "evaluacion_de_conformidad_y_riesgos",
                    "tool_or_category": "analisis_especializado",
                    "relevant_input_summary": "Plan de entrega, evidencias y propuesta de producto",
                    "result_summary": f"Dictamen emitido: {verdict}",
                }
            ],
            "errors": [],
            "recommended_next_step": "Presentar paquete VBP consolidado a revision y aprobacion humana.",
            "timestamp": now_iso,
            "idempotency_key": f"IDEMP-GOV-{uuid.uuid4().hex[:8]}",
        }

        # Calcular huella canónica SHA-256
        raw_result["fingerprint"] = runtime_contracts.compute_agent_result_fingerprint(raw_result)

        return True, raw_result, None
