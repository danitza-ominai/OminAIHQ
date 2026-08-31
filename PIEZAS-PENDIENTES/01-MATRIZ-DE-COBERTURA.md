# Matriz de cobertura del contrato y checklist

Estado: PLANIFICACION_PENDIENTE_DE_EVIDENCIA
Fuente: [CONTRATO-MVP-v1.md](../CONTRATO-MVP-v1.md), seccion 8A y Anexo C, version 1.2-aprobada.
No se altera el checklist original. IDs Cxx-yy son localizadores documentales: seccion y ordinal del control, no nuevos requisitos.
Las 29 fichas fueron aprobadas para construccion por Antigravity el 30 de agosto de 2026. Esa autorizacion no cierra controles, no aporta evidencia de ejecucion ni ratifica automaticamente una excepcion N/A.

## 1. Resumen de alcance planificado

- 174 controles trazados individualmente: 78 P0, 87 P1 y 9 P2.
- 78 P0 con ruta de evidencia, ninguno marcado completo ni N/A automaticamente.
- 71 de 87 P1 seleccionados (81.6 % del total); la mayoria esta PLANIFICADA, no implementada por esta entrega.
- 15 P1 diferidos por PT-006 y 1 N/A propuesto que requiere ratificacion humana.
- 9 P2 diferidos. No se usan para compensar un P0 ausente.
- 15 condiciones de C.18 y cuatro requisitos adicionales del gate 15.7 con responsables.
- CT-003/CT-008 siguen dentro de v0; memoria y recuperacion no se difieren al hipotetico producto de produccion.

SELECCIONADO significa que estas fichas ofrecen una ruta de implementacion/prueba. No acredita cobertura funcional lograda.
Todo estado de ejecucion empieza PENDIENTE_DE_EVIDENCIA. Campos de cierre requeridos: evidence_id, version/huella, fecha, metodo, resultado, limitacion y aprobacion humana si N/A.
El porcentaje no cuenta P0/P2 ni N/A como P1 implementado. El alcance seleccionado de las fichas esta aprobado; la cobertura efectiva y la ratificacion especifica del N/A siguen pendientes.

## 2. Treinta requisitos funcionales

| Requisito | Piezas responsables | Evidencia exigida |
|---|---|---|
| RF-001 | [PZ-004B](FICHA-PZ-004B.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-015A](FICHA-PZ-015A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-002 | [PZ-004B](FICHA-PZ-004B.md), [PZ-010A](FICHA-PZ-010A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-003 | [PZ-004B](FICHA-PZ-004B.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-004 | [PZ-004B](FICHA-PZ-004B.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-005 | [PZ-003C](FICHA-PZ-003C.md), [PZ-004B](FICHA-PZ-004B.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-006 | [PZ-003F](FICHA-PZ-003F.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-013A](FICHA-PZ-013A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-007 | [PZ-003D](FICHA-PZ-003D.md), [PZ-012A](FICHA-PZ-012A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-008 | [PZ-003D](FICHA-PZ-003D.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-009 | [PZ-003C](FICHA-PZ-003C.md), [PZ-004A](FICHA-PZ-004A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-010 | [PZ-003C](FICHA-PZ-003C.md), [PZ-005A](FICHA-PZ-005A.md), [PZ-009A](FICHA-PZ-009A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-011 | [PZ-005A](FICHA-PZ-005A.md), [PZ-009A](FICHA-PZ-009A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-012 | [PZ-006A](FICHA-PZ-006A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-013 | [PZ-007A](FICHA-PZ-007A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-014 | [PZ-003C](FICHA-PZ-003C.md), [PZ-003E](FICHA-PZ-003E.md), [PZ-004B](FICHA-PZ-004B.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-015 | [PZ-008A](FICHA-PZ-008A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-016 | [PZ-003F](FICHA-PZ-003F.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-013A](FICHA-PZ-013A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-017 | [PZ-012A](FICHA-PZ-012A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-018 | [PZ-003E](FICHA-PZ-003E.md), [PZ-003F](FICHA-PZ-003F.md), [PZ-013C](FICHA-PZ-013C.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-019 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-013B](FICHA-PZ-013B.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-020 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013C](FICHA-PZ-013C.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-021 | [PZ-010B](FICHA-PZ-010B.md), [PZ-012B](FICHA-PZ-012B.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-022 | [PZ-010A](FICHA-PZ-010A.md), [PZ-010B](FICHA-PZ-010B.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-023 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004A](FICHA-PZ-004A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-024 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004A](FICHA-PZ-004A.md), [PZ-007A](FICHA-PZ-007A.md), [PZ-012B](FICHA-PZ-012B.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-025 | [PZ-013A](FICHA-PZ-013A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-026 | [PZ-003D](FICHA-PZ-003D.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-027 | [PZ-003D](FICHA-PZ-003D.md), [PZ-013C](FICHA-PZ-013C.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-028 | [PZ-003C](FICHA-PZ-003C.md), [PZ-003E](FICHA-PZ-003E.md), [PZ-006A](FICHA-PZ-006A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-029 | [PZ-004B](FICHA-PZ-004B.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-012B](FICHA-PZ-012B.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |
| RF-030 | [PZ-003E](FICHA-PZ-003E.md), [PZ-003F](FICHA-PZ-003F.md), [PZ-013C](FICHA-PZ-013C.md), [PZ-015A](FICHA-PZ-015A.md) | Criterio exacto de seccion 7, positivo y rechazo; PENDIENTE_DE_EVIDENCIA |

## 3. Quince requisitos no funcionales

| Requisito | Piezas responsables | Estado |
|---|---|---|
| RNF-001 | [PZ-009D](FICHA-PZ-009D.md), [PZ-015A](FICHA-PZ-015A.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |
| RNF-002 | [PZ-003C](FICHA-PZ-003C.md), [PZ-010A](FICHA-PZ-010A.md), [PZ-013C](FICHA-PZ-013C.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |
| RNF-003 | [PZ-004A](FICHA-PZ-004A.md), [PZ-005A](FICHA-PZ-005A.md), [PZ-012A](FICHA-PZ-012A.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |
| RNF-004 | [PZ-009B](FICHA-PZ-009B.md), [PZ-010C](FICHA-PZ-010C.md), [PZ-010D](FICHA-PZ-010D.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |
| RNF-005 | [PZ-010B](FICHA-PZ-010B.md), [PZ-012B](FICHA-PZ-012B.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |
| RNF-006 | [PZ-003D](FICHA-PZ-003D.md), [PZ-010A](FICHA-PZ-010A.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-013C](FICHA-PZ-013C.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |
| RNF-007 | [PZ-004A](FICHA-PZ-004A.md), [PZ-014A](FICHA-PZ-014A.md), [PZ-014B](FICHA-PZ-014B.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |
| RNF-008 | [PZ-008A](FICHA-PZ-008A.md), [PZ-011B](FICHA-PZ-011B.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |
| RNF-009 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013B](FICHA-PZ-013B.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |
| RNF-010 | [PZ-013B](FICHA-PZ-013B.md), [PZ-013C](FICHA-PZ-013C.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |
| RNF-011 | [PZ-013B](FICHA-PZ-013B.md), [PZ-015A](FICHA-PZ-015A.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |
| RNF-012 | [PZ-003C](FICHA-PZ-003C.md), [PZ-004A](FICHA-PZ-004A.md), [PZ-014A](FICHA-PZ-014A.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |
| RNF-013 | [PZ-003C](FICHA-PZ-003C.md), [PZ-010A](FICHA-PZ-010A.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |
| RNF-014 | [PZ-005A](FICHA-PZ-005A.md), [PZ-009A](FICHA-PZ-009A.md), [PZ-012B](FICHA-PZ-012B.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |
| RNF-015 | [PZ-004A](FICHA-PZ-004A.md), [PZ-015A](FICHA-PZ-015A.md) | PENDIENTE_DE_EVIDENCIA; verificar metodo de seccion 8 |

## 4. Diecisiete areas tecnicas CT

| Area | Piezas responsables | Regla de cierre |
|---|---|---|
| CT-001 | [PZ-004B](FICHA-PZ-004B.md), [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-002 | [PZ-003C](FICHA-PZ-003C.md), [PZ-004A](FICHA-PZ-004A.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-013A](FICHA-PZ-013A.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-003 | [PZ-010A](FICHA-PZ-010A.md), [PZ-010B](FICHA-PZ-010B.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-004 | [PZ-010C](FICHA-PZ-010C.md), [PZ-013B](FICHA-PZ-013B.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-005 | [PZ-009A](FICHA-PZ-009A.md), [PZ-009B](FICHA-PZ-009B.md), [PZ-009C](FICHA-PZ-009C.md), [PZ-010D](FICHA-PZ-010D.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-006 | [PZ-005A](FICHA-PZ-005A.md), [PZ-009A](FICHA-PZ-009A.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-007 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-008A](FICHA-PZ-008A.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-008 | [PZ-010B](FICHA-PZ-010B.md), [PZ-012B](FICHA-PZ-012B.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-009 | [PZ-012A](FICHA-PZ-012A.md), [PZ-012B](FICHA-PZ-012B.md), [PZ-013B](FICHA-PZ-013B.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-010 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-011 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-012 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-013 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-014 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-014B](FICHA-PZ-014B.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-015 | [PZ-009B](FICHA-PZ-009B.md), [PZ-010D](FICHA-PZ-010D.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-014A](FICHA-PZ-014A.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-016 | [PZ-013B](FICHA-PZ-013B.md), [PZ-013C](FICHA-PZ-013C.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |
| CT-017 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Evidencia real aplicable; no cerrar por plantilla, mock o afirmacion del constructor |

## 5. Los 174 controles, uno por uno

| ID local | Prioridad | Control del Anexo C | Disposicion propuesta | Piezas | Evidencia o motivo |
|---|---|---|---|---|---|
| C01-01 | P0 | El proyecto identifica un problema real, especifico y comprensible. | PLANIFICADO_P0 | [PZ-004B](FICHA-PZ-004B.md), [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Mision real, criterio medible y matriz de alcance/estado; no solo una ficha. |
| C01-02 | P0 | Esta definido quien es el usuario principal y que resultado necesita. | PLANIFICADO_P0 | [PZ-004B](FICHA-PZ-004B.md), [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Mision real, criterio medible y matriz de alcance/estado; no solo una ficha. |
| C01-03 | P0 | Existe un criterio objetivo para determinar si el agente cumplio la tarea. | PLANIFICADO_P0 | [PZ-004B](FICHA-PZ-004B.md), [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Mision real, criterio medible y matriz de alcance/estado; no solo una ficha. |
| C01-04 | P0 | Se especifica que puede hacer el agente y que queda fuera de su alcance. | PLANIFICADO_P0 | [PZ-004B](FICHA-PZ-004B.md), [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Mision real, criterio medible y matriz de alcance/estado; no solo una ficha. |
| C01-05 | P0 | Se distingue claramente entre funciones implementadas, simuladas y propuestas. | PLANIFICADO_P0 | [PZ-004B](FICHA-PZ-004B.md), [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Mision real, criterio medible y matriz de alcance/estado; no solo una ficha. |
| C01-06 | P1 | El caso demuestra por que un agente aporta mas valor que un formulario o chatbot tradicional. | SELECCIONADO_P1 | [PZ-004B](FICHA-PZ-004B.md), [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Mision real, criterio medible y matriz de alcance/estado; no solo una ficha. |
| C01-07 | P1 | Se describen restricciones reales: tiempo, presupuesto, permisos, disponibilidad, politicas y preferencias. | SELECCIONADO_P1 | [PZ-004B](FICHA-PZ-004B.md), [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Mision real, criterio medible y matriz de alcance/estado; no solo una ficha. |
| C01-08 | P1 | Se identifican los principales casos limite y situaciones de fallo. | SELECCIONADO_P1 | [PZ-004B](FICHA-PZ-004B.md), [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Mision real, criterio medible y matriz de alcance/estado; no solo una ficha. |
| C02-01 | P0 | Existe un agente raiz con instrucciones claras y un objetivo delimitado. | PLANIFICADO_P0 | [PZ-003C](FICHA-PZ-003C.md), [PZ-004A](FICHA-PZ-004A.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-013A](FICHA-PZ-013A.md) | Invocacion real con contrato, lista de tools, trazas minimizadas y Runner/backend propio. |
| C02-02 | P0 | Las herramientas disponibles estan definidas y limitadas segun la responsabilidad del agente. | PLANIFICADO_P0 | [PZ-003C](FICHA-PZ-003C.md), [PZ-004A](FICHA-PZ-004A.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-013A](FICHA-PZ-013A.md) | Invocacion real con contrato, lista de tools, trazas minimizadas y Runner/backend propio. |
| C02-03 | P0 | Las acciones deterministas se realizan mediante codigo o herramientas, no se dejan a la improvisacion del modelo. | PLANIFICADO_P0 | [PZ-003C](FICHA-PZ-003C.md), [PZ-004A](FICHA-PZ-004A.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-013A](FICHA-PZ-013A.md) | Invocacion real con contrato, lista de tools, trazas minimizadas y Runner/backend propio. |
| C02-04 | P0 | El modelo se utiliza para tareas que requieren interpretacion, razonamiento o lenguaje natural. | PLANIFICADO_P0 | [PZ-003C](FICHA-PZ-003C.md), [PZ-004A](FICHA-PZ-004A.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-013A](FICHA-PZ-013A.md) | Invocacion real con contrato, lista de tools, trazas minimizadas y Runner/backend propio. |
| C02-05 | P0 | El agente registra que herramientas utilizo y en que secuencia. | PLANIFICADO_P0 | [PZ-003C](FICHA-PZ-003C.md), [PZ-004A](FICHA-PZ-004A.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-013A](FICHA-PZ-013A.md) | Invocacion real con contrato, lista de tools, trazas minimizadas y Runner/backend propio. |
| C02-06 | P1 | La arquitectura separa modelo, herramientas, sesiones, memoria y artefactos. | SELECCIONADO_P1 | [PZ-003C](FICHA-PZ-003C.md), [PZ-004A](FICHA-PZ-004A.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-013A](FICHA-PZ-013A.md) | Invocacion real con contrato, lista de tools, trazas minimizadas y Runner/backend propio. |
| C02-07 | P1 | Existe un `Runner` o servicio equivalente que permita utilizar el agente fuera de ADK Web. | SELECCIONADO_P1 | [PZ-003C](FICHA-PZ-003C.md), [PZ-004A](FICHA-PZ-004A.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-013A](FICHA-PZ-013A.md) | Invocacion real con contrato, lista de tools, trazas minimizadas y Runner/backend propio. |
| C02-08 | P1 | El agente puede ejecutarse desde un backend o API propia. | SELECCIONADO_P1 | [PZ-003C](FICHA-PZ-003C.md), [PZ-004A](FICHA-PZ-004A.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-013A](FICHA-PZ-013A.md) | Invocacion real con contrato, lista de tools, trazas minimizadas y Runner/backend propio. |
| C02-09 | P1 | Las entradas y salidas importantes utilizan esquemas definidos. | SELECCIONADO_P1 | [PZ-003C](FICHA-PZ-003C.md), [PZ-004A](FICHA-PZ-004A.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-013A](FICHA-PZ-013A.md) | Invocacion real con contrato, lista de tools, trazas minimizadas y Runner/backend propio. |
| C02-10 | P2 | Existen interceptores o callbacks para aplicar validaciones antes y despues de llamadas sensibles. | DIFERIDO_P2 | [PZ-003C](FICHA-PZ-003C.md), [PZ-004A](FICHA-PZ-004A.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-013A](FICHA-PZ-013A.md) | Diferido por PT-006/prioridad P0-P1; no se agrega infraestructura opcional ni se marca cumplido. |
| C03-01 | P0 | Los datos necesarios para ejecutar acciones se guardan como estado estructurado. | PLANIFICADO_P0 | [PZ-010A](FICHA-PZ-010A.md), [PZ-010B](FICHA-PZ-010B.md) | Reinicio en proceso nuevo, mismo checkpoint/contadores, rechazo de cruces y duplicados. |
| C03-02 | P0 | Identificadores, decisiones, montos, estados de procesos y permisos no dependen unicamente del texto del chat. | PLANIFICADO_P0 | [PZ-010A](FICHA-PZ-010A.md), [PZ-010B](FICHA-PZ-010B.md) | Reinicio en proceso nuevo, mismo checkpoint/contadores, rechazo de cruces y duplicados. |
| C03-03 | P0 | Las sesiones se almacenan de forma persistente. | PLANIFICADO_P0 | [PZ-010A](FICHA-PZ-010A.md), [PZ-010B](FICHA-PZ-010B.md) | Reinicio en proceso nuevo, mismo checkpoint/contadores, rechazo de cruces y duplicados. |
| C03-04 | P0 | Una conversacion puede recuperarse despues de reiniciar el servidor. | PLANIFICADO_P0 | [PZ-010A](FICHA-PZ-010A.md), [PZ-010B](FICHA-PZ-010B.md) | Reinicio en proceso nuevo, mismo checkpoint/contadores, rechazo de cruces y duplicados. |
| C03-05 | P0 | El sistema distingue entre historial conversacional, estado operativo y memoria de largo plazo. | PLANIFICADO_P0 | [PZ-010A](FICHA-PZ-010A.md), [PZ-010B](FICHA-PZ-010B.md) | Reinicio en proceso nuevo, mismo checkpoint/contadores, rechazo de cruces y duplicados. |
| C03-06 | P1 | El estado tiene alcance definido por usuario, sesion o aplicacion. | SELECCIONADO_P1 | [PZ-010A](FICHA-PZ-010A.md), [PZ-010B](FICHA-PZ-010B.md) | Reinicio en proceso nuevo, mismo checkpoint/contadores, rechazo de cruces y duplicados. |
| C03-07 | P1 | Se evita compartir accidentalmente el estado entre usuarios. | SELECCIONADO_P1 | [PZ-010A](FICHA-PZ-010A.md), [PZ-010B](FICHA-PZ-010B.md) | Reinicio en proceso nuevo, mismo checkpoint/contadores, rechazo de cruces y duplicados. |
| C03-08 | P1 | Existe una estrategia para reanudar procesos despues de fallos. | SELECCIONADO_P1 | [PZ-010A](FICHA-PZ-010A.md), [PZ-010B](FICHA-PZ-010B.md) | Reinicio en proceso nuevo, mismo checkpoint/contadores, rechazo de cruces y duplicados. |
| C03-09 | P1 | El sistema puede continuar desde el ultimo punto valido sin repetir todas las operaciones anteriores. | SELECCIONADO_P1 | [PZ-010A](FICHA-PZ-010A.md), [PZ-010B](FICHA-PZ-010B.md) | Reinicio en proceso nuevo, mismo checkpoint/contadores, rechazo de cruces y duplicados. |
| C04-01 | P0 | Esta definido cuando una conversacion o resultado se convierte en memoria. | PLANIFICADO_P0 | [PZ-010C](FICHA-PZ-010C.md), [PZ-013B](FICHA-PZ-013B.md) | Confirmacion de recuerdo; uso en nueva mision tras reinicio; bloqueo de conflicto; correccion/purga. |
| C04-02 | P0 | Esta definida la consulta o politica mediante la cual se recupera esa memoria. | PLANIFICADO_P0 | [PZ-010C](FICHA-PZ-010C.md), [PZ-013B](FICHA-PZ-013B.md) | Confirmacion de recuerdo; uso en nueva mision tras reinicio; bloqueo de conflicto; correccion/purga. |
| C04-03 | P0 | El agente puede reconocer informacion relevante de interacciones anteriores. | PLANIFICADO_P0 | [PZ-010C](FICHA-PZ-010C.md), [PZ-013B](FICHA-PZ-013B.md) | Confirmacion de recuerdo; uso en nueva mision tras reinicio; bloqueo de conflicto; correccion/purga. |
| C04-04 | P0 | La memoria esta separada por aplicacion y usuario. | PLANIFICADO_P0 | [PZ-010C](FICHA-PZ-010C.md), [PZ-013B](FICHA-PZ-013B.md) | Confirmacion de recuerdo; uso en nueva mision tras reinicio; bloqueo de conflicto; correccion/purga. |
| C04-05 | P1 | La memoria sobrevive al reinicio del proceso. | SELECCIONADO_P1 | [PZ-010C](FICHA-PZ-010C.md), [PZ-013B](FICHA-PZ-013B.md) | Confirmacion de recuerdo; uso en nueva mision tras reinicio; bloqueo de conflicto; correccion/purga. |
| C04-06 | P1 | Existe un servicio persistente, como Vertex AI Memory Bank o un equivalente justificado. | SELECCIONADO_P1 | [PZ-010C](FICHA-PZ-010C.md), [PZ-013B](FICHA-PZ-013B.md) | Confirmacion de recuerdo; uso en nueva mision tras reinicio; bloqueo de conflicto; correccion/purga. |
| C04-07 | P1 | Se distingue entre guardar la conversacion completa y guardar hechos consolidados. | SELECCIONADO_P1 | [PZ-010C](FICHA-PZ-010C.md), [PZ-013B](FICHA-PZ-013B.md) | Confirmacion de recuerdo; uso en nueva mision tras reinicio; bloqueo de conflicto; correccion/purga. |
| C04-08 | P1 | El usuario puede saber que informacion relevante se conservo. | SELECCIONADO_P1 | [PZ-010C](FICHA-PZ-010C.md), [PZ-013B](FICHA-PZ-013B.md) | Confirmacion de recuerdo; uso en nueva mision tras reinicio; bloqueo de conflicto; correccion/purga. |
| C04-09 | P1 | Existe una politica para corregir o eliminar recuerdos. | SELECCIONADO_P1 | [PZ-010C](FICHA-PZ-010C.md), [PZ-013B](FICHA-PZ-013B.md) | Confirmacion de recuerdo; uso en nueva mision tras reinicio; bloqueo de conflicto; correccion/purga. |
| C04-10 | P2 | La recuperacion es semantica y no depende exclusivamente de coincidencias de palabras. | DIFERIDO_P2 | [PZ-010C](FICHA-PZ-010C.md), [PZ-013B](FICHA-PZ-013B.md) | Diferido por PT-006/prioridad P0-P1; no se agrega infraestructura opcional ni se marca cumplido. |
| C05-01 | P0 | El agente puede procesar los archivos que sean necesarios para el caso de uso. | PLANIFICADO_P0 | [PZ-009A](FICHA-PZ-009A.md), [PZ-009B](FICHA-PZ-009B.md), [PZ-009C](FICHA-PZ-009C.md), [PZ-010D](FICHA-PZ-010D.md) | Original/hash/localizador, extraccion demostrada, limites y privacidad; imagen cuando corresponda. |
| C05-02 | P0 | La informacion extraida de un archivo se guarda como datos estructurados. | PLANIFICADO_P0 | [PZ-009A](FICHA-PZ-009A.md), [PZ-009B](FICHA-PZ-009B.md), [PZ-009C](FICHA-PZ-009C.md), [PZ-010D](FICHA-PZ-010D.md) | Original/hash/localizador, extraccion demostrada, limites y privacidad; imagen cuando corresponda. |
| C05-03 | P0 | El archivo original se conserva como artefacto cuando constituye evidencia. | PLANIFICADO_P0 | [PZ-009A](FICHA-PZ-009A.md), [PZ-009B](FICHA-PZ-009B.md), [PZ-009C](FICHA-PZ-009C.md), [PZ-010D](FICHA-PZ-010D.md) | Original/hash/localizador, extraccion demostrada, limites y privacidad; imagen cuando corresponda. |
| C05-04 | P0 | Los hechos extraidos mantienen una referencia al artefacto original. | PLANIFICADO_P0 | [PZ-009A](FICHA-PZ-009A.md), [PZ-009B](FICHA-PZ-009B.md), [PZ-009C](FICHA-PZ-009C.md), [PZ-010D](FICHA-PZ-010D.md) | Original/hash/localizador, extraccion demostrada, limites y privacidad; imagen cuando corresponda. |
| C05-05 | P1 | Los artefactos tienen usuario, alcance y versiones. | SELECCIONADO_P1 | [PZ-009A](FICHA-PZ-009A.md), [PZ-009B](FICHA-PZ-009B.md), [PZ-009C](FICHA-PZ-009C.md), [PZ-010D](FICHA-PZ-010D.md) | Original/hash/localizador, extraccion demostrada, limites y privacidad; imagen cuando corresponda. |
| C05-06 | P1 | El sistema evita afirmar que conservo un archivo cuando unicamente interpreto el mensaje. | SELECCIONADO_P1 | [PZ-009A](FICHA-PZ-009A.md), [PZ-009B](FICHA-PZ-009B.md), [PZ-009C](FICHA-PZ-009C.md), [PZ-010D](FICHA-PZ-010D.md) | Original/hash/localizador, extraccion demostrada, limites y privacidad; imagen cuando corresponda. |
| C05-07 | P1 | Se controla que formatos, tamanos y tipos de archivo pueden recibirse. | SELECCIONADO_P1 | [PZ-009A](FICHA-PZ-009A.md), [PZ-009B](FICHA-PZ-009B.md), [PZ-009C](FICHA-PZ-009C.md), [PZ-010D](FICHA-PZ-010D.md) | Original/hash/localizador, extraccion demostrada, limites y privacidad; imagen cuando corresponda. |
| C05-08 | P1 | Los datos sensibles de los archivos reciben controles de acceso apropiados. | SELECCIONADO_P1 | [PZ-009A](FICHA-PZ-009A.md), [PZ-009B](FICHA-PZ-009B.md), [PZ-009C](FICHA-PZ-009C.md), [PZ-010D](FICHA-PZ-010D.md) | Original/hash/localizador, extraccion demostrada, limites y privacidad; imagen cuando corresponda. |
| C06-01 | P0 | El agente se conecta con una fuente de informacion real o representativa del proyecto. | PLANIFICADO_P0 | [PZ-005A](FICHA-PZ-005A.md), [PZ-009A](FICHA-PZ-009A.md) | Consulta real autorizada y parametrizada, fuente/localizador verificados y rechazo de acceso ajeno. |
| C06-02 | P0 | Las consultas criticas utilizan herramientas gobernadas y parametrizadas. | PLANIFICADO_P0 | [PZ-005A](FICHA-PZ-005A.md), [PZ-009A](FICHA-PZ-009A.md) | Consulta real autorizada y parametrizada, fuente/localizador verificados y rechazo de acceso ajeno. |
| C06-03 | P0 | El modelo proporciona parametros; no genera libremente consultas sensibles contra toda la base de datos. | PLANIFICADO_P0 | [PZ-005A](FICHA-PZ-005A.md), [PZ-009A](FICHA-PZ-009A.md) | Consulta real autorizada y parametrizada, fuente/localizador verificados y rechazo de acceso ajeno. |
| C06-04 | P0 | Las respuestas importantes incluyen una ruta de evidencia o explicacion verificable. | PLANIFICADO_P0 | [PZ-005A](FICHA-PZ-005A.md), [PZ-009A](FICHA-PZ-009A.md) | Consulta real autorizada y parametrizada, fuente/localizador verificados y rechazo de acceso ajeno. |
| C06-05 | P1 | El proyecto diferencia una coincidencia textual de una relacion real entre registros. | SELECCIONADO_P1 | [PZ-005A](FICHA-PZ-005A.md), [PZ-009A](FICHA-PZ-009A.md) | Consulta real autorizada y parametrizada, fuente/localizador verificados y rechazo de acceso ajeno. |
| C06-06 | P1 | Existe un recorrido determinista para preguntas relacionadas con usuarios, empresas, procesos o decisiones. | SELECCIONADO_P1 | [PZ-005A](FICHA-PZ-005A.md), [PZ-009A](FICHA-PZ-009A.md) | Consulta real autorizada y parametrizada, fuente/localizador verificados y rechazo de acceso ajeno. |
| C06-07 | P1 | La busqueda semantica utiliza embeddings cuando el significado es mas importante que las palabras exactas. | DIFERIDO_PT006 | [PZ-005A](FICHA-PZ-005A.md), [PZ-009A](FICHA-PZ-009A.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C06-08 | P1 | Los datos estructurados, embeddings y resultados permanecen cerca de la fuente empresarial cuando sea posible. | DIFERIDO_PT006 | [PZ-005A](FICHA-PZ-005A.md), [PZ-009A](FICHA-PZ-009A.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C06-09 | P2 | Se utiliza BigQuery, una base vectorial o una arquitectura equivalente con una justificacion clara. | DIFERIDO_P2 | [PZ-005A](FICHA-PZ-005A.md), [PZ-009A](FICHA-PZ-009A.md) | Diferido por PT-006/prioridad P0-P1; no se agrega infraestructura opcional ni se marca cumplido. |
| C07-01 | P0 | El proceso principal esta representado como una secuencia comprensible de pasos. | PLANIFICADO_P0 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-008A](FICHA-PZ-008A.md) | Cinco roles separados en orden fijo; dependencia fallida detiene; contexto y tools minimos. |
| C07-02 | P0 | Las decisiones deterministas estan codificadas mediante condiciones, rutas o grafos. | PLANIFICADO_P0 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-008A](FICHA-PZ-008A.md) | Cinco roles separados en orden fijo; dependencia fallida detiene; contexto y tools minimos. |
| C07-03 | P0 | El agente no decide libremente el orden de un proceso que debe cumplir una secuencia obligatoria. | PLANIFICADO_P0 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-008A](FICHA-PZ-008A.md) | Cinco roles separados en orden fijo; dependencia fallida detiene; contexto y tools minimos. |
| C07-04 | P1 | Se utilizan pasos secuenciales cuando existe dependencia entre resultados. | SELECCIONADO_P1 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-008A](FICHA-PZ-008A.md) | Cinco roles separados en orden fijo; dependencia fallida detiene; contexto y tools minimos. |
| C07-05 | P1 | Se utilizan tareas paralelas solamente cuando son independientes. | DIFERIDO_PT006 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-008A](FICHA-PZ-008A.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C07-06 | P1 | Las ramas tienen condiciones explicitas de entrada y salida. | SELECCIONADO_P1 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-008A](FICHA-PZ-008A.md) | Cinco roles separados en orden fijo; dependencia fallida detiene; contexto y tools minimos. |
| C07-07 | P1 | Los resultados paralelos se reunen antes de producir la respuesta final. | DIFERIDO_PT006 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-008A](FICHA-PZ-008A.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C07-08 | P1 | Cada subagente tiene una responsabilidad limitada. | SELECCIONADO_P1 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-008A](FICHA-PZ-008A.md) | Cinco roles separados en orden fijo; dependencia fallida detiene; contexto y tools minimos. |
| C07-09 | P1 | El agente raiz conserva el control cuando un subagente se utiliza como herramienta. | SELECCIONADO_P1 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-008A](FICHA-PZ-008A.md) | Cinco roles separados en orden fijo; dependencia fallida detiene; contexto y tools minimos. |
| C07-10 | P1 | Se evita enviar a cada subagente informacion que no necesita. | SELECCIONADO_P1 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-008A](FICHA-PZ-008A.md) | Cinco roles separados en orden fijo; dependencia fallida detiene; contexto y tools minimos. |
| C07-11 | P1 | La division de responsabilidades reduce contexto, costo y alucinaciones. | SELECCIONADO_P1 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-008A](FICHA-PZ-008A.md) | Cinco roles separados en orden fijo; dependencia fallida detiene; contexto y tools minimos. |
| C07-12 | P2 | Existen workflows dinamicos cuando el numero de tareas depende de la solicitud. | DIFERIDO_P2 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-008A](FICHA-PZ-008A.md) | Diferido por PT-006/prioridad P0-P1; no se agrega infraestructura opcional ni se marca cumplido. |
| C07-13 | P2 | Las rutas entre agentes y herramientas se pueden inspeccionar como un grafo. | DIFERIDO_P2 | [PZ-003D](FICHA-PZ-003D.md), [PZ-004B](FICHA-PZ-004B.md), [PZ-008A](FICHA-PZ-008A.md) | Diferido por PT-006/prioridad P0-P1; no se agrega infraestructura opcional ni se marca cumplido. |
| C08-01 | P0 | Un proceso largo puede pausarse y reanudarse. | PLANIFICADO_P0 | [PZ-010B](FICHA-PZ-010B.md), [PZ-012B](FICHA-PZ-012B.md) | Interrupcion y reanudacion sin duplicar; datos revalidados; contadores/limites conservados. |
| C08-02 | P0 | El sistema conserva el punto exacto de continuacion. | PLANIFICADO_P0 | [PZ-010B](FICHA-PZ-010B.md), [PZ-012B](FICHA-PZ-012B.md) | Interrupcion y reanudacion sin duplicar; datos revalidados; contadores/limites conservados. |
| C08-03 | P0 | Reanudar no repite operaciones costosas o irreversibles. | PLANIFICADO_P0 | [PZ-010B](FICHA-PZ-010B.md), [PZ-012B](FICHA-PZ-012B.md) | Interrupcion y reanudacion sin duplicar; datos revalidados; contadores/limites conservados. |
| C08-04 | P0 | Antes de ejecutar una accion final se actualizan los datos que pueden haber cambiado. | PLANIFICADO_P0 | [PZ-010B](FICHA-PZ-010B.md), [PZ-012B](FICHA-PZ-012B.md) | Interrupcion y reanudacion sin duplicar; datos revalidados; contadores/limites conservados. |
| C08-05 | P1 | Existen callbacks para consultar informacion fresca antes de confirmar una operacion. | DIFERIDO_PT006 | [PZ-010B](FICHA-PZ-010B.md), [PZ-012B](FICHA-PZ-012B.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C08-06 | P1 | El sistema soporta eventos externos, tareas programadas o mensajes de otros servicios. | DIFERIDO_PT006 | [PZ-010B](FICHA-PZ-010B.md), [PZ-012B](FICHA-PZ-012B.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C08-07 | P1 | Los procesos autonomos tienen limites de tiempo, costo, numero de pasos y reintentos. | SELECCIONADO_P1 | [PZ-010B](FICHA-PZ-010B.md), [PZ-012B](FICHA-PZ-012B.md) | Interrupcion y reanudacion sin duplicar; datos revalidados; contadores/limites conservados. |
| C08-08 | P1 | Los errores transitorios tienen reintentos controlados. | SELECCIONADO_P1 | [PZ-010B](FICHA-PZ-010B.md), [PZ-012B](FICHA-PZ-012B.md) | Interrupcion y reanudacion sin duplicar; datos revalidados; contadores/limites conservados. |
| C08-09 | P1 | Los errores definitivos producen un estado claro y recuperable. | SELECCIONADO_P1 | [PZ-010B](FICHA-PZ-010B.md), [PZ-012B](FICHA-PZ-012B.md) | Interrupcion y reanudacion sin duplicar; datos revalidados; contadores/limites conservados. |
| C08-10 | P2 | Se utilizan Cloud Scheduler, Pub/Sub u otros mecanismos event-driven cuando el caso realmente lo necesita. | DIFERIDO_P2 | [PZ-010B](FICHA-PZ-010B.md), [PZ-012B](FICHA-PZ-012B.md) | Diferido por PT-006/prioridad P0-P1; no se agrega infraestructura opcional ni se marca cumplido. |
| C09-01 | P0 | Las acciones sensibles requieren aprobacion humana. | PLANIFICADO_P0 | [PZ-012A](FICHA-PZ-012A.md), [PZ-012B](FICHA-PZ-012B.md), [PZ-013B](FICHA-PZ-013B.md) | Decision real humana tras contexto completo; unica, versionada y persistida; rechazos negativos. |
| C09-02 | P0 | La solicitud queda realmente pausada; un campo de texto que diga `pending` no se considera aprobacion. | PLANIFICADO_P0 | [PZ-012A](FICHA-PZ-012A.md), [PZ-012B](FICHA-PZ-012B.md), [PZ-013B](FICHA-PZ-013B.md) | Decision real humana tras contexto completo; unica, versionada y persistida; rechazos negativos. |
| C09-03 | P0 | El supervisor recibe el contexto necesario antes de decidir. | PLANIFICADO_P0 | [PZ-012A](FICHA-PZ-012A.md), [PZ-012B](FICHA-PZ-012B.md), [PZ-013B](FICHA-PZ-013B.md) | Decision real humana tras contexto completo; unica, versionada y persistida; rechazos negativos. |
| C09-04 | P0 | La decision conserva responsable, fecha, resultado y observaciones. | PLANIFICADO_P0 | [PZ-012A](FICHA-PZ-012A.md), [PZ-012B](FICHA-PZ-012B.md), [PZ-013B](FICHA-PZ-013B.md) | Decision real humana tras contexto completo; unica, versionada y persistida; rechazos negativos. |
| C09-05 | P0 | Una aprobacion solo puede responderse una vez. | PLANIFICADO_P0 | [PZ-012A](FICHA-PZ-012A.md), [PZ-012B](FICHA-PZ-012B.md), [PZ-013B](FICHA-PZ-013B.md) | Decision real humana tras contexto completo; unica, versionada y persistida; rechazos negativos. |
| C09-06 | P0 | El agente no puede ejecutar una accion fuera de los permisos del usuario. | PLANIFICADO_P0 | [PZ-012A](FICHA-PZ-012A.md), [PZ-012B](FICHA-PZ-012B.md), [PZ-013B](FICHA-PZ-013B.md) | Decision real humana tras contexto completo; unica, versionada y persistida; rechazos negativos. |
| C09-07 | P1 | Existe una interfaz especifica para revisar, aprobar o rechazar acciones. | SELECCIONADO_P1 | [PZ-012A](FICHA-PZ-012A.md), [PZ-012B](FICHA-PZ-012B.md), [PZ-013B](FICHA-PZ-013B.md) | Decision real humana tras contexto completo; unica, versionada y persistida; rechazos negativos. |
| C09-08 | P1 | Las decisiones humanas quedan registradas para auditoria. | SELECCIONADO_P1 | [PZ-012A](FICHA-PZ-012A.md), [PZ-012B](FICHA-PZ-012B.md), [PZ-013B](FICHA-PZ-013B.md) | Decision real humana tras contexto completo; unica, versionada y persistida; rechazos negativos. |
| C09-09 | P1 | Se diferencian claramente aprobacion, rechazo, cancelacion y expiracion. | SELECCIONADO_P1 | [PZ-012A](FICHA-PZ-012A.md), [PZ-012B](FICHA-PZ-012B.md), [PZ-013B](FICHA-PZ-013B.md) | Decision real humana tras contexto completo; unica, versionada y persistida; rechazos negativos. |
| C09-10 | P1 | El sistema solicita confirmacion final para compras, pagos, publicaciones o cambios irreversibles. | NO_APLICA_PROPUESTO | [PZ-012A](FICHA-PZ-012A.md), [PZ-012B](FICHA-PZ-012B.md), [PZ-013B](FICHA-PZ-013B.md) | Pagos/compras/publicaciones externas excluidos de v0. Se prueba su denegacion; la confirmacion de eliminacion local sigue obligatoria en C.15. Ratificar N/A humano. |
| C10-01 | P0 | Existe un conjunto de casos de evaluacion reproducibles. | PLANIFICADO_P0 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Corrida congelada con referencias, umbral, resultado/estados/trayectoria y causas de fallo. |
| C10-02 | P0 | Cada caso contiene entrada, condiciones y resultado esperado. | PLANIFICADO_P0 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Corrida congelada con referencias, umbral, resultado/estados/trayectoria y causas de fallo. |
| C10-03 | P0 | El proyecto evalua el resultado final y tambien la trayectoria de herramientas. | PLANIFICADO_P0 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Corrida congelada con referencias, umbral, resultado/estados/trayectoria y causas de fallo. |
| C10-04 | P0 | Se verifica que el agente llego a la respuesta mediante el proceso autorizado. | PLANIFICADO_P0 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Corrida congelada con referencias, umbral, resultado/estados/trayectoria y causas de fallo. |
| C10-05 | P0 | Existe al menos una metrica determinista conectada con el objetivo real del producto. | PLANIFICADO_P0 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Corrida congelada con referencias, umbral, resultado/estados/trayectoria y causas de fallo. |
| C10-06 | P0 | Esta definido un umbral explicito de aprobacion. | PLANIFICADO_P0 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Corrida congelada con referencias, umbral, resultado/estados/trayectoria y causas de fallo. |
| C10-07 | P0 | Se documentan los casos exitosos y fallidos. | PLANIFICADO_P0 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Corrida congelada con referencias, umbral, resultado/estados/trayectoria y causas de fallo. |
| C10-08 | P1 | Se utilizan respuestas de referencia o conjuntos `golden`. | SELECCIONADO_P1 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Corrida congelada con referencias, umbral, resultado/estados/trayectoria y causas de fallo. |
| C10-09 | P1 | Se incorporan metricas de coincidencia, juez LLM y trayectoria cuando correspondan. | SELECCIONADO_P1 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Corrida congelada con referencias, umbral, resultado/estados/trayectoria y causas de fallo. |
| C10-10 | P1 | Los casos explican por que fallo el agente, no solamente que fallo. | SELECCIONADO_P1 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Corrida congelada con referencias, umbral, resultado/estados/trayectoria y causas de fallo. |
| C10-11 | P1 | Se incluyen restricciones, conflictos y casos limite. | SELECCIONADO_P1 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Corrida congelada con referencias, umbral, resultado/estados/trayectoria y causas de fallo. |
| C10-12 | P1 | Los resultados de evaluacion pueden ejecutarse nuevamente despues de cada cambio. | SELECCIONADO_P1 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Corrida congelada con referencias, umbral, resultado/estados/trayectoria y causas de fallo. |
| C10-13 | P1 | Se conservan evidencias de las metricas antes y despues de mejorar el agente. | SELECCIONADO_P1 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Corrida congelada con referencias, umbral, resultado/estados/trayectoria y causas de fallo. |
| C11-01 | P0 | Los casos utilizados para mejorar instrucciones estan separados de los casos de validacion final. | PLANIFICADO_P0 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Manifest y aislamiento real de dos holdout; ocho desarrollo; sin expectativas en agente. |
| C11-02 | P0 | Existe un conjunto de prueba o `holdout` que el optimizador no haya visto. | PLANIFICADO_P0 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Manifest y aislamiento real de dos holdout; ocho desarrollo; sin expectativas en agente. |
| C11-03 | P0 | El agente no se aprueba unicamente porque funciona con ejemplos conocidos. | PLANIFICADO_P0 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Manifest y aislamiento real de dos holdout; ocho desarrollo; sin expectativas en agente. |
| C11-04 | P1 | Los casos cubren distintas personas, restricciones y combinaciones de condiciones. | SELECCIONADO_P1 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Manifest y aislamiento real de dos holdout; ocho desarrollo; sin expectativas en agente. |
| C11-05 | P1 | Se incluyen ejemplos negativos y situaciones donde el agente debe detenerse. | SELECCIONADO_P1 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Manifest y aislamiento real de dos holdout; ocho desarrollo; sin expectativas en agente. |
| C11-06 | P1 | Los casos nuevos detectados en produccion se agregan al conjunto de evaluacion. | SELECCIONADO_P1 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Manifest y aislamiento real de dos holdout; ocho desarrollo; sin expectativas en agente. |
| C11-07 | P1 | Cada version del conjunto de evaluacion puede identificarse y reproducirse. | SELECCIONADO_P1 | [PZ-011A](FICHA-PZ-011A.md), [PZ-011B](FICHA-PZ-011B.md) | Manifest y aislamiento real de dos holdout; ocho desarrollo; sin expectativas en agente. |
| C12-01 | P1 | Existe una linea base evaluada antes de optimizar. | SELECCIONADO_P1 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Baseline/versionado y aprobacion/reversion manual; no confundirlo con optimizador autonomo. |
| C12-02 | P1 | La optimizacion utiliza los fallos y sus causas para proponer mejores instrucciones. | DIFERIDO_PT006 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C12-03 | P1 | La instruccion mejorada se vuelve a evaluar automaticamente. | DIFERIDO_PT006 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C12-04 | P1 | El ciclo contiene un agente o componente que ejecuta, otro que evalua y un enrutador determinista. | DIFERIDO_PT006 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C12-05 | P1 | El enrutador decide entre aprobar, volver a mejorar o detener. | DIFERIDO_PT006 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C12-06 | P1 | Existen criterios de salida medibles. | DIFERIDO_PT006 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C12-07 | P1 | Existe un numero maximo de iteraciones. | DIFERIDO_PT006 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C12-08 | P1 | Existe un presupuesto maximo de tokens, tiempo y costo. | DIFERIDO_PT006 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C12-09 | P1 | La mejor version se publica solamente despues de superar validacion. | SELECCIONADO_P1 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Baseline/versionado y aprobacion/reversion manual; no confundirlo con optimizador autonomo. |
| C12-10 | P1 | Las instrucciones y resultados estan versionados. | SELECCIONADO_P1 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Baseline/versionado y aprobacion/reversion manual; no confundirlo con optimizador autonomo. |
| C12-11 | P1 | Una persona puede revisar o revertir la version publicada. | SELECCIONADO_P1 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Baseline/versionado y aprobacion/reversion manual; no confundirlo con optimizador autonomo. |
| C12-12 | P2 | Se utiliza ADK Optimize o un mecanismo equivalente para proponer instrucciones. | DIFERIDO_P2 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Diferido por PT-006/prioridad P0-P1; no se agrega infraestructura opcional ni se marca cumplido. |
| C12-13 | P2 | El workflow completo ejecuta el ciclo: agente -> juez -> enrutador -> propuesta -> validacion -> publicacion. | DIFERIDO_P2 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Diferido por PT-006/prioridad P0-P1; no se agrega infraestructura opcional ni se marca cumplido. |
| C13-01 | P0 | La metrica representa el resultado real que importa al usuario. | PLANIFICADO_P0 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Caso de score alto y accion indebida rechazado; holdout, restricciones y reevaluacion. |
| C13-02 | P0 | El proyecto no optimiza unicamente similitud textual o una puntuacion facil de manipular. | PLANIFICADO_P0 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Caso de score alto y accion indebida rechazado; holdout, restricciones y reevaluacion. |
| C13-03 | P0 | Una respuesta correcta por casualidad no se considera ejecucion correcta. | PLANIFICADO_P0 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Caso de score alto y accion indebida rechazado; holdout, restricciones y reevaluacion. |
| C13-04 | P0 | Se verifica que se hayan respetado todas las restricciones. | PLANIFICADO_P0 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Caso de score alto y accion indebida rechazado; holdout, restricciones y reevaluacion. |
| C13-05 | P1 | Se combinan metricas de resultado, trayectoria, seguridad y satisfaccion de condiciones. | SELECCIONADO_P1 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Caso de score alto y accion indebida rechazado; holdout, restricciones y reevaluacion. |
| C13-06 | P1 | Los casos `holdout` detectan sobreajuste a los ejemplos de optimizacion. | SELECCIONADO_P1 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Caso de score alto y accion indebida rechazado; holdout, restricciones y reevaluacion. |
| C13-07 | P1 | Se revisan resultados con puntuacion alta pero comportamiento incorrecto. | SELECCIONADO_P1 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Caso de score alto y accion indebida rechazado; holdout, restricciones y reevaluacion. |
| C13-08 | P1 | Cambiar el juez, la metrica o los datos requiere volver a validar todo el agente. | SELECCIONADO_P1 | [PZ-011B](FICHA-PZ-011B.md), [PZ-015A](FICHA-PZ-015A.md) | Caso de score alto y accion indebida rechazado; holdout, restricciones y reevaluacion. |
| C14-01 | P0 | La interfaz final no expone ADK Web al usuario. | PLANIFICADO_P0 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-014B](FICHA-PZ-014B.md) | UI propia + backend real, auditoria local/cloud saneada y fallos reconstruibles. |
| C14-02 | P0 | Existe un frontend o canal de uso conectado a un backend controlado. | PLANIFICADO_P0 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-014B](FICHA-PZ-014B.md) | UI propia + backend real, auditoria local/cloud saneada y fallos reconstruibles. |
| C14-03 | P0 | Se registran ejecuciones, herramientas, errores, tiempos y decisiones. | PLANIFICADO_P0 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-014B](FICHA-PZ-014B.md) | UI propia + backend real, auditoria local/cloud saneada y fallos reconstruibles. |
| C14-04 | P0 | Se puede reconstruir por que el agente produjo una respuesta. | PLANIFICADO_P0 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-014B](FICHA-PZ-014B.md) | UI propia + backend real, auditoria local/cloud saneada y fallos reconstruibles. |
| C14-05 | P1 | Se habilitan trazas para detectar fallos en produccion. | SELECCIONADO_P1 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-014B](FICHA-PZ-014B.md) | UI propia + backend real, auditoria local/cloud saneada y fallos reconstruibles. |
| C14-06 | P1 | Los fallos se almacenan en una fuente analitica, como BigQuery. | SELECCIONADO_P1 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-014B](FICHA-PZ-014B.md) | Equivalente local propuesto: eventos tipados en repositorio + consultas/reportes de fallo; no obliga BigQuery. |
| C14-07 | P1 | Existe un proceso para convertir fallos reales en nuevos casos de evaluacion. | SELECCIONADO_P1 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-014B](FICHA-PZ-014B.md) | UI propia + backend real, auditoria local/cloud saneada y fallos reconstruibles. |
| C14-08 | P1 | Las nuevas versiones se prueban antes de reemplazar la version anterior. | SELECCIONADO_P1 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-014B](FICHA-PZ-014B.md) | UI propia + backend real, auditoria local/cloud saneada y fallos reconstruibles. |
| C14-09 | P1 | Existe monitoreo de latencia, consumo de tokens, costo y tasa de exito. | SELECCIONADO_P1 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-014B](FICHA-PZ-014B.md) | UI propia + backend real, auditoria local/cloud saneada y fallos reconstruibles. |
| C14-10 | P1 | Existe una ruta de reversion si una mejora reduce la calidad. | SELECCIONADO_P1 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-014B](FICHA-PZ-014B.md) | UI propia + backend real, auditoria local/cloud saneada y fallos reconstruibles. |
| C14-11 | P1 | Los cambios automaticos no llegan a produccion sin los controles definidos. | SELECCIONADO_P1 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-014B](FICHA-PZ-014B.md) | UI propia + backend real, auditoria local/cloud saneada y fallos reconstruibles. |
| C14-12 | P2 | El proyecto implementa un ciclo continuo: observar -> recolectar -> evaluar -> mejorar -> validar -> publicar. | DIFERIDO_P2 | [PZ-009D](FICHA-PZ-009D.md), [PZ-013A](FICHA-PZ-013A.md), [PZ-014B](FICHA-PZ-014B.md) | Diferido por PT-006/prioridad P0-P1; no se agrega infraestructura opcional ni se marca cumplido. |
| C15-01 | P0 | Cada herramienta aplica permisos minimos. | PLANIFICADO_P0 | [PZ-009B](FICHA-PZ-009B.md), [PZ-010D](FICHA-PZ-010D.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-014A](FICHA-PZ-014A.md) | Pruebas negativas de permisos, secretos, aislamiento, confirmacion, retencion y borrado. |
| C15-02 | P0 | Las acciones estan limitadas por identidad, rol y alcance. | PLANIFICADO_P0 | [PZ-009B](FICHA-PZ-009B.md), [PZ-010D](FICHA-PZ-010D.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-014A](FICHA-PZ-014A.md) | Pruebas negativas de permisos, secretos, aislamiento, confirmacion, retencion y borrado. |
| C15-03 | P0 | Los datos de un usuario no aparecen en la sesion o memoria de otro. | PLANIFICADO_P0 | [PZ-009B](FICHA-PZ-009B.md), [PZ-010D](FICHA-PZ-010D.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-014A](FICHA-PZ-014A.md) | Pruebas negativas de permisos, secretos, aislamiento, confirmacion, retencion y borrado. |
| C15-04 | P0 | Los secretos y credenciales no se incorporan a prompts ni repositorios. | PLANIFICADO_P0 | [PZ-009B](FICHA-PZ-009B.md), [PZ-010D](FICHA-PZ-010D.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-014A](FICHA-PZ-014A.md) | Pruebas negativas de permisos, secretos, aislamiento, confirmacion, retencion y borrado. |
| C15-05 | P0 | Las acciones irreversibles requieren confirmacion y registro. | PLANIFICADO_P0 | [PZ-009B](FICHA-PZ-009B.md), [PZ-010D](FICHA-PZ-010D.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-014A](FICHA-PZ-014A.md) | Pruebas negativas de permisos, secretos, aislamiento, confirmacion, retencion y borrado. |
| C15-06 | P0 | Se identifica que informacion se guarda, donde y durante cuanto tiempo. | PLANIFICADO_P0 | [PZ-009B](FICHA-PZ-009B.md), [PZ-010D](FICHA-PZ-010D.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-014A](FICHA-PZ-014A.md) | Pruebas negativas de permisos, secretos, aislamiento, confirmacion, retencion y borrado. |
| C15-07 | P1 | Existe una politica para eliminar sesiones, memorias y artefactos. | SELECCIONADO_P1 | [PZ-009B](FICHA-PZ-009B.md), [PZ-010D](FICHA-PZ-010D.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-014A](FICHA-PZ-014A.md) | Pruebas negativas de permisos, secretos, aislamiento, confirmacion, retencion y borrado. |
| C15-08 | P1 | Las consultas a datos empresariales estan parametrizadas. | SELECCIONADO_P1 | [PZ-009B](FICHA-PZ-009B.md), [PZ-010D](FICHA-PZ-010D.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-014A](FICHA-PZ-014A.md) | Pruebas negativas de permisos, secretos, aislamiento, confirmacion, retencion y borrado. |
| C15-09 | P1 | Las respuestas sensibles incluyen evidencia o una advertencia de incertidumbre. | SELECCIONADO_P1 | [PZ-009B](FICHA-PZ-009B.md), [PZ-010D](FICHA-PZ-010D.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-014A](FICHA-PZ-014A.md) | Pruebas negativas de permisos, secretos, aislamiento, confirmacion, retencion y borrado. |
| C15-10 | P1 | El proyecto documenta riesgos, mitigaciones y limitaciones conocidas. | SELECCIONADO_P1 | [PZ-009B](FICHA-PZ-009B.md), [PZ-010D](FICHA-PZ-010D.md), [PZ-012A](FICHA-PZ-012A.md), [PZ-014A](FICHA-PZ-014A.md) | Pruebas negativas de permisos, secretos, aislamiento, confirmacion, retencion y borrado. |
| C16-01 | P0 | El usuario entiende que esta haciendo el agente. | PLANIFICADO_P0 | [PZ-013B](FICHA-PZ-013B.md), [PZ-013C](FICHA-PZ-013C.md) | Recorrido humano con teclado, esperas/errores/contexto; decisiones y resultados diferenciados. |
| C16-02 | P0 | El sistema muestra cuando una operacion esta pendiente. | PLANIFICADO_P0 | [PZ-013B](FICHA-PZ-013B.md), [PZ-013C](FICHA-PZ-013C.md) | Recorrido humano con teclado, esperas/errores/contexto; decisiones y resultados diferenciados. |
| C16-03 | P0 | Se diferencia claramente entre recomendacion, accion ejecutada y accion aprobada. | PLANIFICADO_P0 | [PZ-013B](FICHA-PZ-013B.md), [PZ-013C](FICHA-PZ-013C.md) | Recorrido humano con teclado, esperas/errores/contexto; decisiones y resultados diferenciados. |
| C16-04 | P0 | Los errores ofrecen una forma segura de reintentar o continuar. | PLANIFICADO_P0 | [PZ-013B](FICHA-PZ-013B.md), [PZ-013C](FICHA-PZ-013C.md) | Recorrido humano con teclado, esperas/errores/contexto; decisiones y resultados diferenciados. |
| C16-05 | P0 | El usuario no necesita conocer la arquitectura interna para completar su tarea. | PLANIFICADO_P0 | [PZ-013B](FICHA-PZ-013B.md), [PZ-013C](FICHA-PZ-013C.md) | Recorrido humano con teclado, esperas/errores/contexto; decisiones y resultados diferenciados. |
| C16-06 | P1 | Las respuestas incluyen evidencia util sin abrumar al usuario. | SELECCIONADO_P1 | [PZ-013B](FICHA-PZ-013B.md), [PZ-013C](FICHA-PZ-013C.md) | Recorrido humano con teclado, esperas/errores/contexto; decisiones y resultados diferenciados. |
| C16-07 | P1 | La interfaz muestra estados de espera, aprobacion, finalizacion y fallo. | SELECCIONADO_P1 | [PZ-013B](FICHA-PZ-013B.md), [PZ-013C](FICHA-PZ-013C.md) | Recorrido humano con teclado, esperas/errores/contexto; decisiones y resultados diferenciados. |
| C16-08 | P1 | El supervisor dispone de una vista diferente de la del usuario final. | SELECCIONADO_P1 | [PZ-013B](FICHA-PZ-013B.md), [PZ-013C](FICHA-PZ-013C.md) | Vista operativa del unico humano y vista publica limitada del expediente; no inventar roles humanos adicionales ni login. |
| C16-09 | P1 | Los archivos y resultados importantes se pueden recuperar posteriormente. | SELECCIONADO_P1 | [PZ-013B](FICHA-PZ-013B.md), [PZ-013C](FICHA-PZ-013C.md) | Recorrido humano con teclado, esperas/errores/contexto; decisiones y resultados diferenciados. |
| C17-01 | P0 | Demostracion funcional de principio a fin. | PLANIFICADO_P0 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Paquete con ejecucion real, cifras, fuentes, memoria, aprobacion, arquitectura y limites. |
| C17-02 | P0 | Comparacion visible entre comportamiento defectuoso y comportamiento corregido. | PLANIFICADO_P0 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Paquete con ejecucion real, cifras, fuentes, memoria, aprobacion, arquitectura y limites. |
| C17-03 | P0 | Diagrama sencillo de arquitectura. | PLANIFICADO_P0 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Paquete con ejecucion real, cifras, fuentes, memoria, aprobacion, arquitectura y limites. |
| C17-04 | P0 | Explicacion de modelo, herramientas, estado, sesiones, memoria y datos. | PLANIFICADO_P0 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Paquete con ejecucion real, cifras, fuentes, memoria, aprobacion, arquitectura y limites. |
| C17-05 | P0 | Caso donde el sistema utiliza memoria de una conversacion anterior. | PLANIFICADO_P0 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Paquete con ejecucion real, cifras, fuentes, memoria, aprobacion, arquitectura y limites. |
| C17-06 | P0 | Caso donde una accion queda esperando aprobacion humana. | PLANIFICADO_P0 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Paquete con ejecucion real, cifras, fuentes, memoria, aprobacion, arquitectura y limites. |
| C17-07 | P0 | Caso donde una respuesta muestra su ruta de evidencia. | PLANIFICADO_P0 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Paquete con ejecucion real, cifras, fuentes, memoria, aprobacion, arquitectura y limites. |
| C17-08 | P0 | Resultados de evaluaciones con cifras verificables. | PLANIFICADO_P0 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Paquete con ejecucion real, cifras, fuentes, memoria, aprobacion, arquitectura y limites. |
| C17-09 | P0 | Lista honesta de funciones actuales, simulaciones y trabajo futuro. | PLANIFICADO_P0 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Paquete con ejecucion real, cifras, fuentes, memoria, aprobacion, arquitectura y limites. |
| C17-10 | P1 | Evidencia de recuperacion despues de reiniciar o interrumpir el proceso. | SELECCIONADO_P1 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Paquete con ejecucion real, cifras, fuentes, memoria, aprobacion, arquitectura y limites. |
| C17-11 | P1 | Evidencia de procesamiento de un archivo o entrada multimodal. | SELECCIONADO_P1 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Paquete con ejecucion real, cifras, fuentes, memoria, aprobacion, arquitectura y limites. |
| C17-12 | P1 | Evidencia de busqueda semantica o integracion empresarial. | DIFERIDO_PT006 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C17-13 | P1 | Metricas antes y despues de optimizar instrucciones. | DIFERIDO_PT006 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Fuera de la seleccion v0 (vectorial, paralelismo, eventos u optimizacion automatica); reevaluar solo mediante nueva decision humana. |
| C17-14 | P1 | Caso limite descubierto y forma en que el sistema aprendio de el. | SELECCIONADO_P1 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Paquete con ejecucion real, cifras, fuentes, memoria, aprobacion, arquitectura y limites. |
| C17-15 | P1 | Explicacion de privacidad, costos y controles humanos. | SELECCIONADO_P1 | [PZ-015A](FICHA-PZ-015A.md), [PZ-015B](FICHA-PZ-015B.md) | Paquete con ejecucion real, cifras, fuentes, memoria, aprobacion, arquitectura y limites. |

## 6. Quince condiciones de C.18

Todas permanecen PENDIENTE_DE_EVIDENCIA. PZ-015A consolida; no elude la prueba concreta de la pieza responsable.

| Gate | Condicion | Piezas |
|---|---|---|
| G01 | El caso de uso y el criterio de exito estan definidos. | [PZ-004B](FICHA-PZ-004B.md), [PZ-015A](FICHA-PZ-015A.md) |
| G02 | Existe un flujo completo funcional. | [PZ-003F](FICHA-PZ-003F.md), [PZ-008A](FICHA-PZ-008A.md), [PZ-015A](FICHA-PZ-015A.md) |
| G03 | Los datos operativos viven en estado estructurado. | [PZ-003C](FICHA-PZ-003C.md), [PZ-010A](FICHA-PZ-010A.md) |
| G04 | Las sesiones sobreviven a un reinicio. | [PZ-010B](FICHA-PZ-010B.md) |
| G05 | La memoria entre conversaciones tiene politica de escritura y recuperacion. | [PZ-010C](FICHA-PZ-010C.md) |
| G06 | Las acciones sensibles requieren aprobacion humana real. | [PZ-012A](FICHA-PZ-012A.md), [PZ-015A](FICHA-PZ-015A.md) |
| G07 | Las consultas criticas utilizan herramientas gobernadas. | [PZ-005A](FICHA-PZ-005A.md) |
| G08 | Existe un conjunto reproducible de evaluaciones. | [PZ-011A](FICHA-PZ-011A.md) |
| G09 | Se evaluan resultado y trayectoria. | [PZ-011B](FICHA-PZ-011B.md) |
| G10 | Existe un conjunto `holdout`. | [PZ-011A](FICHA-PZ-011A.md) |
| G11 | Los loops automaticos tienen limites y criterios de salida. | [PZ-004A](FICHA-PZ-004A.md), [PZ-012B](FICHA-PZ-012B.md) |
| G12 | Los fallos producen trazas y pueden convertirse en nuevos casos de evaluacion. | [PZ-009D](FICHA-PZ-009D.md), [PZ-011A](FICHA-PZ-011A.md) |
| G13 | La interfaz final funciona fuera de ADK Web. | [PZ-013A](FICHA-PZ-013A.md), [PZ-013B](FICHA-PZ-013B.md) |
| G14 | La demostracion distingue implementacion, simulacion y propuesta. | [PZ-015B](FICHA-PZ-015B.md) |
| G15 | Cada afirmacion importante tiene evidencia verificable. | [PZ-009A](FICHA-PZ-009A.md), [PZ-015A](FICHA-PZ-015A.md) |

## 7. Requisitos adicionales de 15.7

| Gate | Evidencia que falta | Piezas |
|---|---|---|
| G16 | Gemini del perfil aprobado, ADK y Google Cloud funcionando realmente; verificar versiones/reglas actuales | [PZ-004A](FICHA-PZ-004A.md), [PZ-008A](FICHA-PZ-008A.md), [PZ-014B](FICHA-PZ-014B.md) |
| G17 | Video real <=4 minutos con prueba visible de backend en Google Cloud | [PZ-015B](FICHA-PZ-015B.md) |
| G18 | Repositorio publico reproducible, arquitectura, pruebas y expediente saneado; publicacion con permiso especifico | [PZ-015B](FICHA-PZ-015B.md) |
| G19 | HQ separado de Business OS y contenido clave ES/EN fiel y versionado | [PZ-013C](FICHA-PZ-013C.md), [PZ-015B](FICHA-PZ-015B.md) |

## 8. Decisiones aprobadas que no se pierden

| Decision | Implementacion propuesta |
|---|---|
| DN-001 / DN-002 / PT-001 | Motor y gateway limitados, ledger durable, umbrales globales: 003D, 004A, 010A/B, 014A/B |
| DN-003 / PT-003 | Fuente real y control de archivos: 005A, 009A/B/C, 010D |
| DN-004 / DN-010 | Perfil unico, privados locales y purga: 010A/C/D; cloud saneada: 014A/B |
| DN-005 / DN-009 | Markdown unico, idioma y ES/EN: 003E, 013C, 015B |
| DN-006 / DN-007 / DN-011 | Plan y VBP con puertas separadas: 003F, 008A, 012A/B |
| DN-008 / DN-012 | Secuencia fija y no ejecutar iniciativa: 003D, 004B a 008A, gate 015A |
| DT-013 | Terminologia aprobacion humana/del usuario en todas las fichas y interfaces |
| PT-002 | Memoria confirmada, conflictiva bloqueada, correccion y borrado: 010C/D y 013B |
| PT-004 / PT-005 | Bloqueadores/100 puntos, 8 desarrollo + 2 holdout: 008A, 011A/B |
| PT-006 | P1 seleccionados y diferimientos explicitos en esta matriz, sin infraestructura por moda |
| PT-007 / PT-008 | Cinco agentes reales, cloud, expediente separado y entrega: 004A a 008A, 014A/B, 015A/B |

## 9. No afirmar "todo completado"

Esta matriz abarca todo el checklist documentalmente, pero solo las ejecuciones pueden demostrar cumplimiento.
Si un control no se puede implementar en su pieza, registrar brecha y proponer nueva decision/division; no borrar el control ni cambiar su prioridad.
Para la entrega real: evidencia por cada P0 aplicable, P1 seleccionado demostrado o diferimiento ratificado, gates satisfechos y aprobacion humana. Las fechas del contrato se verifican nuevamente antes de presentar.
