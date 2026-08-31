"""OminAI HQ - Especialistas simulados deterministas para el motor de tareas (PZ-003D SIMULADA).

Proporciona adaptadores deterministas y controlados para los 4 roles especialistas
utilizados en el recorrido simulado (Research, Architecture, Planning, Governance).
Genera sobre comun de salida conforme a contracts/runtime/agent-result.schema.json
y registros de evidencia conformes a contracts/runtime/evidence.schema.json.
"""

import copy
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple

import app.demo_intake as demo_intake
import app.runtime_contracts as runtime_contracts


class SimulatedSpecialistRunner:
    """Ejecutor de especialistas simulados con soporte para inyeccion de fallos."""

    def __init__(
        self,
        now_fn: Optional[Callable[[], datetime]] = None,
        id_generator: Optional[Callable[[str], str]] = None,
        fault_config: Optional[Dict[str, dict]] = None,
    ) -> None:
        self.now_fn = now_fn or (lambda: datetime.now(timezone.utc))
        self.id_generator = id_generator or (lambda prefix: f"{prefix}-{uuid.uuid4().hex[:8]}")
        self.fault_config = fault_config or {}
        self.validator = runtime_contracts.RuntimeContractsValidator()

    def gen_id(self, prefix: str) -> str:
        return self.id_generator(prefix)

    def execute_task(
        self,
        task: dict,
        mission: dict,
        evidence_store: Dict[str, dict],
        previous_results: Dict[str, dict],
    ) -> Tuple[dict, List[dict]]:
        """Ejecuta una tarea simulada de forma determinista y devuelve (agent_result, new_evidences)."""
        task_id = task["task_id"]
        agent_role = task["agent_role"]
        now_iso = self.now_fn().isoformat()

        # Comprobar si hay un fallo inyectado para esta tarea
        if task_id in self.fault_config:
            override = self.fault_config[task_id]
            status = override.get("status", "FAILED")
            summary = override.get("summary", f"[SIMULADA] Fallo inyectado en {task_id}")
            errors = override.get("errors", [demo_intake.make_error_payload("SYSTEM_ERROR", "Fallo simulado")])
            result_id = self.gen_id("RES")

            result_data = {
                "schema_version": "1.0.0",
                "result_id": result_id,
                "task_id": task_id,
                "mission_id": mission["mission_id"],
                "mission_version": mission["record_version"],
                "agent_role": agent_role,
                "status": status,
                "summary": summary,
                "findings": override.get("findings", []),
                "evidence_refs": override.get("evidence_refs", []),
                "assumptions": override.get("assumptions", []),
                "limitations": override.get("limitations", ["Ejecucion detenida por fallo simulado."]),
                "approved_decisions_used": override.get("approved_decisions_used", []),
                "proposals": override.get("proposals", []),
                "pending_decisions": override.get("pending_decisions", []),
                "risks": override.get("risks", ["Riesgo de bloqueo"]),
                "artifacts": override.get("artifacts", []),
                "attempt_count": override.get("attempt_count", 1),
                "tool_actions_summary": override.get("tool_actions_summary", []),
                "errors": errors,
                "recommended_next_step": override.get("recommended_next_step", "Detener o reintentar"),
                "timestamp": now_iso,
                "idempotency_key": self.gen_id("IDEMP-RES"),
            }
            result_data["fingerprint"] = runtime_contracts.compute_agent_result_fingerprint(result_data)
            self.validator.agent_result_validator.validate(result_data)
            return result_data, []

        new_evidences = []
        evidence_refs = []

        if task_id == "TSK-001-RESEARCH":
            ev1_id = self.gen_id("EVD")
            ev1 = {
                "schema_version": "1.0.0",
                "evidence_id": ev1_id,
                "mission_id": mission["mission_id"],
                "mission_version": mission["record_version"],
                "claim_id": "CLM-001-B2B-MARKET",
                "title": "[SIMULADA] Informe de Mercado de Comercio B2B 2026",
                "author_or_organization": "Analistas del Sector B2B",
                "source_type": "DOCUMENTO_LOCAL",
                "source_locator": "docs/analisis_mercado_2026.pdf",
                "location_in_source": "Pagina 4, Tabla 2",
                "publication_date": "2026-02-10T00:00:00+00:00",
                "retrieval_date": now_iso,
                "excerpt_or_summary": "El 78% de distribuidores corporativos exigen autoservicio de pedidos.",
                "collector": agent_role,
                "confidence": "ALTA",
                "confidence_justification": "Estudio cuantitativo corroborado.",
                "limitations": ["Muestra centrada en empresas medianas."],
                "contradictions": [],
                "verification_status": "VALIDADA",
            }
            ev1["fingerprint"] = runtime_contracts.compute_evidence_fingerprint(ev1)
            self.validator.evidence_validator.validate(ev1)
            new_evidences.append(ev1)
            evidence_refs.append(ev1_id)

            ev2_id = self.gen_id("EVD")
            ev2 = {
                "schema_version": "1.0.0",
                "evidence_id": ev2_id,
                "mission_id": mission["mission_id"],
                "mission_version": mission["record_version"],
                "claim_id": "CLM-002-PRIVACY",
                "title": "[SIMULADA] Marco Regulatorio de Proteccion de Datos",
                "author_or_organization": "Autoridad de Control",
                "source_type": "ENLACE_WEB",
                "source_locator": "https://normativa.example.org/privacidad-2026",
                "location_in_source": "Articulo 15",
                "publication_date": "2026-01-01T00:00:00+00:00",
                "retrieval_date": now_iso,
                "excerpt_or_summary": "Los datos corporativos deben mantenerse aislados por tenant.",
                "collector": agent_role,
                "confidence": "ALTA",
                "confidence_justification": "Normativa legal vigente.",
                "limitations": [],
                "contradictions": [],
                "verification_status": "VALIDADA",
            }
            ev2["fingerprint"] = runtime_contracts.compute_evidence_fingerprint(ev2)
            self.validator.evidence_validator.validate(ev2)
            new_evidences.append(ev2)
            evidence_refs.append(ev2_id)

            summary = "[SIMULADA] Investigacion de mercado y regulaciones completada con 2 evidencias validadas."
            findings = [
                "Demanda corporativa de autoservicio de pedidos plenamente confirmada.",
                "Requisitos estrictos de aislamiento de datos y auditoria de accesos identificados.",
            ]
            artifacts = ["ART-001-RESEARCH-REPORT"]

        elif task_id == "TSK-002-ARCH":
            summary = "[SIMULADA] Arquitectura conceptual y modelo de datos definidos."
            findings = [
                "Arquitectura modular compuesta por modulos de catalogo, pedidos, facturacion y autorizacion.",
                "Esquema relacional y contratos JSON para interoperabilidad con ERP heredados.",
            ]
            artifacts = ["ART-002-ARCH-SPEC"]
            evidence_refs = list(evidence_store.keys())

        elif task_id == "TSK-003-PLAN":
            summary = "[SIMULADA] Cronograma de 4 fases y dependencias tecnicas estructuradas."
            findings = [
                "Fase 1: Nucleo y autenticacion; Fase 2: Gestion de catalogo y pedidos; Fase 3: Integracion ERP; Fase 4: Auditoria y pase a produccion.",
                "Estimacion de plazo en 75 dias, holgura de 15 dias frente al limite de 90 dias.",
            ]
            artifacts = ["ART-003-DELIVERY-PLAN"]
            evidence_refs = list(evidence_store.keys())

        elif task_id == "TSK-004-GOV":
            summary = "[SIMULADA] Evaluacion de riesgos, gobernanza y dictamen de seguridad emitido."
            findings = [
                "Todos los controles de gobernanza, auditoria de cambios y aislamiento de datos verificados.",
                "Dictamen favorable sin riesgos criticos no mitigados.",
            ]
            artifacts = ["ART-004-GOV-REPORT"]
            evidence_refs = list(evidence_store.keys())

        else:
            summary = f"[SIMULADA] Tarea generica {task_id} completada."
            findings = [f"Hallazgo generico para {task_id}"]
            artifacts = [f"ART-{task_id}"]

        result_id = self.gen_id("RES")
        result_data = {
            "schema_version": "1.0.0",
            "result_id": result_id,
            "task_id": task_id,
            "mission_id": mission["mission_id"],
            "mission_version": mission["record_version"],
            "agent_role": agent_role,
            "status": "SUCCESS",
            "summary": summary,
            "findings": findings,
            "evidence_refs": evidence_refs,
            "assumptions": [],
            "limitations": ["Resultado generado en entorno de ensayo SIMULADA."],
            "approved_decisions_used": ["DEC-ALCANCE-PLAN"],
            "proposals": ["Proceder a la siguiente fase de consolidacion."],
            "pending_decisions": [],
            "risks": [],
            "artifacts": artifacts,
            "attempt_count": 1,
            "tool_actions_summary": [
                {
                    "action": f"ejecucion_simulada_{task_id.lower()}",
                    "tool_or_category": "analisis_especializado",
                    "relevant_input_summary": f"Contexto de brief v{mission.get('brief_version', 1)}",
                    "result_summary": summary,
                }
            ],
            "errors": [],
            "recommended_next_step": "Avanzar en el flujo secuencial",
            "timestamp": now_iso,
            "idempotency_key": self.gen_id("IDEMP-RES"),
        }
        result_data["fingerprint"] = runtime_contracts.compute_agent_result_fingerprint(result_data)
        self.validator.agent_result_validator.validate(result_data)

        return result_data, new_evidences
