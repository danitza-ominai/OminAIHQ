# Plan de cierre de OminAI HQ para All Things Agentic

> ACTUALIZACIÓN posterior, 31-08-2026: Niko pidió todas las correcciones y construcción pendiente en un encargo integral para Antigravity, después ajustes autorizados de Codex y únicamente revisión final de Copilot. Usar `competition/ENCARGO-INTEGRAL-ANTIGRAVITY-2026-08-31.md` y `competition/PROMPT-INTEGRAL-ANTIGRAVITY.txt`. La nueva suite ejecutada obtuvo 280 pruebas en 112.441 s: 277 sin fallo/error, 1 fallo y 2 errores, salida 1. Los conteos y ventanas inferiores describen la preparación anterior y no sustituyen ese baseline. Se conservan como historia del plan; no se declaran agentes reales ni nube verificados.

Fecha de preparación: 31 de agosto de 2026. Horario: Ecuador continental, UTC-5.
Estado: PROPUESTA DE COORDINACIÓN; no es autorización de código, gasto, despliegue, publicación ni aceptación del MVP.

**Objetivo de hoy:** entregar una demostración real, reproducible y documentada del recorrido aprobado de OminAI HQ. No ampliar el producto ni presentar simulaciones como integración real. La viabilidad depende de superar los hitos de integración y nube a tiempo; este horario no garantiza conseguirlo.

## 1. Fecha y perfil de entrega

El cierre oficial es el 31 de agosto a las 17:00 PDT, equivalente a las **19:00 de Ecuador**. Objetivo interno: enviar a las **18:30**, dejando treinta minutos de margen. [Actualización oficial](https://allthingsagentichackathon.devpost.com/updates).

Las reglas vigentes exigen Gemini 3.5 o posterior, un framework admitido de Google y un servicio de infraestructura de Google Cloud. También piden repositorio, instrucciones reproducibles, diagrama y video público de hasta cuatro minutos que demuestre el backend en Google Cloud. Los materiales deben estar en inglés o tener traducción. [Reglas oficiales, sección 6](https://allthingsagentichackathon.devpost.com/rules).

El contrato local, sección 11.9, ya fija **Collaborative Partner**, Gemini 3.5 Flash o posterior, Google ADK, Cloud Run, Firestore y Cloud Storage. Firestore y Cloud Storage son elecciones del perfil del proyecto; no son una exigencia universal del concurso. No sustituir este perfil ni cambiar de categoría sin decisión humana.

La misión ya aprobada es ayudar a una fundadora sin equipo a decidir si su producto digital está listo para una beta controlada, convirtiendo documentos dispersos y contradictorios en un VBP verificable. **OminAI HQ es el producto concursante; Business OS es la iniciativa analizada en ese escenario.**

## 2. Qué evidencia tenemos y qué falta verificar

| Observación de esta revisión | Implicación para el cierre |
|---|---|
| Hay contrato, fichas, núcleo Python, UI, persistencia local, pruebas y documentos de competencia. | Reutilizar esta base. No reconstruir el producto. |
| `app/agent_gateway.py` usa un proveedor mock por defecto y rechaza proveedores reales; `app/hq_runtime.py` ejecuta especialistas simulados. | Falta demostrar las cinco ejecuciones reales del perfil aprobado; cambiar etiquetas o nombres de modelo no basta. |
| `app/runtime_config.py` conserva Gemini 2.5 y tarifas sintéticas. | Verificar ID disponible, SDK, credenciales, tokens y precios oficiales antes de activar llamadas. |
| El servidor admite solamente `127.0.0.1:8000`, exige configuración local SIMULADA y se cierra tras 45 minutos. El Dockerfile ejecuta ese servidor. | El contenedor existente no demuestra compatibilidad operativa con Cloud Run. Separar el adaptador cloud y conservar la seguridad local. |
| `app/cloud_demo_repository.py` contiene política de cuota sobre SQLite; lo inspeccionado no acredita adaptadores reales de Firestore/Cloud Storage. | La persistencia y las cuotas de la demo cloud necesitan evidencia propia. |
| El README registra históricamente 272/273, pero una reproducción actual en memoria de la aprobación del plan avanzó la revisión de 4 a 5. | El defecto descrito allí no puede darse por vigente sin volver a probarlo. Tampoco esta prueba aislada cierra la coherencia global. |
| La documentación de competencia y evaluación todavía afirma 231 pruebas verdes, Gemini 2.5 y capacidades sin suficiente distinción entre mock y real. | Actualizar afirmaciones usando una única ejecución final y una versión identificable. |
| No se verificó en esta revisión una URL cloud, un repositorio remoto de entrega ni un video publicado. | Buscar primero si ya existen; no duplicarlos ni asumir que están listos. |

**Límite de verificación:** no se obtuvo una nueva suite completa. Los intentos de la suite de repositorio con Python local fallaron al abrir directorios temporales por permisos de Windows; el runtime empaquetado no tenía `jsonschema`. Esos errores de entorno no equivalen a siete defectos de producto. La prueba puntual en SQLite en memoria sí se ejecutó y devolvió revisión 4→5. No se modificó código de producto.

Cloud Run requiere escuchar en todas las interfaces del contenedor y en el puerto configurado; su sistema de archivos local no conserva datos al detenerse la instancia. No abrir simplemente el servidor local a Internet ni depender de su SQLite para durabilidad cloud. [Contrato de ejecución de Cloud Run](https://docs.cloud.google.com/run/docs/container-contract).

## 3. Cómo usar REQUISITOS sin ampliar el alcance

Se inventariaron **45 PDF y una transcripción**. Se extrajo texto para clasificar el corpus y se consultaron pasajes relevantes; esto no equivale a verificar visualmente todas las páginas ni a validar los ejemplos contra SDK actuales.

Orden de aplicación: decisiones humanas y reglas del equipo; contrato aprobado; reglas oficiales actuales para elegibilidad; materiales educativos para implementación. Si hay incompatibilidad, registrarla y resolverla expresamente.

| Fuente local | Aplicación concreta de hoy | Evidencia que debe devolver el equipo |
|---|---|---|
| Resumen del 11 de agosto, `a5aaf8a8-...2308.pdf`, p. 1 | Funciones para permisos, límites y estados; agentes para razonamiento; orquestación con entradas y salidas claras. | Ejecución de roles separados y transición determinista. |
| `T-DEVAGENTOPT-I-m1-l1-es-file-2.es.pdf`, pp. 1 y 4 | Instrucciones con objetivo, límites, formato e incertidumbre. | Cada agente tiene contrato y rechaza acciones fuera de alcance. |
| `T-DEVAGENTOPT-I-m2-l0-es-file-3.es.pdf`, p. 1 | Salidas estructuradas verificables. | Salida inválida provoca error controlado, no consolidación silenciosa. |
| `T-DEVAGENTMEM-B-m3-l0-es-file-5.es.pdf`, pp. 1–2; familia MEM | Separar estado de misión, información temporal y memoria entre misiones. | Reinicio, aislamiento y recuperación de memoria aprobada sin fugas. |
| Familias TOOL y DEPLOY; `T-DEVAGENTDEPLOY-A-m4-l0-es-file-7.es.pdf`, pp. 1–2 | Herramientas limitadas y despliegue con UI/backend y estado durable. | Fuente autorizada, contenedor operativo y URL cloud con prueba de ejecución. |
| Transcripción `Hi everyone. Uh thank you for joini.txt`, 25:39–26:02 | No premiar una salida aparentemente correcta que viola restricciones. | Negativos con ausencia de efectos indebidos y evaluación separada. |

Registrar cada control como `requisito → fuente/página → pieza/archivo → prueba → resultado → evidencia/versionado`. Reutilizar `PIEZAS-PENDIENTES/01-MATRIZ-DE-COBERTURA.md`; no inventar una segunda lista incompatible.

No copiar automáticamente modelos antiguos, `include_thoughts=True`, compras, correos, MCP, A2A o infraestructuras mostradas en clases. El contrato prohíbe almacenar Chain-of-Thought y excluye ejecutar la iniciativa cliente.

## 4. Plan de producto y responsables

Las ventanas siguientes son objetivos de trabajo desde las 14:30, no promesas de duración. Las piezas siguen siendo secuenciales y sus dependencias deben estar aceptadas. La documentación puede avanzar sobre archivos diferentes mientras se trabaja en código.

| Ventana | Paso | Responsable | Criterio de salida |
|---|---|---|---|
| 14:30–14:50 | Congelar alcance, identificar versión actual, revisar aceptaciones y accesos ya existentes. Preparar encargos cerrados de lo pendiente. | Codex coordina; Niko decide. | Escenario, lista de archivos, dependencias, proyecto cloud, permisos y presupuesto identificados; ningún archivo con dos editores. |
| 14:50–15:40 | Completar integración real aprobada: Gemini vigente + ADK, cinco roles, herramientas limitadas, salidas estructuradas, costes y errores visibles. | Antigravity para construcción inicial pendiente; Codex únicamente para correcciones expresamente autorizadas. | Llamadas reales identificables; no hay fallback oculto a fixtures. Credenciales no expuestas. Una entrada cambia materialmente el resultado. |
| 15:40–16:15 | Validar recorrido completo, revisión nuclear y referencias; aprobación, rechazo, memoria y recuperación. | Constructor devuelve evidencia; Codex inspecciona; Copilot revisa una versión estable. | Misión → plan → aprobación humana → especialistas → evaluación → aprobación humana → descarga exacta de 18 secciones. Ningún bloqueo crítico abierto. |
| 16:15–17:00 | Completar adaptador cloud y persistencia del perfil; desplegar solo tras autorización y revisión. | Constructor prepara; Niko autoriza entorno/gasto/despliegue; Copilot revisa exposición y permisos. | Servicio operativo, datos saneados, identidad del operador protegida, estado/cuota durable y ejecución real demostrada en Google Cloud. |
| 17:00–17:25 | Ejecutar regresión, evaluación y ensayo humano final sobre la versión que se enviará. | Copilot revisa; Codex consolida; Niko realiza decisiones humanas. | Informe con comando, entorno, versión/huella, resultados y limitaciones; demo preparada cumple objetivo contractual de 2:30. |
| 17:25–18:00 | Grabar, subtitular y subir el video; cerrar README, diagrama y descripción. | Niko presenta y autoriza publicación; Codex prepara documentación. | Video real de máximo 4 minutos, evidencia cloud visible, material en inglés y enlaces accesibles. |
| 18:00–18:30 | Comprobar formulario, repositorio, video y acceso; enviar y guardar confirmación. | Niko, con checklist de Codex. | Devpost confirma entrega; enlaces probados desde una sesión sin acceso privilegiado. |
| 18:30–19:00 | Margen para errores de carga o enlaces. | Niko. | Sin nuevas funciones ni modificaciones de alcance. |

**Hitos de viabilidad:** si a las 15:40 no hay integración real, o a las 17:00 no hay ejecución en Google Cloud, el riesgo de no llegar es alto. Priorizar requisitos obligatorios y detener adornos. No presentar un video local como prueba cloud. Si no se supera el gate, registrar que no está listo; cualquier reducción contractual necesita decisión expresa y no elimina exigencias del concurso.

### Validaciones que no se pueden sustituir por un conteo de tests

1. Rechazar aprobación ausente, caducada, cruzada entre misiones o correspondiente a otra versión; comprobar que no cambia estado ni consume indebidamente autorización.
2. Repetir la misma decisión y descarga sin duplicar efectos; fallos de exportación no finalizan la misión.
3. Probar pausa/reanudación y reinicio con estado, referencias, memoria, intentos y presupuesto conservados.
4. Fuente faltante, contradicción o salida inválida bloquea o se etiqueta; el evaluador no declara éxito por puntuación alta con un bloqueo.
5. Ocho casos de desarrollo y dos holdout gestionados separadamente; no pasar respuestas esperadas al constructor ni al agente evaluado. Un manifest de holdout no prueba su ejecución.
6. Demo pública sin documentos privados, sin secretos, sin misión libre y sin aprobaciones administrativas disponibles para visitantes.
7. Cuota diaria y límites de tokens/reintentos/coste se mantienen después de reiniciar. Verificar costes de infraestructura además del ledger de llamadas; no prometer un límite total de factura por tener alertas.
8. Niko completa la interacción real, incluida la descarga nativa. Las decisiones sintéticas de pruebas no son aceptación humana.

## 5. Plan de documentación, aprovechando archivos existentes

| Orden | Archivo | Cambio necesario | Comprobación |
|---|---|---|---|
| 1 | `README.md` | Estado actual al principio; instalación y arranque reproducibles; modos local/cloud; modelo/SDK reales; enlaces y limitaciones. Conservar historia identificada. | Otra persona sigue instrucciones desde un entorno limpio. |
| 2 | `competition/ARQUITECTURA.md` | Diagrama de despliegue además del flujo: UI, backend, ADK/Gemini, Firestore, Storage, puertas, datos privados y expediente saneado. | El diagrama representa lo desplegado y distingue lo pendiente. |
| 3 | `competition/LIMITACIONES-Y-EVIDENCIAS.md` | Separar IMPLEMENTADO_LOCAL, SIMULADA, REAL_VERIFICADO y PENDIENTE; enlazar evidencia por capacidad. | Ninguna capacidad se justifica solamente por existir un archivo o mock. |
| 4 | `evaluation/release_protocol.md` y matriz de cobertura existente | Sustituir cifras desactualizadas por una ejecución fechada; resultados de evaluación, revisión Copilot y gate 15.7/C.18. | No usar porcentajes de planificación como cobertura ejecutada. |
| 5 | `deploy/OPERACION-DEMO.md` y `deploy/VERIFICACION-DEMO.md` | Procedimiento real, identidad, región, parámetros, persistencia, cuotas y recuperación; prueba de URL/logs saneados. | Los comandos coinciden con la versión entregada y no publican secretos. |
| 6 | `competition/ENTREGA.md` | Texto en inglés: problema específico, usuario, solución, funcionamiento, stack real, fuentes, diferenciador, desafíos y aprendizajes. | Evitar promesas de eliminar alucinaciones o madurez productiva sin evidencia. |
| 7 | `competition/GUION-VIDEO-ES-EN.md` | Ajustar guion a lo que realmente funciona; integrar prueba cloud, archivo/evidencia, feedback humano y VBP. | Lo narrado coincide con pantalla y no confunde aprobación con exportación final. |

La revisión documental debe conservar versiones históricas sin presentarlas como estado vigente. No subir indiscriminadamente toda la carpeta: hay bases `.db`, directorios de revisión y PDF educativos cuyo permiso de redistribución no se ha comprobado. `.dockerignore` no protege lo publicado en Git. Revisar código, licencia, atribuciones, expediente saneado y exclusiones antes de publicar.

### Guion propuesto para 3:50

- 0:00–0:25: fundadora, documentos contradictorios y decisión de beta que necesita tomar.
- 0:25–0:45: arquitectura y evidencia visible de Google Cloud.
- 0:45–3:15: ejecución real continua: misión, aclaración, aprobación del plan, especialistas, evidencia/contradicción, evaluación, aprobación y descarga. No recortar una espera para aparentar menor latencia.
- 3:15–3:35: evidencia de memoria/recuperación y límites, indicando si corresponde a otra ejecución.
- 3:35–3:50: resultado, valor, límites y acceso al repositorio.

Subir tan pronto exista una toma completa válida; la plataforma de video puede tardar en procesarla. Los organizadores recomiendan no esperar hasta el último momento. [Aviso de entrega](https://allthingsagentichackathon.devpost.com/updates).

## 6. Flujo del equipo y decisiones necesarias

- **Antigravity:** constructor inicial. Reutiliza fichas aprobadas cuya lista y precondiciones sigan siendo válidas. Las fichas antiguas que dicen «crear; detenerse si existe» no autorizan sobrescribir archivos ya construidos.
- **Codex:** coordinación, reconciliación, criterios y documentación; correcciones solo con hallazgos y archivos exactos autorizados. El README registra dos rondas y una intervención excepcional: no se presume una ronda adicional disponible.
- **GitHub Copilot:** revisión independiente, sin editar ni construir. Recibe ficha, versión/huella, cambios y pruebas, y reporta severidad, ubicación, evidencia, impacto y recomendación.
- **Niko:** aprueba cambios materiales y autorizaciones específicas, controla llamadas/gasto/despliegue/publicación, y acepta o rechaza la entrega. No se vuelve a pedir autorización para una ficha ya aprobada e inalterada.

No delegar un «termina todo» abierto. Cada encargo debe incluir objetivo, fuentes concretas de REQUISITOS, archivos permitidos/prohibidos, pruebas, salida, límites y criterio de aceptación. Las capacidades nuevas no se cuelan dentro de una corrección.

La cuota pública de cinco ejecuciones requiere comprobar que los jueces tendrán acceso suficiente mediante instrucciones o un build de prueba, sin publicar una puerta de gasto ilimitada. Conservar versión y enlaces enviados durante evaluación; continuar desarrollo en copia separada. [FAQ oficial sobre acceso, video y cambios](https://allthingsagentichackathon.devpost.com/details/faqs).

**Primer paso operativo:** preparar el encargo cerrado de integración real y compatibilidad cloud a partir de PZ-004A, PZ-014A/B y el estado actual, separando construcción pendiente de correcciones existentes. Antes de ejecutarlo, tener identificados SDK/modelo, proyecto, región, credenciales seguras, permisos ya concedidos y los que realmente faltan.
