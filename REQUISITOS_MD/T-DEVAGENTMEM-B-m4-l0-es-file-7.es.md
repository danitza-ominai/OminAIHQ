# 🎉 **¡Felicitaciones!** 

Completaste el curso 4, Controla la memoria y el estado de los agentes 

En este curso, tus agentes dejaron de ser respondedores sin estado y los transformaste en asistentes inteligentes con administración de estado. Aprendiste a brindarles **control programático** sobre los datos, lo que permite realizar un seguimiento exacto, otorgar comportamiento dinámico y establecer preferencias persistentes que no se pueden proporcionar solo con el historial de conversaciones. 

### **Transformación:** 

- **Antes del curso 4:** Agentes que responden a consultas, pero dependen completamente del historial de conversaciones (sin acceso programático a los datos ni forma de verificar los valores exactos mediante código) 

- **Después del curso 4:** Agentes con administración de estado completa (control programático sobre valores exactos, inserción automática de datos mediante plantillas y preferencias de usuario persistentes en todas las sesiones con alcances de persistencia adecuados) 

Ahora tienes las habilidades para crear agentes que recuerdan, hacen seguimiento y se adaptan: la base para diseñar aplicaciones sofisticadas con estado. 

# **Objetivos logrados** 

Comenzaste esta lección con agentes basados en LLM básicos y la terminaste con sistemas con estado capaces de hacer lo siguiente: 

- **Acceder al estado de manera programática** con session.state para verificar el valor exacto 

- **Guardar datos automáticamente** usando el parámetro output_key 

- **Insertar valores de estado** en instrucciones con la sintaxis de plantillas {var} 

- **Conservar las preferencias del usuario** en todas las sesiones con el espacio de nombres user: 

- **Hacer un seguimiento de métricas exactas** , como el recuento de interacciones, sin depender de la interpretación del LLM 

- **Elegir los alcances de persistencia adecuados** ( temp: , sesión, user: o app: ) 

- - **Crear agentes dinámicos** con instrucciones que se adaptan según los valores de estado 

### **Habilidades adquiridas:** 

- Comprender los conceptos básicos del estado y por qué son esenciales para el control programático 

- Acceder al estado a través de session.state después de ejecutar agentes con Runner 

- Usar output_key para guardar automáticamente la respuesta en el estado 

- Usar plantillas {var} para inyectar instrucciones dinámicas 

- Administrar espacios de nombres de estado para usar los alcances de persistencia apropiados 

- Decidir cuándo utilizar cada espacio de nombres en función de las necesidades de duración de los datos 

- Implementar patrones de inicialización de sesión y preferencias de usuario 

### **Recorrido:** 

- Parte 1: Comprende el estado de la sesión y el acceso programático con Runner 

- Parte 2: Domina las plantillas de estado {var} para escribir instrucciones dinámicas 

- - Parte 3: Aprende sobre los espacios de nombres de estado y los alcances de persistencia 

# **Tu recorrido** 

## **Parte 1: ¿Qué es el estado de la sesión? (aprox. 15 minutos)** 

Aprendiste qué es el estado de la sesión y por qué es esencial para el control programático, y solucionaste problemas que no se pueden abordar solo con el historial de conversaciones. 

### **Conceptos clave dominados:** 

- ✅ El estado proporciona acceso programático al que el historial de conversaciones no tiene acceso. 

- ✅ session.state es un diccionario al que se accede después de ejecutar agentes. 

- ✅ output_key guarda automáticamente las respuestas del agente en el estado. 

- ✅ El estado permite el seguimiento exacto, la creación de plantillas, las decisiones de enrutamiento y la persistencia entre sesiones. 

- ✅ Utiliza InMemorySessionService y Runner para acceder al estado de manera programática. 

**Consideración clave:** "Si bien los agentes basados en LLM reciben el historial de conversaciones completo de forma predeterminada, la diferencia clave es que el estado proporciona **acceso programático** . Mediante código, puedes verificar if session.state.get('user_name'): , lo cual es imposible solo con el historial de conversaciones". 

### **Patrón de código:** 

from google.adk.agents import LlmAgent from google.adk.runners import Runner from google.adk.sessions import InMemorySessionService 

# Agente con output_key para guardar la respuesta root_agent = LlmAgent( 

model='gemini-2.5-flash', name='name_extractor', instruction="Extrae el nombre de la persona del mensaje. Devuelve SOLO el nombre, nada más.", output_key="user_name"  # Guarda la respuesta en state["user_name"] ) 

# Configuración y ejecución session_service = InMemorySessionService() session = session_service.create_session(app_name="my_app", user_id="user1") runner = Runner(agent=root_agent, app_name="my_app", session_service=session_service) 

result = runner.run(user_id="user1", session_id=session.id, new_message="Me llamo Álex") 

# Accede al estado de manera programática print(session.state)  # {'user_name': 'Álex'} if session.state.get("user_name"): print(" ✅ Se extrajo correctamente el nombre") 

## **Parte 2: Crea plantillas de estado (aprox. 15 minutos)** 

Aprendiste a usar la plantilla {var} para insertar valores de estado en las instrucciones del agente, lo que permite que tenga un comportamiento dinámico. 

### **Conceptos clave dominados:** 

- ✅ La plantilla {var} inserta state["var"] en las instrucciones antes de llamar al LLM. 

- ✅ La sintaxis opcional {var?} no genera un error si falta la clave. 

- ✅ {var?predeterminado} proporciona el valor "predeterminado" si falta la clave. 

- 

- 

- ✅ El ADK resuelve las plantillas automáticamente antes de enviarlas al LLM. 

- ✅ Elimina la necesidad de darles formato manual a las cadenas. 

**Consideración clave:** “La plantilla {var} del ADK resuelve automáticamente los valores de estado antes de que la instrucción llegue al LLM, lo que permite escribir instrucciones dinámicas y contextuales sin administrar cadenas de forma manual”. 

### **Patrón de código:** 

from google.adk.agents import LlmAgent 

# Agente con plantillas de estado root_agent = LlmAgent( model='gemini-2.5-flash', name='personalized_greeter', instruction=""" Eres un asistente amigable. Información del usuario: 

- Nombre: {user_name?usuario} - Idioma preferido: {user_language?English} - Membresía: {membership_tier?free} {membership_tier?Tu nivel de membresía es {membership_tier}} Saluda amablemente al usuario y ofrécele ayuda. Responde en {user_language?English}. """ ) 

# Establece el estado manualmente (simulando interacción previa) session.state["user_name"] = "Álex" session.state["user_language"] = "Spanish" session.state["membership_tier"] = "premium" 

# Cuando se ejecuta el agente, la instrucción se resuelve en lo siguiente: # "Hola, Álex… Responde en español… Tu nivel de membresía es premium" 

## **Parte 3: Espacios de nombres de estado y alcance (aprox. 15 minutos)** 

Aprendiste sobre los cuatro espacios de nombres de estado, que controlan por cuánto tiempo persisten los datos y quiénes pueden acceder a ellos. 

### **Conceptos clave dominados:** 

- ✅ El estado de temp: se descarta después de completar el turno (está centrado en la invocación). 

- ✅ El estado de la sesión (sin prefijo) persiste durante todos los turnos y se pierde cuando finaliza la sesión. 

- 

- 

- 

- 

- ✅ El estado de user: persiste en todas las sesiones de ese usuario. 

- ✅ El estado de app: es global para todos los usuarios. 

- ✅ Utiliza el alcance más limitado necesario (no persistas demasiado). 

- ✅ Los espacios de nombres de estado controlan la duración y el uso compartido. 

**Consideración clave:** "Utiliza el **alcance más limitado** que se ajuste a tus necesidades. No conserves los datos más tiempo del necesario. Para los datos temporales, usa temp: ; para el contexto de la conversación, el estado de la sesión; para las preferencias del usuario, user: , y para la configuración global, app: ". 

### **Patrón de código:** 

from google.adk.agents import LlmAgent 

root_agent = LlmAgent( model='gemini-2.5-flash', name='namespace_demo', instruction=""" 

Eres un asistente de demostración que muestra los espacios de nombres de estado. 

=== Estado de la app (global para todos los usuarios) === Nombre de la app: {app:name?Demostración de espacios de nombres} Versión de la app: {app:version?1.0} 

=== Estado del usuario (persiste entre sesiones) === Preferencia del usuario: {user:theme?not set} === Estado de la sesión (persiste en esta conversación) === Tema de conversación: {topic?not set} 

=== Estado temporal (solo turno actual) === Paso actual: {temp:step?not set} 

Responde con un mensaje amigable mostrando estos valores de espacio de nombres. """, output_key="response" ) # Establece los cuatro tipos de espacios de nombres session.state["app:name"] = "Demostración de espacios de nombres"      # Global para todos los usuarios session.state["app:version"] = "2.0"              # Global para todos los usuarios session.state["user:theme"] = "dark"              # Persiste entre sesiones session.state["topic"] = "state management"       # Persiste en esta sesión session.state["temp:step"] = "initialization"     # Se descarta después del turno 

# Después de que se ejecuta el agente: 

- # - Se DESCARTA temp:step (después del turno). 

- # - topic persiste (centrado en la sesión). 

- # - user:theme persiste (centrado en el usuario, sobrevive al final de la sesión) 

- # - app:version persiste (global, todos los usuarios lo ven) 

# **Qué puedes hacer** 

Con tu dominio del estado, puedes crear agentes inteligentes: 

## **Accede al estado de manera programática** 

- Utiliza InMemorySessionService y Runner para acceder directamente al estado. 

- Verifica los valores exactos con session.state.get("key") . 

- Toma decisiones de enrutamiento basadas en valores de estado. 

- Realiza un seguimiento de métricas y contadores de manera programática. 

## **Utiliza plantillas de estado** 

- Inserta valores de estado en instrucciones con {var} . 

- Maneja claves faltantes con sintaxis opcional {var?} . 

- Proporciona valores predeterminados con el patrón {var?default} . 

- Crea instrucciones dinámicas y adaptadas al contexto. 

## **Administra adecuadamente la persistencia del estado** 

- Utiliza temp: para procesar datos de forma intermedia. 

- Utiliza el estado de la sesión para el contexto de la conversación. 

- Utiliza user: para las preferencias de usuario entre sesiones. 

- Utiliza app: para la configuración global. 

- Elige el espacio de nombres adecuado para cada caso de uso. 

## **Crea aplicaciones con estado** 

- Guarda las respuestas del agente automáticamente con output_key . 

- - Inicializa sesiones con valores de estado predeterminados. - Sigue el progreso de la conversación a lo largo de los turnos. 

- Recuerda las preferencias del usuario en todas las sesiones. 

- Implementa personalización basada en el estado del usuario. 

# **Aplicaciones reales** 

## **Aplicación: Agente personalizado del servicio de atención al cliente** 

Combina plantillas de estado y espacios de nombres para la asistencia al cliente: 

from google.adk.agents import LlmAgent from google.adk.runners import Runner from google.adk.sessions import InMemorySessionService 

# Establece la configuración session_service = InMemorySessionService() session = session_service.create_session(app_name="support", user_id="customer1") 

# Inicializa el estado session.state["user:name"] = "Álex Jiménez" session.state["user:tier"] = "premium" session.state["user:language"] = "English" session.state["app:business_hours"] = "24/7" session.state["app:escalation_threshold"] = 3 

# Agente con plantillas root_agent = LlmAgent( model='gemini-2.5-flash', instruction=""" Eres un agente de asistencia al cliente {user:tier}. Información del cliente: - Nombre: {user:name?Guest} 

- Nivel de asistencia: {user:tier?standard} 

- Idioma: {user:language?English} 

Información de la sesión: 

- Mensaje #{messages_in_conversation?1} - Problema: {issue_category?general support} 

Horario de atención: {app:business_hours} 

{needs_escalation? ⚠ SE ALCANZÓ EL UMBRAL DE DERIVACIÓN. Deriva el caso a un agente humano si no se resuelve.} 

Responde en {user:language} con asistencia personalizada. """, output_key="response" ) 

runner = Runner(agent=root_agent, app_name="support", session_service=session_service) 

### **Casos de uso:** 

- Chat de asistencia al cliente con personalización 

- Asistencia técnica con acceso por niveles 

- Automatización del departamento de ayuda con seguimiento de derivaciones 

# **Conclusiones principales para recordar** 

Estos son los aspectos más importantes de la lección 4: 

## **1. El estado proporciona control programático** 

Si bien los agentes basados en LLM reciben el historial de conversaciones completo de forma predeterminada, el estado habilita lo siguiente: 

- **Acceso programático** : if session.state.get("count") >= 3: 

- **Valores exactos:** No interpretaciones del LLM, sino datos programáticos precisos 

- - **Decisiones de enrutamiento:** Toma decisiones basadas en código sobre valores exactos 

**Principio clave:** El LLM puede leer tanto el historial de conversaciones como el estado, pero solo el estado le otorga a **tu código** control programático. 

## **2. output_key guarda automáticamente las respuestas del agente** 

El patrón para guardar el estado automáticamente es el siguiente: 

- **output_key="result"** : Guarda automáticamente la respuesta del agente en 

state["result"] . 

- No se necesita código manual: el ADK lo controla automáticamente. 

- Funciona con todos los espacios de nombres de estado ( output_key="user:pref" ). 

**Principio clave:** Utiliza la función output_key incorporada del ADK en lugar de la administración manual del estado. 

## **3. La plantilla {var} inserta el estado en las instrucciones** 

- # Instrucción estática (sin estado) instruction="Eres un asistente útil." 

# Instrucción dinámica (con estado) instruction=""" Eres un asistente útil. Idioma del usuario: {user:language?English} Turno {turn_count} {premium_user?Se habilitó el acceso a funciones premium.} """ 

### **Sintaxis de plantillas:** 

- {var} → Inserta un valor (se produce un error si falta). 

- {var?} → Inserta un valor (queda vacío si falta). 

- {var?predeterminado} → Inserta un valor o "predeterminado". 

- {var?Texto condicional} → Muestra texto solo si existe var. 

**Principio clave:** Utiliza plantillas de estado para insertar **valores programáticos exactos** en las instrucciones del LLM. 

## **4. Cuatro espacios de nombres de estado controlan el alcance de la persistencia** 

state["temp:var"]      # Se descarta después del turno state["var"]           # Se descarta después de la sesión state["user:var"]      # Persiste en todas las sesiones del usuario state["app:var"]       # Global para todos los usuarios 

### **Árbol de decisión:** 

- ¿Ahora necesitas solo datos? → temp: 

- ¿Necesitas datos de esta conversación? → sesión (sin prefijo) 

- ¿Necesitas datos de todas las conversaciones de los usuarios? → user: 

- ¿Necesitas datos globales para todos los usuarios? → app: 

**Principio clave:** Utiliza el **alcance más limitado** que requieras. No conserves los datos por 

más tiempo del necesario. 

## **5. Estado de acceso con el patrón Runner** 

# Establece la configuración session_service = InMemorySessionService() session = session_service.create_session(app_name="app", user_id="user1") runner = Runner(agent=agent, app_name="app", session_service=session_service) 

# Ejecuta el agente result = runner.run(user_id="user1", session_id=session.id, new_message=msg) # Accede al estado de manera programática value = session.state.get("key", default) if session.state.get("user_name"): 

- # Toma decisiones basadas en el estado pass 

**Principio clave:** Utiliza Runner para obtener acceso programático al estado de la sesión después de la ejecución del agente. 

# **Lista de verificación de prácticas recomendadas** 

Aplica estas prácticas recomendadas a todos tus agentes con estado: 

## **Administración de estado** 

- ✅ **Usa el patrón Runner** : Accede al estado de manera programática con session.state . 

- ✅ **Usa el alcance más reducido:** No conserves los datos por más tiempo del necesario. 

- ✅ **Limpia el estado temporal:** Usa temp: para datos intermedios. 

- ✅ **Claves de estado del documento** : Comenta qué representa cada variable de estado. 

## **Ahorro de datos** 

- ✅ **Prefiere output_key** : Úsala en lugar de la administración manual del estado. 

- ✅ **Elige el espacio de nombres con atención** : Cumple con las necesidades de persistencia. 

- ✅ **Valida los valores de estado** : Verifica los tipos y rangos antes de usarlos. 

## **Uso de plantillas** 

- ✅ **Usa plantillas {var}** : Inserta el estado en las instrucciones dinámicamente. 

- ✅ **Maneja las claves faltantes** : Usa {var?} para valores opcionales. 

- ✅ **Proporciona valores predeterminados** : Utiliza {var?predeterminado} cuando corresponda. 

- ✅ **Prueba con un estado vacío** : Asegúrate de que los valores predeterminados funcionen correctamente. 

## **Persistencia** 

- ✅ **Usa temp para un solo turno** : Datos de procesamiento intermedio 

- ✅ **Usa la sesión para la conversación** : Recuento de turnos o contexto de la conversación 

- ✅ **Usa user para las preferencias** : Idioma, tema o configuración 

- ✅ **Usa app para la configuración global** : Versión, marcas de funciones o reglas comerciales 

# **Referencia de patrones de código** 

## **Patrón 1: Acceso básico al estado** 

from google.adk.agents import LlmAgent from google.adk.runners import Runner from google.adk.sessions import InMemorySessionService 

# Agente con output_key agent = LlmAgent( instruction="Extrae el tema principal", output_key="topic" ) # Establece la configuración session_service = InMemorySessionService() session = session_service.create_session(app_name="app", user_id="user1") runner = Runner(agent=agent, app_name="app", session_service=session_service) 

# Ejecuta result = runner.run(user_id="user1", session_id=session.id, new_message=msg) # Accede al estado topic = session.state.get("topic") 

## **Patrón 2: Plantillas de estado** 

# Agente con plantillas de estado agent = LlmAgent( instruction=""" ¡Hola, {user_name?usuario}! Idioma preferido: {user:language?English} 

{premium_user? ✨ Se habilitaron las funciones premium.} Responde en {user:language?English}. """ ) # Establece el estado manualmente session.state["user_name"] = "Álex" session.state["user:language"] = "Spanish" session.state["premium_user"] = True # La instrucción se resuelve del siguiente modo: # "¡Hola, Álex! … Responde en español. ✨ Se habilitaron…" 

## **Patrón 3: Los cuatro espacios de nombres** 

agent = LlmAgent( instruction=""" App: {app:name?MyApp} (v{app:version?1.0}) Usuario: {user:name?Invitado} ({user:tier?free}) Sesión: Turno {turn_count?1} Procesamiento: {temp:step?start} """ ) 

# Establece el estado en diferentes espacios de nombres session.state["app:name"] = "Bot de asistencia"      # Global session.state["app:version"] = "2.0"           # Global session.state["user:name"] = "Álex"            # Específico del usuario session.state["user:tier"] = "premium"         # Específico del usuario session.state["turn_count"] = 5                # Específico de la sesión session.state["temp:step"] = "validating"      # Temporal 

# Después de completar el turno, ocurre lo siguiente: 

# - Se DESCARTA temp:step 

# - turn_count persiste (sesión) 

# - user:name persiste (usuario) 

- # - app:name persiste (global) 

# **Errores comunes** 

Errores habituales que debes evitar: 

## **Error 1: Alcance de persistencia incorrecto** 

# ❌ INCORRECTO: Usar el estado de la sesión para las preferencias del usuario state["language"] = "Spanish"  # Se pierde cuando finaliza la sesión 

# ✅ CORRECTO: Usar user: para las preferencias 

state["user:language"] = "Spanish"  # Persiste entre sesiones 

## **Error 2: No administrar las claves de estado faltantes** 

# ❌ INCORRECTO: Suponer que la clave existe instruction="Saluda a {user_name}"  # Se produce un error si user_name no existe # ✅ CORRECTO: Usar sintaxis opcional instruction="Saluda a {user_name?usuario}  # Si falta el valor, se usa el predeterminado: "usuario" 

## **Error 3: Hacer persistir excesivamente los datos temporales** 

# ❌ INCORRECTO: Hacer persistir los datos intermedios state["processing_step"] = "validating"  # Se mantiene para siempre 

# ✅ CORRECTO: Usar temp: para los datos temporales state["temp:processing_step"] = "validating"  # Se descarta después del turno 

# **Tarjeta de referencia rápida** 

## **Espacios de nombres de estados** 

```
temp:var       → Solo turno actual (se descarta después)
var            → Sesión actual (se descarta cuando finaliza la sesión)
user:var       → Específico del usuario (persiste entre sesiones)
app:var        → Global para todos los usuarios
```

## **Cómo acceder al estado** 

# Lectura value = session.state.get("key", default) 

# Escritura session.state["key"] = value 

## **Plantillas de estado** 

```
{var}              → Inserta un valor (se produce un error si falta).
{var?}             → Inserta un valor (queda vacío si falta).
{var?predeterminado}      → Inserta un valor o "predeterminado".
{var?Condicional}  → Muestra texto solo si existe var.
```

## **Ahorro de datos** 

# Guardado automático agent = LlmAgent(output_key="result") 

# Inserción automática 

agent = LlmAgent(instruction="Procesa {result}") 

## **Árbol de decisión** 

¿Qué tipo de datos? 

```
Valores estructurados → STATE
```

- ├─ ¿Para el turno actual? → temp: 

- ├─ ¿Para la sesión actual? → (sin prefijo) 

- ├─ ¿Es específico del usuario o de todas las sesiones? → user: └─ ¿Es global para todos los usuarios? → app: 

# **Comunidad y asistencia** 

## **Referencias principales** 

- 📚 **<u>Introducción al contexto conversacional</u>** <u>: Descripción general de la sesión, el</u> estado y la memoria en el ADK 

- 🔧 **<u>Documentación de la sesión</u>** : Implementaciones de SessionService y ciclo de vida de la sesión 

- 💾 **<u>Guía sobre administración de estado</u>** <u>: Espacios de nombres de estado,</u> persistencia y creación de plantillas con sintaxis {var} 

- 🧠 **<u>Documentación de la memoria</u>** : Memoria a largo plazo y recuperación basada en RAG entre sesiones 

- ☁ **<u>Administración de sesiones de Vertex AI</u>** <u>: Gestión de sesiones con el ADK en</u> Google Cloud 

# **Recursos** 

### **De la comunidad** 

- **<u>Remember this: Agent state and memory with ADK</u>** (una entrada del blog oficial de Google Cloud en la que se explican las sesiones, los prefijos de estado [user:, app: y temp:] y los patrones de persistencia de memoria) 

- **<u>How to use Sessions & State in Google ADK - Google Agent Development Kit for Beginners (Part 5)</u>** (un video tutorial completo de 17 minutos que abarca el ciclo de vida de las sesiones, la administración de estado, las implementaciones de SessionService y ejemplos prácticos de programación) 

- **<u>Google ADK Masterclass Part 5: Session and Memory Management</u>** (una guía detallada en la que se explica cómo el estado permite a los agentes recordar información sin pasarla en cada mensaje) 

- **<u>State and Memory Management in Google ADK: A Practical Tutorial</u>** (un instructivo práctico en el que se muestra cómo el ADK usa prefijos para determinar el alcance de la persistencia de datos) 

- **<u>Sessions and State Management in Google ADK — Building Context-Aware Agents (Part 4)</u>** (una guía práctica para crear agentes que mantengan el contexto en las conversaciones) 

# **Publica tus preguntas en el** **<u>foro de la comunidad</u>** 

