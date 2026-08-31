# Ficha PZ-003A - Entrada de mision y plan controlado

**Estado:** COMPLETADA_Y_ACEPTADA  
**Fecha:** 30 de agosto de 2026  
**Fecha de aprobacion humana:** 30 de agosto de 2026  
**Fecha de aceptacion final:** 30 de agosto de 2026  
**Contrato rector:** `CONTRATO-MVP-v1.md`, version `1.2-aprobada`  
**Dependencias:** PZ-001A y PZ-002A, ambas `COMPLETADA_Y_ACEPTADA`  
**Constructor inicial autorizado:** Antigravity  
**Correcciones posteriores:** Codex, con autorizacion humana concreta por ronda; Copilot revisa sin editar.

> Subpieza completada y aceptada por el usuario humano; ver el registro final de la seccion 16. Se conserva el encargo inicial como historial. El cierre acepta exclusivamente el ensayo SIMULADA de esta ficha, no el bloque 3 completo ni capacidades fuera de alcance.

## 1. Que vamos a crear, en sencillo

Un primer ensayo del recorrido de una mision: leer un ejemplo ficticio, ordenar sus campos, mostrar un plan de prueba y detenerse antes de ejecutarlo.

Si faltan datos, mostrara cuales. No inventara respuestas ni aprobara el plan. Todo el ensayo se identificara como `SIMULADA`.

## 2. Posicion dentro del contrato

Es la primera subpieza de la Pieza 3, `Recorrido vertical Mision a VBP` (seccion 13 del contrato). No pretende completar esa pieza mayor.

El tramo aprobado para construir es:

`BORRADOR -> LISTA_PARA_PLAN -> PLAN_EN_REVISION`

La rama incompleta es:

`BORRADOR -> ACLARACION_REQUERIDA`

Ambas ramas se detienen. Una subpieza posterior, con otra ficha y aprobacion, incorporara la decision humana y continuara hacia el VBP. No se implementan ahora aprobaciones, especialistas reales ni exportacion final.

## 3. Fuentes obligatorias para el constructor

1. `AGENTS.md` y `TEAM-WORKFLOW.md` completos: roles actuales, dos rondas y autorizaciones concretas.
2. `CONTRATO-MVP-v1.md`: secciones 0 a 4, 5.1 a 5.3, 7, 8A, 10, 11.1 a 11.4, 13, y Anexo C.0, C.2, C.3, C.7 y C.9.
3. `FICHA-PZ-001A-CONTRATOS-NUCLEO.md` y `FICHA-PZ-002A-ESTRUCTURA-MINIMA.md`: alcance y aceptaciones.
4. `contracts/core/README.md`, los cinco schemas, `state-machine.json` y los seis ejemplos.
5. Los siete archivos de producto de PZ-002A.
6. Esta ficha completa y su registro de aprobacion, antes de cualquier edicion.

El contrato conserva registros historicos del reparto de roles. La decision humana posterior y los documentos vigentes del equipo rigen las correcciones de Codex; esta ficha no reescribe el contrato.

## 4. Decisiones heredadas e implementacion aprobada

Ya aprobado: Python 3.11+, contratos nucleares inmutables en esta pieza, funciones para lo determinista, una mision por recorrido, sin inferencia de aprobaciones y sin razonamiento interno almacenado.

Aprobado para construir mediante el registro de la seccion 14:

- Tramo limitado a entrada, comprobacion formal y plan preescrito de prueba.
- Ejecucion por terminal, sin modificar el comando base `python -B -m app`.
- Estado solo en memoria del proceso. Cada ejecucion es independiente; no se promete guardar, reanudar ni recordar.
- Tres archivos nuevos y dos modificaciones de documentacion/configuracion del proyecto, enumerados abajo.
- Declarar `jsonschema>=4.18,<5` tambien como extra opcional `demo`, sin cambiar `dependencies=[]` ni el extra `test`. Se utiliza la instalacion compatible ya disponible; no se instala nada.

## 5. Archivos permitidos para esta construccion

| Archivo | Accion permitida | Responsabilidad |
|---|---|---|
| `app/demo_intake.py` | Crear | Funciones deterministas del ensayo y entrada CLI del modulo; sin efectos al importar |
| `examples/demo_mission.json` | Crear | Un caso ficticio saneado, con brief y plantilla de plan marcados `SIMULADA` |
| `tests/test_demo_intake.py` | Crear | Pruebas de funciones, estados, contratos, rechazos y CLI |
| `README.md` | Modificar | Explicar el ensayo, su comando y limites; conservar las instrucciones del arranque base |
| `pyproject.toml` | Modificar | Agregar unicamente el extra opcional `demo = ["jsonschema>=4.18,<5"]` |

Si cualquiera de los tres archivos nuevos ya existe antes de construir, detenerse sin sobrescribirlo. No hay permiso implicito para un sexto archivo.

## 6. Archivos y acciones prohibidos

- No modificar los 13 archivos de `contracts/core`, los dos archivos actuales de `app`, las dos pruebas existentes ni `.gitignore`.
- No modificar contrato, fichas, informes, reglas del equipo ni `REQUISITOS`.
- No crear otro schema, framework, agente, prompt de agente, API, servidor, interfaz grafica, VBP, base de datos, checkpoint ni memoria persistente.
- No instalar ni actualizar paquetes, usar red, llamar modelos, ejecutar el contenido de un campo ni invocar herramientas desde el plan.
- No crear aprobaciones ficticias que parezcan humanas, agregar autoaprobacion ni aceptar un campo de entrada que fuerce un estado reservado.
- No crear `.env`, secretos, logs en disco, bytecode, caches, archivos temporales ni artefactos fuera de la lista. Las pruebas usan entradas en memoria.

## 7. Entrada y separacion de datos

El comando de prueba sera `python -B -m app.demo_intake`. Cargara exclusivamente `examples/demo_mission.json`, resuelto desde la raiz del proyecto y no desde una URL. No admite rutas arbitrarias, cargas privadas ni opciones para ejecutar o aprobar.

La fixture JSON es un dato tecnico del ensayo, no un nuevo formato de adjunto del producto. Debe ser ficticia, en espanol, y no tomar documentos empresariales privados.

Claves admitidas en la fixture:

- `simulation_status`: exactamente `SIMULADA`.
- `user_id` y `title`: cadenas no vacias; identidad de prueba, no perfil real ni prueba de autenticacion.
- `objective`, `context`, `expected_result`: cadenas; faltantes, null o vacias se reportan como campos por aclarar. Otros tipos se rechazan.
- `constraints`: lista de cadenas; puede estar vacia si se aporta explicitamente. Ausencia o null requiere aclaracion; otros tipos se rechazan.
- `assumptions` y `pending_decisions`: listas de cadenas, vacias por defecto. Si alguna no esta vacia, detenerse para aclaracion; no inferir aceptacion humana.
- `plan_template`: objeto con exactamente `title` (cadena no vacia), `tasks` (lista de cuatro tareas) y `risks` (lista de cadenas, puede estar vacia explicitamente). Son datos preescritos, nunca instrucciones ejecutables ni una respuesta generada por un agente real. Si el brief esta completo y falta la plantilla, la entrada se rechaza.

Rechazar claves desconocidas, especialmente intentos de inyectar `current_state`, `actor_role`, `approval_refs`, `approved` o campos de razonamiento interno. Rechazar JSON invalido, raiz no objeto, archivo mayor de 64 KiB y cadenas individuales mayores de 4000 caracteres. Las colecciones se limitan a 20 elementos; los cuatro pasos de la plantilla son una excepcion mas estricta, no una ampliacion de ese limite.

El registro `mission` debe cumplir el schema nuclear sin agregarle campos: el brief y el plan van separados en el sobre del ensayo. No se usan los campos libres para ocultar un segundo registro incompatible.

## 8. Comportamiento verificable

### 8.1 Creacion

- Generar `mission_id` unico, `brief_version=1`, `record_version=1`, estado `BORRADOR`, fechas UTC y evento de creacion.
- `approval_refs=[]`, `active_task=null`, `last_checkpoint_id=null`, `resumable_state=null`.
- Inicializar los limites exactos de 11.4 y todos los contadores a cero.
- Titulo identificable como ensayo: prefijo `[SIMULADA]`.
- Permitir inyectar reloj/generador de IDs en las funciones para pruebas repetibles, sin exponer opciones CLI para falsear autorizaciones.

### 8.2 Brief incompleto o con pendientes declarados

- Listar campos faltantes y pendientes; no rellenarlos con contenido ficticio.
- Aplicar exclusivamente MT-001 hacia `ACLARACION_REQUERIDA`, registrar evento y un ciclo de aclaracion.
- Devolver `plan=null`, sin tareas activas ni aprobaciones. La correccion del brief y su reanudacion quedan fuera de esta subpieza.
- Solo se detectan faltantes formales y pendientes declarados. No afirmar que el programa comprende ambiguedades semanticas.

### 8.3 Brief completo y plan de prueba

- Aplicar MT-002a hacia `LISTA_PARA_PLAN`. El papel del Chief of Staff es simulado, no un agente real.
- Vincular una copia independiente de la plantilla a `mission_id` y `brief_version=1`, con `plan_version=1` y etiqueta `SIMULADA`.
- La plantilla contiene exactamente cuatro tareas en secuencia: Research & Evidence Analyst, Product Architect, Delivery Planner y Governance & Risk. El Chief simulado prepara el plan; estas cuatro tareas solo se proponen y no se ejecutan.
- Cada tarea declara `task_id`, `objective`, `agent_role`, `input_refs`, `expected_output`, `acceptance_criteria`, `dependencies`, `allowed_tool_categories`, `limits`, `status=PENDIENTE` y `simulation_status=SIMULADA`.
- Los roles usan los identificadores del contrato nuclear; `input_refs` contiene la referencia simbolica `brief`, vinculada al brief de prueba de esta mision, y las dependencias apuntan a IDs de tareas de esta misma plantilla. Las categorias de herramientas se entregan vacias: esta pieza no concede su uso.
- `limits` por tarea: `max_attempts=2`, `max_seconds=300`, `max_budget_usd=0`; son limites del ensayo sin ejecucion. Cadenas obligatorias no vacias, listas con tipos correctos, IDs unicos, dependencias existentes y aciclicas, sin auto-dependencia. El primer paso no tiene dependencias; cada siguiente depende del anterior. La plantilla, tareas y limites rechazan claves desconocidas; no se permiten campos internos ocultos en estos objetos.
- Solo si la estructura es valida, aplicar MT-004 hacia `PLAN_EN_REVISION` y registrar el evento. La plantilla defectuosa se rechaza con `INVALID_INPUT`, sin alcanzar ese estado.
- Detenerse con el mensaje: `Plan SIMULADA presentado para revision. No aprobado y no ejecutado.`
- No aceptar comandos posteriores de ejecucion, aprobacion, rechazo ni cancelacion en este modulo. Esos comportamientos pertenecen a otra subpieza.

### 8.4 Estados, eventos y validacion

- Cargar los pares y autoridades de MT-001, MT-002a y MT-004 desde `state-machine.json`; no usar `eval`, ni interpretar sus guardias de texto como codigo.
- Implementar explicitamente las condiciones anteriores. No basta con copiar una lista de estados esperados en la salida.
- El evento inicial usa `previous_state=null`; cada transicion posterior conserva estado anterior/nuevo, ID unico, fecha, motivo resumido y version del registro actualizada.
- Los eventos de pasos del Chief simulado usan `actor_role=chief_of_staff`, un actor identificado como simulado y `SIMULADA` visible en `result_summary`. No se atribuyen a un agente real.
- Validar `mission` y cada evento con `Draft202012Validator` y comprobacion efectiva de fechas; no importar helpers de `tests` desde `app`.
- Los errores de entrada usan `INVALID_INPUT`; archivo de fixture ausente usa `NOT_FOUND`. Los errores estructurados siguen `error.schema.json`, sin reintento automatico. Los fallos internos deben ser visibles y nunca convertirse en salida exitosa.
- `agent_requests`, intentos de razonamiento, reintentos y gasto permanecen en cero. No hay bucles de aclaracion o de generacion ni temporizadores de agentes inexistentes.

## 9. Salida y CLI

Un unico JSON en stdout, sin banners que impidan parsearlo. Sobre con `simulation_status`, `mission`, `brief`, `plan`, `events`, `pending_fields`, `errors` y `next_action`.

- `simulation_status` siempre es `SIMULADA`.
- `mission` puede ser null si no se pudo crear por entrada invalida; `plan` es null antes de una propuesta estructuralmente valida.
- Caso completo: codigo 0 y estado final `PLAN_EN_REVISION`; cero aprobaciones y tareas activas.
- Caso incompleto: codigo 3 y estado `ACLARACION_REQUERIDA`.
- Entrada o plantilla invalida, archivo ausente o dependencia no disponible: codigo distinto de cero, mensaje claro, sin instalar paquetes ni continuar silenciosamente.
- El arranque original `python -B -m app` conserva exactamente su comportamiento; README explica que este es un comando separado de ensayo, no el producto operativo.
- Nada sobrevive a cerrar el proceso. El JSON emitido no es un VBP, una aprobacion ni memoria guardada.

## 10. Pruebas y criterios de aceptacion

| ID | Comprobacion exigida |
|---|---|
| CA-01 | Caso completo produce BORRADOR, LISTA_PARA_PLAN y PLAN_EN_REVISION en orden, con tres eventos incluyendo creacion |
| CA-02 | Cada campo formal faltante produce ACLARACION_REQUERIDA, identifica el campo y no genera plan |
| CA-03 | Supuestos o decisiones pendientes impiden LISTA_PARA_PLAN; no se fabrican aprobaciones |
| CA-04 | JSON invalido, tipo incorrecto, claves desconocidas, limites excedidos y fixture ausente se rechazan explicitamente |
| CA-05 | Mision y eventos reales producidos pasan sus schemas; una fecha invalida de prueba es rechazada por el comprobador |
| CA-06 | Plantilla con campo obligatorio ausente, ID duplicado, rol ajeno, dependencia ausente, propia, circular o desordenada no alcanza PLAN_EN_REVISION |
| CA-07 | La copia de la plantilla no modifica la entrada; ejecuciones independientes no comparten listas, IDs ni estado |
| CA-08 | Etiqueta SIMULADA visible en sobre, titulo, plan, tareas y eventos simulados; no hay afirmaciones de agentes reales |
| CA-09 | Ninguna entrada puede forzar AUTORIZADA_PARA_EJECUTAR, EN_EJECUCION, VBP_APROBADO o FINALIZADA; no hay autoaprobacion |
| CA-10 | No hay llamadas de red, modelos, subprocess para tareas, escrituras ni imports con efectos; comprobar por inspeccion y pruebas dirigidas |
| CA-11 | CLI ejecutable, JSON parseable y codigos de salida correctos; funciones pueden probarse con entradas en memoria |
| CA-12 | Las 16 pruebas anteriores siguen pasando sin modificarlas; matriz anterior mantiene 1440 casos y exactamente 10 aceptados |
| CA-13 | Solo tres archivos nuevos y dos modificados; los otros 18 archivos de producto mantienen huellas, tamanos y fechas |

Ejecutar y devolver salidas completas:

1. `python --version` y version de `jsonschema` por `importlib.metadata`.
2. `python -B -m app`.
3. `python -B -m app.demo_intake`.
4. `python -B -m unittest discover -s tests -v`.
5. Manifiesto y SHA-256 antes/despues de los 20 archivos anteriores; distinguir README/pyproject, los unicos dos permitidos para cambiar.
6. Conteo exacto de los tres nuevos, 13 nucleares y cero residuos. No usar un conteo total de carpeta como sustituto de comparar archivos.

Las huellas previas deben capturarse antes de editar, conservarse en la respuesta y repetirse al terminar. No se reconstruye una linea base a posteriori.

## 11. Trazabilidad al checklist de clases

| Referencia | Aporte de esta subpieza | No demostrado todavia |
|---|---|---|
| RF-001, RF-003, RF-005 | Creacion efimera, faltantes formales y estructura de plan de prueba | Guardado durable, aclaracion inteligente y plan generado por IA |
| RF-026, RF-027; C.2 | Funciones deterministas y etiquetas explicitas | Agente raiz, herramientas y runtime de agentes |
| C.3 | Datos separados en registros estructurados en memoria | Sesiones persistentes y recuperacion tras reinicio |
| C.7 | Tramo inicial secuencial y condiciones de salida | Colaboracion real de los cinco agentes y recorrido hasta VBP |
| C.9 | Detencion antes de ejecutar; no existe ruta de autoaprobacion | Servicio real de aprobaciones, consumo unico y auditoria durable |

No se marcan completos CT-002, CT-003, CT-007, CT-009 ni el gate del concurso con este ensayo parcial.

## 12. Limites y condiciones de detencion

Una sola conversacion de construccion, sin delegacion; tiempo objetivo 45 minutos. Cero instalaciones, llamadas a modelos o red y cero costo externo de ejecucion. Maximo dos rondas de correccion de codigo, cada una autorizada; una tercera requiere nueva decision humana.

Detenerse antes de editar si falta la aprobacion de esta ficha, un archivo nuevo ya existe, faltan dependencias compatibles o no se pueden capturar huellas. Detenerse y consultar si hace falta tocar contratos, otro archivo, una decision de producto o cualquier capacidad excluida. No crear un sustituto silencioso de un schema o de una capacidad real.

## 13. Prompt historico de construccion en Antigravity (no volver a ejecutar)

```text
Actua como constructor inicial de PZ-003A en OminAIHQ. Lee las fuentes obligatorias y FICHA-PZ-003A-ENTRADA-Y-PLAN-CONTROLADO.md completamente.

Primero comprueba que exista aprobacion humana expresa de esta ficha. Si permanece PROPUESTA_PENDIENTE_DE_APROBACION_HUMANA y no hay autorizacion humana posterior que la apruebe expresamente, detente sin editar.

Construye solo el ensayo SIMULADA hasta PLAN_EN_REVISION o ACLARACION_REQUERIDA. No implementes aprobacion, ejecucion de tareas, VBP ni agentes reales.

Crea exclusivamente app/demo_intake.py, examples/demo_mission.json y tests/test_demo_intake.py. Modifica exclusivamente README.md y pyproject.toml segun la ficha. Conserva el resto del producto y todos los contratos sin cambios.

Antes de editar, confirma dependencias ya disponibles, ausencia de los tres nuevos archivos, manifiesto y huellas iniciales de los 20 archivos anteriores, y presenta tu plan breve. No instales ni uses red, no delegues y no generes archivos fuera del permiso.

Implementa los criterios CA-01 a CA-13. Usa Python con -B. Devuelve archivos exactos, cambios, salidas completas, conteos de pruebas y subcasos, hashes antes/despues, residuos, limitaciones y riesgos. La autorizacion es para construir, no constituye aceptacion final: no declares PZ-003A aceptada ni OminAI HQ listo para produccion o para el concurso.
```

## 14. Registro historico de aprobacion humana para construir

```text
Pieza: PZ-003A
Decision: APROBADA
Autorizacion de construir: OTORGADA
Fecha de aprobacion: 30 de agosto de 2026
Aprobado por: usuario humano (A0 actual del proyecto)
Referencia: respuesta expresa "si" a la solicitud de autorizar PZ-003A con tres archivos nuevos y dos ajustes, sin instalar dependencias ni modificar contratos
Constructor inicial autorizado: Antigravity
Archivos nuevos autorizados: app/demo_intake.py; examples/demo_mission.json; tests/test_demo_intake.py
Archivos existentes autorizados para modificar: README.md; pyproject.toml
Instalaciones autorizadas: ninguna
Modificaciones de contratos autorizadas: ninguna
Alcance funcional: ensayo SIMULADA hasta PLAN_EN_REVISION o ACLARACION_REQUERIDA, sin aprobacion ni ejecucion de tareas, agentes reales o VBP
Correcciones de Codex: requieren autorizacion humana concreta por ronda
Condicion de cierre: inspeccion de Chipi/Codex, revision independiente de Copilot y aprobacion humana final
Aceptacion final de la pieza al emitir este encargo inicial: PENDIENTE; la decision posterior de cierre se registra en la seccion 16
```

## 15. Registro de correccion 1 y verificacion de Chipi

**Fecha:** 30 de agosto de 2026. Construccion inicial de Antigravity seguida de una sola ronda de correccion autorizada a Codex; revision independiente posterior de Copilot, sin edicion.

### 15.1 Autorizacion y alcance de la correccion

El usuario humano respondio "si" a la propuesta cerrada de correccion y solicito el prompt para ejecutarla en Codex. El encargo autorizo exclusivamente:

- `app/demo_intake.py`.
- `tests/test_demo_intake.py`.

La correccion resolvio referencias de entrada mal tipadas, listas opcionales null aceptadas, booleanos tratados como limites numericos, tareas no objeto que provocaban excepciones, autoridades de transicion no verificadas y errores de CLI/dependencia no controlados. Se agregaron pruebas ejecutables de rechazo, limites, ausencia de efectos y fallos de arranque, sin ampliar capacidades.

### 15.2 Resultado verificado

- `python -B -m app`: salida 0, `STRUCTURE_READY`, `implemented_capabilities=[]`.
- `python -B -m app.demo_intake`: salida 0, `PLAN_EN_REVISION`, tres eventos, cuatro tareas `PENDIENTE`, `approval_refs=[]`.
- `python -B -m unittest discover -s tests -v`: 49/49 pruebas aprobadas; 27 anteriores conservadas y 22 nuevas. Las 11 pruebas originales de intake se compararon sin cambios.
- Nueva ejecucion de la suite al registrar este cierre: `Ran 49 tests in 2.468s`, `OK`.
- La rama incompleta conserva `ACLARACION_REQUERIDA` y salida 3; entradas invalidas y politicas incompatibles se rechazan.
- La regresion nuclear conserva la matriz de 1440 combinaciones con exactamente 10 aceptadas.
- No se modifico codigo durante las revisiones de Chipi ni durante este cierre documental.

### 15.3 Huellas y alcance temporal de las capturas

Chipi capturo una linea base de 78 archivos antes de la correccion 1 y la comparo con el estado corregido y de nuevo antes del cierre documental: solo cambiaron los dos archivos autorizados; 76 conservaron sus hashes, sin altas ni bajas. Los 13 archivos de `contracts/core` permanecieron intactos. No aparecieron residuos de bytecode o caches.

Esta captura independiente no es una captura previa a la construccion inicial. Para esa etapa se conserva el manifiesto declarado por Antigravity en `INFORME-CONSTRUCCION-PZ-003A.md`.

| Archivo corregido | Bytes antes | Bytes despues | SHA-256 antes de correccion 1 | SHA-256 corregido aceptado |
|---|---:|---:|---|---|
| `app/demo_intake.py` | 32521 | 37011 | `47C6E9937EBF06D93F54CB2F0AEDE5842CB3EA0AB031641D7BCBE811224E5A0E` | `DD6864D6530F1457705A1EF185D2FF0B351498250AE1ECE4BFDB6390E96CDAEA` |
| `tests/test_demo_intake.py` | 17774 | 39078 | `80307A7E314D0733B2C100EC6D833984B1A67A38B52C193546FB8195E22103A4` | `A78F878062216B7E04DDC52596D1A8B2D3A0B839CFFB0C37B22FB89CAF6D3C3B` |

Los siguientes valores son identicos antes de la correccion 1 y al iniciar el cierre documental:

| Contrato nuclear | SHA-256 sin cambios |
|---|---|
| `contracts/core/approval.schema.json` | `7DFFABD0C643E1BEDA566262E3C06C01BD84350FB501DEF5FAB52FCC07C91F14` |
| `contracts/core/checkpoint.schema.json` | `754D7EB58DC4D5052ACB97C2D73B974E214F7E135336D5F6412515650A2BD242` |
| `contracts/core/error.schema.json` | `A78B4D1F5203A732DA0E8EA1C45DB01B5ECA67A79D14B6DE6B48DB6700C3BCA9` |
| `contracts/core/event.schema.json` | `827B43977F1BA89FE727B43E172C52EEB52F941D7FE1DE7C4199F7C5E869681B` |
| `contracts/core/mission.schema.json` | `FE0C4B789362EFD768E1F70D61008401ED1D26BF106AFC2421F37770B1081350` |
| `contracts/core/README.md` | `7988E1864E652845B419313D21A05F3710DF09502DA20056DEF2A7D988E6BDF7` |
| `contracts/core/state-machine.json` | `186A21EB32E4258C0D4FBC799AB0701AA6A2F318F85AAB5A25003D7007F7E840` |
| `contracts/core/examples/approval.invalid.json` | `6BEEB4EC672E3F22BB692D3DBB52348C25E8B873D2BBAE051C68654E6C4777A5` |
| `contracts/core/examples/approval.valid.json` | `C33FCA0E6E576B81E961C2891A9A6A76BE9B5D30CC284CC47C456FDE76106C0F` |
| `contracts/core/examples/mission.invalid.json` | `B8BB9BA8F856A1353E770CD66F43F82EA8FB0EE2CD76E50ABF2C86551B47452B` |
| `contracts/core/examples/mission.valid.json` | `08D47EBBB3554169697F8609FF9AB72C4895329E15A6C42439EEC54C8484F32E` |
| `contracts/core/examples/transitions.invalid.json` | `3403BA2E52C3E964142DBBC76E5AD64EACE6B6697E8082986F429A0CBDF69912` |
| `contracts/core/examples/transitions.valid.json` | `D1D5A4EC2BAD452556D884A3650F5576C741BA39588E4EAC197FA2723C0C077D` |

## 16. Cierre documental y aceptacion humana final

```text
Pieza: PZ-003A
Decision: COMPLETADA_Y_ACEPTADA
Fecha de aceptacion humana: 30 de agosto de 2026
Aprobado por: usuario humano (A0 actual del proyecto)
Referencia: respuesta expresa "completada" a la solicitud de aceptar PZ-003A como COMPLETADA_Y_ACEPTADA y autorizar el archivo de informes y el registro de cierre, sin modificar codigo
Constructor inicial: Antigravity
Correcciones de codigo realizadas: 1, por Codex con autorizacion humana y lista cerrada de dos archivos
Inspeccion de Chipi: correccion verificada; 49/49 pruebas aprobadas y perimetro conservado
Revision independiente de Copilot: APTO_PARA_APROBACION_HUMANA; sin defectos que requieran otra correccion
Observacion documental de huellas: reconciliada en la seccion 15.3 y en los informes archivados
Aceptacion final de esta subpieza: OTORGADA
Aceptacion del bloque 3 completo o del MVP: NO OTORGADA por este cierre
Autorizacion de construir otra subpieza: NO OTORGADA por este cierre
```

### 16.1 Documentos de cierre autorizados

- Actualizar esta ficha para registrar el estado, la correccion, la evidencia y la decision humana.
- Crear [INFORME-CONSTRUCCION-PZ-003A.md](INFORME-CONSTRUCCION-PZ-003A.md) con el informe inicial y notas de reconciliacion separadas.
- Crear [REVISION-COPILOT-PZ-003A.md](REVISION-COPILOT-PZ-003A.md) con el dictamen independiente y su nota de trazabilidad.

Estos tres documentos son el alcance del cierre posterior autorizado. No son archivos adicionales de la construccion inicial ni otra ronda de correccion de codigo. No se modifica README, configuracion, codigo, pruebas, fixture, contratos ni fuentes educativas.

### 16.2 Alcance aceptado y limites que permanecen

Queda aceptado solamente el ensayo `SIMULADA` de entrada, deteccion formal de faltantes y propuesta de plan preescrito, con parada en `PLAN_EN_REVISION` o `ACLARACION_REQUERIDA`.

No se aceptan como implementados aprobaciones del producto, ejecucion de tareas, agentes reales, persistencia, memoria, reanudacion, interfaz, VBP ni despliegue. La aceptacion de esta subpieza por el usuario no equivale a aprobar un plan o VBP dentro del producto.

Las cifras de 27 pruebas, los hashes iniciales y el estado pendiente del informe de construccion son historicos. El estado actual de esta ficha y las 49 pruebas posteriores corresponden a la pieza corregida y aceptada.

La siguiente subpieza requiere su propia ficha y aprobacion humana. Este cierre no declara OminAI HQ listo para produccion ni para presentacion a competencia.
