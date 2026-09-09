# **Introducción** 

## **De las capacidades integradas a las capacidades personalizadas** 

**Tu recorrido:** 

- **Parte 1:** Comprendiste las herramientas a nivel fundamental y creaste tu primer agente habilitado para herramientas. 

- **Parte 2:** Utilizaste las herramientas integradas listas para producción (Búsqueda de Google, ejecución de código). 

- **Parte 3:** Creas herramientas personalizadas adaptadas a tus necesidades específicas. 

**El cambio:** En lugar de importar herramientas listas para usar, escribes funciones de Python que el ADK convierte automáticamente en herramientas. 

# **El problema** 

## **Herramientas genéricas frente a necesidades empresariales específicas** 

Las herramientas integradas son excelentes para tareas comunes: 

- # Las herramientas integradas abordan necesidades universales from google.adk.tools import google_search 

agent = LlmAgent( 

model='gemini-2.5-flash', tools=[google_search]  # Funciona para cualquier búsqueda web ) 

### **Pero ¿qué pasa con TU lógica empresarial específica?** 

- # Tu negocio necesita herramientas únicas para tareas como las siguientes: 

- # - Calcular los costos de envío para TUS productos 

- # - Consultar el inventario en TU base de datos 

- # - Procesar los reembolsos en TU sistema 

- # - Validar los puntos de lealtad de los clientes en TU programa 

- # - Reservar citas en TU calendario 

- # - Consultar el estado de pedido en TU plataforma de comercio electrónico 

- # ¡Las herramientas integradas no pueden conocer tu negocio! 

### **Problemas con las soluciones genéricas:** 

- ❌ **Sin contexto comercial** : las herramientas integradas no conocen tus productos, precios ni políticas. 

- ❌ **No pueden acceder a tus sistemas** : tus bases de datos propias, APIs, servicios 

internos. 

- ❌ **Una solución única** : las herramientas genéricas no se adaptan a tus flujos de trabajo específicos. 

- ❌ **Personalización limitada** : no se puede modificar el comportamiento de la herramienta integrada para adaptarla a tus necesidades. 

**El problema raíz:** Cada empresa tiene una lógica, datos y sistemas únicos que requieren una integración personalizada. 

