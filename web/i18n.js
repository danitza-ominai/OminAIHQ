/**
 * OminAI HQ - Sistema de Internacionalización Bilingüe ES / EN (PZ-013C & PZ-UI-014A).
 *
 * Proporciona diccionario completo y funciones de traducción dinámica para la interfaz
 * cumpliendo con CONTRATO-MVP-v1.md 6.6, 11.9 y FICHA-PZ-013C.md.
 * Conserva identificadores estables y metadatos originales sin traducir.
 */

(function () {
  'use strict';

  const translations = {
    es: {
      // Cabecera y Marca
      app_title: 'OminAI HQ',
      app_subtitle: 'Oficina Digital Agéntica',
      badge_simulated: 'MODO SIMULADA (HACKATHON DEMO)',
      badge_ready: 'ESTRUCTURA_LISTA',
      lang_switch: 'English (EN)',

      // Barra Lateral de Navegación
      nav_title: 'Centro de Gestión',
      nav_operator: 'Resumen',
      nav_intake: 'Admisión de misión',
      nav_gate1: 'Puerta 1: Plan',
      nav_execution: 'Ejecución',
      nav_evidence: 'Evidencias y memoria',
      nav_gate2: 'Puerta 2: VBP',
      nav_export: 'Exportación',
      nav_audit: 'Límites y Auditoría',
      side_status_heading: 'Modo de Operación',
      side_status_desc: 'Gobernanza agéntica con aprobación humana estricta (A0). Ejecución local protegida.',
      side_footer_text: 'OminAI HQ • v1.0.0',

      // Secciones Principales
      section_operator: '1. Operador Humano (A0)',
      section_intake: '2. Admisión de Misión (Intake)',
      section_gate1: '3. Puerta 1: Decisión Humana del Plan',
      section_specialists: '4. Seguimiento de Especialistas',
      section_evidence_memory: '5. Evidencias y Memoria Aprobada',
      section_gate2: '6. Puerta 2: Dictamen y Aprobación del VBP',
      section_vbp: '7. Visualización y Descarga del VBP (PZ-013C)',
      section_audit: '8. Límites y Auditoría en Tiempo Real',

      // Operador
      op_user_label: 'Usuario:',
      op_name_label: 'Nombre:',
      op_role_label: 'Rol de Autoridad:',

      // Admisión
      label_mission_title: 'Título de la Misión:',
      placeholder_mission_title: 'Ej. Plataforma B2B de compras industriales',
      label_mission_objective: 'Objetivo:',
      placeholder_mission_objective: 'Describa el objetivo principal de la misión...',
      label_mission_context: 'Contexto y Requisitos:',
      placeholder_mission_context: 'Contexto de negocio, regulaciones o restricciones aplicables...',
      label_expected_result: 'Resultado Esperado:',
      placeholder_expected_result: 'Ej. VBP completo con plan y validación de gobernanza...',
      btn_submit_mission: 'Iniciar Misión',
      btn_saving: 'Enviando...',
      active_mission_label: 'Misión Activa:',
      active_status_label: 'Estado:',

      // Puerta 1
      gate1_desc: 'El plan de ejecución requiere revisión y autorización expresa antes de activar los especialistas.',
      label_tasks_count: 'Tareas del Plan:',
      label_plan_fingerprint: 'Huella Digital (SHA-256):',
      btn_approve_plan: 'Aprobar Plan',
      btn_reject_plan: 'Rechazar Plan',
      btn_pause_mission: 'Pausar Misión',
      btn_resume_mission: 'Reanudar Misión',
      btn_cancel_mission: 'Cancelar Misión',

      // Especialistas
      spec_task1: 'Tarea 1: Chief of Staff - Planificación inicial y orquestación',
      spec_task2: 'Tarea 2: Research Analyst - Análisis de fuentes y claims',
      spec_task3: 'Tarea 3: Product Architect - Definición de producto y requisitos',
      spec_task4: 'Tarea 4: Delivery Planner - Fases, dependencias y riesgos',
      spec_task5: 'Tarea 5: Governance Risk - Dictamen independiente PASA / NO_PASA',
      btn_execute_step: 'Ejecutar Paso Siguiente',
      btn_executing: 'Ejecutando...',

      // Evidencia y Memoria
      evidence_title: 'Evidencias Registradas',
      memory_title: 'Memorias Aprobadas',
      evidence_none: 'No hay evidencias registradas aún.',
      memory_none: 'No hay hechos memorizados registrados.',
      btn_delete_memory: 'Eliminar',

      // Puerta 2
      label_dictamen: 'Dictamen de Gobernanza:',
      label_score: 'Puntaje Ponderado:',
      label_blockers: 'Bloqueadores:',
      btn_approve_vbp: 'Aprobar VBP Final',
      btn_reject_vbp: 'Rechazar VBP',
      btn_approve_exception: 'Aprobar con Excepción',

      // VBP Visualización y Descarga
      vbp_preview_heading: 'Contenido del VBP Canónico en Markdown (18 Secciones)',
      vbp_manifest_fp: 'Huella del Manifest:',
      vbp_status_text: 'Estado de Aprobación:',
      vbp_sections_badge: '18 Secciones Obligatorias',
      btn_download_vbp: 'Descargar VBP (.md)',
      vbp_download_blocked: 'La descarga requiere que el VBP esté formalmente aprobado por el usuario humano.',

      // Límites y Auditoría
      metric_budget: 'Presupuesto Máximo',
      metric_budget_val: '$25.00 USD (Techo)',
      metric_requests: 'Límite de Solicitudes',
      metric_requests_val: '15 máx.',
      metric_time: 'Tiempo Límite',
      metric_time_val: '300s por puerta',
      timeline_placeholder: 'Registro de eventos auditables en espera...',
      btn_refresh_audit: 'Actualizar Auditoría',

      // Footer
      footer_text: 'OminAI HQ - Sistema de Gobernanza y Venture Building con Autoridad Humana Exclusiva (A0).',

      // Mensajes dinámicos y prompts
      prompt_reject_comment: 'Ingrese el motivo del rechazo (obligatorio):',
      prompt_exception_comment: 'Ingrese el motivo y condiciones de la excepción (obligatorio):',
      confirm_cancel_mission: '¿Está seguro de cancelar la misión activa? Esta acción no se puede deshacer.',
      confirm_delete_memory: '¿Desea eliminar permanentemente esta memoria aprobada?',
      msg_next_action_gate1: 'Siguiente acción humana requerida: Revisar y decidir sobre el plan propuesto.',
      msg_next_action_gate2: 'Siguiente acción humana requerida: Revisar informe de gobernanza y decidir sobre el VBP.',
      msg_next_action_done: 'Misión finalizada. VBP listo para visualización y descarga.',
      msg_next_action_paused: 'Misión pausada. Use "Reanudar Misión" para continuar.',
      msg_next_action_blocked: 'Misión bloqueada por límites o dependencias.',
    },

    en: {
      // Header and Brand
      app_title: 'OminAI HQ',
      app_subtitle: 'Agentic Digital Office',
      badge_simulated: 'SIMULATED MODE (HACKATHON DEMO)',
      badge_ready: 'STRUCTURE_READY',
      lang_switch: 'Español (ES)',

      // Sidebar Navigation
      nav_title: 'Management Center',
      nav_operator: 'Overview',
      nav_intake: 'Mission Intake',
      nav_gate1: 'Gate 1: Plan',
      nav_execution: 'Execution',
      nav_evidence: 'Evidence & Memory',
      nav_gate2: 'Gate 2: VBP',
      nav_export: 'Export',
      nav_audit: 'Limits & Audit',
      side_status_heading: 'Operation Mode',
      side_status_desc: 'Agentic governance with strict human approval (A0). Protected local execution.',
      side_footer_text: 'OminAI HQ • v1.0.0',

      // Main Sections
      section_operator: '1. Human Operator (A0)',
      section_intake: '2. Mission Intake',
      section_gate1: '3. Gate 1: Human Plan Decision',
      section_specialists: '4. Specialist Tracking',
      section_evidence_memory: '5. Evidence & Approved Memory',
      section_gate2: '6. Gate 2: Governance Verdict & VBP Decision',
      section_vbp: '7. VBP View & Download (PZ-013C)',
      section_audit: '8. Real-Time Limits & Audit',

      // Operator
      op_user_label: 'User:',
      op_name_label: 'Name:',
      op_role_label: 'Authority Role:',

      // Intake
      label_mission_title: 'Mission Title:',
      placeholder_mission_title: 'E.g., B2B Industrial Purchasing Platform',
      label_mission_objective: 'Objective:',
      placeholder_mission_objective: 'Describe the main objective of the mission...',
      label_mission_context: 'Context and Requirements:',
      placeholder_mission_context: 'Business context, regulations, or applicable constraints...',
      label_expected_result: 'Expected Result:',
      placeholder_expected_result: 'E.g., Complete VBP with plan and governance validation...',
      btn_submit_mission: 'Start Mission',
      btn_saving: 'Submitting...',
      active_mission_label: 'Active Mission:',
      active_status_label: 'Status:',

      // Gate 1
      gate1_desc: 'The execution plan requires human review and explicit authorization before activating specialist agents.',
      label_tasks_count: 'Plan Tasks:',
      label_plan_fingerprint: 'Digital Fingerprint (SHA-256):',
      btn_approve_plan: 'Approve Plan',
      btn_reject_plan: 'Reject Plan',
      btn_pause_mission: 'Pause Mission',
      btn_resume_mission: 'Resume Mission',
      btn_cancel_mission: 'Cancel Mission',

      // Specialists
      spec_task1: 'Task 1: Chief of Staff - Initial planning and orchestration',
      spec_task2: 'Task 2: Research Analyst - Source analysis and claims',
      spec_task3: 'Task 3: Product Architect - Product definition and requirements',
      spec_task4: 'Task 4: Delivery Planner - Phases, dependencies, and risks',
      spec_task5: 'Task 5: Governance Risk - Independent PASS / FAIL verdict',
      btn_execute_step: 'Execute Next Step',
      btn_executing: 'Executing...',

      // Evidence and Memory
      evidence_title: 'Registered Evidence',
      memory_title: 'Approved Memories',
      evidence_none: 'No evidence registered yet.',
      memory_none: 'No stored facts registered.',
      btn_delete_memory: 'Delete',

      // Gate 2
      label_dictamen: 'Governance Verdict:',
      label_score: 'Weighted Score:',
      label_blockers: 'Blockers:',
      btn_approve_vbp: 'Approve Final VBP',
      btn_reject_vbp: 'Reject VBP',
      btn_approve_exception: 'Approve with Exception',

      // VBP View and Download
      vbp_preview_heading: 'Canonical Markdown VBP Content (18 Sections)',
      vbp_manifest_fp: 'Manifest Fingerprint:',
      vbp_status_text: 'Approval Status:',
      vbp_sections_badge: '18 Mandatory Sections',
      btn_download_vbp: 'Download VBP (.md)',
      vbp_download_blocked: 'Download requires the VBP to be formally approved by the human operator.',

      // Limits and Audit
      metric_budget: 'Maximum Budget',
      metric_budget_val: '$25.00 USD (Ceiling)',
      metric_requests: 'Requests Limit',
      metric_requests_val: '15 max.',
      metric_time: 'Time Limit',
      metric_time_val: '300s per gate',
      timeline_placeholder: 'Auditable events log pending...',
      btn_refresh_audit: 'Refresh Audit',

      // Footer
      footer_text: 'OminAI HQ - Governance and Venture Building System with Exclusive Human Authority (A0).',

      // Dynamic messages and prompts
      prompt_reject_comment: 'Enter the reason for rejection (required):',
      prompt_exception_comment: 'Enter reason and conditions for the exception (required):',
      confirm_cancel_mission: 'Are you sure you want to cancel the active mission? This cannot be undone.',
      confirm_delete_memory: 'Do you want to permanently delete this approved memory?',
      msg_next_action_gate1: 'Next human action required: Review and decide on the proposed plan.',
      msg_next_action_gate2: 'Next human action required: Review governance report and decide on the VBP.',
      msg_next_action_done: 'Mission finalized. VBP ready for view and download.',
      msg_next_action_paused: 'Mission paused. Use "Resume Mission" to continue.',
      msg_next_action_blocked: 'Mission blocked due to limits or unmet dependencies.',
    },
  };

  let currentLang = 'es';

  const i18n = {
    stateLabel: function (value) {
      if (!value) return 'NO_DISPONIBLE';
      const states = {
        PLAN_EN_REVISION: 'Plan under review',
        AUTORIZADA_PARA_EJECUTAR: 'Authorized for execution',
        EN_EJECUCION: 'Executing',
        VBP_EN_REVISION: 'VBP under review',
        VBP_APROBADO: 'VBP approved',
        FINALIZADA: 'Finalized',
        PAUSADA: 'Paused',
        CANCELADA: 'Cancelled',
        COMPLETA: 'Complete',
        PENDIENTE: 'Pending',
        EN_CURSO: 'In progress',
        BLOQUEADA: 'Blocked',
        FALLIDA: 'Failed',
        PARCIAL: 'Partial',
        NO_PASA: 'Does not pass',
        PASA: 'Pass',
        PASA_CON_CONDICIONES: 'Pass with conditions',
        BORRADOR: 'Draft',
        ACLARACION_REQUERIDA: 'Clarification required',
        LISTA_PARA_PLAN: 'Ready for planning',
        LISTA: 'Ready',
        EN_CONSOLIDACION: 'Consolidating',
        EN_EVALUACION: 'Evaluating',
        VBP_RECHAZADO: 'VBP rejected',
        APROBADO: 'Approved',
        APROBADO_CON_EXCEPCION: 'Approved with exception'
      };
      return currentLang === 'en' ? (states[value] || value) + ' [' + value + ']' : value;
    },

    getLanguage: function () {
      return currentLang;
    },

    setLanguage: function (lang) {
      if (lang === 'es' || lang === 'en') {
        currentLang = lang;
        document.documentElement.lang = lang;
        this.updateDOM();
      }
    },

    toggleLanguage: function () {
      this.setLanguage(currentLang === 'es' ? 'en' : 'es');
    },

    t: function (key, fallback) {
      const dict = translations[currentLang] || translations.es;
      return dict[key] !== undefined ? dict[key] : (fallback || key);
    },

    updateDOM: function () {
      const elements = document.querySelectorAll('[data-i18n]');
      elements.forEach((el) => {
        const key = el.getAttribute('data-i18n');
        if (key) {
          el.textContent = this.t(key, el.textContent);
        }
      });

      const placeholderElements = document.querySelectorAll('[data-i18n-placeholder]');
      placeholderElements.forEach((el) => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (key) {
          el.setAttribute('placeholder', this.t(key, el.getAttribute('placeholder')));
        }
      });

      const langBtn = document.getElementById('btn-lang-toggle');
      if (langBtn) {
        langBtn.textContent = currentLang === 'es' ? 'English (EN)' : 'Español (ES)';
      }
    },
  };

  // Exponer al ámbito global
  window.OminaiI18N = i18n;
})();
