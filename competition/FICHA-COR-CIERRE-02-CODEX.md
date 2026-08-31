# COR-CIERRE-02 — Autoridad real e idempotencia del gateway

Fecha: 2026-08-31. Estado: PROPUESTA_PENDIENTE_DE_AUTORIZACION_HUMANA.
Corrector propuesto: Codex. Revisor posterior: GitHub Copilot, sin editar.

## Objetivo cerrado

Corregir exclusivamente C01-R1 y C01-R2 del informe `REVISION-COR-CIERRE-01-CODEX.md`, y el tratamiento seguro asociado de 401/403 si la semántica oficial instalada lo permite. No conectar todavía los cinco roles, Firestore/GCS, Cloud Run ni UI.

## Exactamente cuatro archivos permitidos

1. `app/adk_provider.py`
2. `app/agent_gateway.py`
3. `tests/test_adk_provider.py`
4. `tests/test_agent_gateway.py`

Todos los demás archivos están prohibidos, incluidos runtime_config, local_repository, pyproject, lock, Dockerfile, contratos, AGENTS/TEAM-WORKFLOW, corpus, web, deploy, bases y fixtures ajenos. No crear capacidades nuevas ni relajar límites.

## Criterios ejecutables

- `real_execution_authorized=True` por sí solo deja de autorizar. Sin validación confiable de un mandato concreto: 0 reservas, 0 llamadas, 0 gasto y error seguro.
- El mandato validado queda ligado al menos a misión, tarea, propietario y aprobación/decisión persistida vigente, sin recibir autoridad desde modelo, prompt, body o headers. Dado que local_repository/human_approvals están fuera de alcance, usar una interfaz de validador inyectable y fallar cerrado; no inventar persistencia dentro del gateway.
- Un replay externo con la misma clave lógica después de éxito hace 0 llamadas adicionales y 0 gasto adicional; devuelve exactamente el resultado persistido si ya existe a través de la interfaz inyectada, o rechaza de forma determinista. No guardar respuestas sensibles en una caché volátil presentada como durabilidad.
- Si lograr idempotencia durable exige modificar repositorio/runtime, detener este lote y proponer esos archivos exactos; no simularla en memoria.
- Mantener como máximo dos intentos para un transitorio confirmado y un único intento ante resultado/uso indeterminado.
- Autenticación 401/403: no reintentar; no exponer secreto. Reconciliar a cero únicamente con evidencia contractual del SDK/proveedor; en duda, retener reserva.
- Pruebas negativas verifican llamadas, reservas, gasto y estado antes/después. Suite completa 303+ sin regresión.
- SDK real, Docker, credenciales, llamada facturable y despliegue permanecen fuera de alcance.

## Decisión necesaria

AGENTS exige una autorización humana nueva con archivos exactos. Además, el historial ya registra rondas previas; esta decisión debe autorizar expresamente el pase adicional sin reiniciar ese historial.

Texto exacto si Niko aprueba:

“Autorizo COR-CIERRE-02 como pase adicional: Codex puede corregir exclusivamente app/adk_provider.py, app/agent_gateway.py, tests/test_adk_provider.py y tests/test_agent_gateway.py para C01-R1/C01-R2 y el tratamiento seguro de 401/403. No autorizo otros archivos, instalaciones, credenciales, llamadas reales, gasto, Docker, despliegue ni publicación.”

