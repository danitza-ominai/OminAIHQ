# OminAI HQ - Documento de Entrega para Competencia y Hackathon (PZ-015B)

**Nombre del Proyecto:** OminAI HQ  
**Propósito:** Oficina digital agéntica con gobernanza estricta para transformar una misión de negocio en un *Venture Build Package* (VBP) auditable y listo para ejecución.  
**Autoridad Humana:** Niko (A0) - Operador Humano Exclusivo con poder de decisión y veto.  
**Pila Tecnológica:** Python 3.11, Google Gemini 2.5 Pro / Flash, SQLite (ACID local), HTML5/CSS3 accesible, Google Cloud Run.

---

## 1. Problema que Resuelve

La mayoría de los sistemas multi-agente actuales operan como cajas negras: sufren de bucles infinitos, gasto descontrolado de tokens, alucinaciones sin fuentes verificables y autoaprobaciones riesgosas de tareas críticas.

**OminAI HQ** resuelve esto mediante un marco de gobernanza determinista basado en:
1. **Dos Puertas Humanas Infranqueables (Human-in-the-Loop):**
   - **Puerta 1 (Plan):** Autorización humana obligatoria del plan de 4 tareas antes de activar a los especialistas.
   - **Puerta 2 (VBP Final):** Dictamen independiente de Governance Risk (`PASA`/`NO_PASA`) y aprobación final humana del paquete de negocio.
2. **Límites Presupuestarios y de Intento Estrictos:** Techo duro de $25.00 USD y máximo 15 peticiones de agente por misión.
3. **Trazabilidad y Verificabilidad Criptográfica:** Huellas canónicas SHA-256 en cada fuente, resultado, dictamen y aprobación.
4. **Cero Exposición de Chain-of-Thought (Zero-CoT):** Razonamiento interno aislado y trazas minimizadas.

---

## 2. Los 5 Agentes Especialistas

1. **Chief of Staff:** Aclara la misión humana, desglosa el plan secuencial de tareas y consolida el VBP.
2. **Research Evidence Analyst:** Investiga fuentes autorizadas, valida claims normativos/mercado y previene SSRF e inyecciones de prompt.
3. **Product Architect:** Define requerimientos funcionales/técnicos basados exclusivamente en evidencias validadas.
4. **Delivery Planner:** Estructura el cronograma de ejecución en 3 fases y mapa de dependencias.
5. **Governance Risk:** Evalúa objetivamente el VBP candidato emitiendo un dictamen vinculante `PASA` / `NO_PASA`.

---

## 3. Instrucciones de Reproducción Local

### Requisitos
- Python 3.11 o superior.

### Ejecución de la Suite Completa de Pruebas
```bash
# Ejecutar las 231 pruebas de la suite de validacion
python -B -m unittest discover -s tests -v
```

### Ejecución del Flujo Demostrativo
```bash
# Ejecutar recorrido completo de 2 puertas y 5 agentes
python -B -m app.demo_vbp_flow
```
