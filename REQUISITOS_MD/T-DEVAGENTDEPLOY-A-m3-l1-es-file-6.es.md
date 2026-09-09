

# Cuándo necesitas **Memory Bank** 

### Casos de uso adecuados 

- Agentes del servicio de atención al cliente (recuerdan problemas pasados) 

- Asistentes personales (recuerdan preferencias) 

- Sistemas de aprendizaje (recuerdan lo que aprendió el usuario) 

- Personalización (recuerdan intereses) 

Cuándo el estado de la sesión es suficiente 

- Agentes de preguntas y respuestas simples (no se necesita memoria) 

- Agentes enfocados en tareas (las completan y las olvidan) 

- Interacciones breves (un solo propósito) 

## Recursos para obtener más información 

Cuando tengas todo listo para implementar Memory Bank, consulta estos recursos: 

### Documentación oficial 

- Descripción general de Memory Bank: https://cloud.google.com/vertex ~~-~~ <u>ai/ generative</u> ~~-~~ <u>ai/docs/agent</u> ~~-~~ <u>engine/memory</u> ~~-~~ <u>bank/overview</u> 



<!-- Start of picture text -->
tps://google.github.io/adk<br><!-- End of picture text -->

- Documentación del ADK: <u>https://google.github.io/adk</u> ~~-~~ <u>docs/</u> 

### Detalles de la implementación 

Temas que abarca la documentación del ADK: 

- Configuración de VertexAiMemoryBankService 

- Devoluciones de llamada de transferencia de memoria 

- Uso de PreloadMemoryTool 

- Modo Exprés para pruebas 

## Conclusiones principales 

Ahora entiendes cómo Memory Bank complementa el estado de la sesión para crear una arquitectura de memoria completa. Mientras que el estado de la sesión se encarga de la conversación actual, Memory Bank permite que los agentes aprendan y recuerden durante todas las interacciones, una capacidad clave para la personalización y la participación del usuario a largo plazo. 

### Estado de la sesión vs. Memory Bank 

- Estado de la sesión: Conversación actual (curso 4) 

- Memory Bank: Aprendizaje en todas las sesiones (curso 9) 



- En conjunto: Arquitectura de memoria completa 

### Características básicas de Memory Bank 

- Extracción potenciada por LLM (inteligente, no sin procesar) 

- Búsqueda semántica (comprende la intención) 

- Servicio administrado (no requiere configuración) 

### Cuándo usar cada opción 

|Necesidad|Solución|
|---|---|
|Contexto de la conversación|Estado de la sesión|
|Aprendizaje en todas las sesiones|Memory Bank|
|Ambas opciones|Usarlas en conjunto|





2 

