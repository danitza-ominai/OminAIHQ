# OminAI HQ - Matriz de Capacidades, Limitaciones y Evidencias (PZ-015B)

Esta matriz declara de forma transparente el estado real de cada capacidad del sistema, diferenciando lo implementado, lo simulado para pruebas offline y las limitaciones conocidas conforme a CONTRATO-MVP-v1.md.

---

## 1. Matriz de Capacidades

| Capacidad | Estado | Evidencia / Módulo | Descripción |
|---|---|---|---|
| **Admisión de Misión (Intake)** | IMPLEMENTADO | `app/demo_intake.py` | Admisión con validación de tipos y generación de IDs |
| **Pasarela de Modelos Gemini** | IMPLEMENTADO | `app/agent_gateway.py` | Soporte Gemini 2.5 Pro / Flash con mocks y fallback |
| **Control de Presupuesto ($25 USD)** | IMPLEMENTADO | `app/runtime_config.py` | Techo duro de gasto y pausas en umbrales 70%, 90%, 100% |
| **Límite de Solicitudes (15 máx)** | IMPLEMENTADO | `app/agent_gateway.py` | Límite acumulativo por misión |
| **Puerta 1 (Aprobación del Plan)** | IMPLEMENTADO | `app/human_approvals.py` | TTL 300s, huella SHA-256, bloqueo de autoaprobación de IA |
| **Puerta 2 (Aprobación del VBP)** | IMPLEMENTADO | `app/human_approvals.py` | Independiente de Puerta 1, vinculada a dictamen de gobernanza |
| **5 Agentes Especialistas** | IMPLEMENTADO | `app/chief_of_staff.py`, `app/research_analyst.py`, etc. | Coordinación, investigación, arquitectura, delivery y riesgo |
| **Persistencia ACID Transaccional** | IMPLEMENTADO | `app/local_repository.py` | SQLite con bloqueo de concurrencia y atomicidad |
| **Memoria Aprobada y Retención** | IMPLEMENTADO | `app/approved_memory.py`, `app/data_lifecycle.py` | Memoria declarativa entre misiones y purga segura |
| **Interfaz Web Accesible** | IMPLEMENTADO | `web/index.html`, `web/styles.css`, `web/app.js` | HTML5/CSS3 accesible con protección contra XSS |
| **Despliegue Cloud Run** | CONFIGURADO | `Dockerfile`, `deploy/cloudrun.example.yaml` | Imagen no-root minScale 0 / maxScale 1 |
| **Despliegue en Vivo en GCP** | PENDIENTE | `deploy/VERIFICACION-DEMO.md` | Pendiente de autorización expresa humana y gasto (A0) |

---

## 2. Limitaciones Conocidas del MVP

1. **Monousuario Local:** Diseñado para un único operador local con rol de autoridad (A0).
2. **Una Misión Concurrente:** El repositorio bloquea la creación de misiones simultáneas activas para garantizar aislamiento transaccional.
3. **Demo Pública:** En modo público, se limita a un máximo de 5 ejecuciones diarias con cuota global.
