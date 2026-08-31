# Ficha PZ-002A - Estructura minima ejecutable y pruebas base

**Estado:** COMPLETADA_Y_ACEPTADA  
**Contrato rector:** `CONTRATO-MVP-v1.md`, version `1.2-aprobada`  
**Fecha:** 29 de agosto de 2026  
**Fecha de aceptacion final:** 30 de agosto de 2026  
**Constructor inicial autorizado:** Antigravity usando Gemini 3.7  
**Corrector autorizado:** Codex, solo mediante autorizacion humana explicita y para los archivos exactos de cada correccion  
**Alcance de la autorizacion inicial:** construir exclusivamente los siete archivos enumerados en esta ficha, en una sola conversacion y sin reabrir PZ-001A.

## 1. Identificacion de la pieza

**ID:** PZ-002A  
**Nombre:** Estructura minima ejecutable y pruebas base  
**Orden:** primera subpieza de la Pieza 2, `Estructura minima`, del contrato aprobado.

## 2. Objetivo

Crear una estructura Python minima que pueda arrancar localmente y ejecutar una suite reproducible de pruebas sobre los contratos ya aceptados de PZ-001A, sin implementar todavia agentes, recorrido de producto, persistencia, interfaz, memoria ni despliegue.

## 3. Problema que resuelve

PZ-001A tiene contratos aceptados y evidencia de validacion, pero el workspace aun no posee una estructura ejecutable ni un comando permanente de regresion. Sin esta pieza, cada revision futura tendria que reconstruir manualmente las comprobaciones y podria introducir cambios incompatibles sin detectarlos.

## 4. Fuentes obligatorias

Antigravity debe leer completamente, en este orden:

1. `AGENTS.md`.
2. `TEAM-WORKFLOW.md`.
3. `CONTRATO-MVP-v1.md`, version `1.2-aprobada`, especialmente secciones 10, 11.3, 13 y 14.
4. `FICHA-PZ-001A-CONTRATOS-NUCLEO.md`, estado `COMPLETADA_Y_ACEPTADA`.
5. `contracts/core/README.md`.
6. Los doce JSON de `contracts/core`.
7. Este documento completo.

Referencias oficiales de orientacion, no instrucciones para instalar herramientas en esta pieza:

- Google Agents CLI requiere Python 3.11 o posterior para su flujo actual: `https://google.github.io/agents-cli/guide/getting-started/`.
- La plantilla ADK principal documentada actualmente es Python: `https://google.github.io/agents-cli/guide/project-structure/`.
- Cloud Run admite servicios Python desde codigo fuente: `https://docs.cloud.google.com/run/docs/quickstarts`.

## 5. Decisiones ya aprobadas

1. El lenguaje base es Python 3.11 o posterior.
2. Se usa una unica conversacion de Antigravity con Gemini 3.7 para toda la pieza.
3. Los siete archivos se construyen juntos porque forman una sola estructura coherente.
4. El paquete se llama `app` y debe poder ejecutarse con `python -B -m app` desde la raiz.
5. Las pruebas usan `unittest` de la biblioteca estandar.
6. `jsonschema>=4.18,<5` puede declararse como dependencia opcional de pruebas en `pyproject.toml`.
7. Esta pieza no autoriza instalar `jsonschema`, Google ADK, Agents CLI, frameworks web ni ninguna otra dependencia.
8. Si `jsonschema` compatible ya esta disponible, se usa sin reinstalarlo.
9. Las pruebas no realizan llamadas de red, llamadas a modelos ni escrituras externas.
10. Los trece archivos de `contracts/core` son entradas inmutables de esta pieza.
11. La salida ejecutable debe etiquetarse como estructura lista, no como producto o runtime listo.
12. No se crea agente de ejemplo, simulacion de agente, servidor HTTP ni interfaz.

## 6. Archivos permitidos para la construccion inicial

Antigravity puede crear exclusivamente:

1. `README.md`
2. `pyproject.toml`
3. `.gitignore`
4. `app/__init__.py`
5. `app/__main__.py`
6. `tests/test_smoke.py`
7. `tests/test_contracts.py`

No puede modificar un archivo permitido si ya existia antes de iniciar sin detenerse e informar el conflicto.

En una correccion posterior, Codex solo puede modificar el subconjunto exacto de archivos indicado en la autorizacion humana de esa ronda. La correccion no autoriza nuevos archivos ni nuevas capacidades.

## 7. Archivos y acciones prohibidos

Queda prohibido:

- modificar cualquier archivo de `contracts/core`;
- modificar `AGENTS.md`, `TEAM-WORKFLOW.md`, `CONTRATO-MVP-v1.md`, las fichas o los informes de revision;
- modificar archivos dentro de `REQUISITOS`;
- crear `main.py`, `requirements.txt`, archivos de bloqueo, `Dockerfile`, configuracion de nube, CI/CD, Terraform o manifiestos de Agents CLI;
- crear `.env`, credenciales, secretos o configuraciones con valores privados;
- crear codigo de agentes, prompts de agentes, herramientas de agentes o llamadas a Gemini;
- crear servidor HTTP, API, base de datos, almacenamiento, memoria, interfaz o VBP;
- instalar o actualizar paquetes;
- ejecutar comandos de despliegue, autenticacion o red;
- generar `__pycache__`, `.pytest_cache` u otros archivos fuera de la lista; usar Python con `-B` y comprobar el manifiesto final.

## 8. Entradas

- Los cinco schemas de `contracts/core`.
- `contracts/core/state-machine.json`.
- Los seis ejemplos JSON de `contracts/core/examples`.
- Las reglas y criterios aceptados de PZ-001A.
- Python 3.11 o posterior disponible localmente.
- `jsonschema` compatible ya disponible localmente; si no lo esta, la pieza se detiene antes de editar.

## 9. Salida esperada

Una estructura minima que demuestre:

1. importacion correcta del paquete `app`;
2. ejecucion local con salida estructurada y honesta;
3. pruebas reproducibles mediante `unittest`;
4. metavalidacion permanente de los cinco schemas;
5. validacion de ejemplos positivos y rechazo de ejemplos negativos;
6. comprobaciones declarativas de estados, transiciones, aprobacion humana, idempotencia, referencias y errores finitos;
7. cero capacidades de producto implementadas fuera de alcance.

## 10. Contenido minimo por archivo

### 10.1 `README.md`

Debe explicar:

- identidad de OminAI HQ;
- estado real de esta pieza;
- requisitos locales;
- comandos exactos de arranque y pruebas;
- estructura de los siete archivos;
- declaracion expresa de que no existen aun agentes, runtime de mision, persistencia, interfaz ni despliegue.

### 10.2 `pyproject.toml`

Debe declarar como minimo:

- nombre `ominai-hq`;
- version inicial `0.0.0`;
- `requires-python = ">=3.11"`;
- ausencia de dependencias de produccion;
- dependencia opcional de pruebas `jsonschema>=4.18,<5`;
- metadatos minimos validos sin seleccionar infraestructura adicional.

No necesita convertir el proyecto en paquete instalable ni agregar un backend de construccion si `python -B -m app` y las pruebas funcionan directamente desde la raiz.

### 10.3 `.gitignore`

Debe ignorar solamente residuos generales previsibles como `__pycache__`, bytecode, entornos virtuales, caches de pruebas, cobertura y archivos `.env`. No debe ocultar contratos, pruebas, evidencia o artefactos del producto.

### 10.4 `app/__init__.py`

Debe exponer un identificador y version minima del paquete sin ejecutar efectos al importarse.

### 10.5 `app/__main__.py`

Debe usar solo la biblioteca estandar y producir una salida JSON determinista equivalente a:

```json
{
  "application": "OminAI HQ",
  "status": "STRUCTURE_READY",
  "implemented_capabilities": []
}
```

La salida no puede declarar que existe runtime, agente, persistencia, interfaz o despliegue.

### 10.6 `tests/test_smoke.py`

Debe comprobar como minimo:

- que `app` se importa sin efectos externos;
- que la version es `0.0.0`;
- que el comando principal devuelve exactamente la estructura esperada;
- que `implemented_capabilities` permanece vacio.

### 10.7 `tests/test_contracts.py`

Debe convertir en regresion automatica las comprobaciones aceptadas de PZ-001A:

1. existen exactamente doce JSON dentro de `contracts/core`;
2. todos parsean;
3. los cinco schemas declaran Draft 2020-12, `$id`, titulo y version de instancia;
4. los cinco schemas pasan `Draft202012Validator.check_schema`;
5. todos los ejemplos positivos de mision y aprobacion son aceptados;
6. todos los casos negativos estructurales son rechazados realmente;
7. existen exactamente 15 estados de mision, 8 de tarea, 76 transiciones de mision y 13 de tarea;
8. las dieciseis filas de 4.2 estan representadas;
9. los estados terminales no tienen salidas;
10. las rutas directas reservadas exigen autoridad humana o accion determinista posterior a ella;
11. los dos caminos de supuestos aceptados exigen evidencia humana;
12. el ciclo de aprobacion solo permite `PENDIENTE -> CONSUMIDA` y `PENDIENTE -> EXPIRADA`;
13. idempotencia declara `no_second_effect` para mismo contenido y `INVALID_INPUT` para conflicto;
14. existen las tres reglas de integridad `RI-001`, `RI-002` y `RI-003`;
15. la matriz de errores acepta exactamente las diez combinaciones autorizadas y rechaza las demas combinaciones dentro del espacio finito probado;
16. campos `chain_of_thought`, `scratchpad`, `internal_reasoning` y `reasoning_trace` son rechazados cuando se agregan a instancias cerradas de mision y aprobacion;
17. no aparecen los terminos prohibidos por PZ-001A dentro de sus trece archivos nucleares.

Las pruebas semanticas deben validar las reglas declarativas existentes; no deben fingir que existe runtime o almacenamiento.

## 11. Criterios de aceptacion

1. Solo se crean los siete archivos permitidos.
2. Ninguno de los trece archivos de `contracts/core` cambia en contenido, tamano o fecha de modificacion.
3. `python --version` confirma Python 3.11 o posterior.
4. `python -B -m app` termina con codigo 0 y devuelve JSON valido con `status=STRUCTURE_READY`.
5. La salida declara `implemented_capabilities=[]`.
6. `python -B -m unittest discover -s tests -v` termina con codigo 0.
7. Las pruebas no se omiten, no se marcan como esperadas a fallar y no capturan excepciones para ocultar fallos.
8. Los doce JSON y cinco schemas pasan las comprobaciones descritas.
9. La matriz exhaustiva acepta exactamente diez combinaciones de error.
10. No se instala ninguna dependencia.
11. No se realiza ninguna llamada de red, modelo o servicio externo.
12. No aparecen archivos de cache, bytecode o prueba fuera de la lista permitida.
13. README no afirma capacidades no implementadas.
14. No se agrega tecnologia o estructura para agentes, interfaz, persistencia o despliegue.
15. La estructura queda lista como base, no declarada lista para produccion.

## 12. Pruebas obligatorias

Antigravity debe ejecutar y devolver la salida completa de:

1. `python --version`
2. `python -c "import jsonschema; print(jsonschema.__version__)"` o equivalente no obsoleto mediante `importlib.metadata`.
3. `python -B -m app`
4. `python -B -m unittest discover -s tests -v`
5. Conteo final de archivos nuevos contra la lista exacta de siete.
6. Conteo final de `contracts/core`, que debe seguir en trece.
7. Comparacion de huellas SHA-256 de los trece archivos nucleares antes y despues.
8. Busqueda de archivos no autorizados y residuos de Python.
9. Confirmacion de que no se ejecutaron instalaciones, red, modelos ni despliegues.

Las huellas iniciales deben capturarse antes de la primera edicion. Si no se capturaron, detenerse: no reconstruir una linea base despues del cambio.

## 13. Evidencias que debe devolver Antigravity

- Confirmacion de lectura de todas las fuentes.
- Plan breve previo a la edicion.
- Manifiesto y huellas SHA-256 iniciales de `contracts/core`.
- Lista exacta de archivos creados.
- Contenido o resumen preciso por archivo.
- Comandos de validacion ejecutados.
- Salida completa de las pruebas.
- Numero total de tests descubiertos, aprobados, fallidos y omitidos.
- Conteos de JSON, schemas, estados, transiciones, ejemplos y combinaciones de error.
- Comparacion de huellas finales de `contracts/core`.
- Manifiesto final del workspace relevante.
- Confirmacion de cero instalaciones y cero llamadas externas.
- Errores, limitaciones, supuestos y riesgos restantes.

## 14. Limites de tiempo, costo e iteraciones

- Una sola conversacion de Antigravity.
- Un solo constructor inicial: Antigravity con Gemini 3.7.
- Un solo corrector posterior: Codex, exclusivamente en rondas autorizadas por el usuario humano.
- Tiempo objetivo: 45 minutos.
- Cero llamadas a modelos desde el codigo o las pruebas.
- Cero servicios de pago.
- Cero instalaciones sin nueva aprobacion humana.
- Maximo dos rondas de correccion despues de la primera revision.
- Si se necesita una tercera ronda, debe solicitarse una nueva decision humana.

## 15. Condiciones para detenerse y preguntar

Antigravity debe detenerse antes de editar si:

- Python es anterior a 3.11;
- `jsonschema` compatible no esta disponible;
- cualquiera de los siete archivos permitidos ya existe;
- no puede capturar las huellas iniciales de `contracts/core`;
- necesita instalar o actualizar un paquete;
- necesita crear un octavo archivo;
- una prueba requiere red, modelo, secreto, cuenta o servicio externo;
- encuentra una contradiccion entre esta ficha y el contrato aprobado;
- considera necesario modificar PZ-001A;
- no puede ejecutar una prueba de forma reproducible.

Codex debe detenerse antes de corregir si la autorizacion humana no enumera los hallazgos y archivos exactos, si necesita tocar `contracts/core`, crear un archivo, instalar una dependencia, ampliar el alcance o tomar una decision de producto.

## 16. Prompt unico para Antigravity con Gemini 3.7

```text
Actua como constructor inicial de PZ-002A, Estructura minima ejecutable y pruebas base de OminAI HQ. Usa Gemini 3.7 durante toda esta construccion inicial.

Trabaja en una sola conversacion. No delegues archivos a conversaciones separadas y no uses Claude.

Lee completamente, en este orden:
1. AGENTS.md
2. TEAM-WORKFLOW.md
3. CONTRATO-MVP-v1.md version 1.2-aprobada
4. FICHA-PZ-001A-CONTRATOS-NUCLEO.md
5. contracts/core/README.md y los doce JSON de contracts/core
6. FICHA-PZ-002A-ESTRUCTURA-MINIMA.md

Antes de editar:
- confirma la lectura;
- confirma Python 3.11 o posterior;
- confirma que jsonschema compatible ya esta disponible sin instalar;
- confirma que ninguno de los siete archivos permitidos existe;
- genera el manifiesto y SHA-256 inicial de los trece archivos de contracts/core;
- informa tu plan y la lista exacta de siete archivos.

Si alguna comprobacion falla, detente sin editar y solicita decision humana.

Construye exclusivamente:
- README.md
- pyproject.toml
- .gitignore
- app/__init__.py
- app/__main__.py
- tests/test_smoke.py
- tests/test_contracts.py

No modifiques ningun otro archivo. No instales paquetes. No uses red. No crees agentes, herramientas de agentes, servidor, API, interfaz, persistencia, memoria, nube, despliegue, Docker, CI/CD, Terraform, main.py, requirements.txt, archivos de bloqueo ni manifiestos de Agents CLI.

Implementa exactamente el contenido, las pruebas y los criterios definidos en la ficha. Usa Python con -B para no generar bytecode.

Al terminar ejecuta todas las pruebas de la seccion 12, compara las huellas de contracts/core y comprueba que no aparecieron archivos no autorizados.

Devuelve resumen, archivos, comandos, salidas completas, conteos, huellas antes/despues, confirmacion de cero instalaciones y llamadas externas, errores, limitaciones, supuestos y riesgos. No declares implementados runtime, agentes, persistencia, interfaz ni despliegue.
```

## 17. Registro de aprobacion humana

```text
Pieza: PZ-002A
Decision: APROBAR_PZ-002A_PARA_CONSTRUIR
Lenguaje: Python 3.11 o posterior
Constructor: Antigravity con Gemini 3.7
Modalidad: una sola conversacion para los siete archivos
Dependencia nueva autorizada para declarar: jsonschema>=4.18,<5 como dependencia opcional de pruebas
Instalaciones autorizadas: ninguna
Fecha: 29 de agosto de 2026
Autoridad: usuario humano (A0 actual del proyecto)
Referencia: confirmacion expresa "si dale" en la conversacion del 29 de agosto de 2026
```

## 18. Registro de correccion 1

```text
Pieza: PZ-002A
Ronda: CORRECCION_1
Corrector: Codex
Archivo autorizado y modificado: tests/test_contracts.py
Archivos nuevos autorizados: ninguno
Contratos autorizados para modificar: ninguno
Hallazgos corregidos: conteo exacto de filas 4.2; matriz de 1440 combinaciones; terminos prohibidos completos; version 1.0.0; FormatChecker; rechazo explicito de casos negativos de transicion
Verificacion local: python -B -m app, codigo 0
Pruebas locales: python -B -m unittest discover -s tests -v, 16 aprobadas, 0 fallidas, 0 omitidas
Estado resultante: pendiente de revision independiente de Copilot y de aprobacion humana final
Fecha: 29 de agosto de 2026
```

## 19. Cierre documental y aprobacion humana final

```text
Pieza: PZ-002A
Decision: ACEPTADA
Estado final: COMPLETADA_Y_ACEPTADA
Fecha: 30 de agosto de 2026
Autoridad: usuario humano (A0 actual del proyecto)
Referencia: "listo sigamos c:" despues de la solicitud de aprobacion final y de la explicacion sencilla de lo construido
Alcance aceptado: los siete archivos enumerados en la seccion 6 y la correccion 1 acotada a tests/test_contracts.py
Construccion inicial: Antigravity
Correccion 1: Codex
Revision independiente: Copilot, APTO_PARA_APROBACION_HUMANA
Consolidacion de Chipi/Codex: APTO_PARA_APROBACION_HUMANA tras verificar la evidencia de integridad inicial
Pruebas verificadas: 16 aprobadas, 0 fallidas, 0 omitidas
Matriz vigente: 1440 combinaciones, exactamente 10 aceptadas
Arranque verificado: python -B -m app, codigo 0, STRUCTURE_READY e implemented_capabilities=[]
Integridad: 13/13 huellas SHA-256 iniciales y finales del informe coinciden con los archivos actuales; tamanos coincidentes
Informes conservados: INFORME-CONSTRUCCION-PZ-002A.md y REVISION-COPILOT-PZ-002A.md
Capacidades no acreditadas: agentes reales, runtime completo de mision, persistencia, memoria, interfaz, login, VBP y despliegue
```

### Notas de reconciliacion de la evidencia

- Los informes se conservan como documentos historicos, no como nuevas instrucciones ni permisos de construccion.
- El informe inicial prueba 960 combinaciones; corresponde a la version anterior a la correccion. La suite vigente prueba 1440.
- La limitacion de Copilot sobre ausencia de huellas previas se resolvio al recibir el informe inicial y contrastar individualmente sus 13 pares de huellas y tamanos con los archivos actuales. El conteo de archivos por si solo no demuestra inmutabilidad.
- El total de 72 archivos del workspace coincidia antes de archivar estos informes; el desglose historico "59 + 7 + 6" es una errata y no se utiliza como evidencia del alcance. `app/` y `tests/` contienen dos archivos cada uno, ya incluidos entre los siete autorizados.
- Estos informes y la ficha de la siguiente pieza son documentacion de coordinacion posterior al cierre, no archivos adicionales de la construccion de PZ-002A.
- Esta aprobacion cierra solamente PZ-002A. La siguiente pieza requiere su propia aprobacion humana antes de construir.
