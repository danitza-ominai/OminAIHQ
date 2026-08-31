# PZ-003C - Contratos del recorrido, tareas y resultados

**Estado:** APROBADA_PARA_CONSTRUIR  
**Inicio de ejecucion:** PENDIENTE_DE_VERIFICAR_CONDICIONES_PREVIAS  
**Version de ficha:** 1  
**Implementacion:** NO_INICIADA_EN_ESTE_PAQUETE  
**Contrato rector:** CONTRATO-MVP-v1.md, 1.2-aprobada  
**Constructor inicial:** Antigravity  
**Correcciones:** Codex solo con autorizacion exacta; Copilot solo revisa.

> Aprobacion humana registrada el 30 de agosto de 2026 para Antigravity y esta lista cerrada de archivos. Verificar dependencias y condiciones previas antes de editar; no acredita implementacion ni aceptacion final.

## 1. Objetivo y resultado

Contratos complementarios versionados y validadores deterministas; no runtime ni agentes.

Problema que resuelve: contratos del recorrido, tareas y resultados como tramo acotado del recorrido del contrato; no amplifica la iniciativa cliente ni declara el MVP completo.

## 2. Fuentes obligatorias

- [Reglas comunes y decisiones tecnicas](00-REGLAS-Y-DECISIONES.md), completas.
- [Matriz de checklist y cobertura](01-MATRIZ-DE-COBERTURA.md), filas aplicables.
- [AGENTS.md](../AGENTS.md), [TEAM-WORKFLOW.md](../TEAM-WORKFLOW.md) y [contrato rector](../CONTRATO-MVP-v1.md).
- Contrato: `5.1-5.3`, `6`, `RF-005`, `RF-009`, `RF-010`, `RF-014`, `RF-028`, `RNF-013`, `CT-002`.
- `contracts/core/README.md`, schemas/ejemplos pertinentes y `state-machine.json`.
- Codigo, pruebas, fichas y aceptaciones de las dependencias siguientes; comprobar realidad actual, no asumirla por el mapa.

## 3. Dependencias y condicion previa

- [PZ-003B](../FICHA-PZ-003B-DECISION-HUMANA-DEL-PLAN.md#15-aceptacion-final-humana-de-pz-003b): COMPLETADA_Y_ACEPTADA por el usuario humano el 30 de agosto de 2026. Recorrido manual pendiente declarado; no cierra CT-009.

La dependencia de aceptacion de PZ-003B esta satisfecha. Concretar las interfaces exactas y el dominio de huella antes de iniciar construccion, dentro del alcance aprobado.

La ficha ya esta aprobada para su alcance y archivos enumerados. Si estos requisitos no estan satisfechos, se conserva esa aprobacion pero no se inicia la construccion. Concretar los valores pendientes y verificar las interfaces contra dependencias aceptadas; solo cambios de alcance/lista o permisos especificos requieren nueva autorizacion.

## 4. Archivos de fuente autorizados - lista cerrada

| Accion | Archivo | Limite |
|---|---|---|
| Crear | `contracts/runtime/task.schema.json` | Solo esta pieza; detenerse si ya existe |
| Crear | `contracts/runtime/agent-result.schema.json` | Solo esta pieza; detenerse si ya existe |
| Crear | `contracts/runtime/evidence.schema.json` | Solo esta pieza; detenerse si ya existe |
| Crear | `contracts/runtime/vbp.schema.json` | Solo esta pieza; detenerse si ya existe |
| Crear | `app/runtime_contracts.py` | Solo esta pieza; detenerse si ya existe |
| Crear | `tests/test_runtime_contracts.py` | Solo esta pieza; detenerse si ya existe |


Prohibidos: todos los archivos no enumerados, incluidos contratos nucleares, fichas, informes y pruebas previas no listadas. No crear un archivo auxiliar para eludir el perimetro.
Datos de prueba/ejecucion no son nuevos permisos de fuente: se rigen por el apartado 8 y por la autorizacion de una raiz aislada exacta.

## 5. Entradas y salidas

Entrada: Contrato rector y los 13 contratos nucleares aceptados; plan y registros reales de PZ-003A/B.

Salida: Contratos complementarios versionados y validadores deterministas; no runtime ni agentes.

Los errores, estados y registros nucleares mantienen los schemas aceptados. No convertir una propuesta textual en un cambio de estado autorizado.

## 6. Comportamiento requerido

1. Cerrar claves, tipos, estados, limites y referencias; reutilizar esquemas nucleares sin copiarlos ni ampliarlos.
2. Task incluye identidad/version, objetivo, agente, contexto autorizado, dependencias, criterios, herramientas, limites y categoria determinista/razonamiento; salida incluye todos los campos de 5.2.
3. Evidencia vincula claim, fuente, localizador, fechas, confianza justificada, restricciones y estado; distinguir inexistente, contradictoria y obsoleta.
4. El schema VBP describe datos internos de ensamblaje: no crea un segundo VBP JSON. El artefacto canonico sigue siendo un unico Markdown con manifest y 18 secciones.
5. Documentar dominio de huella sin autorreferencia, compatibilidad y resolucion de referencias; no aprobar ni ejecutar al validar.

## 7. Criterios de aceptacion y pruebas obligatorias

- [ ] AC-01: Metavalidar con Draft 2020-12 y fechas efectivas; ejemplos positivos por contrato.
- [ ] AC-02: Rechazar campos extra, CoT, claves/tipos invalidos, booleanos usados como numeros, fechas invalidas y referencias inexistentes.
- [ ] AC-03: Rechazar dependencias duplicadas/ciclicas, roles ajenos y limites ausentes/excedidos.
- [ ] AC-04: Detectar cada seccion VBP ausente y preservar PENDIENTE con responsable/motivo donde el contrato lo permite.
- [ ] AC-05: Conservar las 82 pruebas y hashes de contratos/core; probar ausencia de red y escrituras al importar.
- [ ] AC-COMUN-01: Regresion completa sin suprimir pruebas; comandos originales preservados.
- [ ] AC-COMUN-02: Entradas invalidas, actor no permitido, referencias cruzadas y fallos producen rechazo comprobable, sin efectos indebidos.
- [ ] AC-COMUN-03: Hashes demuestran solo cambios autorizados; sin secretos, CoT, residuos ni afirmaciones de madurez no probadas.
- [ ] AC-COMUN-04: Cada control del checklist reclamado tiene evidence_id, version, metodo y resultado; no basta la existencia del archivo.
- [ ] AC-COMUN-05: Revision independiente y aceptacion humana pendientes hasta realizarlas.

Pruebas propias propuestas:
- `python -B -m unittest discover -s tests -p test_runtime_contracts.py -v`

Ademas: `python -B -m unittest discover -s tests -v`. Diferenciar tests, subcasos, mocks y ejecuciones reales; no sumar una prueba manual no realizada al resultado.

## 8. Efectos, limites y seguridad

Perfil de efectos: **SIN_RED_NI_DATOS_PERSISTENTES**.

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
Actua como constructor inicial exclusivamente de PZ-003C: Contratos del recorrido, tareas y resultados.
Trabaja en OminAIHQ y lee completa PIEZAS-PENDIENTES/FICHA-PZ-003C.md, sus fuentes y PIEZAS-PENDIENTES/00-REGLAS-Y-DECISIONES.md.

La aprobacion humana de ESTA ficha version 1 y de su lista exacta de archivos consta en el apartado 11: autorizacion del 30 de agosto de 2026 para Antigravity.
No solicites de nuevo esa misma aprobacion. Antes de editar verifica las condiciones previas; esta autorizacion no acepta dependencias ni concede permisos sensibles pendientes o cambios de alcance.
Comprueba aceptacion de PZ-003B y todos los requisitos del apartado 3. No uses archivos futuros ausentes como si ya existieran.

Puedes crear exclusivamente: contracts/runtime/task.schema.json; contracts/runtime/agent-result.schema.json; contracts/runtime/evidence.schema.json; contracts/runtime/vbp.schema.json; app/runtime_contracts.py; tests/test_runtime_contracts.py.
Puedes modificar exclusivamente: ninguno.
No toques archivos fuera de esa lista, contratos/core ni fichas. No desarrolles otra pieza al terminar.

Presenta plan, dependencias disponibles y baseline antes de editar. Implementa solo el apartado 6 y demuestra los AC del apartado 7 con pruebas efectivas.
Respeta el perfil de efectos SIN_RED_NI_DATOS_PERSISTENTES; todo permiso de instalacion, datos, nube, gasto o publicacion debe estar aprobado de forma concreta.
Usa python -B, pruebas sinteticas y capturas en memoria/conversacion; no generes logs/residuos. No otorgues decisiones humanas reales desde pruebas automatizadas.
Devuelve evidencia verificable, limites y pendientes, nunca aprobacion final. Si necesitas otro archivo o decision, detente y pregunta.
```

## 11. Registro de aprobacion humana

```text
Pieza: PZ-003C
Version de ficha: 1
Decision: APROBADA
Autorizacion de construir: OTORGADA A ANTIGRAVITY PARA ESTA PIEZA
Inicio de ejecucion: CONDICIONADO A DEPENDENCIAS Y REQUISITOS DEL APARTADO 3
Dependencias aceptadas verificadas: PZ-003B, aceptacion humana del 30 de agosto de 2026 registrada en la seccion 15 de su ficha; recorrido manual pendiente declarado
Decisiones tecnicas del apartado 3: OPCIONES EXPLICITAS APROBADAS; VALORES NO DEFINIDOS PENDIENTES DE CONCRETAR
Archivos autorizados efectivamente - crear: contracts/runtime/task.schema.json; contracts/runtime/agent-result.schema.json; contracts/runtime/evidence.schema.json; contracts/runtime/vbp.schema.json; app/runtime_contracts.py; tests/test_runtime_contracts.py
Archivos autorizados efectivamente - modificar: NINGUNO
Datos/recursos/instalaciones/gasto autorizados: SIN NUEVOS PERMISOS ESPECIFICOS; MANTENER LOS LIMITES DEL APARTADO 8
Fecha y referencia de aprobacion: 2026-08-30; mensaje del usuario humano en esta conversacion
Declaracion: "todas las fichas quedan aprobadas y lo hare con el antigravity mas a eso me referia"
Aprobado por: usuario humano
Revision Chipi/Codex: PENDIENTE
Revision independiente Copilot: PENDIENTE
Aceptacion final: PENDIENTE
```
