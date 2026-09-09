# **¡Felicitaciones!** 

Completaste el curso 5: Agrega capacidades con herramientas. 

Con este curso, transformaste a tus agentes de respondedores inteligentes en asistentes capaces de tomar medidas. Implementaste el componente **tools** de la ecuación del agente, lo que les brinda a tus agentes el poder de buscar en la Web, ejecutar código, acceder a bases de datos y realizar acciones personalizadas en el mundo real. 

### **Tu transformación:** 

- **Antes del curso 5:** los agentes estaban limitados a los datos de entrenamiento del LLM; solo podían responder con el conocimiento existente. 

- **Después del curso 5:** los agentes pueden realizar acciones como buscar en la Web en tiempo real, ejecutar código, consultar sistemas y, además, integrar tu lógica empresarial. 

Completaste la ecuación principal del agente: **agente = modelo + herramientas + organización** . 

# **Objetivos logrados** 

Comenzaste este curso con agentes sofisticados que tenían una configuración avanzada. Lo estás terminando con agentes que pueden hacer lo siguiente: 

- **Acceder a información en tiempo real** a través de la fundamentación de la Búsqueda de Google 

- **Realizar cálculos precisos** con la ejecución de código 

- **Conectarse a herramientas externas** a través de servidores MCP (sistema de archivos, bases de datos, APIs) 

- **Ejecutar tu lógica empresarial** mediante herramientas de funciones personalizadas 

- **Solucionar los errores con elegancia** con un manejo de errores estratégico 

- **Coordinar múltiples herramientas** en flujos de trabajo complejos 

- **Delegar a especialistas** con patrones de agente como herramienta 

### **Habilidades adquiridas:** 

- Compresión de las herramientas a nivel fundamental (qué son, cómo las utilizan los agentes) 

- Uso de herramientas integradas listas para producción (Búsqueda de Google, ejecución de código) 

- Conexión a servidores MCP preexistentes para las herramientas del ecosistema 

- Creación de herramientas de funciones personalizadas adaptadas a tus necesidades 

- Diseño de instrucciones estratégicas que guíen el uso eficaz de las herramientas 

- - Manejo de errores de herramientas y coordinación de flujos de trabajo con múltiples herramientas 

- Uso de agentes especializados como herramientas para el razonamiento complejo 

### **El recorrido:** 

- Módulo 1: Creaste tu primer agente habilitado para herramientas y aprendiste sobre la vista previa de integración de estados. 

- Módulo 2: Utilizaste herramientas integradas para la búsqueda web y ejecución de código, además de obtener una vista previa del estado. 

- Módulo 3: Te conectaste a servidores MCP externos para herramientas preexistentes. 

- Módulo 4: Creaste herramientas personalizadas con integración de estados completa. 

- Módulo 5: Combinaste herramientas con instrucciones estratégicas, manejo de errores y coordinación de estados. 

### **Mejorado con:** 

- Ayudas visuales de aprendizaje (diagramas de Mermaid en módulos que muestran procesos de herramientas, flujos de trabajo y manejo de errores) 

- Integración de estados en todos los módulos que conectan el curso 4 (Estado) con el curso 5 (Herramientas) 

- Alcance optimizado: se eliminaron las referencias futuras y se simplificaron las secciones detalladas 

- Ejemplos prácticos: Flujos de trabajo de varios pasos, seguimiento de uso y personalización con estado 

# **Tú recorrido** 

## **Módulo 1: Comprende las herramientas (~30 minutos)** 

Aprendiste qué son las herramientas y cómo amplían las capacidades de agente más allá del conocimiento del LLM. 

### **Conceptos clave dominados:** 

- ✅ Las herramientas amplían los agentes para realizar acciones más allá de la generación de texto 

- ✅ El proceso de cinco pasos de las herramientas: Razonamiento → Selección → Invocación → Observación → Finalización 

- ✅ Tres tipos de herramientas: integrada, función personalizada, agente como herramienta 

- ✅ El parámetro tools y cómo los LLM utilizan los metadatos de las funciones 

- ✅ Vista previa: cómo las herramientas pueden leer y escribir el estado de la sesión para la personalización 

**Información clave:** "Las herramientas son componentes de código modulares que ejecutan tareas predefinidas, lo que permite a los agentes acceder a información en tiempo real, afectar sistemas externos y superar las limitaciones de los datos de entrenamiento". 

## **Módulo 2: Herramientas integradas (~25 minutos)** 

Aprendiste a utilizar las herramientas integradas listas para producción del ADK sin escribir código de integración complejo. 

### **Conceptos clave dominados:** 

- ✅ La herramienta Búsqueda de Google proporciona información web en tiempo real con fundamentación 

- ✅ La herramienta de ejecución de código permite realizar cálculos precisos y procesar datos 

- ✅ La fundamentación conecta las respuestas con fuentes confiables 

   - ✅ Requisito de la política: se deben mostrar sugerencias de búsqueda 

- 

   - ✅ Limitación actual: una herramienta integrada por agente raíz 

- 

   - ✅ Vista previa: integración de estados con herramientas integradas 

- 

**Información clave:** "Utiliza herramientas integradas para capacidades comunes (búsqueda, ejecución de código). Utiliza herramientas personalizadas para la lógica específica del negocio. El equipo de ADK se encarga de mantener y optimizar las herramientas integradas". 

## **Módulo 3: Herramientas del MCP (~25 minutos)** 

Aprendiste a conectar agentes del ADK a servidores MCP externos para aprovechar las capacidades de herramientas preexistentes. 

### **Conceptos clave dominados:** 

- ✅ MCP (Protocolo de contexto del modelo) proporciona conectividad de servidor de herramientas estandarizada 

- 

   - ✅ McpToolset conecta agentes del ADK a servidores MCP 

- ✅ Dos tipos de conexión: StdioConnectionParams (local) y SseConnectionParams (remota) 

- ✅ tool_filter controla qué herramientas están expuestas al agente 

- ✅ El ecosistema del MCP proporciona muchas herramientas prediseñadas (sistema de archivos, bases de datos, APIs) 

- ✅ Adopción en la industria: Anthropic, OpenAI, Google y The Linux Foundation 

**Información clave:** "Las herramientas del MCP te permiten aprovechar el ecosistema: utiliza los servidores de herramientas preexistentes y con mantenimiento, en lugar de crear todo por tu cuenta". 

## **Módulo 4: Herramientas de funciones personalizadas (~35 minutos)** 

Aprendiste a escribir herramientas de funciones personalizadas eficaces con firmas adecuadas, sugerencias de tipo y cadenas de documentación. 

### **Conceptos clave dominados:** 

- ✅ Firmas de funciones: nombres descriptivos, sugerencias de tipo, parámetros simples 

- - ✅ Las cadenas de documentación guían la selección de herramientas del LLM (qué, cuándo, argumentos y devoluciones) 

   - ✅ Devuelve diccionarios con claves de estado para la comprensión del LLM 

- 

   - ✅ Varias herramientas cooperan a través de la organización de agentes 

- 

- ✅ ADK genera automáticamente un esquema de herramientas a partir de los metadatos de la función 

- ✅ Integración de estados completa: flujos de trabajo de varios pasos, seguimiento de uso y personalización 

**Información clave:** "La cadena de documentación de la función sirve como descripción de la herramienta y se envía al LLM. Una cadena de documentación completa es fundamental para que el LLM comprenda cómo usar la herramienta de manera eficaz". 

## **Módulo 5: Combina herramientas de manera eficaz (~30 minutos)** 

Aprendiste a diseñar instrucciones estratégicas que guíen a los agentes a utilizar múltiples herramientas de manera eficaz. 

### **Conceptos clave dominados:** 

- ✅ Patrones de instrucciones: selección de herramientas, manejo de resultados, flujos de trabajo secuenciales 

   - ✅ Manejo de errores: diferentes acciones para distintos tipos de errores 

- 

- ✅ Vista previa del patrón de agente como herramienta (se aborda de manera completa en futuros cursos) 

   - ✅ Prácticas recomendadas para la coordinación y el diseño de herramientas 

- 

- ✅ Las instrucciones estratégicas guían cuándo, cómo y en qué orden utilizar las herramientas 

- ✅ Coordinación de estados con herramientas: flujos de trabajo de varios pasos, seguimiento de uso y lógica condicional 

**Información clave:** "Es fundamental instruir claramente al agente sobre cómo gestionar los diferentes valores de devolución que una herramienta podría generar; especifica si el agente debe reintentar, abandonar o solicitar información adicional". 

# **Aplicaciones reales** 

## **Aplicación 1: Atención al cliente de comercio electrónico** 

Gestiona consultas de pedidos, procesa reembolsos y deriva problemas complejos utilizando herramientas personalizadas con instrucciones estratégicas y manejo de errores integral. 

## **Aplicación 2: Investigación y análisis** 

Encuentra información actualizada con la Búsqueda de Google y realiza análisis de datos con ejecución de código (agentes independientes debido a la limitación de una herramienta integrada). 

## **Aplicación 3: Asistencia multiespecialista** 

Dirige los problemas de los clientes a agentes especializados utilizando el patrón de agente como herramienta con experiencia específica en el dominio. 

## **Aplicación 4: Planificación de viajes** 

Busca vuelos y hoteles, calcula presupuestos utilizando varias herramientas personalizadas con coordinación secuencial. 

# **Conclusiones principales para recordar** 

1. **La ecuación del agente completada** : agente = modelo + herramientas + organización. Las herramientas permiten a los agentes realizar acciones más allá de la generación de texto. 

2. **Las herramientas amplían las capacidades del LLM** : los LLM están limitados a los datos de entrenamiento. Las herramientas proporcionan información en tiempo real, cálculos precisos, acceso a datos propios y acciones externas. 

3. **El LLM usa metadatos para la selección de herramientas** : el LLM usa el nombre de la función, la descripción de la cadena de documentación y el esquema de parámetros para decidir qué herramienta llamar. 

4. **Decisión entre herramientas integradas, MCP o personalizadas** : utiliza las herramientas integradas para las capacidades de Google. Utiliza las herramientas del MCP para integraciones de ecosistemas. Utiliza las herramientas de funciones personalizadas para la lógica específica del negocio. 

5. **Patrón de devolución basado en estado** : devuelve siempre diccionarios con la clave de status ('success'/'error'). Incluye tipos de errores específicos para un manejo diferente. 

6. **Las instrucciones estratégicas guían a las herramientas** : especifica cuándo usar cada herramienta, cómo manejar los resultados, en qué orden llamar a las herramientas y cuándo derivar un asunto. 

7. **Los tipos de error necesitan un manejo diferente** : “not_found” necesita una aclaración, “invalid_format” necesita una explicación y “permission_denied” necesita una derivación. 

8. **Agente como herramienta para razonamiento especializado** : cuando las subtareas requieren instrucciones o experiencia diferentes, utiliza un agente como herramienta en lugar de como función. 

# **Lista de verificación de prácticas recomendadas** 

## ✅ **Diseño de herramientas** 

Nombres de funciones descriptivas (patrón verbo-sustantivo) Sugerencias de tipo para todos los parámetros Cadenas de documentación completas (qué, cuándo, argumentos y devoluciones) Devolución de diccionarios con clave de estado Mensajes de error específicos y fáciles de usar Propósito único y específico por herramienta Tipos de parámetros serializables en JSON 

## ✅ **Herramientas integradas** 

Utiliza la Búsqueda de Google para obtener información en tiempo real. Utiliza la ejecución de código para realizar cálculos precisos. Muestra las sugerencias de búsqueda (requisito de la política). Recuerda la limitación de una herramienta integrada por agente. Utiliza los modelos Gemini 2.0+. 

## ✅ **Herramientas del MCP** 

Verifica el registro de MCP antes de escribir herramientas personalizadas. Utiliza tool_filter para limitar las herramientas expuestas. Utiliza StdioConnectionParams para el desarrollo. Utiliza SseConnectionParams para la producción. Asegúrate de que Node.js esté instalado para servidores basados en npx. 

## ✅ **Diseño de instrucciones** 

Haz referencia a las herramientas por nombre. Especifica cuándo utilizar cada herramienta. Define flujos de trabajo secuenciales paso a paso. Maneja todos los tipos de errores con acciones específicas. Incluye rutas de derivación. Organiza en secciones claras. 

## ✅ **Manejo de errores** 

Devuelve tipos de errores específicos. Proporciona mensajes de error legibles por humanos. Especifica estrategias de reintento en comparación con estrategias de abandono. Define los criterios de derivación. Prueba todas las rutas de error. Documenta los errores esperados en las cadenas de documentación. 

# **Referencia de patrones de código** 

## **Patrón 1: Herramienta personalizada básica** 

def tool_name(param: type) -> dict: """Resumen de una línea. Úsalo cuando [situación]. Argumentos: param (tipo): descripción Devuelve lo siguiente: dict: {'status': 'success'/'error', ...} """ if validation_fails: return {"status": "error", "error_message": "explanation"} return {"status": "success", "data": value} 

## **Patrón 2: Uso de herramientas integradas** 

from google.adk.tools import google_search from google.adk.code_executors import BuiltInCodeExecutor 

# Búsqueda de Google agent = LlmAgent( model='gemini-2.5-flash', tools=[google_search] ) 

# Ejecución de código agent = LlmAgent( model='gemini-2.5-flash', code_executor=BuiltInCodeExecutor() ) 

## **Patrón 3: Uso de la herramienta del MCP** 

from google.adk.agents import LlmAgent from google.adk.tools.mcp_tool import McpToolset from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams from mcp import StdioServerParameters 

agent = LlmAgent( model='gemini-2.5-flash', name='mcp_agent', tools=[ McpToolset( connection_params=StdioConnectionParams( server_params=StdioServerParameters( command='npx', args=['-y', '@modelcontextprotocol/server-filesystem', '/path'], 

), ), tool_filter=['list_directory', 'read_file'],  # Seguridad: limita las herramientas ) ], ) 

## **Patrón 4: Varias herramientas con instrucciones estratégicas** 

agent = LlmAgent( instruction=""" ## Selección de herramientas - Utiliza tool_1 cuando [situación] - Utiliza tool_2 cuando [situación] ## Flujos de trabajo Para [tarea]: 1. Primero usa tool_1 2. Luego, usa tool_2 ## Manejo de errores - 'not_found': pídele al usuario que verifique - 'invalid_format': explica el formato correcto """, tools=[tool_1, tool_2] ) 

## **Patrón 5: Agente como herramienta** 

from google.adk.tools.agent_tool import AgentTool 

specialist = LlmAgent( name='specialist', instruction="Experiencia específica del dominio..." ) 

main_agent = LlmAgent( instruction="Enruta al especialista cuando [situación]", tools=[AgentTool(agent=specialist)] ) 

# **Errores frecuentes que debes evitar** 

## ❌ **Diseño de herramientas** 

- Nombres de funciones poco claros ( process() en lugar de process_refund() ) 

- Sugerencias de tipo faltantes (LLM necesita información de tipo) 

- Cadenas de documentación deficientes (LLM depende de ellas para la selección de herramientas) 

- Devolución de cadenas en lugar de diccionarios (los datos estructurados son más claros) 

- Herramientas multipropósito (enfócate en un solo propósito) 

## ❌ **Instrucciones** 

- Demasiado ambiguas (no guían el uso de la herramienta) 

- No hay orientación sobre errores (LLM no sabe cómo manejar las fallas) 

- Secuencias faltantes (sin orden para flujos de trabajo con múltiples herramientas) 

- No hay ruta de derivación (el agente se queda bloqueado) 

## ❌ **Herramientas integradas** 

- Combinación de funciones integradas con personalizadas en el mismo agente (no compatible) 

- Versión de modelo incorrecta (se necesita Gemini 2.0+) 

- Ignorar la política de sugerencias de búsqueda (requisito obligatorio) 

## ❌ **Herramientas del MCP** 

- No verificar el registro del MCP antes de escribir herramientas personalizadas 

- Exponer todas las herramientas sin tool_filter (riesgo de seguridad) 

- Requisito de Node.js faltante para los servidores npx 

## ❌ **Manejo de errores** 

- Devoluciones de errores genéricos (no se pueden diferenciar las fallas) 

- - No hay orientación para el usuario en caso de errores (ayuda a los usuarios a solucionar problemas) 

- Reintentar los bucles sin cambios (misma entrada = misma falla) 

- No documentar los tipos de errores en las cadenas de documentación 

# **Tarjeta de referencia rápida** 

## **Comparación de tipos de herramientas** 

|**Tipo**|**Configuración**|**Ideal para**|**Mantenimiento**|
|---|---|---|---|
|**Integrada**|Importar desde el ADK|Capacidades comunes|Equipo del ADK|
|**MCP**|Conectarse al servidor<br>MCP|Herramientas del<br>ecosistema preexistentes|Encargados de mantener<br>los servidores|
|**Función personalizada**|Escribir una función de<br>Python|Lógica empresarial|Tú|
|**Agente como**|Crear LlmAgent|Razonamiento complejo|Tú|



|**Tipo**|**Configuración**|**Ideal para**|**Mantenimiento**|
|---|---|---|---|
|**herramienta**||||



## **Cuándo usar cada opción** 

|**Situación**|**Enfoque**|**Por qué**|
|---|---|---|
|Búsqueda web|Integrada:google_search|Lista para producción, con<br>mantenimiento|
|Cálculos|Integrada:<br>BuiltInCodeExecutor|Ejecución de código segura|
|Capacidad preexistente|Herramientas del MCP|La comunidad se encarga de<br>mantenerlas|
|Tu lógica empresarial|Herramienta de función<br>personalizada|Tus necesidades específicas|
|Razonamiento complejo|Agente como herramienta|Requiere adaptación|



## **Guía rápida de manejo de errores** 

|**Tipo de error**|**Acción**|**Ejemplo**|
|---|---|---|
|not_found|Solicitar al usuario que verifique|"¿Podrías verificar el ID de<br>pedido?"|
|invalid_format|Explicar con un ejemplo|"Los IDs de pedido comienzan<br>con 'ORD' (p. ej., ORD123)"|
|permission_denied|Derivar inmediatamente|"Te voy a comunicar con un<br>supervisor"|
|temporary_failure|Volver a intentarlo una vez y<br>luego derivar|"Déjame intentarlo de nuevo...<br>Aún hay problemas"|



## **Importaciones esenciales** 

from google.adk.agents import LlmAgent from google.adk.tools import google_search from google.adk.code_executors import BuiltInCodeExecutor from google.adk.tools.agent_tool import AgentTool from google.adk.tools.mcp_tool import McpToolset 

# **Comunidad y asistencia** 

## **Referencias principales** 

- **<u>Descripción general de herramientas personalizadas</u>** <u>: guía completa para crear</u> herramientas personalizadas en ADK 

- **<u>Herramientas integradas</u>** <u>: Búsqueda de Google, ejecución de código y otras</u> herramientas listas para producción 

- **<u>Integración de las herramientas del MCP</u>** <u>: integración de las herramientas del</u> Protocolo de contexto de modelo 

- **<u>Herramientas de función</u>** <u>: documentación detallada sobre firmas de funciones,</u> cadenas de documentación y patrones 

- **<u>Fundamentación de la Búsqueda de Google</u>** : uso de la herramienta Búsqueda de Google con fundamentación y citas 

## **Recursos del MCP** 

- **<u>Registro de los servidores MCP</u>** <u>: catálogo oficial de los servidores MCP</u> 

- **<u>Documentación oficial del MCP</u>** <u>: especificaciones y guías del protocolo</u> 

- **<u>MCP GitHub</u>** : implementaciones de referencia 

# **Recursos** 

## **De la comunidad** 

- **<u>Tools Make an Agent: From Zero to Assistant with ADK</u>** : blog oficial de Google Cloud que ofrece una descripción general completa de las herramientas de funciones, las herramientas integradas y los patrones de organización de herramientas 

- **<u>Google ADK Masterclass Part 2: Adding Tools to Your Agents</u>** : tutorial detallado sobre cómo agregar herramientas a los agentes con ejemplos prácticos y prácticas recomendadas 

- **<u>Building AI Agents with Google's ADK: Part 2 — Function Calling</u>** : análisis profundo de las herramientas de funciones personalizadas que abarcan firmas, cadenas de documentación y patrones de retorno 

- **<u>A Guide to ADK Tools: Leveraging Function Tools and Built-in Tools</u>** : guía con ejemplos prácticos de herramientas integradas y personalizadas 

- **<u>Use Google ADK and MCP with an external server</u>** : guía oficial para integrar las herramientas del MCP (Protocolo de contexto de modelo) para una integración avanzada de herramientas 

# **¿Tienes preguntas? Publica en el foro de la** **<u>comunidad</u>** 

# **Próximos pasos** 

- **Curso 6: Agrega protecciones con devoluciones de llamada** : implementa supervisión, seguridad y control 

# **Reflexiones finales** 

Comenzaste este curso con agentes que podían pensar y responder de manera inteligente. Lo estás terminando con agentes que pueden **actuar** en el mundo. 

### **Tu transformación es significativa:** 

De agentes limitados por datos de entrenamiento del LLM a agentes que pueden buscar en la Web en tiempo real, ejecutar código para cálculos precisos, acceder a tus bases de datos, llamar a las APIs y ejecutar tu lógica empresarial. Esta es la diferencia entre un chatbot y un asistente. 

### **Las habilidades que desarrollaste son fundamentales:** 

El diseño de instrucciones estratégicas, los patrones de manejo de errores, la coordinación de herramientas y el patrón de agente como herramienta no son solo técnicas para este curso. Son principios básicos que aplicarás en toda la ruta de aprendizaje del ADK y en cada agente que crees. 

### **La ecuación principal está completa:** 

Agente = modelo + herramientas + organización 

Entiendes el modelo (cursos 2 a 3). Implementaste herramientas (curso 5). A continuación, dominarás la organización en los próximos cursos. 

**¿Tienes preguntas o comentarios?** Compártelos en el Foro de la comunidad del ADK 

**¿Todo listo para el siguiente desafío?** Los próximos cursos te enseñarán a supervisar, controlar, coordinar y escalar los agentes habilitados para herramientas que ahora puedes crear. 

