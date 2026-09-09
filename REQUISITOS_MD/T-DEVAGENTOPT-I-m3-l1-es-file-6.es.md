# **La solución: Configuración estratégica del modelo** 

## **Comprende la selección de modelos** 

_Referencia:_ _<u>Documentación del modelo de Gemini</u>_ 

_Referencia:_ _<u>Precios de Vertex AI</u>_ 

_Referencia:_ _<u>Modelos de Vertex AI</u>_ 

### **Regla general para la selección de modelos:** 

- **Comienza con Gemini 2.5 Pro** para crear prototipos y establecer modelos de referencia de calidad. 

   - Excelente razonamiento para análisis complejos y tareas esenciales para la calidad 

   - Ventana de contexto de 2 millones de tokens para entradas más grandes 

   - Ideal para desarrollo inicial y evaluación 

- **Realiza optimizaciones con Gemini 2.5 Flash** cuando el costo y la velocidad sean prioridades. 

   - Tiempos de respuesta aproximadamente 2 veces más rápidos 

   - Unas 10 veces más económico que Pro 

   - Ventana de contexto de 1 millón de tokens 

   - Buen razonamiento para la mayoría de las tareas sencillas 

   - Ideal para cargas de trabajo de producción de gran volumen 

- **Analiza las brechas** después de cambiar de Pro a Flash para asegurarte de que Flash cumpla con tus requisitos de calidad. 

# **Conceptos básicos** 

## **1. Configuración con GenerateContentConfig** 

_Referencia:_ _<u>Documentación del ADK sobre la configuración de la generación del LLM</u>_ 

La documentación del ADK brinda la siguiente información: 

- " **generate_content_config (opcional):** Pasa una instancia de <u>google.genai.types.GenerateContentConfig</u> para controlar parámetros como temperature (aleatoriedad), max_output_tokens (longitud de la respuesta), top_p , top_k y la configuración de seguridad". 

from google.genai import types 

agent = LlmAgent( model="gemini-2.5-flash", generate_content_config=types.GenerateContentConfig( temperature=0.2, # Resultado más determinístico max_output_tokens=250, # Limita la longitud de la respuesta top_p=0.8, # Muestreo de núcleo top_k=10 # Muestreo de Top-K ) ) 

## **2. Temperatura: Creatividad frente a coherencia** 

_Referencia:_ _<u>Documentación del ADK sobre la configuración de la generación del LLM</u>_ 

La temperatura controla la aleatoriedad en el resultado del modelo: 

### **Temperatura baja (de 0.0 a 0.3) o determinística:** 

factual_config = types.GenerateContentConfig( temperature=0.1 # Muy coherente y predecible ) 

# Utiliza esta configuración para la extracción de datos, preguntas y respuestas fácticas, y resultados estructurados 

### **Temperatura media (de 0.4 a 0.7) o equilibrada:** 

balanced_config = types.GenerateContentConfig( temperature=0.7 # Equilibrio entre creatividad y coherencia ) 

# Utiliza esta configuración para atención al cliente, tutorías y conversaciones generales 

### **Temperatura alta (de 0.8 a 1.0) o creativa:** 

creative_config = types.GenerateContentConfig( temperature=0.9 # Respuestas más creativas y variadas ) 

# Utiliza esta configuración para escritura creativa, generación de ideas y textos de marketing 

## **3. Configuración de seguridad** 

_Referencia:_ _<u>Ejemplo de configuración de seguridad obtenido de la documentación del ADK</u>_ 

_Referencia:_ _<u>Configuración de seguridad de Gemini</u>_ 

### Configura los umbrales de filtrado de contenido para los modelos de Gemini: 

from google.genai import types 

# Seguridad estricta para agentes que interactúan con el público strict_config = types.GenerateContentConfig( safety_settings=[ types.SafetySetting( category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE ), types.SafetySetting( category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE ), types.SafetySetting( category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE ), types.SafetySetting( category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE ) ] ) 

### **Umbrales de seguridad:** 

- BLOCK_NONE : Sin filtrado (no se recomienda para producción) 

- BLOCK_ONLY_HIGH : Bloquea solo el contenido con alta probabilidad de ser dañino 

- BLOCK_MEDIUM_AND_ABOVE : Bloquea el contenido con probabilidad alta y media de ser dañino 

- BLOCK_LOW_AND_ABOVE : Es el más estricto, ya que bloquea incluso el contenido con baja probabilidad de ser dañino 

**Nota:** Para los modelos que no sean de Gemini (p. ej., Claude o GPT), consulta la documentación del proveedor del modelo específico para conocer las opciones de configuración de seguridad, ya que la API y los parámetros difieren de la configuración de seguridad de Gemini. 

## **4. Tokens de salida y muestreo** 

_Referencia:_ _<u>Documentación del ADK sobre la configuración de la generación del LLM</u>_ 

Controla la longitud y la diversidad de las respuestas: 

- comprehensive_config = types.GenerateContentConfig( 

- temperature=0.7, 

- max_output_tokens=2000, # Permite respuestas más largas 

top_p=0.95, # Considera el 95% superior de la masa de probabilidad top_k=40 # Considera los 40 tokens principales en cada paso ) 

concise_config = types.GenerateContentConfig( temperature=0.3, max_output_tokens=100, # Obliga a dar respuestas breves top_p=0.8, # Muestreo más enfocado top_k=10 # Menos opciones de tokens ) 

### **Explicación de los parámetros:** 

- **max_output_tokens** : Longitud máxima de respuesta (el valor predeterminado varía según el modelo) 

- **top_p** : Muestreo de núcleo, que considera los tokens que corresponden al porcentaje P más alto de probabilidad 

- **top_k** : Muestreo exclusivo de los próximos K tokens con más probabilidad 

# 🧪 **Ejemplo práctico** 

Creemos dos agentes optimizados para diferentes tareas: uno para la extracción de datos fácticos y otro para la generación de ideas creativas. 

## **Paso 1: Crea el proyecto** 

adk create model_comparison cd model_comparison 

## **Paso 2: Escribe el código de agentes optimizados** 

Reemplaza el contenido de agent.py por lo siguiente: 

""" 

Demostración de configuración de modelos que muestra la optimización fáctica frente a la optimización creativa. Demuestra generate_content_config del ADK con diferente configuración. """ 

from google.adk.agents import LlmAgent from google.genai import types 

# Agente 1: Optimizado para la extracción de datos fácticos # Utiliza una temperatura baja para una mayor coherencia y seguridad estricta en pos de la exactitud 

factual_agent = LlmAgent( 

model="gemini-2.5-flash", # Flash es suficiente para la extracción name="data_extractor", description="Extrae información fáctica de forma sumamente coherente", 

instruction="""Eres un extractor de datos precisos. 

Extrae hechos exactamente como se indica. No hagas lo siguiente: - Agregar información que no figure en la entrada - Hacer suposiciones o inferencias - Usar lenguaje creativo Sé preciso, conciso y determinístico.""", generate_content_config=types.GenerateContentConfig( temperature=0.1, # Muy baja para mantener la coherencia max_output_tokens=500, top_p=0.8, top_k=10, safety_settings=[ types.SafetySetting( category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE ) ] ) ) 

# Agente 2: Optimizado para la generación de ideas creativas # Utiliza una temperatura alta para promover la creatividad y el modelo Pro para generar mejores ideas creative_agent = LlmAgent( model="gemini-2.5-pro", # Pro para creatividad superior name="creative_brainstormer", description="Genera ideas creativas y explora posibilidades", instruction="""Eres un socio de generación de ideas creativo. 

Genera ideas innovadoras, diversas y originales. Puedes hacer lo siguiente: - Pensar de forma creativa 

- Combinar conceptos inesperados 

- Explorar enfoques no convencionales 

Sé creativo, ofrece distintas opciones y fomenta la reflexión.""", generate_content_config=types.GenerateContentConfig( temperature=0.9, # Alta para una mayor creatividad max_output_tokens=2000, # Permite ideas detalladas top_p=0.95, top_k=40, safety_settings=[ types.SafetySetting( category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE ) ] ) ) 

# Para el ADK web, utilizaremos el agente fáctico como agente raíz # Cambia a creative_agent para probar un comportamiento diferente root_agent = factual_agent 

## **Paso 3: Ejecuta y compara** 

adk web 

### **Haz la prueba con un agente fáctico:** 

### Prueba esta instrucción: 

Extrae información clave: "El iPhone 15 Pro se lanzó en septiembre de 2023 y tiene un precio inicial de USD 999 para el modelo de 128 GB". 

### **Comportamiento esperado:** 

- Respuesta coherente y fáctica en todo momento 

- Extracción exacta de lo que se indica 

- Sin interpretación creativa 

- Mismo formato en instrucciones repetidas 

### **Haz la prueba con un agente creativo:** 

Cambia a root_agent = creative_agent en el código, reinicia y prueba lo siguiente: 

Propón 5 funciones innovadoras para un smartphone de nueva generación. 

### **Comportamiento esperado:** 

- Ideas variadas y creativas 

- Diferentes respuestas cada vez 

- Sugerencias imaginativas 

- Elaboración rica y detallada 

### **Qué debes tener en cuenta:** 

- **Impacto de la temperatura** : Baja (0.1) para una mayor coherencia y alta (0.9) para una mayor creatividad 

- **Elección del modelo:** Pro para un modelo de referencia de calidad y creatividad compleja, y Flash para la optimización de costos 

- **Límites de tokens:** 500 para el agente fáctico y 2,000 para el agente creativo 

- **Niveles de seguridad** : Más estrictos para el agente fáctico y equilibrados para el agente creativo 

# **Conclusiones principales** 

- **Selección de modelos:** Comienza con Pro para crear prototipos y modelos de referencia de calidad, y optimiza con Flash para reducir costos y mejorar la velocidad 

- **Temperatura** : 0.0-0.3 (fáctica), 0.4-0.7 (equilibrada), 0.8-1.0 (creativa) 

- **Realiza la importación desde google.genai** : from google.genai import types 

- - **GenerateContentConfig** : Configura la temperatura, los tokens, el muestreo y la seguridad 

- **Umbrales de seguridad** : BLOCK_LOW_AND_ABOVE (estricto) a BLOCK_ONLY_HIGH (flexible) 

- - **Realiza optimizaciones en función de la tarea** : Configura los parámetros según el caso de uso y evita recurrir a una solución universal 

