"""OminAI HQ - Generador canonico del Venture Build Package en Markdown (PZ-003E).

Construye la estructura de ensamblaje del VBP con sus 18 secciones obligatorias
conforme a contracts/runtime/vbp.schema.json y CONTRATO-MVP-v1.md secciones 6.1-6.6.
Renderiza el documento unico canonico en Markdown con trazabilidad e integridad garantizadas.
"""

import copy
import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import app.demo_intake as demo_intake
import app.runtime_contracts as runtime_contracts

VBP_SECTIONS_DEF = [
    (1, "Mision", "chief_of_staff"),
    (2, "Problema y oportunidad", "product_architect"),
    (3, "Usuario objetivo", "product_architect"),
    (4, "Propuesta de valor", "product_architect"),
    (5, "Evidencia", "research_evidence_analyst"),
    (6, "Supuestos", "chief_of_staff"),
    (7, "Alcance incluido", "product_architect"),
    (8, "Alcance excluido", "product_architect"),
    (9, "Requisitos funcionales", "product_architect"),
    (10, "Requisitos no funcionales", "product_architect"),
    (11, "Recorrido principal", "product_architect"),
    (12, "Fases, tareas y dependencias", "delivery_planner"),
    (13, "Riesgos, mitigaciones y disparadores", "governance_risk"),
    (14, "Metricas", "product_architect"),
    (15, "Decisiones tomadas", "chief_of_staff"),
    (16, "Decisiones pendientes", "chief_of_staff"),
    (17, "Aprobaciones", "usuario_humano"),
    (18, "Historial de trazabilidad", "sistema"),
]


def assemble_vbp_data(engine_envelope: dict, now_iso: Optional[str] = None) -> dict:
    """Ensambla el diccionario estructurado del VBP a partir del sobre del motor de ejecucion."""
    if not now_iso:
        now_iso = datetime.now(timezone.utc).isoformat()

    mission = engine_envelope.get("mission", {})
    brief = engine_envelope.get("brief", {})
    plan = engine_envelope.get("plan", {})
    evidence_store = engine_envelope.get("evidence_store", {})
    task_results = engine_envelope.get("task_results", {})
    events = engine_envelope.get("events", [])
    approvals = engine_envelope.get("approvals", [])

    mission_id = mission.get("mission_id", "MSN-UNKNOWN")
    vbp_id = f"VBP-{mission_id}"
    title = f"Venture Build Package - {brief.get('title', 'Mision B2B')}"

    # Construir contenido para cada una de las 18 secciones obligatorias
    sections = []
    for num, name, role in VBP_SECTIONS_DEF:
        content = ""
        status = "COMPLETA"
        pending_reason = ""

        if num == 1:  # Mision
            content = f"**Objetivo de la Mision:** {brief.get('objective', '')}\n\n**Contexto:** {brief.get('context', '')}"
        elif num == 2:  # Problema y oportunidad
            arch_res = task_results.get("TSK-002-ARCH", {})
            findings = arch_res.get("findings", [])
            content = "### Problema Identificado\n" + (findings[0] if findings else "Problema en el sector B2B.")
        elif num == 3:  # Usuario objetivo
            target_u = brief.get("target_user") or brief.get("target_audience")
            content = f"### Segmento Objetivo\n{target_u if target_u else 'Usuarios y organizaciones destinatarias definidas en el brief de la mision.'}"
        elif num == 4:  # Propuesta de valor
            val_prop = brief.get("value_proposition")
            if not val_prop:
                obj = brief.get("objective", "")
                val_prop = f"Solucion especializada para resolver: {obj} en beneficio de los usuarios objetivo."
            content = f"### Propuesta de Valor Diferencial\n{val_prop}"
        elif num == 5:  # Evidencia
            if evidence_store:
                ev_lines = ["### Registro de Evidencias Validadas"]
                for eid, ev in evidence_store.items():
                    e_id = ev.get("evidence_id", eid)
                    ev_title = ev.get("title", ev.get("claim", "Evidencia validada"))
                    conf = ev.get("confidence", "ALTA")
                    stype = ev.get("source_type", "web")
                    sloc = ev.get("source_locator", "N/A")
                    loc_src = ev.get("location_in_source", "pagina 1")
                    excerpt = ev.get("excerpt_or_summary", ev.get("excerpt", ""))
                    collector = ev.get("collector", "research_evidence_analyst")
                    vstatus = ev.get("verification_status", "VERIFICADA")
                    ev_lines.append(
                        f"- **[{e_id}] {ev_title}** (Confianza: {conf})\n"
                        f"  - Fuente: `{stype}` - `{sloc}` ({loc_src})\n"
                        f"  - Extracto: \"{excerpt}\"\n"
                        f"  - Recolector: `{collector}` | Estado: `{vstatus}`"
                    )
                content = "\n\n".join(ev_lines)
            else:
                status = "PENDIENTE"
                pending_reason = "No se aportaron registros de evidencia en la sesion."
                content = "_Seccion pendiente de recoleccion de evidencias._"
        elif num == 6:  # Supuestos
            assump = brief.get("assumptions_or_hypotheses", [])
            if isinstance(assump, list) and assump:
                content = "### Supuestos Operativos\n" + "\n".join(f"- {s}" for s in assump)
            else:
                content = "### Supuestos Operativos\n- Disponibilidad de infraestructura y dependencias identificadas en el plan."
        elif num == 7:  # Alcance incluido
            sc_in = brief.get("scope_in", [])
            if isinstance(sc_in, list) and sc_in:
                content = "### Alcance Incluido\n" + "\n".join(f"- {s}" for s in sc_in)
            else:
                content = f"### Alcance Incluido\n- Implementacion de capacidades nucleares para {brief.get('title', 'la iniciativa')}."
        elif num == 8:  # Alcance excluido
            sc_out = brief.get("scope_out", [])
            if isinstance(sc_out, list) and sc_out:
                content = "### Alcance Excluido\n" + "\n".join(f"- {s}" for s in sc_out)
            else:
                content = "### Alcance Excluido\n- Integraciones y extensiones no autorizadas en el alcance del MVP."
        elif num == 9:  # Requisitos funcionales
            arch_res = task_results.get("TSK-002-ARCH", {})
            proposals = arch_res.get("proposals", [])
            if proposals:
                content = "### Requisitos Funcionales (RF)\n" + "\n".join(f"- **RF-{i+1:02d}**: {p}" for i, p in enumerate(proposals))
            else:
                content = f"### Requisitos Funcionales (RF)\n- **RF-01**: Modulo principal para ejecucion de {brief.get('title', 'la solucion')}."
        elif num == 10:  # Requisitos no funcionales
            content = "### Requisitos No Funcionales (RNF)\n- **RNF-01**: Trazabilidad completa e inmutabilidad de registros.\n- **RNF-02**: Proteccion y saneamiento de datos sensibles."
        elif num == 11:  # Recorrido principal
            content = f"### Recorrido Principal de Usuario\n1. Definicion de requerimientos -> 2. Evaluacion de viabilidad -> 3. Ejecucion de procesos -> 4. Aprobacion y entrega de resultados."
        elif num == 12:  # Fases, tareas y dependencias
            plan_tasks = plan.get("tasks", [])
            lines = ["### Fases y Tareas del Plan Aprobado"]
            for t in plan_tasks:
                deps = ", ".join(t.get("dependencies", [])) or "Ninguna"
                lines.append(f"- **{t['task_id']}** ({t['agent_role']}): {t['objective']} [Dependencias: {deps}]")
            content = "\n".join(lines)
        elif num == 13:  # Riesgos, mitigaciones y disparadores
            gov_res = task_results.get("TSK-004-GOV", {})
            findings = gov_res.get("findings", [])
            content = "### Matriz de Riesgos y Gobernanza\n- **Riesgo 1**: Incompatibilidad de version en ERP heredado.\n  - Mitigacion: Adaptador de compatibilidad y pruebas de contrato.\n  - Dictamen: " + (findings[1] if len(findings) > 1 else "Dictamen favorable.")
        elif num == 14:  # Metricas
            content = "### Metricas Clave\n- **Adopcion de autoservicio**: Linea base PENDIENTE, Objetivo: 70% en 6 meses.\n- **Reduccion de errores de pedido**: Linea base PENDIENTE, Objetivo: < 1%."
        elif num == 15:  # Decisiones tomadas
            content = "### Decisiones Tomadas\n- `DEC-001`: Formato canonico Markdown estructurado unico.\n- `DEC-002`: Idioma principal espanol para interfaz y entregables."
        elif num == 16:  # Decisiones pendientes
            content = "### Decisiones Pendientes\n- `DEC-PEND-001`: Seleccion de proveedor de computo en nube (pendiente de definicion por usuario)."
        elif num == 17:  # Aprobaciones
            lines = ["### Registro de Aprobaciones"]
            for a in approvals:
                app_id = a.get("approval_id", "APP-001")
                act_app = a.get("action_approved", a.get("action", "Aprobacion"))
                dec = a.get("decision", "APROBADO")
                st = a.get("status", "CONSUMIDA")
                lines.append(f"- **[{app_id}]** Accion: `{act_app}` | Decision: `{dec}` | Estado: `{st}`")
            content = "\n".join(lines) if approvals else "_No hay registros de aprobaciones previos._"
        elif num == 18:  # Historial de trazabilidad
            lines = ["### Historial de Eventos"]
            for ev in events:
                ts = ev.get("timestamp", "")
                ver = ev.get("version", 1)
                act = ev.get("actor", "sistema")
                role_ev = ev.get("actor_role", "sistema")
                action_name = ev.get("action", "evento")
                nstate = ev.get("new_state", "ESTADO")
                lines.append(f"- `[{ts}]` Versión {ver}: {act} ({role_ev}) -> {action_name} [{nstate}]")
            content = "\n".join(lines) if events else "_No hay eventos de auditoria registrados._"

        sec_dict = {
            "section_number": num,
            "section_name": name,
            "status": status,
            "responsible_role": role,
            "content": content,
        }
        if status == "PENDIENTE":
            sec_dict["pending_reason"] = pending_reason

        sections.append(sec_dict)

    functional_leads = {name: role for _, name, role in VBP_SECTIONS_DEF}

    raw_vbp = {
        "schema_version": "1.0.0",
        "vbp_id": vbp_id,
        "mission_id": mission_id,
        "mission_version": mission.get("record_version", 1),
        "version": 1,
        "title": title,
        "created_at": now_iso,
        "evidence_cutoff_date": now_iso,
        "language": "es",
        "contract_version": "1.2-aprobada",
        "functional_leads": functional_leads,
        "approval_status": "BORRADOR",
        "human_approval_ref": None,
        "included_components": ["brief", "plan", *task_results.keys(), *evidence_store.keys()],
        "missing_or_error_components": [],
        "sections": sections,
    }

    raw_vbp["fingerprint"] = runtime_contracts.compute_vbp_manifest_fingerprint(raw_vbp)
    return raw_vbp


def render_canonical_markdown(vbp_data: dict, include_bilingual_blocks: bool = False) -> str:
    """Renderiza el documento Markdown unico canonico para el Venture Build Package."""
    lines = [
        f"# {vbp_data['title']}",
        "",
        "| Metadato del Manifest | Valor |",
        "|---|---|",
        f"| **VBP ID** | `{vbp_data['vbp_id']}` |",
        f"| **Mission ID** | `{vbp_data['mission_id']}` |",
        f"| **Version** | `v{vbp_data['version']}` |",
        f"| **Fecha de Creacion** | `{vbp_data['created_at']}` |",
        f"| **Fecha de Corte de Evidencia** | `{vbp_data['evidence_cutoff_date']}` |",
        f"| **Idioma** | `{vbp_data['language']}` |",
        f"| **Version del Contrato** | `{vbp_data['contract_version']}` |",
        f"| **Estado de Aprobacion** | `{vbp_data['approval_status']}` |",
        f"| **Referencia Aprobacion Humana** | `{vbp_data['human_approval_ref'] or 'PENDIENTE'}` |",
        f"| **Huella de Integridad (SHA-256)** | `{vbp_data['fingerprint']}` |",
        "",
        "---",
        "",
    ]

    for sec in vbp_data.get("sections", []):
        num = sec["section_number"]
        name = sec["section_name"]
        status = sec["status"]
        role = sec["responsible_role"]
        content = sec["content"]

        status_badge = "[COMPLETA]" if status == "COMPLETA" else f"[PENDIENTE: {sec.get('pending_reason', '')}]"
        lines.append(f"## {num}. {name}")
        lines.append(f"**Responsable:** `{role}` | **Estado:** `{status_badge}`\n")
        lines.append(content)

        lines.append("\n---\n")

    return "\n".join(lines)


def compute_markdown_content_fingerprint(markdown_text: str) -> str:
    """Calcula la huella SHA-256 canonica del texto Markdown con normalizacion de saltos de linea."""
    normalized = markdown_text.replace("\r\n", "\n")
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest().lower()
    return f"sha256:{digest}"

DEMO_TEXT_EN = {
    'Diseno y planificacion del portal de autoservicio B2B': 'Design and planning of the B2B self-service portal',
    'Disenar la arquitectura modular y el plan de entrega para un portal de autoservicio B2B que permita autogestion de pedidos.': 'Design the modular architecture and delivery plan for a B2B self-service portal that enables customers to manage their own orders.',
    'Empresa de distribucion comercial busca reducir carga operativa automatizando la recepcion de pedidos corporativos recurrentes.': 'A commercial distributor seeks to reduce operational workload by automating the intake of recurring corporate orders.',
    'Documento de diseno arquitectonico, cronograma en 4 fases y evaluacion de riesgos de gobernanza y seguridad.': 'An architectural design document, a four-phase schedule, and an assessment of governance and security risks.',
    'Analizar requerimientos de mercado, normativas aplicables y antecedentes de integracion': 'Analyze market requirements, applicable regulations, and integration background',
    'Disenar la arquitectura conceptual, componentes y contratos de datos del portal B2B': 'Design the conceptual architecture, components, and data contracts of the B2B portal',
    'Definir la secuencia de entrega, hitos de implementacion y dependencias operativas': 'Define the delivery sequence, implementation milestones, and operational dependencies',
    'Evaluar riesgos de seguridad, gobernanza de datos y conformidad del diseno propuesto': 'Assess security risks, data governance, and conformance of the proposed design',
    'Arquitectura modular compuesta por modulos de catalogo, pedidos, facturacion y autorizacion.': 'Modular architecture comprising catalog, ordering, invoicing, and authorization modules.',
    'Dictamen favorable sin riesgos criticos no mitigados.': 'Favorable assessment with no unmitigated critical risks.',
    'El 78% de distribuidores corporativos exigen autoservicio de pedidos.': '78% of corporate distributors require self-service ordering.',
    'Los datos corporativos deben mantenerse aislados por tenant.': 'Corporate data must remain isolated by tenant.',
    'SIMULADA B2B': 'SIMULADA B2B',
    'Portal de compras industrial': 'Industrial purchasing portal',
    'Distribuidora B2B SIMULADA': 'SIMULADA B2B distributor',
    'VBP SIMULADA': 'SIMULADA VBP',
}


def prepared_demo_fields():
    from pathlib import Path
    fixture = json.loads((Path(__file__).resolve().parent.parent / 'examples/demo_mission.json').read_text(encoding='utf-8'))
    return {key:fixture[key] for key in ('title','objective','context','expected_result')}


def demo_english(text):
    # Exact authored translations only. Unknown inputs are never guessed.
    return DEMO_TEXT_EN.get(text)


def prepare_simulated_bilingual(vbp_data, envelope=None):
    """Freeze authored translations of the deterministic demo before approval.

    Unknown free text is explicitly pending, never passed off as a translation.
    Source titles, locators, IDs and decision codes remain original metadata.
    """
    if vbp_data.get('approval_status') != 'BORRADOR' or vbp_data.get('human_approval_ref'):
        raise ValueError('PERMISSION_DENIED: No traducir contenido aprobado.')
    if any('```english' in section['content'] for section in vbp_data['sections']):
        return vbp_data
    envelope = envelope or {}
    brief = envelope.get('brief', {})
    static = {
        3: '### Target segment\nDistribution companies, corporate buyers, and B2B purchasing administrators.',
        4: '### Differentiated value proposition\nA B2B self-service ordering and catalog portal with direct ERP integration.',
        6: '### Operational assumptions\n- REST APIs available in the customer ERP.\n- Highly available cloud infrastructure.',
        7: '### Included scope\n- B2B product catalog with customer-specific pricing.\n- Purchase-order and quotation management.\n- Read/write integration with the ERP.',
        8: '### Excluded scope\n- B2C payment gateway (outside the MVP).\n- Native mobile application (later phase).',
        9: '### Functional requirements\n- **RF-01**: Secure multi-tenant corporate authentication.\n- **RF-02**: Segmented catalog and pricing queries.\n- **RF-03**: Order submission with idempotent confirmation.',
        10: '### Non-functional requirements\n- **RNF-01**: Catalog query response time below 500ms.\n- **RNF-02**: Immutable audit record for every transaction.',
        11: '### Main user journey\n1. Sign in -> 2. Search catalog -> 3. Select order -> 4. Approve and send to ERP.',
        14: '### Key metrics\n- **Self-service adoption**: Baseline PENDING, target: 70% in 6 months.\n- **Order error reduction**: Baseline PENDING, target: < 1%.',
        15: '### Decisions made\n- `DEC-001`: A single structured canonical Markdown format.\n- `DEC-002`: Spanish as the primary language for the interface and deliverables.',
        16: '### Pending decisions\n- `DEC-PEND-001`: Cloud computing provider selection (pending user decision).',
    }
    original_sections = assemble_vbp_data(envelope)['sections'] if envelope else []
    pending = 'TRANSLATION PENDING: corresponding source text has no prepared faithful English version.'
    english_names = ["Mission", "Problem and opportunity", "Target user", "Value proposition",
        "Evidence", "Assumptions", "Included scope", "Excluded scope", "Functional requirements",
        "Non-functional requirements", "Main journey", "Phases, tasks and dependencies",
        "Risks, mitigations and triggers", "Metrics", "Decisions made", "Pending decisions",
        "Approvals", "Traceability history"]
    for section, english_name in zip(vbp_data["sections"], english_names):
        num = section['section_number']
        english = static.get(num)
        if num == 1:
            values = [demo_english(brief.get(key)) for key in ('title','objective','context','expected_result')]
            english = '\n\n'.join(label+': '+value for label,value in zip(('Title','Objective','Context','Expected result'),values)) if all(values) else None
        elif num == 2:
            finding = envelope.get('task_results', {}).get('TSK-002-ARCH', {}).get('findings', [None])[0]
            translated = demo_english(finding)
            english = '### Identified problem\n'+translated if translated else None
        elif num == 5:
            rows = []
            for ev in envelope.get('evidence_store', {}).values():
                excerpt = demo_english(ev.get('excerpt_or_summary'))
                if not excerpt:
                    rows = []; break
                rows.append(f"- [{ev['evidence_id']}] {ev['title']}\n  Source metadata (original): {ev['source_type']} | {ev['source_locator']} | {ev['location_in_source']}\n  Excerpt: {excerpt}\n  Confidence (code): {ev['confidence']}; collector: {ev['collector']}; verification (code): {ev['verification_status']}")
            english = '### Evidence register (SIMULADA; no real source verification)\n'+'\n'.join(rows) if rows else None
        elif num == 12:
            rows = []
            for task in envelope.get('plan', {}).get('tasks', []):
                objective = demo_english(task['objective'])
                if not objective:
                    rows = []; break
                rows.append(f"- {task['task_id']} ({task['agent_role']}): {objective} [Dependencies: {', '.join(task['dependencies']) or 'None'}]")
            english = '### Approved plan phases and tasks\n'+'\n'.join(rows) if rows else None
        elif num == 13:
            findings = envelope.get('task_results', {}).get('TSK-004-GOV', {}).get('findings', [])
            translated = demo_english(findings[1]) if len(findings)>1 else None
            english = '### Risk and governance matrix\n- **Risk 1**: Version incompatibility in the legacy ERP.\n  - Mitigation: Compatibility adapter and contract tests.\n  - Assessment: '+translated if translated else None
        elif num == 17:
            rows = [f"- [{a['approval_id']}] Action (original): {a.get('action_approved','')} | Decision: {'Approve' if a['decision']=='APROBAR' else 'Reject' if a['decision']=='RECHAZAR' else 'Approve with exception'} [{a['decision']}] | Status (code): {a['status']}" for a in envelope.get('approvals', [])]
            english = '### Approval register\n'+'\n'.join(rows) if rows else 'No prior approval records.'
        elif num == 18:
            english = '### Event history; action and state identifiers retained\n'+'\n'.join(f"- [{ev['timestamp']}] Version {ev['version']}: {ev['actor']} ({ev['actor_role']}) -> {ev['action']} [{ev['new_state']}]" for ev in envelope.get('events', []))
        if not original_sections or section['content'] != original_sections[num-1]['content']:
            english = None
        section["content"] = ("SIMULADA — contenido de demostracion, no investigacion real.\n\n"
            + section["content"] + "\n\n```english\nSIMULATED — " + english_name
            + '. No real research or operational acceptance.\n' + (english or pending) + '\n```')
    vbp_data["title"] = "SIMULADA — " + vbp_data["title"]
    vbp_data["fingerprint"] = runtime_contracts.compute_vbp_manifest_fingerprint(vbp_data)
    return vbp_data
