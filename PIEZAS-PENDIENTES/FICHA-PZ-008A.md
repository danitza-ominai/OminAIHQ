# PZ-008A - Governance independiente y cinco agentes integrados

**Estado:** APROBADA_PARA_CONSTRUIR  
**Inicio de ejecucion:** PENDIENTE_DE_VERIFICAR_CONDICIONES_PREVIAS  
**Version de ficha:** 1  
**Implementacion:** NO_INICIADA_EN_ESTE_PAQUETE  
**Contrato rector:** CONTRATO-MVP-v1.md, 1.2-aprobada  
**Constructor inicial:** Antigravity  
**Correcciones:** Codex solo con autorizacion exacta; Copilot solo revisa.

> Aprobacion humana registrada el 30 de agosto de 2026 para Antigravity y esta lista cerrada de archivos. Verificar dependencias y condiciones previas antes de editar; no acredita implementacion ni aceptacion final.

## 1. Objetivo y resultado

Dictamen independiente y recorrido real Chief -> Research -> Architect -> Planner -> Governance.

Problema que resuelve: governance independiente y cinco agentes integrados como tramo acotado del recorrido del contrato; no amplifica la iniciativa cliente ni declara el MVP completo.

## 2. Fuentes obligatorias

- [Reglas comunes y decisiones tecnicas](00-REGLAS-Y-DECISIONES.md), completas.
- [Matriz de checklist y cobertura](01-MATRIZ-DE-COBERTURA.md), filas aplicables.
- [AGENTS.md](../AGENTS.md), [TEAM-WORKFLOW.md](../TEAM-WORKFLOW.md) y [contrato rector](../CONTRATO-MVP-v1.md).
- Contrato: `5.9`, `11.8`, `RF-015`, `CT-007`, `CT-010`, `DN-007`.
- `contracts/core/README.md`, schemas/ejemplos pertinentes y `state-machine.json`.
- Codigo, pruebas, fichas y aceptaciones de las dependencias siguientes; comprobar realidad actual, no asumirla por el mapa.

## 3. Dependencias y condicion previa

- [PZ-007A](FICHA-PZ-007A.md) aceptada expresamente.

Las cinco integraciones reales requieren evidencia y presupuesto de prueba aprobado; sin ello no declarar CT-007 cumplido.

La ficha ya esta aprobada para su alcance y archivos enumerados. Si estos requisitos no estan satisfechos, se conserva esa aprobacion pero no se inicia la construccion. Concretar los valores pendientes y verificar las interfaces contra dependencias aceptadas; solo cambios de alcance/lista o permisos especificos requieren nueva autorizacion.

## 4. Archivos de fuente autorizados - lista cerrada

| Accion | Archivo | Limite |
|---|---|---|
| Crear | `app/governance_risk.py` | Solo esta pieza; detenerse si ya existe |
| Crear | `tests/test_governance_risk.py` | Solo esta pieza; detenerse si ya existe |
| Crear | `tests/test_five_agent_flow.py` | Solo esta pieza; detenerse si ya existe |
| Modificar | `app/hq_runtime.py` | Solo integracion/cambio descrito aqui; conservar API y regresiones ajenas |

Prohibidos: todos los archivos no enumerados, incluidos contratos nucleares, fichas, informes y pruebas previas no listadas. No crear un archivo auxiliar para eludir el perimetro.
Datos de prueba/ejecucion no son nuevos permisos de fuente: se rigen por el apartado 8 y por la autorizacion de una raiz aislada exacta.

## 5. Entradas y salidas

Entrada: VBP candidato, evidencias, trayectoria y resultados de validadores; nunca respuestas esperadas de evaluacion.

Salida: Dictamen independiente y recorrido real Chief -> Research -> Architect -> Planner -> Governance.

Los errores, estados y registros nucleares mantienen los schemas aceptados. No convertir una propuesta textual en un cambio de estado autorizado.

## 6. Comportamiento requerido

1. Governance lee y reporta, no corrige VBP ni se autoaprueba.
2. Componer puntuacion determinista de vbp_validation con hallazgos cualitativos fundamentados; no sustituir bloqueadores por opinion LLM.
3. Una invocacion separada por rol; respetar los 15 requests y 2 intentos totales por tarea.
4. Congelar VBP y version evaluados; cualquier cambio material invalida dictamen/puerta afectados.
5. Fallo de un modelo se muestra y pausa; prohibido reemplazo ficticio en ejecucion REAL.

## 7. Criterios de aceptacion y pruebas obligatorias

- [ ] AC-01: PASA, PASA_CON_CONDICIONES y NO_PASA con matriz requisito/resultado.
- [ ] AC-02: NO_PASA impide aprobacion ordinaria; Governance no puede consumir aprobaciones.
- [ ] AC-03: Comprobar que el evaluador no modifica entrada ni consulta expectativas holdout.
- [ ] AC-04: Secuencia real opt-in de los cinco roles con trazas sanitizadas, sin agentes simultaneos.
- [ ] AC-05: Inyectar fallo de cada rol; no avanzar con salida ficticia.
- [ ] AC-COMUN-01: Regresion completa sin suprimir pruebas; comandos originales preservados.
- [ ] AC-COMUN-02: Entradas invalidas, actor no permitido, referencias cruzadas y fallos producen rechazo comprobable, sin efectos indebidos.
- [ ] AC-COMUN-03: Hashes demuestran solo cambios autorizados; sin secretos, CoT, residuos ni afirmaciones de madurez no probadas.
- [ ] AC-COMUN-04: Cada control del checklist reclamado tiene evidence_id, version, metodo y resultado; no basta la existencia del archivo.
- [ ] AC-COMUN-05: Revision independiente y aceptacion humana pendientes hasta realizarlas.

Pruebas propias propuestas:
- `python -B -m unittest discover -s tests -p test_governance_risk.py -v`
- `python -B -m unittest discover -s tests -p test_five_agent_flow.py -v`

Ademas: `python -B -m unittest discover -s tests -v`. Diferenciar tests, subcasos, mocks y ejecuciones reales; no sumar una prueba manual no realizada al resultado.

## 8. Efectos, limites y seguridad

Perfil de efectos: **RED_Y_COSTO_SOLO_CON_AUTORIZACION_SEPARADA**.

Se heredan integramente los limites numericos y de datos de [la guia](00-REGLAS-Y-DECISIONES.md#5-limites-del-producto-no-nuevos-presupuestos-por-ficha).
Una ficha no renueva los USD 25, los intentos ni las aprobaciones. No bucles ilimitados, fallback ficticio, recursividad ni paralelismo de especialistas.
Fuentes/modificaciones son solo las enumeradas. Si hace falta IO, servidor, proceso de prueba, modelo o cloud, registrar antes del permiso: ruta/recursos, datos, comando, limite y forma segura de detener/revertir.
No instalar, enviar datos, desplegar, publicar o eliminar solo por leer este prompt. Las pruebas destructivas solo operan con datos sinteticos en raiz aislada expresamente autorizada.
Una conversacion de construccion, sin delegacion; objetivo 45 minutos, detenerse y reportar si requiere ampliar/dividir el encargo. Cada correccion posterior tiene aprobacion propia.

## 9. Evidencia de entrega y detenciones

Entregar en conversacion: archivos exactos, resumen por AC, comandos/codigos/salidas, conteo real de pruebas, hashes antes/despues, residuos, errores, limites y pendientes.
Antes de editar capturar inventario completo. No crear test_output.log ni informe adicional fuera de lista.
Detenerse si falta aprobacion, dependencia aceptada, decision tecnica, presupuesto, fuente/permiso o si una ruta a crear ya existe. No corregir contratos aceptados desde esta pieza.
Una prueba REAL pendiente se declara asi, aunque todas las pruebas offline pasen. No aprobar la pieza ni el MVP en nombre del usuario.

## 10. Prompt para Antigravity - verificar condiciones previas

```text
Actua como constructor inicial exclusivamente de PZ-008A: Governance independiente y cinco agentes integrados.
Trabaja en OminAIHQ y lee completa PIEZAS-PENDIENTES/FICHA-PZ-008A.md, sus fuentes y PIEZAS-PENDIENTES/00-REGLAS-Y-DECISIONES.md.

La aprobacion humana de ESTA ficha version 1 y de su lista exacta de archivos consta en el apartado 11: autorizacion del 30 de agosto de 2026 para Antigravity.
No solicites de nuevo esa misma aprobacion. Antes de editar verifica las condiciones previas; esta autorizacion no acepta dependencias ni concede permisos sensibles pendientes o cambios de alcance.
Comprueba aceptacion de PZ-007A y todos los requisitos del apartado 3. No uses archivos futuros ausentes como si ya existieran.

Puedes crear exclusivamente: app/governance_risk.py; tests/test_governance_risk.py; tests/test_five_agent_flow.py.
Puedes modificar exclusivamente: app/hq_runtime.py.
No toques archivos fuera de esa lista, contratos/core ni fichas. No desarrolles otra pieza al terminar.

Presenta plan, dependencias disponibles y baseline antes de editar. Implementa solo el apartado 6 y demuestra los AC del apartado 7 con pruebas efectivas.
Respeta el perfil de efectos RED_Y_COSTO_SOLO_CON_AUTORIZACION_SEPARADA; todo permiso de instalacion, datos, nube, gasto o publicacion debe estar aprobado de forma concreta.
Usa python -B, pruebas sinteticas y capturas en memoria/conversacion; no generes logs/residuos. No otorgues decisiones humanas reales desde pruebas automatizadas.
Devuelve evidencia verificable, limites y pendientes, nunca aprobacion final. Si necesitas otro archivo o decision, detente y pregunta.
```

## 11. Registro de aprobacion humana

```text
Pieza: PZ-008A
Version de ficha: 1
Decision: APROBADA
Autorizacion de construir: OTORGADA A ANTIGRAVITY PARA ESTA PIEZA
Inicio de ejecucion: CONDICIONADO A DEPENDENCIAS Y REQUISITOS DEL APARTADO 3
Dependencias aceptadas verificadas: PENDIENTE DE VERIFICACION; NO ACEPTADAS POR ESTE REGISTRO
Decisiones tecnicas del apartado 3: OPCIONES EXPLICITAS APROBADAS; VALORES NO DEFINIDOS PENDIENTES DE CONCRETAR
Archivos autorizados efectivamente - crear: app/governance_risk.py; tests/test_governance_risk.py; tests/test_five_agent_flow.py
Archivos autorizados efectivamente - modificar: app/hq_runtime.py
Datos/recursos/instalaciones/gasto autorizados: SIN NUEVOS PERMISOS ESPECIFICOS; MANTENER LOS LIMITES DEL APARTADO 8
Fecha y referencia de aprobacion: 2026-08-30; mensaje del usuario humano en esta conversacion
Declaracion: "todas las fichas quedan aprobadas y lo hare con el antigravity mas a eso me referia"
Aprobado por: usuario humano
Revision Chipi/Codex: PENDIENTE
Revision independiente Copilot: PENDIENTE
Aceptacion final: PENDIENTE
```
