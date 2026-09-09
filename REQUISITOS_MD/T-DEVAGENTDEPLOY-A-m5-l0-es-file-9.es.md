



# de lectura 



## ¡Felicitaciones! 

Completaste el curso 9: Implementa tu primer agente. 

Tus agentes ahora están listos para producción y se puede acceder a ellos las 24 horas, todos los días, desde cualquier parte del mundo. 

## Qué aprendiste 

### Parte 1: Información sobre la implementación 

- Implementación local vs. en la nube 

- Configuración de Google Cloud (cuenta, APIs, facturación) 

- Cuándo implementar agentes en producción 





1 

### Parte 2: Implementación del agente en Agent Engine 

- 1 Implementación con un solo comando: adk dep ~~l~~ oy agen ~~t-~~ eng ~~i~~ ne 

   - Persistencia automática de la sesión (VertexAiSessionService) 

   - Prueba con el SDK de Python 

   - Shell adk dep ~~l~~ oy agen ~~t-~~ eng ~~i~~ ne \ ~~--~~ p ~~r~~ o ~~j~~ ec ~~t=~~ $PROJ ~~E~~ C ~~T~~ \ ~~--r~~ eg ~~i~~ on ~~=~~ $R ~~E~~ G ~~I~~ ON \ 

   - ~~--~~ s ~~t~~ ag ~~i~~ ng_bucke ~~t=~~ $BUCK ~~ET~~ \ ~~--~~ d ~~i~~ sp ~~l~~ ay_name ~~=~~ "M ~~i~~ agen ~~t~~ e" \ 

   - /pa ~~t~~ h/ ~~t~~ o/agen ~~t~~ 

### Parte 3: Memoria de producción 

- 1 Estado de la sesión vs. Memory Bank Cuándo necesitas el aprendizaje en todas las sesiones 

   - Memory Bank para la personalización a largo plazo 

Ninguno ~~E~~ s ~~t~~ ado de ~~l~~ a ses ~~i~~ ón: "¿Qué sucede en ~~E~~ S ~~T~~ A conve ~~r~~ sac ~~i~~ ón?" Memo ~~r~~ y Bank:         "¿Qué ap ~~r~~ end ~~í E~~ N ~~T~~ ODAS ~~l~~ as conve ~~r~~ sac ~~i~~ ones?" 



### Parte 4: Implementación en Cloud Run 

- 1 Opción de implementación alternativa 

IU web con la marca ~~--~~ w ~~it~~ h_u ~~i~~ 

Cuándo usar Cloud Run en lugar de Agent Engine 

Shell 

adk dep ~~l~~ oy c ~~l~~ oud_ ~~r~~ un \ ~~--~~ p ~~r~~ o ~~j~~ ec ~~t=~~ $PROJ ~~E~~ C ~~T~~ \ ~~--r~~ eg ~~i~~ on ~~=~~ $R ~~E~~ G ~~I~~ ON \ ~~--~~ se ~~r~~ v ~~i~~ ce_name ~~=~~ my ~~-~~ agen ~~t~~ \ 

- ~~--~~ w ~~it~~ h_u ~~i~~ \ 



- /pa ~~t~~ h/ ~~t~~ o/agen ~~t~~ 





2 

## Resumen 

### Opciones de implementación 

|Plataforma|Ideal para|Beneficio clave|
|---|---|---|
|Agent Engine|Agentes estándar del ADK|Opción más sencilla (un solo<br>comando)|
|Cloud Run<br>pciones de me|Necesidades personalizadas<br>moria|Flexibilidad(IU web)|
|Tipo|Alcance|Caso de uso|
|Estado de la sesión|Conversación actual|Seguimiento de solicitudesy flujo|
|Memory Bank|Todas las conversaciones|Preferencias ehistorial|



### Opciones de memoria 

### Puntos clave que debes recordar 

Usa Agent Engine como opción predeterminada para simplificar el proceso. 

- Usa Cloud Run cuando necesites una IU web o contenedores personalizados. 

- El estado de la sesión junto con Memory Bank ofrecen una arquitectura de memoria completa. 

- Todos los espacios de nombres del curso 4 funcionan en producción. 

## Tu proceso completo 

Ninguno Cu ~~r~~ sos de ~~l 1~~ a ~~l~~ 3:  C ~~r~~ eac ~~i~~ ón de agen ~~t~~ es (mode ~~l~~ os, he ~~rr~~ am ~~i~~ en ~~t~~ as e ~~i~~ ns ~~tr~~ ucc ~~i~~ ones) Cu ~~r~~ sos de ~~l~~ 4 a ~~l~~ 6:  Ad ~~i~~ c ~~i~~ ón de capac ~~i~~ dades (es ~~t~~ ado, he ~~rr~~ am ~~i~~ en ~~t~~ as, 

- p ~~r~~ o ~~t~~ ecc ~~i~~ ones) Cu ~~r~~ sos de ~~l~~ 7 a ~~l~~ 8:  Coo ~~r~~ d ~~i~~ nac ~~i~~ ón de ~~fl~~ u ~~j~~ os de ~~tr~~ aba ~~j~~ o (mu ~~lti~~ agen ~~t~~ e, o ~~r~~ gan ~~i~~ zac ~~i~~ ón) Cu ~~r~~ so 9: ~~I~~ MPL ~~E~~ M ~~E~~ N ~~T~~ AC ~~I~~ ÓN D ~~E~~ L AG ~~E~~ N ~~TE E~~ N PRODUCC ~~I~~ ÓN ✓ 

3 

## Recursos 

### Referencias principales 

- 📚 Documentación del ADK: Información completa sobre el ADK 

- 📖 Implementación en Agent Engine: Implementación en Vertex AI Agent Engine 

- 📖 Implementación en Cloud Run: Implementación en Cloud Run 

- 📚 Descripción general de Memory Bank: Memoria entre sesiones 

- 🔗 Nivel gratuito de Google Cloud: $300 de crédito para el aprendizaje 



### De la comunidad 

- 🧪 <u>Cómo implementar, administrar y observar el agente de ADK en Cloud Run: Codelab interactivo</u> con funciones de observabilidad (parte 4) 

- 📚 <u>Implementación de agentes de IA en la empresa con el ADK: Patrones de</u> implementación y prácticas recomendadas para empresas (partes 2 y 4) 

- 📚 <u>Agent Development Kit</u> ~~-~~ <u>Easy to Build Multi</u> ~~-~~ <u>Agent Applications: Anuncio oficial de Google</u> con descripción general de la implementación (parte 1) 

- 📺 Cómo comenzar a usar el ADK: Videotutorial que muestra el flujo de trabajo de implementación (parte 2) 

- 🤖 <u>google/adk</u> ~~-~~ <u>samples: Agentes de muestra</u> oficiales con configuraciones de implementación listas para producción (todas las partes) 

### ¡Felicitaciones por completar la ruta de aprendizaje del ADK! 



4 

