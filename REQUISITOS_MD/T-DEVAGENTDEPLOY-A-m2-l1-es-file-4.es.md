

# La solución: Vertex AI Agent Engine 



Referencia: Documentación del ADK: Agent Engine 

### De la documentación del ADK 

"Agent Engine es un servicio completamente administrado de Google Cloud que les permite a los desarrolladores implementar, administrar y escalar agentes de IA en producción. Se encarga de la infraestructura para escalar a los agentes en producción, de modo que los desarrolladores puedan enfocarse en crear aplicaciones inteligentes". 

### Qué ofrece Agent Engine 

### Qué se implementa 

Tu código de agente del ADK 

Dependencias de ~~r~~ equ ~~ir~~ emen ~~t~~ s. ~~t~~ x ~~t~~ 

Bibliotecas de entorno de ejecución del ADK 

- VertexAiSessionService (persistencia automática de la sesión) 

Contenedor (generado de forma automática) 

Escalamiento de la infraestructura (administrado) 

Py ~~t~~ hon 

~~# I~~ mp ~~l~~ emen ~~t~~ ac ~~i~~ ón con un so ~~l~~ o comando adk dep ~~l~~ oy agen ~~t-~~ eng ~~i~~ ne \ 

- ~~--~~ p ~~r~~ o ~~j~~ ec ~~t=~~ my ~~-~~ gcp ~~-~~ p ~~r~~ o ~~j~~ ec ~~t~~ \ ~~--r~~ eg ~~i~~ on ~~=~~ us ~~-~~ cen ~~tr~~ a ~~l1~~ \ ~~--~~ s ~~t~~ ag ~~i~~ ng_bucke ~~t=~~ gs://my ~~-~~ bucke ~~t~~ \ 

- ~~--~~ d ~~i~~ sp ~~l~~ ay_name ~~=~~ "M ~~i~~ agen ~~t~~ e" \ 

- /pa ~~t~~ h/ ~~t~~ o/agen ~~t~~ 

### Qué NO se implementa 

U ~~I~~ de adk web (usa la consola de Cloud o el SDK en su lugar) 

Herramientas de desarrollo locales 

- ~~# E~~ so es ~~t~~ odo. ~~El~~ agen ~~t~~ e se ~~i~~ mp ~~l~~ emen ~~t~~ ó y es ~~t~~ á ~~li~~ s ~~t~~ o pa ~~r~~ a p ~~r~~ oducc ~~i~~ ón. 

### Beneficios clave 

1 No se requieren conocimientos sobre Docker El ADK se encarga de la creación de contenedores. 

2 Persistencia automática de la sesión VertexAiSessionService se configura automáticamente. 



4 Nativo del ADK Se creó específicamente para agentes del ADK. 

5 Solo para agentes de Python Actualmente, admite Python. 

- 3 Infraestructura administrada Google se encarga del escalamiento, la disponibilidad y las actualizaciones. 

## Conceptos básicos 

### 1. ¿Qué es Agent Engine? 

### De la documentación del ADK 

"Agent Engine es un servicio completamente administrado de Google Cloud. Actualmente, solo admite agentes de Python". 

### Arquitectura 

Ninguno ~~T~~ u cód ~~i~~ go de agen ~~t~~ e (agen ~~t~~ .py) ↓ adk dep ~~l~~ oy agen ~~t-~~ eng ~~i~~ ne ↓ Agen ~~t E~~ ng ~~i~~ ne de Goog ~~l~~ e C ~~l~~ oud 

- ~~├──~~ Con ~~t~~ enedo ~~r~~ (c ~~r~~ eado 

- au ~~t~~ omá ~~ti~~ camen ~~t~~ e) ~~├──~~ Ve ~~rt~~ exA ~~i~~ Sess ~~i~~ onSe ~~r~~ v ~~i~~ ce 

- (con ~~fi~~ gu ~~r~~ ado au ~~t~~ omá ~~ti~~ camen ~~t~~ e) ~~├── E~~ sca ~~l~~ am ~~i~~ en ~~t~~ o (au ~~t~~ omá ~~ti~~ co) ~~└── E~~ ndpo ~~i~~ n ~~t~~ (URL púb ~~li~~ ca) 

### Qué ofrece Agent Engine 

##### Infraestructura administrada: 

- No se requiere administración de servidores 

- Actualizaciones y parches automáticos 

- Alta disponibilidad y redundancia Distribución geográfica (compatibilidad multirregional) 

Escalado automático: 

   - Escalamiento vertical con los aumentos de tráfico 

   - Reducción vertical de la escala durante períodos de poco tráfico 

   - Pago solo por lo que se usa 

   - Control automático de los aumentos repentinos de tráfico 

- Persistencia de la sesión (VertexAiSessionService): 

   - Del curso 4: InMemorySessionService (local, se pierde cuando se reinicia) 

   - En Agent Engine: VertexAiSessionService (persistente, administrado) 

   - Funcionan los 4 espacios de nombres del curso 4: temp:, session, user: y app: 

   - No es necesario realizar cambios en el código 

Supervisión y registro: 

   - Interfaz de la consola de Cloud para pruebas Integración de Cloud Logging Historial de ejecución y depuración Métricas de rendimiento 

- Disponibilidad 24/7: 

   - Siempre en ejecución (sin tiempo de inactividad) 

   - Accesible desde cualquier lugar Confiabilidad de nivel de producción 

   - Administrado por Google Cloud 

2 

### Implementación del agente en Agent Engine 

### Comando de implementación básico 

Shell 

- adk dep ~~l~~ oy agen ~~t-~~ eng ~~i~~ ne \ 

- ~~--~~ p ~~r~~ o ~~j~~ ec ~~t=~~ my ~~-~~ gcp ~~-~~ p ~~r~~ o ~~j~~ ec ~~t~~ \ 

- ~~--r~~ eg ~~i~~ on ~~=~~ us ~~-~~ cen ~~tr~~ a ~~l1~~ \ 

- ~~--~~ s ~~t~~ ag ~~i~~ ng_bucke ~~t=~~ gs://my ~~-~~ bucke ~~t~~ \ 

- ~~--~~ d ~~i~~ sp ~~l~~ ay_name ~~=~~ "M ~~i~~ agen ~~t~~ e" \ 

- /pa ~~t~~ h/ ~~t~~ o/agen ~~t~~ 

### Parámetros obligatorios 

- ~~--~~ p ~~r~~ o ~~j~~ ec ~~t~~ : ID del proyecto de Google Cloud (de la parte 1) 

### Qué sucede durante la implementación: 

   - Se empaqueta el código del agente: El ADK empaqueta tu agen ~~t~~ .py y las dependencias. 

- 1 

         - Se sube al bucket de etapa de pruebas: El código se sube a Google Cloud Storage 

      - 2 

      - 3 Se crea la imagen de contenedor: El ADK crea el contenedor automáticamente. 

      - 4 Se realiza la implementación en Agent Engine: El contenedor se implementa en Vertex AI. 

      - 5 Se devuelve el extremo: Se devuelve el nombre del recurso para acceder al agente implementado. 

   - Tiempo de implementación: Entre 5 y 10 minutos (primera implementación) 

- ~~--r~~ eg ~~i~~ on: Región de implementación (p. ej., us ~~-~~ cen ~~tr~~ a ~~l1~~ o eu ~~r~~ ope ~~-~~ wes ~~t1~~ ) 

- ~~--~~ s ~~t~~ ag ~~i~~ ng_bucke ~~t~~ : Bucket de Google Cloud Storage para el código de etapa de pruebas 

- ~~--~~ d ~~i~~ sp ~~l~~ ay_name: Nombre del agente legible por humanos 

- /pa ~~t~~ h/ ~~t~~ o/agen ~~t~~ : Directorio que contiene agen ~~t~~ .py con ~~r~~ oo ~~t~~ <u>_agen</u> ~~t~~ 

### Parámetros opcionales 

- ~~--r~~ equ ~~ir~~ emen ~~t~~ s: Ruta de acceso a ~~r~~ equ ~~ir~~ emen ~~t~~ s. ~~t~~ x ~~t~~ (de forma predeterminada, es ~~r~~ equ ~~ir~~ emen ~~t~~ s. ~~t~~ x ~~t~~ en el directorio del agente) 

- ~~--~~ enab ~~l~~ e_ ~~tr~~ ac ~~i~~ ng: Habilita el seguimiento detallado ( ~~Tr~~ ue o ~~F~~ a ~~l~~ se) 

- ~~--~~ desc ~~ri~~ p ~~ti~~ on: Descripción del agente 

3 

### Formato del nombre de recurso 

Ninguno p ~~r~~ o ~~j~~ ec ~~t~~ s/{PROJ ~~E~~ C ~~T~~ }/ ~~l~~ oca ~~ti~~ ons/{LOCA ~~TI~~ ON}/ ~~r~~ eason ~~i~~ ng ~~E~~ ng ~~i~~ nes/{ ~~I~~ D} 

#### Ejemplo: 

Ninguno p ~~r~~ o ~~j~~ ec ~~t~~ s/adk ~~-~~ dep ~~l~~ oymen ~~t-~~ cou ~~r~~ se/ ~~l~~ oca ~~ti~~ ons/us ~~-~~ cen ~~tr~~ a ~~l1~~ / ~~r~~ eason ~~i~~ ng ~~E~~ ng ~~i~~ nes/ ~~1~~ 23456789 

#### En el siguiente diagrama, se ilustra el proceso de implementación completo, desde tu código local hasta un extremo de producción: 

Ninguno g ~~r~~ aph LR subg ~~r~~ aph " ~~T~~ u máqu ~~i~~ na" AG ~~E~~ N ~~T~~ [agen ~~t~~ .py] ~~--~~ > ADK_CL ~~I~~ [adk dep ~~l~~ oy agen ~~t-~~ eng ~~i~~ ne] AG ~~E~~ N ~~T --~~ > D ~~E~~ PS[ ~~r~~ equ ~~ir~~ emen ~~t~~ s. ~~t~~ x ~~t~~ ] D ~~E~~ PS ~~--~~ > ADK_CL ~~I~~ end subg ~~r~~ aph "Goog ~~l~~ e C ~~l~~ oud" ADK_CL ~~I --~~ > PACKAG ~~E~~ [ ~~1~~ . ~~E~~ mpaque ~~t~~ a ~~r~~ cód ~~i~~ go] PACKAG ~~E --~~ > GCS[2. Sub ~~ir~~ a ~~l~~ bucke ~~t~~ de GCS] GCS ~~--~~ > CON ~~T~~ A ~~I~~ N ~~E~~ R[3. C ~~r~~ ea ~~r~~ con ~~t~~ enedo ~~r~~ ] CON ~~T~~ A ~~I~~ N ~~E~~ R ~~--~~ > D ~~E~~ PLOY[4. ~~I~~ mp ~~l~~ emen ~~t~~ a ~~r~~ e ~~l~~ agen ~~t~~ e en Agen ~~t E~~ ng ~~i~~ ne] D ~~E~~ PLOY ~~--~~ > ~~E~~ NDPO ~~I~~ N ~~T~~ [5. Se c ~~r~~ eó e ~~l~~ ex ~~tr~~ emo de ~~l~~ agen ~~t~~ e] end subg ~~r~~ aph "P ~~r~~ uebas" ~~E~~ NDPO ~~I~~ N ~~T --~~ > CONSOL ~~E~~ [ ~~I~~ U de ~~l~~ a conso ~~l~~ a de C ~~l~~ oud] ~~E~~ NDPO ~~I~~ N ~~T --~~ > SDK[SDK de Py ~~t~~ hon] ~~E~~ NDPO ~~I~~ N ~~T --~~ > AP ~~I~~ [AP ~~I~~ de R ~~E~~ S ~~T~~ ] end s ~~t~~ y ~~l~~ e AG ~~E~~ N ~~T fill~~ : ~~#fff~~ 3cd s ~~t~~ y ~~l~~ e ~~E~~ NDPO ~~I~~ N ~~T fill~~ : ~~#~~ d4edda s ~~t~~ y ~~l~~ e CONSOL ~~E fill~~ : ~~#~~ e ~~1f~~ 5 ~~ff~~ s ~~t~~ y ~~l~~ e SDK ~~fill~~ : ~~#~~ e ~~1f~~ 5 ~~ff~~ s ~~t~~ y ~~l~~ e AP ~~I fill~~ : ~~#~~ e ~~1f~~ 5 ~~ff~~ 

#### Proceso de implementación de Agent Engine, desde el código hasta el extremo 





4 

### 3. Prueba de los agentes implementados 

Estas son tres formas de probar los agentes implementados: 

Método 1: SDK de Python 

### De la documentación del ADK 



"Usa el SDK de Python para Vertex AI para consultar de manera programática tu agente implementado". 

Py ~~t~~ hon ~~fr~~ om goog ~~l~~ e.c ~~l~~ oud ~~i~~ mpo ~~rt~~ a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m 

~~# I~~ n ~~i~~ c ~~i~~ a ~~li~~ za a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m. ~~i~~ n ~~it~~ (p ~~r~~ o ~~j~~ ec ~~t=~~ "my ~~-~~ p ~~r~~ o ~~j~~ ec ~~t~~ ", ~~l~~ oca ~~ti~~ on ~~=~~ "us ~~-~~ cen ~~tr~~ a ~~l1~~ ") 

~~#~~ Conéc ~~t~~ a ~~t~~ e a ~~l~~ agen ~~t~~ e ~~i~~ mp ~~l~~ emen ~~t~~ ado ~~r~~ esou ~~r~~ ce_name ~~=~~ "p ~~r~~ o ~~j~~ ec ~~t~~ s/…/ ~~r~~ eason ~~i~~ ng ~~E~~ ng ~~i~~ nes/ ~~1~~ 23456789" ~~r~~ emo ~~t~~ e_app ~~=~~ a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m.Reason ~~i~~ ng ~~E~~ ng ~~i~~ ne( ~~r~~ esou ~~r~~ ce_name) 

~~#~~ Consu ~~lt~~ a a ~~l~~ agen ~~t~~ e 

~~r~~ esponse ~~= r~~ emo ~~t~~ e_app.que ~~r~~ y( ~~i~~ npu ~~t=~~ "Cómo es ~~t~~ á e ~~l~~ c ~~li~~ ma en San ~~Fr~~ anc ~~i~~ sco?") p ~~ri~~ n ~~t~~ ( ~~r~~ esponse) 

### Método 2: IU de la consola de Cloud 

Ninguno h ~~tt~~ ps://conso ~~l~~ e.c ~~l~~ oud.goog ~~l~~ e.com/ve ~~rt~~ ex ~~-~~ a ~~i~~ /agen ~~t~~ s/agen ~~t-~~ eng ~~i~~ nes 

### Acciones 

1 Selecciona el agente implementado. 

2 Usa la interfaz de prueba integrada. 

- 3 Consulta los registros de ejecución. 

- 4 Supervisa el rendimiento. 

Beneficios: Interfaz visual, no se necesita código 

5 



### Método 3: API de REST 

Shell ~~#~~ Ob ~~t~~ ene ~~r~~ un ~~t~~ oken de acceso ~~T~~ OK ~~E~~ N ~~=~~ $(gc ~~l~~ oud au ~~t~~ h p ~~ri~~ n ~~t-~~ access ~~-t~~ oken) 



~~#~~ L ~~l~~ ama ~~r~~ a ~~l~~ ex ~~tr~~ emo de ~~l~~ agen ~~t~~ e cu ~~rl -~~ X POS ~~T~~ \ 

- ~~-H~~ "Au ~~t~~ ho ~~ri~~ za ~~ti~~ on: Bea ~~r~~ e ~~r~~ $ ~~T~~ OK ~~E~~ N" \ 

- ~~-H~~ "Con ~~t~~ en ~~t-T~~ ype: app ~~li~~ ca ~~ti~~ on/ ~~j~~ son" \ 

~~-~~ d '{" ~~i~~ npu ~~t~~ ": "¿Cómo es ~~t~~ a ~~r~~ á e ~~l~~ c ~~li~~ ma?"}' \ h ~~tt~~ ps://R ~~E~~ G ~~I~~ ON ~~-~~ a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m.goog ~~l~~ eap ~~i~~ s.com/v ~~1~~ /p ~~r~~ o ~~j~~ ec ~~t~~ s/PROJ ~~E~~ C ~~T~~ / ~~l~~ oca ~~ti~~ ons/LOCA ~~TI~~ ON/ ~~r~~ eason ~~i~~ ng ~~E~~ ng ~~i~~ nes/ ~~I~~ D:que ~~r~~ y 

### Caso de uso: Integración con sistemas que no son de Python 

En el siguiente diagrama, se muestra cómo los desarrolladores pueden probar los agentes implementados con diferentes métodos: 

Ninguno sequenceD ~~i~~ ag ~~r~~ am pa ~~rti~~ c ~~i~~ pan ~~t~~ e Dev como desa ~~rr~~ o ~~ll~~ ado ~~r~~ pa ~~rti~~ c ~~i~~ pan ~~t~~ e Conso ~~l~~ e como conso ~~l~~ a de C ~~l~~ oud pa ~~rti~~ c ~~i~~ pan ~~t~~ e SDK como SDK de Py ~~t~~ hon pa ~~rti~~ c ~~i~~ pan ~~t~~ e Agen ~~t~~ como agen ~~t~~ e ~~i~~ mp ~~l~~ emen ~~t~~ ado pa ~~rti~~ c ~~i~~ pan ~~t~~ e Logs como C ~~l~~ oud Logg ~~i~~ ng Dev ~~-~~ >>Conso ~~l~~ e: ~~1~~ . Navega a ~~l~~ a ~~I~~ U de Agen ~~t E~~ ng ~~i~~ ne Conso ~~l~~ e ~~-~~ >>Agen ~~t~~ : Consu ~~lt~~ a de p ~~r~~ ueba: "¿Cómo es ~~t~~ a ~~r~~ á e ~~l~~ c ~~li~~ ma hoy?" Agen ~~t--~~ >>Conso ~~l~~ e: Respues ~~t~~ a Conso ~~l~~ e ~~--~~ >>Dev: Mos ~~tr~~ a ~~r r~~ espues ~~t~~ a Dev ~~-~~ >>SDK: 2. Usa e ~~l~~ SDK de Py ~~t~~ hon SDK ~~-~~ >>Agen ~~t~~ : ~~r~~ emo ~~t~~ e_app.que ~~r~~ y("¿Cómo es ~~t~~ a ~~r~~ á e ~~l~~ c ~~li~~ ma?") Agen ~~t--~~ >>SDK: Respues ~~t~~ a SDK ~~--~~ >>Dev: ~~I~~ mp ~~ri~~ m ~~ir r~~ espues ~~t~~ a Dev ~~-~~ >>Logs: 3. Consu ~~lt~~ a ~~r l~~ os ~~r~~ eg ~~i~~ s ~~tr~~ os de e ~~j~~ ecuc ~~i~~ ón Logs ~~--~~ >>Dev: ~~Hi~~ s ~~t~~ o ~~ri~~ a ~~l~~ de e ~~j~~ ecuc ~~i~~ ón de ~~l~~ agen ~~t~~ e No ~~t~~ a sob ~~r~~ e Dev y Logs: ~~H~~ ay va ~~ri~~ os mé ~~t~~ odos de p ~~r~~ ueba d ~~i~~ spon ~~i~~ b ~~l~~ es 

Se prueban los agentes implementados a través de la consola, el SDK y los registros 

6 

### 4. Persistencia automática de la sesión 

### De la documentación del ADK 

"Cuando se implementan, los agentes usan automáticamente VertexAiSessionService para obtener un estado de sesión persistente y administrado". 

### Qué significa esto 

Desarrollo local (curso 4): 

#### Implementación en producción (curso 9): 

Py ~~t~~ hon 

~~fr~~ om goog ~~l~~ e.adk.sess ~~i~~ ons ~~i~~ mpo ~~rt I~~ nMemo ~~r~~ ySess ~~i~~ onSe ~~r~~ v ~~i~~ ce 

~~# E~~ s ~~t~~ ado de ~~l~~ a ses ~~i~~ ón con 4 espac ~~i~~ os de nomb ~~r~~ es 

sess ~~i~~ on.s ~~t~~ a ~~t~~ e[' ~~t~~ emp:cu ~~rr~~ en ~~t~~ <u>_s</u> ~~t~~ ep'] ~~=~~ 'b ~~illi~~ ng' sess ~~i~~ on.s ~~t~~ a ~~t~~ e[' ~~r~~ eques ~~t~~ <u>_coun</u> ~~t~~ '] ~~=~~ 5 sess ~~i~~ on.s ~~t~~ a ~~t~~ e['use ~~r~~ : ~~ti~~ e ~~r~~ '] ~~=~~ 'p ~~r~~ em ~~i~~ um' sess ~~i~~ on.s ~~t~~ a ~~t~~ e['app:suppo ~~rt~~ <u>_hou</u> ~~r~~ s'] ~~=~~ '9am ~~-~~ 5pm' 

~~#~~ P ~~r~~ ob ~~l~~ ema: Se p ~~i~~ e ~~r~~ de cuando se ~~r~~ e ~~i~~ n ~~i~~ c ~~i~~ a 

###### Py ~~t~~ hon 

- ~~#~~ Ve ~~rt~~ exA ~~i~~ Sess ~~i~~ onSe ~~r~~ v ~~i~~ ce con ~~fi~~ gu ~~r~~ ado au ~~t~~ omá ~~ti~~ camen ~~t~~ e 

~~#~~ Las m ~~i~~ smas va ~~ri~~ ab ~~l~~ es de es ~~t~~ ado de ~~l~~ a ses ~~i~~ ón ~~f~~ unc ~~i~~ onan: 

- ~~# - t~~ emp: (a ~~l~~ cance de ~~t~~ u ~~r~~ no, pe ~~r~~ o s ~~i~~ gue s ~~i~~ endo ~~t~~ empo ~~r~~ a ~~l~~ ) 

- ~~# -~~ sess ~~i~~ on (a ~~l~~ cance de conve ~~r~~ sac ~~i~~ ón, aho ~~r~~ a es pe ~~r~~ s ~~i~~ s ~~t~~ en ~~t~~ e) 

- ~~# -~~ use ~~r~~ : ( ~~f~~ unc ~~i~~ ona en ~~tr~~ e ses ~~i~~ ones, 

- aho ~~r~~ a es pe ~~r~~ s ~~i~~ s ~~t~~ en ~~t~~ e) 

- ~~# -~~ app: (g ~~l~~ oba ~~l~~ , aho ~~r~~ a es pe ~~r~~ s ~~i~~ s ~~t~~ en ~~t~~ e) 

~~#~~ NO ~~E~~ S N ~~E~~ C ~~E~~ SAR ~~I~~ O R ~~E~~ AL ~~I~~ ZAR CAMB ~~I~~ OS ~~E~~ N ~~E~~ L CÓD ~~I~~ GO 







7 

#### Los 4 espacios de nombres del curso 4 funcionan en producción: 

|Espacio de nombres|Alcance|Persistencia (Agent Engine)|
|---|---|---|
|~~t~~emp:|Alcance de turno|Temporal (según el diseño)|
|session|Conversación|Persistente después de los|
|||reinicios|
|use~~r~~:|Entre sesiones|Persistente en todas las|
|||sesiones|
|app:|Global|Persistente a nivel global|



#### Ejemplo de código: 

Py ~~t~~ hon ~~#~~ agen ~~t~~ e de ~~l~~ cu ~~r~~ so 4 ( ~~l~~ oca ~~l~~ ) agen ~~t =~~ L ~~l~~ mAgen ~~t~~ ( ~~i~~ ns ~~tr~~ uc ~~ti~~ on ~~=~~ """ Recuen ~~t~~ o de so ~~li~~ c ~~it~~ udes: { ~~r~~ eques ~~t~~ <u>_coun</u> ~~t~~ ?0} N ~~i~~ ve ~~l~~ de usua ~~ri~~ o: {use ~~r~~ : ~~ti~~ e ~~r~~ ?es ~~t~~ ánda ~~r~~ } """ ) 

~~# El~~ m ~~i~~ smo agen ~~t~~ e se ~~i~~ mp ~~l~~ emen ~~t~~ a en Agen ~~t E~~ ng ~~i~~ ne (cu ~~r~~ so 9) ~~#~~ → Usa de ~~f~~ o ~~r~~ ma au ~~t~~ omá ~~ti~~ ca Ve ~~rt~~ exA ~~i~~ Sess ~~i~~ onSe ~~r~~ v ~~i~~ ce 

~~#~~ → ~~T~~ odas ~~l~~ as va ~~ri~~ ab ~~l~~ es de es ~~t~~ ado ~~f~~ unc ~~i~~ onan de ~~f~~ o ~~r~~ ma ~~i~~ dén ~~ti~~ ca 

~~#~~ → No es necesa ~~ri~~ o ~~r~~ ea ~~li~~ za ~~r~~ camb ~~i~~ os en e ~~l~~ cód ~~i~~ go 



8 



## Ejemplo práctico 1 

### Implementa un agente meteorológico simple 

Qué crearás: 

Un agente meteorológico simple que demuestre la implementación básica de Agent Engine. 

### Paso 1: Crea el agente 

Crea la estructura del directorio: 

Shell 

cd 09 ~~-~~ dep ~~l~~ oy ~~-~~ you ~~r-fir~~ s ~~t-~~ agen ~~t~~ /pa ~~rt~~ <u>_2_ve</u> ~~rt~~ ex_a ~~i~~ <u>_agen</u> ~~t~~ <u>_eng</u> ~~i~~ ne/ mkd ~~ir -~~ p wea ~~t~~ he ~~r~~ <u>_agen</u> ~~t~~ cd wea ~~t~~ he ~~r~~ <u>_agen</u> ~~t~~ 

Crea agen ~~t~~ .py: 

Py ~~t~~ hon """ Agen ~~t~~ e me ~~t~~ eo ~~r~~ o ~~l~~ óg ~~i~~ co s ~~i~~ mp ~~l~~ e Demues ~~tr~~ a ~~l~~ a ~~i~~ mp ~~l~~ emen ~~t~~ ac ~~i~~ ón bás ~~i~~ ca de Agen ~~t E~~ ng ~~i~~ ne. Re ~~f~~ e ~~r~~ enc ~~i~~ a: h ~~tt~~ ps://goog ~~l~~ e.g ~~it~~ hub. ~~i~~ o/adk ~~-~~ docs/ """ ~~fr~~ om goog ~~l~~ e.adk.agen ~~t~~ s ~~i~~ mpo ~~rt~~ L ~~l~~ mAgen ~~t~~ 

~~r~~ oo ~~t~~ <u>_agen</u> ~~t =~~ L ~~l~~ mAgen ~~t~~ ( mode ~~l=~~ 'gem ~~i~~ n ~~i-~~ 2.5 ~~-fl~~ ash', name ~~=~~ 'wea ~~t~~ he ~~r~~ <u>_agen</u> ~~t~~ ', desc ~~ri~~ p ~~ti~~ on ~~=~~ 'P ~~r~~ ov ~~i~~ des wea ~~t~~ he ~~r i~~ n ~~f~~ o ~~r~~ ma ~~ti~~ on and ~~f~~ o ~~r~~ ecas ~~t~~ s', ~~i~~ ns ~~tr~~ uc ~~ti~~ on ~~=~~ """ ~~Er~~ es un as ~~i~~ s ~~t~~ en ~~t~~ e me ~~t~~ eo ~~r~~ o ~~l~~ óg ~~i~~ co ú ~~til~~ . Cuando ~~l~~ os usua ~~ri~~ os p ~~r~~ egun ~~t~~ an sob ~~r~~ e e ~~l~~ c ~~li~~ ma, haz ~~l~~ o s ~~i~~ gu ~~i~~ en ~~t~~ e: ~~1~~ . P ~~r~~ egun ~~t~~ a po ~~r l~~ a c ~~i~~ udad s ~~i~~ no se p ~~r~~ opo ~~r~~ c ~~i~~ ona 2. P ~~r~~ opo ~~r~~ c ~~i~~ ona ~~i~~ n ~~f~~ o ~~r~~ mac ~~i~~ ón de ~~l~~ c ~~li~~ ma (s ~~i~~ mu ~~l~~ ada po ~~r~~ aho ~~r~~ a) 3. Sé amab ~~l~~ e y se ~~r~~ v ~~i~~ c ~~i~~ a ~~l~~ 

Respues ~~t~~ a de e ~~j~~ emp ~~l~~ o: " ~~E~~ n San ~~Fr~~ anc ~~i~~ sco, ~~l~~ a ~~t~~ empe ~~r~~ a ~~t~~ u ~~r~~ a ac ~~t~~ ua ~~l~~ es de 20 °C (68 ° ~~F~~ ) y e ~~l~~ c ~~i~~ e ~~l~~ o es ~~t~~ á pa ~~r~~ c ~~i~~ a ~~l~~ men ~~t~~ e nub ~~l~~ ado". 

No ~~t~~ a: ~~E~~ n p ~~r~~ oducc ~~i~~ ón, es ~~t~~ o se ~~i~~ n ~~t~~ eg ~~r~~ a ~~rí~~ a con una AP ~~I~~ de c ~~li~~ ma ~~r~~ ea ~~l~~ . Pa ~~r~~ a es ~~t~~ e cu ~~r~~ so, p ~~r~~ opo ~~r~~ c ~~i~~ ona ~~i~~ n ~~f~~ o ~~r~~ mac ~~i~~ ón me ~~t~~ eo ~~r~~ o ~~l~~ óg ~~i~~ ca s ~~i~~ mu ~~l~~ ada, pe ~~r~~ o ~~r~~ ea ~~li~~ s ~~t~~ a. """ ) 

9 

Crea ~~r~~ equ ~~ir~~ emen ~~t~~ s. ~~t~~ x ~~t~~ : 

Ninguno goog ~~l~~ e ~~-~~ c ~~l~~ oud ~~-~~ a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m[adk,agen ~~t~~ <u>_eng</u> ~~i~~ nes]> ~~=1~~ . ~~111~~ 

Crea .env. ~~t~~ emp ~~l~~ a ~~t~~ e: 

Shell GOOGL ~~E~~ <u>_CLOUD_PROJ</u> ~~E~~ C ~~T=~~ you ~~r-~~ p ~~r~~ o ~~j~~ ec ~~t-i~~ d GOOGL ~~E~~ <u>_CLOUD_LOCA</u> ~~TI~~ ON ~~=~~ us ~~-~~ cen ~~tr~~ a ~~l1~~ GOOGL ~~E~~ <u>_AP</u> ~~I~~ <u>_K</u> ~~E~~ Y ~~=~~ you ~~r-~~ ap ~~i-~~ key 

### Paso 2: Crea un bucket de etapa de pruebas de GCS 

Shell ~~#~~ C ~~r~~ ea un nomb ~~r~~ e de bucke ~~t~~ ún ~~i~~ co BUCK ~~ET~~ <u>_NAM</u> ~~E=~~ "adk ~~-~~ s ~~t~~ ag ~~i~~ ng ~~-~~ $(da ~~t~~ e ~~+~~ %s)" 

~~#~~ C ~~r~~ ea e ~~l~~ bucke ~~t~~ 

gsu ~~til~~ mb ~~-~~ p adk ~~-~~ dep ~~l~~ oymen ~~t-~~ cou ~~r~~ se ~~-l~~ us ~~-~~ cen ~~tr~~ a ~~l1~~ gs://$BUCK ~~ET~~ <u>_NAM</u> ~~E~~ 



~~#~~ Ve ~~rifi~~ ca s ~~i~~ se c ~~r~~ eó e ~~l~~ bucke ~~t~~ gsu ~~til l~~ s gs://$BUCK ~~ET~~ <u>_NAM</u> ~~E~~ 

#### Resultado esperado: 

Ninguno C ~~r~~ eando gs://adk ~~-~~ s ~~t~~ ag ~~i~~ ng ~~-1~~ 234567890/… 

### Paso 3: Implementa el agente en Agent Engine 

Shell ~~# E~~ s ~~t~~ ab ~~l~~ ece ~~l~~ as va ~~ri~~ ab ~~l~~ es de en ~~t~~ o ~~r~~ no expo ~~rt~~ GOOGL ~~E~~ <u>_CLOUD_PROJ</u> ~~E~~ C ~~T=~~ "adk ~~-~~ dep ~~l~~ oymen ~~t-~~ cou ~~r~~ se" expo ~~rt~~ GOOGL ~~E~~ <u>_CLOUD_LOCA</u> ~~TI~~ ON ~~=~~ "us ~~-~~ cen ~~tr~~ a ~~l1~~ " expo ~~rt~~ S ~~T~~ AG ~~I~~ NG_BUCK ~~ET=~~ "gs://$BUCK ~~ET~~ <u>_NAM</u> ~~E~~ " 

~~# I~~ mp ~~l~~ emen ~~t~~ a e ~~l~~ agen ~~t~~ e adk dep ~~l~~ oy agen ~~t-~~ eng ~~i~~ ne \ ~~--~~ p ~~r~~ o ~~j~~ ec ~~t=~~ $GOOGL ~~E~~ <u>_CLOUD_PROJ</u> ~~E~~ C ~~T~~ \ ~~--r~~ eg ~~i~~ on ~~=~~ $GOOGL ~~E~~ <u>_CLOUD_LOCA</u> ~~TI~~ ON \ ~~--~~ s ~~t~~ ag ~~i~~ ng_bucke ~~t=~~ $S ~~T~~ AG ~~I~~ NG_BUCK ~~ET~~ \ ~~--~~ d ~~i~~ sp ~~l~~ ay_name ~~=~~ "Agen ~~t~~ e me ~~t~~ eo ~~r~~ o ~~l~~ óg ~~i~~ co" \ wea ~~t~~ he ~~r~~ <u>_agen</u> ~~t~~ / 

10 

#### Resultado esperado: 

Ninguno ~~I~~ mp ~~l~~ emen ~~t~~ ando e ~~l~~ agen ~~t~~ e "wea ~~t~~ he ~~r~~ <u>_agen</u> ~~t~~ "… ~~E~~ mpaque ~~t~~ ando e ~~l~~ cód ~~i~~ go… Sub ~~i~~ endo a gs://adk ~~-~~ s ~~t~~ ag ~~i~~ ng ~~-~~ xyz… C ~~r~~ eando e ~~l~~ con ~~t~~ enedo ~~r~~ … ~~I~~ mp ~~l~~ emen ~~t~~ ando en Agen ~~t E~~ ng ~~i~~ ne… ✓ ~~El~~ agen ~~t~~ e se ~~i~~ mp ~~l~~ emen ~~t~~ ó co ~~rr~~ ec ~~t~~ amen ~~t~~ e 

Nomb ~~r~~ e de ~~l r~~ ecu ~~r~~ so: p ~~r~~ o ~~j~~ ec ~~t~~ s/adk ~~-~~ dep ~~l~~ oymen ~~t-~~ cou ~~r~~ se/ ~~l~~ oca ~~ti~~ ons/us ~~-~~ cen ~~tr~~ a ~~l1~~ / ~~r~~ eason ~~i~~ ng ~~E~~ ng ~~i~~ nes/ ~~1~~ 23456789 



Guarda este nombre de recurso. Lo necesitarás para las pruebas. Tiempo de implementación: Entre 5 y 10 minutos (ten paciencia) 

### Paso 4: Prueba el agente implementado 

Crea ~~t~~ es ~~t~~ <u>_dep</u> ~~l~~ oyed_agen ~~t~~ .py: 

Py ~~t~~ hon """ P ~~r~~ ueba e ~~l~~ agen ~~t~~ e me ~~t~~ eo ~~r~~ o ~~l~~ óg ~~i~~ co ~~i~~ mp ~~l~~ emen ~~t~~ ado """ ~~i~~ mpo ~~rt~~ os ~~fr~~ om goog ~~l~~ e.c ~~l~~ oud ~~i~~ mpo ~~rt~~ a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m ~~# I~~ n ~~i~~ c ~~i~~ a ~~li~~ za a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m. ~~i~~ n ~~it~~ ( p ~~r~~ o ~~j~~ ec ~~t=~~ os.env ~~ir~~ on["GOOGL ~~E~~ <u>_CLOUD_PROJ</u> ~~E~~ C ~~T~~ "], ~~l~~ oca ~~ti~~ on ~~=~~ os.env ~~ir~~ on["GOOGL ~~E~~ <u>_CLOUD_LOCA</u> ~~TI~~ ON"] ) 

~~#~~ Conéc ~~t~~ a ~~t~~ e a ~~l~~ agen ~~t~~ e ~~i~~ mp ~~l~~ emen ~~t~~ ado (R ~~EE~~ MPLAZA POR ~~T~~ U NOMBR ~~E~~ D ~~E~~ R ~~E~~ CURSO) ~~r~~ esou ~~r~~ ce_name ~~=~~ "p ~~r~~ o ~~j~~ ec ~~t~~ s/adk ~~-~~ dep ~~l~~ oymen ~~t-~~ cou ~~r~~ se/ ~~l~~ oca ~~ti~~ ons/us ~~-~~ cen ~~tr~~ a ~~l1~~ / ~~r~~ eason ~~i~~ ng ~~E~~ ng ~~i~~ nes/ ~~1~~ 23456789" ~~r~~ emo ~~t~~ e_app ~~=~~ a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m.Reason ~~i~~ ng ~~E~~ ng ~~i~~ ne( ~~r~~ esou ~~r~~ ce_name) ~~#~~ Consu ~~lt~~ a de p ~~r~~ ueba ~~1~~ p ~~ri~~ n ~~t~~ (" ~~=~~ " * 60) p ~~ri~~ n ~~t~~ ("P ~~r~~ ueba ~~1~~ : Consu ~~lt~~ a sob ~~r~~ e e ~~l~~ c ~~li~~ ma") p ~~ri~~ n ~~t~~ (" ~~=~~ " * 60) ~~r~~ esponse ~~= r~~ emo ~~t~~ e_app.que ~~r~~ y( ~~i~~ npu ~~t=~~ "Cómo es ~~t~~ á e ~~l~~ c ~~li~~ ma en San ~~Fr~~ anc ~~i~~ sco?") p ~~ri~~ n ~~t~~ ( ~~f~~ "Respues ~~t~~ a de ~~l~~ agen ~~t~~ e: { ~~r~~ esponse}") p ~~ri~~ n ~~t~~ () 

~~#~~ Consu ~~lt~~ a de p ~~r~~ ueba 2 p ~~ri~~ n ~~t~~ (" ~~=~~ " * 60) p ~~ri~~ n ~~t~~ ("P ~~r~~ ueba 3: P ~~r~~ onós ~~ti~~ co de ~~l~~ c ~~li~~ ma") 

11 

p ~~ri~~ n ~~t~~ (" ~~=~~ " * 60) ~~r~~ esponse2 ~~= r~~ emo ~~t~~ e_app.que ~~r~~ y( ~~i~~ npu ~~t=~~ "¿L ~~l~~ ove ~~r~~ á mañana en Sea ~~ttl~~ e?") p ~~ri~~ n ~~t~~ ( ~~f~~ "Respues ~~t~~ a de ~~l~~ agen ~~t~~ e: { ~~r~~ esponse2}") p ~~ri~~ n ~~t~~ () 

p ~~ri~~ n ~~t~~ (" ~~=~~ " * 60) p ~~ri~~ n ~~t~~ ("✓ ~~El~~ agen ~~t~~ e ~~i~~ mp ~~l~~ emen ~~t~~ ado ~~f~~ unc ~~i~~ ona co ~~rr~~ ec ~~t~~ amen ~~t~~ e") p ~~ri~~ n ~~t~~ (" ~~=~~ " * 60) 

#### Ejecuta la prueba: 

Shell py ~~t~~ hon ~~t~~ es ~~t~~ <u>_dep</u> ~~l~~ oyed_agen ~~t~~ .py 

#### Resultado esperado: 

Ninguno ~~============================================================~~ P ~~r~~ ueba ~~1~~ : Consu ~~lt~~ a sob ~~r~~ e e ~~l~~ c ~~li~~ ma ~~============================================================~~ Respues ~~t~~ a de ~~l~~ agen ~~t~~ e: ~~El~~ c ~~li~~ ma ac ~~t~~ ua ~~l~~ en San ~~Fr~~ anc ~~i~~ sco es... ~~============================================================~~ P ~~r~~ ueba 2: P ~~r~~ onós ~~ti~~ co de ~~l~~ c ~~li~~ ma 

~~============================================================~~ Respues ~~t~~ a de ~~l~~ agen ~~t~~ e: Según e ~~l~~ p ~~r~~ onós ~~ti~~ co pa ~~r~~ a Sea ~~ttl~~ e... ~~============================================================~~ ✓ ~~El~~ agen ~~t~~ e ~~i~~ mp ~~l~~ emen ~~t~~ ado ~~f~~ unc ~~i~~ ona co ~~rr~~ ec ~~t~~ amen ~~t~~ e ~~============================================================~~ 

### Paso 5: Consulta los registros en la consola de Cloud 

Ve a: 

Ninguno h ~~tt~~ ps://conso ~~l~~ e.c ~~l~~ oud.goog ~~l~~ e.com/ve ~~rt~~ ex ~~-~~ a ~~i~~ /agen ~~t~~ s/agen ~~t-~~ eng ~~i~~ nes 

### Acciones 

- 1 Selecciona "weather_agent". 

- 2 Haz clic en Ver registros. 

- 3 Consulta el historial de ejecución del agente. 

- 4 Consulta los detalles de la solicitud y la respuesta. 





12 

## Ejemplo práctico 2 

### Implementa el flujo de trabajo del curso 8 

Qué crearás: 



Implementa el sistema de QA de contenido de la parte 1 del curso 8 (secuencial + paralelo + de bucle) para demostrar la implementación de flujos de trabajo complejos. 

### Paso 1: Crea un sistema de QA de contenido 

Según la parte 1 del curso 8, crea con ~~t~~ en ~~t~~ <u>_qa_sys</u> ~~t~~ em/agen ~~t~~ .py: 

Py ~~t~~ hon """ S ~~i~~ s ~~t~~ ema de QA de con ~~t~~ en ~~i~~ do: Pa ~~rt~~ e ~~1~~ de ~~l~~ cu ~~r~~ so 8 Demues ~~tr~~ a cómo ~~i~~ mp ~~l~~ emen ~~t~~ a ~~r fl~~ u ~~j~~ os de ~~tr~~ aba ~~j~~ o comp ~~l~~ e ~~j~~ os en Agen ~~t E~~ ng ~~i~~ ne. Re ~~f~~ e ~~r~~ enc ~~i~~ a: Cu ~~r~~ so 8, pa ~~rt~~ e ~~1~~ (Pa ~~tr~~ ones de ~~fl~~ u ~~j~~ o de ~~tr~~ aba ~~j~~ o avanzados) ~~I~~ mp ~~l~~ emen ~~t~~ ac ~~i~~ ón: Documen ~~t~~ ac ~~i~~ ón de ~~l~~ ADK: Agen ~~t E~~ ng ~~i~~ ne """ 

~~fr~~ om goog ~~l~~ e.adk.agen ~~t~~ s ~~i~~ mpo ~~rt~~ L ~~l~~ mAgen ~~t~~ , Sequen ~~ti~~ a ~~l~~ Agen ~~t~~ , Pa ~~r~~ a ~~ll~~ e ~~l~~ Agen ~~t~~ , LoopAgen ~~t~~ , BaseAgen ~~t fr~~ om goog ~~l~~ e.adk.even ~~t~~ s ~~i~~ mpo ~~rt E~~ ven ~~t~~ , ~~E~~ ven ~~t~~ Ac ~~ti~~ ons ~~# Et~~ apa ~~1~~ : Agen ~~t~~ e de ~~r~~ ecepc ~~i~~ ón ~~i~~ n ~~t~~ ake_agen ~~t =~~ L ~~l~~ mAgen ~~t~~ ( mode ~~l=~~ 'gem ~~i~~ n ~~i-~~ 2.5 ~~-fl~~ ash', name ~~=~~ ' ~~i~~ n ~~t~~ ake', ou ~~t~~ pu ~~t~~ <u>_key</u> ~~=~~ 'con ~~t~~ en ~~t~~ ', ~~i~~ ns ~~tr~~ uc ~~ti~~ on ~~=~~ """ ~~Er~~ es espec ~~i~~ a ~~li~~ s ~~t~~ a en ~~r~~ ecepc ~~i~~ ón pa ~~r~~ a e ~~l~~ con ~~tr~~ o ~~l~~ de ca ~~li~~ dad de con ~~t~~ en ~~i~~ do. ~~E~~ x ~~tr~~ ae y es ~~tr~~ uc ~~t~~ u ~~r~~ a e ~~l~~ con ~~t~~ en ~~i~~ do p ~~r~~ opo ~~r~~ c ~~i~~ onado po ~~r~~ e ~~l~~ usua ~~ri~~ o. A ~~l~~ macena e ~~l~~ con ~~t~~ en ~~i~~ do ex ~~tr~~ a ~~í~~ do en e ~~l~~ es ~~t~~ ado pa ~~r~~ a su p ~~r~~ ocesam ~~i~~ en ~~t~~ o pos ~~t~~ e ~~ri~~ o ~~r~~ . """ ) ~~# Et~~ apa 2a: Ve ~~rifi~~ cado ~~r~~ de da ~~t~~ os A ( ~~f~~ uen ~~t~~ es académ ~~i~~ cas) ~~f~~ ac ~~t~~ <u>_checke</u> ~~r~~ <u>_a</u> ~~=~~ L ~~l~~ mAgen ~~t~~ ( mode ~~l=~~ 'gem ~~i~~ n ~~i-~~ 2.5 ~~-fl~~ ash', name ~~=~~ ' ~~f~~ ac ~~t~~ <u>_checke</u> ~~r~~ <u>_academ</u> ~~i~~ c', ou ~~t~~ pu ~~t~~ <u>_key</u> ~~=~~ ' ~~f~~ ac ~~t~~ <u>_check_academ</u> ~~i~~ c', ~~i~~ ns ~~tr~~ uc ~~ti~~ on ~~=~~ """ Ve ~~rifi~~ ca ~~l~~ os da ~~t~~ os ~~i~~ nc ~~l~~ u ~~i~~ dos en e ~~l~~ con ~~t~~ en ~~i~~ do: {con ~~t~~ en ~~t~~ } 

13 

###### ~~E~~ n ~~f~~ óca ~~t~~ e en ~~l~~ as ~~F~~ U ~~E~~ N ~~TE~~ S ACAD ~~É~~ M ~~I~~ CAS: 

- A ~~rtí~~ cu ~~l~~ os de ~~i~~ nves ~~ti~~ gac ~~i~~ ón 

- Rev ~~i~~ s ~~t~~ as académ ~~i~~ cas 

- ~~E~~ s ~~t~~ ud ~~i~~ os de un ~~i~~ ve ~~r~~ s ~~i~~ dades 

Ca ~~lifi~~ ca su p ~~r~~ ec ~~i~~ s ~~i~~ ón de 0 a ~~1~~ 0. """ ) 



~~# Et~~ apa 2b: Ve ~~rifi~~ cado ~~r~~ de da ~~t~~ os B ( ~~f~~ uen ~~t~~ es de no ~~ti~~ c ~~i~~ as) ~~f~~ ac ~~t~~ <u>_checke</u> ~~r~~ <u>_b</u> ~~=~~ L ~~l~~ mAgen ~~t~~ ( mode ~~l=~~ 'gem ~~i~~ n ~~i-~~ 2.5 ~~-fl~~ ash', name ~~=~~ ' ~~f~~ ac ~~t~~ <u>_checke</u> ~~r~~ <u>_news',</u> ou ~~t~~ pu ~~t~~ <u>_key</u> ~~=~~ ' ~~f~~ ac ~~t~~ <u>_check_news',</u> ~~i~~ ns ~~tr~~ uc ~~ti~~ on ~~=~~ """ Ve ~~rifi~~ ca ~~l~~ os da ~~t~~ os ~~i~~ nc ~~l~~ u ~~i~~ dos en e ~~l~~ con ~~t~~ en ~~i~~ do: {con ~~t~~ en ~~t~~ } 

~~E~~ n ~~f~~ óca ~~t~~ e en ~~l~~ as ~~F~~ U ~~E~~ N ~~TE~~ S D ~~E~~ NO ~~TI~~ C ~~I~~ AS: 

- P ~~ri~~ nc ~~i~~ pa ~~l~~ es med ~~i~~ os de comun ~~i~~ cac ~~i~~ ón 

- Pe ~~ri~~ od ~~i~~ smo ~~i~~ nves ~~ti~~ ga ~~ti~~ vo 

- Sucesos ac ~~t~~ ua ~~l~~ es 

Ca ~~lifi~~ ca su p ~~r~~ ec ~~i~~ s ~~i~~ ón de 0 a ~~1~~ 0. """ ) 

~~# Et~~ apa 2c: Ve ~~rifi~~ cado ~~r~~ de da ~~t~~ os C ( ~~f~~ uen ~~t~~ es o ~~fi~~ c ~~i~~ a ~~l~~ es o gube ~~r~~ namen ~~t~~ a ~~l~~ es) ~~f~~ ac ~~t~~ <u>_checke</u> ~~r~~ <u>_c</u> ~~=~~ L ~~l~~ mAgen ~~t~~ ( mode ~~l=~~ 'gem ~~i~~ n ~~i-~~ 2.5 ~~-fl~~ ash', name ~~=~~ ' ~~f~~ ac ~~t~~ <u>_checke</u> ~~r~~ <u>_o</u> ~~ffi~~ c ~~i~~ a ~~l~~ ', ou ~~t~~ pu ~~t~~ <u>_key</u> ~~=~~ ' ~~f~~ ac ~~t~~ <u>_check_o</u> ~~ffi~~ c ~~i~~ a ~~l~~ ', ~~i~~ ns ~~tr~~ uc ~~ti~~ on ~~=~~ """ Ve ~~rifi~~ ca ~~l~~ os da ~~t~~ os ~~i~~ nc ~~l~~ u ~~i~~ dos en e ~~l~~ con ~~t~~ en ~~i~~ do: {con ~~t~~ en ~~t~~ } ~~E~~ n ~~f~~ óca ~~t~~ e en ~~l~~ as ~~F~~ U ~~E~~ N ~~TE~~ S O ~~FI~~ C ~~I~~ AL ~~E~~ S: ~~-~~ Da ~~t~~ os gube ~~r~~ namen ~~t~~ a ~~l~~ es 

~~- E~~ s ~~t~~ ad ~~í~~ s ~~ti~~ cas o ~~fi~~ c ~~i~~ a ~~l~~ es ~~-~~ Documen ~~t~~ os sob ~~r~~ e po ~~líti~~ cas Ca ~~lifi~~ ca su p ~~r~~ ec ~~i~~ s ~~i~~ ón de 0 a ~~1~~ 0. """ ) ~~# Et~~ apa 2: ~~Fl~~ u ~~j~~ o de ~~tr~~ aba ~~j~~ o de ve ~~rifi~~ cac ~~i~~ ón de da ~~t~~ os pa ~~r~~ a ~~l~~ e ~~l~~ a ~~f~~ ac ~~t~~ <u>_check_wo</u> ~~r~~ k ~~fl~~ ow ~~=~~ Pa ~~r~~ a ~~ll~~ e ~~l~~ Agen ~~t~~ ( name ~~=~~ ' ~~f~~ ac ~~t~~ <u>_check_pa</u> ~~r~~ a ~~ll~~ e ~~l~~ ', sub_agen ~~t~~ s ~~=~~ [ ~~f~~ ac ~~t~~ <u>_checke</u> ~~r~~ <u>_a,</u> ~~f~~ ac ~~t~~ <u>_checke</u> ~~r~~ <u>_b,</u> ~~f~~ ac ~~t~~ <u>_checke</u> ~~r~~ <u>_c]</u> ) 

14 



~~# Et~~ apa 3a: Ve ~~rifi~~ cado ~~r~~ de ca ~~li~~ dad qua ~~lit~~ y_checke ~~r =~~ L ~~l~~ mAgen ~~t~~ ( mode ~~l=~~ 'gem ~~i~~ n ~~i-~~ 2.5 ~~-fl~~ ash', name ~~=~~ 'qua ~~lit~~ y_checke ~~r~~ ', ou ~~t~~ pu ~~t~~ <u>_key</u> ~~=~~ 'qua ~~lit~~ y_sco ~~r~~ e', ~~i~~ ns ~~tr~~ uc ~~ti~~ on ~~=~~ """ ~~E~~ va ~~l~~ úa ~~l~~ a ca ~~li~~ dad gene ~~r~~ a ~~l~~ de ~~l~~ con ~~t~~ en ~~i~~ do en ~~f~~ unc ~~i~~ ón de ~~l~~ os ~~r~~ esu ~~lt~~ ados de ~~l~~ a ve ~~rifi~~ cac ~~i~~ ón de da ~~t~~ os: ~~- F~~ uen ~~t~~ es académ ~~i~~ cas: { ~~f~~ ac ~~t~~ <u>_check_academ</u> ~~i~~ c} ~~- F~~ uen ~~t~~ es de no ~~ti~~ c ~~i~~ as: { ~~f~~ ac ~~t~~ <u>_check_news}</u> 

- ~~F~~ uen ~~t~~ es o ~~fi~~ c ~~i~~ a ~~l~~ es: { ~~f~~ ac ~~t~~ <u>_check_o</u> ~~ffi~~ c ~~i~~ a ~~l~~ } 

Ca ~~l~~ cu ~~l~~ a ~~l~~ a PUN ~~T~~ UAC ~~I~~ ÓN D ~~E~~ CAL ~~I~~ DAD G ~~E~~ N ~~E~~ RAL (de 0 a ~~1~~ 0). S ~~i l~~ a pun ~~t~~ uac ~~i~~ ón es ~~i~~ gua ~~l~~ o supe ~~ri~~ o ~~r~~ a 8, e ~~l~~ con ~~t~~ en ~~i~~ do cump ~~l~~ e con ~~l~~ os es ~~t~~ ánda ~~r~~ es de ca ~~li~~ dad. S ~~i l~~ a pun ~~t~~ uac ~~i~~ ón es ~~i~~ n ~~f~~ e ~~ri~~ o ~~r~~ a 8, e ~~l~~ con ~~t~~ en ~~i~~ do debe me ~~j~~ o ~~r~~ a ~~r~~ se. Devue ~~l~~ ve so ~~l~~ o ~~l~~ a pun ~~t~~ uac ~~i~~ ón numé ~~ri~~ ca. """ ) ~~# Et~~ apa 3b: Con ~~tr~~ o ~~l~~ de ca ~~li~~ dad ( ~~fi~~ na ~~li~~ zac ~~i~~ ón d ~~i~~ nám ~~i~~ ca) c ~~l~~ ass Qua ~~lit~~ yGa ~~t~~ eAgen ~~t~~ (BaseAgen ~~t~~ ): """ ~~E~~ sca ~~l~~ a ~~l~~ a ~~fi~~ na ~~li~~ zac ~~i~~ ón de ~~l~~ buc ~~l~~ e s ~~i~~ se a ~~l~~ canza e ~~l~~ umb ~~r~~ a ~~l~~ de ca ~~li~~ dad""" async de ~~f~~ <u>_</u> ~~r~~ un_async_ ~~i~~ mp ~~l~~ (se ~~lf~~ , c ~~t~~ x): qua ~~lit~~ y_sco ~~r~~ e_ ~~t~~ ex ~~t =~~ c ~~t~~ x.sess ~~i~~ on.s ~~t~~ a ~~t~~ e.ge ~~t~~ ('qua ~~lit~~ y_sco ~~r~~ e', '0') ~~tr~~ y: qua ~~lit~~ y_sco ~~r~~ e ~~= fl~~ oa ~~t~~ (qua ~~lit~~ y_sco ~~r~~ e_ ~~t~~ ex ~~t~~ ) excep ~~t~~ Va ~~l~~ ue ~~Err~~ o ~~r~~ : qua ~~lit~~ y_sco ~~r~~ e ~~=~~ 0 ~~if~~ qua ~~lit~~ y_sco ~~r~~ e > ~~=~~ 8: y ~~i~~ e ~~l~~ d ~~E~~ ven ~~t~~ ( au ~~t~~ ho ~~r=~~ se ~~lf~~ .name, ~~t~~ ex ~~t=f~~ "✓ Se a ~~l~~ canzó e ~~l~~ umb ~~r~~ a ~~l~~ de ca ~~li~~ dad: {qua ~~lit~~ y_sco ~~r~~ e}/ ~~1~~ 0", ac ~~ti~~ ons ~~=E~~ ven ~~t~~ Ac ~~ti~~ ons(esca ~~l~~ a ~~t~~ e ~~=Tr~~ ue) ~~#~~ Sa ~~lir~~ an ~~t~~ es de ~~l~~ buc ~~l~~ e ) e ~~l~~ se: y ~~i~~ e ~~l~~ d ~~E~~ ven ~~t~~ ( au ~~t~~ ho ~~r=~~ se ~~lf~~ .name, ~~t~~ ex ~~t=f~~ "Ca ~~li~~ dad po ~~r~~ deba ~~j~~ o de ~~l~~ umb ~~r~~ a ~~l~~ : {qua ~~lit~~ y_sco ~~r~~ e}/ ~~1~~ 0. S ~~i~~ gue me ~~j~~ o ~~r~~ ando e ~~l~~ con ~~t~~ en ~~i~~ do." ) 



15 

qua ~~lit~~ y_ga ~~t~~ e ~~=~~ Qua ~~lit~~ yGa ~~t~~ eAgen ~~t~~ (name ~~=~~ 'qua ~~lit~~ y_ga ~~t~~ e') ~~# Et~~ apa 3c: Pe ~~rf~~ ecc ~~i~~ onado ~~r~~ de con ~~t~~ en ~~i~~ do con ~~t~~ en ~~t~~ <u>_</u> ~~r~~ e ~~fi~~ ne ~~r =~~ L ~~l~~ mAgen ~~t~~ ( mode ~~l=~~ 'gem ~~i~~ n ~~i-~~ 2.5 ~~-fl~~ ash', name ~~=~~ 'con ~~t~~ en ~~t~~ <u>_</u> ~~r~~ e ~~fi~~ ne ~~r~~ ', ou ~~t~~ pu ~~t~~ <u>_key</u> ~~=~~ 'con ~~t~~ en ~~t~~ ', ~~#~~ Ac ~~t~~ ua ~~li~~ za e ~~l~~ con ~~t~~ en ~~i~~ do de ~~l~~ es ~~t~~ ado ~~i~~ ns ~~tr~~ uc ~~ti~~ on ~~=~~ """ Me ~~j~~ o ~~r~~ a e ~~l~~ con ~~t~~ en ~~i~~ do en ~~f~~ unc ~~i~~ ón de ~~l~~ os comen ~~t~~ a ~~ri~~ os de ~~l~~ a ve ~~rifi~~ cac ~~i~~ ón de da ~~t~~ os: ~~-~~ Con ~~t~~ en ~~i~~ do académ ~~i~~ co: { ~~f~~ ac ~~t~~ <u>_check_academ</u> ~~i~~ c} ~~-~~ No ~~ti~~ c ~~i~~ as: { ~~f~~ ac ~~t~~ <u>_check_news}</u> ~~-~~ Con ~~t~~ en ~~i~~ do o ~~fi~~ c ~~i~~ a ~~l~~ : { ~~f~~ ac ~~t~~ <u>_check_o</u> ~~ffi~~ c ~~i~~ a ~~l~~ } Me ~~j~~ o ~~r~~ a ~~l~~ a p ~~r~~ ec ~~i~~ s ~~i~~ ón, ~~l~~ a c ~~l~~ a ~~ri~~ dad y ~~l~~ as c ~~it~~ as de ~~l~~ as ~~f~~ uen ~~t~~ es. Devue ~~l~~ ve con ~~t~~ en ~~i~~ do me ~~j~~ o ~~r~~ ado. """ ) ~~# Et~~ apa 3: Buc ~~l~~ e de ca ~~li~~ dad (con ~~fi~~ na ~~li~~ zac ~~i~~ ón d ~~i~~ nám ~~i~~ ca) qua ~~lit~~ y_ ~~l~~ oop ~~=~~ LoopAgen ~~t~~ ( name ~~=~~ 'qua ~~lit~~ y_ ~~l~~ oop', sub_agen ~~t~~ s ~~=~~ [qua ~~lit~~ y_checke ~~r~~ , qua ~~lit~~ y_ga ~~t~~ e, con ~~t~~ en ~~t~~ <u>_</u> ~~r~~ e ~~fi~~ ne ~~r~~ ], max_ ~~it~~ e ~~r~~ a ~~ti~~ ons ~~=~~ 5 ~~#~~ L ~~í~~ m ~~it~~ e de segu ~~ri~~ dad ) ~~#~~ Agen ~~t~~ e ~~r~~ a ~~í~~ z: ~~Fl~~ u ~~j~~ o de ~~tr~~ aba ~~j~~ o secuenc ~~i~~ a ~~l r~~ oo ~~t~~ <u>_agen</u> ~~t =~~ Sequen ~~ti~~ a ~~l~~ Agen ~~t~~ ( name ~~=~~ 'con ~~t~~ en ~~t~~ <u>_qa_sys</u> ~~t~~ em', sub_agen ~~t~~ s ~~=~~ [ ~~i~~ n ~~t~~ ake_agen ~~t~~ , ~~f~~ ac ~~t~~ <u>_check_wo</u> ~~r~~ k ~~fl~~ ow, ~~#~~ Ve ~~rifi~~ cac ~~i~~ ón de da ~~t~~ os pa ~~r~~ a ~~l~~ e ~~l~~ a qua ~~lit~~ y_ ~~l~~ oop ~~#~~ Me ~~j~~ o ~~r~~ a ~~it~~ e ~~r~~ a ~~ti~~ va de ~~l~~ a ca ~~li~~ dad ] ) 



### Explicación del código 

Este flujo de trabajo del curso 8 demuestra patrones de organización avanzados implementados sin cambios en producción. Analicemos la arquitectura: 

#### Bloque 1: Agente de recepción de contenido (de la línea 574 a la 584) 

Py ~~t~~ hon ~~i~~ n ~~t~~ ake_agen ~~t =~~ L ~~l~~ mAgen ~~t~~ ( name ~~=~~ 'con ~~t~~ en ~~t~~ <u>_</u> ~~i~~ n ~~t~~ ake', ~~i~~ ns ~~tr~~ uc ~~ti~~ on ~~=~~ "Recop ~~il~~ a con ~~t~~ en ~~i~~ do pa ~~r~~ a ~~l~~ a ve ~~rifi~~ cac ~~i~~ ón de da ~~t~~ os…" ) 





16 

Es el punto de entrada del flujo de trabajo. 

Recopila y estructura el contenido para la validación. 

Almacena contenido en el estado de la sesión para los agentes posteriores. 



#### Bloque 2: Verificación de datos paralela (de la línea 586 a la 642) 

Py ~~t~~ hon ~~f~~ ac ~~t~~ <u>_check_wo</u> ~~r~~ k ~~fl~~ ow ~~=~~ Pa ~~r~~ a ~~ll~~ e ~~l~~ Agen ~~t~~ ( sub_agen ~~t~~ s ~~=~~ [ ~~f~~ ac ~~t~~ <u>_checke</u> ~~r~~ <u>_a,</u> ~~f~~ ac ~~t~~ <u>_checke</u> ~~r~~ <u>_b,</u> ~~f~~ ac ~~t~~ <u>_checke</u> ~~r~~ <u>_c]</u> ) 

- Tres validadores se ejecutan de forma simultánea (ejecución paralela). 

- Cada validador verifica diferentes aspectos (fuentes, afirmaciones y estadísticas). 

- Usa claves de estado de sesión distintas (fact_check_a, fact_check_b y fact_check_c) para evitar conflictos. 

- Qué debes tener en cuenta: Las ramas paralelas funcionan de forma idéntica en producción y en localhost. 

#### Bloque 3: Bucle de calidad con finalización dinámica (de la línea 644 a la 709) 

Py ~~t~~ hon qua ~~lit~~ y_ ~~l~~ oop ~~=~~ LoopAgen ~~t~~ ( sub_agen ~~t~~ s ~~=~~ [qua ~~lit~~ y_checke ~~r~~ , qua ~~lit~~ y_ga ~~t~~ e, con ~~t~~ en ~~t~~ <u>_</u> ~~r~~ e ~~fi~~ ne ~~r~~ ], max_ ~~it~~ e ~~r~~ a ~~ti~~ ons ~~=~~ 5 ) 

- Se realiza una mejora iterativa de la calidad (hasta 5 iteraciones). 

- qua ~~lit~~ y_ga ~~t~~ e usa ~~E~~ ven ~~t~~ Ac ~~ti~~ ons.BR ~~E~~ AK_LOOP para la finalización dinámica. 

- El bucle continúa hasta que se alcanza el umbral de calidad o la cantidad máxima de iteraciones. 

- Qué debes tener en cuenta: EventActions funciona en producción (control del bucle dinámico). 

#### Bloque 4: Organización secuencial raíz (de la línea 712 a la 719) 

Py ~~t~~ hon ~~r~~ oo ~~t~~ <u>_agen</u> ~~t =~~ Sequen ~~ti~~ a ~~l~~ Agen ~~t~~ ( sub_agen ~~t~~ s ~~=~~ [ ~~i~~ n ~~t~~ ake_agen ~~t~~ , ~~# Et~~ apa ~~1~~ : Recop ~~il~~ ac ~~i~~ ón ~~f~~ ac ~~t~~ <u>_check_wo</u> ~~r~~ k ~~fl~~ ow, ~~# Et~~ apa 2: Va ~~li~~ dac ~~i~~ ón (pa ~~r~~ a ~~l~~ e ~~l~~ a) qua ~~lit~~ y_ ~~l~~ oop ~~# Et~~ apa 3: Me ~~j~~ o ~~r~~ a (buc ~~l~~ e) ] ) 

17 

- Coordina las tres etapas del flujo de trabajo de forma secuencial. 

- Cada etapa se completa antes de que comience la siguiente. 

- Qué debes tener en cuenta: No es necesario hacer cambios en el código para la implementación en producción. 

### Características clave de producción: 

Cuenta con persistencia del estado de la sesión (VertexAiSessionService automático). 

La ejecución paralela funciona de forma idéntica. 

Las funciones de finalización dinámica del bucle funcionan correctamente. 

Se realizan implementaciones de organización complejas con un solo comando. 

Crea ~~r~~ equ ~~ir~~ emen ~~t~~ s. ~~t~~ x ~~t~~ : 

Ninguno goog ~~l~~ e ~~-~~ c ~~l~~ oud ~~-~~ a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m[adk,agen ~~t~~ <u>_eng</u> ~~i~~ nes]> ~~=1~~ . ~~111~~ 

### Paso 2: Implementa un flujo de trabajo complejo 

Shell ~~# I~~ mp ~~l~~ emen ~~t~~ a e ~~l~~ agen ~~t~~ e en Agen ~~t E~~ ng ~~i~~ ne adk dep ~~l~~ oy agen ~~t-~~ eng ~~i~~ ne \ 

~~--~~ p ~~r~~ o ~~j~~ ec ~~t=~~ $GOOGL ~~E~~ <u>_CLOUD_PROJ</u> ~~E~~ C ~~T~~ \ ~~--r~~ eg ~~i~~ on ~~=~~ $GOOGL ~~E~~ <u>_CLOUD_LOCA</u> ~~TI~~ ON \ 

- ~~--~~ s ~~t~~ ag ~~i~~ ng_bucke ~~t=~~ $S ~~T~~ AG ~~I~~ NG_BUCK ~~ET~~ \ 

- ~~--~~ d ~~i~~ sp ~~l~~ ay_name ~~=~~ "S ~~i~~ s ~~t~~ ema de QA de con ~~t~~ en ~~i~~ do (cu ~~r~~ so 8)" \ 

- con ~~t~~ en ~~t~~ <u>_qa_sys</u> ~~t~~ em/ 

#### Resultado esperado: 

Ninguno ~~I~~ mp ~~l~~ emen ~~t~~ ando e ~~l~~ agen ~~t~~ e "con ~~t~~ en ~~t~~ <u>_qa_sys</u> ~~t~~ em"... ... ✓ ~~El~~ agen ~~t~~ e se ~~i~~ mp ~~l~~ emen ~~t~~ ó co ~~rr~~ ec ~~t~~ amen ~~t~~ e Nomb ~~r~~ e de ~~l r~~ ecu ~~r~~ so: p ~~r~~ o ~~j~~ ec ~~t~~ s/.../ ~~r~~ eason ~~i~~ ng ~~E~~ ng ~~i~~ nes/98765432 ~~1~~ 



18 

### Paso 3: Prueba el flujo de trabajo complejo 

Py ~~t~~ hon """ P ~~r~~ ueba e ~~l fl~~ u ~~j~~ o de ~~tr~~ aba ~~j~~ o de ~~l~~ cu ~~r~~ so 8 ~~i~~ mp ~~l~~ emen ~~t~~ ado """ ~~i~~ mpo ~~rt~~ os ~~fr~~ om goog ~~l~~ e.c ~~l~~ oud ~~i~~ mpo ~~rt~~ a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m 

a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m. ~~i~~ n ~~it~~ ( p ~~r~~ o ~~j~~ ec ~~t=~~ os.env ~~ir~~ on["GOOGL ~~E~~ <u>_CLOUD_PROJ</u> ~~E~~ C ~~T~~ "], ~~l~~ oca ~~ti~~ on ~~=~~ os.env ~~ir~~ on["GOOGL ~~E~~ <u>_CLOUD_LOCA</u> ~~TI~~ ON"] ) 



~~#~~ Conéc ~~t~~ a ~~t~~ e a ~~l fl~~ u ~~j~~ o de ~~tr~~ aba ~~j~~ o ~~i~~ mp ~~l~~ emen ~~t~~ ado ~~r~~ esou ~~r~~ ce_name ~~=~~ "p ~~r~~ o ~~j~~ ec ~~t~~ s/…/ ~~r~~ eason ~~i~~ ng ~~E~~ ng ~~i~~ nes/98765432 ~~1~~ " ~~# El~~ nomb ~~r~~ e de ~~t~~ u ~~r~~ ecu ~~r~~ so ~~r~~ emo ~~t~~ e_app ~~=~~ a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m.Reason ~~i~~ ng ~~E~~ ng ~~i~~ ne( ~~r~~ esou ~~r~~ ce_name) 

~~#~~ P ~~r~~ ueba con con ~~t~~ en ~~i~~ do de mues ~~tr~~ a ~~t~~ es ~~t~~ <u>_con</u> ~~t~~ en ~~t =~~ """ 

Las compu ~~t~~ ado ~~r~~ as cuán ~~ti~~ cas usan b ~~it~~ s cuán ~~ti~~ cos (cúb ~~it~~ s) que pueden ex ~~i~~ s ~~tir~~ de ~~f~~ o ~~r~~ ma supe ~~r~~ pues ~~t~~ a, ~~l~~ o que ~~l~~ es pe ~~r~~ m ~~it~~ e p ~~r~~ ocesa ~~r i~~ n ~~f~~ o ~~r~~ mac ~~i~~ ón exponenc ~~i~~ a ~~l~~ men ~~t~~ e más ~~r~~ áp ~~i~~ do que ~~l~~ as compu ~~t~~ ado ~~r~~ as c ~~l~~ ás ~~i~~ cas. Los avances ~~r~~ ec ~~i~~ en ~~t~~ es de ~~I~~ BM y Goog ~~l~~ e demos ~~tr~~ a ~~r~~ on ~~l~~ a sup ~~r~~ emac ~~í~~ a cuán ~~ti~~ ca. 

""" 

p ~~ri~~ n ~~t~~ ("P ~~r~~ ueba de ~~l fl~~ u ~~j~~ o de ~~tr~~ aba ~~j~~ o comp ~~l~~ e ~~j~~ o de ~~l~~ cu ~~r~~ so 8 (secuenc ~~i~~ a ~~l +~~ pa ~~r~~ a ~~l~~ e ~~l~~ o ~~+~~ de buc ~~l~~ e)") p ~~ri~~ n ~~t~~ (" ~~=~~ " * 70) p ~~ri~~ n ~~t~~ ( ~~f~~ "Con ~~t~~ en ~~i~~ do de en ~~tr~~ ada: { ~~t~~ es ~~t~~ <u>_con</u> ~~t~~ en ~~t~~ }") p ~~ri~~ n ~~t~~ (" ~~=~~ " * 70) 

~~r~~ esponse ~~= r~~ emo ~~t~~ e_app.que ~~r~~ y( ~~i~~ npu ~~t=t~~ es ~~t~~ <u>_con</u> ~~t~~ en ~~t~~ ) 

p ~~ri~~ n ~~t~~ ("\nRespues ~~t~~ a de ~~l fl~~ u ~~j~~ o de ~~tr~~ aba ~~j~~ o:") p ~~ri~~ n ~~t~~ ( ~~r~~ esponse) p ~~ri~~ n ~~t~~ (" ~~=~~ " * 70) p ~~ri~~ n ~~t~~ ("✓ ~~El fl~~ u ~~j~~ o de ~~tr~~ aba ~~j~~ o comp ~~l~~ e ~~j~~ o se ~~i~~ mp ~~l~~ emen ~~t~~ ó y es ~~t~~ á en ~~f~~ unc ~~i~~ onam ~~i~~ en ~~t~~ o") 

### En qué debes fijarte 

El mismo flujo de trabajo del curso 8 se ejecuta en producción. 

No es necesario realizar cambios en el código. 

ParallelAgent (verificación de datos de 3 fuentes) funciona de forma idéntica. 

LoopAgent con funciones de finalización dinámica de EventActions funciona correctamente. 

VertexAiSessionService controla la coordinación de estados. 

19 

## Conclusiones principales 

Ya implementaste tu primer agente en Vertex AI Agent Engine y lo probaste con varios métodos. El proceso de implementación es muy simple: un solo comando transforma tu agente local en un servicio de producción con persistencia automática de la sesión, escalamiento y disponibilidad las 24 horas, todos los días. 

##### Implementación en Agent Engine: 

- Un solo comando: adk dep ~~l~~ oy agen ~~t-~~ eng ~~i~~ ne implementa los agentes en producción 

- Sin conocimientos sobre Docker: El ADK controla la creación de contenedores de manera automática 

- Servicio de sesión automático: VertexAiSessionService está configurado de forma predeterminada 

- Tiempo de implementación: Entre 5 y 10 minutos (incluida la creación del contenedor) 

Integración del curso 8: 

- Flujos de trabajo complejos: Los agentes secuenciales, paralelos y de bucle se implementan sin cambios 

- Las herramientas funcionan: Herramientas de funciones y herramientas integradas que funcionan en producción 

- El estado persiste: VertexAiSessionService brinda persistencia 

- Las EventActions funcionan: Las funciones de finalización dinámica del bucle funcionan correctamente. 

##### Qué se implementa: 

- Tu código de agente: Todos los agentes del ADK (LlmAgent y agentes personalizados) 

- Dependencias: Desde ~~r~~ equ ~~ir~~ emen ~~t~~ s. ~~t~~ x ~~t~~ 

- Persistencia de la sesión: VertexAiSessionService (automático) 

- Infraestructura administrada: Google Cloud se encarga del escalamiento y la disponibilidad 

##### Prueba de los agentes implementados: 

- S DK de Python: 

- a ~~i~~ p ~~l~~ a ~~tf~~ o ~~r~~ m.Reason ~~i~~ ng ~~E~~ ng ~~i~~ ne ( ~~r~~ esou ~~r~~ ce_name) 

- Consola de Cloud: Interfaz de prueba integrada 

- API de REST: curl con token de autenticación 

- Registros: Consola de Cloud → Ver registros 

##### Estado de la sesión de producción (extensión del curso 4): 

   - Los 4 espacios de nombres funcionan: ~~t~~ emp:, session, use ~~r~~ : y  app: 

   - InMemorySessionService → VertexAiSessionService: Actualización automática 

   - No es necesario realizar cambios en el código: Las mismas variables de estado funcionan Persistente después de los reinicios: Estado de la sesión conservado 

- Listo para producción: 

   - Disponibilidad 24/7: El agente se ejecuta de forma continua 

   - Acceso público: Extremo que se puede compartir 

   - Escalado automático: Control de los aumentos repentinos de tráfico 

   - Infraestructura administrada: Administración sin servidores 



20 

