/**
 * OminAI HQ - Durable local SIMULADA UI (PZ-UI-014A).
 * Rendering is text-only and client-safe; server owns authority and state transitions.
 */
function escapeHTML(str) {
  return String(str ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

document.addEventListener('DOMContentLoaded', () => {
  const el = id => document.getElementById(id);
  let missionId = null, mission = null, planRequest = null, vbpRequest = null, csrf = null;
  let vbp = null, canonical = '', busy = false;
  let memories = [], evidence = {}, translations = {}, lastMessage = null;

  const lang = () => window.OminaiI18N.getLanguage();
  const text = (id, value) => { if(el(id)) el(id).textContent = value ?? 'NO_DISPONIBLE'; };
  const tr = (es, en) => lang() === 'en' ? en : es;
  const authored = value => lang() === 'es' ? value : (translations[value] || (tr('', 'TRANSLATION PENDING — original: ') + value));

  function banner(message, error = false) {
    lastMessage = { message, error };
    const code = String(message).split(':')[0];
    const errors = {
      INVALID_INPUT: 'Invalid input',
      NOT_FOUND: 'Record or evidence unavailable',
      PERMISSION_DENIED: 'Permission denied',
      SYSTEM_ERROR: 'Operation not confirmed; inspect persisted state',
      BUDGET_EXHAUSTED: 'Budget exhausted',
      SCHEMA_INVALID: 'Contract validation failed',
      DEPENDENCY_FAILED: 'Dependency incomplete',
      TRANSIENT_FAILURE: 'Transient failure'
    };
    text('action-banner-text', (error ? 'Error: ' : 'SIMULADA — ') + (error && lang() === 'en' && errors[code] ? errors[code] + ' [' + code + '] — ' + message : message));
    if (el('action-banner')) {
      el('action-banner').className = 'alert-banner ' + (error ? 'alert-danger' : 'alert-info');
    }
  }

  async function api(path, method = 'GET', body) {
    const headers = { 'Content-Type': 'application/json' };
    if (method !== 'GET') headers['X-Ominai-CSRF'] = csrf || '';
    const response = await fetch(path, { method, headers, body: body === undefined ? undefined : JSON.stringify(body) });
    if (!response.ok) {
      const result = await response.json();
      throw new Error(result.error || 'HTTP ' + response.status);
    }
    return response;
  }

  async function data(path, method = 'GET', body) {
    return (await (await api(path, method, body)).json()).data;
  }

  const route = sub => '/api/v1/missions/' + encodeURIComponent(missionId) + sub;

  async function action(fn) {
    if (busy) return;
    busy = true;
    render();
    try {
      await fn();
      if (missionId) await refresh();
    } catch (error) {
      banner(error.message, true);
      if (missionId) {
        try { await refresh(false); } catch (e) { banner(e.message, true); }
      }
    } finally {
      busy = false;
      render();
    }
  }

  function render() {
    const status = mission?.status;
    text('server-status-badge', csrf ? 'ONLINE — SIMULADA' : 'NO_DISPONIBLE');
    text('active-mission-state', window.OminaiI18N.stateLabel(status));
    text('active-mission-id', missionId);
    text('plan-fingerprint', planRequest?.fingerprint);
    text('plan-tasks-count', mission?.plan?.tasks?.length);
    text('plan-preview', mission?.plan ? JSON.stringify({ brief: mission.brief, plan: mission.plan }, null, 2) : tr('Plan pendiente', 'Plan pending'));
    
    if (lang() === 'en' && mission?.plan) {
      text('plan-preview', [
        'SIMULADA',
        ...['title', 'objective', 'context', 'expected_result'].map(key => key + ': ' + authored(mission[key])),
        ...mission.plan.tasks.map(task => task.task_id + ' — ' + authored(task.objective) + '; dependencies: ' + task.dependencies.join(', ')),
        'Memory references: ' + JSON.stringify(mission.plan.memory_refs),
        'Original plan / stable IDs and metadata:',
        JSON.stringify(mission.plan, null, 2)
      ].join('\n'));
    }

    const buttons = {
      'btn-submit-mission': !csrf || (!!mission && !['FINALIZADA', 'CANCELADA'].includes(status)),
      'btn-approve-plan': status !== 'PLAN_EN_REVISION' || planRequest?.status !== 'PENDIENTE',
      'btn-reject-plan': status !== 'PLAN_EN_REVISION' || planRequest?.status !== 'PENDIENTE',
      'btn-renew-approval': !['PLAN_EN_REVISION', 'VBP_EN_REVISION'].includes(status),
      'btn-execute-step': !['AUTORIZADA_PARA_EJECUTAR', 'EN_EJECUCION'].includes(status),
      'btn-pause-mission': !status || ['FINALIZADA', 'CANCELADA', 'PAUSADA'].includes(status),
      'btn-resume-mission': status !== 'PAUSADA',
      'btn-cancel-mission': !status || ['FINALIZADA', 'CANCELADA'].includes(status),
      'btn-approve-vbp': status !== 'VBP_EN_REVISION' || !vbpRequest || mission?.evaluation_report?.verdict === 'NO_PASA',
      'btn-reject-vbp': status !== 'VBP_EN_REVISION' || !vbpRequest,
      'btn-approve-exception': status !== 'VBP_EN_REVISION' || !vbpRequest,
      'btn-download-vbp': !['VBP_APROBADO', 'FINALIZADA'].includes(status),
      'btn-load-demo': !csrf,
      'btn-memory-propose': !missionId,
      'btn-memory-approve': !el('memory-picker')?.value,
      'btn-memory-update': !el('memory-picker')?.value,
      'btn-memory-delete': !el('memory-picker')?.value
    };

    Object.entries(buttons).forEach(([id, disabled]) => {
      if (el(id)) {
        el(id).disabled = busy || disabled;
        el(id).title = disabled ? tr('No disponible en el estado actual', 'Unavailable in the current state') : '';
      }
    });

    if (el('btn-resume-mission')) {
      el('btn-resume-mission').classList.remove('hidden');
    }

    text('task-status-1', tr('PLAN DETERMINISTA — no es llamada a agente', 'DETERMINISTIC PLAN — not an agent call'));
    (mission?.tasks || []).forEach((task, i) => {
      const taskElem = el('task-status-' + (i + 2));
      if (taskElem) {
        taskElem.textContent = 'SIMULADA ' + task.task_id + ' — ' + window.OminaiI18N.stateLabel(task.status);
        taskElem.className = 'status-indicator ' + (task.status || 'PENDIENTE');
      }
    });

    for (let i = 1; i <= 5; i++) {
      text('task-subtext-' + i, i === 1 ? tr('Plan y referencias de memoria autorizada', 'Plan and authorized memory references') : tr('Estado persistido; resultados SIMULADA', 'Persisted state; SIMULADA results'));
    }

    text('runtime-metrics', JSON.stringify({
      [tr('segundos_activos', 'active_seconds')]: mission?.active_seconds ?? 0,
      [tr('solicitudes', 'requests')]: mission?.agent_requests ?? 0,
      [tr('errores', 'errors')]: Object.values(mission?.task_results || {}).flatMap(result => result.errors || []),
      [tr('intentos_por_tarea', 'attempts_per_task')]: Object.fromEntries((mission?.tasks || []).map(task => [task.task_id, task.attempt ?? 0]))
    }, null, 2));

    text('metric-req-count', mission?.agent_requests);
    text('metric-spent', mission?.budget ? 'SIMULADA USD ' + mission.budget.spent_usd + ' / ' + tr('reservado ', 'reserved ') + mission.budget.reserved_usd + ' ' + (mission.budget.alert || '') : 'NO_DISPONIBLE');

    const report = mission?.evaluation_report;
    text('vbp-dictamen', report ? 'SIMULADA ' + window.OminaiI18N.stateLabel(report.verdict) : 'NO_DISPONIBLE');
    text('vbp-score', report?.total_score == null ? 'NO_DISPONIBLE' : report.total_score + ' / 100');
    text('vbp-blockers', report ? JSON.stringify({
      blockers: report.blockers,
      findings: report.findings,
      scope: tr('Comprobaciones estructurales y referenciales; calidad real no demostrada.', 'Structural and referential checks; real quality not demonstrated.')
    }) : 'NO_DISPONIBLE');

    text('vbp-approval-status-badge', window.OminaiI18N.stateLabel(vbp?.approval_status));
    text('vbp-fingerprint-display', vbp?.fingerprint);
    text('vbp-markdown-preview', lang() === 'en' && vbp ? vbp.sections.map(s => s.section_number + '. ' + s.section_name + '\n' + (s.content.match(/```english\n([\s\S]*?)\n```/)?.[1] || 'TRANSLATION PENDING')).join('\n\n') : canonical || tr('VBP pendiente', 'VBP pending'));
    text('download-hint', (mission?.translation_status || 'PENDIENTE') + ' — ' + tr('Markdown único ES/EN. Entrega HTTP no demuestra guardado en disco.', 'One ES/EN Markdown. HTTP delivery does not prove saving to disk.'));
    text('evidence-list', Object.values(evidence).map(ev => [ev.evidence_id, ev.title, ev.source_locator, ev.location_in_source, authored(ev.excerpt_or_summary), 'SIMULADA — ' + tr('Fuente real NO_VERIFICADA', 'Real source NOT VERIFIED')].join('\n')).join('\n\n') || tr('Sin evidencia', 'No evidence'));

    if (lastMessage?.error) banner(lastMessage.message, true);
  }

  async function refresh(showBanner = true) {
    mission = await data(route(''));
    const p = await data(route('/plan'));
    planRequest = p.approval_request;
    if (mission.pending_GATE_2_VBP) {
      const view = await data(route('/vbp'));
      vbp = view.vbp_data;
      canonical = view.canonical_markdown;
      vbpRequest = mission.approval_request;
    } else {
      vbp = null;
      canonical = '';
      vbpRequest = null;
    }
    text('audit-timeline', JSON.stringify(await data(route('/audit')), null, 2));
    evidence = await data(route('/evidence'));
    await loadMemories();
    if (el('mission-status-box')) el('mission-status-box').classList.remove('hidden');
    if (showBanner) banner(tr('Estado persistido: ', 'Persisted state: ') + window.OminaiI18N.stateLabel(mission.status));
    render();
  }

  async function decide(gate, decision) {
    const request = gate === 'GATE_1_PLAN' ? planRequest : vbpRequest;
    let comment = '', conditions = [], risks = [];
    if (decision !== 'APROBAR') {
      comment = el('decision-reason').value;
      if (!comment.trim()) throw new Error(tr('Motivo requerido', 'Reason required'));
    }
    if (decision === 'APROBAR_CON_EXCEPCION' || (mission?.evaluation_report?.verdict === 'PASA_CON_CONDICIONES' && gate === 'GATE_2_VBP')) {
      conditions = el('decision-conditions').value.split('\n').filter(x => x.trim());
      if (!conditions.length) throw new Error('CONDICIONES_REQUERIDAS');
    }
    if (decision === 'APROBAR_CON_EXCEPCION') {
      risks = el('decision-risks').value.split('\n').filter(x => x.trim());
      if (!risks.length) throw new Error('RIESGOS_REQUERIDOS');
    }
    await data(route('/decisions'), 'POST', { approval_request: request, decision, comment, conditions, risks });
  }

  if (el('intake-form')) {
    el('intake-form').addEventListener('submit', e => {
      e.preventDefault();
      action(async () => {
        const result = await data('/api/v1/missions', 'POST', {
          mission_id: 'MSN-' + Date.now(),
          title: el('mission-title').value,
          objective: el('mission-objective').value,
          context: el('mission-context').value,
          expected_result: el('mission-expected-result').value
        });
        missionId = result.mission_id;
        vbp = null;
        canonical = '';
        vbpRequest = null;
      });
    });
  }

  [['btn-approve-plan', 'GATE_1_PLAN', 'APROBAR'], ['btn-reject-plan', 'GATE_1_PLAN', 'RECHAZAR'],
   ['btn-approve-vbp', 'GATE_2_VBP', 'APROBAR'], ['btn-reject-vbp', 'GATE_2_VBP', 'RECHAZAR'],
   ['btn-approve-exception', 'GATE_2_VBP', 'APROBAR_CON_EXCEPCION']]
    .forEach(([id, gate, decision]) => {
      if (el(id)) el(id).addEventListener('click', () => action(() => decide(gate, decision)));
    });

  ['pause', 'resume', 'cancel'].forEach(op => {
    const btn = el('btn-' + op + '-mission');
    if (btn) {
      btn.addEventListener('click', () => action(async () => {
        if (op === 'cancel' && !el('decision-reason').value.trim()) throw new Error(tr('Ingrese motivo antes de cancelar', 'Enter a reason before cancelling'));
        await data(route('/' + op), 'POST', { reason: el('decision-reason').value || 'Control de usuario local SIMULADA' });
      }));
    }
  });

  if (el('btn-execute-step')) {
    el('btn-execute-step').addEventListener('click', () => action(() => data(route('/execute-step'), 'POST')));
  }

  if (el('btn-renew-approval')) {
    el('btn-renew-approval').addEventListener('click', () => action(async () => {
      const gate = mission.status === 'PLAN_EN_REVISION' ? 'GATE_1_PLAN' : 'GATE_2_VBP';
      await data(route('/renew-approval'), 'POST', { gate_type: gate });
    }));
  }

  if (el('btn-download-vbp')) {
    el('btn-download-vbp').addEventListener('click', () => action(async () => {
      const response = await api(route('/vbp/export'));
      const blob = await response.blob(), url = URL.createObjectURL(blob), a = document.createElement('a');
      a.href = url;
      a.download = 'VBP-' + missionId + '.md';
      a.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    }));
  }

  if (el('btn-refresh-audit')) {
    el('btn-refresh-audit').addEventListener('click', () => action(() => missionId ? refresh() : Promise.reject(new Error('NOT_FOUND: Mision pendiente'))));
  }

  if (el('btn-lang-toggle')) {
    el('btn-lang-toggle').addEventListener('click', () => {
      window.OminaiI18N.toggleLanguage();
      render();
    });
  }

  function selectedMemory() {
    return memories.find(memory => memory.memory_id === el('memory-picker').value);
  }

  async function loadMemories() {
    if (!el('memory-picker')) return;
    const selected = el('memory-picker').value;
    memories = await data('/api/v1/memory');
    el('memory-picker').replaceChildren();
    const fresh = document.createElement('option');
    fresh.value = '';
    fresh.textContent = 'Nueva / New';
    el('memory-picker').appendChild(fresh);
    for (const memory of memories) {
      const option = document.createElement('option');
      option.value = memory.memory_id;
      option.textContent = memory.memory_id + ' v' + memory.version + ' — ' + memory.status + (memory.blocked ? ' [BLOQUEADA / BLOCKED]' : '');
      el('memory-picker').appendChild(option);
    }
    el('memory-picker').value = memories.some(memory => memory.memory_id === selected) ? selected : '';
    text('memory-list', JSON.stringify(memories, null, 2));
  }

  if (el('memory-picker')) {
    el('memory-picker').addEventListener('change', () => {
      const memory = selectedMemory();
      el('memory-content').value = memory?.content || '';
      el('memory-review-at').value = memory?.review_at || '';
      el('memory-delete-id').value = '';
      el('memory-resolve').checked = false;
      render();
    });
  }

  if (el('btn-memory-propose')) {
    el('btn-memory-propose').addEventListener('click', () => action(async () => {
      await data('/api/v1/memory', 'POST', {
        mission_id: missionId,
        category: el('memory-category').value,
        fact_text: el('memory-content').value,
        review_at: el('memory-review-at').value || null,
        review_required: el('memory-review-required').checked,
        conflict: el('memory-conflict').checked,
        material_impact: el('memory-material').checked
      });
      await loadMemories();
    }));
  }

  ['approve', 'update', 'delete'].forEach(operation => {
    const btn = el('btn-memory-' + operation);
    if (btn) {
      btn.addEventListener('click', () => action(async () => {
        const memory = selectedMemory();
        if (!memory) throw new Error('INVALID_INPUT: ' + tr('Seleccione memoria y versión', 'Select memory and version'));
        const path = '/api/v1/memory/' + encodeURIComponent(memory.memory_id), version = memory.version;
        if (operation === 'approve') {
          await data(path + '/approve', 'POST', { version, resolve_blockers: el('memory-resolve').checked, review_at: el('memory-review-at').value || null });
        }
        if (operation === 'update') {
          await data(path, 'PUT', { version, fact_text: el('memory-content').value });
        }
        if (operation === 'delete') {
          if (el('memory-delete-id').value !== memory.memory_id) throw new Error('INVALID_INPUT: ' + tr('Confirme ID exacto', 'Confirm exact ID'));
          await data(path, 'DELETE', { confirm_memory_id: memory.memory_id, version });
          el('memory-content').value = '';
        }
        await loadMemories();
      }));
    }
  });

  if (el('btn-load-demo')) {
    el('btn-load-demo').addEventListener('click', () => action(async () => {
      const prepared = await data('/api/v1/demo-template');
      ['title', 'objective', 'context', 'expected_result'].forEach(key => {
        const input = el('mission-' + key.replace('_', '-'));
        if (input) input.value = prepared.fields[key];
      });
    }));
  }

  // Navegación lateral activa
  const navLinks = document.querySelectorAll('.side-nav a');
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      navLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
    });
  });

  // Inicialización de sesión y perfil
  action(async () => {
    csrf = (await data('/api/v1/session')).csrf_token;
    translations = (await data('/api/v1/demo-template')).english;
    const p = await data('/api/v1/profile');
    text('op-user-id', p.user_id);
    text('op-display-name', p.display_name);
    text('op-role', p.actor_role);
    await loadMemories();
    const current = await data('/api/v1/missions/current');
    if (current) {
      missionId = current.mission_id;
      ['title', 'objective', 'context', 'expected_result'].forEach(key => {
        const input = el('mission-' + key.replace('_', '-'));
        if (input) input.value = current[key] || '';
      });
    }
    await data('/health');
    text('server-status-badge', 'ONLINE — SIMULADA');
    banner(tr('Revise el plan completo antes de decidir.', 'Review the full plan before deciding.'));
  });
});
