# **Introducción** 

## **Avance** 

**Resumen de la parte:** Aprendiste lo siguiente: 

- El estado de la sesión es un diccionario accesible a través de session.state . 

- output_key guarda automáticamente las respuestas del agente en el estado. 

- Puedes acceder al estado desde fuera del agente usando session.state.get("key") . 

### **Ahora puedes hacer lo siguiente:** 

from google.adk.agents import LlmAgent 

# El agente que guarda su respuesta agent = LlmAgent( instruction="Extrae el nombre del usuario", output_key="user_name" ) 

# Después de la ejecución, session.state["user_name"] contiene el nombre extraído 

**Próximo paso:** Aprende a usar esos valores guardados dentro de las instrucciones del agente, lo que hace que tus agentes sean dinámicos y contextuales. 

# **Problema** 

## **¿Cómo utilizan los agentes los valores de estado en sus instrucciones?** 

Sabes cómo guardar datos en el estado, pero ¿cómo le dices al agente que los use? 

from google.adk.agents import LlmAgent 

- # Supón que el estado ya tiene información del usuario 

- # session.state["user_name"] = "Álex" 

- # session.state["user_language"] = "Spanish" 

# ¿Cómo le dices al agente que USE estos valores? agent = LlmAgent( instruction="Respóndele al usuario"  # ❌ Demasiado genérico # ¿Cómo decimos: "Respóndele a Alex en español"? ) 

**Desafío:** Quieres que las instrucciones se adapten en función de los valores del estado. Quieres que el agente utilice automáticamente “Alex” y “Español” sin usar el método 

hard-coded. 

**Requisito:** Necesitas una forma de insertar state["user_name"] y state["user_language"] en la instrucción automáticamente. 

