# OminAI HQ: Oficina Digital Agéntica de Alta Gobernanza

**Guía Integral y Fundamentos del Proyecto para Análisis en NotebookLM**  
**Versión:** 1.0 (Hackathon Edition)  
**Autoridad del Proyecto:** Usuario Humano (A0)  
**Clasificación:** Sistema Multi-Agente con Gobernanza Humana (Human-in-the-Loop)  

---

## 1. Resumen Ejecutivo e Identidad del Proyecto

### 1.1 ¿Qué es OminAI HQ?
**OminAI HQ** es una oficina digital agéntica diseñada para transformar una misión estratégica de negocio en un **Venture Build Package (VBP)** estructurado, validado y auditable. 

A diferencia de los asistentes de chat convencionales o los sistemas multi-agente sin control que operan como 'cajas negras', OminAI HQ introduce un paradigma de **ingeniería agéntica determinista**:
- Cada interacción está regida por contratos de datos inmutables (**JSON Schema Draft 2020-12**).
- La progresión entre fases requiere la autorización explícita del usuario humano a través de un sistema de **dos puertas obligatorias (Human-in-the-Loop)**.
- El resultado final es un paquete canónico en formato Markdown con **18 secciones obligatorias** e integridad criptográfica sellada con **SHA-256**.

### 1.2 Jerarquía de Identidad y Separación de Alcance
Para mantener claridad operativa y de marca, el proyecto define separaciones estrictas:
* **Ominai:** La compañía paraguas / entidad matriz.
* **OminAI HQ:** El producto actual participante del hackathon (la oficina agéntica de estructuración de misiones a VBP).
* **OminAI Business OS:** Producto independiente para gestión operativa de negocios (fuera del alcance del MVP).
* **Omi:** Agente exclusivo de Business OS (no forma parte de OminAI HQ).
* **OminaiTech Engine:** Motor de integración futura (fuera del alcance del MVP).

---

## 2. El Problema y la Oportunidad

### 2.1 Problemas de los Sistemas de IA Actuales
1. **Falta de Rendición de Cuentas (Black Box):** Los agentes autónomos toman decisiones sin registro auditable ni justificación de fuentes.
2. **Alucinaciones y Supuestos No Verificados:** Mezcla indistinta de hechos comprobados, opiniones del modelo y datos inventados.
3. **Pérdida del Control Humano (Lack of Governance):** Agentes que avanzan sin límites, gastan presupuestos descontrolados o ejecutan acciones irreversibles sin supervisión.
4. **Almacenamiento Inseguro de Razonamiento:** Fuga de secretos o exposición de 'Chain-of-Thought' (CoT) crudo y no estructurado.

### 2.2 La Solución de OminAI HQ
OminAI HQ resuelve estos desafíos mediante:
* **Gobierno Humano Estricto (A0 Authority):** El usuario humano es la máxima autoridad; el sistema propone, pero el humano decide y aprueba.
* **Separación Epistémica de Evidencia:** Todo dato en el VBP clasifica explícitamente si es un *hecho comprobado*, un *supuesto*, una *propuesta*, una *decisión aprobada* o un *pendiente*.
* **Control Presupuestario y de Recursos (Ledger Transaccional):** Control estricto con reserva previa de microdólares, alerta al 70%, bloqueo duro al 90% y techo de gasto fijado en .00 USD.
* **Política Zero-CoT (Zero Chain-of-Thought):** No se almacena ni expone razonamiento no filtrado; solo se persisten acciones, herramientas, fuentes verificadas, decisiones y resultados resumidos.

---

## 3. Arquitectura del Sistema y Principios Fundamentales

`	ext
+-----------------------------------------------------------------------------+
|                      1. USUARIO HUMANO (Autoridad A0)                        |
|             Define Misión • Aprueba Puertas • Controla Presupuesto          |
+--------------------------------------+--------------------------------------+
                                       |
                   +-------------------+-------------------+
                   |                                       |
                   v                                       v
        +----------------------+               +----------------------+
        | PUERTA 1: PLAN       |               | PUERTA 2: VBP        |
        | Aprobación de Tareas |               | Dictamen de Riesgo y |
        | (Ventana 300s)       |               | Aprobación Canónica  |
        +----------+-----------+               +-----------+----------+
                   |                                       |
+------------------v---------------------------------------v------------------+
|                   2. HQ RUNTIME & CONTROL TRANSACCIONAL                     |
|  • Máquina de Estados Finita         • SQLite Transactional Ledger          |
|  • Contratos JSON Schema 2020-12     • Checkpoints y Reanudación Atómica    |
|  • Política Zero-CoT                 • Control de Microdólares (Techo )  |
+--------------------------------------+--------------------------------------+
                                       |
+--------------------------------------v--------------------------------------+
|                     3. ENJAMBRE DE AGENTES ESPECIALIZADOS                   |
|  +--------------------+  +---------------------+  +----------------------+  |
|  | 1. Intake          |  | 2. Planner          |  | 3. Evidence &        |  |
|  |    & Aclarador     |  |    & Estratega      |  |    Investigación     |  |
|  +--------------------+  +---------------------+  +----------------------+  |
|  +--------------------+  +---------------------+  +----------------------+  |
|  | 4. Product         |  | 5. Execution        |  | 6. Governance        |  |
|  |    & Alcance       |  |    & Roadmap        |  |    & Risk Dictamen   |  |
|  +--------------------+  +---------------------+  +----------------------+  |
+--------------------------------------+--------------------------------------+
                                       |
+--------------------------------------v--------------------------------------+
|             4. VENTURE BUILD PACKAGE (VBP) CANÓNICO EN MARKDOWN             |
|       18 Secciones Obligatorias • Integridad Criptográfica SHA-256          |
+-----------------------------------------------------------------------------+
`

### 3.1 Los Cuatro Principios de Diseño
1. **Determinismo sobre Magia:** Las funciones deterministas se resuelven con código; los modelos de lenguaje (LLMs) se usan exclusivamente donde se requiere razonamiento estructurado.
2. **Contratos Inmutables:** Ningún agente produce texto desestructurado como contrato de comunicación. Todos los intercambios cumplen esquemas JSON formales (mission, plan, evidence, checkpoint, vbp).
3. **Idempotencia y Reanudabilidad:** Una falla de red o corte del servidor no destruye el progreso. El estado se recupera desde el último checkpoint persistido en SQLite sin volver a facturar tareas ya concluidas.
4. **Seguridad y Cero Suposiciones:** El sistema aplica validación estricta de Host/Origin, protección CSRF y contexto de seguridad local obligatorio.

---

## 4. El Ciclo de Vida de una Misión: De la Idea al VBP

### Paso 1: Definición de Misión y Aclaración (Intake)
* El usuario ingresa una misión estratégica (ej. *'Lanzar una plataforma agéntica de auditoría fiscal para PYMEs'*).
* El agente **Intake & Clarifier** analiza la entrada, detecta ambigüedades, solicita clarificaciones clave y normaliza los objetivos.

### Paso 2: Generación del Plan y Puerta 1 (Gate 1)
* El agente **Planner & Strategist** descompone la misión en un Grafo Acíclico Dirigido (DAG) de tareas y dependencias, estimando costos y tiempos.
* **🛑 Puerta 1 (Aprobación Humana Obligatoria):**
  * Se abre una ventana de decisión de 300 segundos.
  * El usuario humano revisa las tareas propuestas y debe seleccionar: APROBADO, RECHAZADO o SOLICITAR_CAMBIOS.
  * **Ningún agente especialista puede iniciar sin la aprobación humana explícita del plan.**

### Paso 3: Ejecución Agéntica Especializada
Una vez autorizado el plan, se activan secuencialmente los especialistas:
1. **Evidence & Research Agent:** Recopila datos de mercado, competidores y normativas, asignando a cada hallazgo una fuente, fecha, nivel de confianza y limitaciones conocidas.
2. **Product & Scope Agent:** Traduce la evidencia en la definición funcional del producto, arquitectura base, historias de usuario y matriz de alcance (lo que está dentro y fuera del MVP).
3. **Execution & Roadmap Agent:** Define fases de desarrollo, hitos críticos, asignación de recursos, dependencias y criterios de aceptación verificables.

### Paso 4: Dictamen de Riesgos y Puerta 2 (Gate 2)
* El agente **Governance & Risk** actúa como un auditor independiente. Evalúa el paquete consolidado emitiendo un dictamen formal:
  * PASA (Cumple todos los requisitos y criterios de seguridad).
  * PASA_CON_CONDICIONES (Requiere mitigación explícita de riesgos identificados).
  * NO_PASA (Bloquea la finalización si existen violaciones referenciales o falta de evidencia).
* **🛑 Puerta 2 (Aprobación Final del VBP):**
  * El usuario humano revisa el dictamen de riesgo y autoriza formalmente la emisión del paquete.

### Paso 5: Generación y Exportación Canónica del VBP
* Se compila el **Venture Build Package (VBP)** en un único archivo Markdown estructurado con sus 18 secciones.
* Se calcula y adjunta la huella digital criptográfica **SHA-256** para certificar su inmutabilidad y trazabilidad.

---

## 5. Estructura Canónica del Venture Build Package (18 Secciones)

El VBP exportable contiene estrictamente las siguientes 18 secciones normativas:

1. **Resumen Ejecutivo** *(Executive Summary)*
2. **Declaración de Misión y Objetivos** *(Mission & Strategic Objectives)*
3. **Validación de Mercado y Evidencia** *(Market Evidence & Sources)*
4. **Propuesta de Valor y Diferenciación** *(Value Proposition)*
5. **Público Objetivo y Arquetipos de Usuario** *(Target Audience & Personas)*
6. **Alcance del MVP y Exclusiones Explícitas** *(Scope & Non-Goals)*
7. **Historias de Usuario y Criterios de Aceptación** *(User Stories & Acceptance Criteria)*
8. **Arquitectura Técnica y Decisiones de Diseño** *(System Architecture)*
9. **Contratos de Datos e Interfaces** *(Data Contracts & Schemas)*
10. **Plan de Fases y Hoja de Ruta** *(Roadmap & Milestones)*
11. **Estimación Presupuestaria y Asignación de Recursos** *(Budget & Cost Allocation)*
12. **Matriz de Riesgos y Planes de Mitigación** *(Risk Matrix & Mitigations)*
13. **Gobierno, Seguridad y Cumplimiento Normativo** *(Governance & Security)*
14. **Métricas Clave de Éxito (KPIs / OKRs)** *(Success Metrics)*
15. **Estrategia de Salida al Mercado (GTM)** *(Go-To-Market Strategy)*
16. **Plan de Pruebas y Validación** *(Verification & Testing Strategy)*
17. **Historial de Decisiones y Auditoría** *(Audit Trail & Decision Log)*
18. **Apéndice de Evidencias y Firma Digital SHA-256** *(Evidence Appendix & Cryptographic Digest)*

---

## 6. Stack Tecnológico y Ecosistema Google Cloud

* **Modelos de Inteligencia Artificial:**
  * Gemini 3.5 Flash / Gemini 3.5 Pro / Gemini 3.7 vía Google Gen AI SDK para razonamiento agéntico y extracción de evidencia.
  * Gemma 2 para tareas locales complementarias.
* **Infraestructura de Nube (Google Cloud):**
  * Cloud Run: Despliegue de microservicios contenerizados de alta disponibilidad.
  * Google Cloud Storage (GCS): Almacenamiento seguro de artefactos y paquetes VBP canónicos.
  * Firestore: Persistencia NoSQL para sincronización de misiones y auditoría en la nube.
* **Núcleo del Sistema y Backend:**
  * Python 3.11+ (Biblioteca estándar para máxima estabilidad y portabilidad).
  * JSON Schema Draft 2020-12 para validación estricta de contratos.
  * SQLite 3 para ledger transaccional local y máquina de estados.
* **Frontend y Experiencia de Usuario:**
  * HTML5 Semántico + CSS3 de Alto Contraste (Accesibilidad WCAG).
  * Vanilla JavaScript con arquitectura reactiva basada en eventos.
  * Módulo Bilingüe Nativo (ES / EN).

---

## 7. Preguntas Clave para Audio Overview y Análisis en NotebookLM

### P1: ¿Por qué OminAI HQ no permite que los agentes actúen de forma 100% autónoma?
> **R:** Porque en aplicaciones empresariales y de venture building, la autonomía sin límites genera costos desmedidos, acciones no deseadas y alucinaciones críticas. OminAI HQ adopta el principio de *Gobernanza A0*, donde la IA es un enjambre de análisis de clase mundial, pero la toma de decisiones finales y compromisos presupuestarios recaen siempre en el ser humano.

### P2: ¿Qué significa la política Zero-CoT (Zero Chain-of-Thought)?
> **R:** Significa que las reflexiones crudas o razonamientos desordenados del modelo no se persisten en base de datos ni se exponen a terceros. Esto previene fugas de información confidencial y asegura que la auditoría solo contenga hechos estructurados, fuentes verificables y decisiones formales.

### P3: ¿Cómo asegura OminAI HQ que el contenido del VBP no sea alterado tras su aprobación?
> **R:** Al aprobarse la Puerta 2, el sistema genera la representación canónica del documento y calcula su huella criptográfica mediante el algoritmo SHA-256. Cualquier cambio posterior en el texto invalida la firma digital, garantizando trazabilidad absoluta ante inversores, auditores o equipos técnicos.

### P4: ¿Cuál es la diferencia entre OminAI HQ y OminAI Business OS?
> **R:** **OminAI HQ** es la oficina de planificación y estructuración que convierte misiones en planes de negocio ejecutables (VBPs). **OminAI Business OS** es el producto futuro diseñado para la operación y gestión diaria del negocio ya constituido. Son productos desacoplados e independientes.
