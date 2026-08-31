# COR-CIERRE-01 — Corrección del proveedor entregado

Fecha: 31-08-2026. Estado: PROPUESTA_PENDIENTE_DE_AUTORIZACION_HUMANA.
Constructor de la pieza entregada: Antigravity. Corrector propuesto: Codex. Revisor final: GitHub Copilot, sin editar.

## Objetivo y alcance exacto

Corregir R01/R12 y la parte de dependencias de R13 del informe REVISION-ANTIGRAVITY-2026-08-31.md: el proveedor ya creado no utiliza ADK y es rechazado por su gateway; configuración/modelo, límites y dependencias no coinciden con el encargo.

Esta ficha no autoriza construir los roles, persistencia cloud, identidad ni nueva UI en paralelo. No declara terminados los demás hallazgos. Sustituir el transporte defectuoso del proveedor existente por el ADK solicitado no amplía el producto aprobado.

## Ocho archivos permitidos, solo después de autorización

1. `app/adk_provider.py` — corregir implementación ADK y normalización de respuesta/errores/uso.
2. `app/agent_gateway.py` — seleccionar modo de forma explícita y permitir únicamente proveedor real configurado/autorizado; conservar pre-reserva, límites y rechazo seguro.
3. `app/runtime_config.py` — modelo/configuración reales separados de fixtures, límites y precios con fuente/fecha.
4. `tests/test_adk_provider.py` — tests de contrato del adaptador, sin red facturable.
5. `tests/test_agent_gateway.py` — pruebas de gateway con proveedor inyectado, rechazos y efectos en ledger.
6. `pyproject.toml` — dependencia opcional ADK, preservando extras existentes.
7. `deploy/requirements.lock` — dependencias realmente resueltas y fijadas; nunca inventar versiones transitivas.
8. `Dockerfile` — consumir lock/configuración de dependencia corregida. No desplegar.

Todos los demás archivos de producto están prohibidos en este pase; también AGENTS.md, TEAM-WORKFLOW.md, contratos, corpus REQUISITOS, fixtures ajenos, bases existentes, memoria y el ENTREGA.md agregado en raíz. La evidencia de coordinación puede añadirse con nombre específico de este pase. Capturar hashes antes y después; no hacer ediciones simultáneas con Antigravity/Copilot.

## Fuentes

- Encargo integral H04/H14/H15 y su apartado 4: contiene localizadores de REQUISITOS, reglas de función/agente, instrucciones acotadas y evaluación.
- CONTRATO-MVP-v1.md, secciones 5, 10, 11.4, 11.8 y 11.9.
- Informe de revisión y reproducciones de esta entrega.
- Verificar APIs/versiones vigentes en documentación oficial antes de elegir llamadas del SDK. La propuesta previa google-adk==2.8.0 y gemini-3.5-flash no demuestra que el SDK esté instalado o probado.

## Pruebas y aceptación técnica de este pase

- Gateway deja de rechazar por clase a un proveedor real correctamente configurado; test con cliente inyectado demuestra la llamada y la reconciliación.
- Ausencia de modo, credencial, modelo/tarifa permitidos o autorización provoca fallo cerrado, sin llamada ni fallback ficticio.
- Reserva y validación antes de invocar; límites de generación efectivos y entrada acotada; consumo incluye pensamiento como conteo, nunca su contenido.
- Timeout/resultado incierto retiene reserva y no duplica la llamada; autenticación inválida no reintenta; máximo un reintento transitorio conforme al contrato; SDK no añade intentos ocultos.
- JSON/esquema inválido y contenido sensible son rechazados. No incluir claves/URLs con secretos en errores, logs, artefactos ni pruebas.
- Modelo/mode/usage distinguen SIMULADA, REAL_NO_VERIFICADA y evidencia real cuando exista; no llamar REAL_VERIFICADO a un mock.
- Suite completa sigue pasando; ejecutar además negativos de presupuesto, concurrencia y reinicio.
- La prueba real facturable queda separada: requiere credencial administrada por Niko y autorización de gasto. Los tests offline no certifican la ejecución real ni la entrega completa.

## Dependencias y autorizaciones externas

Editar los ocho archivos no autoriza instalar dependencias. Si el SDK no está disponible, preparar primero cambios y pruebas reproducibles; proponer después una instalación concreta y aislada con paquete/versiones elegidas y directorio nuevo. No instalar globalmente, leer secretos, gastar, desplegar ni publicar por inferencia.

AGENTS exige autorización humana de archivos exactos. La autorización de este pase debe ser una nueva decisión explícita; no borra rondas anteriores ni concede rondas ilimitadas. Si ya se agotó el máximo previo, la misma decisión debe autorizar expresamente este pase adicional. Copilot mantiene revisión final independiente, sin implementar.

Texto para Niko si aprueba:
“Autorizo COR-CIERRE-01: Codex puede corregir exclusivamente los ocho archivos enumerados, para R01/R12 y dependencias de R13. Autorizo este pase adicional sin reiniciar el historial de rondas. Sin instalaciones, gasto, despliegue ni publicación.”

