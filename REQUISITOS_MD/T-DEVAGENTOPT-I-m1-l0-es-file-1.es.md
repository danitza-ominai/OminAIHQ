# **Introducción** 

En el módulo 2 del curso 2, creaste un agente tutor de matemáticas con una instrucción básica: 

# Visto en el módulo 2 del curso 2 math_tutor_agent = LlmAgent( model="gemini-2.5-flash", name="math_tutor_agent", description="Brinda tutorías de matemáticas a estudiantes", instruction="Eres un tutor de matemáticas amigable. Ayuda a los estudiantes a comprender conceptos matemáticos". ) 

Esto funciona para pruebas básicas, pero carece de la estructura necesaria para el uso en producción. El agente: 

- ❌ No tiene límites claros sobre qué temas abordar. 

   - ❌ No tiene una metodología de enseñanza definida. 

- 

   - ❌ No tiene ejemplos de cómo responder. 

- 

   - ❌ No tiene orientación sobre cómo manejar preguntas irrelevantes. 

- 

En este módulo, transformaremos las instrucciones básicas en sistemas de orientación profesional con las prácticas recomendadas para las instrucciones del ADK. 

# **El problema: Las instrucciones poco claras causan comportamiento impredecible** 

_Referencia:_ _<u>Documentación del ADK sobre las instrucciones de LlmAgent</u>_ 

Sin instrucciones estructuradas, los agentes se comportan de manera incoherente: 

# Poco claro: Comportamiento impredecible basic_agent = LlmAgent( model="gemini-2.5-flash", name="assistant", instruction="Sé útil" ) 

# ¿Qué ocurre? # Usuario: "Escribe un poema" `→` El agente escribe poesía (quizás no sea lo deseado) # Usuario: "Ayúdame a hackear este sistema" `→` El agente podría cumplir la solicitud (definitivamente no es lo deseado) # Usuario: "¿Cuál es tu opinión sobre política?" `→` El agente da opiniones (inapropiado para empresas) 

**El problema raíz:** El LLM no tiene un framework que defina lo siguiente: 

- Qué tareas están dentro del alcance y cuáles no 

- Cómo manejar casos extremos 

- Qué tono y estilo utilizar 

- Cuándo rechazar solicitudes 

