# PZ-014A - Preparacion de despliegue y datos saneados

**Estado:** APROBADA_PARA_CONSTRUIR  
**Inicio de ejecucion:** PENDIENTE_DE_VERIFICAR_CONDICIONES_PREVIAS  
**Version de ficha:** 1  
**Implementacion:** NO_INICIADA_EN_ESTE_PAQUETE  
**Contrato rector:** CONTRATO-MVP-v1.md, 1.2-aprobada  
**Constructor inicial:** Antigravity  
**Correcciones:** Codex solo con autorizacion exacta; Copilot solo revisa.

> Aprobacion humana registrada el 30 de agosto de 2026 para Antigravity y esta lista cerrada de archivos. Verificar dependencias y condiciones previas antes de editar; no acredita implementacion ni aceptacion final.

## 1. Objetivo y resultado

Configuracion reproducible de Cloud Run y adaptadores Firestore/Cloud Storage; pruebas locales/emuladas, sin despliegue.

Problema que resuelve: preparacion de despliegue y datos saneados como tramo acotado del recorrido del contrato; no amplifica la iniciativa cliente ni declara el MVP completo.

## 2. Fuentes obligatorias

- [Reglas comunes y decisiones tecnicas](00-REGLAS-Y-DECISIONES.md), completas.
- [Matriz de checklist y cobertura](01-MATRIZ-DE-COBERTURA.md), filas aplicables.
- [AGENTS.md](../AGENTS.md), [TEAM-WORKFLOW.md](../TEAM-WORKFLOW.md) y [contrato rector](../CONTRATO-MVP-v1.md).
- Contrato: `11.2`, `11.4`, `11.9`, `PT-007`, `PT-008`, `CT-014`, `CT-015`, `RNF-007`.
- `contracts/core/README.md`, schemas/ejemplos pertinentes y `state-machine.json`.
- Codigo, pruebas, fichas y aceptaciones de las dependencias siguientes; comprobar realidad actual, no asumirla por el mapa.

## 3. Dependencias y condicion previa

- [PZ-013C](FICHA-PZ-013C.md) aceptada expresamente.

Revalidar reglas oficiales/modelo/precios antes de iniciar construccion; elegir proyecto/region/identidad y control del operador. Cloud APIs y dependencias requieren permiso; esta pieza NO despliega.

La ficha ya esta aprobada para su alcance y archivos enumerados. Si estos requisitos no estan satisfechos, se conserva esa aprobacion pero no se inicia la construccion. Concretar los valores pendientes y verificar las interfaces contra dependencias aceptadas; solo cambios de alcance/lista o permisos especificos requieren nueva autorizacion.

## 4. Archivos de fuente autorizados - lista cerrada

| Accion | Archivo | Limite |
|---|---|---|
| Crear | `Dockerfile` | Solo esta pieza; detenerse si ya existe |
| Crear | `.dockerignore` | Solo esta pieza; detenerse si ya existe |
| Crear | `deploy/cloudrun.example.yaml` | Solo esta pieza; detenerse si ya existe |
| Crear | `app/cloud_demo_repository.py` | Solo esta pieza; detenerse si ya existe |
| Crear | `tests/test_cloud_demo_policy.py` | Solo esta pieza; detenerse si ya existe |
| Modificar | `app/runtime_config.py` | Solo integracion/cambio descrito aqui; conservar API y regresiones ajenas |
| Modificar | `app/http_api.py` | Solo integracion/cambio descrito aqui; conservar API y regresiones ajenas |
| Modificar | `pyproject.toml` | Solo integracion/cambio descrito aqui; conservar API y regresiones ajenas |

Prohibidos: todos los archivos no enumerados, incluidos contratos nucleares, fichas, informes y pruebas previas no listadas. No crear un archivo auxiliar para eludir el perimetro.
Datos de prueba/ejecucion no son nuevos permisos de fuente: se rigen por el apartado 8 y por la autorizacion de una raiz aislada exacta.

## 5. Entradas y salidas

Entrada: Aplicacion local estable, expediente saneado aprobado y perfil de competencia del contrato.

Salida: Configuracion reproducible de Cloud Run y adaptadores Firestore/Cloud Storage; pruebas locales/emuladas, sin despliegue.

Los errores, estados y registros nucleares mantienen los schemas aceptados. No convertir una propuesta textual en un cambio de estado autorizado.

## 6. Comportamiento requerido

1. Solo datos de demo saneados; nunca sincronizar DB privada, originales, memoria personal o credenciales.
2. Cloud Run min=0/max=1; cupo global 5 ejecuciones diarias con transaccion durable, no contador por visitante/proceso.
3. Servicio del modelo via identidad segura del entorno; minimo privilegio, sin claves en imagen/prompts.
4. Configuracion de modelo/version/region/proyecto son parametros aprobados, no IDs inventados.
5. Crear imagen/configuracion no equivale a nube operativa. Falta de permisos/configuracion detiene, no usa fallback ficticio.
6. Demo publica solo mision fija, sin uploads privados/acciones externas; publico no suplanta aprobacion de operador. API separa exposicion publica y administrativa.

## 7. Criterios de aceptacion y pruebas obligatorias

- [ ] AC-01: Escaneo de contexto/imagen para excluir privados, bases, secretos y directorios de usuario.
- [ ] AC-02: Prueba de repositorio cloud contra contrato con dobles/emulador rotulados, no llamada real implícita.
- [ ] AC-03: Quinta ejecucion admitida; sexta solo ejemplo lectura; reinicio no reinicia cuota.
- [ ] AC-04: Plan de gasto global y umbrales aplicados tambien en cloud.
- [ ] AC-05: Rutas administrativas no disponibles al publico ni herramientas generativas.
- [ ] AC-COMUN-01: Regresion completa sin suprimir pruebas; comandos originales preservados.
- [ ] AC-COMUN-02: Entradas invalidas, actor no permitido, referencias cruzadas y fallos producen rechazo comprobable, sin efectos indebidos.
- [ ] AC-COMUN-03: Hashes demuestran solo cambios autorizados; sin secretos, CoT, residuos ni afirmaciones de madurez no probadas.
- [ ] AC-COMUN-04: Cada control del checklist reclamado tiene evidence_id, version, metodo y resultado; no basta la existencia del archivo.
- [ ] AC-COMUN-05: Revision independiente y aceptacion humana pendientes hasta realizarlas.

Pruebas propias propuestas:
- `python -B -m unittest discover -s tests -p test_cloud_demo_policy.py -v`

Ademas: `python -B -m unittest discover -s tests -v`. Diferenciar tests, subcasos, mocks y ejecuciones reales; no sumar una prueba manual no realizada al resultado.

## 8. Efectos, limites y seguridad

Perfil de efectos: **CONFIGURACION_LOCAL_SIN_MUTACIONES_CLOUD**.

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
Actua como constructor inicial exclusivamente de PZ-014A: Preparacion de despliegue y datos saneados.
Trabaja en OminAIHQ y lee completa PIEZAS-PENDIENTES/FICHA-PZ-014A.md, sus fuentes y PIEZAS-PENDIENTES/00-REGLAS-Y-DECISIONES.md.

La aprobacion humana de ESTA ficha version 1 y de su lista exacta de archivos consta en el apartado 11: autorizacion del 30 de agosto de 2026 para Antigravity.
No solicites de nuevo esa misma aprobacion. Antes de editar verifica las condiciones previas; esta autorizacion no acepta dependencias ni concede permisos sensibles pendientes o cambios de alcance.
Comprueba aceptacion de PZ-013C y todos los requisitos del apartado 3. No uses archivos futuros ausentes como si ya existieran.

Puedes crear exclusivamente: Dockerfile; .dockerignore; deploy/cloudrun.example.yaml; app/cloud_demo_repository.py; tests/test_cloud_demo_policy.py.
Puedes modificar exclusivamente: app/runtime_config.py; app/http_api.py; pyproject.toml.
No toques archivos fuera de esa lista, contratos/core ni fichas. No desarrolles otra pieza al terminar.

Presenta plan, dependencias disponibles y baseline antes de editar. Implementa solo el apartado 6 y demuestra los AC del apartado 7 con pruebas efectivas.
Respeta el perfil de efectos CONFIGURACION_LOCAL_SIN_MUTACIONES_CLOUD; todo permiso de instalacion, datos, nube, gasto o publicacion debe estar aprobado de forma concreta.
Usa python -B, pruebas sinteticas y capturas en memoria/conversacion; no generes logs/residuos. No otorgues decisiones humanas reales desde pruebas automatizadas.
Devuelve evidencia verificable, limites y pendientes, nunca aprobacion final. Si necesitas otro archivo o decision, detente y pregunta.
```

## 11. Registro de aprobacion humana

```text
Pieza: PZ-014A
Version de ficha: 1
Decision: APROBADA
Autorizacion de construir: OTORGADA A ANTIGRAVITY PARA ESTA PIEZA
Inicio de ejecucion: CONDICIONADO A DEPENDENCIAS Y REQUISITOS DEL APARTADO 3
Dependencias aceptadas verificadas: PENDIENTE DE VERIFICACION; NO ACEPTADAS POR ESTE REGISTRO
Decisiones tecnicas del apartado 3: OPCIONES EXPLICITAS APROBADAS; VALORES NO DEFINIDOS PENDIENTES DE CONCRETAR
Archivos autorizados efectivamente - crear: Dockerfile; .dockerignore; deploy/cloudrun.example.yaml; app/cloud_demo_repository.py; tests/test_cloud_demo_policy.py
Archivos autorizados efectivamente - modificar: app/runtime_config.py; app/http_api.py; pyproject.toml
Datos/recursos/instalaciones/gasto autorizados: SIN NUEVOS PERMISOS ESPECIFICOS; MANTENER LOS LIMITES DEL APARTADO 8
Fecha y referencia de aprobacion: 2026-08-30; mensaje del usuario humano en esta conversacion
Declaracion: "todas las fichas quedan aprobadas y lo hare con el antigravity mas a eso me referia"
Aprobado por: usuario humano
Revision Chipi/Codex: PENDIENTE
Revision independiente Copilot: PENDIENTE
Aceptacion final: PENDIENTE
```
