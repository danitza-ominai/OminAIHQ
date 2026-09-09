# **Introducción** 

## **De las herramientas personalizadas a las capacidades integradas** 

**Tu recorrido:** 

- **Parte 1:** Comprendiste las herramientas a nivel fundamental y creaste herramientas de funciones personalizadas. 

- **Parte 2:** Usas las herramientas listas para producción que proporciona el ADK. 

**El cambio:** En lugar de escribir código de implementación, importas y usas herramientas prediseñadas que ADK mantiene. 

# **El problema** 

## **Cómo reinventar las capacidades comunes** 

Supongamos que quieres agregar la búsqueda web a tu agente de la parte 1: 

# ¿Cómo implementarías la búsqueda web? def search_web(query: str) -> dict: """Busca información en la Web.""" 

- # ¿Cómo implementamos esto en realidad? 

- # - Se necesita llamar a una API de búsqueda (¿cuál?, ¿cómo autenticarse?). 

- # - Analiza y formatea resultados para que el LLM pueda consumirlos. 

- # - Maneja límites de frecuencia y errores. 

- # - Mantén la integración de la API actualizada. 

- # - Optimiza los resultados para el LLM. 

- # ¡Esto es complejo! pass 

### **Problemas con crearlo todo por tu cuenta:** 

- ❌ **Implementación compleja** : integración de API, autenticación y manejo de errores 

- - ❌ **Carga de mantenimiento** : cambios en la API, actualizaciones y bajas - ❌ **No optimizado** : los resultados deben formatearse para el consumo del LLM - ❌ **Funciones de producción faltantes** : límite de frecuencia, almacenamiento en caché y supervisión 

- ❌ **Consume mucho tiempo** : horas o días para crear lo que debería llevar minutos 

**El problema raíz:** Las capacidades comunes, como la búsqueda web y la ejecución de código, requieren un esfuerzo de ingeniería significativo para su correcta implementación. 

