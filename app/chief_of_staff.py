"""OminAI HQ - Agente Chief of Staff (PZ-004B).

Implementa las responsabilidades del Chief of Staff segun CONTRATO-MVP-v1.md seccion 5.5:
- Aclaracion de la mision y validacion de completitud (maximo 3 ciclos).
- Propuesta de plan de 4 tareas secuenciales estructuradas.
- Consolidacion de resultados de especialistas para el VBP sin autoaprobacion.
- Gestion de contexto minimo, sanitizacion y salidas en espanol.
"""

import copy
import json
from typing import Any, Dict, List, Optional, Tuple

import app.agent_gateway as agent_gateway
import app.approved_memory as approved_memory
import app.demo_intake as demo_intake

MAX_CLARIFICATION_CYCLES = 3


class ChiefOfStaff:
    """Coordinador de mision, aclaracion, planificacion y consolidacion."""

    def __init__(
        self,
        gateway: Optional[agent_gateway.AgentGateway] = None,
        memory_manager: Optional[approved_memory.ApprovedMemoryManager] = None,
    ) -> None:
        self.gateway = gateway or agent_gateway.AgentGateway()
        self.memory_manager = memory_manager

    def evaluate_and_clarify_mission(
        self,
        raw_mission: dict,
        clarification_cycle: int = 0,
    ) -> Tuple[bool, Optional[dict], Optional[List[str]], Optional[dict]]:
        """Evalua la mision humana. Si faltan datos, formula preguntas de aclaracion (max 3 ciclos).
        
        Devuelve (es_completo, brief, preguntas_aclaracion, error_payload).
        """
        # Validar ciclo maximo
        if clarification_cycle >= MAX_CLARIFICATION_CYCLES:
            err = demo_intake.make_error_payload(
                "BUDGET_EXHAUSTED",
                f"Limite de {MAX_CLARIFICATION_CYCLES} ciclos de aclaracion alcanzado sin completar la mision.",
            )
            return False, None, None, err

        title = raw_mission.get("title", "").strip()
        objective = raw_mission.get("objective", "").strip()
        context = raw_mission.get("context", "").strip()
        expected_result = raw_mission.get("expected_result", "").strip()
        user_id = raw_mission.get("user_id", "USR-DEMO-001")

        # Comprobar completitud
        missing_fields = []
        if not title:
            missing_fields.append("title")
        if not objective:
            missing_fields.append("objective")
        if not context:
            missing_fields.append("context")
        if not expected_result:
            missing_fields.append("expected_result")

        if missing_fields:
            questions = [
                f"Por favor detalle o aclare el campo obligatorio '{field}' para continuar con la planificacion."
                for field in missing_fields
            ]
            return False, None, questions, None

        # Si esta completa, construir brief estructurado
        brief = {
            "simulation_status": "SIMULADA",
            "user_id": user_id,
            "title": f"[SIMULADA] {title}" if not title.startswith("[SIMULADA]") else title,
            "objective": objective,
            "context": context,
            "expected_result": expected_result,
            "constraints": raw_mission.get("constraints", ["Presupuesto maximo USD 25", "Plazo 90 dias"]),
            "assumptions": raw_mission.get("assumptions", []),
            "pending_decisions": raw_mission.get("pending_decisions", []),
        }

        return True, brief, None, None

    def propose_plan(
        self,
        mission_id: str,
        brief: dict,
        plan_version: int = 1,
        *, context=None,
    ) -> Tuple[bool, Optional[dict], Optional[dict]]:
        """Propone el plan estructurado de cuatro tareas secuenciales a partir del brief validado."""
        tasks = [
            {
                "task_id": "TSK-001-RESEARCH",
                "objective": "Investigar mercado, fuentes normativas y antecedentes de integracion",
                "agent_role": "research_evidence_analyst",
                "input_refs": ["brief"],
                "expected_output": "Informe de investigacion con evidencias validadas",
                "acceptance_criteria": [
                    "Identificar al menos 2 fuentes verificadas",
                    "Documentar limitaciones y contradicciones",
                ],
                "dependencies": [],
                "allowed_tool_categories": [
                    "recuperacion_interna_solo_lectura",
                    "investigacion_externa_solo_lectura",
                ],
                "limits": {
                    "max_attempts": 2,
                    "max_seconds": 300,
                    "max_budget_usd": 0,
                    "max_depth": 0,
                    "max_breadth": 1,
                },
                "status": "PENDIENTE",
                "simulation_status": "SIMULADA",
            },
            {
                "task_id": "TSK-002-ARCH",
                "objective": "Disenar la arquitectura conceptual, componentes y contratos de datos",
                "agent_role": "product_architect",
                "input_refs": ["brief", "TSK-001-RESEARCH"],
                "expected_output": "Especificacion tecnica de arquitectura y modelo de datos",
                "acceptance_criteria": [
                    "Definir modulos y limites de integracion",
                    "Especificar esquema de datos conceptual",
                ],
                "dependencies": ["TSK-001-RESEARCH"],
                "allowed_tool_categories": [
                    "recuperacion_interna_solo_lectura",
                    "transformacion_determinista",
                ],
                "limits": {
                    "max_attempts": 2,
                    "max_seconds": 300,
                    "max_budget_usd": 0,
                    "max_depth": 0,
                    "max_breadth": 1,
                },
                "status": "PENDIENTE",
                "simulation_status": "SIMULADA",
            },
            {
                "task_id": "TSK-003-PLAN",
                "objective": "Definir la secuencia de entrega, hitos de implementacion y dependencias",
                "agent_role": "delivery_planner",
                "input_refs": ["brief", "TSK-002-ARCH"],
                "expected_output": "Plan de fases y cronograma con estimaciones de esfuerzo",
                "acceptance_criteria": [
                    "Estructurar cronograma en 4 fases",
                    "Validar camino critico y holguras",
                ],
                "dependencies": ["TSK-002-ARCH"],
                "allowed_tool_categories": [
                    "transformacion_determinista",
                    "analisis_especializado",
                ],
                "limits": {
                    "max_attempts": 2,
                    "max_seconds": 300,
                    "max_budget_usd": 0,
                    "max_depth": 0,
                    "max_breadth": 1,
                },
                "status": "PENDIENTE",
                "simulation_status": "SIMULADA",
            },
            {
                "task_id": "TSK-004-GOV",
                "objective": "Evaluar riesgos de seguridad, gobernanza de datos y dictamen de conformidad",
                "agent_role": "governance_risk",
                "input_refs": ["brief", "TSK-003-PLAN"],
                "expected_output": "Matriz de riesgos de gobernanza y dictamen de conformidad",
                "acceptance_criteria": [
                    "Evaluar conformidad contra politicas",
                    "Emitir dictamen de gobernanza",
                ],
                "dependencies": ["TSK-003-PLAN"],
                "allowed_tool_categories": [
                    "analisis_especializado",
                    "recuperacion_interna_solo_lectura",
                ],
                "limits": {
                    "max_attempts": 2,
                    "max_seconds": 300,
                    "max_budget_usd": 0,
                    "max_depth": 0,
                    "max_breadth": 1,
                },
                "status": "PENDIENTE",
                "simulation_status": "SIMULADA",
            },
        ]

        risks = [
            "Retraso en la definicion de interfaces con sistemas heredados",
            "Ajustes requeridos en politicas corporativas de acceso",
        ]

        plan = {
            "simulation_status": "SIMULADA",
            "mission_id": mission_id,
            "brief_version": 1,
            "plan_version": plan_version,
            "title": f"Plan v{plan_version} para {brief.get('title', 'Mision')}",
            "tasks": tasks,
            "risks": risks,
        }

        if self.memory_manager is not None and context is not None:
            memories = self.memory_manager.query_memories_for_role("chief_of_staff", context=context)
            plan["memory_refs"] = [{"memory_id": mem["memory_id"], "version": mem["version"]} for mem in memories]

        return True, plan, None
