# Informe de construccion inicial - PZ-003A

**Autor del informe original:** Antigravity  
**Archivo documental conservado:** 30 de agosto de 2026  
**Fuente:** `C:\Users\Nivez\.codex\attachments\d7f343ec-60c8-46ff-867a-185ed80c9083\pasted-text.txt`  
**SHA-256 del adjunto original:** `64D2587BBAAFFD779CAC18E4B0CDFF208070627951449B6BB09201A7A51EEAD7`

## Contexto de archivo y reconciliacion

Este documento conserva el contenido del informe inicial aportado por el usuario; no sustituye el resultado posterior de la correccion 1 ni la aceptacion humana.

- Las 27 pruebas y los hashes de los archivos nuevos corresponden a la construccion inicial. Tras la correccion 1, la suite tiene 49 pruebas aprobadas.
- La afirmacion original de cobertura exhaustiva fue revisada: se encontraron defectos y pruebas faltantes, corregidos despues con autorizacion humana.
- Errata del original: el tamano declarado de `app/demo_intake.py` es 18.367 bytes. La captura independiente anterior a la correccion registro 32.521 bytes y el mismo SHA-256 publicado. Tras la correccion mide 37.011 bytes; no se reescribe la cifra historica del informe.
- El manifiesto inicial/final de Antigravity es evidencia aportada por el constructor. La linea base independiente de Chipi corresponde al momento anterior a la correccion 1, no al inicio de construccion.
- La aceptacion humana posterior se registra en la [ficha, seccion 16](FICHA-PZ-003A-ENTRADA-Y-PLAN-CONTROLADO.md#16-cierre-documental-y-aceptacion-humana-final).
- El cuerpo original conserva su lenguaje y sus limitaciones historicas; la terminologia vigente es aprobacion humana o del usuario.

## Informe original recibido

````text
Informe de Construcción Inicial: PZ-003A (Entrada de Misión y Plan Controlado - SIMULADA)
Pieza: PZ-003A
Constructor inicial: Antigravity
Estado: CONSTRUIDA_PENDIENTE_DE_INSPECCION
Fecha: 30 de agosto de 2026
Contrato rector: 
CONTRATO-MVP-v1.md
 (v1.2-aprobada)
Ficha de referencia: 
FICHA-PZ-003A-ENTRADA-Y-PLAN-CONTROLADO.md
 (Aprobación humana registrada en Sección 14)

1. Verificación de Entorno y Dependencias
No se realizaron instalaciones, actualizaciones ni uso de red. Se utilizó la instalación compatible ya disponible en el entorno local:

Python: 3.11.15
jsonschema: 4.26.0 (cumple con el rango requerido >=4.18,<5)
2. Alcance Exacto de Archivos
Archivos Creados Exclusivamente (3)
app/demo_intake.py
: Módulo determinista de entrada, evaluación de brief, validación de plantilla y propuesta de plan SIMULADA. Entrada CLI sin efectos al importar.
examples/demo_mission.json
: Fixture ficticia y saneada en español con brief completo y plantilla preescrita de 4 tareas etiquetadas SIMULADA.
tests/test_demo_intake.py
: Suite de pruebas unitarias y de integración que cubre exhaustivamente los criterios CA-01 a CA-11.
Archivos Modificados Exclusivamente (2)
README.md
: Incorporación de la documentación del comando de ensayo python -B -m app.demo_intake, sus límites y árbol de estructura actualizado, conservando el arranque base.
pyproject.toml
: Adición única del extra opcional demo = ["jsonschema>=4.18,<5"] sin alterar dependencies = [] ni el extra test.
Archivos Intactos y No Modificados
Los 13 archivos nucleares de contracts/core/ (schemas, state-machine.json, README y ejemplos).
Los 2 archivos existentes de app/ (
__init__.py
, 
__main__.py
).
Las 2 pruebas existentes (
tests/test_contracts.py
, 
tests/test_smoke.py
).
.gitignore
, reglas del equipo y documentación histórica.
3. Salidas Completas de Ejecución
3.1 Verificación de Versiones
text


Python 3.11.15
jsonschema: 4.26.0
3.2 Comando Base: python -B -m app
json


{
  "application": "OminAI HQ",
  "status": "STRUCTURE_READY",
  "implemented_capabilities": []
}
Código de salida: 0

3.3 Comando de Ensayo: python -B -m app.demo_intake
json


{
  "simulation_status": "SIMULADA",
  "mission": {
    "schema_version": "1.0.0",
    "mission_id": "MSN-SIM-a0477719",
    "user_id": "USR-DEMO-001",
    "title": "[SIMULADA] Diseno y planificacion del portal de autoservicio B2B",
    "brief_version": 1,
    "current_state": "PLAN_EN_REVISION",
    "resumable_state": null,
    "active_task": null,
    "counters": {
      "clarification_cycles": 0,
      "task_reasoning_attempts": 0,
      "transient_retries": 0,
      "vbp_correction_rounds": 0,
      "agent_requests": 0
    },
    "limits": {
      "max_clarification_cycles": 3,
      "max_task_reasoning_attempts": 2,
      "max_transient_retries": 1,
      "max_vbp_correction_rounds": 2,
      "max_concurrent_missions": 1,
      "max_concurrent_agents": 1,
      "max_recursive_decomposition": 0,
      "max_agent_execution_seconds": 300,
      "max_mission_seconds": 1200,
      "max_agent_requests_per_mission": 15,
      "max_budget_usd": 25
    },
    "approval_refs": [],
    "last_checkpoint_id": null,
    "created_at": "2026-08-30T22:33:21.746481+00:00",
    "updated_at": "2026-08-30T22:33:21.746481+00:00",
    "record_version": 3
  },
  "brief": {
    "simulation_status": "SIMULADA",
    "user_id": "USR-DEMO-001",
    "title": "Diseno y planificacion del portal de autoservicio B2B",
    "objective": "Disenar la arquitectura modular y el plan de entrega para un portal de autoservicio B2B que permita autogestion de pedidos.",
    "context": "Empresa de distribucion comercial busca reducir carga operativa automatizando la recepcion de pedidos corporativos recurrentes.",
    "expected_result": "Documento de diseno arquitectonico, cronograma en 4 fases y evaluacion de riesgos de gobernanza y seguridad.",
    "constraints": [
      "Plazo maximo de ejecucion del proyecto estimado en 90 dias",
      "Conformidad estricta con normativa de proteccion de datos y privacidad",
      "Presupuesto de ejecucion acotado a limites de la organizacion"
    ],
    "assumptions": [],
    "pending_decisions": []
  },
  "plan": {
    "simulation_status": "SIMULADA",
    "mission_id": "MSN-SIM-a0477719",
    "brief_version": 1,
    "plan_version": 1,
    "title": "[SIMULADA] Plan de desarrollo de portal de autoservicio B2B",
    "tasks": [
      {
        "task_id": "TSK-001-RESEARCH",
        "objective": "Analizar requerimientos de mercado, normativas aplicables y antecedentes de integracion",
        "agent_role": "research_evidence_analyst",
        "input_refs": [
          "brief"
        ],
        "expected_output": "Informe sintetizado de investigacion de mercado y requerimientos normativos",
        "acceptance_criteria": [
          "Identificar al menos 3 referencias del sector",
          "Documentar requisitos regulatorios y de privacidad aplicables"
        ],
        "dependencies": [],
        "allowed_tool_categories": [],
        "limits": {
          "max_attempts": 2,
          "max_seconds": 300,
          "max_budget_usd": 0
        },
        "status": "PENDIENTE",
        "simulation_status": "SIMULADA"
      },
      {
        "task_id": "TSK-002-ARCH",
        "objective": "Disenar la arquitectura conceptual, componentes y contratos de datos del portal B2B",
        "agent_role": "product_architect",
        "input_refs": [
          "brief"
        ],
        "expected_output": "Especificacion tecnica de arquitectura y modelo de datos conceptual",
        "acceptance_criteria": [
          "Definir componentes funcionales y sus limites",
          "Especificar interfaces y esquema de datos para pedidos"
        ],
        "dependencies": [
          "TSK-001-RESEARCH"
        ],
        "allowed_tool_categories": [],
        "limits": {
          "max_attempts": 2,
          "max_seconds": 300,
          "max_budget_usd": 0
        },
        "status": "PENDIENTE",
        "simulation_status": "SIMULADA"
      },
      {
        "task_id": "TSK-003-PLAN",
        "objective": "Definir la secuencia de entrega, hitos de implementacion y dependencias operativas",
        "agent_role": "delivery_planner",
        "input_refs": [
          "brief"
        ],
        "expected_output": "Plan de entrega estructurado en 4 fases con criterios de aceptacion por hito",
        "acceptance_criteria": [
          "Secuenciar paquetes de trabajo en orden logico de dependencias",
          "Asignar estimaciones de tiempo y condiciones de aceptacion"
        ],
        "dependencies": [
          "TSK-002-ARCH"
        ],
        "allowed_tool_categories": [],
        "limits": {
          "max_attempts": 2,
          "max_seconds": 300,
          "max_budget_usd": 0
        },
        "status": "PENDIENTE",
        "simulation_status": "SIMULADA"
      },
      {
        "task_id": "TSK-004-GOV",
        "objective": "Evaluar riesgos de seguridad, gobernanza de datos y conformidad del diseno propuesto",
        "agent_role": "governance_risk",
        "input_refs": [
          "brief"
        ],
        "expected_output": "Matriz de riesgos de gobernanza, controles de seguridad y recomendaciones de mitigacion",
        "acceptance_criteria": [
          "Evaluar riesgos de seguridad y cumplimiento del plan propuesto",
          "Emitir dictamen de conformidad de gobernanza"
        ],
        "dependencies": [
          "TSK-003-PLAN"
        ],
        "allowed_tool_categories": [],
        "limits": {
          "max_attempts": 2,
          "max_seconds": 300,
          "max_budget_usd": 0
        },
        "status": "PENDIENTE",
        "simulation_status": "SIMULADA"
      }
    ],
    "risks": [
      "Retraso en la definicion de interfaces con sistemas ERP heredados",
      "Ajustes requeridos en politicas corporativas de control de acceso"
    ]
  },
  "events": [
    {
      "schema_version": "1.0.0",
      "event_id": "EVT-CREATION-7a2293e4",
      "mission_id": "MSN-SIM-a0477719",
      "task_id": null,
      "actor": "sistema",
      "actor_role": "sistema",
      "action": "creacion_de_mision",
      "timestamp": "2026-08-30T22:33:21.746481+00:00",
      "version": 1,
      "previous_state": null,
      "new_state": "BORRADOR",
      "tool_or_category": null,
      "source_or_artifact": null,
      "result_summary": "Mision creada en estado BORRADOR (SIMULADA)",
      "typed_error": null,
      "attempt": 0,
      "budget_consumed": null,
      "related_approval_id": null,
      "idempotency_key": "IDEMP-CREATION-b02714c0"
    },
    {
      "schema_version": "1.0.0",
      "event_id": "EVT-READY-33db9644",
      "mission_id": "MSN-SIM-a0477719",
      "task_id": null,
      "actor": "chief_of_staff_simulado",
      "actor_role": "chief_of_staff",
      "action": "validacion_de_brief",
      "timestamp": "2026-08-30T22:33:21.746481+00:00",
      "version": 2,
      "previous_state": "BORRADOR",
      "new_state": "LISTA_PARA_PLAN",
      "tool_or_category": null,
      "source_or_artifact": null,
      "result_summary": "Brief completo validado por Chief of Staff simulado (SIMULADA)",
      "typed_error": null,
      "attempt": 0,
      "budget_consumed": null,
      "related_approval_id": null,
      "idempotency_key": "IDEMP-READY-26e2a1f2"
    },
    {
      "schema_version": "1.0.0",
      "event_id": "EVT-PLAN-REVIEW-7f225223",
      "mission_id": "MSN-SIM-a0477719",
      "task_id": null,
      "actor": "chief_of_staff_simulado",
      "actor_role": "chief_of_staff",
      "action": "presentacion_de_plan",
      "timestamp": "2026-08-30T22:33:21.746481+00:00",
      "version": 3,
      "previous_state": "LISTA_PARA_PLAN",
      "new_state": "PLAN_EN_REVISION",
      "tool_or_category": null,
      "source_or_artifact": null,
      "result_summary": "Plan SIMULADA presentado para revision. No aprobado y no ejecutado.",
      "typed_error": null,
      "attempt": 0,
      "budget_consumed": null,
      "related_approval_id": null,
      "idempotency_key": "IDEMP-PLAN-REVIEW-0326d82d"
    }
  ],
  "pending_fields": [],
  "errors": [],
  "next_action": "Plan SIMULADA presentado para revision. No aprobado y no ejecutado."
}
Código de salida: 0

3.4 Suite Completa: python -B -m unittest discover -s tests -v
text


test_01_json_files_count_and_parsing (test_contracts.TestContractsCore.test_01_json_files_count_and_parsing)
Verifica que existan exactamente 12 archivos JSON y 1 README en contracts/core y que todos parseen. ... ok
test_02_schemas_metadata_and_metavalidation (test_contracts.TestContractsCore.test_02_schemas_metadata_and_metavalidation)
Verifica que los 5 schemas declaran Draft 2020-12, $id, title, version y pasan metavalidacion. ... ok
test_03_positive_examples_validation (test_contracts.TestContractsCore.test_03_positive_examples_validation)
Verifica que todos los ejemplos positivos sean aceptados por sus respectivos schemas y reglas. ... ok
test_04_negative_examples_mission_and_checkpoint_rejected (test_contracts.TestContractsCore.test_04_negative_examples_mission_and_checkpoint_rejected)
Verifica que todos los casos de mission.invalid.json sean rechazados por sus schemas. ... ok
test_05_negative_examples_approval_rejected (test_contracts.TestContractsCore.test_05_negative_examples_approval_rejected)
Verifica que todos los casos de approval.invalid.json sean rechazados por approval.schema.json. ... ok
test_06_negative_examples_transitions_rejected (test_contracts.TestContractsCore.test_06_negative_examples_transitions_rejected)
Verifica que los casos negativos de transitions.invalid.json sean rechazados segun su tipo. ... ok
test_07_state_machine_counts (test_contracts.TestContractsCore.test_07_state_machine_counts)
Verifica conteo exacto de 15 estados de mision, 8 de tarea, 76 transiciones de mision y 13 de tarea. ... ok
test_08_table_4_2_representation_and_terminal_invariants (test_contracts.TestContractsCore.test_08_table_4_2_representation_and_terminal_invariants)
Verifica que las 16 filas de 4.2 estan representadas y los terminales no tienen transiciones salientes. ... ok
test_09_reserved_routes_and_human_evidence (test_contracts.TestContractsCore.test_09_reserved_routes_and_human_evidence)
Verifica que rutas directas reservadas exigen solo_usuario_humano o accion determinista. ... ok
test_10_approval_lifecycle_and_idempotency (test_contracts.TestContractsCore.test_10_approval_lifecycle_and_idempotency)
Verifica el ciclo de vida de aprobaciones e invariantes de idempotencia. ... ok
test_11_referential_integrity_rules (test_contracts.TestContractsCore.test_11_referential_integrity_rules)
Verifica la presencia y definicion de RI-001, RI-002 y RI-003. ... ok
test_12_exhaustive_error_matrix_1440_combinations (test_contracts.TestContractsCore.test_12_exhaustive_error_matrix_1440_combinations)
Verifica exhaustivamente 1440 combinaciones de error y acepta exactamente 10. ... ok
test_13_rejection_of_chain_of_thought_fields (test_contracts.TestContractsCore.test_13_rejection_of_chain_of_thought_fields)
Verifica que campos de razonamiento interno / Chain-of-Thought sean rechazados en todos los schemas. ... ok
test_14_absence_of_forbidden_terms_in_contracts_core (test_contracts.TestContractsCore.test_14_absence_of_forbidden_terms_in_contracts_core)
Verifica que no aparezcan terminos prohibidos dentro de los trece archivos de contracts/core. ... ok
test_ca01_complete_case_flow_and_events (test_demo_intake.TestDemoIntake.test_ca01_complete_case_flow_and_events)
CA-01: Caso completo produce BORRADOR, LISTA_PARA_PLAN y PLAN_EN_REVISION en orden con 3 eventos. ... ok
test_ca02_missing_fields_produce_clarification_required (test_demo_intake.TestDemoIntake.test_ca02_missing_fields_produce_clarification_required)
CA-02: Cada campo formal faltante produce ACLARACION_REQUERIDA, identifica el campo y no genera plan. ... ok
test_ca03_assumptions_or_decisions_prevent_lista_para_plan (test_demo_intake.TestDemoIntake.test_ca03_assumptions_or_decisions_prevent_lista_para_plan)
CA-03: Supuestos o decisiones pendientes impiden LISTA_PARA_PLAN; no se fabrican aprobaciones. ... ok
test_ca04_invalid_inputs_and_exceeded_limits_rejected (test_demo_intake.TestDemoIntake.test_ca04_invalid_inputs_and_exceeded_limits_rejected)
CA-04: JSON invalido, tipo incorrecto, claves desconocidas, limites excedidos y fixture ausente se rechazan. ... ok
test_ca05_schemas_validation_and_invalid_date_format_check (test_demo_intake.TestDemoIntake.test_ca05_schemas_validation_and_invalid_date_format_check)
CA-05: Mision y eventos reales pasan schemas; una fecha invalida de prueba es rechazada. ... ok
test_ca06_plan_template_structural_validation (test_demo_intake.TestDemoIntake.test_ca06_plan_template_structural_validation)
CA-06: Plantilla con campo obligatorio ausente, ID duplicado, rol ajeno, dependencia ausente/propia/circular no alcanza PLAN_EN_REVISION. ... ok
test_ca07_immutability_and_state_isolation (test_demo_intake.TestDemoIntake.test_ca07_immutability_and_state_isolation)
CA-07: La copia de la plantilla no modifica la entrada; ejecuciones independientes no comparten estado. ... ok
test_ca08_simulada_tags_and_no_real_agents (test_demo_intake.TestDemoIntake.test_ca08_simulada_tags_and_no_real_agents)
CA-08: Etiqueta SIMULADA visible en sobre, titulo, plan, tareas y eventos simulados. ... ok
test_ca09_no_forced_reserved_states (test_demo_intake.TestDemoIntake.test_ca09_no_forced_reserved_states)
CA-09: Ninguna entrada puede forzar AUTORIZADA_PARA_EJECUTAR, EN_EJECUCION, VBP_APROBADO o FINALIZADA. ... ok
test_ca10_no_side_effects_on_import_or_execution (test_demo_intake.TestDemoIntake.test_ca10_no_side_effects_on_import_or_execution)
CA-10: Importacion limpia, sin llamadas de red, modelos ni subprocesos. ... ok
test_ca11_cli_execution_and_exit_codes (test_demo_intake.TestDemoIntake.test_ca11_cli_execution_and_exit_codes)
CA-11: CLI ejecutable, JSON parseable y codigos de salida correctos. ... ok
test_app_imports_cleanly (test_smoke.TestSmoke.test_app_imports_cleanly)
Verifica que el paquete se importa y expone sus metadatos sin efectos. ... ok
test_main_execution_output (test_smoke.TestSmoke.test_main_execution_output)
Verifica que main() devuelve codigo 0 y JSON con la estructura esperada. ... ok
----------------------------------------------------------------------
Ran 27 tests in 1.014s
OK
4. Conteo de Pruebas y Subcasos
Total de pruebas en la suite: 27 pruebas (16 preexistentes + 11 nuevas).
test_contracts.py: 14 pruebas (incluye la matriz exhaustiva de 1440 combinaciones con exactamente 10 aceptadas).
test_smoke.py: 2 pruebas.
test_demo_intake.py: 11 pruebas (cubriendo CA-01 a CA-11 con más de 25 subcasos evaluados con subTest).
5. Manifiesto y Huellas Criptográficas SHA-256 (Antes / Después)
Archivo	Estado	SHA-256 Inicial	SHA-256 Final	Tamaño (bytes)
AGENTS.md	INTACTO	2e695d684fbc149d7748d9ea0bbc053953bc7c9be9bda5a118952a8f11accc98	2e695d684fbc149d7748d9ea0bbc053953bc7c9be9bda5a118952a8f11accc98	5,379
CONTRATO-MVP-v1.md	INTACTO	d98d47a861009c01394f1273defd7990386f6dc57586660ac3a74b45545b273b	d98d47a861009c01394f1273defd7990386f6dc57586660ac3a74b45545b273b	107,005
FICHA-PZ-001A-CONTRATOS-NUCLEO.md	INTACTO	8e49da127c5671b55d5cda2123f97ddfbce378eceaeb9b5c14c4f7985b539e38	8e49da127c5671b55d5cda2123f97ddfbce378eceaeb9b5c14c4f7985b539e38	13,409
FICHA-PZ-002A-ESTRUCTURA-MINIMA.md	INTACTO	a590936afe48aef65e90f9eec8e43315a8b754bb647a84aa6d66d98af36f8a5d	a590936afe48aef65e90f9eec8e43315a8b754bb647a84aa6d66d98af36f8a5d	18,644
FICHA-PZ-003A-ENTRADA-Y-PLAN-CONTROLADO.md	INTACTO	5f12afe12cc81658a65fb92228bd8cadbc3a8708bff920a07038462d75a26e48	5f12afe12cc81658a65fb92228bd8cadbc3a8708bff920a07038462d75a26e48	18,578
INFORME-CONSTRUCCION-PZ-002A.md	INTACTO	e38c5354cf619439ed6ed44b555842dcf4fb897398df65630a93dec0e47c6abd	e38c5354cf619439ed6ed44b555842dcf4fb897398df65630a93dec0e47c6abd	11,773
REVISION-COPILOT-PZ-001A.md	INTACTO	5a68aa2be944caf91347c1f1b790443ccccf5d1a33670edab175287f23c1a664	5a68aa2be944caf91347c1f1b790443ccccf5d1a33670edab175287f23c1a664	18,131
REVISION-COPILOT-PZ-002A.md	INTACTO	bee1416890e3b633765015cd0a256c83fa562ff6497819f5c2c9d4c1ecf64e48	bee1416890e3b633765015cd0a256c83fa562ff6497819f5c2c9d4c1ecf64e48	14,013
TEAM-WORKFLOW.md	INTACTO	8c401ec1cd81078ddef5d65e13f1243ae4e9c29384d810edea960258c7f8327c	8c401ec1cd81078ddef5d65e13f1243ae4e9c29384d810edea960258c7f8327c	4,843
README.md	MODIFICADO	dfbc3e11733e2f7038aa5e25b57001825187cf5e508ecb9acfb4045f962aa985	93d9eed1eb33daa626957fc7391f2e5ff6137e9ab38cc48cecc91f5efa0b57c1	3,591
pyproject.toml	MODIFICADO	b5892f8e31ba0972d0f45a47662e5082d1f853d863451daabac66827a6730647	77b639ba40550cb67753120ed9f4aa952fc39d08e1cfb87090eaad12d6041392	341
.gitignore	INTACTO	86be820647116f087bb58eb6c088c1e29e510a474416990fc111bc76510d1018	86be820647116f087bb58eb6c088c1e29e510a474416990fc111bc76510d1018	215
app/__init__.py	INTACTO	9b9b2d39de97a69e0cc39b510c311755cec2f9ce665fddae899ad57c1be27915	9b9b2d39de97a69e0cc39b510c311755cec2f9ce665fddae899ad57c1be27915	241
app/__main__.py	INTACTO	06a4e7fcc308c8b124ff7504cb25b30b10ff553751eceef6a175fa53a46e88d8	06a4e7fcc308c8b124ff7504cb25b30b10ff553751eceef6a175fa53a46e88d8	557
contracts/core/README.md	INTACTO	7988e1864e652845b419313d21a05f3710df09502da20056def2a7d988e6bdf7	7988e1864e652845b419313d21a05f3710df09502da20056def2a7d988e6bdf7	5,530
contracts/core/mission.schema.json	INTACTO	fe0c4b789362efd768e1f70d61008401ed1d26bf106afc2421f37770b1081350	fe0c4b789362efd768e1f70d61008401ed1d26bf106afc2421f37770b1081350	6,981
contracts/core/event.schema.json	INTACTO	827b43977f1ba89fe727b43e172c52eeb52f941d7fe1de7c4199f7c5e869681b	827b43977f1ba89fe727b43e172c52eeb52f941d7fe1de7c4199f7c5e869681b	5,453
contracts/core/error.schema.json	INTACTO	a78b4d1f5203a732da0e8ea1c45db01b5eca67a79d14b6de6b48db6700c3bca9	a78b4d1f5203a732da0e8ea1c45db01b5eca67a79d14b6de6b48db6700c3bca9	5,996
contracts/core/approval.schema.json	INTACTO	7dffabd0c643e1beda566262e3c06c01bd84350fb501def5fab52fcc07c91f14	7dffabd0c643e1beda566262e3c06c01bd84350fb501def5fab52fcc07c91f14	5,429
contracts/core/checkpoint.schema.json	INTACTO	754d7eb58dc4d5052acb97c2d73b974e214f7e135336d5f6412515650a2bd242	754d7eb58dc4d5052acb97c2d73b974e214f7e135336d5f6412515650a2bd242	5,900
contracts/core/state-machine.json	INTACTO	186a21eb32e4258c0d4fbc799ab0701aa6a2f318f85aab5a25003d7007f7e840	186a21eb32e4258c0d4fbc799ab0701aa6a2f318f85aab5a25003d7007f7e840	36,945
contracts/core/examples/mission.valid.json	INTACTO	08d47ebbb3554169697f8609ff9ab72c4895329e15a6c42439eec54c8484f32e	08d47ebbb3554169697f8609ff9ab72c4895329e15a6c42439eec54c8484f32e	1,220
contracts/core/examples/mission.invalid.json	INTACTO	b8bb9ba8f856a1353e770cd66f43f82ea8fb0ee2cd76e50abf2c86551b47452b	b8bb9ba8f856a1353e770cd66f43f82ea8fb0ee2cd76e50abf2c86551b47452b	6,205
contracts/core/examples/approval.valid.json	INTACTO	c33fca0e6e576b81e961c2891a9a6a76be9b5d30cc284cc47c456fde76106c0f	c33fca0e6e576b81e961c2891a9a6a76be9b5d30cc284cc47c456fde76106c0f	4,986
contracts/core/examples/approval.invalid.json	INTACTO	6beeb4ec672e3f22bb692d3dbb52348c25e8b873d2bbae051c68654e6c4777a5	6beeb4ec672e3f22bb692d3dbb52348c25e8b873d2bbae051c68654e6c4777a5	6,732
contracts/core/examples/transitions.valid.json	INTACTO	d1d5a4ec2bad452556d884a3650f5576c741ba39588e4eac197fa2723c0c077d	d1d5a4ec2bad452556d884a3650f5576c741ba39588e4eac197fa2723c0c077d	535
contracts/core/examples/transitions.invalid.json	INTACTO	3403ba2e52c3e964142dbbc76e5ad64eace6b6697e8082986f429a0cbdf69912	3403ba2e52c3e964142dbbc76e5ad64eace6b6697e8082986f429a0cbdf69912	12,587
tests/test_contracts.py	INTACTO	c234178c74953b0718c962a36cc24e6de46d5a64b763dd3c375479f77bffe54e	c234178c74953b0718c962a36cc24e6de46d5a64b763dd3c375479f77bffe54e	23,925
tests/test_smoke.py	INTACTO	e3c0b8edee2b384a10e0ec6040a8b5f57d939fe0fb904457ffaba8a1d698c552	e3c0b8edee2b384a10e0ec6040a8b5f57d939fe0fb904457ffaba8a1d698c552	1,298
app/demo_intake.py	NUEVO	(no existía)	47c6e9937ebf06d93f54cb2f0aede5842cb3ea0ab031641d7bcbe811224e5a0e	18,367
examples/demo_mission.json	NUEVO	(no existía)	34c605ebc37f6b5ff7d510fe6d07478b2cdf3a652ff5302ced9eedaac6b0f3a7	4,438
tests/test_demo_intake.py	NUEVO	(no existía)	80307a7e314d0733b2c100ec6d833984b1a67a38b52c193546fb8195e22103a4	17,774
6. Verificación de Residuos
Archivos bytecode / caches (__pycache__, .pyc, .pyo): 0 encontrados.
Variables de entorno / .env: 0 encontrados.
Archivos temporales fuera de lista: 0 encontrados.
7. Limitaciones y Riesgos Conocidos
Ensayo estrictamente en memoria (efímero): Nada sobrevive al cierre del proceso python -B -m app.demo_intake. No implementa persistencia ni base de datos.
Sin ejecución ni agentes reales: Las 4 tareas propuestas por el Chief of Staff simulado no se ejecutan y sus categorías de herramientas se entregan vacías ([]).
Detención controlada: El flujo se detiene en PLAN_EN_REVISION (o ACLARACION_REQUERIDA). No contiene rutas de autoaprobación ni avance hacia AUTORIZADA_PARA_EJECUTAR o EN_EJECUCION.
Validación formal: El módulo detecta faltantes estructurales y supuestos declarados; no realiza comprensión semántica de ambigüedades.
8. Declaración de Cumplimiento de Procedimiento
En estricto apego a 
AGENTS.md
 y 
FICHA-PZ-003A-ENTRADA-Y-PLAN-CONTROLADO.md
:

No se declara PZ-003A aprobada ni aceptada.
No se declara OminAI HQ listo para producción ni para el concurso.
El resultado queda listo para la inspección de Chipi/Codex, la revisión independiente de Copilot y la decisión final de aprobación de la autoridad humana (Niko).
````

