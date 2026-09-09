

# Memoria de producción (Memory Bank) 

## Introducción 



### La brecha de memoria 

Después de la parte 2, implementaste agentes con persistencia de la sesión. Sin embargo, hay una brecha: 

Py ~~t~~ hon ~~#~~ Ses ~~i~~ ón ~~1~~ ( ~~l~~ unes): Usua ~~ri~~ o: "P ~~r~~ e ~~fi~~ e ~~r~~ o ~~l~~ as no ~~tifi~~ cac ~~i~~ ones po ~~r~~ co ~~rr~~ eo e ~~l~~ ec ~~tr~~ ón ~~i~~ co a ~~l~~ as de SMS" Agen ~~t~~ e: "¡ ~~E~~ n ~~t~~ end ~~i~~ do!" ~~#~~ Ses ~~i~~ ón 2 (v ~~i~~ e ~~r~~ nes, d ~~if~~ e ~~r~~ en ~~t~~ e conve ~~r~~ sac ~~i~~ ón): Usua ~~ri~~ o: "¿Cómo se me no ~~tifi~~ ca ~~r~~ á?" Agen ~~t~~ e: "No ~~r~~ ecue ~~r~~ do" ❌ ~~# El~~ es ~~t~~ ado de ~~l~~ a ses ~~i~~ ón es ~~t~~ á ~~li~~ m ~~it~~ ado a ~~l~~ a conve ~~r~~ sac ~~i~~ ón 

La brecha: El estado de la sesión solo persiste en una conversación. Memory Bank permite el aprendizaje en todas las conversaciones. Estado de la sesión vs. Memory Bank 

### Breve comparación 

|Característica|Estado de la sesión (curso 4)|Memory Bank|
|---|---|---|
|Alcance|Conversación actual|Todas las conversaciones|
|Persistencia|Fin de la sesión|Indefinidamente|
|Caso de uso|Flujo de conversación|Aprendizaje a largoplazo|
|Acceso|Directo ({va~~ri~~ab~~l~~e})|Através de una herramienta<br>(búsqueda semántica)|





### Cuándo usar cada opción 

#### Memory Bank (curso 9): 

Estado de la sesión (curso 4): 

   - "El usuario prefiere las notificaciones por correo electrónico" (se aprendió esto la semana pasada) 

- Tema actual: ~~t~~ emp:cu ~~rr~~ en ~~t~~ <u>_</u> ~~t~~ op ~~i~~ c 

- Cantidad de solicitudes: ~~r~~ eques ~~t~~ <u>_coun</u> ~~t~~ 

   - "Tuvo un problema con la facturación antes" (se aprendió el mes pasado) 

- Preferencias del usuario: use ~~r~~ : ~~ti~~ e ~~r~~ 

- "Le interesa la API de Enterprise" (se aprendió a partir de varias conversaciones) 



<!-- Start of picture text -->
avés de una<br>cé t e r a).<br>r<br><!-- End of picture text -->

### Funcionan en conjunto 

Ninguno 

~~E~~ s ~~t~~ ado de ~~l~~ a ses ~~i~~ ón: "¿Qué sucede en ~~E~~ S ~~T~~ A conve ~~r~~ sac ~~i~~ ón?" Memo ~~r~~ y Bank:         "¿Qué ap ~~r~~ end ~~í E~~ N ~~T~~ ODAS ~~l~~ as conve ~~r~~ sac ~~i~~ ones?" 

## Cómo funciona Memory Bank 

### El ciclo de vida (conceptual) 

##### Ninguno 

- ~~1~~ . ~~El~~ usua ~~ri~~ o ~~i~~ n ~~t~~ e ~~r~~ ac ~~t~~ úa con e ~~l~~ agen ~~t~~ e. 

2. La conve ~~r~~ sac ~~i~~ ón se gua ~~r~~ da en Memo ~~r~~ y Bank (au ~~t~~ omá ~~ti~~ camen ~~t~~ e a ~~tr~~ avés de una devo ~~l~~ uc ~~i~~ ón de ~~ll~~ amada). 

3. ~~El~~ LLM ex ~~tr~~ ae ~~i~~ n ~~f~~ o ~~r~~ mac ~~i~~ ón s ~~i~~ gn ~~ifi~~ ca ~~ti~~ va (p ~~r~~ e ~~f~~ e ~~r~~ enc ~~i~~ as, ~~i~~ n ~~t~~ e ~~r~~ eses, e ~~t~~ cé ~~t~~ e ~~r~~ a). 4. ~~E~~ n una conve ~~r~~ sac ~~i~~ ón pos ~~t~~ e ~~ri~~ o ~~r~~ , e ~~l~~ agen ~~t~~ e usa ~~l~~ a he ~~rr~~ am ~~i~~ en ~~t~~ a pa ~~r~~ a busca ~~r~~ memo ~~ri~~ as pasadas. 

5. ~~El~~ agen ~~t~~ e ~~r~~ esponde con con ~~t~~ ex ~~t~~ o h ~~i~~ s ~~t~~ ó ~~ri~~ co. 

### Componentes clave 

VertexAiMemoryBankService: 

- Servicio administrado (sin configuración de base de datos) 

- Extracción potenciada por LLM (almacenamiento inteligente, no sin procesar) 

#### PreloadMemoryTool: 

   - Recupera automáticamente las memorias relevantes 

   - El agente usa memorias para fundamentar las respuestas 

- Búsqueda semántica (comprende la intención) 

### Devolución de llamada de guardado automático: 

Py ~~t~~ hon 

~~#~~ Después de cada ~~t~~ u ~~r~~ no, gua ~~r~~ da ~~r~~ en Memo ~~r~~ y Bank async de ~~f~~ au ~~t~~ o_save_sess ~~i~~ on_ ~~t~~ o_memo ~~r~~ y_ca ~~ll~~ back(ca ~~ll~~ back_con ~~t~~ ex ~~t~~ ): awa ~~it~~ ca ~~ll~~ back_con ~~t~~ ex ~~t~~ ._ ~~i~~ nvoca ~~ti~~ on_con ~~t~~ ex ~~t~~ .memo ~~r~~ y_se ~~r~~ v ~~i~~ ce.add_sess ~~i~~ on_ ~~t~~ o_memo ~~r~~ y( ca ~~ll~~ back_con ~~t~~ ex ~~t~~ ._ ~~i~~ nvoca ~~ti~~ on_con ~~t~~ ex ~~t~~ .sess ~~i~~ on) 

2 

