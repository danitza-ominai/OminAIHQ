# Mapa de piezas restantes - OminAI HQ v0

**Estado:** 29 FICHAS APROBADAS PARA ANTIGRAVITY; EJECUCION SECUENCIAL CONDICIONADA  
**Fecha:** 30 de agosto de 2026  
**Contrato de referencia:** [CONTRATO-MVP-v1.md](CONTRATO-MVP-v1.md), 1.2-aprobada

## Que se entrega

29 fichas nuevas, cada una con objetivo, fuentes, dependencias, archivos cerrados, comportamiento, criterios, pruebas, limites, detenciones, prompt para Antigravity y aprobacion humana de construccion registrada; la aceptacion final sigue pendiente.
Cubren lo restante de los bloques 3 a 15; no son 29 bloques adicionales al contrato.
Se prepararon documentos, no funcionalidades. Ningun modelo, servidor, base de datos, nube o publicacion se ejecuto por crear estas fichas.

- [Reglas comunes, decisiones tecnicas y limites](PIEZAS-PENDIENTES/00-REGLAS-Y-DECISIONES.md).
- [Matriz completa: RF, RNF, CT y 174 controles](PIEZAS-PENDIENTES/01-MATRIZ-DE-COBERTURA.md).
- [Siguiente ficha aprobada, con condiciones previas: PZ-003C](PIEZAS-PENDIENTES/FICHA-PZ-003C.md).

## Donde estamos

| Pieza | Estado sustentado |
|---|---|
| PZ-001A | COMPLETADA_Y_ACEPTADA segun ficha vigente |
| PZ-002A | COMPLETADA_Y_ACEPTADA segun ficha vigente |
| PZ-003A | COMPLETADA_Y_ACEPTADA segun ficha vigente |
| PZ-003B | COMPLETADA_Y_ACEPTADA por el usuario humano el 30 de agosto de 2026; correccion 1 y dictamen Copilot previos; recorrido manual pendiente, CT-009 no cerrado |
| PZ-003C a PZ-015B de este mapa | APROBADA_PARA_CONSTRUIR por Antigravity; verificar condiciones previas; no implementadas por esta entrega |

PZ-003B sigue siendo un ensayo SIMULADA en memoria. Ni su aprobacion ni este mapa significan que exista ya un VBP real, persistencia, interfaz o despliegue.
Aprobacion posterior del usuario humano, 30 de agosto de 2026: "todas las fichas quedan aprobadas y lo hare con el antigravity mas a eso me referia".
Quedan aprobadas las 29 fichas version 1 de este mapa, cada una con su alcance y lista cerrada. No cambia el constructor. Esa autorizacion conjunta no aceptaba PZ-003B ni resultados futuros, ni concedia permisos sensibles pendientes.
Decision posterior del mismo dia: "registra la aprobacion de la pieza faltante". La aceptacion final de PZ-003B queda registrada en la [seccion 15 de su ficha](FICHA-PZ-003B-DECISION-HUMANA-DEL-PLAN.md#15-aceptacion-final-humana-de-pz-003b), manteniendo el recorrido manual como pendiente.

## Orden de construccion y dependencias

Las dependencias son de aceptacion, no solo de presencia de archivos. La lista esta ordenada sin ciclos.
Las letras dividen un bloque grande en entregas inspeccionables; se conservan los numeros de bloque del contrato.

| Orden | Ficha | Resultado acotado | Dependencia inmediata |
|---:|---|---|---|
| 1 | [PZ-003C](PIEZAS-PENDIENTES/FICHA-PZ-003C.md) | Contratos del recorrido, tareas y resultados | PZ-003B |
| 2 | [PZ-003D](PIEZAS-PENDIENTES/FICHA-PZ-003D.md) | Motor secuencial de tareas SIMULADA | PZ-003C |
| 3 | [PZ-003E](PIEZAS-PENDIENTES/FICHA-PZ-003E.md) | VBP canonico y validacion determinista SIMULADA | PZ-003D |
| 4 | [PZ-003F](PIEZAS-PENDIENTES/FICHA-PZ-003F.md) | Recorrido completo Mision a VBP SIMULADA | PZ-003E |
| 5 | [PZ-004A](PIEZAS-PENDIENTES/FICHA-PZ-004A.md) | Adaptador ADK y control de llamadas reales | PZ-003F |
| 6 | [PZ-004B](PIEZAS-PENDIENTES/FICHA-PZ-004B.md) | Chief of Staff y composicion del runtime | PZ-004A |
| 7 | [PZ-005A](PIEZAS-PENDIENTES/FICHA-PZ-005A.md) | Research y consulta gobernada de fuentes | PZ-004B |
| 8 | [PZ-006A](PIEZAS-PENDIENTES/FICHA-PZ-006A.md) | Product Architect trazable | PZ-005A |
| 9 | [PZ-007A](PIEZAS-PENDIENTES/FICHA-PZ-007A.md) | Delivery Planner y dependencias verificables | PZ-006A |
| 10 | [PZ-008A](PIEZAS-PENDIENTES/FICHA-PZ-008A.md) | Governance independiente y cinco agentes integrados | PZ-007A |
| 11 | [PZ-009A](PIEZAS-PENDIENTES/FICHA-PZ-009A.md) | Registro de evidencia y validacion de procedencia | PZ-008A |
| 12 | [PZ-009B](PIEZAS-PENDIENTES/FICHA-PZ-009B.md) | Archivos de texto, PDF y DOCX con originales privados | PZ-009A |
| 13 | [PZ-009C](PIEZAS-PENDIENTES/FICHA-PZ-009C.md) | Imagenes y expediente saneado de competencia | PZ-009B |
| 14 | [PZ-009D](PIEZAS-PENDIENTES/FICHA-PZ-009D.md) | Auditoria consultable y trazas minimizadas | PZ-009C |
| 15 | [PZ-010A](PIEZAS-PENDIENTES/FICHA-PZ-010A.md) | Persistencia local y perfil humano unico | PZ-009D |
| 16 | [PZ-010B](PIEZAS-PENDIENTES/FICHA-PZ-010B.md) | Recuperacion sin duplicar ejecuciones | PZ-010A |
| 17 | [PZ-010C](PIEZAS-PENDIENTES/FICHA-PZ-010C.md) | Memoria aprobada entre misiones | PZ-010B |
| 18 | [PZ-010D](PIEZAS-PENDIENTES/FICHA-PZ-010D.md) | Archivo, eliminacion y ciclo de datos | PZ-010C |
| 19 | [PZ-011A](PIEZAS-PENDIENTES/FICHA-PZ-011A.md) | Suite versionada y separacion del holdout | PZ-010D |
| 20 | [PZ-011B](PIEZAS-PENDIENTES/FICHA-PZ-011B.md) | Evaluacion adversarial y control de mejoras | PZ-011A |
| 21 | [PZ-012A](PIEZAS-PENDIENTES/FICHA-PZ-012A.md) | Aprobaciones humanas integradas y durables | PZ-011B |
| 22 | [PZ-012B](PIEZAS-PENDIENTES/FICHA-PZ-012B.md) | Pausa, cancelacion y cambios de alcance | PZ-012A |
| 23 | [PZ-013A](PIEZAS-PENDIENTES/FICHA-PZ-013A.md) | Backend local controlado | PZ-012B |
| 24 | [PZ-013B](PIEZAS-PENDIENTES/FICHA-PZ-013B.md) | Interfaz de mision, trabajo y decisiones | PZ-013A |
| 25 | [PZ-013C](PIEZAS-PENDIENTES/FICHA-PZ-013C.md) | VBP visible, descarga fiel y demo ES/EN | PZ-013B |
| 26 | [PZ-014A](PIEZAS-PENDIENTES/FICHA-PZ-014A.md) | Preparacion de despliegue y datos saneados | PZ-013C |
| 27 | [PZ-014B](PIEZAS-PENDIENTES/FICHA-PZ-014B.md) | Despliegue controlado y verificacion de nube | PZ-014A |
| 28 | [PZ-015A](PIEZAS-PENDIENTES/FICHA-PZ-015A.md) | Pruebas integrales y gate del MVP | PZ-014B |
| 29 | [PZ-015B](PIEZAS-PENDIENTES/FICHA-PZ-015B.md) | Paquete de competencia y entrega humana | PZ-015A |

## Cobertura y seleccion

| Cobertura | Ruta documental | Implementacion |
|---|---|---|
| RF-001 a RF-030 | 30 con responsables | No se declara completada por este mapa |
| RNF-001 a RNF-015 | 15 con responsables | Pendiente de evidencia aplicable |
| CT-001 a CT-017 | 17 areas asignadas | Pendiente de evidencia aplicable |
| Checklist P0 | 78 con ruta de evidencia | Todos pendientes de cierre verificable |
| Checklist P1 | 71 seleccionados de 87 (81.6 %); 15 diferidos y 1 N/A propuesto | Alcance de fichas aprobado, no 71 implementados |
| Checklist P2 | 9 diferidos | No desplazan P0/P1 |
| Gate | 15 condiciones C.18 + 4 adicionales de 15.7 | Pendiente de evidencia y decision humana |

No se rebaja persistencia, memoria o recuperacion a "fuera del MVP". La politica aprobada de P1 permite diferir vectorial, paralelismo, eventos y autooptimizacion.
La fila N/A es una propuesta a ratificar: confirmaciones de pagos/compras/publicaciones que la v0 no ejecuta. Su denegacion sigue probandose.

## Como usar cada ficha

1. Resolver/aceptar la dependencia y leer el apartado 3 de la nueva ficha.
2. Verificar interfaces contra lo realmente aceptado y completar decisiones tecnicas pendientes. Las rutas listadas ya estan aprobadas; las APIs/versiones futuras no se inventan.
3. Usar la aprobacion registrada en el apartado 11: no pedir de nuevo permiso para la misma ficha/lista. Cambios de alcance y permisos de instalaciones, datos, coste o acciones externas requieren autorizacion especifica.
4. Copiar el prompt del apartado 10 de esa ficha en Antigravity.
5. Recibir archivos y evidencia. Chipi revisa sin editar; si hay defectos, prepara una correccion cerrada para autorizacion humana.
6. Copilot revisa independientemente y el usuario acepta/rechaza. Solo entonces pasar a la siguiente.
7. No ejecutar las 29 fichas en una sola conversacion ni permitir edicion simultanea.

Las 29 fichas ya tienen aprobacion humana de construccion; no necesitan otra aprobacion del mismo alcance. Antes de cada una, verificar la aceptacion de la anterior, las interfaces reales y los requisitos pendientes. Esto no autoriza ejecutar todas sin pausas de revision y aceptacion.
Este mapa es un plan de alcance, no una promesa de completar 29 entregas antes de una fecha. Si el calendario exige recorte, el usuario decide formalmente; no se omiten P0 por urgencia.

## Proximo paso real

PZ-003B ya tiene aceptacion final humana registrada; no solicitarla de nuevo.
- Concretar los detalles tecnicos pendientes de [PZ-003C](PIEZAS-PENDIENTES/FICHA-PZ-003C.md) y usar su prompt con Antigravity. La dependencia de aceptacion esta satisfecha; verificar los demas requisitos antes de editar.
- El recorrido manual de PZ-003B permanece declarado PENDIENTE. El usuario puede realizarlo en su terminal con `python -B -m app.demo_plan_review --interactive`; el asistente no responde por el usuario.
- Registrar evidencia solo cuando exista. La aceptacion de la pieza no demuestra la prueba manual ni completa CT-009.
- El log de pruebas fue eliminado con autorizacion en la entrega anterior; no crearlo nuevamente como residuo.

## Cambios de esta entrega

Preparacion original: este mapa, dos documentos comunes y 29 fichas en PIEZAS-PENDIENTES; se elimino test_output.log con autorizacion expresa en esa entrega.
Actualizacion de aprobacion del 30 de agosto de 2026: solo esos 32 documentos. No se modifica el contrato, AGENTS.md, TEAM-WORKFLOW.md, fichas anteriores, README, pruebas, configuracion o codigo; no hay nuevas eliminaciones.
Registro posterior de aceptacion de PZ-003B: se actualizan unicamente su ficha, este mapa, la guia comun y la dependencia en PZ-003C. No se modifica codigo ni se ejecutan pruebas nuevas por registrar la decision.
Las huellas y validacion del paquete se comunican al usuario; no se crean logs ni archivos de reporte adicionales.

## Limites de vigencia

La seleccion cloud/modelo y la fecha del concurso se heredan como decisiones registradas del contrato, no como verificacion externa actual.
Antes de llamadas reales, despliegue, gasto o presentacion se verifican versiones, precios, disponibilidad, reglas y plazo en fuentes oficiales.
No hay credenciales, recursos cloud ni permiso de publicacion en este paquete. Los valores faltantes estan en el registro tecnico de la guia comun.
