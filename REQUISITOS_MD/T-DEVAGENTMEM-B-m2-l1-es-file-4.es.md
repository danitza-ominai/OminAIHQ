# **Solución: Plantillas de estado con {var}** 

_Referencia:_ _<u>Plantillas de estado (documentación del ADK)</u>_ 

### **De la documentación del ADK:** 

"Para insertar un valor de estado de sesión, encierra la clave de la variable de estado deseada entre llaves: {key} . El framework reemplazará automáticamente este marcador de posición por el valor correspondiente de session.state antes de pasar la instrucción al LLM". 

### **De la documentación del ADK:** 

"La sintaxis {var} es un marcador de posición. Antes de enviar la instrucción al LLM, el framework del ADK reemplaza automáticamente (ejemplo: {topic} ) por el valor de session.state['topic'] . Esta es la forma recomendada de proporcionar contexto a un agente, utilizando plantillas en las instrucciones". 

### **Cómo funciona:** 

# El estado contiene información del usuario session.state["user_name"] = "Álex" 

# El agente utiliza plantillas agent = LlmAgent( instruction="Hola, {user_name}. ¿En qué puedo ayudarte hoy?" ) 

# Antes de que el LLM vea la instrucción, el ADK realiza las siguientes tareas automáticamente: 

- # 1. Busca session.state["user_name"]. 

- # 2. Reemplaza {user_name} por "Álex". 

# 3. Envía instrucción resuelta al LLM: "Hola, Álex. ¿En qué puedo ayudarte hoy?". 

### **Ejemplo completo:** 

from google.adk.agents import LlmAgent from google.adk.runners import Runner from google.adk.sessions import InMemorySessionService 

# Establece la configuración session_service = InMemorySessionService() session = session_service.create_session(app_name="app", user_id="user1") 

# Establece el estado manualmente (simulando interacción previa o datos externos) session.state["user_name"] = "Álex" session.state["user_language"] = "Spanish" 

# Agente con plantillas agent = LlmAgent( 

model='gemini-2.5-flash', instruction="Hola, {user_name}. Responde en {user_language}." ) 

# Cuando el agente se ejecuta: 

# El LLM recibe: "Hola, Álex. Responde en español." 

# **Conceptos básicos** 

## **1. Sintaxis de plantillas de estado: {key}** 

_Referencia:_ _<u>Uso de plantillas {key} (documentación del ADK)</u>_ 

### **De la documentación del ADK:** 

"Para insertar un valor de estado de sesión, encierra la clave de la variable de estado deseada entre llaves: {key} . El framework reemplazará automáticamente este marcador de posición por el valor correspondiente de session.state antes de pasar la instrucción al LLM". 

### **Sintaxis básica:** 

instruction="Procesa {variable_name}" 

# El ADK realiza las siguientes tareas automáticamente: 

- # 1. Analiza instrucciones en busca de patrones {key}. # 2. Busca session.state["variable_name"]. 

- # 3. Reemplaza {variable_name} por el valor real. 

- # 4. Envía la instrucción resuelta al LLM. 

### **Ejemplo:** 

# El estado contiene: session.state["topic"] = "computación cuántica" 

agent = LlmAgent( instruction="Proporciona una descripción general sobre {topic}" ) 

# Antes de llamar al LLM, la instrucción se convierte en lo siguiente: 

# "Proporciona una descripción general sobre computación cuántica" 

### **Puntos clave:** 

- La creación de plantillas se realiza **antes de cada invocación del agente** . 

- Las variables se reemplazan por sus valores de estado **actual** . 

- Funciona con cualquier clave de estado. 

- Distingue mayúsculas de minúsculas: {name} ≠ {Name} . 

## **2. Plantilla opcional: {key?}** 

_Referencia:_ _<u>Consideraciones importantes (documentación del ADK)</u>_ 

### **De la documentación del ADK:** 

"Asegúrate de que la clave a la que haces referencia en la cadena de instrucciones exista en session.state. De lo contrario, el agente arrojará un error. Para utilizar una clave que puede o no estar presente, puedes incluir un signo de interrogación (?) después de la clave (p. ej., {topic?})”. 

### **Por qué la necesitas:** 

# ❌ Sin sintaxis opcional: arroja un error si falta la clave instruction="Saluda a {user_name}" `# Si state["user_name"] no existe → Se arroja un error` 

# ✅ Con sintaxis opcional: no hay error si falta la clave instruction="Saluda a {user_name?}" `# Si state["user_name"] no existe → Se resuelve como "Saluda a "` 

### **Variaciones de sintaxis:** 

# Opcional básico: vacío si falta "{var?}" 

# Resultado si falta var: "" (cadena vacía) 

# Opcional con texto predeterminado "{var?texto predeterminado}" # Resultado si var="valor": "valor" 

# Resultado si falta var: "texto predeterminado" 

# Bloque de texto condicional "{premium_user?Tienes acceso premium.}" # Resultado si premium_user existe y es verdadero: "Tienes acceso premium". 

# Resultado si premium_user falta o es falso: "" (cadena vacía) 

### **Ejemplo práctico:** 

agent = LlmAgent( instruction=""" Eres un asistente útil. Preferencias del usuario: - Nombre: {user_name?Invitado} - Idioma: {user_language?English} {premium_user? ✨ Se habilitaron las funciones premium.} Responde a la pregunta del usuario. """ 

) 

# Si user_name no está en el estado, el valor predeterminado es "Invitado" 

# Si premium_user no está en el estado, esa línea desaparece por completo 

## **3. Cómo funcionan las plantillas con estado** 

### **Patrón:** 

graph LR 

A[El estado contiene<br/>user_name='Álex'] -->|Uso de plantillas| B[Instrucción:<br/>"Hola, user_name"] B -->|El ADK resuelve| C[El LLM recibe<br/>"Hola, Álex"] 

style A fill:#e1f5ff style C fill:#eeffee 

### **Flujo de ejecución:** 

# 1. El estado se establece (desde el turno anterior o manualmente) session.state["user_name"] = "Álex" session.state["topic"] = "computación cuántica" 

# 2. El agente tiene instrucciones en plantillas agent = LlmAgent( instruction="Hola, {user_name}. Hablemos sobre {topic}." ) 

# 3. Cuando se ejecuta el agente, el ADK resuelve las plantillas: 

- # Antes: "Hola, {user_name}. Hablemos sobre {topic}." # Después: "Hola, Álex. "Hablemos sobre computación cuántica." 

- # 4. El LLM recibe la instrucción resuelta 

# 5. El LLM genera una respuesta basada en la instrucción resuelta 

**Consideración clave:** Las plantillas hacen que las instrucciones sean **dinámicas** según el estado, sin cambiar el código del agente. 

# 🧪 **Ejemplo práctico** 

## **Crea un agente de bienvenida personalizado** 

**Lo que crearás:** Un agente que utiliza plantillas de estado para crear respuestas personalizadas basadas en la información del usuario almacenada en el estado. 

## **Paso 1: Crea el proyecto** 

adk create personalized_greeter cd personalized_greeter 

## **Paso 2: Escribe el agente** 

Reemplaza el contenido de agent.py por lo siguiente: 

""" 

Agente de bienvenida personalizado (demuestra las plantillas de estado) Muestra cómo la plantilla {var} inserta valores de estado en las instrucciones. 

Referencia: https://google.github.io/adk-docs/sessions/state """ 

from google.adk.agents import LlmAgent 

# Agente con plantillas de estado root_agent = LlmAgent( model='gemini-2.5-flash', name='personalized_greeter', 

instruction=""" 

Eres un asistente amigable. 

Información del usuario: 

- Nombre: {user_name?usuario} 

- Idioma preferido: {user_language?English} 

- Membresía: {membership_tier?free} 

{membership_tier?Tu nivel de membresía es: {membership_tier}} 

Saluda amablemente al usuario y ofrécele ayuda. Responde en {user_language?English}. """ 

) 

### **Explicación del código:** 

### **Líneas 13–24: Instrucciones basadas en plantillas** 

- {user_name?usuario} : Usa "usuario" si user_name no está en el estado. 

- {user_language?English} : El valor predeterminado es "English" si no se configura. 

- {membership_tier?free} : Muestra "free" si no se especifica. 

- La línea condicional solo aparece si existe membership_tier. 

- La instrucción se adapta según el estado disponible. 

## **Paso 3: Prueba con Runner** 

Crea test_templating.py : 

""" Prueba crear plantillas de estado con diferentes valores. Ejecútalo con: python test_templating.py """ 

from agent import root_agent from google.adk.runners import Runner from google.adk.sessions import InMemorySessionService from google.genai.types import Content, Part # Establece la configuración session_service = InMemorySessionService() session = session_service.create_session( app_name="greeter_app", user_id="user1", session_id="session1" ) runner = Runner( agent=root_agent, app_name="greeter_app", session_service=session_service ) # Prueba 1: No hay estado establecido (todos los valores predeterminados) print("=== Prueba 1: Sin estado (todos los valores predeterminados) ===") result1 = runner.run( user_id="user1", session_id="session1", new_message=Content(parts=[Part(text="Hola")]) ) for event in result1: if event.is_final_response(): print(f"Agente: {event.content.parts[0].text}\n") # Prueba 2: Establece solo el nombre de usuario print("=== Prueba 2: Con nombre de usuario ===") session.state["user_name"] = "Álex" result2 = runner.run( user_id="user1", session_id="session1", new_message=Content(parts=[Part(text="Hola de nuevo")]) ) for event in result2: if event.is_final_response(): print(f"Agente: {event.content.parts[0].text}\n") 

# Prueba 3: Establece todos los valores de estado print("=== Prueba 3: Con todos los valores de estado ===") session.state["user_name"] = "Álex" session.state["user_language"] = "Spanish" session.state["membership_tier"] = "premium" 

result3 = runner.run( user_id="user1", session_id="session1", new_message=Content(parts=[Part(text="Hola de nuevo")]) ) for event in result3: if event.is_final_response(): print(f"Agente: {event.content.parts[0].text}\n") print("=== Estado actual ===") print(session.state) 

### Ejecútalo: 

python test_templating.py 

### **Resultado esperado:** 

=== Prueba 1: Sin estado (todos los valores predeterminados) === Agente: Hola, usuario. Estoy aquí para ayudarte con todo lo que necesites. ¿En qué puedo ayudarte? 

=== Prueba 2: Con nombre de usuario === Agente: Hola, Álex. Qué bueno volver a verte. ¿En qué puedo ayudarte? === Prueba 3: Con todos los valores de estado === Agente: Hola, Álex. Tu nivel de membresía es premium. ¿En qué puedo ayudarte hoy? 

=== Estado actual === {'user_name': 'Álex', 'user_language': 'Spanish', 'membership_tier': 'premium'} 

### **Qué debes tener en cuenta:** 

- ✅ Prueba 1: Se utilizan todos los valores predeterminados ({user_name?usuario} → "usuario"). 

- ✅ Prueba 2: Estado parcial ({user_name} → "Álex", otros predeterminados). 

- ✅ Prueba 3: Estado completo, la respuesta está en español y se muestra la membresía. 

- ✅ La instrucción se adapta dinámicamente según el estado disponible. 

# **Conclusiones principales** 

### **Las plantillas de estado permiten instrucciones dinámicas:** 

- Utiliza la sintaxis {var} para insertar valores de estado en las instrucciones. 

- El ADK resuelve las plantillas **antes** de enviarlas al LLM. 

- Funciona con cualquier clave de estado. 

- Hace que los agentes sean conscientes del contexto sin cambios en el código. 

### **La sintaxis opcional evita errores:** 

- {var} → Arroja un error si falta (modo estricto). 

- {var?} → Queda vacía si falta (modo opcional). 

- {var?predeterminado} → Utiliza el texto "predeterminado" si falta. 

- {var?Texto condicional} → Muestra texto solo si existe var. 

### **Patrón común:** 

# 1. Se establece el estado (a partir del turno anterior o datos externos) session.state["user_name"] = "Álex" 

# 2. El agente utiliza plantillas agent = LlmAgent( instruction="Hola {user_name?usuario}" ) 

# 3. La instrucción se resuelve automáticamente 

- # El LLM recibe: "Hola, Álex" 

### **Cuándo utilizar plantillas:** 

- ✅ Cuando las instrucciones deben adaptarse según el estado 

   - ✅ Cuando se personaliza el comportamiento del agente 

- 

   - ✅ Cuando se insertan valores exactos desde tu aplicación 

- 

   - ✅ Cuando se crean instrucciones teniendo en cuenta el contexto 

- 

**Siguiente parte:** Aprenderás sobre los espacios de nombres de estado ( temp: , user: y app: ), que controlan por cuánto tiempo persisten los valores de estado. 

