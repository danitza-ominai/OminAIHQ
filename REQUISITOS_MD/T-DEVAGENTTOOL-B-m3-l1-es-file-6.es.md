# **La solución: Protocolo de contexto del modelo (MCP)** 

## **Un adaptador universal para herramientas** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre las herramientas del MCP | Documentación oficial del MCP</u>_ 

### **¿Qué es el MCP?** 

El MCP (Protocolo de contexto del modelo) es un **estándar abierto** que creó Anthropic y ahora aloja The Linux Foundation. Permite que los agentes de IA se conecten a servidores de herramientas externos a través de un protocolo universal. Piensa en ello como un USB para herramientas de IA: cualquier servidor compatible con MCP puede proporcionar herramientas a cualquier cliente compatible con MCP, independientemente del framework de IA que se utilice. 

### **De la documentación del ADK:** 

“ADK te ayuda a utilizar y consumir herramientas del MCP en tus agentes. Consulta la documentación de las herramientas del MCP para ver muestras de código y patrones de diseño que te ayudarán a usar el ADK junto con los servidores MCP”. 

### **Dos patrones de integración con el ADK:** 

ADK admite dos patrones de integración del MCP: 

1. **Uso de servidores de MCP existentes** : Tu agente de ADK actúa como un cliente del MCP y consume herramientas de servidores externos _(este módulo)_ . 

2. **Exposición de herramientas del ADK a través del MCP** : Se crea un servidor MCP que encapsula las herramientas del ADK, lo que las hace accesibles para cualquier cliente de MCP _(avanzado, consulta la documentación)_ . 

Este módulo se centra en el **Patrón 1** : Conexión a servidores MCP preexistentes para ampliar las capacidades de tu agente. 

## **Por qué es importante el MCP** 

### **El poder de la estandarización:** 

|**Sin MCP**|**Con MCP**|
|---|---|
|Cada herramienta necesita un código de<br>integración personalizado|Un patrón de integración funciona para todas las<br>herramientas|
|Las herramientas están limitadas a frameworks<br>de IA específicos|Las herramientas funcionan con Claude, GPT,<br>Gemini y más|



|**Sin MCP**|**Con MCP**|
|---|---|
|Te encargas de mantener cada integración|La comunidad y los proveedores mantienen sus<br>herramientas|
|Se limita a lo que está integrado en tu framework|Acceso a un ecosistema en crecimiento de<br>cientos de herramientas|



### **Adopción por parte de la industria:** 

- ✅ **Anthropic** creó el protocolo (noviembre de 2024) 

- ✅ **OpenAI** adoptó oficialmente MCP (marzo de 2025) 

- ✅ **Google ADK** proporciona compatibilidad nativa con MCP a través de McpToolset 

- ✅ **The Linux Foundation** ahora aloja MCP como estándar abierto 

### **Qué significa esto para ti:** 

- **Escribe una vez, usa en cualquier lugar** : las herramientas del MCP funcionan en todos los frameworks de IA 

- **Aprovecha el ecosistema** : utiliza las herramientas que crean los especialistas (bases de datos, APIs, servicios en la nube) 

- **Mantente al día:** a medida que se publiquen nuevos servidores MCP, tu agente podrá usarlos inmediatamente 

- **Separación de preocupaciones** : concéntrate en la lógica de tu agente y deja que los encargados del mantenimiento de las herramientas se ocupen de las integraciones 

## **Encuentra servidores MCP** 

Antes de crear herramientas personalizadas, verifica si ya existe un servidor MCP para tu caso de uso. 

### **Recursos oficiales:** 

|**Recurso**|**Descripción**|**Vínculo**|
|---|---|---|
|**Registro del servidor MCP**|Catálogo oficial de servidores<br>MCP con opciones de búsqueda|registry.modelcontextprotocol.io|
|**Servidores de referencia**|Servidores oficiales que<br>mantiene el equipo de MCP|github.com/modelcontextprotocol<br>/servers|
|**Documentación de MCP**|Especificación completa del<br>protocolo y guías|modelcontextprotocol.io|



### **Los servidores MCP más populares incluyen lo siguiente:** 

- **Sistema de archivos** : lee/escribe archivos y directorios 

- **GitHub** : gestión de repositorios, incidencias y solicitudes de extracción 

- **Slack** : envía mensajes y lee canales 

- **PostgreSQL/MySQL** : consultas de bases de datos 

- **Notion** : acceso a documentos y bases de datos 

- **Google Drive** : acceso al almacenamiento de archivos 

**Sugerencia:** Busca en el <u>registro de MCP</u> antes de escribir herramientas personalizadas; es posible que la capacidad que necesitas ya exista. 

## **Cómo funciona MCP en ADK** 

### **Flujo de integración:** 

graph LR A[Agente del ADK] --> B[McpToolset] B --> C[Servidor MCP] C --> D[Herramientas: list_directory, read_file, etc.] style A fill:#e1f5ff style B fill:#ffeb99 style C fill:#eeffee 

### **El proceso:** 

1. Los **servidores MCP** exponen herramientas a través del protocolo MCP estandarizado. 

2. Los **agentes del ADK** se conectan a los servidores con McpToolset . 

3. **Las herramientas se descubren automáticamente** , no es necesario realizar un registro manual. 

4. **Tu agente usa estas herramientas** exactamente como cualquier otra herramienta del ADK. 

_Los agentes del ADK se conectan a los servidores MCP a través de McpToolset y descubren automáticamente las herramientas disponibles_ 

# **Conceptos básicos** 

## **1. La clase McpToolset** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre las herramientas del MCP</u>_ 

### **De la documentación del ADK:** 

“La clase McpToolset se puede agregar directamente a la lista tools de tu agente, lo que permite una conexión fluida a un servidor MCP, el descubrimiento de sus herramientas y su disponibilidad para que el agente las use”. 

### **Qué hace McpToolset :** 

1. **Se conecta** a un servidor MCP con parámetros de conexión 

2. **Descubre** automáticamente las herramientas disponibles en el servidor 

3. **Actúa como proxy** para las llamadas a herramientas desde tu agente hacia el servidor MCP 

4. **Devuelve** los resultados a tu agente 

### **Cómo usarla:** 

from google.adk.agents import LlmAgent from google.adk.tools.mcp_tool import McpToolset from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams from mcp import StdioServerParameters 

agent = LlmAgent( model='gemini-2.5-flash', name='my_agent', instruction="Utiliza las herramientas disponibles para ayudar a los usuarios.", tools=[ McpToolset( connection_params=StdioConnectionParams( server_params=StdioServerParameters( command='npx', args=['-y', '@some/mcp-server'], ), ), ) ], ) 

### **Qué se debe tener en cuenta:** 

- McpToolset se incluye en la lista tools como cualquier otra herramienta. 

- Los parámetros de conexión le indican al ADK cómo llegar al servidor MCP. 

- Las herramientas del servidor estarán disponibles para tu agente de forma automática. 

## **2. Tipos de conexiones** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre las herramientas del MCP</u>_ 

ADK admite dos formas de conectarse a servidores MCP: 

**StdioConnectionParams (servidores locales)** 

Inicia un servidor MCP como un subproceso local en tu máquina. 

from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams from mcp import StdioServerParameters 

# Conexión al servidor local connection = StdioConnectionParams( server_params=StdioServerParameters( command='npx',                                    # Comando a ejecutar args=['-y', '@modelcontextprotocol/server-filesystem', '/path'],  # Argumentos ), ) 

**Cuándo se usa:** desarrollo, pruebas y situaciones de usuario único. 

### **SseConnectionParams (servidores remotos)** 

Se conecta a un servidor MCP que se ejecuta de forma remota a través de HTTP. 

from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams 

# Conexión al servidor remoto connection = SseConnectionParams( url="https://your-mcp-server.example.com/sse", headers={'Authorization': 'Bearer YOUR_TOKEN'}, ) 

**Cuándo se usa:** implementaciones de producción, servidores MCP alojados en la nube. 

### **Comparación de tipos de conexión:** 

|**Aspecto**|**StdioConnectionParams**|**SseConnectionParams**|
|---|---|---|
|**Ubicación del servidor**|Local (subproceso)|Remoto (HTTP)|
|**Configuración**|Simple (comando npx)|Requiere infraestructura de<br>servidor|
|**Ideal para**|Desarrollo, pruebas|Producción, nube|
|**Escalabilidad**|Único usuario|Varios usuarios|



## **3. Filtrado de herramientas** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre las herramientas del MCP</u>_ 

Los servidores MCP pueden exponer muchas herramientas, pero es posible que solo desees que tu agente use algunas específicas. El parámetro tool_filter te permite controlar qué herramientas están disponibles. 

### **Por qué filtrar herramientas** 

- ✅ **Seguridad** : Usa herramientas de solo lectura y excluye las operaciones peligrosas. 

- ✅ **Simplicidad** : Dale al agente solo lo que necesita para su tarea. 

- ✅ **Enfoque** : Reduce la confusión causada por demasiadas opciones de herramientas. 

### **Cómo usarla:** 

McpToolset( connection_params=StdioConnectionParams(...), tool_filter=['list_directory', 'read_file'],  # Solo estas herramientas ) 

### **Ejemplo: Cómo restringir el acceso al sistema de archivos** 

# ✅ Recomendable: exponer únicamente herramientas seguras y de solo lectura McpToolset( connection_params=StdioConnectionParams( server_params=StdioServerParameters( command='npx', args=['-y', '@modelcontextprotocol/server-filesystem', '/allowed/path'], ), ), tool_filter=['list_directory', 'read_file'],  # Sin acceso de escritura ) # ❌ Riesgoso: exponer todas las herramientas, incluidas las operaciones de escritura McpToolset( connection_params=StdioConnectionParams( server_params=StdioServerParameters( command='npx', args=['-y', '@modelcontextprotocol/server-filesystem', '/'], ), ), # Sin filtro = todas las herramientas expuestas, incluidas write_file, delete, etc. ) 

**Práctica recomendada:** Utiliza siempre tool_filter en producción para exponer solo las herramientas que necesita tu agente. 

## **4. Elige el tipo de herramienta adecuado** 

_¿Cuándo deberías utilizar las herramientas del MCP en lugar de herramientas integradas o herramientas con funciones personalizadas?_ 

### **El marco de decisiones:** 

¿Necesitas esta capacidad? 

│ ├─► ¿Es la Búsqueda de Google o la ejecución de código? │ └─► SÍ → Usa herramientas integradas (módulo 2) │ 

├─► ¿Ya existe un servidor MCP para esto? 

- │ └─► SÍ → Utiliza las herramientas del MCP (este módulo) 

- │           Consulta: registry.modelcontextprotocol.io 

- │ 

- └─► ¿Es esta tu propia lógica empresarial o un sistema propio? 

- └─► SÍ → Escribe herramientas de funciones personalizadas (módulo 4) 

### **Diferencias clave que importan:** 

|**Aspecto**|**Herramientas del MCP**|**Herramientas**<br>**integradas**|**Herramientas de**<br>**funciones**<br>**personalizadas**|
|---|---|---|---|
|**¿Quién se encarga del**<br>**mantenimiento?**|Comunidad/proveedores|Equipo del ADK|Tú|
|**Esfuerzo de**<br>**configuración**|Conectar y configurar|Importar|Escribir código|
|**Portabilidad**|Funciona en todos los<br>frameworks de IA|Solo ADK|Solo ADK|
|**Personalización**|Limitada a las opciones<br>del servidor|Limitada|Control total|
|**Tiempo para**<br>**implementar**|Minutos|Minutos|Horas a días|



### **Las herramientas del MCP son ideales cuando:** 

- ✅ La capacidad es **común** (archivos, bases de datos, APIs populares) 

   - ✅ Alguien más **ya resolvió** el problema de integración 

- 

   - ✅ Quieres **portabilidad** entre frameworks de IA 

- 

- ✅ Prefieres **herramientas mantenidas** en lugar de escribir las tuyas propias 

### **Las herramientas de funciones personalizadas son mejores cuando:** 

- ✅ La lógica es **única** para tu negocio 

- ✅ Te estás conectando a sistemas internos **propios** 

   - ✅ Necesitas **control total** sobre el comportamiento y el manejo de errores 

- 

- ✅ **No existe ningún servidor MCP** para tu caso de uso específico 

### **Ejemplo de toma de decisiones real:** 

|**Necesidad**|**Decisión**|**Razones**|
|---|---|---|
|Leer los archivos del disco|MCP:<br>@modelcontextprotocol/se<br>rver-filesystem|El acceso al sistema de archivos<br>es común; existe un servidor<br>MCP|
|Consultar la base de datos de|MCP:|El acceso a la base de datos es|



|**Necesidad**|**Decisión**|**Razones**|
|---|---|---|
|PostgreSQL|@modelcontextprotocol/se<br>rver-postgres|común; existe un servidor MCP|
|Calcular el costo de envío|Herramienta de función<br>personalizada|Lógica específica de cada<br>negocio; solo tú conoces las<br>tarifas|
|Acceder a la API interna de<br>empleados|Herramienta de función<br>personalizada|Sistema propio; sin servidor MCP<br>público|



# 🧪 **Ejemplo práctico** 

## **Crea un asistente de lectura de archivos con las herramientas del MCP** 

**Lo que crearás:** un agente que pueda enumerar y leer archivos con el servidor MCP del sistema de archivos. 

### **Requisitos previos:** 

- Node.js y npm instalados (para el comando npx) 

## **Paso 1: Crea el proyecto** 

adk create file_reader_assistant cd file_reader_assistant 

### **Qué hace:** 

- Crea un nuevo directorio de proyecto del ADK. 

- Configura la estructura básica del agente. 

- Crea agent.py con el código de agente predeterminado. 

## **Paso 2: Crea una carpeta de prueba con archivos** 

mkdir -p my_files echo "Hola, este es un archivo de prueba." > my_files/hello.txt echo "Este es otro archivo con contenido diferente." > my_files/notes.txt 

### **Qué hace:** 

- Crea una carpeta a la que accederá el servidor MCP. 

- Agrega archivos de muestra para que el agente los lea. 

## **Paso 3: Escribe el agente** 

Reemplaza el contenido de agent.py por lo siguiente: 

""" Agente asistente de lectura de archivos Demuestra la integración de herramientas del MCP con ADK utilizando el servidor MCP del sistema de archivos. 

Referencia: https://google.github.io/adk-docs/tools-custom/mcp-tools/ """ 

import os from google.adk.agents import LlmAgent from google.adk.tools.mcp_tool import McpToolset from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams from mcp import StdioServerParameters # Define la carpeta para permitir el acceso al archivo (debe ser una ruta de acceso absoluta) ALLOWED_PATH = os.path.abspath("./my_files") # Crea la carpeta si no existe os.makedirs(ALLOWED_PATH, exist_ok=True) # Crea el agente con las herramientas del sistema de archivos MCP root_agent = LlmAgent( model='gemini-2.5-flash', name='file_reader_assistant', description='Ayuda a los usuarios a leer y explorar archivos con las herramientas del MCP.', instruction=""" Eres un asistente de lectura de archivos que ayuda a los usuarios a explorar archivos. Tus capacidades: - Mostrar una lista de archivos en los directorios con list_directory - Leer el contenido del archivo con read_file Cuando ayudes a los usuarios: 1. Utiliza list_directory para mostrar los archivos disponibles. 2. Utiliza read_file para mostrar el contenido del archivo cuando se te solicite. 3. Describe lo que encuentras de una manera útil. Expresa con claridad cuál es la carpeta con la que estás trabajando. """, tools=[ McpToolset( 

connection_params=StdioConnectionParams( server_params=StdioServerParameters( command='npx', args=[ '-y', '@modelcontextprotocol/server-filesystem', ALLOWED_PATH, ], ), ), # Filtra para exponer únicamente herramientas seguras y de solo lectura tool_filter=['list_directory', 'read_file'], ) ], ) 

### **Explicación del código:** 

### **Líneas 9 a 14: Ajuste y configuración** 

- Importa McpToolset y clases de conexión desde ADK. 

- Importa StdioServerParameters desde el paquete MCP. 

- Define ALLOWED_PATH como una ruta de acceso absoluta a la carpeta de archivos. 

### **Líneas 17 a 18: Crea una carpeta** 

- Asegúrate de que la carpeta de destino exista antes de que se ejecute el agente. 

### **Líneas 21 a 47: Crea un agente con las herramientas del MCP** 

- McpToolset se conecta al servidor MCP del sistema de archivos. 

- StdioConnectionParams inicia el servidor a través de npx. 

- tool_filter limita las herramientas a list_directory y read_file 

- Las instrucciones guían al agente sobre cómo utilizar estas herramientas. 

## **Paso 4: Ejecuta y prueba** 

adk web 

Desde tu navegador, ve a http://localhost:8000 . 

## **Paso 5: Situaciones de prueba** 

### **Prueba 1: Muestra listas de archivos** 

Tú: ¿Qué archivos hay en la carpeta? 

### **Comportamiento esperado:** 

- El agente llama a la herramienta list_directory a través de MCP. 

- La herramienta devuelve una lista de archivos en la carpeta my_files . 

- El agente te presenta la lista de archivos. 

### **Qué se debe tener en cuenta:** 

- El agente descubrió y utilizó la herramienta del MCP automáticamente. 

- No se necesitó ningún código de herramienta personalizado: el servidor MCP proporcionó todo. 

### **Prueba 2: Lee un archivo** 

Tú: Muéstrame el contenido de hello.txt 

### **Comportamiento esperado:** 

- El agente llama a la herramienta read_file con la ruta de acceso al archivo. 

- La herramienta devuelve el contenido del archivo. 

- El agente te presenta el contenido. 

### **Qué se debe tener en cuenta:** 

- El agente invocó correctamente la herramienta del MCP con el argumento correcto. 

- - El contenido del archivo se devuelve a través del protocolo MCP. 

### **Prueba 3: Operaciones múltiples** 

Tú: Enumera los archivos y, a continuación, lee el archivo notes.txt 

### **Comportamiento esperado:** 

- El agente llama primero a list_directory . 

- Luego, el agente llama a read_file para notes.txt. 

- El agente presenta ambos resultados juntos. 

### **Qué se debe tener en cuenta:** 

- El agente organiza múltiples llamadas a las herramientas del MCP. 

- Los mismos patrones que aprendiste en el módulo 1 se aplican a las herramientas del MCP. 

# **Conclusiones principales** 

### **Qué es el MCP y por qué es importante:** 

- **Estándar abierto** para conectar agentes de IA a servidores de herramientas externos 

- - **Interoperabilidad universal:** compatible con todos los frameworks de IA (ADK, Claude, GPT) 

- **Adopción en la industria** : Anthropic, OpenAI, Google y The Linux Foundation 

- **Acceso al ecosistema:** cientos de herramientas prediseñadas para tareas comunes 

### **Usa MCP en ADK:** 

- **McpToolset** conecta tu agente a los servidores MCP. 

- **Las herramientas se detectan automáticamente** : no es necesario realizar un registro manual. 

- **Úsala como cualquier otra herramienta** : se aplican los mismos patrones del módulo 1. 

### **Tipos de conexiones:** 

- **StdioConnectionParams** : servidores locales a través de subprocesos (desarrollo) 

- **SseConnectionParams** : servidores remotos a través de HTTP (producción) 

### **Seguridad con filtrado de herramientas:** 

- **Usa tool_filter** para exponer solo las herramientas necesarias. 

- **Limita a solo lectura** cuando sea posible por seguridad. 

- **Menos herramientas = decisiones más claras** para tu agente. 

### **Cuándo utilizar cada tipo de herramienta:** 

|**Situación**|**Enfoque**|**Por qué**|
|---|---|---|
|Capacidad preexistente<br>(archivos, bases de datos, APIs)|Herramientas del MCP|La comunidad se encarga de<br>mantenerlas|
|Capacidades de Google<br>(búsqueda, ejecución de código)|Herramientas integradas|El equipo de ADK se encarga de<br>mantenerlas|
|La lógica específica de tu<br>negocio|Herramientas de funciones<br>personalizadas|Solo tú conoces tu negocio|



### **Recursos clave:** 

- <u>Registro de servidores MCP: Encuentra servidores MCP existentes</u> 

- <u>Documentación oficial del MCP: Documentación del protocolo</u> 

- <u>Guía de MCP para ADK: Documentación de integración del ADK</u> 

# **Más allá de este módulo: capacidades avanzadas del MCP** 

En este módulo, se abordaron los aspectos básicos del uso de servidores MCP existentes. MCP y ADK ofrecen capacidades adicionales para casos de uso más avanzados. 

### **¿Qué más puedes hacer con MCP en el ADK?** 

|**Capacidad**|**Descripción**|**Documentación**|
|---|---|---|
|**Crea tu propio servidor MCP**|Une tus herramientas<br>personalizadas en un servidor<br>MCP para compartirlas con otros|Artículo de la documentación del<br>ADK sobre cómo crear<br>servidores MCP|
|**Expón las herramientas del**<br>**ADK a través de MCP**|Haz que tus herramientas del<br>ADK sean accesibles para<br>cualquier cliente de MCP<br>(Claude, GPT, etc.)|Artículo de la documentación del<br>ADK sobre las herramientas del<br>MCP|
|**Conéctate a múltiples**<br>**servidores MCP**|Utiliza herramientas de varios<br>servidores MCP en un solo<br>agente|Artículo de la documentación del<br>ADK sobre las herramientas del<br>MCP|
|**Implementa servidores MCP en**<br>**Cloud Run**|Aloja tus servidores MCP para su<br>uso en producción|Artículo de la documentación del<br>ADK sobre las herramientas del<br>MCP|



### **El segundo patrón de integración (avanzado):** 

Anteriormente, mencionamos que ADK admite dos patrones de integración del MCP. El segundo patrón ( **exponer las herramientas del ADK a través de un servidor MCP** ) te permite lo siguiente: 

1. Unir tus herramientas del ADK existentes en un servidor MCP 

2. Poner esas herramientas a disposición de cualquier cliente compatible con MCP 

3. Compartir tus herramientas con el ecosistema de IA más amplio 

Esto es valioso cuando deseas que otros frameworks de IA (Claude, GPT, etc.) utilicen herramientas que creaste en ADK. 

