

# La solución: Opciones de implementación del ADK 



El ADK proporciona dos plataformas de implementación para que se pueda acceder a tus agentes en línea: 

1. Vertex AI Agent Engine 

De la documentación del ADK: 

"Agent Engine es un servicio completamente administrado de Google Cloud que les permite a los desarrolladores implementar, administrar y escalar agentes de IA en producción. Se encarga de la infraestructura para escalar a los agentes en producción, de modo que los desarrolladores puedan enfocarse en crear aplicaciones inteligentes". 

#### Características clave: 

- Implementación con un solo comando: adk dep ~~l~~ oy agen ~~t-~~ eng ~~i~~ ne 

- Completamente administrado: Google se encarga de la infraestructura, el escalamiento y la persistencia 

- Nativo del ADK: Creado específicamente para agentes del ADK 

- Servicio de sesión automático: VertexAiSessionService se configura automáticamente 

Exclusivo para Python: Admite agentes de Python 

Referencia: Documentación del ADK: Agent Engine | Documentación <u>del ADK: Cloud Run</u> 

#### Comando de implementación: 

Shell 

adk dep ~~l~~ oy agen ~~t-~~ eng ~~i~~ ne \ 

~~--~~ p ~~r~~ o ~~j~~ ec ~~t=~~ my ~~-~~ gcp ~~-~~ p ~~r~~ o ~~j~~ ec ~~t~~ \ 

~~--r~~ eg ~~i~~ on ~~=~~ us ~~-~~ cen ~~tr~~ a ~~l1~~ \ 

- ~~--~~ s ~~t~~ ag ~~i~~ ng_bucke ~~t=~~ gs://my ~~-~~ bucke ~~t~~ \ 



- ~~--~~ d ~~i~~ sp ~~l~~ ay_name ~~=~~ "M ~~i~~ agen ~~t~~ e" \ 

- /pa ~~t~~ h/ ~~t~~ o/agen ~~t~~ 

Qué obtienes: 

Extremo público (accesible a nivel global) 

- Disponibilidad 24/7 

- Escalado automático 

Estado de sesión persistente (VertexAiSessionService) 

- Compatibilidad con Memory Bank 

- Infraestructura administrada 

### 2. Cloud Run 

#### De la documentación del ADK: 

"Cloud Run es una plataforma completamente administrada que permite ejecutar código en la infraestructura escalable de Google. Admite agentes de Python, Go y Java". 

#### Características clave: 

- Contenedores sin servidores: Generación automática de contenedores 

- Compatibilidad con diferentes lenguajes: Python, Go y Java 

- Opción de IU web: Implementación de una interfaz interactiva con la 

- marca ~~--~~ w ~~it~~ h_u ~~i~~ 

- Flexible: Contenedores personalizados y control detallado 

- Pago por uso: Cobro solo cuando el agente está en ejecución 

2 

#### Comando de implementación: 

Shell 

adk dep ~~l~~ oy c ~~l~~ oud_ ~~r~~ un \ 

- ~~--~~ p ~~r~~ o ~~j~~ ec ~~t=~~ my ~~-~~ gcp ~~-~~ p ~~r~~ o ~~j~~ ec ~~t~~ \ 

- ~~--r~~ eg ~~i~~ on ~~=~~ us ~~-~~ cen ~~tr~~ a ~~l1~~ \ ~~--~~ se ~~r~~ v ~~i~~ ce_name ~~=~~ my ~~-~~ agen ~~t~~ \ 

- ~~--~~ w ~~it~~ h_u ~~i~~ \ 

- /pa ~~t~~ h/ ~~t~~ o/agen ~~t~~ 

Qué obtienes: 

URL HTTPS pública (p. ej., https://my ~~-~~ <u>agent</u> ~~-~~ <u>xyz.us</u> ~~-~~ <u>central1.run.app)</u> 

- Disponibilidad 24/7 

- Escalado automático 

IU web (con la marca ~~--~~ w ~~it~~ h_u ~~i~~ ) 

- API de REST para acceso programático 

Compatibilidad con diferentes lenguajes 

## Conceptos básicos 









### 1. Ejecución local vs. en la nube 

Desarrollo local (cursos del 1 al 8): 

Py ~~t~~ hon 

~~# Ej~~ ecuc ~~i~~ ón ~~l~~ oca ~~l~~ 

~~# T~~ e ~~r~~ m ~~i~~ na ~~l~~ : adk web 

~~#~~ Acceso: h ~~tt~~ p:// ~~l~~ oca ~~l~~ hos ~~t~~ :8000 

~~#~~ Ca ~~r~~ ac ~~t~~ e ~~rí~~ s ~~ti~~ cas: 

~~# -~~ Se e ~~j~~ ecu ~~t~~ a en ~~t~~ u compu ~~t~~ ado ~~r~~ a 

- ~~# -~~ Requ ~~i~~ e ~~r~~ e que ~~l~~ a ~~t~~ e ~~r~~ m ~~i~~ na ~~l~~ es ~~t~~ é ab ~~i~~ e ~~rt~~ a 

~~# -~~ So ~~l~~ o ~~t~~ ú puedes accede ~~r~~ a é ~~l~~ 

- ~~# -~~ Se de ~~ti~~ ene cuando ~~l~~ a compu ~~t~~ ado ~~r~~ a en ~~tr~~ a en suspens ~~i~~ ón ~~# - I~~ nMemo ~~r~~ ySess ~~i~~ onSe ~~r~~ v ~~i~~ ce (s ~~i~~ n pe ~~r~~ s ~~i~~ s ~~t~~ enc ~~i~~ a) 

- ~~# - I~~ dea ~~l~~ pa ~~r~~ a e ~~l~~ desa ~~rr~~ o ~~ll~~ o y ~~l~~ as p ~~r~~ uebas 

3 

#### Implementación en la nube (curso 9): 

##### Py ~~t~~ hon 

- ~~# I~~ mp ~~l~~ emen ~~t~~ ac ~~i~~ ón en Agen ~~t E~~ ng ~~i~~ ne o C ~~l~~ oud Run 

- ~~# T~~ e ~~r~~ m ~~i~~ na ~~l~~ : adk dep ~~l~~ oy agen ~~t-~~ eng ~~i~~ ne ~~--~~ p ~~r~~ o ~~j~~ ec ~~t=~~ my ~~-~~ p ~~r~~ o ~~j~~ ec ~~t~~ ... ~~#~~ Acceso: h ~~tt~~ ps://agen ~~t-~~ xyz. ~~r~~ un.app (URL púb ~~li~~ ca) 

- ~~#~~ Ca ~~r~~ ac ~~t~~ e ~~rí~~ s ~~ti~~ cas: 

- ~~# -~~ Se e ~~j~~ ecu ~~t~~ a en ~~l~~ a ~~i~~ n ~~fr~~ aes ~~tr~~ uc ~~t~~ u ~~r~~ a de Goog ~~l~~ e C ~~l~~ oud ~~# -~~ S ~~i~~ emp ~~r~~ e d ~~i~~ spon ~~i~~ b ~~l~~ e (24/7) 

- ~~# -~~ Acces ~~i~~ b ~~l~~ e pa ~~r~~ a cua ~~l~~ qu ~~i~~ e ~~r~~ pe ~~r~~ sona con ~~l~~ a URL 

- ~~# - E~~ sca ~~l~~ ado au ~~t~~ omá ~~ti~~ co 

- ~~# -~~ Ve ~~rt~~ exA ~~i~~ Sess ~~i~~ onSe ~~r~~ v ~~i~~ ce (pe ~~r~~ s ~~i~~ s ~~t~~ en ~~t~~ e) 

- ~~# -~~ L ~~i~~ s ~~t~~ o pa ~~r~~ a p ~~r~~ oducc ~~i~~ ón 

### Comparación: 

|Factor|Local (cursos del 1 al 8)|En la nube (curso 9)|
|---|---|---|
|Acceso|http://localhost:8000(solo en tu máquina)|https://agent~~-~~xyz.run.app(global)|
|Disponibilidad|Solo cuando la terminal está en ejecución|Automática 24/7|
|Uso compartido|No se puede compartir|URL pública, se puede compartir|
|Escalamiento|Instancia única|Escalado automático|
|Persistencia de la<br>sesión|InMemorySessionService(sepierde<br>cuando se reinicia)|VertexAiSessionService<br>(persistente)|
|Caso de uso|Desarrolloypruebas|Producciónycolaboración<br>en equipo|



#### Cuándo implementar el agente: 

Uso compartido con el equipo o los usuarios 

Integración en aplicaciones de producción 

- Necesidad de disponibilidad 24/7 

- Escala más allá de la máquina local 

Desarrollo o experimentación inicial (usa adk web) 



2 

En el siguiente diagrama, se ilustra la diferencia fundamental entre el desarrollo local y la implementación en la nube en cuanto a accesibilidad y persistencia: 

Ninguno g ~~r~~ aph ~~T~~ B subg ~~r~~ aph "Desa ~~rr~~ o ~~ll~~ o ~~l~~ oca ~~l~~ (cu ~~r~~ sos de ~~l 1~~ a ~~l~~ 8)" LOCAL[ ~~T~~ u compu ~~t~~ ado ~~r~~ a] ~~--~~ > ADK_W ~~E~~ B[adk web] ADK_W ~~E~~ B ~~--~~ > LOCAL ~~H~~ OS ~~T~~ [h ~~tt~~ p:// ~~l~~ oca ~~l~~ hos ~~t~~ :8000] LOCAL ~~H~~ OS ~~T --~~ > YOU[So ~~l~~ o ~~t~~ ú puedes accede ~~r~~ a ~~l~~ agen ~~t~~ e] LOCAL ~~--~~ > M ~~E~~ MORY[ ~~I~~ nMemo ~~r~~ ySess ~~i~~ onSe ~~r~~ v ~~i~~ ce] M ~~E~~ MORY ~~--~~ > LOS ~~T~~ [Los da ~~t~~ os se p ~~i~~ e ~~r~~ den después de un ~~r~~ e ~~i~~ n ~~i~~ c ~~i~~ o] end subg ~~r~~ aph " ~~I~~ mp ~~l~~ emen ~~t~~ ac ~~i~~ ón en ~~l~~ a nube (cu ~~r~~ so 9)" CLOUD[Goog ~~l~~ e C ~~l~~ oud] ~~--~~ > AG ~~E~~ N ~~T~~ <u>_</u> ~~E~~ NG ~~I~~ N ~~E~~ [Agen ~~t E~~ ng ~~i~~ ne/C ~~l~~ oud Run] AG ~~E~~ N ~~T~~ <u>_</u> ~~E~~ NG ~~I~~ N ~~E --~~ > PUBL ~~I~~ C_URL[h ~~tt~~ ps://agen ~~t-~~ xyz. ~~r~~ un.app] PUBL ~~I~~ C_URL ~~--~~ > ANYON ~~E~~ [Cua ~~l~~ qu ~~i~~ e ~~r~~ pe ~~r~~ sona puede accede ~~r~~ a ~~l~~ agen ~~t~~ e] 

CLOUD ~~--~~ > V ~~E~~ R ~~TE~~ X_S ~~E~~ SS ~~I~~ ON[Ve ~~rt~~ exA ~~i~~ Sess ~~i~~ onSe ~~r~~ v ~~i~~ ce] V ~~E~~ R ~~TE~~ X_S ~~E~~ SS ~~I~~ ON ~~--~~ > P ~~E~~ RS ~~I~~ S ~~TE~~ N ~~T~~ [Los da ~~t~~ os pe ~~r~~ s ~~i~~ s ~~t~~ en] 

CLOUD ~~--~~ > M ~~E~~ MORY_BANK[Ve ~~rt~~ exA ~~i~~ Memo ~~r~~ yBankSe ~~r~~ v ~~i~~ ce] M ~~E~~ MORY_BANK ~~--~~ > CROSS_S ~~E~~ SS ~~I~~ ON[Ap ~~r~~ end ~~i~~ za ~~j~~ e en ~~t~~ odas ~~l~~ as ses ~~i~~ ones] end s ~~t~~ y ~~l~~ e LOCAL ~~fill~~ : ~~#ff~~ e ~~1~~ e ~~1~~ s ~~t~~ y ~~l~~ e CLOUD ~~fill~~ : ~~#~~ ee ~~ff~~ ee s ~~t~~ y ~~l~~ e LOCAL ~~H~~ OS ~~T fill~~ : ~~#ff~~ eb99 s ~~t~~ y ~~l~~ e PUBL ~~I~~ C_URL ~~fill~~ : ~~#~~ d4edda 

Desarrollo local vs. implementación en la nube: accesibilidad y persistencia 

### 2. Requisitos previos de Google Cloud 

Qué necesitas para la implementación: 

1. Cuenta de Google Cloud: 

   - Regístrate en https://cloud.google.com/free. 



Nivel gratuito: Obtienes $300 de crédito por 90 días. 

- Se requiere una tarjeta de crédito (sin cargos mientras no se actualice el nivel). 

Es ideal para el aprendizaje del curso 9. 



5 

#### 2. Proyecto de Google Cloud: 

- Es el contenedor lógico de tus agentes y recursos. 

- Se crea a través de la consola de Cloud o gc ~~l~~ oud CLI. 

- La facturación debe estar habilitada. 

#### 3. APIs requeridas: 

   - API de Vertex AI: Es necesaria para implementar Agent Engine. 

   - API de Cloud Run: Es necesaria para implementar Cloud Run. 

   - Se habilitan a través de la consola de Cloud o gcloud services enable. 

4. gcloud CLI: 

   - Es la herramienta de línea de comandos para Google Cloud. 

   - Descárgala en https://cloud.google.com/sdk/docs/install. 

   - Autentícate con gc ~~l~~ oud au ~~t~~ h ~~l~~ og ~~i~~ n. 

   - Establece el proyecto con gc ~~l~~ oud con ~~fi~~ g se ~~t~~ p ~~r~~ o ~~j~~ ec ~~t~~ PROJ ~~E~~ C ~~T~~ <u>_</u> ~~I~~ D. 

#### 5. SDK de Vertex AI: 

Shell 

p ~~i~~ p ~~i~~ ns ~~t~~ a ~~ll --~~ upg ~~r~~ ade goog ~~l~~ e ~~-~~ c ~~l~~ oud ~~-~~ a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m[adk,agen ~~t~~ <u>_eng</u> ~~i~~ nes]> ~~=1~~ . ~~111~~ 

Beneficios del nivel gratuito: 

- Crédito de $300 (dura 90 días) 

- Sin cargos automáticos después de que vence el crédito 

- Suficiente para el aprendizaje y las pruebas del curso 9 

- Opción de configurar alertas de facturación para mayor seguridad 



6 

### 3. Comparación de las opciones de implementación 

|Factor|Agent Engine|Cloud Run|
|---|---|---|
|Facilidad de uso|La más alta (nativo de ADK, un solo<br>comando)|Moderada (conceptos de<br>contenedores)|
|Lenguajes|Solo Python|Python, Go y Java|
|Servicio de sesión|VertexAiSessionService (automático)|Se necesita una configuración<br>manual|
|Memory Bank|Compatibilidad integrada|Funciona (necesita una instancia<br>de AgentEngine)|
|Conocimiento sobre<br>contenedores|Noson necesarios|Los conocimientosbásicos son<br>útiles|
|Implementación<br>de laIU|Soloen laconsolade Cloud|Puede incluir IU web (~~--~~w~~it~~h_u~~i~~)|
|Idealpara|Agentes estándar del ADK con Python|Contenedores personalizados,<br>varios lenguajes,IU web|
|Tiempo de<br>implementación|De 5a10 minutosaprox.|De 5a8 minutosaprox.|
|Costo|Precios de VertexAI|Precios de CloudRun (nivel gratuito<br>generoso)|



### Matriz de decisiones: 

#### Usa Vertex AI Agent Engine en los siguientes casos: 

|ertex AI Agent Engine en los siguientes casos:|Usa Cloud Run en los siguientes casos:|
|---|---|
|Cuando crees agentes estándar del ADK<br>con Python|Cuando necesitas compatibilidad con<br>varios lenguajes (Go, Java)|
|Cuando desees la implementación más<br>sencilla (un solo comando)|Cuando deseas implementar la IU web<br>con el agente (~~--~~w~~it~~h_u~~i~~)|
|Cuando necesites servicios automáticos<br>de sesión y memoria|Cuando requieras dependencias de<br>contenedores personalizados|
|Cuando no necesites un control<br>personalizado de contenedores|Cuando tengas una infraestructura<br>existente de Cloud Run|
|Cuando prefieras una infraestructura<br>completamente administrada|Cuando necesites un control detallado<br>de escalamiento y recursos|





Recomendación para el curso 9: 

Comienza con Agent Engine (parte 2): La ruta más sencilla para la implementación Luego, aprende sobre Cloud Run (parte 4): Flexibilidad adicional 

Ambas plataformas están listas para producción. Elige una en función de tus necesidades. 

7 

#### El siguiente árbol de decisión te ayudará a elegir la plataforma de implementación adecuada para tu agente: 

Ninguno g ~~r~~ aph ~~T~~ D S ~~T~~ AR ~~T~~ {Neces ~~i~~ dad de ~~i~~ mp ~~l~~ emen ~~t~~ ac ~~i~~ ón de ~~l~~ agen ~~t~~ e} ~~--~~ > LANGUAG ~~E~~ {¿Va ~~ri~~ os ~~l~~ engua ~~j~~ es?} LANGUAG ~~E --~~ >|So ~~l~~ o Py ~~t~~ hon| S ~~T~~ ANDARD{¿Agen ~~t~~ e de ~~l~~ ADK es ~~t~~ ánda ~~r~~ ?} LANGUAG ~~E --~~ >|Se neces ~~it~~ a Go o Java| CLOUD_RUN_ ~~1~~ [ ~~I~~ mp ~~l~~ emen ~~t~~ a ~~r~~ en C ~~l~~ oud Run] S ~~T~~ ANDARD ~~--~~ >|S ~~í~~ , es ~~t~~ ánda ~~r~~ | S ~~I~~ MPL ~~E~~ {¿Qu ~~i~~ e ~~r~~ es ~~l~~ a opc ~~i~~ ón más s ~~i~~ mp ~~l~~ e?} S ~~T~~ ANDARD ~~--~~ >|Con ~~t~~ enedo ~~r~~ pe ~~r~~ sona ~~li~~ zado| CLOUD_RUN_2[ ~~I~~ mp ~~l~~ emen ~~t~~ a ~~r~~ en C ~~l~~ oud Run] S ~~I~~ MPL ~~E --~~ >|S ~~í~~ | AG ~~E~~ N ~~T~~ <u>_</u> ~~E~~ NG ~~I~~ N ~~E~~ [ ~~I~~ mp ~~l~~ emen ~~t~~ a ~~r~~ en Agen ~~t E~~ ng ~~i~~ ne] S ~~I~~ MPL ~~E --~~ >|Se neces ~~it~~ a una ~~I~~ U ~~i~~ mp ~~l~~ emen ~~t~~ ada| CLOUD_RUN_3[ ~~I~~ mp ~~l~~ emen ~~t~~ a ~~r~~ en C ~~l~~ oud Run<b ~~r~~ />con ~~--~~ w ~~it~~ h_u ~~i~~ ] AG ~~E~~ N ~~T~~ <u>_</u> ~~E~~ NG ~~I~~ N ~~E --~~ > SUCC ~~E~~ SS_ ~~1~~ [✓ Ses ~~i~~ ón/memo ~~ri~~ a adm ~~i~~ n ~~i~~ s ~~tr~~ ada<b ~~r~~ />✓ Un so ~~l~~ o comando<b ~~r~~ />✓ Comp ~~l~~ e ~~t~~ amen ~~t~~ e adm ~~i~~ n ~~i~~ s ~~tr~~ ado] CLOUD_RUN_ ~~1 --~~ > SUCC ~~E~~ SS_2[✓ Mú ~~lti~~ p ~~l~~ es ~~l~~ engua ~~j~~ es<b ~~r~~ />✓ Con ~~t~~ enedo ~~r~~ pe ~~r~~ sona ~~li~~ zado<b ~~r~~ />✓ ~~Fl~~ ex ~~i~~ b ~~l~~ e] CLOUD_RUN_2 ~~--~~ > SUCC ~~E~~ SS_2 CLOUD_RUN_3 ~~--~~ > SUCC ~~E~~ SS_3[✓ ~~I~~ U web ~~i~~ nc ~~l~~ u ~~i~~ da<b ~~r~~ />✓ URL púb ~~li~~ ca<b ~~r~~ />✓ AP ~~I~~ de R ~~E~~ S ~~T~~ ] s ~~t~~ y ~~l~~ e AG ~~E~~ N ~~T~~ <u>_</u> ~~E~~ NG ~~I~~ N ~~E fill~~ : ~~#~~ ee ~~ff~~ ee s ~~t~~ y ~~l~~ e CLOUD_RUN_ ~~1 fill~~ : ~~#~~ e ~~1f~~ 5 ~~ff~~ s ~~t~~ y ~~l~~ e CLOUD_RUN_2 ~~fill~~ : ~~#~~ e ~~1f~~ 5 ~~ff~~ s ~~t~~ y ~~l~~ e CLOUD_RUN_3 ~~fill~~ : ~~#~~ e ~~1f~~ 5 ~~ff~~ s ~~t~~ y ~~l~~ e SUCC ~~E~~ SS_ ~~1 fill~~ : ~~#~~ d4edda s ~~t~~ y ~~l~~ e SUCC ~~E~~ SS_2 ~~fill~~ : ~~#~~ d4edda s ~~t~~ y ~~l~~ e SUCC ~~E~~ SS_3 ~~fill~~ : ~~#~~ d4edda 

#### Árbol de decisión de implementación: Agent Engine vs. Cloud Run 





8 

## Ejemplo práctico 

### Configura el entorno de Google Cloud 

Qué harás: Prepararás tu entorno de Google Cloud para la implementación del agente. 

Tiempo: 15 minutos 

### Paso 1: Crea una cuenta de Google Cloud (5 min aprox.) 

#### Ve a https://cloud.google.com/free. 

Acciones: 

Verificación: 

Haz clic en "Comenzar gratis". 

Accede con una Cuenta de Google. 

Verifica los beneficios del nivel gratuito: 

Cuenta creada 

Nivel gratuito activado (crédito de $300 visible) 

Crédito de $300 



<!-- Start of picture text -->
tps://cloud.google.com/sdk/docs/install<br><!-- End of picture text -->

90 días gratis 

Sin cargos mientras no se actualice el nivel 

Proporciona una tarjeta de crédito (obligatorio, 

pero no se realizan cargos automáticos). 

Completa la configuración de la cuenta. 

### Paso 2: Instala gcloud CLI (3 min aprox.) 

Descarga e instalación: 

macOS: b ~~r~~ ew ~~i~~ ns ~~t~~ a ~~ll~~ goog ~~l~~ e ~~-~~ c ~~l~~ oud ~~-~~ sdk 

Windows: Descarga el instalador en https://cloud.google.com/sdk/docs/install 

Linux: Sigue las instrucciones de <u>https://cloud.google.com/sdk/docs/install</u> 

#### Autenticación: 

Shell gc ~~l~~ oud au ~~t~~ h ~~l~~ og ~~i~~ n 

Se abrirá el navegador para la autenticación. Accede con tu cuenta de Google Cloud. 

#### Verifica la instalación: 

Shell gc ~~l~~ oud ~~--~~ ve ~~r~~ s ~~i~~ on 

9 

#### Resultado esperado: 

Ninguno SDK de Goog ~~l~~ e C ~~l~~ oud 450.0.0 ... 

### Paso 3: Crea un proyecto de Google Cloud (3 min aprox.) 

Shell 

~~#~~ C ~~r~~ ea ~~r~~ p ~~r~~ oyec ~~t~~ o 

gc ~~l~~ oud p ~~r~~ o ~~j~~ ec ~~t~~ s c ~~r~~ ea ~~t~~ e adk ~~-~~ dep ~~l~~ oymen ~~t-~~ cou ~~r~~ se ~~--~~ name ~~=~~ "Cu ~~r~~ so de ~~i~~ mp ~~l~~ emen ~~t~~ ac ~~i~~ ón de ~~l~~ ADK" 

~~# E~~ s ~~t~~ ab ~~l~~ ece ~~r~~ e ~~l~~ p ~~r~~ oyec ~~t~~ o como ac ~~ti~~ vo 

gc ~~l~~ oud con ~~fi~~ g se ~~t~~ p ~~r~~ o ~~j~~ ec ~~t~~ adk ~~-~~ dep ~~l~~ oymen ~~t-~~ cou ~~r~~ se 

~~#~~ Ve ~~rifi~~ ca ~~r~~ gc ~~l~~ oud con ~~fi~~ g ge ~~t-~~ va ~~l~~ ue p ~~r~~ o ~~j~~ ec ~~t~~ 

#### Resultado esperado: 

Ninguno 

adk ~~-~~ dep ~~l~~ oymen ~~t-~~ cou ~~r~~ se 

#### Alternativa (a través de la consola de Cloud): 

   - Ve a https://console.cloud.google.com/. 

- Haz clic en el menú desplegable del proyecto → 

   - selecciona "Proyecto nuevo". 

Nombre: "Curso de implementación del ADK" 

- Haz clic en "Crear". 

### Paso 4: Habilita la facturación (2 min aprox.) 

#### A través de la consola de Cloud: 



   - Ve a https://console.cloud.google.com/billing. 

- Haz clic en "Vincular una cuenta de facturación". 

   - Selecciona tu cuenta de facturación (creada con el nivel gratuito). 



- Haz clic en "Establecer cuenta". 



10 

#### Verifica que la facturación esté habilitada: 

Shell 

gc ~~l~~ oud be ~~t~~ a b ~~illi~~ ng p ~~r~~ o ~~j~~ ec ~~t~~ s desc ~~ri~~ be adk ~~-~~ dep ~~l~~ oymen ~~t-~~ cou ~~r~~ se 

Busca b ~~illi~~ ng ~~E~~ nab ~~l~~ ed: ~~tr~~ ue 

### Paso 5: Habilita las APIs obligatorias (2 min aprox.) 

Shell 

- ~~# H~~ ab ~~ilit~~ a ~~r l~~ a AP ~~I~~ de Ve ~~rt~~ ex A ~~I~~ (pa ~~r~~ a Agen ~~t E~~ ng ~~i~~ ne) gc ~~l~~ oud se ~~r~~ v ~~i~~ ces enab ~~l~~ e a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m.goog ~~l~~ eap ~~i~~ s.com 

~~# H~~ ab ~~ilit~~ a ~~r l~~ a AP ~~I~~ de C ~~l~~ oud Run gc ~~l~~ oud se ~~r~~ v ~~i~~ ces enab ~~l~~ e ~~r~~ un.goog ~~l~~ eap ~~i~~ s.com 

~~#~~ Ve ~~rifi~~ ca ~~r~~ que ~~l~~ as AP ~~I~~ s es ~~t~~ én hab ~~ilit~~ adas gc ~~l~~ oud se ~~r~~ v ~~i~~ ces ~~li~~ s ~~t --~~ enab ~~l~~ ed | g ~~r~~ ep ~~-E~~ "a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m| ~~r~~ un" 

#### Resultado esperado: 



Ninguno a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m.goog ~~l~~ eap ~~i~~ s.com        AP ~~I~~ de Ve ~~rt~~ ex A ~~I r~~ un.goog ~~l~~ eap ~~i~~ s.com               AP ~~I~~ de C ~~l~~ oud Run Adm ~~i~~ n 

### Paso 6: Configura alertas de facturación (3 min aprox.) 

Protégete contra los cargos inesperados: 

#### A través de la consola de Cloud: 

   - Ve a https://console.cloud.google.com/billing/ <u>budgets.</u> 

- Haz clic en "Crear presupuesto". Presupuesto 1: 

Nombre: "Alerta del curso 9: $50" 

#### Presupuesto 2: 

Nombre: "Alerta del curso 9: $100" 

Importe: $100 Umbral: 50%, 90% y 100% Haz clic en "Finalizar". 

- Importe: $50 Umbral: 50%, 90% y 100% Notificaciones por correo electrónico: Tu correo electrónico 

Haz clic en "Finalizar". 

11 

#### Qué hace esta acción: 

- Se envían alertas por correo electrónico cuando los gastos llegan a $25, $45 y $50 (presupuesto 1). Se envían alertas por correo electrónico cuando los gastos llegan a $50, $90 y $100 (presupuesto 2). 

- No se detienen los cargos automáticamente (solo se envían alertas). 

- Obtienes tranquilidad para el aprendizaje. 

### Paso 7: Instala el SDK de Vertex AI (2 min aprox.) 

Shell p ~~i~~ p ~~i~~ ns ~~t~~ a ~~ll --~~ upg ~~r~~ ade goog ~~l~~ e ~~-~~ c ~~l~~ oud ~~-~~ a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m[adk,agen ~~t~~ <u>_eng</u> ~~i~~ nes]> ~~=1~~ . ~~111 #~~ Ve ~~rifi~~ ca ~~r l~~ a ~~i~~ ns ~~t~~ a ~~l~~ ac ~~i~~ ón py ~~t~~ hon ~~-~~ c " ~~fr~~ om goog ~~l~~ e.c ~~l~~ oud ~~i~~ mpo ~~rt~~ a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m; p ~~ri~~ n ~~t~~ (a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m.__ve ~~r~~ s ~~i~~ on__)" 



#### Resultado esperado: 

Ninguno ~~1~~ . ~~111~~ .0 



#### En el siguiente diagrama, se muestra el flujo completo de configuración del entorno de Google Cloud: 

Ninguno sequenceD ~~i~~ ag ~~r~~ am pa ~~rti~~ c ~~i~~ pan ~~t~~ e ~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e pa ~~rti~~ c ~~i~~ pan ~~t~~ e GCP como Goog ~~l~~ e C ~~l~~ oud pa ~~rti~~ c ~~i~~ pan ~~t~~ e P ~~r~~ oyec ~~t~~ o pa ~~rti~~ c ~~i~~ pan ~~t~~ e AP ~~I~~ s pa ~~rti~~ c ~~i~~ pan ~~t~~ e ~~F~~ ac ~~t~~ u ~~r~~ ac ~~i~~ ón 

~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e ~~-~~ >>GCP: ~~1~~ . C ~~r~~ ea ~~r~~ cuen ~~t~~ a (n ~~i~~ ve ~~l~~ g ~~r~~ a ~~t~~ u ~~it~~ o) GCP ~~--~~ >> ~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e: $300 de c ~~r~~ éd ~~it~~ o, 90 d ~~í~~ as 

~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e ~~-~~ >>P ~~r~~ oyec ~~t~~ o: 2. C ~~r~~ ea ~~r~~ p ~~r~~ oyec ~~t~~ o P ~~r~~ oyec ~~t~~ o ~~--~~ >> ~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e: ~~I~~ D de ~~l~~ p ~~r~~ oyec ~~t~~ o: adk ~~-~~ dep ~~l~~ oymen ~~t-~~ cou ~~r~~ se 

~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e ~~-~~ >> ~~F~~ ac ~~t~~ u ~~r~~ ac ~~i~~ ón: 3. ~~H~~ ab ~~ilit~~ a ~~r l~~ a ~~f~~ ac ~~t~~ u ~~r~~ ac ~~i~~ ón ~~F~~ ac ~~t~~ u ~~r~~ ac ~~i~~ ón ~~--~~ >> ~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e: V ~~i~~ ncu ~~l~~ ada (s ~~i~~ n ca ~~r~~ gos s ~~i~~ no se ac ~~t~~ ua ~~li~~ za e ~~l~~ n ~~i~~ ve ~~l~~ ) 

~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e ~~-~~ >>AP ~~I~~ s: 4. ~~H~~ ab ~~ilit~~ a ~~r l~~ a AP ~~I~~ de Ve ~~rt~~ ex A ~~I~~ AP ~~I~~ s ~~--~~ >> ~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e: ✓ a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m.goog ~~l~~ eap ~~i~~ s.com 

~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e ~~-~~ >>AP ~~I~~ s: 5. ~~H~~ ab ~~ilit~~ a ~~r l~~ a AP ~~I~~ de C ~~l~~ oud Run AP ~~I~~ s ~~--~~ >> ~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e: ✓ ~~r~~ un.goog ~~l~~ eap ~~i~~ s.com ~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e ~~-~~ >> ~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e: 6. ~~I~~ ns ~~t~~ a ~~l~~ a ~~r~~ gc ~~l~~ oud CL ~~I E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e ~~-~~ >> ~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e: 7. ~~I~~ ns ~~t~~ a ~~l~~ a ~~r~~ e ~~l~~ SDK de Ve ~~rt~~ ex A ~~I~~ 

No ~~t~~ a sob ~~r~~ e ~~E~~ s ~~t~~ ud ~~i~~ an ~~t~~ e: L ~~i~~ s ~~t~~ o pa ~~r~~ a ~~i~~ mp ~~l~~ emen ~~t~~ a ~~r~~ se ✓ 

#### Flujo de configuración del entorno de Google Cloud 

12 

### Lista de verificación 

Completa la verificación de la configuración: 

Shell ~~# 1~~ . gc ~~l~~ oud au ~~t~~ en ~~ti~~ cado gc ~~l~~ oud au ~~t~~ h ~~li~~ s ~~t~~ 

~~#~~ 2. P ~~r~~ oyec ~~t~~ o con ~~fi~~ gu ~~r~~ ado gc ~~l~~ oud con ~~fi~~ g ge ~~t-~~ va ~~l~~ ue p ~~r~~ o ~~j~~ ec ~~t~~ 

~~#~~ 3. ~~F~~ ac ~~t~~ u ~~r~~ ac ~~i~~ ón hab ~~ilit~~ ada gc ~~l~~ oud be ~~t~~ a b ~~illi~~ ng p ~~r~~ o ~~j~~ ec ~~t~~ s desc ~~ri~~ be adk ~~-~~ dep ~~l~~ oymen ~~t-~~ cou ~~r~~ se | g ~~r~~ ep b ~~illi~~ ng ~~E~~ nab ~~l~~ ed ~~#~~ 4. AP ~~I~~ s hab ~~ilit~~ adas gc ~~l~~ oud se ~~r~~ v ~~i~~ ces ~~li~~ s ~~t --~~ enab ~~l~~ ed | g ~~r~~ ep ~~-E~~ "a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m| ~~r~~ un" 

~~#~~ 5. SDK de Ve ~~rt~~ ex A ~~I i~~ ns ~~t~~ a ~~l~~ ado py ~~t~~ hon ~~-~~ c " ~~fr~~ om goog ~~l~~ e.c ~~l~~ oud ~~i~~ mpo ~~rt~~ a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m; p ~~ri~~ n ~~t~~ ('Ve ~~rt~~ ex A ~~I~~ SDK ~~r~~ eady')" 

### Lista de verificación: 

Cuenta de Google Cloud creada 

Nivel gratuito verificado ($300 de crédito) 

gcloud CLI instalada y autenticada 

Proyecto creado y configurado como activo 

Facturación habilitada 

API de Vertex AI habilitada 

API de Cloud Run habilitada 

Alertas de facturación configuradas ($50, $100) 

SDK de Vertex AI instalado 

¿Ya revisaste todo? Ya puedes pasar a la parte 2. 



13 

## Conclusiones principales 

Ya configuraste tu entorno de Google Cloud y comprendes la diferencia fundamental entre el desarrollo local y la implementación en la nube. Los conceptos de esta parte forman la base para la implementación en producción: comprender cuándo implementar el agente, qué plataforma elegir y cómo preparar tu entorno. 

#### Implementación local vs. en la nube: 

- Desarrollo local (cursos del 1 al 8): adk web para crear y probar el agente en localhost:8000 

- Implementación en la nube (curso 9): Agent Engine o Cloud Run para compartir el agente y pasarlo a producción 

- Cuándo implementar el agente: Para compartirlo con el equipo, usarlo en producción y que esté disponible 24/7 

#### Beneficios de la implementación en producción: 

- U RLs públicas: Agente accesible a nivel global, se puede compartir con el equipo 

- Disponibilidad 24/7: Siempre en ejecución, escalado automático 

- Estado persistente: VertexAiSessionService conserva el estado de la sesión 

- Memoria entre sesiones: Memory Bank (parte 3) permite el aprendizaje en diferentes conversaciones 

#### Configuración de Google Cloud: 

- Nivel gratuito: $300 de crédito por 90 días, sin cargos automáticos después del vencimiento 

- Requisitos previos: Cuenta, proyecto, facturación, APIs (Vertex AI y Cloud Run) 

- Control de costos: Alertas de facturación (umbrales de $50 y $100) para tu tranquilidad 

#### Requisitos previos completados: 

- Google Cloud listo: Proyecto creado, facturación habilitada y APIs activadas 

- Herramientas instaladas: gcloud CLI y SDK de Vertex AI 

- Próximo paso: Implementar tu agente en Agent Engine 

#### Plataformas de implementación: 

- Vertex AI Agent Engine: 

- Implementación más sencilla, nativo del ADK, completamente administrado, servicios automáticos de sesión y memoria, solo para Python 

- Cloud Run: Implementación flexible, compatibilidad con varios lenguajes, contenedores personalizados, opción de IU web ( ~~--~~ w ~~it~~ h_u ~~i~~ ) 

Decisión: Agent Engine para la mayoría de los agentes del ADK, Cloud Run para necesidades personalizadas 







14 

