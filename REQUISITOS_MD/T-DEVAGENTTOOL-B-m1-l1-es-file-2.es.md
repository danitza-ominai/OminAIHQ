# **La solución: Herramientas** 

## **Amplía las capacidades del agente** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre qué es GTool</u>_ 

### **De la documentación del ADK:** 

“En el contexto del ADK, una herramienta representa una capacidad específica que se proporciona a un agente de IA, lo que le permite realizar acciones y, además, interactuar con el mundo más allá de sus capacidades básicas de generación de texto y razonamiento”. 

### **Qué permiten las herramientas:** 

- ✅ **Acceder a la información en tiempo real** : búsqueda web, APIs de Weather, precios de acciones 

- ✅ **Realizar cálculos** : ejecuta código, ejecuta modelos financieros y procesa datos 

- ✅ **Consultar bases de datos** : recupera pedidos de clientes, inventario de productos y perfiles de usuario 

- ✅ **Interactuar con sistemas externos** : envía correos electrónicos, programa citas y procesa pagos 

- ✅ **Realizar acciones en el mundo** : actualiza registros, activa flujos de trabajo y controla dispositivos 

### **Este es un ejemplo sencillo:** 

def get_weather(city: str) -> dict: """Recupera el clima actual de una ciudad específica.""" # En una implementación real, esto llamaría a una API de Weather return { 

"status": "success", 

"informe": f"El tiempo en {ciudad} es soleado, 25 °C" } 

# Esta función de Python se convierte en una herramienta cuando se agrega a un agente 

# **Conceptos básicos** 

## **1. ¿Qué es una herramienta?** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre qué es una herramienta</u>_ 

### **De la documentación del ADK:** 

“Técnicamente, una herramienta suele ser un componente de código modular (como una función de Python, un método de clase o incluso otro agente especializado) diseñado para ejecutar una tarea específica y predefinida”. 

### **Características clave:** 

**Orientadas a la acción:** Las herramientas realizan acciones específicas para un agente, como buscar información, llamar a una API o realizar cálculos. 

**Amplían las capacidades de agente:** Permiten a los agentes acceder a información en tiempo real, afectar sistemas externos y superar las limitaciones de conocimiento inherentes a los datos de entrenamiento. 

**Ejecución de lógica predefinida:** Fundamentalmente, las herramientas ejecutan una lógica específica definida por el desarrollador. No poseen capacidades de razonamiento independientes propias, como el LLM central del agente. El LLM razona sobre qué herramienta utilizar, cuándo y con qué datos de entrada, pero la herramienta en sí misma simplemente ejecuta su función designada. 

### **Ejemplo de herramienta sencilla:** 

def get_capital_city(country: str) -> str: """Recupera la capital de un país determinado.""" capitals = { "france": "Paris", "japan": "Tokyo", "canada": "Ottawa" } return capitals.get( country.lower(), f"Lo siento, no sé la capital de {país}." ) 

### **Qué hace que esto sea una herramienta:** 

- Es una **función de Python** (componente de código modular) 

- Realiza una **tarea específica** (busca capitales) 

- Tiene una **lógica predefinida** (el diccionario de capitales) 

- **Amplía las capacidades del agente** (acceso a datos estructurados) 

## **2. Cómo utilizan las herramientas los agentes** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre cómo usan las herramientas los agentes</u>_ 

### **De la documentación del ADK:** 

“Los agentes aprovechan las herramientas de forma dinámica a través de mecanismos que suelen implicar la llamada a función. Por lo general, el proceso sigue estos pasos: 

1. **Razonamiento:** El LLM del agente analiza las instrucciones del sistema, el historial de conversaciones y la solicitud del usuario. 

2. **Selección:** Según el análisis, el LLM decide qué herramienta ejecutar, si corresponde, en función de las herramientas disponibles para el agente y las cadenas de documentación que describen cada herramienta. 

3. **Invocación:** El LLM genera los argumentos necesarios (entradas) para la herramienta seleccionada y activa su ejecución. 

4. **Observación:** El agente recibe la salida (resultado) que devuelve la herramienta. 

5. **Finalización:** El agente incorpora el resultado de la herramienta en su proceso de razonamiento continuo para formular la siguiente respuesta, decidir el paso siguiente o determinar si se ha alcanzado el objetivo”. 

### **Flujo de ejemplo:** 

El usuario pregunta: "¿Cuál es el clima en París?" 

```
    ↓
```

Paso 1: Razonamiento El agente analiza: "El usuario necesita datos meteorológicos actuales de París". `↓` 

Paso 2: Selección El agente decide: "La herramienta get_weather cumple con esta necesidad" `↓` 

Paso 3: Invocación El agente llama a: get_weather(city="Paris") `↓` Paso 4: Observación La herramienta devuelve: {"status": "success", "report": "París está soleado, 20 °C"} `↓` Paso 5: Finalización El agente responde: "El clima actual en París es soleado, con una temperatura de 20 °C". 

**Información clave:** El LLM se encarga del razonamiento y la toma de decisiones, mientras que la herramienta se encarga de la acción y la recuperación de datos. Esta separación es lo que hace que los agentes sean potentes. 

### **Representación visual:** 

graph TD A[Solicitud de usuario] --> B[1. Razonamiento:<br/>El agente analiza la solicitud] B --> C{2. Selección:<br/>¿Qué herramienta?} C -->|Herramienta necesaria| D[3. Invocación:<br/>llama a la herramienta con argumentos] C -->|No se necesita herramienta| E[Genera una respuesta directa] D --> F[4. Observación:<br/>recibe el resultado de la herramienta] F --> G[5. Finalización:<br/>formula la respuesta] G --> H[Respuesta del agente] E --> H 

style B fill:#e1f5ff style D fill:#ffeb99 style F fill:#e1f5ff style G fill:#eeffee 

_El proceso de cinco pasos que utilizan los agentes para aprovechar las herramientas_ 

## **3. Tipos de herramientas en el ADK** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre los tipos de herramientas</u>_ 

### **De la documentación del ADK:** 

“ADK ofrece flexibilidad; para ello, admite varios tipos de herramientas: 

1. **Herramientas de funciones:** herramientas que creas tú y se adaptan a las necesidades específicas de tu aplicación. 

2. **Herramientas integradas:** herramientas listas para usar que proporciona el framework para tareas comunes. Ejemplos: Búsqueda de Google, ejecución de código y Generación mejorada por recuperación (RAG). 

3. **Herramientas de terceros:** integra herramientas de bibliotecas externas populares sin problemas”. 

### **En esta lección introductoria, nos enfocaremos en lo siguiente:** 

### **1. Herramientas de funciones personalizadas** 

- Funciones de Python que escribes 

- Se adapta a tu lógica empresarial específica 

- Ejemplo: calculate_shipping_cost , lookup_order_status 

- **Se aborda en:** Parte 3 

### **2. Herramientas integradas** 

- El framework del ADK las proporciona 

- Listas para producción, Google se encarga de su mantenimiento 

- Ejemplos: Búsqueda de Google, ejecución de código 

- **Se aborda en:** Parte 2 

### **3. Agente como herramienta** 

- Utiliza otro agente especializado como herramienta. 

- Permite la delegación y el razonamiento especializado. 

- Ejemplo: El agente principal llama a un agente especializado de “asistencia técnica”. 

- **Vista previa en** Parte 4; **se aborda de manera completa en** futuras lecciones. 

### **Comparación:** 

|**Tipo**|**Complejidad**|**Configuración**|**Casos en que se debe**<br>**usar**|
|---|---|---|---|
|**Integrada**|Baja|Importar y utilizar|Cuando necesites|



|**Tipo**|**Complejidad**|**Configuración**|**Casos en que se debe**<br>**usar**<br>capacidades comunes<br>(búsqueda, ejecución de<br>código)|
|---|---|---|---|
|**Herramientas de**<br>**funciones**|Media|Escribir una función de<br>Python|Cuando necesites una<br>lógica empresarial<br>personalizada|
|**Agente como**<br>**herramienta**|Media-alta|Crear agente<br>especializado|Cuando necesites<br>razonamiento<br>especializado para<br>subtareas|



## **4. El parámetro tools** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre cómo equipar al agente con herramientas</u>_ 

### **De la documentación del ADK:** 

" tools (opcional): proporciona una lista de herramientas que el agente puede usar. Cada elemento de la lista puede ser: 

- Una función o un método nativos (encapsulados como FunctionTool ) 

- Una instancia de una clase que hereda de BaseTool 

- Una instancia de otro agente ( AgentTool )” 

### **Cómo entiende el LLM las herramientas:** 

“El LLM utiliza los nombres de funciones/herramientas, las descripciones (de cadenas de documentación o del campo de descripción) y los esquemas de parámetros para decidir qué herramienta llamar según la conversación y sus instrucciones”. 

### **Ejemplo de código:** 

from google.adk.agents import LlmAgent 

# Paso 1: Define una función de herramienta def get_capital_city(country: str) -> str: 

"""Recupera la capital de un país determinado.""" capitals = {"france": "Paris", "japan": "Tokyo", "canada": "Ottawa"} return capitals.get(country.lower(), f"Lo siento, no sé la capital de {país}".) 

# Paso 2: Agrega la herramienta al agente capital_agent = LlmAgent( 

model="gemini-2.5-flash", name="capital_agent", description="Responde preguntas sobre capitales.", instrucción="Eres un agente que proporciona la capital de un país.", tools=[get_capital_city]  # ✨ NOVEDAD: parámetro de herramientas ) 

### **Qué se debe tener en cuenta:** 

1. **Tools es una lista:** tools=[...] ; puedes proporcionar varias herramientas 

2. **Función pasada directamente:** el ADK envuelve automáticamente las funciones de Python como FunctionTool 

3. **LLM usa metadatos:** el nombre de la función, la cadena de documentación y los parámetros guían la decisión del LLM 

4. **No se necesita ajuste manual:** el ADK de Python gestiona la creación de FunctionTool automáticamente 

### **Cómo ve el LLM esta herramienta:** 

Nombre de la herramienta: get_capital_city Descripción: "Recupera la capital de un país determinado". Parámetros: - country (str): Un nombre de país Devuelve: str 

El LLM utiliza este esquema para decidir cuándo y cómo llamar a la herramienta. 

## **5. Herramientas y estado de la sesión (vista previa)** 

_Conexión con la lección 4: Administra el estado y la memoria_ 

Las herramientas pueden trabajar junto con el estado de la sesión para proporcionar un comportamiento personalizado y adaptado al contexto. Si bien la mecánica de acceso al estado en las herramientas ( tool_context ) se abarca en futuras lecciones sobre devoluciones de llamadas y control, aquí hay una vista previa de lo que es posible: 

### **Ejemplo: Herramienta que guarda la preferencia del usuario en el estado** 

def save_user_preference(preference_key: str, preference_value: str, ctx) -> dict: """Guarda una preferencia del usuario en el estado de la sesión. 

Argumentos: preference_key: el nombre de la preferencia (p. ej., "language", "theme") preference_value: el valor de preferencia (p. ej., "Spanish", "dark") ctx: contexto de la herramienta (proporciona acceso al estado de la sesión) 

Devuelve lo siguiente: dict: Mensaje de estado Nota: El parámetro ctx (tool_context) se aborda en la lección 6. 

""" 

# Guarda en el espacio de nombres user: para la persistencia entre sesiones ctx.session.state[f"user:{preference_key}"] = preference_value 

return { "status": "success", "message": f"Saved {preference_key} = {preference_value}" } 

### **Esto permite lo siguiente:** 

- ✅ **Personalización** : Las herramientas pueden leer las preferencias del usuario desde el estado. 

- ✅ **Reconocimiento del contexto** : Las herramientas pueden verificar el estado de una conversación anterior. 

- ✅ **Flujos de trabajo de varios pasos** : Las herramientas pueden guardar resultados intermedios en el estado. 

- ✅ **Memoria entre sesiones** : Las herramientas pueden usar el espacio de nombres user: para la persistencia. 

### **Ejemplo de caso de uso:** 

# Turno 1: El usuario establece sus preferencias Usuario: "Guarda mi preferencia de idioma como español" El agente llama a: save_user_preference("language", "Spanish", ctx) # Ahora state["user:language"] = "Spanish" 

# Turno 2: El agente usa la preferencia (a través de la plantilla de estado de la lección 4) Instrucción del agente: "Responde en {user:language?English}" # Se resuelve como: "Responder en español" 

**Vista previa:** la integración completa de herramientas con la administración de estados se aborda en la lección 6, en la que aprenderás sobre tool_context , el parámetro ctx y patrones avanzados de coordinación de estados. 

# 🧪 **Ejemplo práctico** 

## **Crearás tu primer agente habilitado para herramientas** 

**Lo que crearás:** un asistente de geografía que ayuda a los usuarios a aprender sobre las capitales del mundo con una herramienta personalizada. 

## **Paso 1: Crea el proyecto** 

adk create geography_assistant cd geography_assistant 

### **Qué hace:** 

- Crea un nuevo directorio de proyecto del ADK. 

- Configura la estructura básica del agente. 

- Crea agent.py con el código de agente predeterminado. 

## **Paso 2: Escribe el agente** 

Reemplaza el contenido de agent.py por lo siguiente: 

""" Agente asistente de geografía Demuestra el parámetro tools del ADK con una herramienta de función personalizada simple. Referencia: https://google.github.io/adk-docs/agents/llm-agents#tools """ from google.adk.agents import LlmAgent # Paso 1: Define una función de herramienta def get_capital_city(country: str) -> str: """Recupera la ciudad capital de un país específico. Argumentos: country (str): el nombre del país. Devuelve lo siguiente: str: el nombre de la capital o el mensaje de error. """ # Base de datos de capitales simulada capitals = { "france": "Paris", "japan": "Tokyo", "canada": "Ottawa", "germany": "Berlin", "brazil": "Brasília", "australia": "Canberra", "india": "New Delhi", "mexico": "Mexico City" } # Busca la capital return capitals.get( country.lower(), f"Lo siento, no tengo información sobre la capital de {país}." ) 

# Paso 2: Crea un agente con la herramienta root_agent = LlmAgent( 

model='gemini-2.5-flash', name='geography_assistant', description='Ayuda a los usuarios a aprender sobre geografía mundial.', instruction=""" 

Eres un asistente de geografía que ayuda a los usuarios a aprender sobre las capitales del mundo. 

Cuando un usuario pregunta por una capital: 

1. Utiliza la herramienta get_capital_city para encontrar la respuesta. 

2. Proporciona la información de una manera amigable y educativa. 

3. Puedes agregar datos interesantes si los conoces. 

Si la herramienta devuelve un mensaje de error, dile de manera amable al usuario que no tienes esa información. 

""", 

tools=[get_capital_city]  # Proporciona la función como una herramienta ) 

### **Explicación del código:** 

### **Líneas 10 a 28: Define la función de herramienta** 

- El nombre de la función es descriptivo: get_capital_city . 

- Tiene sugerencias de tipo: country: str -> str . 

- Incluye una cadena de documentación que explica el propósito y los parámetros. 

- Devuelve una cadena simple (nombre de la capital o mensaje de error). 

### **Líneas 30 a 44: Crea el agente** 

- Usa LlmAgent (de la lección 2 **–** 3). 

- Agrega el nuevo parámetro tools con nuestra función. 

- Las instrucciones guían al agente sobre cuándo y cómo utilizar la herramienta. 

- Explica cómo manejar los casos de éxito y de error. 

## **Paso 3: Ejecuta y prueba** 

adk web 

Desde tu navegador, ve a http://localhost:8000 . 

## **Paso 4: Situaciones de prueba** 

### **Prueba 1: Consulta básica de capital** 

Tú: ¿Cuál es la capital de Japón? 

### **Comportamiento esperado:** 

- El agente llama a get_capital_city(country="Japan") . 

- La herramienta devuelve "Tokyo" . 

- El agente responde: “La capital de Japón es Tokio”. 

### **Qué se debe tener en cuenta:** 

- El agente seleccionó automáticamente la herramienta correcta. 

- El agente extrajo correctamente “Japón” como parámetro de país. 

- El agente mostró el resultado de la herramienta con formato en lenguaje natural. 

### **Prueba 2: Varias capitales** 

Tú: Dime las capitales de Francia, Alemania y Brasil 

### **Comportamiento esperado:** 

- El agente llama a get_capital_city tres veces (una por cada país). 

- La herramienta devuelve: “París”, “Berlín”, “Brasilia”. 

- El agente proporciona una lista con formato. 

### **Qué se debe tener en cuenta:** 

- El agente organiza varias llamadas a herramientas. 

- El agente entiende que necesita llamar a la herramienta para cada país. 

- El agente sintetiza los resultados en una respuesta cohesiva. 

### **Prueba 3: Capital desconocida** 

Tú: ¿Cuál es la capital de Islandia? 

### **Comportamiento esperado:** 

- El agente llama a get_capital_city(country="Iceland") . 

- La herramienta devuelve: “Lo siento, no tengo información sobre la capital de Islandia”. 

- El agente le informa esto al usuario de manera educada. 

### **Qué se debe tener en cuenta:** 

- El agente maneja los mensajes de error de forma ordenada. 

- El mensaje de error de la herramienta es fácil de usar. 

- El agente no alucina una respuesta cuando los datos no están disponibles. 

### **Prueba 4: No se necesitan herramientas** 

Tú: Cuéntame sobre geografía 

### **Comportamiento esperado:** 

- El agente responde sin llamar a ninguna herramienta. 

- - Utiliza conocimientos generales sobre geografía. 

- No se produce ninguna invocación de herramienta. 

### **Qué se debe tener en cuenta:** 

- Las herramientas se llaman solo cuando son necesarias. 

- El agente utiliza su razonamiento para determinar la necesidad de la herramienta. 

- No todas las consultas requieren una herramienta. 

# **Conclusiones principales** 

### **Conceptos básicos:** 

- **Las herramientas amplían las capacidades del agente** más allá del conocimiento del LLM, lo que permite acciones reales y acceso a los datos. 

- **Los agentes utilizan herramientas a través de cinco pasos:** Razonamiento → Selección → Invocación → Observación → Finalización **.** 

- **Tres tipos principales de herramientas:** herramientas integradas (listas para usar), herramientas de funciones (personalizadas) y agente como herramienta (delegación). 

### **Cómo funcionan las herramientas:** 

- **El LLM selecciona las herramientas según** el nombre de la función, la cadena de documentación y el esquema de parámetros. 

- **Las herramientas son simplemente funciones de Python** que el ADK encapsula automáticamente. 

- **Las herramientas devuelven resultados** que los agentes incorporan en sus respuestas. 

- La **organización se realiza automáticamente** a través del bucle del agente del ADK. 

### **El parámetro tools :** 

- **Se agrega a LlmAgent -** tools=[function1, function2, ...] . 

- **Las funciones se convierten en herramientas automáticamente:** no es necesario ajustarlas manualmente en Python. 

- **LLM decide cuándo usar cada herramienta:** según el contexto de la conversación y las instrucciones. 

### **Prácticas recomendadas:** 

- **Nombres de funciones descriptivas:** Utiliza get_capital_city , no lookup ni get_data . 

- **Borra las cadenas de documentación:** Explica qué hace la herramienta y cuándo usarla. 

- **Sugerencias de tipo:** Ayuda a ADK a generar un esquema adecuado para el LLM. 

- - **Valores de retorno simples:** Comienza con tipos básicos antes de estructuras complejas. 

### **Comportamiento del agente:** 

- **Las herramientas son opcionales:** Los agentes llaman a las herramientas solo cuando el razonamiento determina que son necesarias. 

- **Posibilidad de múltiples llamadas:** Los agentes pueden llamar a la misma herramienta varias veces o a diferentes herramientas. 

- **Integración natural:** Los resultados de la herramienta se incorporan a las respuestas sin dificultad. 

- **Manejo de errores:** Las herramientas deben devolver mensajes de error claros para los casos de falla. 

