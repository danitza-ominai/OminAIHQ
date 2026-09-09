# **Solución: Estado de la sesión** 

_Referencia:_ _<u>Estado de la sesión (documentación del ADK)</u>_ 

### **De la documentación del ADK:** 

Conceptualmente, session.state es una colección (un diccionario o un mapa) que contiene pares clave-valor. Está diseñada para la información que el agente necesita recuperar o monitorear para que la conversación actual sea eficaz: 

- **Personaliza la interacción:** Recuerda las preferencias del usuario mencionadas anteriormente (p. ej., 'user_preference_theme': 'dark' ). 

- **Monitorea el progreso de las tareas:** Controla los pasos de un proceso de varios turnos (p. ej., 'booking_step': 'confirm_payment' ). 

- **Acumula información:** Crea listas o resúmenes (p. ej., 'shopping_cart_items': ['book', 'pen'] ). 

- **Toma decisiones fundamentadas:** Almacena marcas o valores que influyen en la siguiente respuesta (p. ej., 'user_is_authenticated': True ). 

### **¿Qué es el estado de la sesión?** 

Es un **diccionario de Python** accesible a través del atributo session.state . Considéralo una colección de variables que almacena el agente y que puedes verificar con código: 

from google.adk.agents import LlmAgent from google.adk.runners import Runner from google.adk.sessions import InMemorySessionService 

# Crea un agente con output_key para guardar la respuesta agent = LlmAgent( model='gemini-2.5-flash', instruction=""Extrae el nombre del usuario y devuelve SOLO el nombre.", output_key="user_name"  # Guarda la respuesta en state["user_name"] ) 

# Configura la sesión y Runner session_service = InMemorySessionService() session = session_service.create_session(app_name="my_app", user_id="user1") runner = Runner(agent=agent, app_name="my_app", session_service=session_service) 

# Ejecuta el agente result = runner.run(user_id="user1", session_id=session.id, new_message="Me llamo Álex") 

# Accede al estado desde fuera del agente print(session.state)  # {'user_name': 'Álex'} print(session.state.get("user_name"))  # 'Álex' 

# Ahora tu código puede tomar decisiones: if session.state.get("user_name"): print(" ✅ El usuario indicó su nombre.") 

### **Qué permite hacer el estado:** 

- ✅ **Acceder de forma programática** : A través del código, puedes leer valores exactos con session.state.get("key") . 

- ✅ **Guardar datos automáticamente** : Usa output_key para guardar las respuestas del agente sin código manual. 

- ✅ **Tomar decisiones** : Verifica los valores de estado para tomar decisiones programáticas. 

- ✅ **Conservar datos** : Los valores permanecen accesibles en todos los turnos de conversación. 

# **Conceptos básicos** 

## **1. Estado vs. historial de conversaciones** 

**Ambos** están disponibles para tus agentes, pero cumplen diferentes propósitos: 

|**Función**|**Historial de conversaciones**|**Estado de la sesión**|
|---|---|---|
|**En qué consiste**|Mensajes de texto (usuario y<br>agente)|Diccionario de pares clave-valor|
|**¿Puede leerlo el LLM?**|✅Sí (automáticamente)|✅Sí (mediante la plantilla<br>{var}, parte 2)|
|**¿Se puede comprobar**<br>**mediante código?**|❌No|✅Sí<br>(session.state.get("key")<br>)|
|**Uso**|Contexto para el LLM|Valores exactos para tu código|
|**Acceso**|Automático (enviado al modelo)|Programático (session.state)|



### **Comparación visual:** 

graph TB 

subgraph "Historial de conversaciones" 

CH1[Mensajes de texto<br/>entre usuario y agente] CH2[Legible para el LLM ✅ ] 

CH3[INACCESIBLE mediante código ❌ ] end 

subgraph "Estado de la sesión" 

SS1[Diccionario<br/>de pares clave-valor] 

SS2[Legible para el LLM ✅ ] SS3[ACCESIBLE mediante código ✅ ] end style CH2 fill:#e1f5ff style CH3 fill:#ffeeee style SS2 fill:#e1f5ff style SS3 fill:#eeffee 

### **Cuándo utilizar el estado:** 

- ✅ Cuando tu código necesita verificar valores exactos (if state.get("name"): ) 

- ✅ Cuando se toman decisiones de enrutamiento de forma programática 

   - ✅ Cuando se monitorea el progreso de la conversación o la información del usuario 

- 

   - ❌ NO lo utilices solo para proporcionarle contexto al LLM (el historial de conversaciones ya se encarga de ello) 

- 

## **2. Accede al estado con session.state** 

_Referencia:_ _<u>Cómo acceder al estado (documentación del ADK)</u>_ 

Después de ejecutar tu agente, puedes acceder al estado a través del diccionario session.state : 

from google.adk.runners import Runner from google.adk.sessions import InMemorySessionService from google.genai.types import Content, Part # Crea una sesión session_service = InMemorySessionService() session = session_service.create_session(app_name="app", user_id="user1") # Ejecuta el agente runner = Runner(agent=my_agent, app_name="app", session_service=session_service) result = runner.run( user_id="user1", session_id=session.id, new_message=Content(parts=[Part(text="Hola")]) ) # Accede al estado DESPUÉS de que se ejecute el agente print(session.state)  # Diccionario de estado completo name = session.state.get("user_name", "Invitado")  # Lectura segura con valor predeterminado count = session.state.get("count", 0)  # Devuelve 0 si la clave no existe 

### **Puntos clave:** 

- Se accede al estado como un diccionario: session.state . 

- Utiliza .get(key, default) para leer de forma segura (devuelve el valor 

predeterminado si la clave no existe). 

- El estado persiste entre todos los turnos de la misma sesión. 

- Puedes verificar valores de estado mediante código para tomar decisiones programáticas. 

## **3. Guarda respuestas con output_key** 

_Referencia:_ _<u>output_key (documentación del ADK)</u>_ 

### **De la documentación del ADK:** 

output_key (opcional): Proporciona una clave de cadena. Si se establece, el contenido de texto de la respuesta _definitiva_ del agente se guardará automáticamente en el diccionario de estado de la sesión con esta clave. Resulta útil para pasar resultados entre agentes o pasos en un flujo de trabajo. 

La forma más sencilla de guardar la respuesta de un agente en el estado es usando output_key : 

from google.adk.agents import LlmAgent 

agent = LlmAgent( model='gemini-2.5-flash', instruction="Extrae el tema principal y devuelve SOLO el tema.", output_key="topic"  # Guarda automáticamente la respuesta en state["topic"] ) 

- # Después de que se ejecuta el agente, state["topic"] contiene el texto de respuesta # No se necesita código manual 

### **Cómo funciona:** 

1. El agente genera una respuesta (p. ej., "computación cuántica"). 

2. El framework guarda la respuesta automáticamente en state["topic"] = 

   - "computación cuántica" . 

3. Puedes acceder a él con session.state.get("topic") . 

### **Cuándo se usa:** 

- ✅ Cuando quieres guardar la respuesta del agente para usarla más adelante 

   - ✅ Cuando necesitas acceso programático a lo que dijo el agente 

- 

   - ✅ Cuando creas aplicaciones que necesitan monitorear información extraída 

- 

   - ❌ NO lo uses para respuestas que no necesites consultar más adelante 

- 

# 🧪 **Ejemplo práctico** 

## **Crea un agente de extracción de nombres** 

**Qué crearás:** Un agente sencillo que extrae el nombre de un usuario y lo guarda en el estado, lo que demuestra cómo el estado permite el acceso programático 

## **Paso 1: Crea el proyecto** 

adk create name_extractor cd name_extractor 

## **Paso 2: Escribe el agente** 

Reemplaza el contenido de agent.py por lo siguiente: 

""" Extractor de nombres (demuestra los conceptos básicos del estado de la sesión) Muestra cómo usar output_key para guardar datos y acceder a ellos a través de session.state. 

Referencia: https://google.github.io/adk-docs/sessions/state """ 

from google.adk.agents import LlmAgent 

# Agente único que extrae y guarda el nombre root_agent = LlmAgent( model='gemini-2.5-flash', name='name_extractor', 

instruction="Extrae el nombre de la persona del mensaje. Devuelve SOLO el nombre, nada más.", output_key="user_name"  # Guarda la respuesta en state["user_name"] ) 

### **Explicación del código:** 

### **Líneas 10-16: Agente extractor de nombres** 

- Utiliza output_key="user_name" para guardar automáticamente la respuesta. 

- - Después de que se ejecuta este agente, state["user_name"] contiene el nombre extraído. 

- No se necesita código para administrar el estado manualmente. 

## **Paso 3: Prueba con Runner** 

En lugar de adk web , usemos Runner directamente para ver el acceso al estado: 

Crea un archivo llamado test_state.py : 

""" 

Secuencia de comandos de prueba para ver el acceso al estado directamente. Se ejecuta con python test_state.py """ 

from agent import root_agent from google.adk.runners import Runner from google.adk.sessions import InMemorySessionService from google.genai.types import Content, Part 

# Configura la sesión y Runner session_service = InMemorySessionService() session = session_service.create_session( app_name="name_extractor_app", user_id="test_user", session_id="test_session" ) runner = Runner( agent=root_agent, app_name="name_extractor_app", session_service=session_service ) # Prueba: Extrae el nombre user_message = Content(parts=[Part(text="Hola, me llamo Álex Jiménez")]) print("=== Agente en ejecución ===") result = runner.run( user_id="test_user", session_id="test_session", new_message=user_message ) # Muestra la respuesta definitiva for event in result: if event.is_final_response(): print(f"\nRespuesta del agente: {event.content.parts[0].text}") # Accede al estado de manera programática print(f"\n=== Estado posterior a la ejecución ===") print(f"Estado completo: {session.state}") print(f"Nombre extraído: {session.state.get('user_name')}") # Ahora puedes tomar decisiones basadas en el estado a través del código if session.state.get("user_name"): print(" ✅ Se extrajo y almacenó correctamente el nombre") else: print(" ❌ No se pudo extraer el nombre") # Prueba de acceso en turnos posteriores 

print("\n=== Simulación del turno dos ===") result2 = runner.run( user_id="test_user", session_id="test_session", new_message=Content(parts=[Part(text="¿Cómo me llamo?")]) ) 

for event in result2: if event.is_final_response(): print(f"Respuesta del agente: {event.content.parts[0].text}") print(f"\nEl estado aún contiene {session.state.get('user_name')}") print(" ✅ El estado persiste entre turnos") 

### Ejecútalo: 

python test_state.py 

### **Resultado esperado:** 

=== Agente en ejecución === 

Respuesta del agente: Álex Jiménez 

=== Estado posterior a la ejecución === Estado completo: {'user_name': 'Álex Jiménez'} Nombre extraído: Álex Jiménez ✅ Se extrajo y almacenó correctamente el nombre 

=== Simulación del turno dos === Respuesta del agente: Te llamas Álex Jiménez 

El estado aún contiene Álex Jiménez ✅ El estado persiste entre turnos 

### **Qué debes tener en cuenta:** 

- ✅ output_key="user_name" guardó automáticamente "Álex Jiménez" en el estado. 

- - ✅ A través del código, puedes acceder a session.state.get("user_name") de manera programática. 

- 

   - ✅ Puedes tomar decisiones: if session.state.get("user_name"):. 

- ✅ El estado persiste entre varios turnos en la misma sesión. 

# **Conclusiones principales** 

### **Conceptos básicos del estado de la sesión:** 

- El **estado de la sesión** es un diccionario en el que los agentes almacenan datos a los que puedes acceder mediante código de manera programática. 

- El **historial de conversaciones** le proporciona contexto al LLM, pero no puedes 

verificarlo de manera programática mediante código. 

- Ambos están disponibles y se complementan entre sí (historial para el contexto del LLM, estado para el control programático). 

### **Cómo utilizar el estado:** 

- Accede al estado con session.state después de ejecutar agentes con Runner . 

- Utiliza .get(key, default) para leer valores de estado de forma segura. 

- Utiliza output_key="key" para guardar automáticamente las respuestas del agente en el estado. 

- El estado persiste entre todos los turnos de la misma sesión. 

### **Cuándo utilizar el estado:** 

- ✅ Cuando necesitas verificar valores exactos de manera programática mediante código 

- ✅ Cuando tomas decisiones de enrutamiento basadas en datos de conversaciones 

   - ✅ Cuando se monitorea el progreso de la conversación o la información del usuario 

- 

   - ✅ Cuando almacenas información extraída para la lógica de la aplicación 

- 

### **Patrón común:** 

# 1. El agente guarda el estado con output_key agent = LlmAgent(output_key="result") 

# 2. Ejecuta el agente runner.run(...) 

# 3. Accede al estado de manera programática if session.state.get("result"): 

- # Toma decisiones basadas en el estado pass 

**Siguiente parte:** Aprenderás a usar plantillas {var} para insertar valores de estado en instrucciones, lo que permite que los agentes tengan un comportamiento dinámico. 

