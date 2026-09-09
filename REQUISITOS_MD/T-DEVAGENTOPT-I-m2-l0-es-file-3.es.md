# **Introducción: Del texto a los datos estructurados** 

En el módulo 1 del curso 2, tus agentes devolvieron texto en formato libre: 

# Visto en módulos anteriores agent = LlmAgent( model="gemini-2.5-flash", instruction="Extrae información del producto de los mensajes del usuario" ) 

# Usuario: "Quiero el iPhone 15 Pro con 256 GB" 

# Respuesta del agente: "El usuario está interesado en un iPhone 15 Pro con almacenamiento de 256 GB." 

Esto funciona para los lectores humanos, pero causa problemas para los sistemas: 

- ❌ Formato no garantizado: Las respuestas varían cada vez. 

   - ❌ Difícil de analizar: El procesamiento de texto es propenso a errores. 

- 

   - ❌ Falta de validación: Los campos faltantes pasan desapercibidos. 

- 

   - ❌ Integración compleja: Las bases de datos necesitan una estructura coherente. 

- 

En este módulo, utilizaremos output_schema del ADK para garantizar respuestas JSON estructuradas en las que los sistemas puedan confiar. 

# **El problema: Los resultados impredecibles interrumpen las integraciones** 

Sin un resultado estructurado, incluso las buenas instrucciones producen resultados inconsistentes: 

# Sin esquema de salida: formato impredecible text_agent = LlmAgent( model="gemini-2.5-flash", instruction="Extrae el nombre del producto, el precio y el almacenamiento del mensaje del usuario" ) 

# ¿Qué ocurre? # Usuario: "Quiero un iPhone 15 Pro de 256 GB por USD 999" 

# Respuesta 1: "Producto: iPhone 15 Pro; precio: USD 999; almacenamiento: 256 GB" # Respuesta 2: "El iPhone 15 Pro cuesta USD 999 y tiene un almacenamiento de 256 GB" # Respuesta 3: "iPhone 15 Pro con 256 GB por USD 999" 

**El problema raíz:** Tu aplicación no puede analizar de manera confiable estos formatos variables. Necesitas una estructura JSON garantizada. 

