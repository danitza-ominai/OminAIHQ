# Contrato MVP v1 de OminAI HQ

**Estado del documento:** APROBADO - GO_CON_CONDICIONES PARA PREPARAR PIEZAS  
**Version:** 1.2-aprobada  
**Fecha:** 28 de agosto de 2026  
**Autoridad actual del proyecto:** Niko, A0 humana  
**Rol de aprobacion dentro del producto:** usuario humano  
**Proposito de control:** esta version recibio aprobacion humana para preparar piezas. Cada encargo de construccion todavia requiere ficha y aprobacion humana propia antes de entregarse a Antigravity.

> Este contrato describe el producto y su comportamiento funcional. Mantiene neutralidad tecnologica salvo el perfil de entrega exigido y aprobado para el concurso: Gemini 3.5 Flash o posterior, Google ADK, Cloud Run, Firestore y Cloud Storage. Esta seleccion no demuestra que una capacidad ya este implementada, desplegada o lista para produccion.

## 0. Autoridad, lenguaje de evidencia y vigencia

### 0.1 Jerarquia de autoridad

1. Niko es la A0 humana actual del proyecto. Dentro del producto, la capacidad se denomina `usuario humano` y conserva la autoridad para aprobar, rechazar, pausar, cancelar o pedir cambios.
2. Las decisiones expresas del encargo de Niko y de `AGENTS.md` prevalecen sobre recomendaciones educativas.
3. `TEAM-WORKFLOW.md` gobierna la construccion y revision de piezas del producto; no debe confundirse con el flujo interno de una mision dentro de OminAI HQ.
4. Los PDF y la transcripcion de `REQUISITOS` son material educativo. Respaldan principios de diseño, pero sus herramientas, ejemplos, proveedores, metricas y arquitecturas no son requisitos del MVP.
5. Los agentes internos de OminAI HQ no son los participantes del equipo constructor. Antigravity construye; Copilot revisa; Chipi/Codex coordina e inspecciona; Niko decide.

### 0.2 Etiquetas normativas

| Etiqueta | Significado en este documento |
|---|---|
| **DECISION APROBADA** | Ya fue establecida por Niko en el encargo o en `AGENTS.md`. |
| **PRINCIPIO DE GUIA** | Practica respaldada por una fuente educativa local. Orienta el contrato, pero no obliga a adoptar la tecnologia mostrada en la fuente. |
| **PROPUESTA** | Definicion funcional recomendada en este contrato. Solo se convierte en decision aprobada mediante aprobacion humana de esta version o de la decision individual. |
| **PENDIENTE DE DECISION HUMANA** | Eleccion material que todavia necesita una decision del usuario humano. |
| **PENDIENTE DE EVIDENCIA** | Capacidad o control del checklist tecnico que no puede marcarse completo hasta contar con prueba reproducible. |

### 0.3 Entrada en vigor y control de version

- **DECISION APROBADA:** no se entrega ninguna pieza a Antigravity antes de la aprobacion humana correspondiente.
- **DECISION APROBADA:** esta version entra en vigor mediante el registro `GO_CON_CONDICIONES` de la seccion 15.6.
- Toda modificacion posterior incrementa la version y vuelve a estado `PENDIENTE_DE_APROBACION`.
- Una version reemplazada permanece disponible como historia; no se sobrescribe silenciosamente.

## 1. Proposito, usuario y resultado del MVP

### 1.1 Identidad del producto

- **DECISION APROBADA:** Ominai es la compania paraguas.
- **DECISION APROBADA:** OminAI HQ es el producto actual y participante del hackathon.
- **DECISION APROBADA:** OminAI Business OS es un producto independiente.
- **DECISION APROBADA:** Omi pertenece exclusivamente a Business OS.
- **DECISION APROBADA:** OminaiTech Engine es una integracion futura y esta fuera del MVP.

### 1.2 Proposito y usuario

- **DECISION APROBADA:** OminAI HQ es una oficina digital agentica donde Niko trabaja con agentes internos especializados para transformar una mision de negocio en un Venture Build Package (VBP) auditable.
- **DECISION APROBADA:** la v0 tiene un solo usuario humano. Niko es la usuaria actual, pero su nombre no se codifica como funcion del producto.
- **DECISION APROBADA:** el usuario tiene un perfil local persistente con `user_id`, nombre y correo opcional; no existe login real, contrasena, equipo ni roles multiples en la v0.
- **DECISION APROBADA:** cada mision constituye una unidad de trabajo versionada, reanudable y auditable, separada de otras misiones.

### 1.3 Resultado verificable del MVP

El MVP produce, para una mision aprobada, un VBP que:

1. contiene todas las secciones obligatorias definidas en la seccion 6;
2. diferencia hechos respaldados, supuestos, propuestas, decisiones aprobadas y pendientes;
3. enlaza cada afirmacion material con evidencia o la identifica como no verificada;
4. conserva decisiones, aprobaciones, cambios de estado y resultados resumidos sin guardar Chain-of-Thought;
5. puede ser revisado por el usuario humano dentro de la interfaz y descargado como un unico archivo Markdown (`.md`);
6. solo recibe estado final despues de una aprobacion humana expresa vinculada a la version exacta.

El resultado es un paquete de definicion y planificacion de una iniciativa. No es, por si mismo, codigo construido, despliegue, compra, publicacion ni garantia de viabilidad o calidad.

## 2. Alcance incluido, excluido y limites

### 2.1 Alcance incluido

| Capacidad | Clasificacion |
|---|---|
| Crear una mision de negocio | DECISION APROBADA |
| Versionar la mision y conservar su historia | DECISION APROBADA |
| Aclarar ambiguedades y registrar respuestas del usuario | DECISION APROBADA |
| Proponer un plan con tareas y dependencias | DECISION APROBADA |
| Ejecutar analisis mediante cinco agentes internos con contratos separados | DECISION APROBADA |
| Reunir evidencia con fuente, fecha, confianza y limitaciones | DECISION APROBADA |
| Convertir evidencia en definicion de producto, alcance y requisitos | DECISION APROBADA |
| Preparar fases, tareas, dependencias, riesgos y criterios de aceptacion | DECISION APROBADA |
| Evaluar completitud, coherencia, trazabilidad, limites y riesgos | DECISION APROBADA |
| Consolidar y someter el VBP a aprobacion humana | DECISION APROBADA |
| Mostrar progreso, evidencia, decisiones y aprobaciones en una interfaz minima | DECISION APROBADA |
| Reanudar trabajo desde un punto de control sin repetir pasos ya confirmados | DECISION APROBADA |
| Descargar el VBP final y consultar su auditoria | DECISION APROBADA: un unico Markdown estructurado, visible en la interfaz y descargable como `.md` |
| Ejecutar localmente la v0 y desplegar una demostracion controlada en Google Cloud | DECISION APROBADA para cumplir el concurso; requiere evidencia real antes de marcarse implementada |

### 2.2 Alcance excluido del MVP

- **DECISION APROBADA:** OminAI Business OS, Omi y OminaiTech Engine quedan fuera del MVP.
- **DECISION APROBADA:** queda prohibido almacenar o exponer Chain-of-Thought.
- **DECISION APROBADA:** queda prohibido convertir tecnologias opcionales en requisitos sin necesidad demostrada.
- **DECISION APROBADA:** construir o desplegar la iniciativa descrita por una mision queda fuera de la v0; el recorrido funcional termina en el VBP aprobado y descargable. Esta exclusion no impide desplegar OminAI HQ como demostracion del concurso.
- **DECISION APROBADA:** ejecutar pagos, compras, cobros, correos, publicaciones, eliminaciones, despliegues o escrituras en sistemas externos queda fuera de la v0.
- **DECISION APROBADA:** queda excluido operar sin supervision humana, autoaprobar alcance o declarar una mision exitosa basandose solo en la opinion de un agente.
- **DECISION APROBADA:** queda excluido prometer eliminacion de alucinaciones, exactitud total, produccion autonoma o disponibilidad de grado productivo.

### 2.3 Limites obligatorios

1. Una salida sin evidencia suficiente se marca `NO_VERIFICADA`, `SUPUESTO` o `BLOQUEADA`; no se presenta como hecho.
2. Ningun agente puede aprobar su propia salida ni mover la mision a un estado reservado al usuario humano.
3. Todo bucle, reintento, descomposicion, duracion y presupuesto debe tener un limite finito antes de ejecutarse.
4. Un reinicio no restablece contadores de reintento ni borra el historial.
5. Las acciones sensibles permanecen bloqueadas salvo aprobacion humana explicita y, para este MVP, se consideran fuera de alcance por defecto.
6. Las capacidades simuladas deben mostrar la etiqueta `SIMULADA` en la interfaz, la salida y la auditoria.

## 3. Recorrido vertical completo: Mision a VBP

| Paso | Responsable principal | Entrada | Salida verificable | Condicion de salida |
|---:|---|---|---|---|
| 1. Mision | Usuario humano | Objetivo inicial | Borrador con objetivo, contexto y restricciones | El usuario guarda el borrador |
| 2. Aclaracion | Chief of Staff + usuario humano | Borrador y brechas | Brief de mision versionado; respuestas y pendientes | No quedan ambiguedades bloqueantes o el usuario acepta explicitamente los supuestos |
| 3. Plan | Chief of Staff | Brief vigente | Tareas, responsables funcionales, dependencias, criterios, limites y riesgos | El plan supera validacion estructural |
| 4. Revision del plan | Usuario humano | Plan propuesto | Aprobacion, rechazo o solicitud de cambios | **DECISION APROBADA:** solo la aprobacion humana de la version exacta habilita la ejecucion |
| 5. Tareas | Chief of Staff | Plan aprobado | Instancias de tarea con contratos completos | Cada tarea tiene entradas, salida, criterio, herramientas permitidas y presupuesto |
| 6. Analisis especializado | Agente asignado | Tarea y contexto minimo | Resultado `COMPLETO`, `PARCIAL`, `BLOQUEADO` o `FALLIDO` | La salida cumple su esquema o se escala |
| 7. Evidencia | Research & Evidence Analyst | Preguntas y hallazgos | Registros de evidencia y contradicciones | Cada afirmacion material queda respaldada o etiquetada |
| 8. Consolidacion | Chief of Staff | Salidas y evidencias | Borrador de VBP sin contradicciones silenciosas | Validacion de estructura completa |
| 9. Evaluacion | Governance & Risk | Borrador, requisitos y evidencia | Informe con `PASA`, `PASA_CON_CONDICIONES` o `NO_PASA` | Todos los bloqueos se resuelven, aceptan o escalan |
| 10. Aprobacion humana | Usuario humano | VBP evaluado e informe | Aprobar, aprobar con excepcion, rechazar, pedir cambios, pausar o cancelar | Solo `APROBAR` o `APROBAR_CON_EXCEPCION` autoriza la finalizacion |
| 11. VBP final | Accion determinista | Version aprobada | Paquete descargable con manifest, contenido y auditoria | Huella/version coinciden con lo aprobado |
| 12. Auditoria | Usuario humano | Mision o VBP | Linea de tiempo filtrable de acciones, fuentes, decisiones y aprobaciones | Consulta disponible sin revelar razonamiento interno |

### Reglas transversales del recorrido

- La evidencia puede reunirse antes o durante el analisis, pero siempre debe vincularse al hallazgo que respalda.
- Una contradiccion entre fuentes no se resuelve por ocultamiento: se presenta con impacto y necesidad de decision.
- Un resultado parcial puede alimentar el VBP solo si conserva su etiqueta y limitacion.
- Cualquier cambio de alcance invalida la aprobacion del plan afectado y genera una nueva version.
- La generacion final es posterior a la aprobacion humana y no puede alterar el contenido aprobado.

## 4. Estados y reglas de transicion

### 4.1 Estados de la mision

Los siguientes estados son **DECISION APROBADA** mediante el `GO_CON_CONDICIONES` de la version 1.2:

| Estado | Significado |
|---|---|
| `BORRADOR` | La mision existe, pero aun puede estar incompleta. |
| `ACLARACION_REQUERIDA` | Hay preguntas o decisiones bloqueantes para el usuario humano. |
| `LISTA_PARA_PLAN` | El brief cumple los campos minimos. |
| `PLAN_EN_REVISION` | Existe un plan propuesto pendiente de decision humana. |
| `AUTORIZADA_PARA_EJECUTAR` | El usuario humano aprobo la version exacta del plan. |
| `EN_EJECUCION` | Hay tareas autorizadas activas. |
| `BLOQUEADA` | No puede avanzar por falta de entrada, permiso, evidencia, dependencia o presupuesto. |
| `PAUSADA` | El usuario humano o una regla de seguridad suspendio el trabajo conservando el punto de control. |
| `EN_CONSOLIDACION` | Se prepara el borrador integrado del VBP. |
| `EN_EVALUACION` | Governance & Risk evalua el borrador. |
| `VBP_EN_REVISION` | El paquete evaluado espera decision humana. |
| `VBP_RECHAZADO` | El usuario humano rechazo la version y registro motivos. |
| `VBP_APROBADO` | El usuario humano aprobo la version exacta, de forma ordinaria o con excepcion documentada. |
| `FINALIZADA` | El paquete aprobado se genero y verifico sin alterar su contenido. |
| `CANCELADA` | El usuario humano cerro la mision sin VBP final. |

### 4.2 Transiciones autorizadas

| Desde | Evento y guardia | Hacia | Autoridad |
|---|---|---|---|
| `BORRADOR` | Faltan campos o hay ambiguedades materiales | `ACLARACION_REQUERIDA` | Regla determinista / Chief of Staff |
| `BORRADOR` o `ACLARACION_REQUERIDA` | Brief completo o supuestos aceptados | `LISTA_PARA_PLAN` | Chief of Staff; aceptacion de supuestos por el usuario humano |
| `LISTA_PARA_PLAN` | Plan estructuralmente valido | `PLAN_EN_REVISION` | Chief of Staff |
| `PLAN_EN_REVISION` | Aprobacion humana de version y alcance | `AUTORIZADA_PARA_EJECUTAR` | Solo usuario humano |
| `AUTORIZADA_PARA_EJECUTAR` | Se inicia una tarea autorizada | `EN_EJECUCION` | Orquestacion determinista |
| Cualquier estado no terminal | Falta entrada, permiso, dependencia, evidencia o presupuesto | `BLOQUEADA` | Regla o agente, con motivo |
| Cualquier estado no terminal | El usuario pausa; o se activa limite de seguridad | `PAUSADA` | Usuario humano / regla de seguridad |
| `BLOQUEADA` o `PAUSADA` | Se resuelve el bloqueo y permanece vigente la autorizacion | Estado anterior reanudable | Usuario humano o regla autorizada |
| `EN_EJECUCION` | Todas las tareas obligatorias estan en estado admisible | `EN_CONSOLIDACION` | Chief of Staff |
| `EN_CONSOLIDACION` | Borrador completo y validado | `EN_EVALUACION` | Accion determinista |
| `EN_EVALUACION` | Evaluacion emitida | `VBP_EN_REVISION` | Governance & Risk no aprueba; solo remite |
| `VBP_EN_REVISION` | Rechazo humano con motivos | `VBP_RECHAZADO` | Solo usuario humano |
| `VBP_RECHAZADO` | El usuario autoriza una revision acotada | `EN_CONSOLIDACION` | Solo usuario humano |
| `VBP_EN_REVISION` | Aprobacion humana ordinaria o con excepcion documentada | `VBP_APROBADO` | Solo usuario humano |
| `VBP_APROBADO` | Exportacion y verificacion correctas | `FINALIZADA` | Accion determinista |
| Cualquier estado no terminal | El usuario cancela | `CANCELADA` | Solo usuario humano |

### 4.3 Invariantes de transicion

- Cada transicion registra `mission_id`, estado anterior, estado nuevo, evento, actor, fecha/hora, version, motivo y referencia al artefacto afectado.
- `AUTORIZADA_PARA_EJECUTAR`, `VBP_APROBADO`, `FINALIZADA` y `CANCELADA` nunca se alcanzan por inferencia de un modelo.
- Una solicitud duplicada con la misma clave de idempotencia no duplica tareas, aprobaciones ni paquetes.
- Cancelar o rechazar no elimina evidencia ni auditoria.
- Reanudar usa el ultimo punto de control valido y no repite una accion ya confirmada.

### 4.4 Estados minimos de tarea

`PENDIENTE -> LISTA -> EN_CURSO -> COMPLETA | PARCIAL | BLOQUEADA | FALLIDA | CANCELADA`

- Una dependencia no satisfecha impide pasar a `EN_CURSO`.
- `PARCIAL` requiere limitacion explicita y decision sobre si puede consolidarse.
- `FALLIDA` no se convierte automaticamente en `COMPLETA` por un reintento; cada intento queda registrado.

## 5. Contratos de agentes internos

### 5.1 Sobre comun de entrada

Toda invocacion de agente recibe, como minimo:

| Campo | Regla |
|---|---|
| `mission_id`, `mission_version`, `task_id` | Obligatorios y no ambiguos |
| objetivo y pregunta | Una sola responsabilidad verificable por tarea |
| contexto autorizado | Referencias, no un volcado indiscriminado de toda la mision |
| decisiones aprobadas | Separadas de supuestos y propuestas |
| entrada estructurada | Campos y tipos definidos antes de ejecutar |
| salida esperada | Esquema, estado y criterios de aceptacion |
| herramientas permitidas | Categorias expresamente autorizadas |
| prohibiciones | Acciones y datos fuera de alcance |
| limites | Intentos, tiempo, profundidad, amplitud y presupuesto |
| regla de escalamiento | Condiciones para detenerse y pedir decision |

### 5.2 Sobre comun de salida

Toda salida debe incluir:

`status`, `summary`, `findings`, `evidence_refs`, `assumptions`, `limitations`, `approved_decisions_used`, `proposals`, `pending_decisions`, `risks`, `artifacts`, `attempt_count`, `tool_actions_summary`, `errors` y `recommended_next_step`.

- Los estados admitidos son `SUCCESS`, `PARTIAL`, `BLOCKED` y `FAILED`.
- Los campos no aplicables se entregan vacios, no se omiten silenciosamente.
- `tool_actions_summary` describe accion, herramienta/categoria, entrada relevante y resultado, pero nunca Chain-of-Thought.
- **PRINCIPIO DE GUIA:** las salidas estructuradas reducen ambiguedad de integracion; un esquema debe declarar tambien estados, metadatos y errores necesarios (`T-DEVAGENTOPT-I-m2-l0-es-file-3.es.pdf`, p. 1; `T-DEVAGENTOPT-I-m2-l1-es-file-4.es.pdf`, p. 4).

### 5.3 Reglas comunes

1. Ningun agente decide producto en nombre del usuario humano.
2. Ningun agente altera el alcance de su tarea ni accede a una herramienta no autorizada.
3. La ausencia de evidencia se declara; no se rellena con una afirmacion plausible.
4. Los conflictos de fuentes se conservan y escalan.
5. Un agente no aprueba ni evalua como final una salida propia.
6. No se expone ni almacena Chain-of-Thought. Se registran decisiones resumidas, evidencia y acciones.
7. Las instrucciones deben declarar proposito, limites, formato, manejo de incertidumbre y escalamiento. **PRINCIPIO DE GUIA:** las instrucciones vagas producen comportamiento impredecible y los limites deben especificar que no inventar y cuando derivar (`T-DEVAGENTOPT-I-m1-l1-es-file-2.es.pdf`, pp. 1 y 4).

### 5.4 Categorias de herramientas

Las categorias son funcionales; no prescriben productos ni protocolos.

| Categoria | Uso permitido | Control minimo |
|---|---|---|
| Recuperacion interna de solo lectura | Consultar fuentes aportadas o aprobadas | Lista de origenes y permisos por tarea |
| Investigacion externa de solo lectura | Consultar fuentes externas autorizadas | Fecha de acceso, URL/localizador y politica de evidencia |
| Transformacion determinista | Parsear, normalizar, calcular, validar esquemas, comparar o empaquetar | Entrada/salida estructurada, errores tipados e idempotencia |
| Analisis especializado | Clasificar, sintetizar, comparar alternativas o detectar contradicciones | Criterios, evidencia, limites y evaluacion independiente |
| Gestion de artefactos internos | Crear versiones, puntos de control y VBP dentro del espacio autorizado | Historial, integridad y no sobrescritura silenciosa |
| Accion externa sensible | Correo, pago, compra, publicacion, eliminacion, despliegue o escritura externa | Fuera del MVP por defecto; exige aprobacion humana explicita si se incorpora despues |

**PRINCIPIO DE GUIA:** una herramienta debe declarar cuando usarla, entradas, devoluciones y errores; los resultados deben distinguir exito, error y pendiente (`T-DEVAGENTTOOL-B-m4-l1-es-file-8.es.pdf`, pp. 6-7 y 19).

### 5.5 Chief of Staff

| Aspecto | Contrato |
|---|---|
| Proposito | Coordinar la mision, aclararla, proponer el plan, asignar tareas autorizadas y consolidar resultados. |
| Entradas | Mision del usuario humano, decisiones vigentes, estados, dependencias, contratos y resultados de especialistas. |
| Salidas | Brief versionado, preguntas de aclaracion, plan, mapa de tareas, estado consolidado, borrador de VBP y asuntos para decision humana. |
| Herramientas como categorias | Recuperacion interna, transformacion determinista, analisis de coordinacion y gestion de artefactos internos. |
| Limites | Solo contexto necesario; no investiga como sustituto del Research Analyst; no autoaprueba plan o VBP. |
| Prohibiciones | Inventar evidencia, ocultar contradicciones, cambiar alcance, ejecutar tareas sensibles o declarar exito final. |
| Evidencia exigida | Enlace entre cada tarea y la mision, dependencia, salida, criterio, fuente y decision que la autoriza. |
| Escalamiento | Ambiguedad material, cambio de alcance, conflicto no resoluble, dependencia imposible, limite agotado o decision reservada. |

### 5.6 Research & Evidence Analyst

| Aspecto | Contrato |
|---|---|
| Proposito | Producir hallazgos respaldados por fuentes, fecha, confianza y limitaciones. |
| Entradas | Pregunta de investigacion, criterios de fuente, periodo, alcance y repositorios autorizados. |
| Salidas | Hallazgos atomicos, registros de evidencia, fuentes contradictorias, vacios, nivel de confianza con justificacion y limitaciones. |
| Herramientas como categorias | Recuperacion interna y externa de solo lectura; extraccion y normalizacion deterministas. |
| Limites | Solo fuentes autorizadas; respeta fecha y alcance; separa dato, inferencia y opinion de la fuente. |
| Prohibiciones | Tomar decisiones de producto, presentar ausencia de fuente como confirmacion, inventar citas o escribir externamente. |
| Evidencia exigida | Fuente real, localizador, fecha de publicacion si existe, fecha de consulta, afirmacion respaldada y limitaciones. |
| Escalamiento | Fuente inaccesible, conflicto material, evidencia insuficiente, dato sensible o necesidad de ampliar el universo de fuentes. |

### 5.7 Product Architect

| Aspecto | Contrato |
|---|---|
| Proposito | Convertir mision y evidencia en definicion de producto, alcance, recorrido y requisitos verificables. |
| Entradas | Brief, decisiones aprobadas, hallazgos, evidencia, riesgos y restricciones. |
| Salidas | Problema, oportunidad, usuario, propuesta de valor, alcance, recorrido, requisitos, criterios y alternativas. |
| Herramientas como categorias | Recuperacion interna, transformacion determinista y analisis de producto. |
| Limites | Mantener separaciones de producto; etiquetar toda recomendacion no aprobada. |
| Prohibiciones | Elegir infraestructura o proveedor, declarar factibilidad tecnica no probada, convertir un patron de clase en requisito. |
| Evidencia exigida | Cada requisito se vincula con mision, decision, evidencia, riesgo o principio de guia. |
| Escalamiento | Alternativas con impacto material, contradiccion entre valor y restriccion, alcance insuficiente o decision de producto faltante. |

### 5.8 Delivery Planner

| Aspecto | Contrato |
|---|---|
| Proposito | Convertir la definicion aprobada en fases, piezas, tareas, dependencias, riesgos y criterios de aceptacion. |
| Entradas | Alcance, requisitos, restricciones, riesgos, capacidades y decisiones vigentes. |
| Salidas | Secuencia, fichas de tarea, dependencias, criterios, pruebas, limites y puntos de aprobacion. |
| Herramientas como categorias | Transformacion y validacion deterministas; analisis de planificacion. |
| Limites | Una pieza pequena por vez; no presupone capacidad, fecha, costo ni paralelismo no confirmados. |
| Prohibiciones | Autorizar construccion, asignar tecnologia, ocultar camino critico o crear ciclos sin limite. |
| Evidencia exigida | Trazabilidad tarea-requisito-riesgo-prueba; supuestos de estimacion visibles. |
| Escalamiento | Dependencia circular, recurso no confirmado, plazo incompatible, presupuesto faltante o mas de dos rondas de correccion del equipo constructor. |

### 5.9 Governance & Risk

| Aspecto | Contrato |
|---|---|
| Proposito | Revisar calidad, limites, trazabilidad, riesgos, permisos y aprobaciones de forma independiente. |
| Entradas | VBP, requisitos, evidencia, registro de acciones, limites y resultados de validacion. |
| Salidas | Dictamen `PASA`, `PASA_CON_CONDICIONES` o `NO_PASA`; hallazgos con severidad, evidencia, impacto y correccion recomendada. |
| Herramientas como categorias | Validadores deterministas, recuperacion interna de solo lectura y analisis de gobernanza. |
| Limites | Evalua contra criterios declarados; no redefine la mision ni optimiza para una metrica aislada. |
| Prohibiciones | Autoaprobar el VBP, corregir silenciosamente contenido, ignorar fallas de prueba, usar Chain-of-Thought como evidencia. |
| Evidencia exigida | Matriz requisito-criterio-resultado; excepciones, datos faltantes, permisos y limites agotados. |
| Escalamiento | Riesgo critico, evidencia falsa o no verificable, accion no autorizada, criterio incorrecto, conflicto de interes o bloqueo no resuelto. |

Reglas de dictamen aprobadas para la v0:

- `PASA`: todas las secciones obligatorias estan presentes, no existen bloqueos y las afirmaciones criticas tienen evidencia.
- `PASA_CON_CONDICIONES`: el VBP es utilizable, pero conserva asuntos no criticos identificados; la aprobacion humana debe aceptar las condiciones.
- `NO_PASA`: falta contenido obligatorio, hay evidencia falsa o inexistente, contradicciones ocultas, riesgos criticos sin tratar, mezcla de productos o acciones no autorizadas.
- `NO_PASA` bloquea la aprobacion ordinaria. El usuario humano puede usar `APROBAR_CON_EXCEPCION`, pero debe registrar motivo, condiciones y riesgos aceptados.
- Governance & Risk no modifica el VBP ni utiliza una puntuacion unica como sustituto del resultado real.

## 6. Contrato completo del Venture Build Package

### 6.1 Manifest del paquete

Cada VBP contiene:

- `vbp_id`, `mission_id`, version y estado;
- titulo, fecha de creacion, fecha de corte de evidencia e idioma;
- version del contrato usada;
- huella o identificador de integridad del contenido aprobado;
- responsables funcionales por seccion;
- estado de aprobacion y referencia al registro del usuario humano;
- lista de componentes incluidos y errores o componentes faltantes.

### 6.2 Secciones obligatorias

1. Mision.
2. Problema y oportunidad.
3. Usuario objetivo.
4. Propuesta de valor.
5. Evidencia.
6. Supuestos.
7. Alcance incluido.
8. Alcance excluido.
9. Requisitos funcionales con criterios de aceptacion.
10. Requisitos no funcionales con forma de verificacion.
11. Recorrido principal.
12. Fases, tareas y dependencias.
13. Riesgos, mitigaciones y disparadores.
14. Metricas, con definicion, fuente, linea base, objetivo o estado `PENDIENTE`.
15. Decisiones tomadas.
16. Decisiones pendientes.
17. Aprobaciones.
18. Historial de trazabilidad.

### 6.3 Registro de evidencia

Cada evidencia usa los campos:

`evidence_id`, `claim_id`, titulo, autor u organizacion si consta, tipo de fuente, ubicacion o URL, pagina/seccion/marca temporal, fecha de publicacion si consta, fecha de consulta, extracto o resumen pertinente, recolector, nivel de confianza, justificacion de confianza, limitaciones, contradicciones y estado de verificacion.

Reglas:

- Una fuente puede respaldar varios `claim_id`, pero cada relacion se declara.
- La confianza no reemplaza la cita.
- La fecha de consulta no se presenta como fecha de publicacion.
- Una fuente inaccesible o no verificable no se promociona a evidencia confirmada.
- Una afirmacion material sin evidencia queda como supuesto, propuesta o pendiente.
- La investigacion es hibrida: comienza con archivos, texto y enlaces aportados por el usuario y puede usar investigacion publica de solo lectura cuando el plan aprobado la incluya.
- Una afirmacion material necesita al menos una fuente real. La confianza alta exige una fuente primaria solida o corroboracion de dos fuentes independientes.
- Una afirmacion critica sin evidencia bloquea la aprobacion ordinaria; un supuesto no critico puede mantenerse si el usuario humano lo acepta expresamente.
- Las fuentes contradictorias permanecen visibles y no se resuelven silenciosamente.

### 6.4 Registro de decisiones y aprobaciones

Cada decision contiene `decision_id`, pregunta, alternativas consideradas, decision, autoridad, fecha, fundamento, evidencia vinculada, impacto, condiciones y version afectada.

Cada aprobacion contiene `approval_id`, `user_id`, actor, accion aprobada, version o huella exacta, fecha, comentario, condiciones, expiracion si aplica y estado. Solo un registro atribuible al usuario humano satisface las puertas humanas. Una aprobacion no se edita ni elimina; si el contenido cambia, la nueva version requiere otra aprobacion. Rechazar o solicitar cambios exige motivo. La v0 no utiliza firma digital ni contrasena.

### 6.5 Historial de trazabilidad

El historial registra eventos observables: actor, accion, herramienta o categoria, fuente, entrada relevante resumida, salida o estado, error, duracion, contador de intento, decision y artefacto. No registra Chain-of-Thought ni secretos.

### 6.6 Reglas de completitud e integridad

- Ninguna seccion obligatoria puede desaparecer del paquete; si no hay contenido, muestra `PENDIENTE`, responsable y motivo.
- Las metricas no se inventan: una metrica sin linea base u objetivo lo declara.
- Los riesgos incluyen probabilidad cualitativa, impacto, mitigacion, senal de activacion y responsable funcional.
- El VBP final es exactamente la version aprobada. La exportacion puede cambiar presentacion, no significado.
- **DECISION APROBADA:** existe un unico VBP canonico en Markdown estructurado, legible por humanos y agentes, renderizado dentro de la interfaz y descargable como `.md`. El manifest forma parte del mismo documento; no existe una segunda version paralela en JSON o PDF para la v0.
- **DECISION APROBADA:** la interfaz, las conversaciones, las salidas de agentes y el VBP se presentan en espanol. Los titulos y datos de las fuentes conservan su idioma original y se resumen en espanol; los identificadores estables no se traducen.

## 7. Requisitos funcionales y criterios de aceptacion

Todos los requisitos de esta seccion son **DECISION APROBADA** mediante el `GO_CON_CONDICIONES` de la version 1.2.

| ID | Requisito funcional | Criterio de aceptacion verificable |
|---|---|---|
| RF-001 | Crear una mision con objetivo, contexto, restricciones y resultado esperado. | Dada una usuaria autorizada, al guardar campos validos se crea un `mission_id`, version 1, estado `BORRADOR` y evento de auditoria; si falta un campo obligatorio, se indica cual y no se avanza. |
| RF-002 | Editar y versionar el brief sin perder historia. | Al modificar un brief guardado se crea una nueva version; la anterior sigue consultable y el cambio muestra actor, fecha y motivo. |
| RF-003 | Identificar ambiguedades y solicitar aclaracion. | Con una mision incompleta, el sistema lista preguntas vinculadas a campos concretos y pasa a `ACLARACION_REQUERIDA`; no crea un plan ejecutable mientras exista un bloqueo. |
| RF-004 | Registrar supuestos aceptados y pendientes. | Cada supuesto muestra estado, autor, impacto y aceptacion humana cuando corresponda; un supuesto no aparece como hecho confirmado. |
| RF-005 | Generar un plan con tareas, dependencias, criterios, limites y riesgos. | Un validador confirma que cada tarea tiene ID, objetivo, agente, entrada, salida, dependencia, criterio, herramientas permitidas y presupuesto antes de `PLAN_EN_REVISION`. |
| RF-006 | Permitir que el usuario humano revise, apruebe, rechace o pida cambios al plan. | Cada accion exige una version exacta y comentario para rechazo/cambio; solo aprobar crea el evento que permite `AUTORIZADA_PARA_EJECUTAR`. |
| RF-007 | Evitar ejecutar un plan no aprobado o una version obsoleta. | Una prueba intenta iniciar ambos casos y recibe bloqueo sin crear tareas activas ni consumir intentos. |
| RF-008 | Crear tareas respetando dependencias. | Una tarea con dependencia incompleta permanece `PENDIENTE`; al completarse la dependencia pasa a `LISTA` una sola vez. |
| RF-009 | Invocar cada agente con su contrato y contexto minimo. | La inspeccion de una invocacion muestra todos los campos del sobre comun, solo herramientas autorizadas y referencias de contexto; falta de campo produce error estructurado. |
| RF-010 | Recopilar evidencia trazable por hallazgo. | Todo hallazgo material consolidado tiene `evidence_id` real y localizador, o etiqueta visible `NO_VERIFICADO`/`SUPUESTO`; el validador detecta una cita inexistente. |
| RF-011 | Registrar contradicciones, confianza y limitaciones. | Al aportar dos fuentes incompatibles, ambas permanecen visibles, se registra impacto y se crea un pendiente en lugar de elegir silenciosamente. |
| RF-012 | Producir definicion de producto sin elegir infraestructura. | La salida del Product Architect contiene problema, usuario, valor, alcance, recorrido, requisitos y criterios; una prueba de validacion marca como fuera de contrato una seleccion de proveedor o framework. |
| RF-013 | Producir un plan de entrega trazable. | Cada fase y tarea se vincula con al menos un requisito o riesgo y contiene criterio de aceptacion, prueba y dependencia; ciclos de dependencia son rechazados. |
| RF-014 | Consolidar resultados en un VBP completo. | El borrador contiene las 18 secciones de 6.2, conserva etiquetas de parcialidad y no pierde referencias de evidencia. |
| RF-015 | Evaluar el VBP contra requisitos y evidencia. | Governance & Risk entrega dictamen, matriz requisito-criterio-resultado y hallazgos con severidad, ubicacion, impacto y correccion; no modifica el contenido evaluado. |
| RF-016 | Someter la version evaluada a decision humana. | La interfaz permite aprobar, aprobar con excepcion, rechazar, pedir cambios, pausar o cancelar y registra la version exacta; ningun agente puede activar controles reservados al usuario humano. |
| RF-017 | Gestionar rechazo y revision acotada. | Un rechazo registra motivos, conserva la version y solo abre una revision cuando el usuario humano la autoriza; el contador de rondas no se reinicia. |
| RF-018 | Generar y descargar el VBP aprobado. | Solo desde `VBP_APROBADO` se produce un paquete; su manifest y huella corresponden a la version aprobada y una verificacion confirma todas las secciones. |
| RF-019 | Mostrar el recorrido, trabajo y evidencia. | Para una mision activa, el usuario humano puede ver estado general, tareas, dependencias, agente, intentos, limites, evidencia, errores y proximos puntos de decision. |
| RF-020 | Mantener auditoria sin Chain-of-Thought. | Cada evento requerido esta disponible y exportable; una inspeccion confirma ausencia de campos de razonamiento interno y presencia de decisiones resumidas. |
| RF-021 | Pausar, reanudar y cancelar. | El usuario humano puede pausar/cancelar desde cualquier estado no terminal; reanudar continua desde el ultimo punto valido y cancelar no borra historia. |
| RF-022 | Crear puntos de control y reanudar tras fallo. | Al interrumpir una ejecucion despues de un paso confirmado, la reanudacion no repite ese paso y conserva resultados, intentos y aprobaciones previos. |
| RF-023 | Aplicar errores tipados y politica de reintentos. | Los errores `INVALID_INPUT`, `NOT_FOUND`, `PERMISSION_DENIED`, `TRANSIENT_FAILURE`, `SCHEMA_INVALID`, `DEPENDENCY_FAILED`, `BUDGET_EXHAUSTED` y `SYSTEM_ERROR` producen la accion definida en 11.3. |
| RF-024 | Imponer limites finitos antes de ejecutar. | No se inicia una tarea si falta alguno de sus limites obligatorios; al alcanzar un limite pasa a `BLOQUEADA` o `PAUSADA` y solicita decision, sin nuevo intento automatico. |
| RF-025 | Proteger acciones sensibles y permisos. | Un agente sin permiso recibe `PERMISSION_DENIED`, no reintenta ni busca una ruta alternativa y genera evento de escalamiento; en el MVP no se ejecuta la accion externa. |
| RF-026 | Diferenciar funciones deterministas y tareas de razonamiento. | El plan etiqueta cada paso; validaciones, transiciones, conteos, empaquetado e idempotencia no dependen de juicio generativo, mientras los analisis incluyen criterios y limites. |
| RF-027 | Etiquetar capacidades simuladas. | Cualquier simulacion muestra `SIMULADA` en tarea, interfaz, salida y VBP; el checklist final falla si falta una de las etiquetas. |
| RF-028 | Registrar decisiones aprobadas, propuestas y pendientes por separado. | Una consulta por categoria devuelve registros disjuntos y la consolidacion no cambia la categoria sin un evento de decision autorizado. |
| RF-029 | Detectar cambios de alcance posteriores a la aprobacion. | Al modificar un elemento de alcance aprobado, el plan afectado queda obsoleto, la ejecucion nueva se bloquea y se solicita nueva aprobacion. |
| RF-030 | Verificar el paquete antes de finalizar. | `FINALIZADA` solo se alcanza si manifest, integridad, secciones, aprobacion y descarga pasan validacion; un fallo deja la mision en estado recuperable. |

## 8. Requisitos no funcionales

Todos son independientes de infraestructura.

| ID | Requisito | Verificacion | Estado |
|---|---|---|---|
| RNF-001 Auditabilidad | Toda accion material es atribuible, fechada, versionada y vinculada a su entrada/salida. | Reconstruir una mision de prueba desde la linea de tiempo sin usar Chain-of-Thought. | DECISION APROBADA; PENDIENTE DE EVIDENCIA |
| RNF-002 Integridad | No hay sobrescritura silenciosa de briefs, planes, VBP, evidencia ni aprobaciones. | Comparar versiones y detectar alteracion del paquete aprobado. | DECISION APROBADA; PENDIENTE DE EVIDENCIA |
| RNF-003 Seguridad y minimo privilegio | Cada agente y tarea solo accede a categorias y recursos autorizados. | Pruebas positivas y negativas de permisos, incluida accion sensible. | DECISION APROBADA; PENDIENTE DE EVIDENCIA |
| RNF-004 Privacidad y minimizacion | Solo se conserva informacion necesaria con alcance y retencion definidos. | Inventario de datos por campo y prueba de aislamiento entre misiones. | DECISION APROBADA: datos privados locales; nube solo para expediente saneado de competencia; sin secretos, contrasenas ni Chain-of-Thought |
| RNF-005 Reanudabilidad | Un fallo o pausa no obliga a repetir pasos confirmados ni pierde contadores. | Pruebas de interrupcion en al menos aclaracion, tarea y exportacion. | DECISION APROBADA; PENDIENTE DE EVIDENCIA |
| RNF-006 Idempotencia | Repetir la misma orden identificada no duplica efectos. | Reenviar ordenes de crear tarea, aprobar y exportar; obtener un solo efecto. | DECISION APROBADA; PENDIENTE DE EVIDENCIA |
| RNF-007 Limites y costo | Cada ejecucion tiene limites finitos visibles y detencion segura. | Pruebas de agotamiento para intentos, tiempo, solicitudes y gasto. | DECISION APROBADA: techo de USD 25, avisos al 70 %, pausa al 90 % y detencion al 100 % |
| RNF-008 Calidad evaluable | Los criterios miden el objetivo declarado y no una metrica sustituta aislada. | Casos positivos, negativos, parciales y contradictorios; revision de posibles falsos positivos. | DECISION APROBADA; PENDIENTE DE EVIDENCIA |
| RNF-009 Observabilidad | El usuario humano puede conocer estado, progreso, error, espera y consumo respecto del limite. | Inspeccion de una mision exitosa, bloqueada y reanudada. | DECISION APROBADA; PENDIENTE DE EVIDENCIA |
| RNF-010 Usabilidad | Las decisiones humanas muestran contexto, impacto, alternativas y consecuencia. | Prueba de recorrido sin consultar registros tecnicos. | DECISION APROBADA; PENDIENTE DE EVIDENCIA |
| RNF-011 Accesibilidad | La interfaz esencial puede operarse con teclado, foco visible, etiquetas y contraste suficiente. | Revision automatizada y manual de los flujos principales. | DECISION APROBADA; PENDIENTE DE EVIDENCIA |
| RNF-012 Neutralidad tecnologica | Los contratos funcionales no dependen de un proveedor o framework, salvo requisitos externos verificados y decisiones humanas expresas. | Revision del nucleo funcional y trazabilidad de cada excepcion tecnologica. | DECISION APROBADA; excepcion de concurso documentada |
| RNF-013 Mantenibilidad | Esquemas, requisitos, estados y reglas tienen version y compatibilidad declaradas. | Un cambio incompatible exige nueva version y migracion o rechazo explicito. | DECISION APROBADA; PENDIENTE DE EVIDENCIA |
| RNF-014 Actualidad de evidencia | El sistema conserva fechas y advierte evidencia potencialmente obsoleta. | Una fuente fuera del periodo de la mision aparece marcada y no se usa silenciosamente como actual. | DECISION APROBADA; el periodo concreto se fija por mision |
| RNF-015 Rendimiento | Las operaciones informan progreso y no quedan indefinidamente activas. | Cada agente termina, pausa o bloquea a los 5 minutos y la mision a los 20 minutos. | DECISION APROBADA |

## 8A. Perfil de conformidad tecnica derivado de las clases

Este perfil incorpora el checklist tecnico aportado el 28 de agosto de 2026. El checklist tiene 174 controles (78 P0, 87 P1 y 9 P2) mas 15 condiciones del gate minimo. Es una guia de aplicacion de las clases, no una obligacion de adoptar una tecnologia concreta.

Reglas de uso:

1. Todos los controles comienzan como **PENDIENTE DE EVIDENCIA**.
2. Un P0 aplicable debe demostrarse antes de presentar la v0 o declararse `NO_APLICA` con justificacion y aprobacion humana.
3. Los P1 se seleccionan para aportar profundidad tecnica; la v0 debe cubrir la mayoria de los P1 pertinentes a su recorrido, no todos indiscriminadamente.
4. Los P2 solo se incorporan despues de estabilizar P0 y P1 seleccionados.
5. Ningun control se marca completo por existir en el contrato: requiere pantalla, evento, prueba, metrica o recorrido reproducible con `evidence_id`.
6. Nombres de productos, servicios o patrones de las clases son ejemplos; se admite un equivalente justificado.

| ID | Cobertura tecnica | Disposicion para v0 | Evidencia minima de aceptacion | Estado contractual actual |
|---|---|---|---|---|
| CT-001 | Problema, objetivo, usuario, criterio de exito, alcance y casos limite | P0 obligatorio | Mision de demo, criterio determinista y matriz implementado/simulado/propuesto | PENDIENTE DE EVIDENCIA |
| CT-002 | Agente raiz, instrucciones, herramientas limitadas, funciones deterministas, esquemas y runtime equivalente | P0 obligatorio; callbacks son P2 | Ejecucion fuera de una UI de desarrollo, contrato de tools y trayectoria registrada | PENDIENTE DE EVIDENCIA |
| CT-003 | Estado estructurado, sesiones persistentes, aislamiento y recuperacion tras reinicio | P0 obligatorio | Reiniciar la aplicacion o servicio y recuperar mision, sesion, intentos y punto de control | PENDIENTE DE EVIDENCIA |
| CT-004 | Memoria de largo plazo, politica de escritura/recuperacion, visibilidad, correccion y eliminacion | P0 de politica; recuperacion semantica P2 | Mostrar que se conserva un hecho aprobado entre conversaciones y que el usuario puede revisarlo o eliminarlo | POLITICA APROBADA; PENDIENTE DE EVIDENCIA |
| CT-005 | Archivos, imagenes y artefactos vinculados a evidencia | P0 para los formatos necesarios del caso | Procesar al menos un archivo admitido, conservar referencia al original y extraer datos estructurados | FORMATOS Y LIMITES APROBADOS; PENDIENTE DE EVIDENCIA |
| CT-006 | Integracion con una fuente real o representativa y consultas gobernadas | P0 obligatorio | Consulta reproducible, parametros controlados y ruta de evidencia | PENDIENTE DE EVIDENCIA |
| CT-007 | Workflow y colaboracion entre agentes | P0 obligatorio en secuencia fija | Recorrido Chief of Staff -> Research -> Product Architect -> Delivery Planner -> Governance, una tarea a la vez | PENDIENTE DE EVIDENCIA |
| CT-008 | Pausa, reanudacion, datos frescos, errores y limites de procesos largos | P0 obligatorio; eventos externos P1/P2 condicionales | Interrupcion controlada, reanudacion sin duplicar y agotamiento seguro de limite | PENDIENTE DE EVIDENCIA |
| CT-009 | Aprobacion humana real y permisos | P0 obligatorio | El flujo se pausa realmente; una decision se responde una vez y conserva `user_id`, version, fecha y resultado | PENDIENTE DE EVIDENCIA |
| CT-010 | Evaluacion reproducible de resultado y trayectoria | P0 obligatorio | Casos con entrada, condiciones, resultado, tools esperadas, metrica determinista y umbral definido por ficha | FICHA APROBADA; PENDIENTE DE EVIDENCIA |
| CT-011 | Separacion de optimizacion, validacion y holdout | P0 obligatorio para el gate del concurso | Dataset versionado, ocho casos de desarrollo, dos holdout no vistos y regresion repetible | POLITICA APROBADA; PENDIENTE DE EVIDENCIA |
| CT-012 | Optimizacion y ciclo autoevolutivo acotado | P1 diferido; solo mejora manual y revalidada para la v0 | Linea base, propuesta de mejora, revalidacion, maximo de iteraciones y reversa humana | PRIORIZACION APROBADA; PENDIENTE DE EVIDENCIA APLICABLE |
| CT-013 | Prevencion de reward hacking | P0 obligatorio | Metricas de resultado, trayectoria y restricciones; caso de puntuacion alta con conducta incorrecta | PENDIENTE DE EVIDENCIA |
| CT-014 | Frontend controlado, backend/runtime, registros, trazas y mejora | P0 de demo; P1/P2 de produccion quedan condicionados | UI final fuera de herramienta de desarrollo y reconstruccion de una ejecucion sin Chain-of-Thought | PENDIENTE DE EVIDENCIA |
| CT-015 | Seguridad, privacidad y gobernanza | P0 obligatorio | Pruebas de permisos, ausencia de secretos, datos locales, eliminacion confirmada y advertencias de incertidumbre | PENDIENTE DE EVIDENCIA |
| CT-016 | Experiencia de usuario | P0 obligatorio | Usuario completa mision, espera, aprobacion, error y descarga sin conocer arquitectura interna | PENDIENTE DE EVIDENCIA |
| CT-017 | Evidencias para la presentacion del concurso | P0 obligatorio antes de presentar | Demo end-to-end, diagrama, evaluaciones, memoria, aprobacion, evidencia y lista honesta de estados | PENDIENTE DE EVIDENCIA |

## 9. Interfaz minima

### 9.0 Perfil local del usuario

- En el primer uso se crea un unico perfil con `user_id`, nombre y correo opcional.
- El perfil persiste localmente en el mismo dispositivo; no es un login y no solicita contrasena.
- La interfaz se presenta en espanol y atribuye decisiones, aprobaciones y eliminaciones al `user_id`.
- No existen invitaciones, equipos, sincronizacion entre dispositivos ni roles humanos adicionales en la v0.

### 9.1 Crear mision

- Campos para objetivo, contexto, restricciones, resultado esperado y fuentes iniciales.
- Indicacion de campos obligatorios, version y estado.
- Acciones `Guardar borrador`, `Enviar a aclaracion` y `Cancelar`.

### 9.2 Revisar plan

- Vista de fases, tareas, agente, dependencias, criterios, riesgos y limites.
- Diferencias entre versiones.
- Acciones exclusivas del usuario humano: `Aprobar`, `Rechazar`, `Solicitar cambios`, `Pausar` y `Cancelar`.

### 9.3 Observar trabajo

- Estado de mision y tareas, dependencias, intentos, punto de control y limites consumidos.
- Actividad resumida por agente, sin Chain-of-Thought.
- Errores, bloqueos, elementos simulados y solicitudes de decision destacados.

### 9.4 Revisar evidencia

- Lista por afirmacion con fuente, localizador, fecha, confianza, limitaciones y contradicciones.
- Filtros por verificada, no verificada, contradictoria y obsoleta.
- Navegacion desde afirmacion a evidencia y desde evidencia a secciones del VBP.

### 9.5 Aprobar o rechazar VBP

- Vista del VBP, informe de Governance & Risk, pendientes bloqueantes y diferencias de version.
- Confirmacion que identifica la version o huella exacta.
- Rechazo y solicitud de cambios requieren motivo.
- `APROBAR_CON_EXCEPCION` exige motivo y aceptacion explicita de condiciones y riesgos.
- La aprobacion es de una sola respuesta: una orden duplicada no crea una segunda aprobacion.

### 9.6 Descargar y auditar

- Descarga habilitada solo para una version aprobada y verificada.
- Acceso a manifest, contenido y auditoria.
- Un unico documento Markdown estructurado se muestra en la interfaz y se descarga como `.md`; las fuentes se enlazan mediante sus referencias y no se duplican automaticamente.
- `Cancelar` conserva la historia; `Archivar` la oculta de la vista principal; `Eliminar permanentemente` exige confirmacion humana y explica que no puede deshacerse.

## 10. Acciones deterministas frente a tareas de razonamiento

**PRINCIPIO DE GUIA:** si un paso tiene reglas y salida predecibles, debe resolverse con una funcion o validacion determinista; si requiere juicio sobre evidencia, alternativas o ambiguedad, corresponde a un agente con contrato y limites. Este principio aparece en `a5aaf8a8-fe07-4a6a-8f9a-fc29a5baa691_11_de_agosto_de_2026_2308.pdf`, pp. 3, 5-6, y en la transcripcion `Hi everyone. Uh thank you for joini.txt`, 1:25:04-1:25:38 de la primera sesion.

| Accion | Tipo | Razon |
|---|---|---|
| Validar campos y esquemas | Determinista | Reglas exactas y reproducibles |
| Crear IDs, versiones y huellas | Determinista | No requiere juicio |
| Comprobar dependencias y transiciones | Determinista | Estado y guardias conocidos |
| Contar intentos, tiempo y presupuesto | Determinista | Medicion exacta |
| Aplicar permisos e idempotencia | Determinista | Politica explicita |
| Empaquetar la version aprobada | Determinista | No debe reinterpretar contenido |
| Detectar ausencia formal de una seccion o cita | Determinista | Validacion contra contrato |
| Aclarar una mision ambigua | Razonamiento | Requiere interpretar contexto y formular preguntas |
| Sintetizar evidencia contradictoria | Razonamiento | Requiere comparar fuerza y limitaciones |
| Definir problema, alcance y propuesta de valor | Razonamiento | Implica juicio de producto, sujeto a decision humana |
| Proponer fases y riesgos | Razonamiento | Requiere analizar dependencias y compensaciones |
| Evaluar coherencia y suficiencia cualitativa | Razonamiento con controles deterministas | Combina juicio independiente y checklist verificable |
| Aprobar plan o VBP | Humana | Autoridad exclusiva del usuario humano |

No se usa razonamiento generativo para rutas de aprobacion, permisos, limites o transiciones reservadas. **PRINCIPIO DE GUIA:** los flujos estructurados pueden limitar que herramientas o agentes son accesibles en cada etapa e insertar una pausa humana (`f8fda720-0ba5-4713-9b93-73f51d0d1a3a_13_de_agosto_de_2026_2309.pdf`, p. 5).

## 11. Trazabilidad, permisos, limites, reanudacion y fallos

### 11.1 Trazabilidad minima

Todo evento material incluye:

`event_id`, `mission_id`, `task_id` si aplica, actor, rol, accion, fecha/hora, version, estado anterior/nuevo, herramienta o categoria, fuente o artefacto, resultado resumido, error tipado, intento, limite consumido, aprobacion relacionada y clave de idempotencia.

### 11.2 Permisos

- El unico usuario humano puede crear, decidir, pausar, cancelar, aprobar y descargar.
- Chief of Staff puede proponer y coordinar solo dentro de un plan autorizado.
- Los especialistas solo leen el contexto y usan las categorias declaradas en su tarea.
- Governance & Risk lee y evalua; no reescribe la salida evaluada ni aprueba como A0.
- Las escrituras internas se limitan a artefactos de la mision y generan version/evento.
- Las acciones externas sensibles estan denegadas por defecto.
- En el entorno personal, perfil, misiones, planes, evidencia, decisiones, aprobaciones y VBP se guardan localmente. La demostracion desplegada utiliza solo el expediente saneado y puede persistir sus datos de prueba en Firestore y Cloud Storage. No se guardan contrasenas, credenciales, secretos ni Chain-of-Thought, y los documentos privados no se sincronizan con la nube.

### 11.3 Matriz de fallos y reintentos

Los valores numericos de reintento y detencion de esta seccion son **DECISION APROBADA** para la v0.

| Error | Reintento automatico | Accion |
|---|---:|---|
| `INVALID_INPUT` | 0 | Indicar campo y solicitar correccion. |
| `NOT_FOUND` | 0 con la misma entrada | Pedir verificacion o fuente alternativa autorizada. |
| `PERMISSION_DENIED` | 0 | Detener y escalar; no buscar una via alternativa. |
| `TRANSIENT_FAILURE` | 1 | Reintentar una vez; si falla, guardar punto de control y bloquear. |
| `SCHEMA_INVALID` | 1 | Solicitar una regeneracion con el error del validador; luego bloquear. |
| `DEPENDENCY_FAILED` | 0 | Bloquear tareas descendientes y notificar impacto. |
| `BUDGET_EXHAUSTED` | 0 | Pausar y pedir decision humana. |
| `SYSTEM_ERROR` | 0 por defecto | Conservar diagnostico y punto de control; solo reintentar con regla aprobada. |

**PRINCIPIO DE GUIA:** distintos errores requieren respuestas distintas; un fallo temporal puede admitir un intento, mientras entrada invalida o permiso denegado exige correccion o escalamiento (`T-DEVAGENTTOOL-B-m5-l1-es-file-10.es.pdf`, pp. 4-6).

### 11.4 Limites aprobados para la v0

| Dimension | Limite v0 | Al agotarse |
|---|---:|---|
| Ciclos de aclaracion iniciados por el sistema | 3 por version de brief | `BLOQUEADA`, decision humana |
| Intentos de una tarea de razonamiento | 2 totales | `BLOQUEADA` o `PARTIAL` segun evidencia |
| Reintentos de error transitorio de herramienta | 1 | `BLOQUEADA` |
| Rondas de correccion del VBP | 2 | Nueva decision humana |
| Misiones activas simultaneas | 1 | No iniciar otra hasta finalizar, cancelar o archivar la activa |
| Agentes especialistas simultaneos | 1 | Mantener la secuencia fija |
| Descomposicion recursiva o agentes dinamicos | 0 en v0 | Detener expansion y usar la secuencia aprobada |
| Tiempo maximo por ejecucion de agente | 5 minutos | `PAUSADA` |
| Tiempo maximo por mision | 20 minutos | `PAUSADA` |
| Solicitudes totales a agentes por mision | 15 | `PAUSADA` |
| Presupuesto monetario total | USD 25 de gasto real | Avisar al 70 %, pausar al 90 % y detener al 100 %; ampliar requiere nueva aprobacion humana |
| Cloud Run | Minimo 0 y maximo 1 instancia para la demo | No aumentar automaticamente |
| Demo publica | 5 ejecuciones diarias | Mostrar VBP de ejemplo en modo lectura al agotar el limite |

Los numeros no se heredan de los ejemplos educativos; fueron aprobados por el usuario para forzar finitud en la v0. **PRINCIPIO DE GUIA:** ancho, profundidad, maximo de rondas y criterio de salida evitan consumo indefinido (`a5aaf8a8-fe07-4a6a-8f9a-fc29a5baa691_11_de_agosto_de_2026_2308.pdf`, p. 3; `Hi everyone. Uh thank you for joini.txt`, 1:15:29-1:17:23 y 1:24:44-1:25:38 de la primera sesion).

### 11.5 Reanudacion

Se crea punto de control al menos despues de:

1. guardar o aclarar el brief;
2. aprobar el plan;
3. completar cada tarea;
4. adjuntar evidencia;
5. consolidar una version de VBP;
6. emitir la evaluacion;
7. decidir el VBP;
8. verificar la exportacion.

El punto de control guarda estado estructurado, artefactos, dependencias, intentos y autorizaciones; no una transcripcion interna de razonamiento. **PRINCIPIO DE GUIA:** los procesos largos necesitan estado durable, puntos de control y recuperacion para no repetir trabajo costoso (`f8fda720-0ba5-4713-9b93-73f51d0d1a3a_13_de_agosto_de_2026_2309.pdf`, pp. 2 y 4; `Hi everyone. Uh thank you for joini.txt`, 26:04-27:09 y 1:08:32-1:09:23 de la tercera sesion).

### 11.6 Politica aprobada de memoria

La v0 separa dos alcances:

1. **Memoria de sesion o mision:** se genera automaticamente como estado estructurado para guardar objetivo, respuestas, plan, tareas, evidencia, decisiones, versiones, limites y punto de continuacion. Sirve para reanudar la misma mision.
2. **Memoria aprobada entre misiones:** contiene solo hechos consolidados, preferencias, restricciones, decisiones y referencias a VBP aprobados. Se propone al aprobar/cerrar un VBP o cuando el usuario solicita expresamente recordar algo; solo se guarda con confirmacion humana.

Reglas:

- No se guardan conversaciones completas, borradores ni razonamientos internos.
- El usuario puede ver, confirmar, corregir y eliminar memorias.
- Chief of Staff es el unico agente que consulta la memoria completa y propone nuevos recuerdos. Los especialistas reciben solo el fragmento necesario; Governance puede verificar referencia, version y autorizacion, pero no modificar.
- Las memorias normales pueden recuperarse automaticamente y se muestran en el plan. Si contradicen la solicitud actual, parecen desactualizadas o pueden cambiar materialmente el resultado, quedan bloqueadas y no pueden usarse hasta que el usuario las confirme, corrija o descarte.
- Corregir crea una nueva version; la anterior queda inactiva en auditoria y no vuelve a utilizarse.
- Eliminar borra definitivamente el contenido y conserva solo `memory_id`, fecha, usuario y mision de origen. El evento no permite recuperar el texto.
- La memoria de mision se conserva mientras exista la mision. La memoria entre misiones permanece hasta correccion o eliminacion. Informacion sensible o dependiente del tiempo incluye fecha de revision y se bloquea al vencer.
- Eliminar una memoria no altera retroactivamente un VBP ya aprobado; impide reutilizarla en misiones futuras.

### 11.7 Politica aprobada de archivos e imagenes

- Formatos v0: `.pdf`, `.docx`, `.txt`, `.md`, `.png`, `.jpg`, `.jpeg` y enlaces web publicos. CSV y Excel se difieren salvo nueva necesidad demostrada.
- Limites: 5 archivos por mision, 20 MB por archivo, 50 MB totales y 10 enlaces. Una entrada excedida se rechaza completa y puede reemplazarse.
- Cuando un archivo es evidencia se conserva el original como artefacto local con huella, tipo, tamano, mision y version; todo dato extraido mantiene referencia al original.
- Si el original desaparece antes de aprobar el VBP, la mision se pausa en `EVIDENCIA_REQUERIDA`. El usuario debe restaurar, reemplazar o retirar las afirmaciones dependientes; ningun agente puede ignorar el problema.
- Si el original se elimina despues de aprobar, el VBP y su aprobacion historica permanecen, la evidencia queda `ELIMINADA_POR_EL_USUARIO` y el VBP se marca como ya no completamente verificable.
- Archivos con contrasenas, claves API, tokens, credenciales de pago u otros secretos se bloquean y requieren una copia saneada.
- Datos personales o empresariales confidenciales pausan el procesamiento, muestran una advertencia y requieren confirmacion humana. Cada agente recibe solo el fragmento estrictamente necesario.
- El expediente publico de competencia utiliza copias autorizadas y saneadas; conserva referencia a fuentes privadas sin publicar sus originales.

### 11.8 Politica aprobada de evaluacion

El dictamen combina bloqueadores con una puntuacion de 100 puntos:

- `PASA`: 80 o mas y ningun bloqueador.
- `PASA_CON_CONDICIONES`: 70 a 79 y ningun bloqueador.
- `NO_PASA`: menos de 70 o al menos un bloqueador.

Bloquean: seccion obligatoria ausente, afirmacion critica sin evidencia valida, mezcla de productos, contradiccion o riesgo critico oculto, accion no autorizada o incumplimiento del recorrido/aprobacion humana.

Pesos: evidencia y trazabilidad 30; completitud y coherencia 25; correspondencia con la mision y valor 20; viabilidad de tareas/dependencias 15; riesgos, limites y gobernanza 10. Los bloqueadores se revisan antes de puntuar.

La suite inicial contiene diez misiones: correcta, ambigua, evidencia insuficiente, fuentes contradictorias, mezcla de productos, rechazo/correccion, interrupcion/reanudacion, evidencia eliminada, memoria conflictiva/desactualizada y accion no autorizada. Ocho son de desarrollo y dos `holdout`.

Cada caso registra entrada, condiciones, resultado, estados, herramientas permitidas/prohibidas, aprobaciones, evidencia, puntuacion y causa de fallo. Cada cambio crea una version inmutable; el agente no ve el resultado esperado ni las reglas especificas del holdout antes de terminar. Un fallo real puede proponerse para la siguiente version tras revision humana, sin alterar resultados pasados y sin datos sensibles ni duplicados.

### 11.9 Perfil aprobado de competencia

- Categoria: **Collaborative Partner**.
- Mision de demo: ayudar en 48 horas a una fundadora sin equipo a decidir si su producto digital esta listo para una beta controlada, convirtiendo documentos dispersos y contradictorios en un VBP verificable.
- Producto concursante: OminAI HQ. Iniciativa cliente: OminAI Business OS. La interfaz, el video y la documentacion mantienen esta separacion.
- Desarrollo local con interfaz propia y backend controlado; demostracion desplegada con Gemini 3.5 Flash o posterior, Google ADK, Cloud Run, Firestore y Cloud Storage.
- La identidad de servicio y credenciales de infraestructura se administran mediante el entorno seguro de Google Cloud; nunca se incluyen en prompts, repositorio, expediente de demo ni archivos descargables.
- Los cinco agentes son ejecuciones reales y separadas. Las transiciones son deterministas; un fallo pausa y se muestra, nunca se sustituye con una respuesta ficticia.
- Repositorio publico con codigo, instrucciones, diagrama, pruebas y datos saneados; sin credenciales ni documentos privados.
- Interfaz de demo bilingue `ES / EN` para mision, estados, decisiones, evidencia, errores, puntuacion y VBP. La narracion puede ser en espanol, con subtitulos en ingles incorporados manualmente al video.
- La mision preparada para video tiene objetivo de 2 minutos y 30 segundos dentro del limite general de 20 minutos. Incumplir el objetivo bloquea la declaracion `LISTA_PARA_DEMO`.
- La demo publica es un entorno separado: expediente saneado, sin carga privada ni mision libre, maximo 5 ejecuciones diarias, sin acciones externas y con VBP de ejemplo en modo lectura cuando se agota el cupo.
- El video dura maximo cuatro minutos, muestra ejecucion real, arquitectura y prueba visible de Google Cloud. El objetivo interno de v0 es el 30 de agosto de 2026; el cierre oficial verificado es el 31 de agosto de 2026 a las 5:00 p. m. PT.

## 12. Riesgos, supuestos, propuestas y decisiones pendientes

### 12.1 Riesgos del MVP

| Riesgo | Impacto | Control contractual |
|---|---|---|
| Evidencia inventada o mal atribuida | VBP no confiable | Localizador obligatorio, validacion y etiqueta `NO_VERIFICADA` |
| Evidencia obsoleta | Decision basada en contexto vencido | Fechas, periodo de vigencia y advertencia de actualidad |
| Metrica mal elegida o manipulada | Falso positivo de calidad | Criterios multiples, casos negativos y revision independiente |
| Bucle o descomposicion sin limite | Costo y tiempo no controlados | Limites previos, contadores persistentes y detencion segura |
| Exceso de persistencia | Riesgo de privacidad y contexto cruzado | Alcances de datos y politica de retencion |
| Contexto excesivo o contaminado | Deriva y resultados incoherentes | Contexto minimo por tarea y agentes especializados |
| Accion no autorizada | Impacto externo o legal | Minimo privilegio, denegacion por defecto y aprobacion humana |
| Repeticion tras fallo | Duplicados, costo o inconsistencia | Checkpoints e idempotencia |
| Evaluador que corrige su propia referencia | Sesgo y perdida de independencia | Governance reporta; no reescribe ni aprueba |
| Apariencia de madurez | Confundir prototipo con produccion | Etiquetas de estado, pruebas reales y prohibicion de sobreafirmar |
| Mezcla de productos | Alcance incorrecto | Reglas de identidad y validacion de terminos |
| Fuente local faltante | Trazabilidad incompleta | Registrar ausencia; no inventar ni sustituir sin autorizacion |

**PRINCIPIO DE GUIA:** el historial conversacional no basta para decisiones programaticas y los datos con vidas distintas requieren alcances distintos para evitar fugas y cruces de contexto (`T-DEVAGENTMEM-B-m1-l0-es-file-1.es.pdf`, pp. 1-2; `T-DEVAGENTMEM-B-m3-l0-es-file-5.es.pdf`, pp. 1-2).

### 12.2 Supuestos y limites vigentes

- Niko es la A0 actual del proyecto; dentro del producto, la identidad funcional y auditable es `usuario humano`.
- Una mision produce un unico VBP canonico en Markdown, con versiones historicas y una aprobacion vinculada a una version exacta.
- La evidencia es hibrida: primero se usan archivos, texto o enlaces aportados; la investigacion publica de solo lectura se permite cuando el plan aprobado la incluye.
- El recorrido de la v0 es fijo y secuencial: Chief of Staff, Research & Evidence Analyst, Product Architect, Delivery Planner y Governance & Risk.
- Solo puede existir una mision activa y un agente especialista en ejecucion a la vez.
- La v0 termina en un VBP aprobado y descargable; no construye, compra, publica, despliega ni ejecuta la iniciativa descrita.
- Los controles del checklist tecnico permanecen pendientes hasta que exista evidencia reproducible; su inclusion en este contrato no equivale a implementacion.

### 12.3 Decisiones de v0 aprobadas

| ID | Decision aprobada | Resultado contractual | Estado |
|---|---|---|---|
| DN-001 | Limites finitos de razonamiento y correccion. | Maximo 3 ciclos de aclaracion, 2 intentos de razonamiento por tarea, 1 reintento transitorio y 2 rondas de correccion del VBP. | APROBADA |
| DN-002 | Limites temporales, de solicitudes y costo. | Maximo 5 minutos por agente, 20 minutos por mision, 15 solicitudes totales y USD 25 de gasto real total, con avisos y detencion progresiva. | APROBADA |
| DN-003 | Politica de evidencia hibrida. | Toda afirmacion material requiere fuente real; confianza alta requiere fuente primaria fuerte o dos fuentes independientes; una afirmacion critica sin sustento bloquea la aprobacion ordinaria. | APROBADA |
| DN-004 | Privacidad y ciclo de datos. | Persistencia local para datos privados; la nube solo recibe el expediente saneado de competencia. No guardar contrasenas, secretos ni Chain-of-Thought. Cancelar conserva, archivar oculta y eliminar exige confirmacion irreversible. | APROBADA |
| DN-005 | Formato del VBP. | Un solo artefacto canonico Markdown, visible en la interfaz y descargable como `.md`; las fuentes se referencian, no se copian automaticamente. | APROBADA |
| DN-006 | Puerta del plan. | El plan siempre requiere aprobacion humana explicita antes de ejecutar agentes especialistas. | APROBADA |
| DN-007 | Dictamen de gobernanza. | `PASA`, `PASA_CON_CONDICIONES` o `NO_PASA`; un `NO_PASA` bloquea la aprobacion ordinaria, pero el usuario puede aprobar con excepcion documentada. | APROBADA |
| DN-008 | Concurrencia. | Una mision activa, especialistas secuenciales y sin agentes dinamicos, recursivos o paralelos en la v0. | APROBADA |
| DN-009 | Idioma. | Producto en espanol; la demo muestra `ES / EN` en contenido importante y el video incorpora subtitulos en ingles. Metadatos de fuentes conservan idioma original e identificadores estables. | APROBADA |
| DN-010 | Usuario de la v0. | Un unico perfil humano local y persistente; sin login real, contrasena, equipos ni roles adicionales. | APROBADA |
| DN-011 | Registro de aprobacion. | Incluye identidad local, version exacta, fecha, decision y comentario; no se edita ni elimina y cualquier cambio posterior exige una nueva aprobacion. No requiere firma ni contrasena. | APROBADA |
| DN-012 | Limite funcional. | La v0 termina en el VBP; la ejecucion posterior de la iniciativa queda fuera de alcance. | APROBADA |
| DT-013 | Terminologia de autoridad. | En requisitos, interfaz, eventos y auditoria se usa `aprobacion humana` o `aprobacion del usuario`, no `aprobacion de Niko`. | APROBADA |

### 12.4 Resolucion de pendientes derivados del checklist tecnico

Las decisiones humanas de PT-001 a PT-008 estan resueltas. `RESUELTO` define el contrato; no significa que la capacidad ya tenga evidencia ejecutable.

| ID | Resolucion aprobada | Estado de decision | Evidencia aun necesaria |
|---|---|---|---|
| PT-001 | Techo de USD 25; avisar al 70 %, pausar al 90 % y detener al 100 %; ninguna ampliacion automatica. | RESUELTO | Prueba de contadores, avisos y detencion |
| PT-002 | Dos alcances de memoria, confirmacion humana para persistir entre misiones, recuperacion bloqueada ante conflicto, correccion versionada y eliminacion privada. | RESUELTO | Pruebas de escritura, recuperacion, bloqueo, correccion y eliminacion |
| PT-003 | PDF, DOCX, TXT, MD, PNG, JPG/JPEG y enlaces; 5 archivos, 20 MB por archivo, 50 MB totales y 10 enlaces; controles de evidencia y secretos. | RESUELTO | Pruebas de formato, limites, extraccion, desaparicion y saneamiento |
| PT-004 | Dictamen por bloqueadores y escala 100: `PASA` >=80, condicional 70-79 y `NO_PASA` <70 o con bloqueador; pesos y trayectoria definidos. | RESUELTO | Implementar y ejecutar la ficha reproducible |
| PT-005 | Suite versionada de 10 casos, ocho de desarrollo y dos holdout; resultados inmutables y fallos reales como candidatos revisados. | RESUELTO | Dataset, ejecuciones y evidencia de no fuga |
| PT-006 | Priorizar persistencia, esquemas, artefactos, secuencia, aprobacion, evaluacion, logs, privacidad y recuperacion; diferir vectorial, paralelismo, eventos y autooptimizacion. | RESUELTO | Matriz P1 seleccionada con pruebas o diferimiento explicito |
| PT-007 | Localhost para desarrollo y Google Cloud para concurso: Gemini 3.5+, Google ADK, Cloud Run, Firestore y Cloud Storage; cinco agentes reales y checkpoints deterministas. | RESUELTO | Implementacion, despliegue y prueba visible de Google Cloud |
| PT-008 | Collaborative Partner; mision de beta en 48 horas; Business OS como iniciativa cliente separada; expediente saneado, repo publico, demo bilingue y entorno publico acotado. | RESUELTO | Video, diagrama, README, demo publica y paquete Devpost |

## 13. Secuencia funcional de construccion por piezas

Esta secuencia sigue el orden aprobado de `AGENTS.md`. No autoriza construccion por si misma. Cada pieza requiere ficha, aprobacion humana del encargo, construccion unica por Antigravity, inspeccion de Chipi/Codex, revision independiente de Copilot y aceptacion humana.

| Orden | Pieza | Resultado demostrable | Dependencia | Puerta de salida |
|---:|---|---|---|---|
| 0 | Cierre del contrato y pendientes tecnicos | Registro DN aprobado y PT resuelto o diferido expresamente | Este documento | Go humano del contrato |
| 1 | Contratos y esquemas | Estados, eventos, entradas, salidas y validadores acordados | Pieza 0 | Pruebas de esquemas y transiciones |
| 2 | Estructura minima | Proyecto ejecutable sin funciones de producto no solicitadas | Pieza 1 | Prueba basica y limites de archivos |
| 3 | Recorrido vertical Mision a VBP | Camino completo con datos controlados y etiquetas de simulacion | Pieza 2 | Prueba de extremo a extremo del happy path y rechazos |
| 4 | Chief of Staff | Aclaracion, plan y consolidacion bajo contrato | Pieza 3 | Casos completos, ambiguos y cambio de alcance |
| 5 | Research & Evidence Analyst | Hallazgos con evidencia, contradiccion y vacio | Pieza 4 | Pruebas de fuente real, ausente y conflictiva |
| 6 | Product Architect | Definicion y requisitos trazables sin infraestructura | Pieza 5 | Revision de alcance y criterios |
| 7 | Delivery Planner | Fases, tareas, dependencias y limites | Pieza 6 | Deteccion de dependencia circular y tarea incompleta |
| 8 | Governance & Risk | Dictamen independiente y matriz de cumplimiento | Piezas 5-7 | Casos pasa, condicional y no pasa |
| 9 | Evidencia y trazabilidad | Navegacion afirmacion-fuente-evento | Piezas 3-8 | Reconstruccion de una mision |
| 10 | Persistencia y reanudacion | Checkpoints, aislamiento e idempotencia | Pieza 9 | Pruebas de interrupcion y duplicado |
| 11 | Evaluacion, holdout y antimanipulacion | Suite versionada, casos negativos, trayectorias y controles contra reward hacking | Piezas 8-10 | CT-010 a CT-013 demostrados |
| 12 | Aprobacion humana y reanudacion | Puertas de plan y VBP, rechazo, excepcion, pausa y continuidad | Piezas 8-11 | Ningun actor no humano puede aprobar |
| 13 | Interfaz y exportacion | Crear, revisar, observar, evidenciar, decidir y descargar `.md` | Piezas 3-12 | Recorrido visual y accesibilidad esencial |
| 14 | Despliegue controlado de competencia | Backend en Cloud Run, estado de demo en Firestore y artefactos saneados en Cloud Storage | Pieza 13 | Prueba visible de nube, seguridad, limites y escala cero |
| 15 | Pruebas integrales y paquete de competencia | VBP, auditoria, video, arquitectura, metricas, README, limites y diferenciador | Pieza 14 | Gate minimo y P0 aplicables con evidencia |

No se trabaja simultaneamente sobre los mismos archivos y no se permiten mas de dos rondas de correccion sin nueva decision humana (`AGENTS.md`, "Forma de trabajo"; `TEAM-WORKFLOW.md`, "Flujo").

## 14. Matriz de trazabilidad

La columna de fuentes usa nombres de archivos reales, secciones, paginas o marcas temporales. El encargo escrito se conserva en `C:\Users\Nivez\.codex\attachments\ec85c4ee-1b2f-4f45-8914-b99c10ac2aad\pasted-text.txt`.

| Requisitos | Fundamento | Clasificacion | Fuentes reales |
|---|---|---|---|
| RF-001 a RF-004 | Mision, aclaracion, autoridad y separacion de categorias | DECISION APROBADA; versionado aprobado con este contrato | `pasted-text.txt`, "VERDAD DEL PRODUCTO" y "REGLAS DE EVIDENCIA"; `AGENTS.md`, "Autoridad y roles" |
| RF-005 a RF-009 | Plan, tareas, contratos y autorizacion humana | DECISION APROBADA; puerta del plan aprobada | `pasted-text.txt`, "Flujo principal" y "DOCUMENTO REQUERIDO"; `TEAM-WORKFLOW.md`, "Plantilla de ficha de pieza"; `a5aaf8a8-fe07-4a6a-8f9a-fc29a5baa691_11_de_agosto_de_2026_2308.pdf`, pp. 5-6 |
| RF-010 y RF-011 | Evidencia con fuente, fecha, confianza, limitaciones y contradicciones | DECISION APROBADA | `pasted-text.txt`, "Equipo interno" y "REGLAS DE EVIDENCIA" |
| RF-012  | Arquitectura funcional sin seleccion tecnologica | DECISION APROBADA | `pasted-text.txt`, "LIMITES"; `AGENTS.md`, "Reglas de construccion" |
| RF-013 | Fases, tareas, dependencias, riesgos y criterios | DECISION APROBADA | `pasted-text.txt`, "Equipo interno" y "VBP"; `TEAM-WORKFLOW.md`, "Plantilla de ficha de pieza" |
| RF-014 a RF-018 | Consolidacion, evaluacion, aprobacion y VBP final | DECISION APROBADA; version y huella aprobadas | `pasted-text.txt`, "Flujo principal" y "VBP"; `AGENTS.md`, "Autoridad y roles" |
| RF-019 y RF-020 | Interfaz de observacion y auditoria sin Chain-of-Thought | DECISION APROBADA | `pasted-text.txt`, "DOCUMENTO REQUERIDO" y "LIMITES"; `AGENTS.md`, "Reglas de construccion" |
| RF-021 y RF-022 | Pausa, cancelacion, checkpoints y reanudacion | DECISION APROBADA para autoridad; PRINCIPIO DE GUIA para recuperacion | `pasted-text.txt`, "AUTORIDAD"; `f8fda720-0ba5-4713-9b93-73f51d0d1a3a_13_de_agosto_de_2026_2309.pdf`, pp. 2 y 4; `Hi everyone. Uh thank you for joini.txt`, 26:04-27:09 y 1:08:32-1:09:23 de la tercera sesion |
| RF-023 y RF-024 | Errores tipados, reintentos y limites finitos | DECISION APROBADA + PRINCIPIO DE GUIA | `AGENTS.md`, "Reglas de construccion"; `T-DEVAGENTTOOL-B-m5-l1-es-file-10.es.pdf`, pp. 4-6; `Hi everyone. Uh thank you for joini.txt`, 1:15:29-1:17:23 de la primera sesion |
| RF-025 | Aprobacion de acciones sensibles y minimo privilegio | DECISION APROBADA + PRINCIPIO DE GUIA | `AGENTS.md`, "Reglas de construccion"; `f8fda720-0ba5-4713-9b93-73f51d0d1a3a_13_de_agosto_de_2026_2309.pdf`, p. 5; `Hi everyone. Uh thank you for joini.txt`, 1:26:03-1:26:21 de la tercera sesion |
| RF-026 | Funciones para lo determinista y agentes para razonamiento | DECISION APROBADA + PRINCIPIO DE GUIA | `AGENTS.md`, "Reglas de construccion"; `a5aaf8a8-fe07-4a6a-8f9a-fc29a5baa691_11_de_agosto_de_2026_2308.pdf`, pp. 3 y 5-6 |
| RF-027 | Etiquetado de simulaciones | DECISION APROBADA | `AGENTS.md`, "Reglas de revision" |
| RF-028 y RF-029 | Separacion de categorias y revalidacion de alcance | DECISION APROBADA; invalidacion aprobada | `pasted-text.txt`, "REGLAS DE EVIDENCIA"; `AGENTS.md`, "Forma de trabajo" |
| RF-030 | Verificacion antes de finalizar | DECISION APROBADA; validacion final aprobada | `pasted-text.txt`, "CRITERIOS DE EXITO"; `AGENTS.md`, "Reglas de revision" |
| RNF-001 a RNF-003 | Auditoria, integridad, seguridad y permisos | DECISION APROBADA | `pasted-text.txt`, "VBP" y "CRITERIOS DE EXITO"; `AGENTS.md`, "Reglas de construccion" y "Reglas de revision" |
| RNF-004 | Alcance de estado, memoria y privacidad | PRINCIPIO DE GUIA + DECISION APROBADA | `T-DEVAGENTMEM-B-m1-l0-es-file-1.es.pdf`, pp. 1-2; `T-DEVAGENTMEM-B-m3-l0-es-file-5.es.pdf`, pp. 1-2; secciones 11.6 y 11.7 de este contrato |
| RNF-005 y RNF-006 | Reanudacion e idempotencia | PRINCIPIO DE GUIA + DECISION APROBADA | `f8fda720-0ba5-4713-9b93-73f51d0d1a3a_13_de_agosto_de_2026_2309.pdf`, pp. 2 y 4; `Hi everyone. Uh thank you for joini.txt`, 1:08:32-1:09:23 de la tercera sesion |
| RNF-007 | Limites y costo | DECISION APROBADA + PRINCIPIO DE GUIA | `AGENTS.md`, "Reglas de construccion"; `a5aaf8a8-fe07-4a6a-8f9a-fc29a5baa691_11_de_agosto_de_2026_2308.pdf`, p. 3; `Hi everyone. Uh thank you for joini.txt`, 1:17:08-1:17:23 de la primera sesion |
| RNF-008 | Calidad evaluable y riesgo de optimizar la metrica incorrecta | PRINCIPIO DE GUIA + DECISION APROBADA | `Hi everyone. Uh thank you for joini.txt`, 42:31-59:28 de la primera sesion |
| RNF-009 a RNF-011 | Observabilidad, decisiones comprensibles y accesibilidad | DECISION APROBADA | `pasted-text.txt`, "DOCUMENTO REQUERIDO"; criterios de producto de este contrato |
| RNF-012 | Neutralidad tecnologica | DECISION APROBADA | `pasted-text.txt`, "LIMITES"; `AGENTS.md`, "Reglas de construccion" |
| RNF-013 a RNF-015 | Versionado, actualidad y detencion temporal | DECISIONES APROBADAS | `f8fda720-0ba5-4713-9b93-73f51d0d1a3a_13_de_agosto_de_2026_2309.pdf`, pp. 2-4; secciones 11.4 a 11.9 de este contrato |
| CT-001 a CT-017 | Cobertura tecnica de las clases, priorizada por pertinencia y evidencia | PENDIENTE DE EVIDENCIA; P0 obligatorio o N/A justificado | `C:\Users\Nivez\.codex\attachments\fdeaf8bc-b68b-4c32-a227-f9a9938831af\pasted-text.txt`, secciones 1 a 17; seccion 8A y Anexo C de este contrato |
| Gate tecnico de competencia | Quince comprobaciones minimas antes de presentar | PENDIENTE DE EVIDENCIA | `C:\Users\Nivez\.codex\attachments\fdeaf8bc-b68b-4c32-a227-f9a9938831af\pasted-text.txt`, "Gate minimo antes de presentar"; seccion 15.7 y Anexo C |
| PT-001 a PT-008 | Memoria, archivos, evaluacion, seleccion P1, arquitectura y presentacion | DECISIONES APROBADAS; IMPLEMENTACION PENDIENTE DE EVIDENCIA | Secciones 11.6 a 11.9 y 12.4; reglas oficiales del concurso en Anexo A.4 |

## 15. Checklist Go/No-Go para aprobar el contrato

El usuario humano marca cada elemento. Un elemento bloqueante sin resolver produce **NO-GO**. Aprobar este contrato autoriza preparar piezas; no certifica que el producto ya cumpla el checklist tecnico.

### 15.1 Autoridad y alcance

- [x] El usuario humano confirma que esta version refleja la mision del producto.
- [x] Se mantienen separados Ominai, OminAI HQ, Business OS, Omi y OminaiTech Engine.
- [x] Se ratifica DN-012: la v0 termina en el VBP aprobado y descargable.
- [x] El nucleo funcional sigue neutral y la excepcion tecnologica del concurso esta justificada, aprobada y trazada a las reglas oficiales.
- [x] No hay afirmaciones de produccion o capacidades implementadas sin evidencia.

### 15.2 Flujo y agentes

- [x] El recorrido Mision a VBP tiene entradas, salidas y puertas claras.
- [x] El usuario humano aprueba los estados y transiciones.
- [x] Se ratifica DN-006: el plan siempre exige aprobacion humana previa.
- [x] Los cinco agentes tienen proposito, entradas, salidas, herramientas por categoria, limites, prohibiciones, evidencia y escalamiento.
- [x] Ningun agente puede aprobar su propia salida ni sustituir al usuario humano.

### 15.3 VBP, evidencia y evaluacion

- [x] Las 18 secciones obligatorias del VBP son suficientes.
- [x] Se ratifica DN-003 sobre fuentes y suficiencia de evidencia.
- [x] Se ratifica DN-005: un Markdown canonico visible y descargable.
- [x] Se ratifica DN-007: `PASA`, `PASA_CON_CONDICIONES`, `NO_PASA` y excepcion humana documentada.
- [x] Propuestas, supuestos, pendientes y decisiones aprobadas permanecen separados.
- [x] Las citas apuntan a archivos reales, paginas o marcas temporales identificables.

### 15.4 Seguridad, limites y continuidad

- [x] El usuario humano ratifica los limites de 11.4.
- [x] Se ratifican DN-002 y PT-001: techo de USD 25 y detencion progresiva.
- [x] Se ratifican DN-004 y PT-002: memoria controlada, datos privados locales y solo expediente saneado en nube.
- [x] Reintentos, errores, pausas y escalamiento tienen comportamiento finito.
- [x] Las acciones sensibles estan denegadas por defecto y requieren aprobacion humana explicita si se incorporan.
- [x] La reanudacion conserva estado, intentos, resultados y aprobaciones sin guardar Chain-of-Thought.

### 15.5 Preparacion para construir

- [x] Todos los RF tienen criterio de aceptacion verificable.
- [x] Los RNF tienen metodo de verificacion y sus pendientes estan resueltos o diferidos expresamente.
- [x] Los CT P0 aplicables tienen una ruta de evidencia o una declaracion N/A que requerira aprobacion humana.
- [x] La primera pieza autorizada es pequena y debe recibir ficha completa con archivos permitidos/prohibidos antes de construir.
- [x] Antigravity es el unico constructor de la pieza.
- [x] Chipi/Codex y Copilot revisaran sin modificar el codigo.
- [x] El usuario humano registra decision final: `GO_CON_CONDICIONES`.

### 15.6 Registro de decision

```text
Version del contrato: 1.2-aprobada
Decision: GO_CON_CONDICIONES
Condiciones o cambios exigidos:
- Antigravity permanece como unico constructor.
- Cada pieza debe producir evidencia ejecutable contra sus criterios.
- Ningun control CT se marca implementado antes de demostrarlo.
- OminAI HQ no se declara listo para el concurso hasta superar el gate tecnico de 15.7 y C.18.
Pendientes diferidos expresamente:
- Capacidades P1/P2 excluidas por PT-006; deben conservar estado DIFERIDO o NO_APLICA justificado.
- Toda implementacion y evidencia del checklist tecnico.
Primera pieza autorizada:
- Preparar la ficha de Pieza 1: contratos, esquemas, estados, eventos, entradas, salidas y validadores.
- Esta autorizacion no permite construir codigo ni entregar el encargo a Antigravity hasta aprobar su ficha.
Fecha: 28 de agosto de 2026
Aprobado por: usuario humano (A0 actual del proyecto)
Referencia de aprobacion: confirmacion expresa "si" en la conversacion de decisiones del 28 de agosto de 2026.
```

### 15.7 Gate tecnico antes de presentar a competencia

Este segundo gate no bloquea la aprobacion documental del contrato, pero si bloquea afirmar que la v0 esta lista para presentarse. Cada marca exige evidencia vinculada; no se acepta una declaracion verbal como sustituto.

- [ ] Problema, objetivo y alcance estan cerrados.
- [ ] Runtime y arquitectura de agentes estan demostrados de extremo a extremo.
- [ ] Estado por mision, aislamiento, checkpoint y reanudacion fueron probados.
- [ ] Memoria entre misiones tiene politica y pruebas de escritura, recuperacion, correccion y eliminacion.
- [ ] Entradas de archivos, enlaces e imagenes aplicables tienen limites, validacion y manejo seguro.
- [ ] Al menos una fuente real autorizada fue consultada, atribuida y validada.
- [ ] La secuencia multiagente, los contratos y la consolidacion central fueron demostrados.
- [ ] Una interrupcion real puede pausarse y reanudarse sin duplicar acciones.
- [ ] Las puertas de aprobacion humana, rechazo y excepcion funcionan y quedan auditadas.
- [ ] Existe una suite de evaluacion reproducible con metrica determinista, umbral y trayectoria.
- [ ] El dataset de evaluacion esta versionado y separa holdout, casos negativos y desarrollo.
- [ ] Las optimizaciones, si existen, se comparan con baseline y no modifican produccion sin autorizacion.
- [ ] Existen controles contra reward hacking, fuga de evaluacion y metricas sustitutas.
- [ ] Frontend y backend real estan integrados con logs, fallos visibles, privacidad y limites de costo.
- [ ] La demo final, arquitectura, pruebas, metricas, limitaciones y diferenciador estan empaquetados para presentacion.
- [ ] La ejecucion usa Gemini 3.5 o posterior, Google ADK y al menos el despliegue aprobado en Google Cloud.
- [ ] El video muestra prueba visible del backend en Google Cloud y no supera cuatro minutos.
- [ ] El repositorio publico incluye README reproducible, arquitectura, pruebas y expediente saneado, sin secretos.
- [ ] La demo conserva separacion entre OminAI HQ y Business OS y presenta contenido clave en `ES / EN`.

## Anexo A. Fuentes locales revisadas

### A.1 Fuentes normativas y operativas

- `C:\Users\Nivez\Desktop\08_Ominai\OminAIHQ\AGENTS.md`
- `C:\Users\Nivez\Desktop\08_Ominai\OminAIHQ\TEAM-WORKFLOW.md`
- `C:\Users\Nivez\.codex\attachments\ec85c4ee-1b2f-4f45-8914-b99c10ac2aad\pasted-text.txt`
- `C:\Users\Nivez\.codex\attachments\fdeaf8bc-b68b-4c32-a227-f9a9938831af\pasted-text.txt` (checklist tecnico de clases incorporado como pendiente de evidencia)

### A.2 Material educativo de REQUISITOS

Se revisaron los siguientes archivos como material educativo, no como decisiones de producto:

- `a5aaf8a8-fe07-4a6a-8f9a-fc29a5baa691_11_de_agosto_de_2026_2308.pdf`
- `engineer_ai_agents_adk_es.es.pdf`
- `f8fda720-0ba5-4713-9b93-73f51d0d1a3a_13_de_agosto_de_2026_2309.pdf`
- `Hi everyone. Uh thank you for joini.txt`
- `T-DEVAGENT-I-m1-l1-es-file-1.es.pdf`
- `T-DEVAGENT-I-m2-l0-es-file-2.es.pdf`
- `T-DEVAGENT-I-m2-l1-es-file-3.es.pdf`
- `T-DEVAGENT-I-m3-l0-es-file-4.es.pdf`
- `T-DEVAGENT-I-m4-l0-es-file-5.es.pdf`
- `T-DEVAGENT-I-m4-l0-es-file-6.es.pdf`
- `T-DEVAGENTDEPLOY-A-m1-l0-es-file-1.es.pdf`
- `T-DEVAGENTDEPLOY-A-m1-l1-es-file-2.es.pdf`
- `T-DEVAGENTDEPLOY-A-m2-l0-es-file-3.es.pdf`
- `T-DEVAGENTDEPLOY-A-m2-l1-es-file-4.es.pdf`
- `T-DEVAGENTDEPLOY-A-m3-l0-es-file-5.es.pdf`
- `T-DEVAGENTDEPLOY-A-m3-l1-es-file-6.es.pdf`
- `T-DEVAGENTDEPLOY-A-m4-l0-es-file-7.es.pdf`
- `T-DEVAGENTDEPLOY-A-m4-l1-es-file-8.es.pdf`
- `T-DEVAGENTDEPLOY-A-m5-l0-es-file-9.es.pdf`
- `T-DEVAGENTMEM-B-m1-l0-es-file-1.es.pdf`
- `T-DEVAGENTMEM-B-m1-l1-es-file-2.es.pdf`
- `T-DEVAGENTMEM-B-m2-l0-es-file-3.es.pdf`
- `T-DEVAGENTMEM-B-m2-l1-es-file-4.es.pdf`
- `T-DEVAGENTMEM-B-m3-l0-es-file-5.es.pdf`
- `T-DEVAGENTMEM-B-m3-l1-es-file-6.es.pdf`
- `T-DEVAGENTMEM-B-m4-l0-es-file-7.es.pdf`
- `T-DEVAGENTOPT-I-m1-l0-es-file-1.es.pdf`
- `T-DEVAGENTOPT-I-m1-l1-es-file-2.es.pdf`
- `T-DEVAGENTOPT-I-m2-l0-es-file-3.es.pdf`
- `T-DEVAGENTOPT-I-m2-l1-es-file-4.es.pdf`
- `T-DEVAGENTOPT-I-m3-l0-es-file-5.es.pdf`
- `T-DEVAGENTOPT-I-m3-l0-es-file-7.es.pdf`
- `T-DEVAGENTOPT-I-m3-l1-es-file-6.es.pdf`
- `T-DEVAGENTOPT-I-m3-l1-es-file-8.es.pdf`
- `T-DEVAGENTOPT-I-m4-l0-es-file-9.es.pdf`
- `T-DEVAGENTTOOL-B-m1-l0-es-file-1.es.pdf`
- `T-DEVAGENTTOOL-B-m1-l1-es-file-2.es.pdf`
- `T-DEVAGENTTOOL-B-m2-l0-es-file-3.es.pdf`
- `T-DEVAGENTTOOL-B-m2-l1-es-file-4.es.pdf`
- `T-DEVAGENTTOOL-B-m3-l0-es-file-5.es.pdf`
- `T-DEVAGENTTOOL-B-m3-l1-es-file-6.es.pdf`
- `T-DEVAGENTTOOL-B-m4-l0-es-file-7.es.pdf`
- `T-DEVAGENTTOOL-B-m4-l1-es-file-8.es.pdf`
- `T-DEVAGENTTOOL-B-m5-l0-es-file-9.es.pdf`
- `T-DEVAGENTTOOL-B-m5-l1-es-file-10.es.pdf`
- `T-DEVAGENTTOOL-B-m6-l0-es-file-11.es.pdf`

### A.3 Contraejemplos rechazados

- Leido solo como contraejemplo: `C:\Users\Nivez\Downloads\Requisitos y Diseño Funcional del MVP de OminAI HQ (1).md`.
- No encontrado durante esta revision: `C:\Users\Nivez\Downloads\Requisitos y Diseño Funcional del MVP de OminAI HQ.md`.

Del documento rechazado no se heredaron: tecnologias obligatorias, supuestas fuentes como "Source 1" o "Pillar 1", ejemplos y metricas del curso, almacenamiento de Chain-of-Thought, auto-correccion sin limites, ni afirmaciones de produccion.

### A.4 Fuentes oficiales del concurso verificadas el 28 de agosto de 2026

- `https://allthingsagentichackathon.devpost.com/`
- `https://allthingsagentichackathon.devpost.com/rules`
- `https://allthingsagentichackathon.devpost.com/details/faqs`

Estas fuentes respaldan la categoria Collaborative Partner, los componentes obligatorios, la prueba de despliegue en Google Cloud, el video de hasta cuatro minutos, el repositorio/diagrama y la fecha oficial. Si las reglas cambian, prevalece la version oficial vigente y el contrato debe revisarse.

## Anexo B. Validacion documental previa a la aprobacion

- El contrato describe producto, comportamiento, estados y evidencia; no una plataforma tecnologica.
- El VBP incluye todo el contenido minimo exigido y reglas de integridad.
- RF-001 a RF-030 tienen criterio de aceptacion verificable.
- Los RNF mantienen neutralidad en el nucleo funcional y documentan la excepcion tecnologica exigida/aprobada para el concurso.
- Reintentos, ciclos, profundidad, amplitud, tiempo y gasto son finitos; PT-001 fija un techo de USD 25.
- Correos, pagos, compras, publicaciones, eliminaciones y ejecucion/despliegue de la iniciativa descrita por el VBP quedan fuera del MVP. El despliegue controlado de OminAI HQ para el concurso es una excepcion aprobada y no ejecuta la iniciativa cliente.
- El usuario humano conserva aprobacion exclusiva del plan propuesto, del VBP y del cierre; Niko permanece identificada solo como la A0 actual del proyecto.
- No se copiaron dominios, personajes ni metricas de los ejemplos educativos.
- No se almacena ni expone Chain-of-Thought.
- Toda referencia citada corresponde a un archivo real revisado; el archivo rechazado ausente se declara como tal.
- Las decisiones DN-001 a DN-012 y DT-013 estan registradas como aprobadas; PT-001 a PT-008 estan resueltos y conservan su evidencia pendiente.
- Los 174 controles tecnicos de clases (78 P0, 87 P1 y 9 P2) y el gate minimo de 15 puntos se incorporan como **PENDIENTES DE EVIDENCIA**.
- Ningun control del Anexo C se considera cumplido por aparecer en el contrato: necesita evidencia enlazada o una declaracion N/A justificada y aprobada por el usuario humano.

## Anexo C. Checklist tecnico de clases - PENDIENTE DE EVIDENCIA

### C.0 Como interpretar y cerrar los controles

- **P0 - Esencial:** debe implementarse y demostrarse en la v0 cuando sea aplicable; de lo contrario se marca N/A con justificacion y aprobacion humana.
- **P1 - Alto valor:** se selecciona la mayoria pertinente que fortalezca el caso sin comprometer la fecha ni la estabilidad.
- **P2 - Diferenciador:** solo se incorpora despues de estabilizar el recorrido principal.
- **Evidencia:** una pantalla, evento, prueba, metrica o recorrido reproducible vinculado a la version evaluada.
- **Estado inicial:** todos los elementos siguientes estan desmarcados y en `PENDIENTE DE EVIDENCIA`.

Este anexo traduce lo ensenado en las clases a controles del proyecto. No declara que todos sean requisitos oficiales del concurso ni obliga a utilizar los proveedores citados como ejemplo; se admite un equivalente justificado.

### C.1 Problema, objetivo y alcance

- [ ] **P0** El proyecto identifica un problema real, especifico y comprensible.
- [ ] **P0** Esta definido quien es el usuario principal y que resultado necesita.
- [ ] **P0** Existe un criterio objetivo para determinar si el agente cumplio la tarea.
- [ ] **P0** Se especifica que puede hacer el agente y que queda fuera de su alcance.
- [ ] **P0** Se distingue claramente entre funciones implementadas, simuladas y propuestas.
- [ ] **P1** El caso demuestra por que un agente aporta mas valor que un formulario o chatbot tradicional.
- [ ] **P1** Se describen restricciones reales: tiempo, presupuesto, permisos, disponibilidad, politicas y preferencias.
- [ ] **P1** Se identifican los principales casos limite y situaciones de fallo.

### C.2 Arquitectura basica del agente

- [ ] **P0** Existe un agente raiz con instrucciones claras y un objetivo delimitado.
- [ ] **P0** Las herramientas disponibles estan definidas y limitadas segun la responsabilidad del agente.
- [ ] **P0** Las acciones deterministas se realizan mediante codigo o herramientas, no se dejan a la improvisacion del modelo.
- [ ] **P0** El modelo se utiliza para tareas que requieren interpretacion, razonamiento o lenguaje natural.
- [ ] **P0** El agente registra que herramientas utilizo y en que secuencia.
- [ ] **P1** La arquitectura separa modelo, herramientas, sesiones, memoria y artefactos.
- [ ] **P1** Existe un `Runner` o servicio equivalente que permita utilizar el agente fuera de ADK Web.
- [ ] **P1** El agente puede ejecutarse desde un backend o API propia.
- [ ] **P1** Las entradas y salidas importantes utilizan esquemas definidos.
- [ ] **P2** Existen interceptores o callbacks para aplicar validaciones antes y despues de llamadas sensibles.

### C.3 Estado y sesiones

- [ ] **P0** Los datos necesarios para ejecutar acciones se guardan como estado estructurado.
- [ ] **P0** Identificadores, decisiones, montos, estados de procesos y permisos no dependen unicamente del texto del chat.
- [ ] **P0** Las sesiones se almacenan de forma persistente.
- [ ] **P0** Una conversacion puede recuperarse despues de reiniciar el servidor.
- [ ] **P0** El sistema distingue entre historial conversacional, estado operativo y memoria de largo plazo.
- [ ] **P1** El estado tiene alcance definido por usuario, sesion o aplicacion.
- [ ] **P1** Se evita compartir accidentalmente el estado entre usuarios.
- [ ] **P1** Existe una estrategia para reanudar procesos despues de fallos.
- [ ] **P1** El sistema puede continuar desde el ultimo punto valido sin repetir todas las operaciones anteriores.

### C.4 Memoria de largo plazo

- [ ] **P0** Esta definido cuando una conversacion o resultado se convierte en memoria.
- [ ] **P0** Esta definida la consulta o politica mediante la cual se recupera esa memoria.
- [ ] **P0** El agente puede reconocer informacion relevante de interacciones anteriores.
- [ ] **P0** La memoria esta separada por aplicacion y usuario.
- [ ] **P1** La memoria sobrevive al reinicio del proceso.
- [ ] **P1** Existe un servicio persistente, como Vertex AI Memory Bank o un equivalente justificado.
- [ ] **P1** Se distingue entre guardar la conversacion completa y guardar hechos consolidados.
- [ ] **P1** El usuario puede saber que informacion relevante se conservo.
- [ ] **P1** Existe una politica para corregir o eliminar recuerdos.
- [ ] **P2** La recuperacion es semantica y no depende exclusivamente de coincidencias de palabras.

### C.5 Archivos, imagenes y evidencia multimodal

- [ ] **P0** El agente puede procesar los archivos que sean necesarios para el caso de uso.
- [ ] **P0** La informacion extraida de un archivo se guarda como datos estructurados.
- [ ] **P0** El archivo original se conserva como artefacto cuando constituye evidencia.
- [ ] **P0** Los hechos extraidos mantienen una referencia al artefacto original.
- [ ] **P1** Los artefactos tienen usuario, alcance y versiones.
- [ ] **P1** El sistema evita afirmar que conservo un archivo cuando unicamente interpreto el mensaje.
- [ ] **P1** Se controla que formatos, tamanos y tipos de archivo pueden recibirse.
- [ ] **P1** Los datos sensibles de los archivos reciben controles de acceso apropiados.

### C.6 Integracion con datos reales

- [ ] **P0** El agente se conecta con una fuente de informacion real o representativa del proyecto.
- [ ] **P0** Las consultas criticas utilizan herramientas gobernadas y parametrizadas.
- [ ] **P0** El modelo proporciona parametros; no genera libremente consultas sensibles contra toda la base de datos.
- [ ] **P0** Las respuestas importantes incluyen una ruta de evidencia o explicacion verificable.
- [ ] **P1** El proyecto diferencia una coincidencia textual de una relacion real entre registros.
- [ ] **P1** Existe un recorrido determinista para preguntas relacionadas con usuarios, empresas, procesos o decisiones.
- [ ] **P1** La busqueda semantica utiliza embeddings cuando el significado es mas importante que las palabras exactas.
- [ ] **P1** Los datos estructurados, embeddings y resultados permanecen cerca de la fuente empresarial cuando sea posible.
- [ ] **P2** Se utiliza BigQuery, una base vectorial o una arquitectura equivalente con una justificacion clara.

### C.7 Workflows y colaboracion entre agentes

- [ ] **P0** El proceso principal esta representado como una secuencia comprensible de pasos.
- [ ] **P0** Las decisiones deterministas estan codificadas mediante condiciones, rutas o grafos.
- [ ] **P0** El agente no decide libremente el orden de un proceso que debe cumplir una secuencia obligatoria.
- [ ] **P1** Se utilizan pasos secuenciales cuando existe dependencia entre resultados.
- [ ] **P1** Se utilizan tareas paralelas solamente cuando son independientes.
- [ ] **P1** Las ramas tienen condiciones explicitas de entrada y salida.
- [ ] **P1** Los resultados paralelos se reunen antes de producir la respuesta final.
- [ ] **P1** Cada subagente tiene una responsabilidad limitada.
- [ ] **P1** El agente raiz conserva el control cuando un subagente se utiliza como herramienta.
- [ ] **P1** Se evita enviar a cada subagente informacion que no necesita.
- [ ] **P1** La division de responsabilidades reduce contexto, costo y alucinaciones.
- [ ] **P2** Existen workflows dinamicos cuando el numero de tareas depende de la solicitud.
- [ ] **P2** Las rutas entre agentes y herramientas se pueden inspeccionar como un grafo.

### C.8 Procesos de larga duracion y autonomia

- [ ] **P0** Un proceso largo puede pausarse y reanudarse.
- [ ] **P0** El sistema conserva el punto exacto de continuacion.
- [ ] **P0** Reanudar no repite operaciones costosas o irreversibles.
- [ ] **P0** Antes de ejecutar una accion final se actualizan los datos que pueden haber cambiado.
- [ ] **P1** Existen callbacks para consultar informacion fresca antes de confirmar una operacion.
- [ ] **P1** El sistema soporta eventos externos, tareas programadas o mensajes de otros servicios.
- [ ] **P1** Los procesos autonomos tienen limites de tiempo, costo, numero de pasos y reintentos.
- [ ] **P1** Los errores transitorios tienen reintentos controlados.
- [ ] **P1** Los errores definitivos producen un estado claro y recuperable.
- [ ] **P2** Se utilizan Cloud Scheduler, Pub/Sub u otros mecanismos event-driven cuando el caso realmente lo necesita.

### C.9 Supervision humana y autorizacion

- [ ] **P0** Las acciones sensibles requieren aprobacion humana.
- [ ] **P0** La solicitud queda realmente pausada; un campo de texto que diga `pending` no se considera aprobacion.
- [ ] **P0** El supervisor recibe el contexto necesario antes de decidir.
- [ ] **P0** La decision conserva responsable, fecha, resultado y observaciones.
- [ ] **P0** Una aprobacion solo puede responderse una vez.
- [ ] **P0** El agente no puede ejecutar una accion fuera de los permisos del usuario.
- [ ] **P1** Existe una interfaz especifica para revisar, aprobar o rechazar acciones.
- [ ] **P1** Las decisiones humanas quedan registradas para auditoria.
- [ ] **P1** Se diferencian claramente aprobacion, rechazo, cancelacion y expiracion.
- [ ] **P1** El sistema solicita confirmacion final para compras, pagos, publicaciones o cambios irreversibles.

### C.10 Evaluacion del agente

- [ ] **P0** Existe un conjunto de casos de evaluacion reproducibles.
- [ ] **P0** Cada caso contiene entrada, condiciones y resultado esperado.
- [ ] **P0** El proyecto evalua el resultado final y tambien la trayectoria de herramientas.
- [ ] **P0** Se verifica que el agente llego a la respuesta mediante el proceso autorizado.
- [ ] **P0** Existe al menos una metrica determinista conectada con el objetivo real del producto.
- [ ] **P0** Esta definido un umbral explicito de aprobacion.
- [ ] **P0** Se documentan los casos exitosos y fallidos.
- [ ] **P1** Se utilizan respuestas de referencia o conjuntos `golden`.
- [ ] **P1** Se incorporan metricas de coincidencia, juez LLM y trayectoria cuando correspondan.
- [ ] **P1** Los casos explican por que fallo el agente, no solamente que fallo.
- [ ] **P1** Se incluyen restricciones, conflictos y casos limite.
- [ ] **P1** Los resultados de evaluacion pueden ejecutarse nuevamente despues de cada cambio.
- [ ] **P1** Se conservan evidencias de las metricas antes y despues de mejorar el agente.

### C.11 Datos de entrenamiento y validacion

- [ ] **P0** Los casos utilizados para mejorar instrucciones estan separados de los casos de validacion final.
- [ ] **P0** Existe un conjunto de prueba o `holdout` que el optimizador no haya visto.
- [ ] **P0** El agente no se aprueba unicamente porque funciona con ejemplos conocidos.
- [ ] **P1** Los casos cubren distintas personas, restricciones y combinaciones de condiciones.
- [ ] **P1** Se incluyen ejemplos negativos y situaciones donde el agente debe detenerse.
- [ ] **P1** Los casos nuevos detectados en produccion se agregan al conjunto de evaluacion.
- [ ] **P1** Cada version del conjunto de evaluacion puede identificarse y reproducirse.

### C.12 Optimizacion y agente autoevolutivo

- [ ] **P1** Existe una linea base evaluada antes de optimizar.
- [ ] **P1** La optimizacion utiliza los fallos y sus causas para proponer mejores instrucciones.
- [ ] **P1** La instruccion mejorada se vuelve a evaluar automaticamente.
- [ ] **P1** El ciclo contiene un agente o componente que ejecuta, otro que evalua y un enrutador determinista.
- [ ] **P1** El enrutador decide entre aprobar, volver a mejorar o detener.
- [ ] **P1** Existen criterios de salida medibles.
- [ ] **P1** Existe un numero maximo de iteraciones.
- [ ] **P1** Existe un presupuesto maximo de tokens, tiempo y costo.
- [ ] **P1** La mejor version se publica solamente despues de superar validacion.
- [ ] **P1** Las instrucciones y resultados estan versionados.
- [ ] **P1** Una persona puede revisar o revertir la version publicada.
- [ ] **P2** Se utiliza ADK Optimize o un mecanismo equivalente para proponer instrucciones.
- [ ] **P2** El workflow completo ejecuta el ciclo: agente -> juez -> enrutador -> propuesta -> validacion -> publicacion.

### C.13 Prevencion de reward hacking

- [ ] **P0** La metrica representa el resultado real que importa al usuario.
- [ ] **P0** El proyecto no optimiza unicamente similitud textual o una puntuacion facil de manipular.
- [ ] **P0** Una respuesta correcta por casualidad no se considera ejecucion correcta.
- [ ] **P0** Se verifica que se hayan respetado todas las restricciones.
- [ ] **P1** Se combinan metricas de resultado, trayectoria, seguridad y satisfaccion de condiciones.
- [ ] **P1** Los casos `holdout` detectan sobreajuste a los ejemplos de optimizacion.
- [ ] **P1** Se revisan resultados con puntuacion alta pero comportamiento incorrecto.
- [ ] **P1** Cambiar el juez, la metrica o los datos requiere volver a validar todo el agente.

### C.14 Produccion, monitoreo y mejora continua

- [ ] **P0** La interfaz final no expone ADK Web al usuario.
- [ ] **P0** Existe un frontend o canal de uso conectado a un backend controlado.
- [ ] **P0** Se registran ejecuciones, herramientas, errores, tiempos y decisiones.
- [ ] **P0** Se puede reconstruir por que el agente produjo una respuesta.
- [ ] **P1** Se habilitan trazas para detectar fallos en produccion.
- [ ] **P1** Los fallos se almacenan en una fuente analitica, como BigQuery.
- [ ] **P1** Existe un proceso para convertir fallos reales en nuevos casos de evaluacion.
- [ ] **P1** Las nuevas versiones se prueban antes de reemplazar la version anterior.
- [ ] **P1** Existe monitoreo de latencia, consumo de tokens, costo y tasa de exito.
- [ ] **P1** Existe una ruta de reversion si una mejora reduce la calidad.
- [ ] **P1** Los cambios automaticos no llegan a produccion sin los controles definidos.
- [ ] **P2** El proyecto implementa un ciclo continuo: observar -> recolectar -> evaluar -> mejorar -> validar -> publicar.

### C.15 Seguridad, privacidad y gobernanza

- [ ] **P0** Cada herramienta aplica permisos minimos.
- [ ] **P0** Las acciones estan limitadas por identidad, rol y alcance.
- [ ] **P0** Los datos de un usuario no aparecen en la sesion o memoria de otro.
- [ ] **P0** Los secretos y credenciales no se incorporan a prompts ni repositorios.
- [ ] **P0** Las acciones irreversibles requieren confirmacion y registro.
- [ ] **P0** Se identifica que informacion se guarda, donde y durante cuanto tiempo.
- [ ] **P1** Existe una politica para eliminar sesiones, memorias y artefactos.
- [ ] **P1** Las consultas a datos empresariales estan parametrizadas.
- [ ] **P1** Las respuestas sensibles incluyen evidencia o una advertencia de incertidumbre.
- [ ] **P1** El proyecto documenta riesgos, mitigaciones y limitaciones conocidas.

### C.16 Experiencia de usuario

- [ ] **P0** El usuario entiende que esta haciendo el agente.
- [ ] **P0** El sistema muestra cuando una operacion esta pendiente.
- [ ] **P0** Se diferencia claramente entre recomendacion, accion ejecutada y accion aprobada.
- [ ] **P0** Los errores ofrecen una forma segura de reintentar o continuar.
- [ ] **P0** El usuario no necesita conocer la arquitectura interna para completar su tarea.
- [ ] **P1** Las respuestas incluyen evidencia util sin abrumar al usuario.
- [ ] **P1** La interfaz muestra estados de espera, aprobacion, finalizacion y fallo.
- [ ] **P1** El supervisor dispone de una vista diferente de la del usuario final.
- [ ] **P1** Los archivos y resultados importantes se pueden recuperar posteriormente.

### C.17 Evidencias para la presentacion del concurso

- [ ] **P0** Demostracion funcional de principio a fin.
- [ ] **P0** Comparacion visible entre comportamiento defectuoso y comportamiento corregido.
- [ ] **P0** Diagrama sencillo de arquitectura.
- [ ] **P0** Explicacion de modelo, herramientas, estado, sesiones, memoria y datos.
- [ ] **P0** Caso donde el sistema utiliza memoria de una conversacion anterior.
- [ ] **P0** Caso donde una accion queda esperando aprobacion humana.
- [ ] **P0** Caso donde una respuesta muestra su ruta de evidencia.
- [ ] **P0** Resultados de evaluaciones con cifras verificables.
- [ ] **P0** Lista honesta de funciones actuales, simulaciones y trabajo futuro.
- [ ] **P1** Evidencia de recuperacion despues de reiniciar o interrumpir el proceso.
- [ ] **P1** Evidencia de procesamiento de un archivo o entrada multimodal.
- [ ] **P1** Evidencia de busqueda semantica o integracion empresarial.
- [ ] **P1** Metricas antes y despues de optimizar instrucciones.
- [ ] **P1** Caso limite descubierto y forma en que el sistema aprendio de el.
- [ ] **P1** Explicacion de privacidad, costos y controles humanos.

### C.18 Gate minimo antes de presentar

OminAI HQ no se declara listo para el concurso hasta poder marcar estas condiciones con evidencia:

- [ ] El caso de uso y el criterio de exito estan definidos.
- [ ] Existe un flujo completo funcional.
- [ ] Los datos operativos viven en estado estructurado.
- [ ] Las sesiones sobreviven a un reinicio.
- [ ] La memoria entre conversaciones tiene politica de escritura y recuperacion.
- [ ] Las acciones sensibles requieren aprobacion humana real.
- [ ] Las consultas criticas utilizan herramientas gobernadas.
- [ ] Existe un conjunto reproducible de evaluaciones.
- [ ] Se evaluan resultado y trayectoria.
- [ ] Existe un conjunto `holdout`.
- [ ] Los loops automaticos tienen limites y criterios de salida.
- [ ] Los fallos producen trazas y pueden convertirse en nuevos casos de evaluacion.
- [ ] La interfaz final funciona fuera de ADK Web.
- [ ] La demostracion distingue implementacion, simulacion y propuesta.
- [ ] Cada afirmacion importante tiene evidencia verificable.

### C.19 Lectura estrategica aprobada

1. Implementar completamente los P0 aplicables al caso de uso o justificar formalmente por que un control es N/A.
2. Seleccionar la mayoria pertinente de P1 que demuestre profundidad tecnica y pueda probarse antes de la presentacion.
3. Anadir P2 solo si no comprometen la estabilidad ni la fecha objetivo.
4. No presentar prototipos visuales o planes futuros como capacidades operativas.
5. Demostrar cada capacidad seleccionada con una prueba reproducible.
