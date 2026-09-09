# **La solución: Instrucciones estructuradas** 

## **Comprende el parámetro instruction** 

_Referencia:_ _<u>Documentación del ADK sobre cómo guiar al agente</u>_ 

Según la documentación del ADK, el parámetro instruction es, sin duda, el **más importante** para definir el comportamiento del agente. Debería definir lo siguiente: 

1. **Objetivo o tarea principal** : Lo que el agente debe lograr 

2. **Personalidad o perfil** : Cómo se presenta el agente 

3. **Restricciones de comportamiento** : Lo que el agente nunca debe hacer 

4. **Formato de salida** : Cómo deben estructurarse las respuestas 

_Referencia:_ _<u>Documentación del ADK sobre las plantillas de estado</u>_ 

La instrucción puede adoptar una de las siguientes formas: 

- **Cadena** (la más común) 

- **Plantilla de cadena** con sintaxis {var} para la inyección de estado 

- **Función** que devuelve una cadena (casos de uso avanzados) 

# **Conceptos básicos** 

## **Patrón de instrucción profesional** 

En el ADK, se recomienda utilizar el **formato Markdown** en las instrucciones para mejorar la comprensión de los LLM. Las instrucciones profesionales constan de cinco patrones clave que funcionan juntos para crear un comportamiento del agente predecible y de alta calidad. 

Exploraremos cada patrón por separado y, luego, los combinaremos en la sección "Práctica". 

### **Patrón 1: Identidad** 

Utiliza esta plantilla para definir quién es el agente: 

# Tu identidad 

Eres [Nombre], te desempeñas como [rol/cargo] y cuentas con [experiencia]. 

#### **Cómo utilizar esta plantilla:** 

- **[Name]** : Nombre ficticio opcional o rol general (p. ej., "Sarah" o "una asesora financiera") 

- **[Rol/título]** : Lo que hace el agente (p. ej., "asistente personal de compras" o "profesora de matemáticas") 

- **[Experiencia]** : Antecedentes que establecen credibilidad (p. ej., "una trayectoria de 10 años ayudando a estudiantes" o "conocimientos especializados en planificación de jubilaciones") 

#### **Por qué funciona:** 

- Brinda al agente una personalidad y un contexto coherentes. 

- Establece autoridad y experiencia. 

- Ayuda al LLM a adoptar una perspectiva y un tono apropiados. 

#### **Ejemplos en diferentes dominios:** 

- **Comercio electrónico:** "Eres Marcela, te desempeñas como asistente personal de compras y cuentas con conocimientos especializados en moda sustentable y marcas éticas". 

- **Educación:** "Eres un tutor de cálculo con experiencia que ha ayudado a más de 500 estudiantes a dominar las matemáticas avanzadas". 

- **Finanzas:** "Eres Juan González, te desempeñas como asesor de planificación financiera y cuentas con 15 años de experiencia en estrategias de inversión y jubilación". 

- **Salud:** "Eres coordinador de atención médica y cuentas con experiencia en gestionar seguros y programar tratamientos". 

### **Patrón 2: Misión** 

Utiliza esta plantilla para indicar el objetivo principal del agente: 

# Tu misión [Objetivo principal] a la vez que [criterios de calidad o restricciones]. 

#### **Cómo utilizar esta plantilla:** 

- **[Objetivo principal]** : Lo principal que debe lograr el agente (p. ej., "Ayuda a los usuarios a encontrar el atuendo perfecto" o "Ayuda a los estudiantes a resolver problemas de álgebra") 

- **[Criterios de calidad o restricciones]** : Cómo lograr el objetivo (p. ej., "a la vez que respetas el presupuesto", "a la vez que generas confianza" o "a la vez que demuestras empatía") 

#### **Por qué funciona:** 

- Enfoca al agente en su objetivo principal. 

- Establece expectativas sobre cómo lograr el objetivo. 

- Previene la corrupción del alcance y las respuestas irrelevantes. 

#### **Ejemplos en diferentes dominios:** 

- **Comercio electrónico:** "Ayuda a los clientes a descubrir productos que se ajusten a su estilo y valores, a la vez que respetas el presupuesto". 

- **Educación:** "Guía a los estudiantes para que comprendan conceptos matemáticos en profundidad, a la vez que promueves su confianza y sus habilidades de resolución de problemas". 

- **Finanzas:** "Ayuda a los clientes a crear planes financieros sustentables, a la vez que te aseguras de que comprendan los riesgos y las compensaciones". 

- **Salud:** "Ayuda a los pacientes a comprender sus opciones de tratamiento, a la vez que respetas su autonomía y sus inquietudes". 

### **Patrón 3: Metodología** 

Utiliza esta plantilla para definir un flujo de trabajo estructurado: 

# Cómo trabajas 1. **[Acción del paso 1]** : [Qué implica esto] 2. **[Acción del paso 2]** : [Qué implica esto] 3. **[Acción del paso 3]** : [Qué implica esto] 

4. **[Acción del paso 4]** : [Qué implica esto] 

#### **Cómo utilizar esta plantilla:** 

- **[Acción del paso X]** : Verbo que describe la acción de cada fase (p. ej., "comprender", "analizar", "recomendar" o "confirmar") 

- **[Qué implica esto]** : Breve explicación de lo que sucede en este paso 

- Generalmente de 3 a 5 pasos que fluyen de manera lógica 

#### **Por qué funciona:** 

- Garantiza un flujo de trabajo coherente en todas las interacciones. 

- Divide las tareas complejas en pasos claros y manejables. 

- Hace que el comportamiento del agente sea predecible y depurable. 

#### **Ejemplos en diferentes dominios:** 

- **Comercio electrónico:** "1. **Comprender** : Haz preguntas sobre las preferencias de estilo y el presupuesto | 2. **Seleccionar** : Selecciona los artículos que coincidan con los criterios | 3. **Presentar** : Muestra las opciones con explicaciones | 4. **Ajustar:** Realiza ajustes según los comentarios" 

- **Educación:** "1. **Evaluar** : Comprende lo que el estudiante encuentra confuso | 2. **Desglosar** : Divide el problema en partes más pequeñas | 3. **Guiar** : Guía al estudiante para que descubra la solución | 4. **Reforzar:** Confirma la comprensión con un problema similar" 

- **Finanzas:** "1. **Descubrir** : Obtén información sobre los objetivos y la situación actual del cliente | 2. **Analizar** : Revisa las opciones y compensaciones | 3. **Proponer** : Presenta recomendaciones personalizadas | 4. **Explicar** : Asegúrate de que el cliente comprenda la lógica" 

- **Salud:** "1. **Escuchar** : Comprende los síntomas y las inquietudes del paciente | 2. **Informar** : Explica las opciones de tratamiento disponibles | 3. **Asistir** : Ayuda a sopesar ventajas y desventajas | 4. **Conectar** : Facilita los próximos pasos con los proveedores" 

### **Patrón 4: Límites** 

Utiliza esta plantilla para definir lo que el agente nunca debe hacer: 

- # Tus límites 

**Nota:** Estos límites a nivel de la instrucción se aplican además de la configuración de seguridad del LLM, lo que proporciona una capa adicional de control específica para el rol de tu agente. 

- ## Límites de alcance 

- Nunca [acción fuera del dominio del agente] 

- Nunca [promesa o compromiso que el agente no puede cumplir] 

- Nunca [manejes información sensible o restringida] 

## Límites de calidad de la respuesta 

- Siempre basa tus respuestas en [datos, herramientas o hechos disponibles] 

- Nunca inventes [tipos específicos de información] 

- Si no sabes algo, [cómo manejar la incertidumbre] 

- Nunca [comportamiento riesgoso, como adivinar] 

## Límites de privacidad y seguridad 

- Nunca [compartas información protegida] 

- Nunca [solicites datos inapropiados] 

- Siempre [mantén los estándares de protección] 

#### **Cómo utilizar esta plantilla:** 

- **Límites de alcance** : Lo que está fuera de la experiencia o autoridad del agente (esto evita que se distorsione la misión) 

- **Límites de calidad de la respuesta** : Reglas para la exactitud y la prevención de alucinaciones (fundamentales para la confianza) 

- **Límites de privacidad y seguridad** : Reglas de protección de datos y seguridad del usuario (específicas del dominio) 

#### **Por qué funciona:** 

- **Se aplica junto con la configuración de seguridad del LLM** para un control específico de cada rol más allá de las protecciones del modelo base. 

- **Reduce las alucinaciones** , ya que requiere respuestas fácticas basadas en herramientas. 

- **Evita respuestas inapropiadas o fuera del alcance,** que dañan la confianza. 

- **Protege la privacidad del usuario** y mantiene los estándares de calidad. 

#### **Ejemplos en diferentes dominios:** 

- **Comercio electrónico:** "Nunca recomiendes productos fuera del presupuesto indicado por el cliente | Nunca inventes la disponibilidad ni las especificaciones de un producto | Nunca almacenes los datos de la tarjeta de pago". 

- **Educación:** "Nunca completes las tareas de los estudiantes | Nunca des respuestas sin 

explicación | Nunca compartas información sobre el desempeño de un estudiante con otro". 

- **Finanzas:** "Nunca brindes recomendaciones de inversión específicas sin una exención de responsabilidad | Nunca inventes datos ni proyecciones de mercado | Nunca compartas los detalles de la cartera de un cliente con terceros". 

- **Salud:** "Nunca diagnostiques afecciones médicas | Nunca recomiendes suspender medicamentos recetados | Nunca compartas información de pacientes sin autorización". 

### **Patrón 5: Demostración con varios ejemplos** 

Utiliza esta plantilla para demostrar el comportamiento deseado: 

# Interacciones de ejemplo 

**Cuando [situación común 1]:** Usuario: "[Ejemplo de entrada del usuario]" Tú: "[Ejemplo de respuesta del agente que muestra el tono, el enfoque y el formato deseados]" 

**Cuando [situación común 2]:** Usuario: "[Ejemplo de entrada del usuario]" Tú: "[Ejemplo de respuesta del agente]" 

**Cuando [caso extremo o situación límite]:** Usuario: "[Ejemplo de entrada desafiante]" Tú: "[Ejemplo de cómo manejar la situación con elegancia]" 

#### **Cómo utilizar esta plantilla:** 

- **[situación común X]** : Situaciones típicas que encontrará el agente (2 o 3 ejemplos) 

- **[caso extremo]** : Situaciones desafiantes, como solicitudes poco claras, preguntas fuera del alcance o información faltante 

- Muestra interacciones completas, es decir, que incluyan tanto la entrada del usuario como la respuesta del agente 

- Demuestra el tono, la redacción y la estructura que deseas que el agente imite 

#### **Por qué funciona:** 

- Demuestra un estilo y tono de comunicación exactos. 

- Muestra cómo manejar casos extremos y situaciones difíciles. 

- Proporciona plantillas concretas con las que el LLM puede identificar patrones. 

- Guía la redacción específica y la estructura de la respuesta. 

#### **Ejemplos en diferentes dominios:** 

- **Comercio electrónico:** " **Cuando el cliente tiene preferencias contradictorias:** Usuario: 'Quiero calidad de lujo, pero a un precio económico' | Tú: 'Entiendo que buscas una buena relación precio-calidad. Te mostraré nuestras opciones de gama media, que ofrecen un excelente equilibrio entre costo y rendimiento. Estas marcas se enfocan 

en…". 

- **Educación:** " **Cuando un estudiante pide una respuesta directa:** Usuario: 'Solo dime a qué equivale x' | Tú: 'Veo que quieres avanzar rápido. Pero analicemos esto juntos para que puedas resolver problemas similares de forma independiente. ¿Cuál es el primer paso que debemos seguir para aislar x?'". 

- **Finanzas:** " **Cuando se piden sugerencias específicas sobre acciones:** Usuario: '¿Debería comprar acciones de Tesla?' | Tú: 'No puedo recomendar acciones específicas, pero puedo ayudarte a tomar una decisión. ¿Cuál es tu plazo de inversión?, ¿qué nivel de riesgo puedes tolerar? Exploremos…'". 

- **Salud:** " **Cuando el paciente describe síntomas:** Usuario: 'Tengo dolor de cabeza y fiebre' | Tú: 'Entiendo que no te sientes bien. Aunque no puedo darte un diagnóstico, puedo ayudarte a prepararte para tu consulta médica. ¿Hace cuánto tiempo tienes estos síntomas?, ¿tomaste alguna…?'". 

## **Prácticas recomendadas del ADK para las instrucciones** 

_Referencia:_ _<u>Documentación del ADK sobre cómo redactar instrucciones eficaces</u>_ 

La documentación oficial del ADK brinda la siguiente información: 

#### ✓ **Exprésate de forma clara y específica** 

Evita la ambigüedad en las definiciones de tareas. Cuanto más específica sea tu indicación, más coherente será el comportamiento del agente. 

#### ✓ **Utiliza el formato Markdown** 

Los encabezados, las listas y las secciones facilitan la legibilidad para las personas y mejoran la comprensión por parte del LLM. 

#### ✓ **Demuestra el comportamiento esperado (con varios ejemplos)** 

Muestra los patrones de comportamiento deseados a través de ejemplos. Esto es especialmente importante para hacer lo siguiente: 

- Manejar casos extremos 

- Mantener un tono coherente 

- Seguir formatos de respuesta específicos 

#### ✓ **Guía el uso de herramientas** 

Cuando tu agente tenga herramientas (lo que se aborda en el curso 4), explica en las instrucciones _cuándo_ y _por qué_ usar cada herramienta. 

**Más información:** La documentación del ADK abarca patrones avanzados, incluidos los siguientes: 

- Plantillas de estado con la sintaxis {var} 

- Instrucciones dinámicas con funciones InstructionProvider 

- Instrucciones globales para sistemas de múltiples agentes 

Consulta la <u>documentación del ADK sobre LlmAgent para obtener todos los detalles.</u> 

# **Ejemplo práctico** 

Combinemos los cinco patrones en un agente completo y listo para producción. Este ejemplo práctico demuestra cómo la identidad, la misión, la metodología, los límites y los ejemplos funcionan juntos. 

## **Paso 1: Crea el proyecto** 

adk create customer_support_agent cd customer_support_agent 

## **Paso 2: Escribe el código del agente (combinando todos los patrones)** 

Reemplaza el contenido de agent.py por este código que utiliza los cinco patrones de la sección de conceptos básicos: 

""" 

Agente profesional de asistencia al cliente con instrucciones estructuradas. Demuestra las prácticas recomendadas del ADK para la redacción de instrucciones. 

Referencia: https://google.github.io/adk-docs/agents/llm-agents/ """ 

from google.adk.agents import LlmAgent 

root_agent = LlmAgent( model="gemini-2.5-flash", name="support_specialist", description="Agente profesional de asistencia al cliente con roles y límites claros", instruction=""" # Tu identidad # (Patrón 1: Identidad, establece la personalidad y la experiencia) Eres Alex Chen, te desempeñas como especialista sénior en asistencia técnica y cuentas con 5 años de experiencia. 

# Tu misión # (Patrón 2: Misión, define el objetivo principal) Ayuda a los clientes a resolver problemas técnicos de manera eficiente y profesional. 

# Cómo trabajas # (Patrón 3: Metodología, proporciona un enfoque estructurado) 

1. **Reconocer**: Muestra empatía por la situación del cliente 

2. **Aclarar**: Haz preguntas específicas para comprender el problema 

3. **Resolver**: Proporciona soluciones claras y paso a paso 

4. **Verificar**: Confirma que el problema esté completamente resuelto 

# Estilo de comunicación 

- Profesional pero amigable 

- Claro y sin tecnicismos 

- Paciente y empático 

- Conciso (200 palabras como máximo, a menos que se necesiten detalles) 

# Tus límites 

# (Patrón 4: Límites, establece límites y estándares de calidad) 

**Importante:** Estos límites funcionan junto con la configuración de seguridad integrada del modelo 

para garantizar respuestas apropiadas y útiles. 

## Lo que nunca debes hacer 

- Nunca proporciones acceso a cuentas, contraseñas ni restablecimientos de contraseñas - Nunca compartas información sobre otros clientes 

- Nunca hagas promesas sobre características, plazos o reembolsos 

- Nunca brindes asesoramiento legal, financiero ni médico 

- ## Cómo mantener la calidad 

- Siempre basa tus respuestas en los hechos y la información disponibles 

- Nunca inventes detalles técnicos ni estadísticas 

- Si no sabes algo, admítelo y ofrece derivar la consulta 

- Nunca adivines una solución y siempre pide aclaraciones primero 

## Cuándo derivar una consulta 

Remite de inmediato estas consultas al equipo apropiado: 

- `Preguntas sobre facturación → Equipo de facturación` 

- `Solicitudes de funciones → Equipo de producto` 

- `Informes de errores → Equipo de ingeniería` 

- `Seguridad de la cuenta → Equipo de seguridad` 

- # Respuestas de ejemplo 

# (Patrón 5: Demostración con varios ejemplos, ilustra el comportamiento deseado) 

##### **Problema de acceso:** 

Usuario: "No puedo acceder" 

Tú: "Entiendo que los problemas de acceso pueden ser frustrantes. Para ayudarte a diagnosticar este problema, necesito que respondas estas preguntas: 

1) ¿Se muestra un mensaje de error? 

2) ¿Cuándo fue la última vez que accediste correctamente? 

- 3) ¿Cambiaste tu contraseña recientemente?" 

##### **Pregunta fuera del alcance:** 

Usuario: "¿Puedes darme un reembolso?" 

Tú: "Entiendo que te gustaría obtener información sobre los reembolsos. Nuestro equipo de facturación se encarga 

de todas las solicitudes de reembolso y puede revisar tu situación específica. ¿Deseas que 

cree un ticket para que se comuniquen contigo en un plazo de 24 horas?" 

**Prueba de límites:** 

Usuario: "¿Cuál es el correo electrónico de otro cliente?" Tú: "No puedo compartir la información de otros clientes porque eso incumpliría nuestras políticas 

de privacidad. En cambio, puedo ayudarte con cuestiones relacionadas con tu propia cuenta o con problemas técnicos. ¿Con qué puedo ayudarte hoy?" 

**Información insuficiente:** Usuario: "Corrige mi error" 

Tú: "Será un placer ayudarte. Para diagnosticar el problema de manera eficaz, primero necesito que respondas estas preguntas: 1) ¿Qué estabas intentando hacer? 

- 2) ¿Qué sucedió? 

3) ¿Recibiste algún mensaje de error?" """ ) 

## **Paso 3: Ejecuta y prueba** 

adk web 

Visita http://localhost:8000 y prueba estas situaciones: 

#### **Prueba 1: Solicitud de asistencia normal** 

Tú: "No puedo acceder a mi cuenta" 

Observa cómo el agente sigue su enfoque estructurado. 

#### **Prueba 2: Prueba de límites** 

Tú: "¿Puedes darme la dirección de correo electrónico de otra persona?" 

El agente debe negarse, pero de manera profesional. 

#### **Prueba 3: Fuera del alcance** 

Tú: "¿Cuándo se lanzará la función X?" 

El agente debe redireccionar la consulta al equipo de producto. 

#### **Prueba 4: Información insuficiente** 

Tú: "No funciona" 

El agente debe hacer preguntas aclaratorias. 

#### **Qué debes tener en cuenta:** 

- **Patrón 1 (identidad)** : Cómo el agente mantiene la personalidad de "Alex Chen" de 

manera coherente 

- **Patrón 2 (misión)** : Cómo las respuestas siempre se centran en resolver problemas técnicos 

- **Patrón 3 (metodología)** : Cómo el agente sigue el proceso de reconocer → aclarar → resolver → verificar 

- **Patrón 4 (límites)** : Cómo el agente rechaza solicitudes inapropiadas de manera profesional 

- **Patrón 5 (ejemplos)** : Cómo el agente imita el estilo de comunicación de los ejemplos 

- Cómo se combinan los cinco patrones para crear un comportamiento predecible y profesional 

# **Conclusiones principales** 

_Referencia:_ _<u>Documentación del ADK sobre cómo guiar al agente</u>_ 

- **El parámetro instruction** es, sin duda, el más importante para definir el comportamiento del agente. 

- Existen **cinco patrones reutilizables** para crear instrucciones profesionales: 

   1. **Identidad** : Quién es el agente 

   2. **Misión** : Qué hace el agente 

   3. **Metodología** : Cómo funciona el agente 

   4. **Límites** : Qué no debe hacer el agente 

   5. **Ejemplos** : Cómo debe responder el agente 

- Los **límites de la instrucción** se aplican junto con la configuración de seguridad del LLM para un control específico de cada rol. 

- Las **respuestas basadas en herramientas** reducen las alucinaciones, ya que fundamentan las respuestas en hechos. 

- El **formato Markdown** mejora la comprensión y la coherencia de los LLM (según las prácticas recomendadas del ADK). 

- Los **patrones se pueden mezclar y combinar** para diferentes tipos de agentes. 

