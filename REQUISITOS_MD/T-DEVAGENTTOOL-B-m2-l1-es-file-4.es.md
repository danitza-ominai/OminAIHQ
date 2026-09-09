# **La solución: Herramientas integradas** 

## **Capacidades listas para producción** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre herramientas integradas</u>_ 

#### **De la documentación del ADK:** 

“Estas herramientas integradas proporcionan funcionalidades listas para usar, como la Búsqueda de Google o los ejecutores de código que brindan a los agentes capacidades comunes”. 

#### **Herramientas integradas disponibles:** 

- **Búsqueda de Google** : búsqueda web con fundamentación (esta parte) 

- **Ejecución de código** : ejecuta código de Python de forma segura (esta parte) 

- **Vertex AI Search** : búsqueda de documentos empresariales 

- **Motor de RAG de Vertex AI** : Generación mejorada por recuperación 

- **BigQuery** : realización de consultas en los almacenes de datos 

- **Spanner** : realización de consultas en las bases de datos de Spanner 

- **Bigtable** : realización de consultas en las bases de datos de Bigtable 

#### **En esta lección introductoria, nos enfocaremos en lo siguiente:** 

1. **Búsqueda de Google** : la más útil a nivel universal para obtener información actualizada 

2. **Ejecución de código:** permite realizar tareas matemáticas y de procesamiento 

#### **Descripción general de las herramientas integradas:** 

graph LR 

A[Herramientas integradas] --> B[Búsqueda de Google] A --> C[Ejecución de código] A --> D[Vertex AI Search] A --> E[RAG de Vertex AI] A --> F[BigQuery] A --> G[Spanner] A --> H[Bigtable] 

B --> I[Información web en tiempo real] C --> J[Ejecución de Python] D --> K[Documentos empresariales] E --> L[Recuperación de documentos] F --> M[Almacenes de datos] G --> N[Bases de datos de Spanner] H --> O[Datos de Bigtable] 

style B fill:#4285f4,color:#fff style C fill:#4285f4,color:#fff style D fill:#f0f0f0 style E fill:#f0f0f0 

style F fill:#f0f0f0 style G fill:#f0f0f0 style H fill:#f0f0f0 

_Herramientas integradas disponibles en ADK (azul = se abarca en esta parte)_ 

# **Conceptos básicos** 

## **1. Herramienta Búsqueda de Google** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre la Búsqueda de Google</u>_ 

#### **De la documentación del ADK:** 

“La herramienta google_search permite al agente realizar búsquedas web con la Búsqueda de Google. La herramienta google_search solo es compatible con los modelos Gemini 2”. 

#### **Qué permite:** 

- Resultados de la búsqueda web en tiempo real 

- Información confiable y actualizada 

- Fundamentación automática de respuestas basadas en fuentes 

- Sugerencias de búsqueda (deben mostrarse según la política) 

#### **Cómo usarla:** 

from google.adk.agents import LlmAgent 

from google.adk.tools import google_search  # Importa la herramienta integrada 

search_agent = LlmAgent( 

model='gemini-2.5-flash',  # Debe usar Gemini 2.0 o una versión posterior name='search_agent', 

instruction="Ayuda a los usuarios a encontrar información con la búsqueda web.", tools=[google_search]  # Agrega la herramienta Búsqueda de Google ) 

#### **Diferencias clave con respecto a la parte 1:** 

- **Uso de importaciones en lugar de definiciones:** from google.adk.tools import google_search 

- **Sin escritura de funciones:** ADK proporciona la implementación completa 

- **Listo para producción:** Google se encarga de la optimización y el mantenimiento 

- - **Requisito del modelo:** solo funciona con modelos Gemini 2.0+ 

#### **¿Qué sucede cuando el agente utiliza esta herramienta?** 

1. El agente determina que es necesaria la búsqueda según la consulta del usuario. 

2. El agente genera una búsqueda de forma automática. 

3. La Búsqueda de Google devuelve resultados relevantes. 

4. El agente sintetiza los resultados en una respuesta. 

5. La respuesta incluye citas de fuentes. 

### **Fundamentación con la Búsqueda de Google** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre la fundamentación de la Búsqueda de Google</u>_ 

#### **¿Qué es la fundamentación?** 

La fundamentación conecta las respuestas del agente con fuentes confiables, lo que reduce las alucinaciones y mejora la exactitud. En lugar de confiar únicamente en los datos de entrenamiento del LLM, el agente basa sus respuestas en información actual y verificable. 

#### **Beneficios de la fundamentación de la Búsqueda de Google:** 

- ✅ Respuestas basadas en datos web en tiempo real 

   - ✅ Fuentes citadas para verificación 

- 

   - ✅ Alucinaciones reducidas 

- 

   - ✅ Información actualizada más allá de la fecha límite de entrenamiento 

- 

#### **Requisito de la política IMPORTANTE:** 

Cuando utilizas la fundamentación de la Búsqueda de Google, **DEBES** mostrar sugerencias de búsqueda ( renderedContent ) en la IU de tu aplicación. Esto es obligatorio según la política de uso de la Búsqueda de Google. 

# En el código de tu aplicación (no en agent.py) response = runner.run(...) 

if hasattr(response, 'rendered_content') and response.rendered_content: display_html(response.rendered_content)  # REQUERIDO por la política 

**¿Por qué es importante?:** Las respuestas de la fundamentación incluyen sugerencias de búsqueda HTML que deben mostrarse a los usuarios para cumplir con las políticas. La falta de visualización infringe las condiciones de uso. 

## **2. Herramienta de ejecución de código** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre la ejecución de código</u>_ 

#### **De la documentación del ADK:** 

“La herramienta built_in_code_execution permite al agente ejecutar código, específicamente cuando se utilizan modelos Gemini 2. Esto permite que el modelo realice tareas como cálculos, manipulación de datos o ejecución de secuencias de comandos 

#### pequeñas”. 

#### **Qué permite:** 

- Ejecutar código de Python de forma segura 

- Realizar cálculos precisos 

- Procesar y analizar datos 

- Ejecutar algoritmos y transformaciones 

#### **Cómo usarla:** 

from google.adk.agents import LlmAgent 

from google.adk.code_executors import BuiltInCodeExecutor 

code_agent = LlmAgent( 

model='gemini-2.5-flash',  # Debe usar Gemini 2.0 o una versión posterior name='code_agent', 

instruction="Ayuda a los usuarios con los cálculos y el procesamiento de datos.", code_executor=BuiltInCodeExecutor()  # Habilita la ejecución de código ) 

**Ten en cuenta la diferencia:** la ejecución de código utiliza el parámetro code_executor , no la lista tools . 

#### **Qué puede hacer el agente con la ejecución de código:** 

- Realizar cálculos matemáticos complejos 

- Procesar y transformar datos 

- Generar visualizaciones 

- Implementar algoritmos 

- Validar cálculos 

#### **Situación de ejemplo:** 

Usuario: "Calcula el interés compuesto de $10,000 a una tasa anual del 5% durante 10 años" 

Pensamiento del agente: 

1. Reconoce que esto requiere un cálculo preciso. 

2. Genera código de Python: capital = 10000 tasa = 0.05 plazo = 10 importe = capital * (1 + tasa) ** plazo interés = importe - capital 

3. Ejecuta el código. 

4. Devuelve: "El interés compuesto es $6,288.95. El importe total es $16,288.95". 

#### **Ventajas clave:** 

- **Cálculos precisos** : sin errores de redondeo de la estimación del LLM 

- **Operaciones complejas** : puede ejecutar algoritmos de varios pasos 

- **Verificación** : el código se puede inspeccionar y verificar 

- **Reproducible** : el mismo código produce los mismos resultados 

## **3. Herramientas integradas y estado de la sesión (vista previa)** 

_Conexión con la lección 4: Administra el estado y la memoria_ 

Las herramientas integradas pueden trabajar con el estado de la sesión para lograr un comportamiento personalizado y consciente del contexto. Si bien la integración completa se analizará en lecciones futuras, aquí te presentamos lo que puedes hacer: 

#### **Casos de uso:** 

- La Búsqueda de Google puede usar las preferencias del usuario según su estado (p. ej., idioma preferido, ubicación). 

- Los resultados de la ejecución de código se pueden guardar en el estado para usar como referencia en otro momento. 

- Las consultas de búsqueda se pueden personalizar según los datos del espacio de nombres user: . 

#### **Patrón de ejemplo (se aborda en la lección 6):** 

# Preferencia del usuario en el estado state["user:preferred_units"] = "metric" 

# La instrucción del agente puede usar plantillas instruction = """ Cuando realices cálculos, utiliza unidades {user:preferred_units?imperial}. Utiliza la ejecución de código para realizar cálculos precisos. """ 

**Vista previa:** La integración completa del estado con herramientas integradas, incluido el acceso al estado dentro del contexto de ejecución de la herramienta, se analiza en la lección 6. 

## **4. Cuándo utilizar las herramientas integradas** 

#### **Comparación: herramientas integradas frente a herramientas de funciones personalizadas** 

|**Aspecto**|**Herramientas integradas**|**Herramientas de funciones**<br>**personalizadas**|
|---|---|---|
|**Configuración**|Importar y utilizar|Escribir la implementación de la<br>función|
|**Mantenimiento**|El equipo de ADK se encarga del|Tú te encargas del|



|**Aspecto**|**Herramientas integradas**|**Herramientas de funciones**<br>**personalizadas**|
|---|---|---|
||mantenimiento|mantenimiento|
|**Optimización**|Preoptimizadas para los LLM|Tú realizas la optimización|
|**Personalización**|Limitada a las funciones de la<br>herramienta|Control total|
|**Ejemplos**|Búsqueda de Google, ejecución<br>de código|get_capital_city,<br>calculate_shipping|
|**Ideal para**|Capacidades comunes|Lógica específica del negocio|



#### **Utiliza herramientas integradas cuando:** 

- ✅ Necesites capacidades comunes (búsqueda, ejecución de código) 

- - ✅ Quieras soluciones con mantenimiento y listas para producción 

   - ✅ No quieras implementar integraciones complejas 

- 

- ✅ Necesites optimización para las interacciones con LLM 

- ✅ Necesites confiabilidad de nivel empresarial 

#### **Utiliza herramientas de funciones personalizadas cuando:** 

- ✅ Necesites una lógica específica para el negocio 

- ✅ Realices integraciones con sistemas propios 

   - ✅ Implementes algoritmos únicos 

- 

- ✅ Necesites tareas simples, específicas y únicas para tu aplicación 

- ✅ Necesites control total sobre la implementación 

#### **Ejemplo de decisión:** 

Tarea: "Agrega búsqueda web al agente" Decisión: Utiliza google_search (integrada) Por qué: capacidad común, compleja de implementar, ADK se encarga del mantenimiento 

Tarea: "Consulta el inventario en nuestra base de datos" Decisión: Escribe una herramienta de función personalizada Por qué: sistema propio, consulta de base de datos sencilla, específico para tu negocio 

## **5. Limitaciones de las herramientas integradas** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre las limitaciones de las herramientas integradas</u>_ 

#### **De la documentación del ADK:** 

“Actualmente, solo se admite una herramienta integrada para cada agente raíz o agente único. No se podrán utilizar otras herramientas de ningún tipo en el mismo agente”. 

#### **Qué significa esto:** 

#### ❌ **NO COMPATIBLE: herramienta integrada + herramienta personalizada en el mismo agente** 

# Esto NO funcionará root_agent = LlmAgent( model='gemini-2.5-flash', tools=[google_search, my_custom_function]  # ❌ No se pueden mezclar ) 

#### ❌ **NO COMPATIBLE: varias herramientas integradas en el mismo agente** 

# Esto NO funcionará root_agent = LlmAgent( model='gemini-2.5-flash', tools=[google_search],  # ❌ No se pueden tener ambos code_executor=BuiltInCodeExecutor()  # ❌ No se pueden tener ambos ) 

**Limitación actual:** Solo una herramienta integrada por agente. Las soluciones de varios agentes (que utilizan agentes especializados para diferentes herramientas) se analizarán en futuras lecciones sobre la coordinación de varios agentes. 

#### **Solución alternativa de Python (avanzada):** 

ADK Python tiene una solución alternativa incorporada para GoogleSearchTool y VertexAiSearchTool con bypass_multi_tools_limit=True . Esto está fuera del alcance de esta lección introductoria. 

# 🧪 **Ejemplo práctico** 

## **Crea agentes con herramientas integradas** 

Crearemos dos agentes independientes para demostrar ambas herramientas: 

1. **Asistente de investigación** : utiliza la Búsqueda de Google para obtener información actualizada. 

2. **Asistente de matemáticas** : utiliza la ejecución de código para los cálculos. 

## **Ejemplo 1: Asistente de investigación con la Búsqueda de Google** 

**Lo que crearás:** Un asistente de investigación que responde preguntas la fundamentación de 

la Búsqueda de Google. 

### **Paso 1: Crea el proyecto** 

adk create research_assistant cd research_assistant 

### **Paso 2: Escribe el agente** 

Reemplaza el contenido de agent.py por lo siguiente: 

""" 

Agente de asistente de investigación 

Demuestra la herramienta integrada de la Búsqueda de Google del ADK para obtener información en tiempo real. 

Referencia: https://google.github.io/adk-docs/tools/built-in-tools#google-search """ 

from google.adk.agents import LlmAgent 

from google.adk.tools import google_search  # Importa la herramienta Búsqueda de Google 

# Crea un asistente de investigación con la Búsqueda de Google root_agent = LlmAgent( 

model='gemini-2.5-flash',  # Debe usar Gemini 2.0+ para google_search name='research_assistant', 

description='Ayuda a los usuarios a investigar temas con la Búsqueda de Google'., instruction=""" 

Eres un asistente de investigación que ayuda a los usuarios a encontrar información precisa y actualizada. 

Tu enfoque: 

1. Cuando los usuarios hagan preguntas que requieran información actual, utiliza la Búsqueda de Google 

2. Basa tus respuestas en los resultados de la búsqueda 

3. Cita fuentes cuando proporciones información 

4. Si los resultados de la búsqueda son insuficientes, reconoce las limitaciones 

Prioriza siempre la exactitud sobre la especulación. Si no estás seguro, dilo. """, 

tools=[google_search]  # Habilita la fundamentación de la Búsqueda de Google ) 

#### **Explicación del código:** 

#### **Línea 7: Importa la Búsqueda de Google** 

- Importa la herramienta integrada desde google.adk.tools 

- No se necesita implementación: ADK la proporciona 

#### **Líneas 10 a 24: Crea un agente con la Búsqueda de Google** 

- model='gemini-2.5-flash' : se requiere Gemini 2.0+ 

- tools=[google_search] : agrega la herramienta integrada 

- La instrucción guía al agente para utilizar la búsqueda de información actual 

### **Paso 3: Ejecuta y prueba** 

adk web 

Desde tu navegador, ve a http://localhost:8000 . 

### **Paso 4: Situaciones de prueba** 

#### **Prueba 1: Eventos actuales** 

Tú: ¿Cuáles son los avances más recientes en energía renovable? 

#### **Comportamiento esperado:** 

- El agente utiliza la Búsqueda de Google para encontrar información actualizada. 

- La respuesta incluye los desarrollos recientes. 

- Se citan fuentes. 

- La información está actualizada. 

#### **Qué se debe tener en cuenta:** 

- El agente buscó en la Web automáticamente. 

- La respuesta se basa en datos actuales, no en datos de entrenamiento. 

- Las fuentes proporcionan verificabilidad. 

#### **Prueba 2: Búsqueda de información fáctica** 

Tú: ¿Quién es el actual director general de Microsoft? 

#### **Comportamiento esperado:** 

- El agente busca información actual. 

- Devuelve una respuesta exacta y actualizada. 

- Cita la fuente. 

#### **Qué se debe tener en cuenta:** 

- La respuesta refleja la realidad actual, no los datos de entrenamiento. 

- La búsqueda proporciona fuentes confiables. 

#### **Prueba 3: Investigación compleja** 

Tú: Compara vehículos eléctricos y vehículos de pila de combustible de hidrógeno 

#### **Comportamiento esperado:** 

- El agente busca varias perspectivas. 

- Sintetiza información de los resultados de la búsqueda. 

- Proporciona una descripción general equilibrada con fuentes. 

#### **Qué se debe tener en cuenta:** 

- El agente puede manejar consultas complejas y multifacéticas. 

- Los resultados de la búsqueda informan sobre una respuesta integral. 

#### **IMPORTANTE: Política de sugerencias de búsqueda** 

Si tu respuesta incluye sugerencias de búsqueda (en renderedContent ), **DEBES** mostrarlas en la IU de tu aplicación. Este es un requisito de la política obligatorio. 

Para aplicaciones de producción, manéjalo de esta manera: 

# En el código de tu aplicación (no en agent.py) from google.adk.runners import Runner 

runner = Runner(...) response = runner.run(...) 

# Busca y muestra sugerencias de búsqueda 

if hasattr(response, 'rendered_content') and response.rendered_content: 

- # Muestra las sugerencias de búsqueda HTML en tu IU 

- # Esto es OBLIGATORIO según la política de fundamentación de la Búsqueda de Google display_in_ui(response.rendered_content) 

## **Ejemplo 2: Asistente matemático con ejecución de código** 

**Lo que crearás:** un asistente matemático que realiza cálculos precisos con la ejecución de código. 

### **Paso 1: Crea el proyecto** 

adk create math_assistant cd math_assistant 

### **Paso 2: Escribe el agente** 

Reemplaza el contenido de agent.py por lo siguiente: 

""" 

Agente asistente de matemáticas 

Demuestra la herramienta integrada de ejecución de código del ADK para realizar cálculos. 

Referencia: https://google.github.io/adk-docs/tools/built-in-tools#code-execution """ 

from google.adk.agents import LlmAgent 

from google.adk.code_executors import BuiltInCodeExecutor  # Importa el ejecutor de código 

# Crea un asistente matemático con ejecución de código root_agent = LlmAgent( 

model='gemini-2.5-flash',  # Debe usar Gemini 2.0+ para la ejecución de código name='math_assistant', 

description='Ayuda a los usuarios con cálculos y análisis matemáticos.', instruction=""" 

Eres un asistente de matemáticas que ayuda a los usuarios con cálculos y análisis matemáticos. 

Tus capacidades: 

1. Cuando los usuarios pidan cálculos, utiliza la ejecución de código para mayor precisión. 

2. Muestra tu trabajo explicando los pasos del cálculo. 

3. Verifica los resultados ejecutando el código. 

4. Realiza operaciones matemáticas complejas (estadísticas, álgebra, etc.). 

Utiliza siempre la ejecución de código para cálculos numéricos para garantizar la exactitud. """, 

code_executor=BuiltInCodeExecutor()  # Habilita la ejecución de código ) 

#### **Explicación del código:** 

#### **Línea 8: Importa el ejecutor de código** 

- Importa desde google.adk.code_executors . 

- Proporciona ejecución segura de código de Python. 

#### **Líneas 11 a 25: Crea un agente con ejecución de código** 

- code_executor=BuiltInCodeExecutor() : habilita la ejecución de código (Nota: No está en la lista tools ). 

- Las instrucciones guían al agente para utilizar el código para los cálculos. 

### **Paso 3: Ejecuta y prueba** 

adk web 

Desde tu navegador, ve a http://localhost:8000 . 

### **Paso 4: Situaciones de prueba** 

#### **Prueba 1: Cálculo simple** 

Tú: Calcula una propina del 15% en una factura de $87.50 

#### **Comportamiento esperado:** 

- El agente genera el código de Python para realizar el cálculo 

- El código se ejecuta: 87.50 * 0.15 

- Devuelve el resultado preciso: $13.13 

#### **Qué se debe tener en cuenta:** 

- El cálculo es preciso (sin errores de redondeo). 

- El agente muestra o explica el cálculo. 

#### **Prueba 2: Cálculo complejo** 

Tú: ¿Cuál es el interés compuesto de $5,000 invertidos a una tasa anual del 6% durante 8 años, con capitalización mensual? 

#### **Comportamiento esperado:** 

- El agente genera una fórmula de interés compuesto en Python. 

- - El código ejecuta el cálculo. 

- Devuelve un resultado preciso con una explicación. 

#### **Qué se debe tener en cuenta:** 

- Fórmula financiera compleja manejada correctamente. 

- La ejecución de código garantiza la exactitud matemática. 

#### **Prueba 3: Procesamiento de datos** 

Tú: Calcula el promedio, la mediana y la desviación estándar de estos números: 12, 15, 18, 20, 22, 25, 28, 30 

#### **Comportamiento esperado:** 

- El agente genera el código de Python con funciones estadísticas. 

- El código calcula las tres métricas. 

- Devuelve resultados exactos. 

#### **Qué se debe tener en cuenta:** 

- Puede realizar múltiples cálculos en una sola solicitud. 

- Las operaciones estadísticas se manejan con precisión. 

# **Conclusiones principales** 

#### **Herramientas integradas:** 

- **Capacidades listas para usar** importadas desde google.adk.tools o google.adk.code_executors 

- **Listo para producción:** el equipo de ADK se encarga del mantenimiento y la optimización 

- **Dos herramientas en esta parte:** la Búsqueda de Google (para obtener información) y la ejecución de código (para cálculos) 

#### **Herramienta Búsqueda de Google:** 

- **Búsqueda web en tiempo real** con fundamentación automática 

- **Requiere modelos Gemini 2.0+** 

- **Requisito de la política:** se deben mostrar sugerencias de búsqueda cuando se proporcionen 

- **Importaciones:** from google.adk.tools import google_search 

- **Uso:** tools=[google_search] 

#### **Herramienta de ejecución de código:** 

- **Ejecuta código de Python** para cálculos precisos 

- **Requiere modelos Gemini 2.0+** 

- **Ejecución segura** en un entorno controlado 

- **Importaciones:** from google.adk.code_executors import BuiltInCodeExecutor 

- **Uso:** code_executor=BuiltInCodeExecutor() (Nota: No está en la lista tools) 

#### **Diferencias clave:** 

|**Aspecto**|**Herramientas integradas**|**Herramientas personalizadas**<br>**(parte 1)**|
|---|---|---|
|Implementación|Importar y utilizar|Escribir función|
|Mantenimiento|ADK se encarga del<br>mantenimiento|Tú te encargas del<br>mantenimiento|
|Uso|Capacidades comunes|Lógica empresarial|



#### **Limitaciones actuales:** 

- **Una herramienta integrada por agente:** No se pueden mezclar herramientas integradas ni combinarlas con herramientas personalizadas en el mismo agente. 

- **Solución:** Usa agentes secundarios con AgentTool (esto se aborda en lecciones futuras). 

- **Existe una solución alternativa** para algunas herramientas en Python (tema avanzado). 

#### **Cuándo se usa:** 

- **Herramientas integradas:** funciones comunes (búsqueda, ejecución de código, consultas a bases de datos) 

- **Herramientas personalizadas:** lógica específica del negocio, sistemas propios 

