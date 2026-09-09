# **Introducción** 

## **De los conceptos básicos sobre los agentes a las herramientas** 

Aprendiste la ecuación principal del agente: 

Agente = modelo + herramientas + organización 

En este curso, se completa la ecuación principal del agente, ya que se te enseña a equiparlos con herramientas: las capacidades que transforman a los agentes de respondedores inteligentes a asistentes capaces de realizar acciones. 

# **El problema** 

## **Agentes limitados por los datos de entrenamiento** 

Revisemos nuevamente un agente del curso 3: 

# Del curso 3: agente sofisticado sin herramientas from google.adk.agents import LlmAgent 

agent = LlmAgent( model='gemini-2.5-flash', instruction=""" 

Eres un asistente servicial que proporciona a los usuarios información actualizada. 

Sé siempre preciso y mantente actualizado en tus respuestas. """, 

) 

### **Ahora ten en cuenta estas solicitudes del usuario:** 

Usuario: “¿Cómo está el clima en Tokio ahora mismo?” Usuario: “Calcula el costo de envío de un paquete de 5 kg a Canadá” 

Usuario: “Busca el pedido #ORD12345 en nuestro sistema” 

### **Las limitaciones fundamentales:** 

- ❌ **El LLM solo conoce los datos de entrenamiento** : la información corresponde al momento del entrenamiento y no se puede acceder a los datos en tiempo real. 

- ❌ **No puede realizar cálculos** : si bien los LLM pueden razonar sobre matemáticas, no pueden ejecutar cálculos precisos de manera confiable. 

- ❌ **No puede acceder a sistemas externos** : no puede consultar bases de datos, llamar a las APIs ni interactuar con servicios. 

- ❌ **No puede realizar acciones** : solo puede generar texto, no puede realizar 

operaciones en el mundo real. 

**El problema raíz:** El agente está limitado a lo que el LLM sabe a partir de sus datos de entrenamiento. Para obtener información actual, datos externos o acciones reales, necesitas herramientas. 

