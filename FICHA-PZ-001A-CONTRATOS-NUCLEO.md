# Ficha PZ-001A - Contratos nucleares y maquina de estados

**Estado:** COMPLETADA_Y_ACEPTADA  
**Contrato rector:** `CONTRATO-MVP-v1.md`, version `1.2-aprobada`  
**Fecha de ficha:** 28 de agosto de 2026  
**Fecha de aceptacion final:** 29 de agosto de 2026  
**Constructor autorizado cuando se apruebe la ficha:** Antigravity  
**Construccion realizada:** Antigravity ejecuto la construccion y las dos rondas ordinarias de correccion; Codex ejecuto una tercera correccion excepcional, concreta y expresamente autorizada por el usuario humano.  
**Alcance construido:** exclusivamente los trece archivos permitidos de `contracts/core`.

## 1. Identificacion de la pieza

**ID:** PZ-001A  
**Nombre:** Contratos nucleares y maquina de estados  
**Orden:** primera subpieza de la Pieza 1 del contrato aprobado.

## 2. Objetivo

Crear contratos estructurados, versionados y verificables para la identidad de una mision, sus eventos, aprobaciones, checkpoints, errores y transiciones. Estos contratos deben convertirse en la unica referencia de los estados nucleares antes de crear runtime, agentes, persistencia o interfaz.

## 3. Problema que resuelve

Sin contratos ejecutables, cada capa podria interpretar de forma distinta los estados, permisos, reintentos o aprobaciones. Eso permitiria transiciones no autorizadas, duplicados, perdida de reanudacion y pruebas que solo validen texto. PZ-001A fija el nucleo determinista sin seleccionar todavia la estructura completa de la aplicacion.

## 4. Fuentes obligatorias

1. `AGENTS.md`, especialmente autoridad, forma de trabajo, reglas de construccion y revision.
2. `TEAM-WORKFLOW.md`, estados de una pieza, plantilla y encargo para Antigravity.
3. `CONTRATO-MVP-v1.md` version `1.2-aprobada`:
   - secciones 0, 2.3, 4.1 a 4.4;
   - secciones 5.1 y 6.2;
   - RF-003, RF-006 a RF-009, RF-016 a RF-024;
   - RNF-001 a RNF-007 y RNF-013;
   - secciones 11.1, 11.3, 11.4 y 11.5;
   - CT-002, CT-003, CT-007, CT-008, CT-009 y CT-015.

No usar como fuente normativa ejemplos del curso, implementaciones de otros productos ni documentos de Business OS.

## 5. Decisiones ya aprobadas

- Quince estados de mision definidos en 4.1.
- Transiciones y autoridades definidas en 4.2.
- Invariantes de 4.3.
- Ocho estados de tarea definidos en 4.4.
- Solo el usuario humano activa controles humanos.
- Una aprobacion esta vinculada a una version exacta y solo puede responderse una vez.
- Una clave de idempotencia repetida no duplica efectos.
- Reanudar utiliza el ultimo checkpoint valido y no repite acciones confirmadas.
- Ocho tipos de error y sus politicas de reintento definidos en 11.3.
- Limites finitos definidos en 11.4.
- No se almacena ni expone Chain-of-Thought.
- El contrato nuclear debe permanecer independiente de UI, proveedor de modelo, base de datos y servicio de nube.

## 6. Archivos permitidos

Antigravity solo podra crear o modificar, cuando esta ficha sea aprobada para construir:

- `contracts/core/README.md`
- `contracts/core/mission.schema.json`
- `contracts/core/event.schema.json`
- `contracts/core/approval.schema.json`
- `contracts/core/checkpoint.schema.json`
- `contracts/core/error.schema.json`
- `contracts/core/state-machine.json`
- `contracts/core/examples/mission.valid.json`
- `contracts/core/examples/mission.invalid.json`
- `contracts/core/examples/approval.valid.json`
- `contracts/core/examples/approval.invalid.json`
- `contracts/core/examples/transitions.valid.json`
- `contracts/core/examples/transitions.invalid.json`

No se permiten archivos adicionales sin una nueva decision humana.

## 7. Archivos prohibidos

- `CONTRATO-MVP-v1.md`
- `AGENTS.md`
- `TEAM-WORKFLOW.md`
- Esta ficha despues de su aprobacion.
- Cualquier archivo de interfaz, backend, agente, memoria, persistencia, despliegue o configuracion de nube.
- Archivos de Business OS, Omi, OminaiTech Engine o cualquier otro producto.
- Dependencias, lockfiles, credenciales, variables de entorno o configuraciones de proveedor.

## 8. Entradas

- Estados, transiciones e invariantes del contrato aprobado.
- Campos de evento de 11.1.
- Campos de aprobacion de 6.2.
- Errores y reintentos de 11.3.
- Limites y checkpoints de 11.4 y 11.5.

## 9. Salida esperada

Un directorio `contracts/core` que contenga:

1. JSON Schemas Draft 2020-12 validos y versionados para mision, evento, aprobacion, checkpoint y error.
2. Una maquina de estados declarativa que enumere estados, terminalidad, transiciones, guardias, autoridades y si requieren aprobacion humana.
3. Ejemplos positivos y negativos que permitan demostrar aceptacion y rechazo.
4. Un README corto con version, alcance, invariantes, compatibilidad, forma de validacion y declaracion expresa de que estos archivos no prueban runtime ni persistencia.

## 10. Contenido minimo de los contratos

### 10.1 Mision

Debe incluir como minimo: `schema_version`, `mission_id`, `user_id`, titulo, version de brief, estado actual, estado reanudable anterior cuando aplique, tarea activa opcional, contadores, limites, referencias a aprobaciones, ultimo checkpoint, fechas de creacion/actualizacion y version del registro.

### 10.2 Evento

Debe incluir los campos de 11.1: identificadores, actor, rol, accion, fecha, version, estado anterior/nuevo, herramienta o categoria, fuente/artefacto, resultado resumido, error, intento, limite consumido, aprobacion relacionada y clave de idempotencia.

No puede contener campos para razonamiento interno, scratchpad o Chain-of-Thought.

### 10.3 Aprobacion

Debe incluir: `approval_id`, `user_id`, actor, accion, version/huella exacta, fecha, decision, comentario, condiciones, expiracion opcional y estado. Debe distinguir aprobar, aprobar con excepcion, rechazar y solicitar cambios. Una aprobacion consumida no vuelve a estado pendiente.

### 10.4 Checkpoint

Debe identificar mision, version, estado, estado reanudable, tareas, dependencias, intentos, limites consumidos, artefactos, autorizaciones, fecha, huella e idempotencia. No guarda transcripcion de razonamiento.

### 10.5 Error

Debe admitir exactamente las categorias aprobadas: `INVALID_INPUT`, `NOT_FOUND`, `PERMISSION_DENIED`, `TRANSIENT_FAILURE`, `SCHEMA_INVALID`, `DEPENDENCY_FAILED`, `BUDGET_EXHAUSTED` y `SYSTEM_ERROR`, con reintento permitido, intento actual, recuperabilidad y accion requerida.

### 10.6 Maquina de estados

Debe representar los quince estados de mision, los ocho estados de tarea y todas las transiciones de 4.2. Las transiciones humanas deben quedar identificadas de forma que un consumidor determinista pueda denegar un actor no humano.

## 11. Criterios de aceptacion

1. Todos los JSON son sintacticamente validos.
2. Cada schema declara Draft 2020-12, identificador, titulo y version.
3. Los cinco schemas pasan metavalidacion con un validador compatible.
4. Los ejemplos `valid` son aceptados y los `invalid` son rechazados por la razon documentada.
5. La maquina contiene exactamente 15 estados de mision y 8 estados de tarea.
6. Todas las transiciones de 4.2 estan representadas, sin rutas adicionales a estados reservados.
7. `AUTORIZADA_PARA_EJECUTAR`, `VBP_APROBADO`, `FINALIZADA` y `CANCELADA` no pueden alcanzarse por decision de modelo.
8. Aprobar, aprobar con excepcion, rechazar, solicitar cambios y cancelar quedan reservados al usuario humano cuando corresponda.
9. Una aprobacion duplicada o ya consumida es rechazada por contrato.
10. Una clave de idempotencia duplicada no describe un segundo efecto.
11. Un checkpoint permite identificar el estado exacto de continuacion sin guardar Chain-of-Thought.
12. Los ocho errores tienen comportamiento finito consistente con 11.3.
13. No aparecen nombres de Business OS, Omi, OminaiTech Engine, UI, Firestore, Cloud Run, Cloud Storage ni un proveedor de modelos dentro de los contratos nucleares.
14. No se crean ni modifican archivos fuera de la lista permitida.
15. README y evidencia del constructor no afirman que runtime, persistencia, agentes o interfaz ya existan.

## 12. Pruebas obligatorias

1. Parseo de todos los JSON.
2. Metavalidacion de cada schema contra JSON Schema Draft 2020-12.
3. Validacion de cada ejemplo positivo.
4. Rechazo de cada ejemplo negativo, mostrando la regla incumplida.
5. Conteo automatico de estados de mision y tarea.
6. Comparacion automatica entre la tabla 4.2 y las transiciones declaradas.
7. Prueba negativa de actor no humano intentando aprobar plan y VBP.
8. Prueba negativa de doble respuesta a la misma aprobacion.
9. Prueba negativa de campo `chain_of_thought` o equivalente.
10. Prueba de referencia rota a checkpoint, aprobacion o estado inexistente.

La ficha no autoriza instalar dependencias. Si el workspace no dispone de un validador compatible, Antigravity debe detenerse, informar el requisito exacto y solicitar aprobacion antes de instalar o crear infraestructura de pruebas.

## 13. Evidencias que debe devolver Antigravity

- Resumen preciso de lo construido.
- Lista exacta de archivos creados o modificados.
- Comandos de validacion ejecutados.
- Resultado completo de cada prueba obligatoria.
- Conteo de schemas, estados, transiciones, ejemplos aceptados y ejemplos rechazados.
- Muestra de un rechazo por actor no humano, duplicado y Chain-of-Thought.
- Confirmacion de que no se instalaron dependencias ni se tocaron archivos prohibidos.
- Errores, supuestos, riesgos y decisiones solicitadas.

## 14. Limites de tiempo, costo e iteraciones

- Tiempo objetivo de construccion: 60 minutos.
- Una sola pieza activa.
- Cero llamadas a modelos o servicios de pago para validar contratos.
- Cero instalaciones sin aprobacion humana.
- Maximo dos rondas de correccion despues de la primera revision.
- Si una correccion exige cambiar el contrato aprobado, detenerse y escalar.

## 15. Condiciones para detenerse y preguntar

Antigravity debe detenerse sin editar si:

- encuentra contradicciones entre esta ficha y el contrato aprobado;
- necesita elegir lenguaje, runtime, libreria o dependencia no existente;
- no puede ejecutar la metavalidacion sin instalar software;
- una transicion o autoridad no esta definida de forma univoca;
- necesita modificar un archivo no permitido;
- detecta que el alcance requiere contratos de agentes, VBP, memoria o persistencia todavia no autorizados;
- una prueba obligatoria no puede ejecutarse de forma reproducible.

## 16. Prompt preparado para Antigravity

> **APROBADO PARA EJECUTAR EN ANTIGRAVITY.** La aprobacion se limita a PZ-001A y no autoriza archivos, dependencias ni capacidades fuera de esta ficha.

```text
Actua como unico constructor de PZ-001A, Contratos nucleares y maquina de estados de OminAI HQ.

Lee completamente, en este orden:
1. AGENTS.md
2. TEAM-WORKFLOW.md
3. CONTRATO-MVP-v1.md version 1.2-aprobada
4. FICHA-PZ-001A-CONTRATOS-NUCLEO.md aprobada

Tu alcance se limita a los archivos enumerados en la seccion 6 de la ficha. No modifiques codigo o documentacion fuera de esa lista, no instales dependencias, no elijas infraestructura y no agregues capacidades de UI, agentes, memoria, persistencia o nube.

Antes de editar:
- confirma que leiste las cuatro fuentes;
- informa el plan y la lista exacta de archivos previstos;
- confirma que existe una forma disponible de validar JSON Schema Draft 2020-12 sin instalar dependencias.

Si falta esa capacidad o existe una decision ambigua, detente y pregunta antes de editar.

Despues construye los contratos, ejecuta todas las pruebas de la seccion 12 y verifica los 15 criterios de aceptacion. Devuelve resumen, archivos, comandos, resultados, conteos, evidencia de rechazos, supuestos, errores, riesgos y pendientes. No declares implementados runtime, persistencia, agentes, interfaz ni despliegue.
```

## 17. Registro de aprobacion humana

```text
Pieza: PZ-001A
Decision: APROBAR_PZ-001A_PARA_CONSTRUIR
Version de contrato: 1.2-aprobada
Alcance: exclusivamente los archivos de la seccion 6
Constructor: Antigravity
Dependencias nuevas autorizadas: ninguna
Fecha: 28 de agosto de 2026
Aprobado por: usuario humano (A0 actual del proyecto)
Referencia: confirmacion expresa "aprobado" en la conversacion del 28 de agosto de 2026
```

La siguiente puerta humana ocurre despues de que Antigravity devuelva archivos, pruebas y evidencias. La construccion no se considera aceptada hasta completar inspeccion de Chipi/Codex, revision independiente de Copilot y decision humana `ACEPTADA`.

## 18. Registro de aceptacion final de la pieza

```text
Pieza: PZ-001A
Decision: ACEPTADA
Fecha: 29 de agosto de 2026
Autoridad: usuario humano (A0 actual del proyecto)
Alcance aceptado: los trece archivos autorizados de contracts/core
Revision Chipi/Codex: APROBADA
Revision independiente de Copilot: APROBADA, con limitaciones de ejecucion documentadas en REVISION-COPILOT-PZ-001A.md
Validacion independiente complementaria: cinco schemas metavalidados, ejemplos positivos y negativos ejecutados y 960 combinaciones de error comprobadas; se aceptaron exactamente las diez autorizadas
Archivos adicionales dentro de contracts/core: ninguno
Dependencias instaladas: ninguna
Capacidades no demostradas por esta pieza: runtime, persistencia, agentes, interfaz y despliegue
Referencia: confirmacion expresa "si correcto" del usuario humano en la conversacion del 29 de agosto de 2026
```

Con esta decision, PZ-001A queda cerrada como `COMPLETADA_Y_ACEPTADA`. Cualquier cambio posterior a sus contratos requiere una nueva pieza, version y aprobacion humana.
