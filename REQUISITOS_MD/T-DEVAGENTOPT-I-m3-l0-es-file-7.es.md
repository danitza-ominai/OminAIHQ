# **Introducción: De agentes reactivos a agentes reflexivos** 

En los módulos anteriores, tus agentes respondieron de inmediato: 

# Visto en los módulos 1 a 3 agent = LlmAgent( 

model="gemini-2.5-flash", instruction="Resuelve problemas de los usuarios" ) 

# Usuario: "Planifica un viaje a Japón de 2 semanas con un presupuesto de USD 5,000" # El agente genera una respuesta inmediata, por lo que podría pasar por alto algunas consideraciones 

Esto funciona para tareas simples, pero los problemas complejos se benefician de un pensamiento estructurado: 

- ❌ No hay una descomposición de problemas paso a paso. 

   - ❌ No se consideran alternativas. 

- 

   - ❌ No hay un razonamiento interno visible para depurar. 

- 

   - ❌ Sin planificación, se podrían sacar conclusiones precipitadas. 

- 

## **¿Qué se considera un "problema complejo"?** 

Los problemas complejos requieren varias consideraciones, análisis de compensaciones o razonamiento secuencial: 

- **Estrategia empresarial:** "¿Cómo puedo reducir los costos de la nube en un 30% sin afectar el rendimiento?" (requiere analizar los factores relacionados con los costos, evaluar los requisitos de rendimiento y crear un enfoque por etapas). 

- **Decisiones técnicas:** "¿Debería utilizar microservicios o una arquitectura monolítica para el MVP de mi startup?" (requiere un análisis de compensaciones, como velocidad frente a escalabilidad, y considerar factores como el tamaño del equipo y crecimiento futuro). 

- **Planificación de varios pasos:** "Planifica un viaje a Japón de 2 semanas para una familia de 4 personas con un presupuesto de USD 5,000" (requiere coordinar vuelos, hoteles, actividades y comidas, todo dentro del presupuesto indicado). 

Problemas sencillos que no necesitan planificación: 

- **Preguntas fácticas y directas:** "¿Cuál es la capital de Francia?". 

- **Cálculos individuales:** "Convierte USD 100 a EUR". 

- **Tareas sencillas:** "Saluda cordialmente al usuario". 

## **Comparación de enfoques: planificación frente a múltiples agentes** 

Utiliza la planificación cuando un solo agente necesite razonar sobre varios pasos o compensaciones dentro de su dominio. Utiliza múltiples agentes (lo que se aborda en el curso 

5) cuando el problema requiera diferentes habilidades especializadas que deban repartirse entre varios agentes. Este módulo se enfoca en la incorporación de la planificación para mejorar las capacidades de razonamiento de un solo agente. 

En este módulo, agregaremos el planificador BuiltInPlanner del ADK para habilitar el razonamiento de varios pasos. 

# **El problema: Las tareas complejas requieren pensamiento estructurado** 

Sin planificación, los agentes tienen dificultades con los problemas de varios pasos: 

# Sin planificación: El agente intenta resolver el problema de inmediato problem_solver = LlmAgent( 

model="gemini-2.5-flash", instruction="Ayuda a los usuarios a resolver problemas complejos" ) 

# Usuario: "¿Cómo puedo reducir los costos de la nube de mi empresa en un 30% sin afectar el rendimiento?" 

# El agente podría hacer lo siguiente: 

- # - Pasar por alto consideraciones importantes 

- # - Proporcionar sugerencias superficiales 

- # - Omitir el análisis de compensaciones 

- # - Sacar conclusiones precipitadas 

**El problema raíz:** Las tareas complejas requieren desglosar el problema, considerar diferentes opciones y planificar un enfoque antes de responder. 

