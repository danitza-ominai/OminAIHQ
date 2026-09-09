# **Introducción** 

## **De las herramientas individuales a los sistemas coordinados** 

**Tu recorrido:** 

- **Parte 1:** Comprendiste las herramientas a nivel fundamental y creaste el primer agente habilitado para herramientas. 

- **Parte 2:** Utilizaste las herramientas integradas de Búsqueda de Google y ejecución de código. 

- **Parte 3:** Creaste herramientas de funciones personalizadas adaptadas a tus necesidades. 

- **Parte 4:** Combinas herramientas de forma eficaz para situaciones reales. 

**El cambio:** Las herramientas por sí solas no son suficientes; se necesitan instrucciones estratégicas para guiar a los agentes hacia un uso eficaz. 

# **El problema** 

## **Herramientas sin guía** 

Tienes herramientas potentes, pero sin un diseño de instrucciones adecuado, los agentes tienen dificultades, como se ve a continuación: 

from google.adk.agents import LlmAgent # Tienes varias herramientas... def check_order_status(order_id: str) -> dict: """Consulta el estado de un pedido.""" # Implementación pass def process_refund(order_id: str, amount: float) -> dict: """Procesa un reembolso para un pedido.""" # Implementación pass def lookup_customer(email: str) -> dict: """Busca información del cliente.""" # Implementación pass # Pero con instrucciones poco claras... agent = LlmAgent( model='gemini-2.5-flash', instruction="Eres un agente del servicio de atención al cliente.",  # ¡Demasiado ambiguo! tools=[check_order_status, process_refund, lookup_customer] 

) 

### **Qué sale mal:** 

- ❌ **Selección de la herramienta incorrecta** : El agente usa process_refund antes de verificar si el pedido existe. 

- ❌ **Manejo de errores deficiente** : El agente no sabe qué hacer cuando la herramienta devuelve un error. 

- ❌ **Pedido incorrecto** : El agente llama a las herramientas en una secuencia ilógica. 

   - ❌ **Resultados ignorados** : El agente no utiliza correctamente el resultado de la 

- herramienta en la respuesta. 

- ❌ **Sin ruta de derivación** : El agente no puede manejar situaciones que exceden las capacidades de la herramienta. 

**El problema raíz:** Las herramientas necesitan instrucciones estratégicas que guíen cuándo, cómo y en qué orden usarlas. 

