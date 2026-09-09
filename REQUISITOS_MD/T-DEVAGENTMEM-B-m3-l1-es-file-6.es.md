# **Solución: Espacios de nombres de estado** 

_Referencia:_ _<u>Organiza el estado con prefijos (documentación del ADK)</u>_ 

### **De la documentación del ADK:** 

“Los prefijos de las claves de estado definen su alcance y comportamiento de persistencia, especialmente con servicios persistentes”. 

El ADK proporciona **cuatro espacios de nombres de estado** con diferentes duraciones: 

|**Espacio de**<br>**nombres**|**Prefijo**|**Duración**|**Alcance**|**Ejemplo**|
|---|---|---|---|---|
|**Temporal**|temp:|Solo turno actual|Se descarta<br>después de la<br>invocación.|temp:step =<br>"validating"|
|**Sesión**|(ninguno)|Conversación<br>actual|Se pierde cuando<br>finaliza la sesión.|topic =<br>"refunds"|
|**Usuario**|usuario:|Todas las sesiones<br>de este usuario|Persiste entre<br>conversaciones.|user:theme =<br>"dark"|
|**App**|app:|Global para todos<br>los usuarios|Persiste durante<br>toda la app.|app:api_url =<br>"..."|



### **Cronología visual:** 

graph TD 

T[Estado de temp:] -->|Se descarta| T1[después de que termina el turno 1] S[Estado de la sesión] -->|Persiste| S1[hasta que termina la sesión] U[Estado de user:] -->|Persiste| U1[entre todas las sesiones] A[Estado de app:] -->|Persiste| A1[para todos los usuarios] 

style T fill:#ffe4e4 style S fill:#fff4e4 style U fill:#e4f4ff style A fill:#e4ffe4 

### **Ejemplo de código:** 

from google.adk.runners import Runner from google.adk.sessions import InMemorySessionService 

# Después de ejecutar el agente session.state["temp:current_step"] = "validation"      # ❌ Se pierde después del turno session.state["conversation_topic"] = "refunds"        # ⚠ Se pierde después de la sesión 

session.state["user:language"] = "Spanish"             # ✅ Persiste entre sesiones session.state["app:version"] = "2.0"                   # ✅ Global para todos los usuarios 

# **Conceptos básicos** 

## **1. Estado temporal: temp:** 

_Referencia:_ _<u>Prefijo temp: (documentación del ADK)</u>_ 

### **De la documentación del ADK:** 

Prefijo temp: (estado de invocación temporal): 

- **Alcance:** Específico de la **invocación** actual (todo el proceso desde que un agente recibe la entrada del usuario hasta que genera la salida final para esa entrada) 

- **Persistencia: Ninguna** (el estado se descarta una vez que se completa la invocación y no se transfiere a la siguiente) 

- **Caso de uso:** Almacenar cálculos, marcas o datos intermedios pasados entre llamadas a herramientas en una sola invocación 

### **¿Qué es una invocación?** 

Una invocación es **un turno completo** desde la entrada del usuario hasta la respuesta del agente. 

El usuario envía un mensaje 

```
    ↓
[COMIENZA LA INVOCACIÓN] ← Se crea el estado de temp:
    ↓
```

El agente procesa la solicitud 

```
    ↓
```

El agente devuelve la respuesta 

```
    ↓
[FINALIZA LA INVOCACIÓN] ← Se DESCARTA el estado de temp:
```

### **Uso:** 

from google.adk.agents import LlmAgent 

# Agente que usa el estado de temp: agent = LlmAgent( instruction="Procesa la solicitud y guarda el paso {temp:current_step?starting}", output_key="temp:processing_result"  # Se guarda en temp: namespace ) 

# Turno 1: # - state["temp:current_step"] = "validating" `# - Después de que termina el turno → Se DESCARTA temp:current_step` 

# Turno 2: `# - state.get("temp:current_step") → Ninguno (se descartó)` 

### **Cuándo se usa:** 

- ✅ Pasos de procesamiento intermedios 

   - ✅ Marcas temporales solo para el turno actual 

- 

- ✅ Datos que deben descartarse una vez finalizado el agente 

- ❌ NO se usa para datos necesarios entre turnos 

## **2. Estado de la sesión (sin prefijo)** 

_Referencia:_ _<u>Sin prefijo (documentación del ADK)</u>_ 

### **De la documentación del ADK:** 

Sin prefijo (estado de la sesión): 

- **Alcance:** Específico de la sesión _actual_ ( id ) 

- **Persistencia:** Solo si SessionService es persistente ( Database y VertexAI ) 

- **Casos de uso:** Monitorear el progreso en la tarea actual (p. ej., 'current_booking_step' ) o guardar marcas temporales para esta interacción (p. ej., 'needs_clarification' ) 

### **¿Qué es una sesión?** 

Una sesión es **una conversación** de principio a fin. 

El usuario inicia la conversación `↓ [COMIENZA LA SESIÓN] ← Se crea el estado de la sesión ↓` Turno 1, turno 2, turno 3… (el estado persiste) `↓` El usuario cierra o reinicia la conversación `↓ [FINALIZA LA SESIÓN] ← Se DESCARTA el estado de la sesión` 

### **Uso:** 

agent = LlmAgent( instruction="Tema actual: {conversation_topic?none}", output_key="conversation_topic"  # Sin prefijo = estado de la sesión ) # Sesión 1: # Turno 1: state["conversation_topic"] = "refunds" 

# Turno 2: state["conversation_topic"] sigue siendo "refunds" ✅ # Turno 3: state["conversation_topic"] sigue siendo "refunds" ✅ # [Termina la sesión] 

# Sesión 2 (nueva conversación): `# Turno 1: state.get("conversation_topic") → Ninguno (nueva sesión)` 

### **Cuándo se usa:** 

- ✅ Monitorear temas de conversación 

   - ✅ Contadores de turnos 

- 

- ✅ Artículos del carrito de compras (solo sesión actual) 

- ❌ NO se usa para datos necesarios en múltiples conversaciones 

## **3. Estado del usuario: user:** 

_Referencia:_ _<u>Prefijo user: (documentación del ADK)</u>_ 

### **De la documentación del ADK:** 

Prefijo user: (estado del usuario): 

- **Alcance:** Vinculado al user_id , compartido entre _todas_ las sesiones del usuario (dentro del mismo app_name ) 

- **Persistencia:** Con Database o VertexAI ( InMemory lo almacena, pero 

   - se pierde al reiniciar) 

- **Casos de uso:** Preferencias del usuario (p. ej., 'user:theme' ) o detalles del perfil (p. ej., 'user:name' ) 

### **Alcance:** 

El estado del usuario persiste **en todas las sesiones** para el mismo usuario. 

Sesión 1 del usuario: state["user:language"] = "Spanish" state["user:theme"] = "dark" [Finaliza la sesión] 

Sesión 2 del usuario (días después): state.get("user:language") → "Spanish" ✅ (persistió) state.get("user:theme") → "dark" ✅ (persistió) 

### **Uso:** 

agent = LlmAgent( instruction=""" Eres un asistente útil. 

Preferencias del usuario: 

- Idioma: {user:language?English} - Tema: {user:theme?light} Responde en {user:language?English}. """ ) 

# Primera conversación: # state["user:language"] = "Spanish"  # Se establece una vez 

# Conversaciones futuras: # El agente usa automáticamente el español (lee el estado de user:) 

### **Cuándo se usa:** 

- ✅ Preferencias de idioma 

   - ✅ Tema de visualización (oscuro o claro) 

- - ✅ Nivel de suscripción - ✅ Información del perfil del usuario - ❌ NO se usa para datos específicos de la conversación actual 

## **4. Estado de la app: app:** 

_Referencia:_ _<u>Prefijo app: (documentación del ADK)</u>_ 

### **De la documentación del ADK:** 

Prefijo app: (estado de la app): 

- **Alcance:** Vinculado a app_name , compartido entre _todos_ los usuarios y sesiones de la aplicación 

- **Persistencia:** Con Database o VertexAI ( InMemory lo almacena, pero se pierde al reiniciar) 

- **Casos de uso:** Parámetros de configuración globales (p. ej., 'app:api_endpoint' ) o plantillas compartidas 

### **Alcance:** 

El estado de la app es **global** : todos los usuarios ven los mismos valores. 

Sesión 1 del usuario A: state["app:api_url"] = "https://api.example.com" Sesión 1 del usuario B: state.get("app:api_url") → "https://api.example.com" ✅ (compartido) Sesión 5 del usuario C: state.get("app:api_url") → "https://api.example.com" ✅ (sigue siendo compartido) 

### **Uso:** 

agent = LlmAgent( instruction=""" Eres la versión {app:version?1.0}. 

Endpoint de API: {app:api_url?not set} Marcas de función: {app:features?basic} """ ) 

# Se establece una vez y se aplica a todos los usuarios: 

- # state["app:version"] = "2.0" 

# state["app:api_url"] = "https://api.example.com" 

### **Cuándo se usa:** 

- ✅ Endpoints de APIs 

   - ✅ Marcas de función 

- 

   - ✅ Configuración global 

- 

   - ✅ Versión de la aplicación 

- 

   - ❌ NO se usa para datos específicos del usuario o de la sesión 

- 

# 🧪 **Ejemplo práctico** 

## **Crea un agente que demuestre los cuatro espacios de nombres** 

**Qué crearás:** un agente que utiliza los cuatro espacios de nombres de estado para mostrar sus diferentes comportamientos de persistencia. 

## **Paso 1: Crea el proyecto** 

adk create namespace_demo cd namespace_demo 

## **Paso 2: Escribe el agente** 

Reemplaza el contenido de agent.py por lo siguiente: 

""" 

Demostración de espacios de nombres (muestra los cuatro espacios de nombres de estado) Demuestra los alcances de persistencia de temp:, session:, user: y app:. 

Referencia: https://google.github.io/adk-docs/sessions/state """ 

from google.adk.agents import LlmAgent 

# Crea un agente que use los cuatro espacios de nombres root_agent = LlmAgent( model='gemini-2.5-flash', name='namespace_demo', 

instruction=""" 

Eres un asistente de demostración que muestra los espacios de nombres de estado. === Estado de la app (global para todos los usuarios) === Nombre de la app: {app:name?Demostración de espacios de nombres} Versión de la app: {app:version?1.0} 

=== Estado del usuario (persiste entre sesiones) === Preferencia del usuario: {user:theme?not set} 

=== Estado de la sesión (persiste en esta conversación) === Tema de conversación: {topic?not set} 

=== Estado temporal (solo turno actual) === Paso actual: {temp:step?not set} 

Responde con un mensaje amigable mostrando estos valores de espacio de nombres. """, 

output_key="response" ) 

## **Paso 3: Prueba con Runner** 

Crea test_namespaces.py : 

""" 

Prueba los espacios de nombres de estado para ver las diferencias de persistencia. Se ejecuta con python test_namespaces.py """ 

from agent import root_agent from google.adk.runners import Runner from google.adk.sessions import InMemorySessionService from google.genai.types import Content, Part 

# Establece la configuración session_service = InMemorySessionService() session = session_service.create_session( app_name="namespace_demo_app", user_id="user1", session_id="session1" ) 

runner = Runner( agent=root_agent, app_name="namespace_demo_app", session_service=session_service ) 

# Establece los cuatro tipos de espacios de nombres print("=== Estableciendo el estado en todos los espacios de nombres ===") session.state["app:name"] = "Demostración de espacios de nombres" session.state["app:version"] = "2.0" session.state["user:theme"] = "dark" session.state["topic"] = "state management" session.state["temp:step"] = "initialization" 

print(f"Estado previo a la ejecución: {session.state}\n") 

# Ejecuta el agente print("=== Agente en ejecución (turno 1) ===") result = runner.run( user_id="user1", session_id="session1", new_message=Content(parts=[Part(text="Muéstrame los valores de los espacios de nombres")]) ) 

# Muestra la respuesta for event in result: if event.is_final_response(): print(f"Respuesta del agente:\n{event.content.parts[0].text}\n") 

# Verifica el estado después del turno print("=== Estado posterior al turno 1 ===") print(f"Estado completo: {session.state}") print(f"temp:step: {session.state.get('temp:step')}")  # Debe haberse DESCARTADO print(f"topic: {session.state.get('topic')}")  # Debe persistir print(f"user:theme: {session.state.get('user:theme')}")  # Debe persistir print(f"app:version: {session.state.get('app:version')}")  # Debe persistir print("\n=== Simulación del turno 2 (misma sesión) ===") result2 = runner.run( user_id="user1", session_id="session1", new_message=Content(parts=[Part(text="Vuelve a verificar el estado")]) ) 

for event in result2: if event.is_final_response(): print(f"Respuesta del agente:\n{event.content.parts[0].text}\n") 

print("=== Estado posterior al turno 2 ===") print(f"Estado completo: {session.state}") print(f"temp:step: {session.state.get('temp:step')}")  # Sigue DESCARTADO print(f"topic: {session.state.get('topic')}")  # Sigue disponible (estado de la 

sesión) 

print(f"user:theme: {session.state.get('user:theme')}")  # Sigue disponible (estado del usuario) 

# Simula una nueva sesión print("\n=== Simulando una NUEVA sesión (session2) ===") session2 = session_service.create_session( app_name="namespace_demo_app", user_id="user1",  # Mismo usuario session_id="session2"  # Sesión diferente ) print(f"Estado de la nueva sesión: {session2.state}") print(f"topic: {session2.state.get('topic')}")  # Debe haberse DESCARTADO (centrado en la sesión) print(f"user:theme: {session2.state.get('user:theme')}")  # Debe PERSISTIR (centrado en el usuario) print(f"app:version: {session2.state.get('app:version')}")  # Debe PERSISTIR (centrado en la app) 

Ejecútalo: 

python test_namespaces.py 

### **Resultado esperado:** 

=== Estableciendo el estado en todos los espacios de nombres === Estado previo a la ejecución: {'app:name': 'Demostración de espacios de nombres', 'app:version': '2.0', 'user:theme': 'dark', 'topic': 'state management', 'temp:step': 'initialization'} 

=== Agente en ejecución (turno 1) === Respuesta del agente: ¡Hola! Aquí están los valores del espacio de nombres: - App: Demostración de espacios de nombres (v2.0) - Tema del usuario: dark - Tema: state management - Paso actual: initialization === Estado posterior al turno 1 === Estado completo: {'app:name': 'Demostración de espacios de nombres', 'app:version': '2.0', 'user:theme': 'dark', 'topic': 'state management', 'response': '...'} `temp:step: None  ← Se DESCARTÓ después del turno topic: state management  ← Persistió (sesión) user:theme: dark  ← Persistió (usuario) app:version: 2.0 ← Persistió (app)` === Simulación del turno 2 (misma sesión) === Respuesta del agente: Hola de nuevo. Estos son los valores: - App: Demostración de espacios de nombres (v2.0) - Tema del usuario: dark - Tema: state management 

```
- Paso actual: not set  ← Se descartó temp:
```

=== Estado posterior al turno 2 === Estado completo: {igual que después del turno 1} `temp:step: None  ← Sigue DESCARTADO topic: state management  ← Sigue disponible user:theme: dark  ← Sigue disponible` === Simulando una NUEVA sesión (session2) === Estado de la nueva sesión: {'app:name': 'Demostración de espacios de nombres', 'app:version': '2.0', 'user:theme': 'dark'} `topic: None  ← Se DESCARTÓ (estaba centrado en la sesión) user:theme: dark  ← PERSISTIÓ entre sesiones app:version: 2.0 ← PERSISTIÓ globalmente` 

### **Qué debes tener en cuenta:** 

- 

   - ✅ temp:step se descartó después del turno 1 (era temporal). 

- ✅ topic persistió hasta el turno 2, pero se perdió en la nueva sesión (estaba centrado en la sesión). 

- ✅ user:theme persistió entre sesiones para el mismo usuario (estaba centrado en el usuario). 

- ✅ app:version persistió globalmente (estaba centrado en la app). 

# **Conclusiones principales** 

### **Cuatro espacios de nombres con diferentes duraciones:** 

state["temp:var"]      # ❌ Se descarta después del turno state["var"]           # ⚠ Se descarta cuando finaliza la sesión state["user:var"]      # ✅ Persiste entre sesiones (mismo usuario) state["app:var"]       # ✅ Persiste globalmente (todos los usuarios) 

### **Árbol de decisión:** 

¿Por cuánto tiempo deben conservarse los datos? 

- ├─ ¿Solo los necesitas AHORA MISMO (turno actual)? 

- │ └─ Usa el espacio de nombres temp: 

- │      Ejemplos: temp:processing_step, temp:validation_status 

- │ 

- ├─ ¿Los necesitas solo en esta CONVERSACIÓN? 

- │ └─ Usa el estado de la sesión (sin prefijo) 

- │      Ejemplos: conversation_topic, turn_count, shopping_cart │ 

- ├─ ¿Los necesitas en TODAS las conversaciones para este USUARIO? 

- │ └─ Usa el espacio de nombres user: 

- │      Ejemplos: user:language, user:theme, user:tier 

- │ 

- └─ ¿Los necesitas GLOBALMENTE para todos los usuarios? 

- └─ Usa el espacio de nombres app: 

Ejemplos: app:api_url, app:version, app:feature_flags 

### **Práctica recomendada: Utiliza el alcance más limitado necesario** 

- No conserves los datos más tiempo del necesario. 

- Usa temp: para los pasos intermedios. 

- Usa el estado de la sesión para el contexto de la conversación. 

- Usa user: para las preferencias. 

- Usa app: para la configuración global. 

### **Todos los espacios de nombres funcionan con plantillas:** 

instruction=""" App: {app:name?MyApp} Usuario: {user:language?English} Tema: {topic?none} Paso: {temp:step?start} """ 

**Próximos pasos:** Completaste la lección 4. A continuación, aprenderás sobre las herramientas en la **<u>lección 5, Agrega funciones con herramientas</u>** <u>, que incluye búsqueda de memoria y</u> otras funciones avanzadas. 

