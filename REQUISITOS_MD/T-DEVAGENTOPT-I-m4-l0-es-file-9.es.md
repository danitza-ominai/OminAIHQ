# **Qué lograste** 

## **Módulo 1: Redacción de instrucciones avanzadas** 

✅ Aprendiste 5 patrones de instrucción reutilizables (identidad, misión, metodología, límites y demostración con varios ejemplos). 

✅ Creaste patrones neutrales en cuanto al dominio con plantillas y [marcadores de posición]. ✅ Implementaste ejemplos de varios dominios en comercio electrónico, educación, finanzas y salud. 

✅ Diseñaste instrucciones con la organización en Markdown para mayor claridad. 

**Información clave:** Las instrucciones son especificaciones de comportamiento integrales. Usa patrones reutilizables con plantillas para crear agentes profesionales en cualquier dominio. 

## **Módulo 2: Resultados estructurados** 

- ✅ Definiste esquemas de Pydantic BaseModel para obtener resultados JSON predecibles. 

- ✅ Utilizaste output_key para pasar datos en flujos de trabajo. 

- ✅ Entendiste la integridad del esquema: solo los campos definidos aparecen en el resultado. ✅ Aprendiste que los resultados estructurados funcionan tanto para los agentes raíz como para los agentes secundarios intermedios. 

**Información clave:** Los resultados estructurados cierran la brecha entre la IA en lenguaje natural y la integración del sistema. El esquema es un contrato que define exactamente lo que necesitas. 

## **Módulo 3: Elección y configuración de modelos** 

- ✅ Seleccionaste los modelos de forma estratégica: comenzaste con Pro para crear prototipos y aplicaste optimizaciones con Flash. 

- ✅ Estableciste la configuración de seguridad con GenerateContentConfig y SafetySetting. 

- ✅ Utilizaste los rangos de temperatura para diferentes tareas (de 0.0 a 0.3 para tareas fácticas y de 0.8 a 1.0 para tareas creativas). 

✅ Aprendiste patrones de precios y selección de modelos de Vertex AI. 

**Información clave:** Comienza con Gemini Pro para modelos de referencia de calidad y creación de prototipos. Utiliza Flash para optimización de costos y velocidad después de realizar un análisis de brechas. 

## **Módulo 4: Planificación para tareas complejas** 

- ✅ Habilitaste el razonamiento de varios pasos con BuiltInPlanner y ThinkingConfig. 

- ✅ Entendiste los enfoques de planificación y de múltiples agentes. ✅ Comparaste el resultado de la planificación con ejemplos concretos (comprar un auto frente a alquilarlo). 

- ✅ Aprendiste cuándo utilizar BuiltInPlanner (Gemini) y PlanReActPlanner (modelos que no son de Gemini). 

**Información clave:** La planificación transforma a los agentes reactivos en pensadores 

estratégicos. Utiliza BuiltInPlanner para modelos de Gemini con capacidades de pensamiento. Las instrucciones simples son suficientes, ya que la planificación agrega el razonamiento estructurado de forma automática. 

# **Aplicaciones reales** 

Con estas habilidades, ahora puedes crear lo siguiente: 

## **Sistemas de atención al cliente** 

from pydantic import BaseModel, Field 

class TicketOutput(BaseModel): ticket: dict = Field(description="Detalles del ticket") priority: str = Field(description="Nivel de prioridad") 

LlmAgent( model="gemini-2.5-flash", instruction="[Personalidad detallada con límites]", planner=BuiltInPlanner( thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=1024) ), output_schema=TicketOutput ) 

## **Canalizaciones de procesamiento de datos** 

from pydantic import BaseModel, Field from typing import List 

class AnalysisOutput(BaseModel): insights: List[str] = Field(description="Información clave") metrics: dict = Field(description="Métricas de rendimiento") LlmAgent( model="gemini-2.5-pro", instruction="[Framework de análisis]", output_schema=AnalysisOutput ) 

## **Automatización de flujos de trabajo** 

LlmAgent( model="gemini-2.5-flash", instruction="[Reglas del proceso]", output_key="approved", generate_content_config=types.GenerateContentConfig( temperature=0.2, safety_settings=[...] 

) ) 

## **Asistentes educativos** 

LlmAgent( model="gemini-2.5-pro", instruction="[Metodología de enseñanza]", 

planner=BuiltInPlanner( thinking_config=types.ThinkingConfig(include_thoughts=False, thinking_budget=2048) ), generate_content_config=types.GenerateContentConfig(temperature=0.5) ) 

# **Lista de verificación de prácticas recomendadas** 

## ✅ **Redacción de instrucciones** 

Utiliza los cinco patrones reutilizables: identidad, misión, metodología, límites y ejemplos. 

Crea plantillas genéricas con [marcadores de posición] que permitan la adaptabilidad a diferentes dominios. 

Define una personalidad clara con experiencia específica. Establece límites explícitos (listas de lo que nunca o siempre se debe hacer). Incluye 2 o 3 demostraciones con varios ejemplos en este formato: entrada → resultado. Utiliza la estructura Markdown para facilitar la lectura. 

## ✅ **Selección del modelo** 

Comienza con Gemini 2.5 Pro para crear prototipos y modelos de referencia de calidad. Realiza optimizaciones con Gemini 2.5 Flash tras analizar las brechas para la producción. 

Establece una configuración de seguridad adecuada para tu público. Establece la temperatura según la tarea: 0.0-0.3 (fáctica), 0.4-0.7 (equilibrada), 0.8-1.0 (creativa). 

## ✅ **Planificación** 

Habilita BuiltInPlanner para modelos de Gemini con tareas de varios pasos. Utiliza PlanReActPlanner para modelos que no sean de Gemini. Configura ThinkingConfig con include_thoughts=True para la depuración. Establece thinking_budget de forma adecuada (lo normal es entre 512 y 2,048 tokens). Aplica restricciones realistas en las instrucciones. 

Utiliza una temperatura más baja (0.2-0.3) para una planificación sistemática. 

## ✅ **Resultados estructurados** 

Define esquemas de Pydantic BaseModel (en lugar de diccionarios). Incluye TODOS los campos necesarios en el esquema (ya que solo aparecerán los campos definidos). Utiliza Field(descripción=…) para guiar el LLM. Utiliza output_key para pasar datos entre agentes. Maneja campos opcionales con Optional[T] y valores predeterminados. Valida los resultados antes de pasar a la etapa de producción. 

# **Referencia de patrones de código** 

## **Patrón 1: Agente de servicios profesionales** 

from google.adk.agents import LlmAgent, BuiltInPlanner from google.genai import types from pydantic import BaseModel, Field 

class ServiceResponse(BaseModel): response: str = Field(description="La respuesta al usuario") action_required: bool = Field(description="Si se debe realizar una acción") metadata: dict = Field(default={}, description="Metadatos adicionales") professional_agent = LlmAgent( model="gemini-2.5-flash", name="service_pro", instruction=\"\"\" # PERSONALIDAD Eres [Nombre], te desempeñas como [rol] y cuentas con [experiencia]. # LÍMITES Nunca: [Lista de restricciones] Siempre: [Lista de requisitos] # EJEMPLOS [Demostraciones con varios ejemplos] \"\"\", planner=BuiltInPlanner( thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=1024) ), output_schema=ServiceResponse, generate_content_config=types.GenerateContentConfig( temperature=0.5, safety_settings=[ types.SafetySetting( category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE ) ] ) ) 

## **Patrón 2: Canalización de extracción de datos** 

from pydantic import BaseModel, Field from typing import List from google.genai import types 

class Entity(BaseModel): type: str = Field(description="Tipo de entidad") value: str = Field(description="Valor de la entidad") confidence: float = Field(description="Puntuación de confianza 0-1") 

class ExtractionOutput(BaseModel): entities: List[Entity] = Field(description="Entidades extraídas") relationships: List[str] = Field(description="Relaciones encontradas") metadata: dict = Field(default={}, description="Metadatos de extracción") extractor = LlmAgent( model="gemini-2.5-flash", name="data_extractor", instruction="Extrae datos estructurados del texto", output_schema=ExtractionOutput, generate_content_config=types.GenerateContentConfig( temperature=0.2 # Baja para mantener la coherencia ) ) 

## **Patrón 3: Sistema de toma de decisiones** 

from google.genai import types 

decision_agent = LlmAgent( model="gemini-2.5-pro", name="decision_maker", instruction=\"\"\" Evalúa solicitudes en relación con la política. Considera todos los factores y las dependencias. \"\"\", planner=BuiltInPlanner( thinking_config=types.ThinkingConfig(include_thoughts=False, thinking_budget=2048) ), output_key="approved", # Resultado booleano simple generate_content_config=types.GenerateContentConfig( temperature=0.1 # Muy baja para mantener la coherencia ) ) 

# **Errores frecuentes que debes evitar** 

## ❌ **Errores relacionados con la instrucción** 

- Crear personalidades indefinidas sin experiencia específica ni conocimiento del dominio 

- - No incluir límites, lo que provoca respuestas inapropiadas o irrelevantes para la marca - No incluir demostraciones con varios ejemplos, lo que genera patrones de comportamiento incoherentes 

- Redactar instrucciones demasiado complejas, que confunden al modelo 

- Crear patrones específicos para cada dominio en lugar de usar plantillas reutilizables 

## ❌ **Errores relacionados con la configuración** 

- Comenzar con Flash en lugar de Pro para crear prototipos (modelo de referencia incorrecto) 

- Utilizar Pro para tareas simples de gran volumen después de la optimización (genera gastos innecesarios) 

- Establecer una configuración de seguridad incorrecta para el público (demasiado permisiva o demasiado estricta) 

- Definir una temperatura demasiado alta para tareas fácticas (provoca alucinaciones) 

- No realizar un análisis de brechas al cambiar de Pro a Flash 

## ❌ **Errores relacionados con la planificación** 

- No utilizar el parámetro planner para tareas complejas de varios pasos 

- Utilizar un tipo de planificador incorrecto (BuiltInPlanner para modelos que no son de Gemini) 

- No incluir restricciones realistas, lo que hace que los planes sean poco prácticos 

- Aplicar planificación excesiva para tareas sencillas de un solo paso 

- No configurar thinking_budget de forma adecuada 

- Establecer una temperatura alta junto con la planificación (reduce el pensamiento sistemático) 

## ❌ **Errores relacionados con el resultado** 

- Utilizar diccionarios en lugar de Pydantic BaseModel para los esquemas 

- No definir todos los campos necesarios (solo los campos definidos aparecen en el resultado) 

- No incluir Field(description=…) para guiar al LLM 

- No manejar datos opcionales o faltantes 

- Utilizar convenciones de nomenclatura incongruentes para los campos 

- No validar el resultado antes de pasar a la etapa de producción 

# **Comunidad y asistencia** 

## **Referencias principales** 

- 📚 **<u>Documentación del ADK sobre agentes de LLM</u>** : Configuración avanzada y parámetros 

- 🤖 **<u>Documentación del modelo de Gemini</u>** : Capacidades y funciones del modelo 

- - 🔧 **<u>Precios de Vertex AI</u>** : Optimización de costos y selección de modelos - 📖 **<u>Configuración de seguridad de Gemini</u>** <u>: Guía de configuración de seguridad</u> 

- 🧠 **<u>Pensamiento de Gemini</u>** : Capacidades de planificación 

# **Recursos** 

### **De la comunidad** 

- **<u>Implementing Anthropic's Agent Design Patterns with Google ADK</u>** (Implementa los patrones de diseño de agentes de Anthropic con el ADK de Google): Aprende cómo aplicar patrones de diseño de agentes profesionales y técnicas de instrucción con el ADK. Esto abarca la creación de personalidades y el diseño de comportamientos. 

- **<u>Building Agentic Applications with Google's ADK: A Hands-On SQL Agent Example</u>** (Crea aplicaciones de agentes con el ADK de Google: Ejemplo práctico de un agente de SQL): Consulta una explicación práctica sobre la creación de agentes listos para producción con integración en el mundo real y resultados estructurados. 

- **<u>Fun with agentic workflows in ADK</u>** (Diviértete con los flujos de trabajo de agentes en el ADK): Explora las capacidades de planificación y el razonamiento de varios pasos con patrones de organización de flujos de trabajo. 

- **<u>Practical AI Agent Development Using ADK</u>** (Desarrollo práctico de agentes de IA con el ADK): Consulta las prácticas recomendadas para el desarrollo de agentes, desde la configuración y las instrucciones hasta las estrategias de implementación. 

- **<u>Fast-Track Your Agentic AI Journey with Google's ADK: Hands-On from Code to Cloud</u>** (Agiliza tu recorrido en IA de agentes con el ADK de Google: Práctica desde el código hasta la nube): Consulta una guía práctica y completa con todo lo que necesitas saber, desde la creación de un agente básico hasta la configuración de Gemini y la implementación en la nube. 

# **¿Tienes alguna pregunta? Publícala en el foro de la** **<u>comunidad</u>** 

# **Tarjeta de referencia rápida** 

## **Estrategia de selección de modelos** 

1. Comienza con Gemini 2.5 Pro: Creación de prototipos, modelos de referencia de calidad, razonamiento complejo 

2. Realiza optimizaciones con Gemini 2.5 Flash: Producción, gran volumen, optimización de costos 

3. Siempre realiza un análisis de brechas cuando cambies de Pro `a` Flash 

## **Guía de temperatura** 

- 0.0-0.3: Hechos, extracción de datos, análisis, coherencia 0.4-0.7: Equilibrado, asistencia general, asistencia al cliente 

- 0.8-1.0: Escritura creativa, generación de ideas, marketing 

## **Umbrales de seguridad** 

BLOCK_LOW_AND_ABOVE: El más estricto; para menores o aplicaciones de cara al público BLOCK_MEDIUM_AND_ABOVE: Estándar; para empresas y uso general BLOCK_ONLY_HIGH: Flexible; para investigación y herramientas internas 

## **Cuándo usar cada uno** 

BuiltInPlanner: Modelos de Gemini, tareas de varios pasos, dependencias PlanReActPlanner: Modelos que no son de Gemini con planificación estructurada output_schema: Pydantic BaseModel para resultados JSON estructurados output_key: Transferencia de datos entre agentes, extracción de valores simple 

## **Patrones de instrucción** 

Identidad: [Nombre], [rol], [experiencia] Misión: Qué hace el agente Metodología: Cómo funciona el agente Límites: Listas de lo que nunca o siempre se debe hacer Demostraciones con varios ejemplos: `Ejemplos con el formato de entrada → salida` 

# **Reflexiones finales** 

Pasaste de crear agentes simples a diseñar sistemas de IA sofisticados. Tus agentes ahora pueden hacer lo siguiente: 

- Pensar con personalidad y límites 

- Planificar soluciones complejas de varios pasos 

- Producir datos estructurados listos para su uso en el sistema 

- Operar de forma segura y eficiente 

Con esto, ya sentaste las bases. 

