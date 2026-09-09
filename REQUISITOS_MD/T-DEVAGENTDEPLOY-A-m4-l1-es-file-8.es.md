

# Ejemplo práctico Implementa el agente meteorológico en Cloud Run 



Paso 1: Crea el agente 

Shell mkd ~~ir~~ wea ~~t~~ he ~~r~~ <u>_agen</u> ~~t~~ <u>_c</u> ~~l~~ oud_ ~~r~~ un cd wea ~~t~~ he ~~r~~ <u>_agen</u> ~~t~~ <u>_c</u> ~~l~~ oud_ ~~r~~ un 

Crea agen ~~t~~ .py: 

Py ~~t~~ hon ~~fr~~ om goog ~~l~~ e.adk.agen ~~t~~ s ~~i~~ mpo ~~rt~~ L ~~l~~ mAgen ~~t~~ 

~~r~~ oo ~~t~~ <u>_agen</u> ~~t =~~ L ~~l~~ mAgen ~~t~~ ( mode ~~l=~~ 'gem ~~i~~ n ~~i-~~ 2.5 ~~-fl~~ ash', name ~~=~~ 'wea ~~t~~ he ~~r~~ <u>_agen</u> ~~t~~ ', desc ~~ri~~ p ~~ti~~ on ~~=~~ 'Wea ~~t~~ he ~~r~~ agen ~~t~~ on C ~~l~~ oud Run', ~~i~~ ns ~~tr~~ uc ~~ti~~ on ~~=~~ ''' 

~~Er~~ es un as ~~i~~ s ~~t~~ en ~~t~~ e me ~~t~~ eo ~~r~~ o ~~l~~ óg ~~i~~ co ú ~~til~~ . P ~~r~~ opo ~~r~~ c ~~i~~ ona ~~i~~ n ~~f~~ o ~~r~~ mac ~~i~~ ón sob ~~r~~ e e ~~l~~ c ~~li~~ ma de c ~~i~~ udades de ~~t~~ odo e ~~l~~ mundo. ''' ) 



Crea __ ~~i~~ n ~~it~~ <u>__.py:</u> 

Py ~~t~~ hon ~~fr~~ om .agen ~~t i~~ mpo ~~rt r~~ oo ~~t~~ <u>_agen</u> ~~t~~ 





### Paso 2: Implementa el agente 

Shell 

expo ~~rt~~ GOOGL ~~E~~ <u>_CLOUD_PROJ</u> ~~E~~ C ~~T=~~ "you ~~r-~~ p ~~r~~ o ~~j~~ ec ~~t-i~~ d" expo ~~rt~~ GOOGL ~~E~~ <u>_CLOUD_LOCA</u> ~~TI~~ ON ~~=~~ "us ~~-~~ cen ~~tr~~ a ~~l1~~ " 

adk dep ~~l~~ oy c ~~l~~ oud_ ~~r~~ un \ 

~~--~~ p ~~r~~ o ~~j~~ ec ~~t=~~ $GOOGL ~~E~~ <u>_CLOUD_PROJ</u> ~~E~~ C ~~T~~ \ ~~--r~~ eg ~~i~~ on ~~=~~ $GOOGL ~~E~~ <u>_CLOUD_LOCA</u> ~~TI~~ ON \ ~~--~~ se ~~r~~ v ~~i~~ ce_name ~~=~~ wea ~~t~~ he ~~r-~~ agen ~~t~~ \ ~~--~~ w ~~it~~ h_u ~~i~~ \ wea ~~t~~ he ~~r~~ <u>_agen</u> ~~t~~ <u>_c</u> ~~l~~ oud_ ~~r~~ un/ 

### Resultado esperado: 

Ninguno 

C ~~r~~ eando e ~~l~~ con ~~t~~ enedo ~~r~~ ... ~~I~~ mp ~~l~~ emen ~~t~~ ando en C ~~l~~ oud Run... ✓ Se ~~r~~ v ~~i~~ c ~~i~~ o ~~i~~ mp ~~l~~ emen ~~t~~ ado 

URL de ~~l~~ se ~~r~~ v ~~i~~ c ~~i~~ o: h ~~tt~~ ps://wea ~~t~~ he ~~r-~~ agen ~~t-~~ xyz ~~1~~ 23.us ~~-~~ cen ~~tr~~ a ~~l1~~ . ~~r~~ un.app 

### Paso 3: Prueba 

Abre la URL del servicio en tu navegador para acceder a la IU web (similar a adk web). 

# Accede a los agentes implementados 

IU web (con ~~--~~ w ~~it~~ h_u ~~i~~ ) 

### Ve a la URL del servicio en el navegador: 

Ninguno 

h ~~tt~~ ps://wea ~~t~~ he ~~r-~~ agen ~~t-~~ xyz ~~1~~ 23.us ~~-~~ cen ~~tr~~ a ~~l1~~ . ~~r~~ un.app 

### Interfaz de chat interactiva, comparte la URL con el equipo para realizar pruebas. 

## Acceso a la API 

Shell S ~~E~~ RV ~~I~~ C ~~E~~ <u>_URL</u> ~~=~~ "h ~~tt~~ ps://wea ~~t~~ he ~~r-~~ agen ~~t-~~ xyz ~~1~~ 23.us ~~-~~ cen ~~tr~~ a ~~l1~~ . ~~r~~ un.app" 

cu ~~rl -~~ X POS ~~T~~ $S ~~E~~ RV ~~I~~ C ~~E~~ <u>_URL/ap</u> ~~i~~ /que ~~r~~ y \ ~~-H~~ "Con ~~t~~ en ~~t-T~~ ype: app ~~li~~ ca ~~ti~~ on/ ~~j~~ son" \ 

~~-~~ d '{" ~~i~~ npu ~~t~~ ": "¿Cómo es ~~t~~ á e ~~l~~ c ~~li~~ ma en Sea ~~ttl~~ e?"}' 



2 

## Acceso a Python 

Py ~~t~~ hon ~~i~~ mpo ~~rt r~~ eques ~~t~~ s 

S ~~E~~ RV ~~I~~ C ~~E~~ <u>_URL</u> ~~=~~ "h ~~tt~~ ps://wea ~~t~~ he ~~r-~~ agen ~~t-~~ xyz ~~1~~ 23.us ~~-~~ cen ~~tr~~ a ~~l1~~ . ~~r~~ un.app" 

~~r~~ esponse ~~= r~~ eques ~~t~~ s.pos ~~t~~ ( ~~f~~ "{S ~~E~~ RV ~~I~~ C ~~E~~ <u>_URL}/ap</u> ~~i~~ /que ~~r~~ y", ~~j~~ son ~~=~~ {" ~~i~~ npu ~~t~~ ": "¿Cómo es ~~t~~ á e ~~l~~ c ~~li~~ ma en Lond ~~r~~ es?"} ) p ~~ri~~ n ~~t~~ ( ~~r~~ esponse. ~~j~~ son()) 

# Nota sobre el servicio de sesión 

Importante: Cloud Run NO configura automáticamente el servicio de sesión, como sí lo hace Agent Engine. Para la persistencia en producción, configura VertexAiSessionService en tu agente: 

Py ~~t~~ hon 

~~fr~~ om goog ~~l~~ e.adk.sess ~~i~~ ons ~~i~~ mpo ~~rt~~ Ve ~~rt~~ exA ~~i~~ Sess ~~i~~ onSe ~~r~~ v ~~i~~ ce 

sess ~~i~~ on_se ~~r~~ v ~~i~~ ce ~~=~~ Ve ~~rt~~ exA ~~i~~ Sess ~~i~~ onSe ~~r~~ v ~~i~~ ce( 

p ~~r~~ o ~~j~~ ec ~~t=~~ os.env ~~ir~~ on.ge ~~t~~ ('GOOGL ~~E~~ <u>_CLOUD_PROJ</u> ~~E~~ C ~~T~~ '), ~~l~~ oca ~~ti~~ on ~~=~~ os.env ~~ir~~ on.ge ~~t~~ ('GOOGL ~~E~~ <u>_CLOUD_LOCA</u> ~~TI~~ ON') ) 

## Comparación 

|Plataforma|Servicio de sesión|
|---|---|
|Agent Engine|Automático|
|Cloud Run|Configuraciónmanual|











3 

# Conclusiones principales 

Implementaste un agente en Cloud Run, lo que te brinda una ruta de implementación alternativa con mayor flexibilidad. Cloud Run es particularmente útil cuando necesitas una IU web implementada junto con tu agente o tienes requisitos de contenedor personalizados. Para la mayoría de los agentes estándar del ADK, Agent Engine sigue siendo la opción más sencilla. 

Características básicas de Cloud Run 

adk depl ~~o~~ y cl ~~o~~ ud_r ~~u~~ n empaqueta e implementa el agente. ~~--~~ w ~~it~~ h_u ~~i~~ incluye la interfaz web. Devuelve una URL HTTPS pública para acceder al agente. 

Cuándo usar Cloud Run 



Cuando quieras que la IU web se implemente con el agente 

Cuando haya requisitos personalizados de contenedores 



Cuando haya una infraestructura existente de Cloud Run 

### Cuándo usar Agent Engine 

Cuando crees agentes estándar del ADK (más simples) Cuando necesites servicios automáticos de sesión y memoria 

Cuando prefieras una infraestructura completamente administrada 

El mismo agente en diferentes plataformas 

El código de tu agente funciona tanto en Agent Engine como en Cloud Run, solo que con diferentes comandos de implementación. 

4 

