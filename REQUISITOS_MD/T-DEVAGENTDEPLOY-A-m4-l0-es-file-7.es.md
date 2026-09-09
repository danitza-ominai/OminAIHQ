

# Implementación en Cloud Run 

## Introducción 

### Cloud Run vs. Agent Engine 

En la parte 2, realizaste la implementación en Agent Engine, la ruta más sencilla para los agentes del ADK. En esta parte, se muestra a Cloud Run como alternativa. 

|Factor|Agent Engine|Cloud Run|
|---|---|---|
|Facilidad de uso|La más alta (un solo comando)|Moderada|
|Servicio de sesión|Automático|Configuración manual|
|IU web|Solo en la consola de Cloud|Puede incluir IU web|
|Ideal para|Agentes estándar del ADK|Necesidades personalizadas,<br>implementación de una IU|



Regla para tomar una decisión: Usa Agent Engine como opción predeterminada. Usa Cloud Run cuando necesites lo siguiente: 

Implementación de IU web con el agente ( ~~--~~ w ~~it~~ h_u ~~i~~ ) 

Configuración de un contenedor personalizado 

Infraestructura de Cloud Run existente 





## Implementación en Cloud Run 

### Implementación básica 

Shell 

adk dep ~~l~~ oy c ~~l~~ oud_ ~~r~~ un \ 

- ~~--~~ p ~~r~~ o ~~j~~ ec ~~t=~~ $GOOGL ~~E~~ <u>_CLOUD_PROJ</u> ~~E~~ C ~~T~~ \ 

- ~~--r~~ eg ~~i~~ on ~~=~~ $GOOGL ~~E~~ <u>_CLOUD_LOCA</u> ~~TI~~ ON \ 

- ~~--~~ se ~~r~~ v ~~i~~ ce_name ~~=~~ my ~~-~~ agen ~~t~~ \ 

- ~~--~~ w ~~it~~ h_u ~~i~~ \ 

- /pa ~~t~~ h/ ~~t~~ o/agen ~~t~~ 

#### Parámetros: 

- ~~-p~~ r ~~o~~ j ~~e~~ ct : Tu proyecto de Google Cloud 



- ~~--r~~ eg ~~i~~ on: Región de implementación (p. ej., us ~~-~~ central1) 

- ~~--~~ se ~~r~~ v ~~i~~ ce_name: Nombre del servicio de Cloud Run 

- ~~--~~ w ~~it~~ h_u ~~i~~ : Para incluir la interfaz web (opcional, pero recomendado) 

- /pa ~~t~~ h/ ~~t~~ o/agen ~~t~~ : El directorio de tu agente 

### Qué ocurre 



- 1 El ADK empaqueta el código de tu agente. 

- 2 Se genera la imagen de contenedor. 

- 3 El agente se implementa en Cloud Run. 

- 4 Se devuelve la URL pública. 

Tiempo de implementación: De 5 a 8 minutos aprox. 







2 

