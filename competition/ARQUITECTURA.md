# OminAI HQ - Arquitectura Técnica del Sistema (PZ-015B)

Este documento describe la arquitectura modular, contratos de datos, separación de capas y políticas de seguridad de OminAI HQ conforme al contrato rector `CONTRATO-MVP-v1.md`.

---

## 1. Diagrama de Flujo y Puertas de Gobernanza

```
[ Usuario Humano (A0) ]
        │
        ▼ (1. Intake)
[ Chief of Staff ] ───► Propuesta de Plan (4 Tareas)
                              │
                              ▼
               ┌──────────────────────────────┐
               │  PUERTA 1: DECISIÓN DEL PLAN │ ◄── [ Aprobación Humana Obligatoria (A0) ]
               │  (TTL: 300s, SHA-256)        │
               └──────────────┬───────────────┘
                              │ APROBADA
                              ▼
               ┌──────────────────────────────┐
               │     MOTOR DE EJECUCIÓN       │
               │   (Secuencia Estricta)       │
               └──────────────┬───────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
 [ Tarea 1: Research ] ──► [ Tarea 2: Architect ] ──► [ Tarea 3: Planner ]
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                       [ Chief of Staff ]
                   (Consolidación de VBP)
                              │
                              ▼
                   [ Tarea 4: Governance Risk ]
                   (Dictamen: PASA / NO_PASA)
                              │
                              ▼
               ┌──────────────────────────────┐
               │  PUERTA 2: DECISIÓN DEL VBP  │ ◄── [ Aprobación Humana Final (A0) ]
               │  (Venture Build Package)     │
               └──────────────┬───────────────┘
                              │ APROBADA
                              ▼
                     [ Estado FINALIZADA ]
                   (VBP Exportado y Sellado)
```

---

## 2. Componentes Principales

1. **`app/hq_runtime.py` (HQRuntime):** Contenedor de composición y cableado de dependencias entre pasarela de modelos, repositorios, gestor de memoria y agentes.
2. **`app/agent_gateway.py` (AgentGateway):** Pasarela unificada hacia Google Gemini con control de presupuestos ($25 USD), conteo de intentos (15 máx) y filtro de saneamiento Zero-CoT.
3. **`app/human_approvals.py` (HumanApprovalEngine):** Motor transaccional de puertas de decisión humana con TTL de 300s, huellas canónicas e idempotencia.
4. **`app/mission_controls.py` (MissionControlManager):** Controlador de estados de misión (`PAUSADA`, `CANCELADA`, `EN_EJECUCION`) y reanudación segura.
5. **`app/local_repository.py` (LocalRepository):** Persistencia ACID en SQLite local con bloqueos de concurrencia y transacciones atómicas.
6. **`app/sanitized_dossier.py` (SanitizedDossierManager):** Constructor de expedientes públicos con anonimización de rutas y revocación instantánea.
7. **`app/http_api.py` (LocalAPIRouter):** Adaptador HTTP loopback seguro para la interfaz web.
