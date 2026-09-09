# **Introducción** 

## **Avance** 

**Resumen de los módulos 1 y 2:** Aprendiste lo siguiente: 

- El estado de la sesión es un diccionario accesible a través de session.state . 

- output_key guarda automáticamente las respuestas del agente en el estado. 

- La plantilla {var} inserta valores de estado en las instrucciones. 

### **Ahora puedes hacer lo siguiente:** 

from google.adk.agents import LlmAgent 

# Guarda datos con output_key agent = LlmAgent( instruction="Extrae el tema principal", output_key="topic" ) 

# Utiliza plantillas para insertar valores de estado agent = LlmAgent( instruction="Proporciona una descripción general sobre {topic}" ) 

### **Siguiente pregunta:** ¿Cuánto tiempo persiste el estado? 

# Todos estos valores se escriben en el estado, pero ¿cuánto duran? session.state["processing_step"] = "validation" session.state["user_language"] = "Spanish" session.state["api_endpoint"] = "https://api.example.com" 

**Respuesta:** Los espacios de nombres de estado controlan el alcance de la persistencia. 

# **Problema** 

## **No todos los estados deben persistir de la misma manera** 

Considera los diferentes tipos de datos que necesita un agente: 

# Estos datos tienen requisitos de vida útil MUY diferentes: state["current_step"] = "validating"      # Solo se necesita en este momento state["conversation_topic"] = "refunds"   # Solo se necesita en esta conversación state["user_theme"] = "dark"              # Se necesita en todas las conversaciones state["api_url"] = "https://api.com"      # Global para todos los usuarios 

### **Problemas sin espacios de nombres:** 

❌ **Los datos temporales persisten para siempre** → Se producen fugas de memoria con el tiempo ❌ **Las preferencias del usuario se pierden cuando finaliza la sesión** → El usuario debe reconfigurarlas cada vez ❌ **La configuración global se almacena por sesión** → Duplicación innecesaria ❌ **Los datos de conversación se filtran entre sesiones** → Problemas de privacidad y contexto 

**Requisito:** Necesitas diferentes alcances de persistencia para distintos tipos de datos. 

