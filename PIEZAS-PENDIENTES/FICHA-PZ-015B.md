# PZ-015B - Paquete de competencia y entrega humana

**Estado:** APROBADA_PARA_CONSTRUIR  
**Inicio de ejecucion:** PENDIENTE_DE_VERIFICAR_CONDICIONES_PREVIAS  
**Version de ficha:** 1  
**Implementacion:** NO_INICIADA_EN_ESTE_PAQUETE  
**Contrato rector:** CONTRATO-MVP-v1.md, 1.2-aprobada  
**Constructor inicial:** Antigravity  
**Correcciones:** Codex solo con autorizacion exacta; Copilot solo revisa.

> Aprobacion humana registrada el 30 de agosto de 2026 para Antigravity y esta lista cerrada de archivos. Verificar dependencias y condiciones previas antes de editar; no acredita implementacion ni aceptacion final.

## 1. Objetivo y resultado

Paquete documental para repo/video/Devpost; instrucciones de grabacion y entrega, no publicacion automatica.

Problema que resuelve: paquete de competencia y entrega humana como tramo acotado del recorrido del contrato; no amplifica la iniciativa cliente ni declara el MVP completo.

## 2. Fuentes obligatorias

- [Reglas comunes y decisiones tecnicas](00-REGLAS-Y-DECISIONES.md), completas.
- [Matriz de checklist y cobertura](01-MATRIZ-DE-COBERTURA.md), filas aplicables.
- [AGENTS.md](../AGENTS.md), [TEAM-WORKFLOW.md](../TEAM-WORKFLOW.md) y [contrato rector](../CONTRATO-MVP-v1.md).
- Contrato: `11.9`, `15.7`, `C.17`, `C.18`, `PT-008`, `CT-017`, `DN-009`.
- `contracts/core/README.md`, schemas/ejemplos pertinentes y `state-machine.json`.
- Codigo, pruebas, fichas y aceptaciones de las dependencias siguientes; comprobar realidad actual, no asumirla por el mapa.

## 3. Dependencias y condicion previa

- [PZ-015A](FICHA-PZ-015A.md) aceptada expresamente.

Verificar reglas/plazos vigentes en fuentes oficiales antes de presentar; la fecha contractual es historica, no una promesa actual. Autorizar grabacion/publicacion/envio aparte.

La ficha ya esta aprobada para su alcance y archivos enumerados. Si estos requisitos no estan satisfechos, se conserva esa aprobacion pero no se inicia la construccion. Concretar los valores pendientes y verificar las interfaces contra dependencias aceptadas; solo cambios de alcance/lista o permisos especificos requieren nueva autorizacion.

## 4. Archivos de fuente autorizados - lista cerrada

| Accion | Archivo | Limite |
|---|---|---|
| Crear | `competition/ENTREGA.md` | Solo esta pieza; detenerse si ya existe |
| Crear | `competition/ARQUITECTURA.md` | Solo esta pieza; detenerse si ya existe |
| Crear | `competition/GUION-VIDEO-ES-EN.md` | Solo esta pieza; detenerse si ya existe |
| Crear | `competition/LIMITACIONES-Y-EVIDENCIAS.md` | Solo esta pieza; detenerse si ya existe |
| Modificar | `README.md` | Solo integracion/cambio descrito aqui; conservar API y regresiones ajenas |

Prohibidos: todos los archivos no enumerados, incluidos contratos nucleares, fichas, informes y pruebas previas no listadas. No crear un archivo auxiliar para eludir el perimetro.
Datos de prueba/ejecucion no son nuevos permisos de fuente: se rigen por el apartado 8 y por la autorizacion de una raiz aislada exacta.

## 5. Entradas y salidas

Entrada: Evidencia de gate, ejecuciones reales, limites, metrica, diagrama y links revisados por el humano.

Salida: Paquete documental para repo/video/Devpost; instrucciones de grabacion y entrega, no publicacion automatica.

Los errores, estados y registros nucleares mantienen los schemas aceptados. No convertir una propuesta textual en un cambio de estado autorizado.

## 6. Comportamiento requerido

1. Actualizar README a estado real por version, instrucciones reproducibles, dependencias y datos saneados; conservar historia de demos.
2. Arquitectura textual verificable y especificacion para diagrama posterior, sin imagen inventada de infraestructura no desplegada.
3. Guion maximo cuatro minutos con prueba visible cloud; segmentos ES y #english y subtitulos ingles incorporados manualmente, no asumir YouTube automatico.
4. Separar OminAI HQ de iniciativa Business OS; explicar diferenciador sin prometer produccion/autonomia total.
5. Tabla implementado/simulado/propuesto/pendiente con evidencias y cifras reales; no ocultar fallos/limitaciones.
6. Repositorio publico, video y envio Devpost requieren permiso expreso adicional; no publicar secretos ni fuentes privadas. Grabacion/video binario fuera de esta lista hasta encargo autorizado.

## 7. Criterios de aceptacion y pruebas obligatorias

- [ ] AC-01: Cada afirmacion, metrica y captura propuesta apunta a evidencia real.
- [ ] AC-02: Guion cronometrado <=240 segundos y demo preparada <=150 para declarar lista.
- [ ] AC-03: README reproducible en entorno limpio autorizado; dependencias/licencias revisadas.
- [ ] AC-04: Auditoria de secretos/datos privados en archivos a publicar y URLs.
- [ ] AC-05: Revision humana de ingles, separaciones, limites, fuentes/reglas vigentes y autorizacion de entrega.
- [ ] AC-COMUN-01: Regresion completa sin suprimir pruebas; comandos originales preservados.
- [ ] AC-COMUN-02: Entradas invalidas, actor no permitido, referencias cruzadas y fallos producen rechazo comprobable, sin efectos indebidos.
- [ ] AC-COMUN-03: Hashes demuestran solo cambios autorizados; sin secretos, CoT, residuos ni afirmaciones de madurez no probadas.
- [ ] AC-COMUN-04: Cada control del checklist reclamado tiene evidence_id, version, metodo y resultado; no basta la existencia del archivo.
- [ ] AC-COMUN-05: Revision independiente y aceptacion humana pendientes hasta realizarlas.

Pruebas propias propuestas:
- Verificaciones operativas/documentales del apartado 7; no inventar pruebas unitarias para sustituir despliegue, video o revision humana.

Ademas: `python -B -m unittest discover -s tests -v`. Diferenciar tests, subcasos, mocks y ejecuciones reales; no sumar una prueba manual no realizada al resultado.

## 8. Efectos, limites y seguridad

Perfil de efectos: **DOCUMENTACION_LOCAL_SIN_PUBLICACION**.

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
Actua como constructor inicial exclusivamente de PZ-015B: Paquete de competencia y entrega humana.
Trabaja en OminAIHQ y lee completa PIEZAS-PENDIENTES/FICHA-PZ-015B.md, sus fuentes y PIEZAS-PENDIENTES/00-REGLAS-Y-DECISIONES.md.

La aprobacion humana de ESTA ficha version 1 y de su lista exacta de archivos consta en el apartado 11: autorizacion del 30 de agosto de 2026 para Antigravity.
No solicites de nuevo esa misma aprobacion. Antes de editar verifica las condiciones previas; esta autorizacion no acepta dependencias ni concede permisos sensibles pendientes o cambios de alcance.
Comprueba aceptacion de PZ-015A y todos los requisitos del apartado 3. No uses archivos futuros ausentes como si ya existieran.

Puedes crear exclusivamente: competition/ENTREGA.md; competition/ARQUITECTURA.md; competition/GUION-VIDEO-ES-EN.md; competition/LIMITACIONES-Y-EVIDENCIAS.md.
Puedes modificar exclusivamente: README.md.
No toques archivos fuera de esa lista, contratos/core ni fichas. No desarrolles otra pieza al terminar.

Presenta plan, dependencias disponibles y baseline antes de editar. Implementa solo el apartado 6 y demuestra los AC del apartado 7 con pruebas efectivas.
Respeta el perfil de efectos DOCUMENTACION_LOCAL_SIN_PUBLICACION; todo permiso de instalacion, datos, nube, gasto o publicacion debe estar aprobado de forma concreta.
Usa python -B, pruebas sinteticas y capturas en memoria/conversacion; no generes logs/residuos. No otorgues decisiones humanas reales desde pruebas automatizadas.
Devuelve evidencia verificable, limites y pendientes, nunca aprobacion final. Si necesitas otro archivo o decision, detente y pregunta.
```

## 11. Registro de aprobacion humana

```text
Pieza: PZ-015B
Version de ficha: 1
Decision: APROBADA
Autorizacion de construir: OTORGADA A ANTIGRAVITY PARA ESTA PIEZA
Inicio de ejecucion: CONDICIONADO A DEPENDENCIAS Y REQUISITOS DEL APARTADO 3
Dependencias aceptadas verificadas: PENDIENTE DE VERIFICACION; NO ACEPTADAS POR ESTE REGISTRO
Decisiones tecnicas del apartado 3: OPCIONES EXPLICITAS APROBADAS; VALORES NO DEFINIDOS PENDIENTES DE CONCRETAR
Archivos autorizados efectivamente - crear: competition/ENTREGA.md; competition/ARQUITECTURA.md; competition/GUION-VIDEO-ES-EN.md; competition/LIMITACIONES-Y-EVIDENCIAS.md
Archivos autorizados efectivamente - modificar: README.md
Datos/recursos/instalaciones/gasto autorizados: SIN NUEVOS PERMISOS ESPECIFICOS; MANTENER LOS LIMITES DEL APARTADO 8
Fecha y referencia de aprobacion: 2026-08-30; mensaje del usuario humano en esta conversacion
Declaracion: "todas las fichas quedan aprobadas y lo hare con el antigravity mas a eso me referia"
Aprobado por: usuario humano
Revision Chipi/Codex: PENDIENTE
Revision independiente Copilot: PENDIENTE
Aceptacion final: PENDIENTE
```
