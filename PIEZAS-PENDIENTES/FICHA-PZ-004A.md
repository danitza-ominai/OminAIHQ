# PZ-004A - Adaptador ADK y control de llamadas reales

**Estado:** APROBADA_PARA_CONSTRUIR  
**Inicio de ejecucion:** PENDIENTE_DE_VERIFICAR_CONDICIONES_PREVIAS  
**Version de ficha:** 1  
**Implementacion:** NO_INICIADA_EN_ESTE_PAQUETE  
**Contrato rector:** CONTRATO-MVP-v1.md, 1.2-aprobada  
**Constructor inicial:** Antigravity  
**Correcciones:** Codex solo con autorizacion exacta; Copilot solo revisa.

> Aprobacion humana registrada el 30 de agosto de 2026 para Antigravity y esta lista cerrada de archivos. Verificar dependencias y condiciones previas antes de editar; no acredita implementacion ni aceptacion final.

## 1. Objetivo y resultado

Adaptador injectable de Google ADK y Gemini segun perfil contractual; validacion, presupuesto, errores y trazas sanitizadas.

Problema que resuelve: adaptador adk y control de llamadas reales como tramo acotado del recorrido del contrato; no amplifica la iniciativa cliente ni declara el MVP completo.

## 2. Fuentes obligatorias

- [Reglas comunes y decisiones tecnicas](00-REGLAS-Y-DECISIONES.md), completas.
- [Matriz de checklist y cobertura](01-MATRIZ-DE-COBERTURA.md), filas aplicables.
- [AGENTS.md](../AGENTS.md), [TEAM-WORKFLOW.md](../TEAM-WORKFLOW.md) y [contrato rector](../CONTRATO-MVP-v1.md).
- Contrato: `5.1-5.4`, `10`, `11.3-11.4`, `11.9`, `RF-009`, `RF-023`, `RF-024`, `CT-002`, `PT-007`.
- `contracts/core/README.md`, schemas/ejemplos pertinentes y `state-machine.json`.
- Codigo, pruebas, fichas y aceptaciones de las dependencias siguientes; comprobar realidad actual, no asumirla por el mapa.

## 3. Dependencias y condicion previa

- [PZ-003F](FICHA-PZ-003F.md) aceptada expresamente.

Obligatorio ratificar SDK/versiones, ID de modelo disponible, modo de credenciales del entorno, limites de tokens y precio/techo de prueba mediante fuentes oficiales vigentes. No inferir permiso de red, instalacion o gasto.

La ficha ya esta aprobada para su alcance y archivos enumerados. Si estos requisitos no estan satisfechos, se conserva esa aprobacion pero no se inicia la construccion. Concretar los valores pendientes y verificar las interfaces contra dependencias aceptadas; solo cambios de alcance/lista o permisos especificos requieren nueva autorizacion.

## 4. Archivos de fuente autorizados - lista cerrada

| Accion | Archivo | Limite |
|---|---|---|
| Crear | `app/agent_gateway.py` | Solo esta pieza; detenerse si ya existe |
| Crear | `app/runtime_config.py` | Solo esta pieza; detenerse si ya existe |
| Crear | `tests/test_agent_gateway.py` | Solo esta pieza; detenerse si ya existe |
| Modificar | `pyproject.toml` | Solo integracion/cambio descrito aqui; conservar API y regresiones ajenas |

Prohibidos: todos los archivos no enumerados, incluidos contratos nucleares, fichas, informes y pruebas previas no listadas. No crear un archivo auxiliar para eludir el perimetro.
Datos de prueba/ejecucion no son nuevos permisos de fuente: se rigen por el apartado 8 y por la autorizacion de una raiz aislada exacta.

## 5. Entradas y salidas

Entrada: Contratos aceptados y configuracion no secreta aprobada del modelo/runtime.

Salida: Adaptador injectable de Google ADK y Gemini segun perfil contractual; validacion, presupuesto, errores y trazas sanitizadas.

Los errores, estados y registros nucleares mantienen los schemas aceptados. No convertir una propuesta textual en un cambio de estado autorizado.

## 6. Comportamiento requerido

1. Separar proveedor, herramientas, estado y agentes; sin migrar el nucleo al SDK.
2. Fallar cerrado si falta configuracion, credencial segura o dependencia; nunca sustituir llamada real por fixture.
3. Limitar tambien reintentos internos del SDK, timeout y tokens entrada/salida; los valores de tokens y precio verificado son requisitos de aprobacion, no numeros inventados aqui.
4. Reservar presupuesto antes de llamar y reconciliar uso real; USD 25 es total, no por agente ni por sesion.
5. Contrato de datos salientes: solo fragmentos saneados y autorizados; no enviar originales privados, secretos, expectativas holdout ni CoT.
6. Modificar pyproject solo para dependencias/versiones expresamente aprobadas; no instalar por el mero hecho de generar este documento.

## 7. Criterios de aceptacion y pruebas obligatorias

- [ ] AC-01: Proveedor simulado de prueba para exito, schema invalido, timeout, 429/transitorio y permiso denegado con limites.
- [ ] AC-02: Ausencia de credenciales/dependencia produce error controlado y ninguna llamada.
- [ ] AC-03: Comprobar 70/90/100 por ciento, 15 solicitudes y contadores de regeneracion/SDK.
- [ ] AC-04: Capturar parametros y datos enviados, sin secretos; salida rechaza CoT.
- [ ] AC-05: Una prueba real opt-in con datos saneados y permiso/gasto explicito; sin ella marcar integracion REAL_NO_VERIFICADA.
- [ ] AC-COMUN-01: Regresion completa sin suprimir pruebas; comandos originales preservados.
- [ ] AC-COMUN-02: Entradas invalidas, actor no permitido, referencias cruzadas y fallos producen rechazo comprobable, sin efectos indebidos.
- [ ] AC-COMUN-03: Hashes demuestran solo cambios autorizados; sin secretos, CoT, residuos ni afirmaciones de madurez no probadas.
- [ ] AC-COMUN-04: Cada control del checklist reclamado tiene evidence_id, version, metodo y resultado; no basta la existencia del archivo.
- [ ] AC-COMUN-05: Revision independiente y aceptacion humana pendientes hasta realizarlas.

Pruebas propias propuestas:
- `python -B -m unittest discover -s tests -p test_agent_gateway.py -v`

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
Actua como constructor inicial exclusivamente de PZ-004A: Adaptador ADK y control de llamadas reales.
Trabaja en OminAIHQ y lee completa PIEZAS-PENDIENTES/FICHA-PZ-004A.md, sus fuentes y PIEZAS-PENDIENTES/00-REGLAS-Y-DECISIONES.md.

La aprobacion humana de ESTA ficha version 1 y de su lista exacta de archivos consta en el apartado 11: autorizacion del 30 de agosto de 2026 para Antigravity.
No solicites de nuevo esa misma aprobacion. Antes de editar verifica las condiciones previas; esta autorizacion no acepta dependencias ni concede permisos sensibles pendientes o cambios de alcance.
Comprueba aceptacion de PZ-003F y todos los requisitos del apartado 3. No uses archivos futuros ausentes como si ya existieran.

Puedes crear exclusivamente: app/agent_gateway.py; app/runtime_config.py; tests/test_agent_gateway.py.
Puedes modificar exclusivamente: pyproject.toml.
No toques archivos fuera de esa lista, contratos/core ni fichas. No desarrolles otra pieza al terminar.

Presenta plan, dependencias disponibles y baseline antes de editar. Implementa solo el apartado 6 y demuestra los AC del apartado 7 con pruebas efectivas.
Respeta el perfil de efectos RED_Y_COSTO_SOLO_CON_AUTORIZACION_SEPARADA; todo permiso de instalacion, datos, nube, gasto o publicacion debe estar aprobado de forma concreta.
Usa python -B, pruebas sinteticas y capturas en memoria/conversacion; no generes logs/residuos. No otorgues decisiones humanas reales desde pruebas automatizadas.
Devuelve evidencia verificable, limites y pendientes, nunca aprobacion final. Si necesitas otro archivo o decision, detente y pregunta.
```

## 11. Registro de aprobacion humana

```text
Pieza: PZ-004A
Version de ficha: 1
Decision: APROBADA
Autorizacion de construir: OTORGADA A ANTIGRAVITY PARA ESTA PIEZA
Inicio de ejecucion: CONDICIONADO A DEPENDENCIAS Y REQUISITOS DEL APARTADO 3
Dependencias aceptadas verificadas: PENDIENTE DE VERIFICACION; NO ACEPTADAS POR ESTE REGISTRO
Decisiones tecnicas del apartado 3: OPCIONES EXPLICITAS APROBADAS; VALORES NO DEFINIDOS PENDIENTES DE CONCRETAR
Archivos autorizados efectivamente - crear: app/agent_gateway.py; app/runtime_config.py; tests/test_agent_gateway.py
Archivos autorizados efectivamente - modificar: pyproject.toml
Datos/recursos/instalaciones/gasto autorizados: SIN NUEVOS PERMISOS ESPECIFICOS; MANTENER LOS LIMITES DEL APARTADO 8
Fecha y referencia de aprobacion: 2026-08-30; mensaje del usuario humano en esta conversacion
Declaracion: "todas las fichas quedan aprobadas y lo hare con el antigravity mas a eso me referia"
Aprobado por: usuario humano
Revision Chipi/Codex: PENDIENTE
Revision independiente Copilot: PENDIENTE
Aceptacion final: PENDIENTE
```
