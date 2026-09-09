# **Introducción: De la configuración predeterminada a la configuración optimizada** 

En los módulos anteriores, utilizaste la configuración predeterminada del modelo: 

# Visto en los módulos 1 y 2 agent = LlmAgent( model="gemini-2.5-flash", instruction="…" ) 

Esto funciona, pero utiliza la configuración predeterminada para todo: 

- ❌ No hay control sobre la creatividad frente a la coherencia. 

   - ❌ No hay umbrales de seguridad configurados. 

- 

   - ❌ No hay límites de tokens establecidos. 

- 

   - ❌ Se utiliza la misma configuración para todas las tareas (escritura creativa frente a extracción de datos). 

- 

En este módulo, aprenderemos cómo configurar modelos para requisitos específicos con la función generate_content_config del ADK. 

# **El problema: No hay una solución universal** 

El uso de la configuración predeterminada o de un modelo incorrecto desperdicia recursos o sacrifica la calidad: 

# Problema 1: Modelo costoso para tareas sencillas greeting_agent = LlmAgent( model="gemini-2.5-pro", # ¡Es excesivo! Cuesta 10 veces más que Flash instruction="Saluda cordialmente al usuario" ) 

# Problema 2: Temperatura incorrecta para la tarea factual_agent = LlmAgent( model="gemini-2.5-flash", instruction="Extrae fechas exactas de los documentos" 

# No se configuró la temperatura, por lo que se usa el valor predeterminado 1.0 (alta creatividad o aleatoriedad) 

# Para tareas fácticas, se recomienda una temperatura cercana a 0 ) 

# Problema 3: No hay una configuración de seguridad personalizada public_agent = LlmAgent( model="gemini-2.5-flash", instruction="Responde las preguntas de los clientes" 

# Utiliza la configuración de seguridad predeterminada, que puede no satisfacer las necesidades específicas de cumplimiento ) 

**El problema principal:** Sin una configuración estratégica, los agentes desperdician dinero, producen resultados incoherentes o no satisfacen los requisitos específicos de seguridad y cumplimiento. 

