# Ficha PZ-003B - Decision humana del plan en ensayo local

**Estado:** COMPLETADA_Y_ACEPTADA  
**Fecha:** 30 de agosto de 2026  
**Fecha de aprobacion humana:** 30 de agosto de 2026  
**Fecha de aceptacion final humana:** 30 de agosto de 2026  
**Contrato rector:** `CONTRATO-MVP-v1.md`, version `1.2-aprobada`  
**Dependencia:** PZ-003A, `COMPLETADA_Y_ACEPTADA`  
**Constructor inicial autorizado:** Antigravity  
**Correcciones:** Codex, solo con autorizacion humana concreta y archivos enumerados; Copilot revisa sin editar.

> Construccion autorizada mediante "de acuerdo" (seccion 14) y pieza corregida aceptada posteriormente por el usuario humano (seccion 15). El recorrido manual no esta acreditado y sigue pendiente; CT-009 no se cierra. La aceptacion de esta subpieza SIMULADA no autoriza ejecutar tareas ni aprueba una mision del producto.

## 1. Que vamos a crear, en sencillo

Una puerta de decision sobre el plan de prueba: mostrar que se propone y permitir al usuario aprobarlo, rechazarlo o pedir cambios. Aprobar vincula la decision al contenido exacto; si ese contenido cambia, la respuesta anterior no sirve para autorizarlo.

Aunque el usuario apruebe, este ensayo se detiene antes de ejecutar tareas. No llama agentes, no produce un VBP y no guarda la sesion al cerrar el proceso.

## 2. Posicion y frontera de la pieza

Segunda subpieza del bloque 3, `Recorrido vertical Mision a VBP`. Reutiliza PZ-003A para llegar a `PLAN_EN_REVISION` y agrega exclusivamente la puerta de decision del plan.

- Aprobar: `PLAN_EN_REVISION -> AUTORIZADA_PARA_EJECUTAR`, mediante MT-005, y detenerse.
- Rechazar o solicitar cambios: registrar la decision y permanecer en `PLAN_EN_REVISION`, sin autorizar tareas.
- No responder: conservar la solicitud pendiente; no interpretar silencio como aprobacion.
- Brief incompleto: conservar `ACLARACION_REQUERIDA`, sin abrir solicitud de aprobacion.

`AUTORIZADA_PARA_EJECUTAR` no significa `EN_EJECUCION`: MT-006 y toda ejecucion estan fuera de esta ficha. No se inventa un estado `PLAN_RECHAZADO`, ni se usa `VBP_RECHAZADO` para un plan.

Esta subpieza aporta un ensayo acotado a RF-006 y RF-007. No completa el bloque 3 ni reemplaza el bloque 12 de aprobaciones integradas, pausa, continuidad y VBP.

## 3. Fuentes obligatorias

1. `AGENTS.md` y `TEAM-WORKFLOW.md` completos.
2. `CONTRATO-MVP-v1.md`: 0 a 4; 6.4; 7 (especialmente RF-006, RF-007, RF-020, RF-022, RF-025, RF-027 y RF-029); 8A; 10; 11.1 a 11.5; 13; Anexo C.0, C.3 y C.9.
3. `FICHA-PZ-003A-ENTRADA-Y-PLAN-CONTROLADO.md`, incluidas correccion y aceptacion final; `INFORME-CONSTRUCCION-PZ-003A.md` y `REVISION-COPILOT-PZ-003A.md`, distinguiendo historia de resultado corregido.
4. `contracts/core/README.md`, los cinco schemas y `state-machine.json`; MT-005, AT-001/AT-002, reglas de aprobacion, idempotencia y RI-001/RI-002/RI-003. Consultar los ejemplos de aprobacion y transiciones.
5. `app/demo_intake.py`, `examples/demo_mission.json`, las tres pruebas actuales, `README.md` y `pyproject.toml`.
6. Esta ficha completa y su registro de aprobacion, antes de editar.

No es necesario consultar red ni adoptar tecnologias adicionales. El checklist aporta controles; no obliga a implementar infraestructura en esta subpieza.

## 4. Decisiones heredadas e implementacion aprobada

### 4.1 Ya aprobado

Funciones deterministas para permisos y transiciones; decisiones reservadas al usuario humano; version exacta; idempotencia; errores tipados; datos de ensayo etiquetados `SIMULADA`; ausencia de razonamiento interno almacenado. El perfil local de v0 no implica login, contrasenas ni firmas digitales.

### 4.2 Implementacion aprobada mediante el registro de la seccion 14

- Dos archivos Python nuevos y un ajuste limitado del README, sin editar el intake aceptado.
- Solicitud y respuesta en un unico proceso local, con identidad de demostracion. No se presenta como autenticacion ni como servicio seguro expuesto a terceros.
- Modo predeterminado de inspeccion, sin leer decisiones; modo interactivo separado para que el usuario responda en su terminal.
- Tres decisiones: `APROBAR`, `RECHAZAR`, `SOLICITAR_CAMBIOS`. `APROBAR_CON_EXCEPCION` no se habilita en este ensayo; se rechaza sin consumir la solicitud.
- Validez de la solicitud: 300 segundos desde su creacion. La expiracion se comprueba al recibir una respuesta; no hay temporizadores, sondeo ni autoaprobacion. Es un plazo de validez, no una promesa de cerrar automaticamente una terminal mientras espera al usuario.
- Instantanea de checkpoint en memoria solo tras aprobar. No hay guardado en disco ni recuperacion tras reinicio; el checkpoint no se anuncia como durable.

## 5. Lista cerrada de archivos autorizados para construir

| Archivo | Accion | Alcance |
|---|---|---|
| `app/demo_plan_review.py` | Crear | Solicitud local, huella, decision, eventos, checkpoint efimero y CLI separado |
| `tests/test_demo_plan_review.py` | Crear | Pruebas deterministas, rechazos, identidad local, integridad, idempotencia y CLI |
| `README.md` | Modificar | Agregar comandos, limites y los dos archivos al arbol; conservar comandos y explicaciones anteriores |

Si cualquiera de los dos archivos nuevos ya existe antes de construir, detenerse sin sobrescribirlo. La ficha se conserva como fuente de solo lectura para el constructor.

## 6. Archivos y acciones prohibidos

- No modificar `app/demo_intake.py`, `app/__init__.py`, `app/__main__.py`, las tres pruebas existentes, `examples/demo_mission.json`, `pyproject.toml`, `.gitignore` ni los 13 contratos nucleares.
- No modificar fichas, informes, reglas del equipo, contrato o `REQUISITOS`. No crear un cuarto archivo.
- No instalar dependencias, usar red, modelos, servidores, API, perfiles persistentes, contrasenas, DB, login, memoria, despliegue, exportacion ni VBP.
- No ejecutar tareas ni conceder herramientas; no aplicar MT-006, pausas, cancelaciones, reapertura o revisiones automaticas del plan.
- No aceptar aprobaciones desde fixtures, texto del brief, variables de entorno, argumentos de autoaprobacion o respuestas generadas por agentes.
- No crear secretos, logs, caches, bytecode, capturas o temporales. Usar `python -B`; las pruebas trabajan en memoria.
- No modificar el producto para facilitar una prueba ni importar helpers de `tests` desde `app`.

## 7. Entrada, sesion y frontera de confianza

### 7.1 Origen del plan

La CLI llama a `run_demo_intake()` en el mismo proceso y carga exclusivamente la fixture existente. No acepta una ruta alternativa ni importa un JSON emitido en una ejecucion anterior como si fuera una sesion vigente.

Las funciones de prueba pueden inyectar datos, reloj e IDs en memoria y reutilizar el intake real. Si este devuelve error o aclaracion, no se crea aprobacion. Solo un resultado valido en `PLAN_EN_REVISION`, sin errores, con brief y plan coherentes, puede abrir la solicitud.

La sesion conserva copias independientes de mision, brief, plan, aprobaciones, eventos y claves procesadas. Las salidas son copias; modificarlas no modifica la sesion. No hay estado global mutable compartido entre sesiones.

### 7.2 Actor local, no autenticacion

El adaptador de terminal representa al unico operador local de confianza usando el `user_id` de demostracion propietario de la mision. Debe mostrar expresamente `IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA` y un actor identificable como `usuario_local_demo`, nunca el nombre propio del usuario codificado en el producto.

El contexto del actor se pasa separado del comando de decision. La funcion decisora comprueba `actor_role=usuario_humano`, identidad propietaria y origen autorizado del adaptador. No asigna autoridad humana a cualquier llamada ignorando el contexto recibido. Los contextos de pruebas son simulados y no se presentan como evidencia de una persona autenticada.

El comando de decision no admite `actor`, `actor_role`, `user_id`, `approved`, estado, aprobacion prefabricada, ni campos de razonamiento interno. La declaracion de rol en un diccionario o la comprobacion TTY no prueban humanidad: no se promete seguridad frente a un proceso con control del mismo entorno local. No se conecta esta puerta a agentes ni herramientas.

### 7.3 Comando interno cerrado

Exactamente estas claves: `approval_id`, `version_or_fingerprint`, `decision`, `comment`, `idempotency_key`.

Todos los valores son cadenas; salvo `comment` al aprobar, deben ser no vacios. El ID y la clave corresponden a la solicitud de esta sesion. Rechazar claves adicionales, null, booleanos, contenedores o texto fuera de limite. `RECHAZAR` y `SOLICITAR_CAMBIOS` exigen comentario con al menos un caracter no blanco. No se interpreta texto libre como decision ni se usa eval.

Limites heredados: 4000 caracteres por cadena, 20 elementos por coleccion y 64 KiB para la fixture. La lectura de cada linea interactiva se limita a 4096 caracteres, sin lectura no acotada; desbordamiento implica error y salida sin decision. Solo un envio por ejecucion interactiva y, cuando corresponda, una linea adicional de comentario; no hay bucle automatico de reintentos.

## 8. Huella y solicitud pendiente

### 8.1 Contenido exacto sometido

Construir un objeto para la huella con exactamente: `mission_id`, `user_id`, `brief_version`, `plan_version`, `brief` completo y `plan` completo. Confirmar concordancia de IDs y versiones entre registros y estructura del plan mediante la validacion existente. Incluir tareas, dependencias, criterios, herramientas, limites y riesgos: no basta con titulo o numero de version.

Calcular SHA-256 sobre UTF-8 de `json.dumps(objeto, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)`. Usar `sha256:<64 hexadecimales minusculos>`. Es una convencion interna reproducible de este ensayo, no una firma digital ni una afirmacion de estandar universal de canonicalizacion.

La huella excluye fechas de eventos, estado mutable de la mision y la propia aprobacion. Si cambia cualquier dato del objeto sometido, la huella cambia; reordenar claves de diccionario no cambia la huella. No se ordenan arrays ni se normaliza contenido para ocultar cambios.

Antes de aceptar una decision se compara la huella del comando, la guardada en la solicitud y la recalculada sobre el contenido vigente. Una discrepancia devuelve `INVALID_INPUT`, no consume la solicitud ni autoriza la mision. Editar/reversionar el plan y abrir otra solicitud queda para otra subpieza.

### 8.2 Registro y evento de solicitud

Crear un registro conforme a `approval.schema.json`: ID unico, usuario destinatario, actor local de demo, `actor_role=usuario_humano`, `action_approved` ligado a mision y plan v1, huella, fecha UTC, `decision=null`, `comment=""`, `conditions=[]`, `expiration=creacion+300 segundos`, `status=PENDIENTE` y clave de idempotencia propia.

El actor del registro pendiente identifica a quien debera responder, no una decision emitida. El evento de solicitud lo emite `sistema`, con etiqueta `SIMULADA` y referencia a la aprobacion pendiente.

Vincular el ID en `mission.approval_refs` no significa autorizar: siempre se debe comprobar el registro, su decision y su huella. Tras crear la solicitud, la mision permanece `PLAN_EN_REVISION`, `record_version` pasa de 3 a 4 y se agrega un cuarto evento de registro sin cambio de estado. No inventar una transicion de maquina para este evento informativo.

## 9. Decision atomica, expiracion y doble respuesta

### 9.1 Controles previos

Comprobar contexto autorizado, tipos, ID/clave, pertenencia de registros, huella, estado y reglas nucleares. IDs inexistentes producen `NOT_FOUND`; actor ajeno produce `PERMISSION_DENIED`; contenido invalido o conflicto produce `INVALID_INPUT`; contrato incompatible o fallo interno produce `SYSTEM_ERROR`.

Cargar y comprobar AT-001/AT-002 y sus autoridades, las reglas de idempotencia y MT-005. Si faltan, se duplican o son incompatibles con el tramo, detenerse. No evaluar sus guardias textuales como codigo ni limitarse a comprobar que aparece un ID.

Preparar y validar copias del resultado completo antes de reemplazar el estado de sesion: un fallo no deja una aprobacion consumida con mision sin autorizar, ni una mision autorizada sin registro/evento/checkpoint valido. El error devuelto no equivale a un cambio silencioso del estado interno.

### 9.2 Aprobar

Solo `APROBAR`, por el actor local autorizado y antes de expirar, puede consumir la solicitud mediante AT-001 y aplicar MT-005. Esta ultima debe ser exactamente `PLAN_EN_REVISION -> AUTORIZADA_PARA_EJECUTAR`, `authority=solo_usuario_humano` y `requires_human_approval=true`.

Registrar `decision=APROBAR`, `status=CONSUMIDA`, timestamp de respuesta y comentario. Mantener identidad, ID, accion, huella, expiracion y clave originales. Preservar una copia historica de la solicitud pendiente sin reutilizarla como registro vigente.

Actualizar mision a version 5, generar un evento de decision con `actor_role=usuario_humano`, `related_approval_id` resoluble y huella en la referencia al artefacto. Generar el checkpoint de 9.5. Ninguna tarea sale de `PENDIENTE`; `active_task=null`; intentos, peticiones a agentes y gasto siguen en cero. Salida: `Plan SIMULADA autorizado por decision local explicita. No ejecutado; sesion no persistida.`

### 9.3 Rechazar o solicitar cambios

Consumir la solicitud una sola vez mediante AT-001, guardar decision, motivo, actor y fecha, y agregar evento de decision sin cambio del estado de mision. La version del registro pasa a 5; `current_state` sigue en `PLAN_EN_REVISION`, sin checkpoint nuevo ni tareas activas.

No aplicar MT-005, no borrar el plan, no generar otra version y no reabrir automaticamente la solicitud consumida. `CONSUMIDA` significa respondida, no necesariamente aprobada. Explicar que el plan no fue autorizado y que su revision queda fuera de este ensayo.

### 9.4 Expiracion e idempotencia

Para una solicitud aun pendiente, `ahora >= expiration` aplica AT-002: `EXPIRADA`, `decision=null`, fecha de expiracion conservada, evento de sistema sin cambio de estado y version de mision incrementada una vez. Devolver error `PERMISSION_DENIED` y detenerse sin autorizar. Una solicitud expirada no puede consumirse ni regresar a pendiente.

La primera decision valida queda registrada con el comando completo y contexto autorizado. Misma clave y mismo contenido devuelve una copia del resultado original sin nuevo evento, version, aprobacion ni checkpoint. No recalcular fechas o IDs para ese duplicado. Misma clave y distinto contenido devuelve `INVALID_INPUT`, sin sobrescribir. Otra clave o segunda respuesta para una solicitud consumida tampoco produce efectos.

Verificar identidad antes de devolver un resultado previo. Una respuesta ya consumida no se convierte en expirada por repetirla mas tarde. El primer consumo y su registro de idempotencia deben ser atomicos en memoria. No se prometen idempotencia durable, concurrencia de usuarios o proteccion entre procesos.

### 9.5 Checkpoint efimero e integridad

Solo al aprobar, crear un checkpoint conforme al schema existente y vincularlo en `mission.last_checkpoint_id`, dentro de la misma actualizacion a version 5. Capturar estado autorizado, `resumable_state=null`, las cuatro tareas pendientes con cero intentos, dependencias reales no satisfechas, contadores, duracion medida del ensayo y gasto cero. No inventar duracion cero si hubo espera: permitir inyectar un reloj monotono en pruebas.

`mission_version` coincide con la version final de mision. `authorizations` contiene el ID de la aprobacion consumida con `APROBAR`, no una respuesta de rechazo. `artifacts=["brief", "plan"]` son referencias simbolicas que deben resolverse a esos objetos del mismo sobre/mision; no son rutas de archivos ni evidencia externa.

Calcular `fingerprint` sobre todos los campos del checkpoint salvo `fingerprint`, con la misma serializacion de 8.1. Usar ID y clave propios, estables al repetir la misma decision. Validar RI-001/RI-002/RI-003, pertenencia a la mision y resolucion del brief, plan y tareas. Referencias ausentes: `NOT_FOUND`, sin publicar resultado autorizado parcial.

Este objeto es una instantanea en memoria, no almacenamiento durable ni mecanismo de reanudacion. No implementar una operacion para cargarlo o continuar tras reinicio.

## 10. CLI y salida verificable

### 10.1 Inspeccion segura por defecto

`python -B -m app.demo_plan_review`

Genera la mision y la solicitud pendiente, emite un unico JSON a stdout y termina con codigo 3. No lee stdin ni fabrica una decision. Si el intake necesita aclaracion, conserva esa rama sin solicitud. Cada ejecucion es una sesion nueva; el JSON no permite reanudarla despues.

### 10.2 Interaccion local explicita

`python -B -m app.demo_plan_review --interactive`

Exige stdin y stderr interactivos; con entrada redirigida o entorno no interactivo se detiene sin leer una decision y devuelve `PERMISSION_DENIED`. No admite `--approve`, `--yes`, JSON de decisiones por tuberia ni parametros de actor.

Mostrar en stderr, antes de leer: advertencia `SIMULADA`, identidad local no autenticada, mision, brief completo, plan completo con cuatro tareas/limites/riesgos, ID de solicitud, huella exacta, vencimiento y aclaracion de que no se ejecutara nada. Mostrar texto como dato, escapando controles de terminal, sin interpretar ANSI del contenido. stdout queda reservado al JSON final.

Aceptar exclusivamente una primera linea con `APROBAR <huella>`, `RECHAZAR <huella>`, `SOLICITAR_CAMBIOS <huella>` o `SALIR`. Para rechazo/cambios pedir una segunda linea de motivo. La CLI construye los campos de ID y clave desde su sesion, no desde la fixture. Un texto ambiguo o una huella distinta no autoriza.

`SALIR`, EOF o interrupcion del usuario no consumen la solicitud ni cancelan la mision: devuelven el sobre actual sin decision y codigo 3. No confundir salir del programa con `CANCELADA`. Antes de la respuesta no se consume la solicitud, no se ejecutan tareas y no se invocan modelos.

### 10.3 Sobre, codigos y errores

Conservar las ocho claves de salida del intake y agregar solamente `approvals`, `approval_history`, `checkpoints` y `review`. Cada coleccion empieza vacia cuando no hay solicitud. `approvals` contiene como maximo el registro vigente; `approval_history` conserva como maximo la solicitud original y la version terminal, sin alterar una decision ya emitida; `checkpoints` contiene como maximo uno.

`review` es null sin solicitud; en otro caso contiene exactamente `simulation_status=SIMULADA`, `approval_id`, `version_or_fingerprint`, `identity_scope=IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA` y `durable=false`. Los objetos nucleares no reciben campos extra para estas etiquetas. Eventos, advertencias y resumen conservan `SIMULADA` visible.

Codigos: 0 solo para plan autorizado; 3 para pendiente, aclaracion, salida sin decidir o decision negativa valida; 1 para entrada/politica/operacion invalida o fallo interno; 2 para archivo/referencia ausente. Rechazo y solicitud de cambios validos no son errores tecnicos: la decision y `next_action` los distinguen de pendiente.

Los errores siguen el schema nuclear, sin reintento automatico, filtracion de trazas, secretos o texto de excepciones. Dependencia ausente: JSON de error claro y no cero, sin fingir validacion ni instalarla. Mantener JSON valido incluso con texto Unicode. Fallos internos no se convierten en exito. Los comandos anteriores `python -B -m app` y `python -B -m app.demo_intake` conservan su salida y comportamiento.

## 11. Pruebas y criterios de aceptacion

Pruebas en memoria con reloj/IDs controlados. Los mocks se limitan a fronteras IO, terminal, relojes o copias de contratos; no reemplazan validadores ni la funcion de decision que se quiere comprobar. Ningun test se presenta como aprobacion humana real.

| ID | Evidencia exigida |
|---|---|
| CB-01 | Modo predeterminado: solicitud PENDIENTE, decision null, estado PLAN_EN_REVISION, cuatro tareas pendientes y codigo 3; no lectura de stdin |
| CB-02 | Aprobacion explicita: solicitud CONSUMIDA/APROBAR, MT-005 valida, mision version 5 autorizada, un evento decisorio y un checkpoint coherente; no MT-006 |
| CB-03 | RECHAZAR y SOLICITAR_CAMBIOS consumen con motivo y mantienen PLAN_EN_REVISION; motivo ausente, null o blanco se rechaza sin consumo |
| CB-04 | Actor no humano, otro usuario, origen no permitido e inyecciones de actor/estado/aprobacion por comando o fixture se rechazan sin efectos |
| CB-05 | Huella de otra mision/version o cambios en brief, riesgos, tareas, dependencias, criterios, herramientas y limites no autorizan; reordenar claves no cambia huella |
| CB-06 | Primera respuesta aplicada una vez; duplicado identico devuelve el resultado original; contenido diferente con misma clave y segunda decision con otra clave se rechazan; comprobar conteos, IDs y versiones |
| CB-07 | Justo antes del vencimiento puede responder; exactamente al vencimiento o despues no puede; EXPIRADA y CONSUMIDA son terminales; duplicado de decision consumida posterior al vencimiento no crea efectos |
| CB-08 | Contratos manipulados en memoria: MT-005/AT-001/AT-002 ausentes, duplicados, con pares/autoridad incompatibles o politica booleana incorrecta detienen el flujo; no se modifican contratos reales |
| CB-09 | Validar mision, aprobaciones e historia, eventos, checkpoint y errores con schemas reales y comprobacion efectiva de fechas; referencias ausentes y cruzadas no producen autorizacion parcial |
| CB-10 | Fallo inducido antes de publicar resultado demuestra atomicidad; modificar salidas no cambia sesion; sesiones nuevas no comparten decisiones, claves, IDs ni listas |
| CB-11 | Brief incompleto o intake invalido no abre solicitud; APROBAR_CON_EXCEPCION y comandos/claves/tipos desconocidos se rechazan explicitamente |
| CB-12 | CLI: un JSON stdout, contexto completo antes de leer decision en stderr, codigos correctos; no TTY, EOF, interrupcion, SALIR, huella errada, linea excesiva y dependencia ausente son controlados |
| CB-13 | Interceptar red, escrituras, procesos externos e importacion para detectar intentos incluso si se captura su excepcion; cero tareas activas, gasto y peticiones a agentes |
| CB-14 | Las 49 pruebas anteriores pasan sin cambios; matriz nuclear 1440/10 preservada; solo dos archivos nuevos y README modificado; 13 contratos intactos y cero residuos |

Ejecutar y devolver salidas completas de:

1. Versiones de Python y jsonschema ya instaladas, sin instalar.
2. `python -B -m app`.
3. `python -B -m app.demo_intake`.
4. `python -B -m app.demo_plan_review` (salida 3 esperada, no fallo de construccion).
5. `python -B -m unittest discover -s tests -v`.

El constructor prueba las ramas interactivas con entradas y contexto de terminal simulados en tests, etiquetandolos como tales. No responde en nombre del usuario a la CLI real. Tras la revision tecnica, el usuario puede realizar el recorrido manual; si no se realizo, el informe debe indicarlo, sin sustituirlo por una prueba automatica presentada como intervencion humana.

Capturar antes de editar inventario de rutas, SHA-256, tamanos y fechas del proyecto; verificar ausencia de los dos archivos nuevos. Devolver la linea base y la comparacion final en la conversacion, no en un archivo adicional. Comparar por ruta todos los preexistentes, no solo conteos; el unico existente autorizado a cambiar es README.

## 12. Trazabilidad al checklist y limites

| Referencia | Aporte esperado de esta subpieza | No demostrado por este ensayo |
|---|---|---|
| RF-006 / C.9 | Contexto previo, tres decisiones explicitas y una sola respuesta por solicitud | Aprobacion integrada de VBP, UI final y seguridad del entorno desplegado |
| RF-007 / RF-029 | No avanzar sin decision valida o con contenido distinto | Motor real de ejecucion y edicion/reversionado de alcance |
| RF-020 / C.9 | Actor local, fecha, huella, resultado, eventos e idempotencia en memoria | Auditoria durable y aislamiento entre procesos |
| RF-022 / C.3 | Checkpoint estructural efimero vinculado a aprobacion | Reinicio, recuperacion y persistencia; CT-003/CT-008 no se cierran |
| CT-009 / C.9 | Puerta local con espera explicita y pruebas negativas | CT-009 no se marca completo por mocks: queda pendiente la evidencia humana e integrada aplicable |

No marcar el gate del concurso ni el bloque 12 completos. No se modifica el checklist rector en esta construccion.

Una conversacion de construccion, sin delegacion; objetivo 45 minutos, detenerse y reportar si hace falta ampliar el encargo. Una mision y una solicitud por proceso; una respuesta valida; sin bucles de correccion, ejecucion ni reintento. Cero costo externo, instalaciones, red o modelos. Maximo dos rondas de correccion, cada una con autorizacion humana concreta.

Detenerse antes de editar si no existe aprobacion de esta ficha, faltan dependencias disponibles, existen los archivos nuevos, no se puede capturar la linea base, hay edicion simultanea o se requiere modificar un contrato/archivo excluido. No ampliar silenciosamente la pieza para resolverlo.

## 13. Prompt historico para la construccion autorizada en Antigravity

La construccion inicial ya termino. Este prompt se conserva como historial; no autoriza reconstruir ni sobrescribir los archivos existentes.

```text
Actua como constructor inicial de PZ-003B en OminAIHQ. Lee completa FICHA-PZ-003B-DECISION-HUMANA-DEL-PLAN.md y sus fuentes obligatorias.

Comprueba aprobacion humana expresa posterior de esta ficha o su registro actualizado. Si sigue PROPUESTA_PENDIENTE_DE_APROBACION_HUMANA y no hay aprobacion posterior expresa, detente sin editar. El mensaje "sigamos" y la aceptacion de PZ-003A no autorizan construir PZ-003B.

Crea exclusivamente app/demo_plan_review.py y tests/test_demo_plan_review.py. Modifica exclusivamente README.md en los apartados autorizados. No toques app/demo_intake.py, las pruebas anteriores, la fixture, configuracion, contratos, fichas o informes; no crees otros archivos.

Implementa la puerta local SIMULADA de decision del plan: pendiente por defecto; en modo interactivo, decision explicita sobre huella exacta; aprobar solo llega a AUTORIZADA_PARA_EJECUTAR y se detiene. Rechazar/pedir cambios conservan PLAN_EN_REVISION con decision registrada. Sin autoaprobacion, ejecucion, agentes, persistencia, login, VBP ni red.

Respeta identidad local no autenticada, contexto separado del comando, AT-001/AT-002/MT-005, atomicidad, idempotencia, expiracion y checkpoint solo en memoria. No inventes estados ni uses eval. No respondas por el usuario a la CLI real; usa tests simulados para probar sus ramas.

Antes de editar presenta plan, versiones disponibles, ausencia de archivos nuevos y manifiesto previo. Sin instalaciones, delegacion, caches o temporales; usa python -B.

Demuestra CB-01 a CB-14 con aserciones reales y conserva las 49 pruebas existentes. Devuelve archivos exactos, salidas, conteos reales de pruebas/subcasos, hashes antes/despues, residuos, limitaciones y recorrido manual pendiente si no se realizo. No declares aprobacion final de PZ-003B ni del MVP. Si necesitas otro archivo o decision, detente y pregunta.
```

## 14. Registro de aprobacion humana

```text
Pieza: PZ-003B
Decision: APROBADA
Autorizacion de construir: OTORGADA
Fecha de aprobacion: 30 de agosto de 2026
Aprobado por: usuario humano (A0 actual del proyecto)
Referencia: respuesta expresa "de acuerdo" a "Apruebas construir PZ-003B con esos tres archivos y ese alcance?"
Constructor inicial autorizado: Antigravity
Archivos nuevos autorizados: app/demo_plan_review.py; tests/test_demo_plan_review.py
Archivo existente autorizado para modificar: README.md (solo comandos, limites y arbol)
Modificaciones de codigo/contratos aceptados: ninguna
Instalaciones: ninguna
Alcance autorizado: puerta de decision local SIMULADA del plan, hasta AUTORIZADA_PARA_EJECUTAR, sin ejecucion; registros y checkpoint efimeros; solicitud valida por 300 segundos
Correcciones posteriores: requieren autorizacion humana concreta por ronda y lista exacta de archivos
Aceptacion final de la pieza: OTORGADA; ver seccion 15
```

## 15. Aceptacion final humana de PZ-003B

```text
Pieza: PZ-003B
Decision: ACEPTADA
Estado: COMPLETADA_Y_ACEPTADA
Version aceptada: construccion inicial con correccion 1 revisada
Fecha de aceptacion: 30 de agosto de 2026
Aprobado por: usuario humano
Referencia: mensaje "registra la aprobacion de la pieza faltante", posterior a la identificacion explicita de PZ-003B como pendiente de aceptacion final
Alcance: puerta local SIMULADA de decision del plan; sin ejecucion de tareas, agentes, persistencia, VBP ni red
Revision tecnica: evidencia previa de la correccion 1; no se ejecutaron nuevas pruebas al registrar esta decision
Revision independiente: dictamen previo de Copilot APTO_PARA_APROBACION_HUMANA
Recorrido manual humano: PENDIENTE; no se ha aportado evidencia de realizacion
CT-009 y aprobaciones integradas: PENDIENTES DE EVIDENCIA APLICABLE; no se cierran por esta aceptacion
Efecto sobre PZ-003C: dependencia de aceptacion humana satisfecha; conservar sus demas condiciones tecnicas previas
Permisos adicionales de codigo, gasto o acciones externas: NINGUNO
```

La solicitud actual registra la aceptacion final de la pieza, no una respuesta a la CLI del producto ni una aprobacion automatica de piezas futuras. Se conserva expresamente la limitacion del recorrido manual pendiente.

Huellas SHA-256 de los archivos de la pieza al registrar la aceptacion. La comparacion con el inventario previo confirma que no cambiaron desde la actualizacion documental anterior; estas huellas no sustituyen las pruebas.

| Archivo | SHA-256 |
|---|---|
| `app/demo_plan_review.py` | `b4ec7152bb8327e4de33efa8d8854e1e480927c06937c58b13b15ec048dd4c71` |
| `tests/test_demo_plan_review.py` | `74ec722fd9d3bd709bbc2938c293b88f252c4d589b19563e6cfd0cee5e1e28f2` |
| `README.md` | `092bf4c22bd3d6b44cd65e2742f77bf7f85f12657f3fe7b9418055d68844bc72` |
