# **Introducción** 

Aprendiste a crear agentes con instrucciones sofisticadas. Tus agentes pueden responder de forma inteligente utilizando el historial de conversaciones: el LLM recibe automáticamente los mensajes anteriores y comprende el contexto. Pero ¿y si necesitas, **mediante código** , verificar valores específicos o tomar decisiones programáticas basadas en datos de conversación? 

Por ejemplo: 

- ¿Cómo compruebas en el código si el usuario proporcionó su nombre? 

- ¿Cómo almacenas un valor extraído para usarlo más tarde en tu aplicación? 

- ¿Cómo tomas decisiones de enrutamiento basándose en datos exactos (no en la interpretación del LLM)? 

**Limitación:** El historial de conversaciones se envía al LLM, pero no puedes acceder a él de manera programática. No puedes escribir if 

conversation_history.contains("Álex"): porque el historial de conversaciones no es una estructura de datos que se pueda consultar a través del código; solo es un conjunto de mensajes de texto enviados al modelo. 

Esta parte presenta el **estado de la sesión** , un diccionario que tu código puede leer y escribir de manera programática. 

# **Problema** 

## **El historial de conversaciones no basta por sí solo para ejercer control programático** 

Veamos qué sucede cuando intentas crear agentes que necesitan tomar decisiones basadas en datos de la conversación: 

from google.adk.agents import LlmAgent 

# El agente que debe extraer y recordar el nombre del usuario agent = LlmAgent( model='gemini-2.5-flash', instruction="Extrae el nombre del usuario y recuérdalo para futuras preguntas." ) 

# Turno 1 # Usuario: "Me llamo Álex" # Agente: "Mucho gusto, Álex" # Turno 2 # Usuario: "¿Cómo me llamo?" # Agente: "Te llamas Álex" ✅ (el LLM lo recuerda del historial) 

# Pero en tu código: 

# ¿Cómo compruebas si se proporcionó el nombre? ❌ # ¿Cómo accedes al nombre exacto "Álex"? ❌ # ¿Cómo lo utilizas en la lógica de la aplicación? ❌ 

**Problema raíz:** Si bien el LLM puede leer el historial de conversaciones y responder adecuadamente, no puedes verificar mediante código los valores de manera programática ni tomar decisiones de enrutamiento. Necesitas datos estructurados y accesibles de manera programática. 

