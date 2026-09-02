# OminAI HQ - Estado vigente de release gates del MVP (PZ-015A)

Fecha de corte: 2026-09-02. Versión técnica evaluada: `0.1.0`.

Este documento registra el estado técnico actual conforme a
`CONTRATO-MVP-v1.md`. No constituye autorización de release, despliegue ni
aceptación humana integral.

## 1. Evidencia automatizada disponible

- Suite completa local: `308/308` pruebas pasan en el entorno funcional.
- El recorrido cubierto por esa suite usa fixtures, dobles, clientes inyectados,
  almacenamiento en memoria y ejecución `SIMULADA` según el componente.
- Hay pruebas de flujo local, SQLite, aprobaciones humanas controladas, límites,
  auditoría, exportación del VBP y evaluación adversarial reproducible.
- El conteo de pruebas no demuestra por sí solo cobertura completa de RF-001 a
  RF-030, RNF-001 a RNF-015 y CT-001 a CT-017. Falta una matriz ejecutable que
  vincule cada control aplicable con evidencia reproducible.

## 2. Snapshot de gates

| Gate | Evidencia actual | Estado |
|---|---|---|
| Flujo local Misión → Plan → VBP | Recorrido automatizado con datos sintéticos, dos puertas separadas y exportación validada | `VERIFICADO_EN_SIMULADA` |
| Persistencia y reanudación local | Pruebas con SQLite, reinicio, checkpoints e idempotencia | `VERIFICADO_EN_SIMULADA` |
| Límites, permisos y Zero-CoT | Pruebas positivas y negativas del runtime local y del gateway | `VERIFICADO_EN_SIMULADA` |
| Evaluación reproducible | Harness, checksum, casos adversariales y separación declarada del holdout | `VERIFICADO_EN_SIMULADA` |
| Gemini mediante Google ADK | Módulo presente; pruebas offline con ejecutor inyectado | `PENDIENTE_DE_EVIDENCIA_REAL` |
| Cloud Run | Entrypoint, Dockerfile y manifiesto de ejemplo presentes; sin servicio desplegado demostrado | `PENDIENTE_DE_EVIDENCIA_REAL` |
| Firestore | Adaptador presente; implementación observada en memoria | `PENDIENTE_DE_EVIDENCIA_REAL` |
| Google Cloud Storage | Adaptador presente; implementación observada en memoria | `PENDIENTE_DE_EVIDENCIA_REAL` |
| Cobertura integral RF/RNF/CT | No existe aquí una matriz ejecutable completa por control | `NO_CERRADO` |
| Aceptación humana integral del MVP | Solo constan aceptaciones por pieza | `NO_CERRADO` |

## 3. Condiciones antes de release o despliegue

- Obtener autorización humana expresa para cualquier uso de credenciales,
  servicio externo, gasto o despliegue.
- Ejecutar y registrar una integración real con Gemini/ADK.
- Construir y demostrar el servicio en Cloud Run con identidad y límites
  observables.
- Verificar persistencia real en Firestore y Google Cloud Storage.
- Completar la matriz RF/RNF/CT y resolver los controles aplicables pendientes.
- Realizar revisión independiente y decisión humana final sobre la versión exacta.

## 4. Dictamen vigente

El estado general es `NO_CERRADO`. La evidencia local `SIMULADA` es válida para
los comportamientos que ejercita, pero no autoriza inferir integración real,
operación productiva, despliegue, cobertura contractual total ni aceptación
humana integral. Un resultado automatizado verde no sustituye esa decisión.
