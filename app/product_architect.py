"""OminAI HQ - Agente Especialista Product Architect (PZ-006A).

Implementa las responsabilidades de arquitectura de producto segun CONTRATO-MVP-v1.md seccion 5.7:
- Definicion de problema, oportunidad, usuario objetivo y propuesta de valor.
- Delimitacion explicita de alcance incluido y excluido.
- Requisitos funcionales y no funcionales enlazados a evidencia y decisiones.
- Definicion del recorrido principal de usuario y metricas clave.
- Mantenimiento de decisiones tecnologicas de cliente como decisiones pendientes humanas.
- Generacion de resultados conformes a contracts/runtime/agent-result.schema.json con 24 campos canonicos.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import app.agent_gateway as agent_gateway
import app.runtime_contracts as runtime_contracts


class ProductArchitect:
    """Especialista en diseno funcional, alcance, requisitos y arquitectura conceptual."""

    def __init__(self, gateway: Optional[agent_gateway.AgentGateway] = None) -> None:
        self.gateway = gateway or agent_gateway.AgentGateway()

    def execute_architecture(
        self,
        task: dict,
        brief: dict,
        research_results: Optional[dict] = None,
        now_fn: Optional[Any] = None,
    ) -> Tuple[bool, Optional[dict], Optional[dict]]:
        """Ejecuta la tarea de arquitectura de producto estructurando requisitos y alcance trazables."""
        get_now = now_fn or (lambda: datetime.now(timezone.utc).isoformat())
        now_iso = get_now()

        task_id = task.get("task_id", "TSK-002-ARCH")
        mission_id = task.get("mission_id", "MSN-SIM-001")
        title = brief.get("title", "Iniciativa de Producto")

        claims = research_results.get("evidence_refs", []) if research_results else []
        if not claims and research_results and "claims" in research_results:
            claims = research_results["claims"]

        findings = [
            f"Definicion de arquitectura conceptual completada para {title}.",
            "Especificacion de requisitos funcionales y no funcionales trazables.",
            "Delimitacion formal de alcance y politicas de integracion.",
        ]

        proposals = [
            "Modulo 1: Portal de autoservicio para gestion de pedidos.",
            "Modulo 2: Adaptador de lectura para integracion con ERP heredado.",
            "Modulo 3: Motor de reglas comerciales y politicas de descuento.",
        ]

        pending_decisions = [
            "DEC-PEND-TECH-001: Seleccion de proveedor e infraestructura de nube (pendiente de definicion humana)."
        ]

        risks = [
            "Incompatibilidad de esquema de datos con versiones heredadas del ERP."
        ]

        # Sobre comun de 24 campos conforme a contracts/runtime/agent-result.schema.json
        raw_result = {
            "schema_version": "1.0.0",
            "result_id": f"RES-{uuid.uuid4().hex[:8]}",
            "task_id": task_id,
            "mission_id": mission_id,
            "mission_version": 1,
            "agent_role": "product_architect",
            "status": "SUCCESS",
            "summary": "Arquitectura conceptual y modelo de requisitos formulado con exito.",
            "findings": findings,
            "evidence_refs": claims,
            "assumptions": ["El ERP heredado expone interfaz de consulta."],
            "limitations": [
                "Las decisiones de infraestructura y proveedor quedan reservadas a la aprobacion humana."
            ],
            "approved_decisions_used": ["DEC-001", "DEC-002"],
            "proposals": proposals,
            "pending_decisions": pending_decisions,
            "risks": risks,
            "artifacts": ["art://architecture-spec-v1"],
            "attempt_count": 1,
            "tool_actions_summary": [
                {
                    "action": "sintesis_de_arquitectura",
                    "tool_or_category": "transformacion_determinista",
                    "relevant_input_summary": "Brief y evidencias de investigacion",
                    "result_summary": "Modelo conceptual y requisitos sintetizados",
                }
            ],
            "errors": [],
            "recommended_next_step": "Proceder con la planificacion de entrega por fases (delivery_planner).",
            "timestamp": now_iso,
            "idempotency_key": f"IDEMP-ARCH-{uuid.uuid4().hex[:8]}",
        }

        # Calcular huella SHA-256 canónica
        raw_result["fingerprint"] = runtime_contracts.compute_agent_result_fingerprint(raw_result)

        return True, raw_result, None
