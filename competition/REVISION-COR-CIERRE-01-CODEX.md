# Revisión de COR-CIERRE-01 — Codex

Fecha: 2026-08-31. Estado: CORRECCION_PARCIAL_CON_DOS_BLOQUEADORES. No es revisión de Copilot ni aceptación humana. Codex no modificó código de producto en esta revisión.

## Evidencia confirmada

- Comparación SHA-256 contra el inventario previo de 224 archivos: exactamente ocho archivos cambiaron: `Dockerfile`, `app/adk_provider.py`, `app/agent_gateway.py`, `app/runtime_config.py`, `deploy/requirements.lock`, `pyproject.toml`, `tests/test_adk_provider.py`, `tests/test_agent_gateway.py`.
- Tres archivos de coordinación creados por Codex en la revisión anterior explican 224 -> 227. No hubo otras altas ni eliminaciones.
- Suite repetida: `Ran 303 tests in 87.430s — OK`.
- Pruebas dirigidas ADK/gateway/cloud policy: 26 pruebas, 0 fallos.
- `py_compile` de cinco archivos afectados terminó sin error.
- Preflight actual: `(False, 'google-adk no esta disponible en el entorno.')`, coherente con NO_INSTALADO/REAL_NO_VERIFICADA.
- Lock: 56 requisitos con pin exacto; 1,432 líneas de hash; contiene google-adk 2.8.0, google-genai 2.20.0 y jsonschema 4.23.0. No se instaló ni se probó la resolución/imagen.
- La API usada fue contrastada contra el código oficial de la etiqueta v2.8.0: LlmAgent admite `mode='single_turn'`, `include_contents='none'`, `output_schema` dict y `generate_content_config`; Gemini admite cliente y retry_options; InMemoryRunner expone run y RunConfig expone max_llm_calls. Fuentes: https://github.com/google/adk-python/blob/v2.8.0/src/google/adk/agents/llm_agent.py, https://github.com/google/adk-python/blob/v2.8.0/src/google/adk/models/google_llm.py, https://github.com/google/adk-python/blob/v2.8.0/src/google/adk/runners.py.

No se usaron credenciales, SDK instalado, red del proveedor, gasto, Docker build, despliegue ni publicación.

## Avances válidos

1. El transporte REST fue retirado; el código intenta usar Agent/Gemini/InMemoryRunner, sin herramientas y con una sola llamada ADK.
2. El modo SIMULADA sigue siendo el predeterminado y no admite proveedor real.
3. El modo REAL exige modelo/tarifa/fecha, credencial presente, preflight, flag de autorización y proveedor ADK.
4. Reserva antes de invocar, uso incierto retenido, límites de salida, esquema JSON, rechazo de herramientas/CoT/secreto y separación REAL_NO_VERIFICADA.
5. La suite previa permanece verde y el perímetro coincide.

## Hallazgos bloqueadores reproducidos

### C01-R1 — P0 — autorización real no vinculada a autoridad humana

`AgentGateway(..., real_execution_authorized=True)` habilita la llamada con un proveedor que declara `provider_kind='ADK_REAL'`, `has_credentials=True` y `preflight=True`. No recibe ni valida contexto humano, aprobación persistida, misión, propietario, puerta, huella, expiración ni estado.

Reproducción offline: solo el booleano; `human_context=false`; `approval_reference=false`; primera llamada aceptada. Esto no demuestra explotación por HTTP, porque los roles reales aún no están conectados, pero el límite inferior no puede tratar un booleano programático como autorización facturable.

Impacto: cuando H05 conecte los roles, cualquier composición que active el flag podría gastar sin probar el mandato humano concreto. La autorización del trabajo de código tampoco equivale a autorizar llamadas facturables futuras.

Corrección: sustituir el booleano como prueba suficiente por un validador confiable inyectado o un comando verificable que ate misión, tarea, dueño y aprobación persistida vigente. Sin adaptador confiable, fallar cerrado. No aceptar identidad o aprobación desde prompt, cuerpo, headers o agente.

### C01-R2 — P0 — replay exitoso vuelve a invocar y cobrar

Dos llamadas a `execute_agent_call` con la misma misión y `task_id='T-SAME'` dieron:

```json
{
  "first_ok": true,
  "second_ok": true,
  "provider_calls": 2,
  "requests_after_first": 1,
  "requests_after_second": 2,
  "spent_after_first": 0.000195,
  "spent_after_second": 0.00039
}
```

El control solo bloquea replays cuando una reserva queda INDETERMINADA. Un resultado exitoso no se persiste como respuesta terminal idempotente en el gateway.

Impacto: un reenvío/reinicio puede duplicar gasto y resultado si llega directamente al gateway. El bloqueo de repetición del runtime SIMULADA no prueba este nuevo camino real.

Corrección: la misma clave lógica debe devolver exactamente la respuesta terminal persistida, o rechazar sin nueva llamada y sin efecto. Un reintento transitorio confirmado sigue siendo un intento distinto, acotado y registrado; no debe confundirse con replay externo.

## Hallazgo adicional para la corrección

Una excepción ADK con código 401/403 se normaliza con `usage_confirmed=False`; el gateway sale por “uso indeterminado” antes de la rama PERMISSION_DENIED y retiene la reserva. Verificar en el SDK instalado si esos rechazos garantizan cero generación/uso. Solo si existe garantía oficial se pueden confirmar a cero; de lo contrario conservar la reserva, pero devolver el estado seguro adecuado sin filtrar detalle.

## Dictamen

COR-CIERRE-01 mejora sustancialmente el adaptador, pero queda **NO_ACEPTADA** hasta cerrar C01-R1 y C01-R2 con pruebas negativas que comprueben cero efectos indebidos. No enviar aún a Copilot como versión final: su revisión debe hacerse después de la corrección, conforme al flujo acordado.

El producto completo sigue bloqueado además por R02–R14 del informe `REVISION-ANTIGRAVITY-2026-08-31.md`; este dictamen solo cubre la pieza COR-CIERRE-01.

