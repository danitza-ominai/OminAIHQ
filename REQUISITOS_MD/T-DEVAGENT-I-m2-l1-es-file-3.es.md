# **Manos a la obra: Transforma a tu agente** 

Transformemos al agente predeterminado del módulo 1 en un tutor de matemáticas especializado. 

## **Punto de partida (configuración predeterminada del módulo 1)** 

from google.adk.agents.llm_agent import Agent 

root_agent = Agent( model='gemini-2.5-flash', name='root_agent', description='Un agente de asistente útil.', instruction='Eres un asistente útil.' ) 

## **Paso 1: Actualiza el nombre interno** 

Asigna un nombre más descriptivo que refleje lo que realmente hace este agente: 

root_agent = Agent( model='gemini-2.5-flash', name='math_tutor_agent', # Un nombre interno más específico description='Un agente de asistente útil.', instruction='Eres un asistente útil.' ) 

## **Paso 2: Escribe una descripción específica** 

Recuerda que el parámetro description le dice a otros agentes qué hace este agente (lo cual es importante en sistemas de múltiples agentes). 

root_agent = Agent( model='gemini-2.5-flash', name='math_tutor_agent', description='Ayuda a los estudiantes a aprender álgebra guiándolos a través de los pasos para la resolución de problemas.', instruction='Eres un asistente útil.' ) 

**Qué cambió:** Otros agentes ahora pueden entender que este agente es específico para enseñar álgebra y no para preguntas generales. 

## **Paso 3: Escribe una instrucción simple** 

Recuerda que el parámetro instruction le dice a **este** agente **cómo** comportarse y responder. 

root_agent = Agent( model='gemini-2.5-flash', 

name='math_tutor_agent', 

description='Ayuda a los estudiantes a aprender álgebra guiándolos a través de los pasos para la resolución de problemas.', instruction='Eres un tutor de matemáticas paciente. Ayuda a los estudiantes con los problemas de álgebra.' ) 

### **Qué hace esta instrucción:** 

- Define la función del agente (tutor de matemáticas). 

- Establece su personalidad (paciente). 

- Especifica la tarea (ayudar con álgebra). 

**Nota:** Esta instrucción sencilla es perfecta para aprender los conceptos básicos. En el curso 3, aprenderás a escribir instrucciones listas para producción con una descripción detallada de la personalidad, límites y ejemplos. 

## **Transformación del agente completa** 

from google.adk.agents.llm_agent import Agent 

root_agent = Agent( model='gemini-2.5-flash', name='math_tutor_agent', description='Ayuda a los estudiantes a aprender álgebra guiándolos a través de los pasos para la resolución de problemas.', 

instruction='Eres un tutor de matemáticas paciente. Ayuda a los estudiantes con los problemas de álgebra.' ) 

**Guarda esto en tu archivo agent.py** en el directorio my_first_agent del módulo 1. 

### **Este agente sencillo expone los siguientes puntos:** 

- ✅ La definición de una función específica (tutor de matemáticas) 

   - ✅ Una personalidad definida (paciente) 

- 

   - ✅ La definición del alcance de la tarea (problemas de álgebra) 

- 

**¿Todo listo para continuar?** En el curso 3, aprenderás a mejorar tu agente con patrones de instrucciones profesionales, límites y ejemplos para su uso en producción. 

# **Pon a prueba tu agente personalizado** 

_Referencia:_ _<u>Documentación del ADK – Guía de inicio rápido de Python: Interacción con el agente</u>_ 

Ahora, veamos a tu agente tutor de matemáticas personalizado en acción con la interfaz web del ADK. 

## **Paso 1: Inicia la interfaz web** 

Desde tu directorio my_first_agent (o el directorio superior que lo contiene), ejecuta el siguiente comando: 

adk web 

### **Resultado esperado:** 

INFO: Started server process INFO: Waiting for application startup. INFO: Application startup complete. INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit) 

### **Qué hace:** 

- Inicia un servidor de desarrollo local en http://localhost:8000 . 

- Abre automáticamente tu navegador a la interfaz web del ADK. 

- Carga tu math_tutor_agent personalizado desde agent.py . 

### **La documentación del ADK brinda la siguiente información:** 

"Puedes iniciar la interfaz web con el siguiente comando: adk web . Este comando inicia un servidor web con una interfaz de chat para tu agente". 

## **Paso 2: Interactúa con tu tutor de matemáticas** 

Una vez que se abre la interfaz web, sigue estos pasos: 

1. **Selecciona a tu agente** en el menú desplegable (debería mostrar el nombre del agente). 

2. **Prueba las siguientes preguntas** para ver cómo funcionan tus instrucciones personalizadas: 

### **Ejemplos de interacciones:** 

**Pregunta:** "¿Cuánto es 2x + 5= 13?" 

**Comportamiento esperado:** Tu agente debería realizar estas tareas: 

- Actuar como tutor de matemáticas 

- Ayudar con el problema 

- Mostrar un tono paciente 

**Pregunta:** "No entiendo nada de álgebra". 

**Comportamiento esperado:** Tu agente debería realizar estas tareas: 

- Responder como un tutor paciente 

- Ofrecer ayuda con conceptos de álgebra 

- Mantener una actitud alentadora 

## **Paso 3: Observa la diferencia** 

Compara las respuestas de tu agente personalizado con la instrucción genérica “Eres un asistente útil” del módulo 1. 

### **Agente genérico (módulo 1):** 

instruction='Eres un asistente útil.' 

- Respuestas genéricas 

- Sin experiencia en un dominio específico 

### **Tutor de matemáticas personalizado (módulo 2):** 

instruction='Eres un tutor de matemáticas paciente. Ayuda a los estudiantes con los problemas de álgebra.' 

- Se enfoca en enseñar matemáticas. 

- Tiene una actitud paciente hacia la enseñanza. 

- Está especializado para ayudar con álgebra. 

Esto demuestra cómo incluso instrucciones simples y específicas pueden mejorar significativamente el comportamiento del agente. 

## **Paso 4: Detén el servidor** 

Cuando hayas terminado la prueba: 

- Presiona Ctrl + C en la terminal para detener el servidor web. 

### **Solución de problemas:** 

### **Si el agente no aparece en el menú desplegable, sigue estos pasos:** 

- Asegúrate de ejecutar adk web desde el directorio superior de my_first_agent . 

- O ejecuta adk web my_first_agent para especificar la ruta. 

### **Si ves las respuestas genéricas antiguas, sigue estos pasos:** 

- Asegúrate de haber guardado los cambios en agent.py . 

- Detén el servidor ( Ctrl + C ) y reinicia adk web . 

- Es necesario reiniciar el servidor para que detecte los cambios de código. 

# **Conclusiones principales** 

### **Parámetros obligatorios:** 

- Técnicamente, solo se requieren los parámetros model y name 

- Pero el parámetro instruction es fundamental para un comportamiento útil. 

- El parámetro description es importante en el caso los sistemas multiagente. 

### **Prácticas recomendadas para el curso 2:** 

- Escribe instrucciones sencillas y específicas que definan la función y la tarea. 

- Especifica lo que debe hace el agente (no te limites a "sé útil"). 

- Incluye un rasgo de su personalidad para establecer un tono. 

- Prueba con adk web para ver cómo las instrucciones afectan el comportamiento. 

### **Errores comunes:** 

- ❌ Usar instrucciones imprecisas, como "sé útil" 

- ❌ Confundir description con instruction 

- ❌ Olvidar asignar la variable root_agent 

- 

- ❌ Usar nombres poco claros o genéricos 

**Siguiente nivel:** En el curso 3, se enseñan patrones de instrucciones avanzados, que incluyen estructuras de múltiples secciones, límites y muestras de instrucciones con varios ejemplos con el objetivo de contar con agentes listos para producción. 

