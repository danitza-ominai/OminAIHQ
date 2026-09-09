# **La solución: Planifica con BuiltInPlanner** 

## **Habilita el razonamiento de varios pasos** 

_Referencia:_ _<u>Documentación del ADK sobre planificación</u>_ 

Según la documentación del ADK, utiliza BuiltInPlanner para aprovechar la función de pensamiento de Gemini: 

" **planner (opcional):** Asigna una instancia de BasePlanner para habilitar el razonamiento y la planificación de varios pasos antes de la ejecución. **BuiltInPlanner :** Aprovecha las capacidades de planificación integradas del modelo (p. ej., la función de pensamiento de Gemini)". 

from google.adk.agents import LlmAgent from google.adk.planners import BuiltInPlanner from google.genai import types 

planning_agent = LlmAgent( model="gemini-2.5-flash", planner=BuiltInPlanner( thinking_config=types.ThinkingConfig( include_thoughts=True, # Muestra el razonamiento en la respuesta thinking_budget=1024 # Tokens asignados para el pensamiento ) ), instruction="Resuelve problemas complejos de forma sistemática" ) 

**Nota:** Esta función utiliza las capacidades de <u>pensamiento de Gemini.</u> 

## **Observa la planificación en acción** 

Comparemos el mismo problema con la planificación y sin ella para entender su verdadero impacto: 

**Instrucción de ejemplo:** "¿Debería comprar o alquilar un auto para mi viaje diario de 80 kilómetros?". 

### **Sin planificación** 

basic_agent = LlmAgent( model="gemini-2.5-flash", instruction="Ayuda a los usuarios a tomar decisiones" ) 

#### **Respuesta típica sin planificación:** 

El alquiler ofrece pagos mensuales más bajos y te permite obtener un auto nuevo cada pocos años. 

Si compras, el auto será tuyo y podrás hacer todos los kilómetros que quieras. Para un viaje diario 

de 80 kilómetros, quizá sea mejor comprar, ya que los alquileres ofrecen kilometraje limitado. 

#### **Qué falta:** 

- No hay un desglose de las implicaciones financieras. 

- No se considera el costo total a lo largo del tiempo. 

- No cuantifica el problema del kilometraje (80 kilómetros/día = ~29,000 kilómetros/año) 

- No se comparan diferentes situaciones. 

### **Con BuiltInPlanner** 

planning_agent = LlmAgent( 

model="gemini-2.5-flash", 

planner=BuiltInPlanner( 

   - thinking_config=types.ThinkingConfig( 

   - include_thoughts=True, # Observa el proceso de razonamiento thinking_budget=1024 # Asigna tokens para el pensamiento 

   - ) 

   - ), 

- instruction="Ayuda a los usuarios a tomar decisiones" 

- ) 

#### **Respuesta con planificación (include_thoughts=True muestra el razonamiento):** 

[Razonamiento interno: Visible porque se configuró include_thoughts=True] Déjame analizar esto de forma sistemática: 

- 80 kilómetros/día × 5 días/semana × 52 semanas = ~21,000 kilómetros/año 

- La mayoría de los alquileres limitan el uso a 16,000-19,000 kilómetros/año, lo que 

- está al límite 

- Es necesario comparar el costo total, la flexibilidad y los cargos por exceso de 

- kilometraje 

- Se debe considerar cuánto tiempo se conservará el auto 

Factores clave: 

1. Límites de kilometraje del alquiler: El estándar es 19,000, pero se necesitaría un paquete de 24,000 (pago más alto) 

2. Comprar implica un pago mensual más alto, pero genera valor líquido 3. Hacer muchos kilómetros afecta el valor de reventa de ambas formas 

Déjame crear algunas situaciones… 

##### [Respuesta final] 

Para tu viaje diario de 80 kilómetros (~21,000 kilómetros/año), esta es la comparación: 

**Alquilar:** 

- Costo mensual: USD 350 (con el paquete de 24,000 kilómetros/ año , superarías el estándar de 19,000) - Total de 3 años: USD 12,600 en pagos - Resultado final: Devuelves el auto, sin valor líquido - Riesgo: Cargos por exceso si superas el kilometraje (a USD 0.25/kilómetro pueden acumularse de manera rápida) 

**Comprar:** 

- Costo mensual: USD 450 (préstamo típico de 5 años) - Total de 3 años: USD 16,200 en pagos 

- Resultado final: Tienes la propiedad de un auto que vale USD ~15,000 (contabilizando la depreciación por kilometraje alto) - Costo neto: USD ~1,200 después de considerar el capital propio 

**Recomendación para tu situación:** 

Deberías comprar en lugar de alquilar. El kilometraje alto (21,000/año) hace que el alquiler sea riesgoso y caro: 

1. Necesitarías un paquete de alquiler con mayor kilometraje (más caro) 

2. Cualquier viaje imprevisto puede generar cargos por exceso costosos 

3. Al cabo de 3 años, los costos de compra representan solo USD ~1,200 más si se tiene en cuenta el capital propio 

4. Comprar te da flexibilidad, dado que no hay restricciones de kilometraje 

Excepción: Si priorizas un pago mensual más bajo sobre el costo a largo plazo, un alquiler 

de 24,000 kilómetros podría ser adecuado, pero deberás tener en cuantas los posibles cargos por exceso de kilometraje. 

#### **Qué agregó la planificación:** 

- **Descomposición del problema:** Se desglosaron el cálculo del kilometraje y los factores de costo. 

- **Análisis de varios factores:** Se compararon el costo total, el capital, los riesgos y la flexibilidad. 

- **Pensamiento cuantitativo:** Se calcularon números reales en lugar de generalizaciones. 

- - **Comparación de situaciones:** Se examinaron ambas opciones en un contexto específico. 

- **Recomendación matizada:** Se ofrecieron un consejo principal y un caso de excepción. 

#### **Información clave sobre las instrucciones:** 

La instrucción fue simple: "Ayuda a los usuarios a tomar decisiones". No es necesario redactar instrucciones complejas como "Divide el problema en fases" o "Considera las compensaciones y restricciones". La capacidad de planificación permite este razonamiento estructurado de forma automática: thinking_budget determina la profundidad de pensamiento del modelo, mientras que include_thoughts te permite ver (y depurar) ese proceso de razonamiento. 

# **Conceptos básicos** 

## **1. Comprende el parámetro planner** 

_Referencia:_ _<u>Documentación del ADK sobre el parámetro planner</u>_ 

El parámetro planner (singular, no plural) habilita la planificación: 

from google.adk.planners import BuiltInPlanner 

agent = LlmAgent( model="gemini-2.5-flash", planner=BuiltInPlanner(...) # Singular: planner=, no planners= ) 

#### **Puntos clave:** 

- Por el momento, esta función solo está disponible en Python. 

- Utiliza las capacidades de pensamiento integradas del modelo. 

- Es ideal para problemas complejos de varios pasos. 

## **2. Configura ThinkingConfig** 

_Referencia:_ _<u>Documentación del ADK sobre los parámetros ThinkingConfig</u>_ 

La documentación brinda la siguiente información: 

"Aquí, el parámetro thinking_budget indica al modelo cuántos tokens de pensamiento puede utilizar al generar una respuesta. El parámetro include_thoughts controla si el modelo debe incluir sus pensamientos sin procesar y su proceso de razonamiento interno en la respuesta". 

from google.genai import types 

# Configuración con razonamiento visible transparent_config = types.ThinkingConfig( include_thoughts=True, # Muestra el razonamiento del agente thinking_budget=1024 # Asigna 1,024 tokens de pensamiento ) 

# Configuración con razonamiento oculto opaque_config = types.ThinkingConfig( include_thoughts=False, # Oculta el razonamiento interno thinking_budget=512 # Utiliza menos tokens de pensamiento ) 

#### **Explicación de los parámetros:** 

- **include_thoughts** : Si se establece como verdadero, la respuesta incluye el proceso de razonamiento interno del agente. 

- **thinking_budget** : Es la cantidad de tokens que el modelo puede utilizar para pensar 

(no se incluye en la respuesta final). 

## **3. Elige entre distintos tipos de planificadores** 

_Referencia:_ _<u>Documentación del ADK sobre los tipos de planificadores</u>_ 

El ADK ofrece dos tipos de planificadores, cada uno adecuado para diferentes situaciones: 

### **BuiltInPlanner (recomendado para modelos de Gemini)** 

Aprovecha las capacidades de pensamiento nativas del modelo. La documentación del ADK brinda la siguiente información: 

" **BuiltInPlanner :** Aprovecha las capacidades de planificación integradas del modelo (p. ej., la función de pensamiento de Gemini)". 

#### **Es ideal para lo siguiente:** 

- **Modelos de Gemini:** 2.5 Flash, 2.5 Pro, etc., con compatibilidad de pensamiento integrada 

- **Razonamiento transparente:** Consulta el proceso de pensamiento interno con include_thoughts=True 

- **Control flexible:** Ajusta la profundidad del razonamiento con thinking_budget 

#### **Configuración:** 

from google.adk.planners import BuiltInPlanner from google.genai import types 

agent = LlmAgent( model="gemini-2.5-flash", planner=BuiltInPlanner( thinking_config=types.ThinkingConfig( include_thoughts=True, # Muestra el razonamiento (ideal para la depuración) thinking_budget=1024 # Tokens de pensamiento (por lo general, entre 512 y 2,048) ) ) ) 

#### **Parámetros clave:** 

- **thinking_budget :** Controla la profundidad con la que el modelo puede razonar. Los valores más altos (p. ej., 2,048) permiten un análisis más exhaustivo para problemas complejos. Los valores más bajos (p. ej., 512) son más rápidos para tareas más simples. 

- **include_thoughts :** Cuando se establece como verdadero, la respuesta incluye el proceso de razonamiento interno del modelo. Es fundamental para depurar y 

comprender cómo el agente llegó a su respuesta. 

### **PlanReActPlanner (para modelos que no sean de Gemini)** 

_Referencia:_ _<u>Documentación del ADK sobre PlanReActPlanner</u>_ 

La documentación del ADK brinda la siguiente información: 

" **PlanReActPlanner :** Este planificador le indica al modelo que siga una estructura específica en su resultado: primero, crear un plan; luego, ejecutar acciones (como llamar a herramientas), y, por último, proporcionar un razonamiento para sus pasos. _Resulta particularmente útil para modelos que no tienen una función de 'pensamiento' integrada_ ". 

#### **Es ideal para lo siguiente:** 

- **Modelos que no son de Gemini:** P. ej., otros LLM sin capacidades de razonamiento nativas 

- **Formato de salida estructurado:** Aplica la estructura PLANIFICACIÓN → ACCIÓN → RAZONAMIENTO → RESPUESTA_FINAL 

- **Flujos de trabajo con muchas herramientas:** Las fases explícitas de acción y razonamiento funcionan bien con las llamadas a herramientas 

- **Aplicación de un enfoque sistemático:** Cuando necesitas una estructura de salida garantizada 

#### **Configuración:** 

from google.adk.planners import PlanReActPlanner 

agent = LlmAgent( model="your-model", # Cualquier modelo, especialmente los que no sean de Gemini planner=PlanReActPlanner() ) 

#### **Ejemplo de estructura de salida:** 

Según la documentación del ADK, PlanReActPlanner produce un resultado estructurado como el siguiente: 

[usuario]: Ayúdame a planificar una reunión externa con el equipo 

[agente]: /*PLANIFICACIÓN*/ 

1. Determina el tamaño del equipo y las restricciones del presupuesto 2. Sugiere opciones de lugares según el tamaño del equipo 

3. Propón un cronograma de actividades 

4. Proporciona una lista de verificación de logística 

/*ACCIÓN*/ 

[Cualquier llamada a herramientas aparecerá aquí] 

/*RAZONAMIENTO*/ 

Para que una reunión externa con el equipo sea todo un éxito, debe incluir tanto 

actividades estructuradas como tiempo libre. Combinar ejercicios de integración con momentos sociales informales genera un mejor compromiso que los enfoques puramente empresariales o puramente sociales. 

##### /*RESPUESTA_FINAL*/ 

Aquí tienes un plan recomendado para la reunión externa con tu equipo: 

Lugar: Considera [recomendaciones específicas] Cronograma: Talleres por la mañana, actividades de equipo por la tarde y tiempo social por la noche 

Presupuesto: Entre USD 150 y USD 200 por persona para cubrir los gastos del lugar y las actividades 

#### **¿Qué planificador deberías usar?** 

- **Utiliza BuiltInPlanner** cuando trabajes con modelos de Gemini (2.5 Flash, 2.5 Pro o 2.0 Flash) 

   - Proceso de razonamiento más natural 

   - Profundidad de pensamiento configurable con thinking_budget 

   - Visibilidad opcional del razonamiento con include_thoughts 

- **Utiliza PlanReActPlanner** en los siguientes casos: 

   - Cuando trabajes con modelos que no sean de Gemini que carezcan de capacidades de pensamiento integradas 

   - Cuando necesites una estructura de salida estricta (PLANIFICACIÓN/ACCIÓN/RAZONAMIENTO/RESPUESTA_FINAL) 

   - Para crear agentes con muchas herramientas en los que las fases de acción explícitas ayudan 

En este curso, nos centramos en **BuiltInPlanner** ya que utilizamos modelos de Gemini. PlanReActPlanner se aborda en cursos avanzados de múltiples agentes. 

## **4. Cuándo utilizar la planificación** 

#### **Utiliza la planificación para lo siguiente:** 

- ✅ Resolución de problemas de varios pasos 

   - ✅ Tareas que requieren análisis de compensaciones 

- 

   - ✅ Toma de decisiones complejas 

- 

   - ✅ Depuración del razonamiento del agente 

- 

#### **Omite la planificación para lo siguiente:** 

- ❌ Preguntas sencillas y directas 

   - ❌ Búsquedas fácticas rápidas 

- 

   - ❌ Tareas de un solo paso 

- 

- ❌ Respuestas urgentes 

# Buen uso de la planificación strategic_agent = LlmAgent( model="gemini-2.5-flash", planner=BuiltInPlanner( thinking_config=types.ThinkingConfig( include_thoughts=True, thinking_budget=2048 # Gran presupuesto para análisis complejos ) ), instruction="Analiza estrategias comerciales y brinda recomendaciones" ) 

# Planificación innecesaria simple_agent = LlmAgent( model="gemini-2.5-flash", # No se incluye el parámetro planner, ya que se trata de una tarea simple instruction="Saluda cordialmente a los usuarios" ) 

## **5. Depura el agente haciendo visibles sus pensamientos internos** 

Habilita include_thoughts=True para ver el razonamiento del agente: 

debug_agent = LlmAgent( model="gemini-2.5-flash", planner=BuiltInPlanner( thinking_config=types.ThinkingConfig( include_thoughts=True, # Observa el razonamiento interno thinking_budget=1024 ) ), instruction="Ayuda a los usuarios a depurar problemas de forma sistemática" ) 

# La respuesta mostrará lo siguiente: # 1. El proceso de pensamiento interno del agente # 2. Cómo desglosó el problema # 3. La respuesta final 

# 🧪 **Ejemplo práctico** 

Creemos un agente de resolución de problemas que utilice la planificación para abordar preguntas complejas. 

## **Paso 1: Crea el proyecto** 

adk create problem_solver cd problem_solver 

## **Paso 2: Escribe el código del agente habilitado para planificación** 

Reemplaza el contenido de agent.py por lo siguiente: 

""" Agente de resolución de problemas con capacidades de planificación integradas. Demuestra cómo utilizar BuiltInPlanner del ADK con ThinkingConfig. """ 

from google.adk.agents import LlmAgent from google.adk.planners import BuiltInPlanner from google.genai import types 

- # Agente habilitado para planificación para la resolución de problemas complejos root_agent = LlmAgent( 

model="gemini-2.5-flash", name="strategic_problem_solver", description="Resuelve problemas complejos con razonamiento y planificación de varios pasos", instruction="""Te encargas de la resolución estratégica de problemas. 

Tu enfoque ante problemas complejos: 

1. **Entender**: Desglosa el problema en componentes 

2. **Analizar**: Considera varios enfoques y compensaciones 

3. **Planificar**: Desarrolla una estrategia de solución paso a paso 

4. **Ejecutar**: Proporciona recomendaciones claras y prácticas 

Para problemas complejos: 

- Analiza las implicaciones y los casos extremos 

- Considera las consecuencias a corto y largo plazo 

- Identifica riesgos potenciales y estrategias de mitigación 

- Comparte el razonamiento detrás de tus recomendaciones 

Actúa de manera exhaustiva, analítica y sistemática en tu enfoque.""", 

planner=BuiltInPlanner( thinking_config=types.ThinkingConfig( include_thoughts=True, # Muestra el proceso de razonamiento thinking_budget=2048 # Gran presupuesto para el pensamiento complejo ) ) ) 

## **Paso 3: Ejecuta y prueba** 

adk web 

#### **Prueba 1: Problema complejo de varios pasos** 

Prueba esta instrucción: 

¿Cómo debería prepararme para una transición profesional de la ingeniería de software a la administración de productos en los próximos 12 meses? 

#### **Comportamiento esperado con la planificación:** 

- El agente muestra su proceso de pensamiento. 

- Desglosa la transición en fases, cada una con distintos requisitos de habilidades. 

- Considera varias estrategias de preparación. 

- Analiza qué habilidades desarrollar y en qué orden. 

- Proporciona una hoja de ruta estructurada y por fases. 

#### **Lo que verás:** 

[Proceso de razonamiento: Visible porque se configuró include_thoughts=True] 

- Se analizan las brechas de habilidades: habilidades de ingeniería (actuales) frente 

- a habilidades de gerente de producto (por desarrollar) 

- Principales competencias de un gerente de producto: estrategia de productos, 

- investigación sobre los usuarios, administración de partes interesadas y elaboración de hojas de ruta 

- Habilidades transferibles desde SWE: conocimiento técnico, análisis de datos y 

- ejecución de proyectos 

- Cronograma: Un plazo de 12 meses permite una transición gradual mientras se mantiene 

- el empleo actual 

- Estrategia: Desarrollar habilidades `→` obtener experiencia como gerente de producto `→` 

- crear una red de contactos `→` transición 

##### [Respuesta final] 

Aquí tienes una hoja de ruta de 12 meses para tu transición de la ingeniería de software a la administración de productos: 

Meses 1 a 3: Adquiere conocimientos básicos en administración de productos 

- Lee libros clave sobre la administración de productos (como Inspired o The Lean 

- Product Playbook) 

- Anótate en cursos en línea sobre administración de productos (como Reforge o Product 

- School) 

- Empieza a escribir especificaciones de productos para las funciones actuales de tu 

- equipo 

- Asiste como observador a las reuniones del gerente de producto actual 

Meses 4 a 6: Desarrolla las habilidades clave de un gerente de producto 

- Lidera un pequeño proyecto de principio a fin (desde la especificación de la función 

- a su lanzamiento) 

- Realiza entrevistas a usuarios del producto de tu equipo 

- Practica la administración de partes interesadas en tu puesto actual 

- Crea una cartera de artefactos de productos (especificaciones, hojas de ruta, 

- análisis de métricas) 

Meses 7 a 9: Obtén experiencia y desarrolla tu presencia en el mundo de la administración de productos 

- Haz trabajo voluntario en proyectos relacionados con la administración de productos 

- (planificación de hojas de ruta o investigación sobre los usuarios) 

- Inicia un proyecto propio como gerente de producto para demostrar tus habilidades 

- Contáctate con gerentes de producto (entrevistas informativas o reuniones) 

- Habla con un gerente de producto para que te ofrezca mentoría en administración de 

- productos 

Meses 10 a 12: Busca trabajo activamente 

- Actualiza tu currículum destacando los logros más importantes para el puesto de 

- gerente de producto 

- Postúlate a programas de APM o puestos de gerente de producto en empresas más 

- pequeñas 

- Aprovecha oportunidades internas, si las hubiera 

- Prepárate para aceptar un puesto júnior (no sénior) al principio 

Este enfoque gradual te permite desarrollar habilidades mientras mantienes el empleo actual, por lo que reduce el riesgo. 

#### **Prueba 2: Pregunta directa simple (observa la diferencia)** 

Prueba esta instrucción: 

¿Cuál es la capital de Francia? 

#### **Comportamiento esperado:** 

- Incluso con la planificación habilitada, las preguntas simples obtienen respuestas directas. 

- La sobrecarga de pensamiento es mínima para las consultas directas. 

- El agente adapta la complejidad a la tarea. 

#### **Prueba 3: Análisis de compensaciones** 

Prueba esta instrucción: 

¿Debería alquilar o comprar una casa en San Francisco si tengo planeado quedarme de 3 a 5 años? 

#### **Comportamiento esperado con la planificación:** 

- El modelo considera ambas opciones de forma sistemática. 

- Considera las implicaciones financieras (pago inicial, costos mensuales, capital y costo de oportunidad). 

- Analiza factores específicos del mercado (precios de las viviendas en San Francisco, control de alquileres y apreciación). 

- Evalúa el impacto en el plazo de 3 a 5 años. 

- 

- Proporciona recomendaciones adaptadas al contexto junto con situaciones hipotéticas. 

#### **Qué debes tener en cuenta:** 

- El proceso de pensamiento es visible cuando se utiliza include_thoughts=True . 

- Con la planificación, los problemas complejos se analizan de forma estructurada. 

- - Las preguntas sencillas siguen siendo eficientes incluso cuando la planificación está habilitada. 

- El presupuesto limita la profundidad de pensamiento (2,048 tokens = análisis exhaustivo). 

# **Conclusiones principales** 

- El parámetro **planner** (singular) habilita el razonamiento de varios pasos. 

- **BuiltInPlanner** aprovecha las capacidades de pensamiento integradas de Gemini. 

- **ThinkingConfig** controla el presupuesto y la visibilidad del pensamiento. 

- **include_thoughts=True** muestra el razonamiento interno (ideal para la depuración). 

- - **thinking_budget** asigna tokens de pensamiento (aparte de los de respuesta). 

- **Utiliza la planificación para tareas complejas** y omítela para consultas simples. 

- **Importa desde google.adk.planners** y **google.genai types** . 

