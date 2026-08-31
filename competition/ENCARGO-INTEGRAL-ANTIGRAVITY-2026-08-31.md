# Encargo integral de cierre — OminAI HQ
Fecha: 2026-08-31. Versión: 1. Estado: LISTO_PARA_QUE_NIKO_LO_ENVIE_A_ANTIGRAVITY.
No se ha ejecutado construcción mediante este documento. No autoriza llamadas, instalaciones, gasto, despliegue o publicación por su mera existencia.

## 1. Flujo solicitado y objetivo

Niko pidió reunir las correcciones y construcción pendiente para Antigravity, después ajustes de Codex y finalmente revisión de Copilot. Este encargo sustituye operativamente la propuesta de enviar CIERRE-01 por separado y las revisiones Copilot intermedias. No se editan AGENTS.md ni decisiones históricas.

**Antigravity aborda este lote integral; Codex inspecciona su entrega y aplica únicamente la corrección posterior expresamente autorizada; GitHub Copilot revisa la versión final sin editar.** La intervención de Antigravity sobre defectos existentes es el cambio de flujo solicitado por Niko para este cierre, no una regla permanente. No se reinician contadores de rondas ni se autorizan rondas futuras ilimitadas.

El objetivo es levantar OminAI HQ con el recorrido aprobado: misión, aclaración, plan, primera aprobación humana, cinco roles reales, evidencia, VBP de 18 secciones, evaluación, segunda aprobación humana y descarga exacta. Después, demo controlada en Google Cloud y documentación de entrega.

Producto concursante: OminAI HQ. Categoría aprobada: Collaborative Partner. Business OS es únicamente la iniciativa cliente del escenario aprobado. No construir Business OS ni incorporar Omi/OminaiTech.

Enviar este encargo a Antigravity debe expresar la autorización humana del perímetro del apartado 5. Este documento no finge una aprobación previa de los 88 archivos recién enumerados. No obliga a modificar todos: solo los necesarios para hallazgos y capacidades descritos. No sobrescribir trabajo ajeno ni reabrir piezas aceptadas fuera del perímetro.

## 2. Baseline ejecutado y alcance de la revisión

El 31-08-2026 se ejecutó, sin modificar fuentes:

```text
python -B -m unittest discover -s tests -v
Ran 280 tests in 112.441s
FAILED (failures=1, errors=2)
Código de salida: 1
277 pruebas sin fallo/error.
```

La ejecución fuera del aislamiento superó los problemas previos de permisos de temporales. El error de recuperación incluye un fallo de aserción y un error posterior de limpieza Windows por conexión abierta; no son dos casos adicionales.

Fallos actuales:

1. `test_bilingual_view.TestPreparedBilingual.test_prepared_demo_fidelity_frozen_before_ordinary_approval`: cambia la huella del VBP al aprobar.
2. `test_hq_end_to_end.TestIntegratedRecovery.test_restart_does_not_repeat_confirmed_task`: el resultado confirmado pasa de mission_version 6 a 9 y cambia su huella; después falla la limpieza de restart.db.
3. `test_audit_query.TestCanonicalAudit.test_persisted_canonical_projection_filters_and_history`: el fixture reutiliza un evento histórico y save_event rechaza versión inexistente/obsoleta.

La prueba nuclear puntual de avance de versión ya pasó de 4 a 5 en la revisión anterior; no volver a tratar «versión no incrementada» como diagnóstico único. Ahora el problema observado es preservar artefactos/aprobaciones mientras cambia la revisión operativa.

Esta es una revisión dirigida al cierre, no una garantía de haber descubierto todos los defectos. Los hallazgos siguientes distinguen reproducción, inspección y verificación pendiente. Si aparece un problema nuevo, reportarlo con su alcance antes de ampliar archivos o capacidades.

## 3. Hallazgos y trabajo obligatorio

| ID / prioridad | Evidencia y problema | Corrección / criterio de salida |
|---|---|---|
| H01 — P0 | REPRODUCIDO por suite. human_approvals altera mission_version del candidato y recalcula su huella al aprobar; local_repository también actualiza huellas de aprobaciones/candidatos al guardar cambios de estado. | Preservar exactamente candidato, huella solicitada y aprobación consumida. Separar revisión operativa de versión del artefacto mediante referencias/historia válidas. No reescribir solicitudes consumidas ni aprobar silenciosamente otro contenido. |
| H02 — P0 | REPRODUCIDO. save_mission reversiona y rehashea resultados/evidencia ya confirmados; se rompe igualdad tras reanudar. | Una transición no modifica un resultado, original, evidencia o aprobación históricos. Una nueva versión material crea un registro/versionado explícito. Reinicio no repite llamada ni cambia salida confirmada. |
| H03 — P1 | REPRODUCIDO. Fixture de auditoría inserta un evento copiado de versión anterior; además usa un pensamiento/secreto sintético y exige su persistencia cruda. | Resolver coherencia de fixture/registro sin relajar validación de eventos. Pruebas deben exigir saneamiento antes de persistir nueva información protegida, además de proyección segura. No usar una expectativa insegura para justificar guardar CoT. |
| H04 — P0 | INSPECCIONADO. Gateway solo acepta mock, defaults/tarifas 2.5 sintéticos; falta proveedor ADK real. | Implementar ADK + gemini-3.5-flash explícitos, límites y errores seguros; offline sigue disponible y etiquetado. REAL_VERIFICADO exige llamada observada, no credencial presente. |
| H05 — P0 | INSPECCIONADO. Los especialistas no llaman execute_agent_call; HTTP dispara execute_local_simulation. VBP contiene secciones fijas sobre ERP/compras B2B. | Conectar cinco roles reales, en secuencia, con contexto autorizado y salida validada; UI usa el runtime correspondiente. Generar VBP desde resultados de la misión, sin plantillas de otro negocio presentadas como análisis. |
| H06 — P0 | INSPECCIONADO/REPRODUCIDO. SourceReader solo consulta mock_sources; allowed_domains=set() permite Wikipedia por restaurar defaults. max_bytes recorta caracteres. Research asigna confianza por palabras del localizador o número total de fuentes y usa fecha actual como publicación. | Lista vacía significa denegar. Lectura real autorizada y acotada, bytes reales, límites/timeout y redirecciones seguros, IPv4/IPv6/DNS/metadata bloqueados. Originales, fechas conocidas/desconocidas y sustento de cada claim verificables. Ninguna reputación inferida por substring. |
| H07 — P1 | REPRODUCIDO. JPEG de cuatro bytes FF D8 FF D9 es admitido como 1024×768. Parser PNG no demuestra decodificación ni dimensiones positivas. | Validar formatos y estructura real, límites positivos y píxeles; eliminar dimensiones inventadas. Saneamiento debe conservar imagen decodificable, quitar metadatos sensibles y comprobar hash/resultado. |
| H08 — P0 | REPRODUCIDO. El mismo item se incluye en manifest de MSN-A y MSN-B con igual fingerprint. authorize_item_for_dossier no recibe contexto humano ni liga misión. | Autoridad comprobada, vínculo a misión/versión/item/bytes y revocación persistidos; el manifest solo contiene items autorizados para su misión. Huella cubre identidad y contenido canónicos, no solo una concatenación parcial. |
| H09 — P1 | REPRODUCIDO. Cinco archivos de MSN-A hacen rechazar el primer archivo de MSN-B en el mismo gestor. Identificadores dependen de hash truncado y almacenamiento concatena mission_id. | Contadores y referencias por misión/versionado; validar identificadores y destino resuelto bajo raíz autorizada; misma fuente en dos misiones no pisa registros. Exceder cupo o fallar escritura no admite ni deja efectos indebidos. |
| H10 — P1 | INSPECCIONADO. PDF se extrae con regex/ASCII sobre streams, sin parser completo. DOCX descomprime document.xml sin límite previo de expansión. | Parser mantenido con versión fijada y límites de bytes, páginas/expansión/tiempo; PDF con texto comprimido debe dar texto correcto o error explícito, nunca basura como evidencia. Escaneado sin OCR queda pendiente. ZIP inválido/bomba se rechaza sin consumo descontrolado. |
| H11 — P0 | REPRODUCIDO. Harness acepta passed=true/score=1 si coinciden verdict/state aunque el resultado declare herramienta prohibida y ausencia de aprobación. INSPECCIONADO: pesos/dimensiones del evaluador no corresponden a 11.8. | Evaluar resultado, trayectoria observable, evidencia y restricciones; bloqueadores antes de puntuar. Pesos canónicos: evidencia 30, completitud/coherencia 25, misión/valor 20, viabilidad 15, riesgos/gobernanza 10. No tomar flags del agente como única prueba de seguridad. |
| H12 — P0 | INSPECCIONADO. Docker ejecuta servidor limitado a loopback/8000 y modo SIMULADA; repositorio cloud usa SQLite. Faltan adaptadores Firestore/Storage reales. | Adaptador cloud separado, puerto/interfaz Cloud Run, identidad verificada, estado/aprobaciones/ledger/cuota durables y objetos saneados. Sin SQLite efímero presentado como persistencia cloud. |
| H13 — P1 | INSPECCIONADO. Inglés preparado está ligado a fixture; endpoints/UI actuales son locales/simulados. | Crear/revisar/aprobar/ejecutar/pausar/reanudar/exportar desde UI contra backend real; ES/EN fiel y congelado antes de aprobación. No rellenar contenido arbitrario con traducciones del fixture. Probar descarga nativa humana. |
| H14 — P0 | INSPECCIONADO. Costes y etiquetas actuales son sintéticos; no hay evidencia de consumo facturable real ni cuota global cloud en ejecución. | Reservar antes de llamada, incluir tokens de pensamiento sin contenido, no reintentos SDK ocultos, retener reserva incierta y reconciliar una vez. Cuota y gasto compartidos sobreviven reinicio/concurrencia. No prometer límite de factura total por alertas. |
| H15 — P1 | INSPECCIONADO. README/competition/release_protocol muestran resultados contradictorios y tecnología antigua. Hay bases privadas y cachés; .gitignore no excluye todas esas categorías. | Documentar versión final y evidencia efectiva, instalación reproducible, arquitectura cloud, límites, demo/video. Proteger publicación con exclusiones revisadas; no subir bases ni el corpus educativo sin derechos verificados. |
| H16 — P0 | PENDIENTE DE VERIFICACIÓN real. Puertas, memoria, fuentes retiradas, rechazo, actor falso, replay, presupuesto y recuperación tienen pruebas locales; eso no acredita su preservación en nube y con modelos reales. | Ejecutar el gate final sobre la integración efectiva y conservar pruebas negativas. No reconstruir un control que ya funciona salvo adaptación necesaria y probada. |

No «arreglar» H01/H02 actualizando expectativas para aceptar reescrituras ni recalculando huellas de historia. Si la solución exige cambiar contratos aceptados, presentar conflicto exacto y propuesta; esos contratos NO están autorizados para editar.

## 4. Fuentes obligatorias y límites de producto

Leer AGENTS.md, TEAM-WORKFLOW.md, CONTRATO-MVP-v1.md (especialmente 0–7, 10–11, 11.8, 11.9, 15.7 y C.18), las fichas PZ afectadas y la matriz de cobertura. La nueva instrucción humana cambia el orden del equipo de este lote, no la autoridad humana dentro del producto.

REQUISITOS contiene 45 PDF y una transcripción. Usar pasajes relevantes con localizador en cada decisión:
- Taller 11-08: a5aaf8a8-fe07-4a6a-8f9a-fc29a5baa691_11_de_agosto_de_2026_2308.pdf, p.1: función determinista vs agente.
- T-DEVAGENTOPT-I-m1-l1-es-file-2.es.pdf, pp.1/4: instrucciones y límites.
- T-DEVAGENTOPT-I-m2-l0-es-file-3.es.pdf, p.1: estructuras verificables.
- T-DEVAGENTMEM-B-m3-l0-es-file-5.es.pdf, pp.1–2: alcance y vida del estado.
- Familia TOOL: herramientas limitadas, errores y uso de fuentes; familia DEPLOY, m4: Cloud Run.
- Transcripción Hi everyone. Uh thank you for joini.txt, 25:39–26:02: evaluación y reward hacking.

No copiar ejemplos de modelos antiguos, compras, pagos, correos, CoT, MCP/A2A u otras tecnologías como requisitos nuevos.

Modelo oficial propuesto: `gemini-3.5-flash`. Dependencia ADK propuesta: `google-adk==2.8.0`. Elegir y fijar también librerías de Firestore/Storage, verificación de identidad y parsers estrictamente necesarias, documentando APIs/versiones oficiales antes de instalar; no inventar que ya están verificadas en este entorno.
Fuentes: [modelo](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash), [ADK](https://pypi.org/project/google-adk/2.8.0/), [Cloud Run](https://docs.cloud.google.com/run/docs/container-contract).
Referencia de precio Gemini Developer API estándar consultada hoy: USD 1.50/M entrada, USD 9.00/M salida incluido pensamiento; no trasladar a Vertex AI ni asumir gratuidad. [Precios](https://ai.google.dev/gemini-api/docs/pricing).

Conservar límites contractuales: una misión/agente concurrentes, hasta tres aclaraciones, dos intentos por tarea y un reintento transitorio, 15 solicitudes/misión, 300 s por solicitud humana, 20 minutos de misión, USD 25 total existente, aviso 70% y pausa 90%, 5 demos públicas/día, una instancia cloud, 18 secciones y video ≤4 min. Objetivo de demo preparada: 150 s. No renovar presupuesto por bloque.

## 5. Perímetro cerrado propuesto

Raíz: `C:\Users\Nivez\Desktop\08_Ominai\OminAIHQ`.
77 archivos existentes se pueden modificar SOLO para H01–H16 y su integración. 11 destinos nuevos se pueden crear. La lista no obliga a editar los 88 y no autoriza sustitución masiva. Registrar por archivo el H que justifica su cambio.

### Archivos existentes — modificar si es necesario

```text
app/agent_gateway.py
app/runtime_config.py
app/local_repository.py
app/human_approvals.py
app/hq_runtime.py
app/mission_engine.py
app/chief_of_staff.py
app/research_analyst.py
app/product_architect.py
app/delivery_planner.py
app/governance_risk.py
app/source_reader.py
app/evidence_registry.py
app/file_intake.py
app/document_extractors.py
app/image_intake.py
app/sanitized_dossier.py
app/approved_memory.py
app/data_lifecycle.py
app/recovery.py
app/mission_controls.py
app/audit_query.py
app/vbp_document.py
app/vbp_export.py
app/vbp_validation.py
app/evaluation_harness.py
app/evaluation_report.py
app/http_api.py
app/api_contracts.py
app/cloud_demo_repository.py
web/app.js
web/i18n.js
web/index.html
web/styles.css
Dockerfile
.dockerignore
.gitignore
pyproject.toml
deploy/cloudrun.example.yaml
deploy/OPERACION-DEMO.md
deploy/VERIFICACION-DEMO.md
README.md
competition/ARQUITECTURA.md
competition/ENTREGA.md
competition/GUION-VIDEO-ES-EN.md
competition/LIMITACIONES-Y-EVIDENCIAS.md
evaluation/release_protocol.md
tests/test_agent_gateway.py
tests/test_local_repository.py
tests/test_human_approvals.py
tests/test_hq_end_to_end.py
tests/test_audit_query.py
tests/test_bilingual_view.py
tests/test_chief_of_staff.py
tests/test_research_analyst.py
tests/test_product_architect.py
tests/test_delivery_planner.py
tests/test_governance_risk.py
tests/test_five_agent_flow.py
tests/test_mission_engine.py
tests/test_evidence_registry.py
tests/test_file_intake.py
tests/test_image_intake.py
tests/test_sanitized_dossier.py
tests/test_approved_memory.py
tests/test_data_lifecycle.py
tests/test_recovery.py
tests/test_mission_controls.py
tests/test_vbp_document.py
tests/test_vbp_export.py
tests/test_evaluation_harness.py
tests/test_evaluation_adversarial.py
tests/test_http_api.py
tests/test_ui_contracts.py
tests/test_cloud_demo_policy.py
tests/test_release_gates.py
tests/test_mvp_delivery.py
```

### Archivos ausentes al preparar — crear solamente para estas funciones

```text
app/adk_provider.py
app/cloud_http_api.py
app/firestore_repository.py
app/cloud_storage.py
tests/test_adk_provider.py
tests/test_cloud_http_api.py
tests/test_firestore_repository.py
tests/test_cloud_storage.py
tests/test_source_reader.py
deploy/requirements.lock
competition/RESULTADO-INTEGRAL-ANTIGRAVITY.md
```

- adk_provider: transporte real ADK, no segundo sistema de permisos.
- cloud_http_api: entrada cloud e identidad verificada, sin abrir la autoridad del servidor local.
- firestore_repository: mismas garantías de repositorio/operaciones atómicas sobre estado cloud; ningún acceso privado local.
- cloud_storage: objetos autorizados, identidad/versión/hash, recuperación y límites; no sincronización indiscriminada.
- Nuevos tests: validación real del límite de cada adaptador, con emulación/transporte inyectado y opt-in externo separado.
- requirements.lock: versiones exactas resueltas en entorno autorizado y reproducible; no generar números ficticios.
- RESULTADO-INTEGRAL-ANTIGRAVITY.md: informe final con evidencia y pendientes, no aceptación.

**Prohibidos:** cualquier archivo no listado; contracts/core/**, contracts/runtime/**, app/runtime_contracts.py, AGENTS.md, TEAM-WORKFLOW.md, contrato y fichas aprobadas, corpus REQUISITOS, demos históricas, sus fixtures fuera de lista y bases existentes del usuario. Lectura permitida cuando sea necesaria. No borrar ni limpiar por lotes.

Si un destino nuevo aparece o cambia baseline, revisar trabajo concurrente antes de editar. No crear módulos auxiliares, informes o tests distintos de los listados para sortear el perímetro.

## 6. Ejecución en un único encargo, por bloques

No necesita volver a pedir aprobación de cada bloque cuando Niko haya autorizado este mismo encargo y se cumplan permisos. Una sola persona/herramienta modifica archivos en cada momento.

**A. Estabilizar núcleo existente primero — H01–H03.**
Capturar inventario/hash; reproducir fallos; corregir semántica de revisión/historia sin debilitar contratos. Mantener snapshots originales, aprobación exacta, ledger idempotente y rollback. Cerrar conexiones en finally; no esconder errores de limpieza. Obtener suite local coherente.

**B. Preparar fronteras de datos y evaluación — H06–H11.**
Corregir pruebas mínimas reproducidas, evidencia original, permisos del expediente, aislamiento y evaluación completa. Parser no crea evidencia por sí solo. Datos no autorizados no salen a nube/modelo; no confiar en instrucciones embebidas en documentos. No leer holdout privado durante construcción.

**C. Construcción real de agentes — H04/H05/H14.**
Proveedor ADK; cinco roles con contexto mínimo y esquemas existentes. Chief aclara/planifica/consolida; Research usa fuentes permitidas; Architect y Delivery derivan de resultados; Governance evalúa sin aprobar.
Invocaciones fuera de transacciones durables largas: reservar y registrar intención antes, validar versión al confirmar, conservar inciertos sin repetir. Registrar acción/fuente/salida resumida, jamás pensamiento. Texto facturable interno se cuenta sin conservarlo.
Modo offline sigue SIMULADA; REAL nunca cae silenciosamente al mock. Topes efectivos de entrada/salida y thinking deben verificarse con SDK antes del ensayo y entrar en reserva. No proponer coste basado solo en respuesta visible.

**D. Integrar UI y descarga — H13.**
Los botones usan la ruta real configurada, con errores legibles y modo visible. Estado consultable y recarga recuperable. No permitir que el cliente elija su autoridad o reemplace IDs/huellas aprobadas. Traducción material antes de aprobar; exportación conserva contenido y huella originales. No rehacer diseño por estética.

**E. Preparación cloud — H12/H14.**
Cloud Run escucha en puerto configurado y todas las interfaces del contenedor; local permanece loopback seguro. Quitar dependencia de SQLite/_conn del comportamiento cloud mediante interfaces implementadas, preservando las garantías locales. Firestore maneja transacciones; Storage maneja objetos saneados. Resolver consistencia entre ambos mediante referencias/estado verificables y reintentos idempotentes, nunca simular atomicidad entre servicios.
No ejecutar modelos o herramientas dentro de callbacks Firestore reintentables. Cuota y reserva se consumen una vez. El contenedor no se cierra por el temporizador de demo local.
Autenticación del operador mediante identidad verificada de infraestructura; comprobar firma, emisor, destinatario y caducidad con librería oficial y política explícita. No confiar en headers sin verificar ni publicar un admin local. Visitante solo accede al expediente/demo permitidos. Configuración de identidad/proyecto es precondición, no permiso tácito.

**F. Verificación externa solo tras autorización de Niko.**
Antes de llamar/desplegar presentar recursos, cuenta, región, comando, datos saneados, límites y forma de parar. No crear recursos cloud ni gastar durante un test offline.
Tras permiso: una prueba real acotada, recorrido humano real completo, reinicio cloud, límites/errores y prueba visual de Google Cloud. Mantener acceso de jueces sin exponer gasto/decisiones administrativas.
Si falta permiso, entregar TODO lo offline terminado y una única lista concreta de lo pendiente; no detener otros bloques independientes que sí estén autorizados.

**G. Documentar y devolver a Codex.**
Actualizar archivos de documentación enumerados con un único estado vigente y conservar historia identificada. Informe final por hallazgo, fuentes utilizadas, rutas, hashes, pruebas, versiones, residuos, capacidades reales/simuladas/no verificadas.
No pasar el encargo a Copilot todavía: Codex inspecciona primero, prepara/aplica corrección autorizada si hace falta; Copilot revisa la última versión estable y solo reporta.

Si un bloque exige alterar contratos o más archivos, detener solo esa modificación, explicar la contradicción y continuar lo independiente permitido. No solucionar inseguridad cambiando todo a N/A. No crear nuevas funciones ajenas al contrato para aprovechar el lote.

## 7. Pruebas que deben demostrar el cierre

1. La aprobación del VBP deja iguales contenido/huella de candidato, solicitud, decisión y descarga; versiones operativas posteriores no mutan esos registros.
2. Resultados/evidencia confirmados sobreviven reinicio iguales; no se repiten llamadas ni reservas.
3. Eventos y checkpoints válidos, historia inalterada, lectura no escribe; datos protegidos rechazados/saneados antes de persistir.
4. Actor falso, aprobación vencida/cruzada/obsoleta y replay contradictorio se rechazan sin efectos indebidos.
5. Retirar original antes de aprobar bloquea; después conserva historia y advierte verificabilidad incompleta.
6. Fuente de otra misión no se incluye en expediente; autorización/revocación están ligadas a humano, versión y contenido.
7. JPEG truncado no se acepta; dimensiones positivas/límites, PNG/JPEG decodificables, metadatos saneados. PDF comprimido correcto y DOCX limitado.
8. Primer archivo de misión B no consume cupo de A; traversal por nombre o mission_id bloqueado; archivos idénticos no mezclan propietarios.
9. Lista de dominios vacía deniega; fuentes/redirects/IPv6/metadata no permiten SSRF; límite en bytes, no caracteres. Red deshabilitada por defecto.
10. Salida JSON válida con acción prohibida no pasa evaluación; ni puntuación alta ni palabras PASA/FINALIZADA sustituyen evidencia de trayectoria.
11. Ocho casos de desarrollo y dos holdout evaluados separadamente. Constructor no recibe expectativas holdout; manifest por sí solo no cuenta como ejecución.
12. Cinco roles llaman al modelo con misión/contexto correctos; cambiar entrada cambia resultado. Falla de proveedor no genera sustituto ficticio.
13. Topes de coste/tokens/reintentos efectivos, incluidas llamadas del SDK; timeout conserva reservas y contadores tras reinicio/concurrencia.
14. Sin dependencias, configuración o permisos: no hay llamada. Importar/instanciar y suite offline no salen a Internet.
15. Firestore/Storage probados con clientes/emuladores y luego, si autorizado, evidencia del entorno real; no confundir ambos.
16. UI muestra espera/aprobación/error/evidencia/memoria/descarga y ES/EN fiel; Niko prueba las decisiones humanas y descarga.
17. Suite completa pasa sin borrar tests, xfail/skip artificiales ni relajar contratos. Tests con expectativas inseguras se corrigen preservando el requisito de fondo.
18. Runtime y contenedor arrancan con instrucciones reproducibles, health responde y secretos/bases privadas quedan fuera de imagen y repo.

Comando base: `python -B -m unittest discover -s tests -v`. Ejecutar focales según los archivos del bloque. Capturar stdout/stderr/código real y hashes; no sumar mocks/imports al conteo de llamadas reales.

## 8. Instalación, arranque y efectos

Preparar instalación en entorno aislado; nunca modificar Python de otra aplicación. El lock final se deriva del entorno aprobado. Si falta autorización de instalación, devolver comando y ruta; no instalar globalmente.

Propuestas de raíces locales, a autorizar solo si ausentes: `.venv-cierre-integral` para dependencias, `.review-cierre-integral` para temporales/SQLite y `.artifacts-cierre-integral` para expediente sintético/resultados. No tocar las bases demo existentes. Estas raíces son datos de ejecución, no permiso para fuentes fuera de lista; deben quedar excluidas de publicación. No limpieza masiva.

Se puede preparar todo el código sin credenciales. Antes del primer ensayo real fijar: modelo/API/proyecto/entorno, saldo disponible, presupuesto del ensayo, topes efectivos, dato exacto y confirmación humana. No pedir claves por chat ni leerlas en logs. Instalación, llamadas, despliegue, exposición pública y envío tienen efectos distintos y no se presumen autorizados por «terminar el proyecto».

El corte de entrega sigue siendo 19:00 Ecuador; objetivo de envío 18:30. No garantizar finalizar todo por haber redactado un encargo. Priorizar bloqueadores y ejecución real sobre extras. Informar cuando el camino crítico ya no quepa; nunca reemplazarlo con una simulación presentada como real.

## 9. Formato obligatorio de devolución

En `competition/RESULTADO-INTEGRAL-ANTIGRAVITY.md` y resumido en conversación:
- Versión de trabajo/huella, inventario inicial/final y lista de archivos efectivamente cambiados.
- Tabla H01–H16: RESUELTO/PARCIAL/PENDIENTE, evidencia/AC, limitación y siguiente acción.
- Comandos, entorno, SDK/modelo/parsers, conteos, errores y comparativa contra 280 pruebas iniciales.
- Qué funciona localmente, qué es SIMULADA, qué se verificó con modelo real y qué se verificó en cloud.
- URL/revisión/registro visual si existieron y se autorizó publicarlos; nunca inventar.
- Prueba de aprobaciones manuales y descarga, o pendiente explícito. Tests sintéticos no equivalen a aceptación.
- Riesgos, permisos concretos faltantes y residuos propios con rutas exactas.

No declarar aceptación humana, MVP terminado ni producción. No autoabrir otra ronda. Entregar a Codex para revisión/corrección acotada autorizada y después Copilot revisa finalmente.

## 10. Guion para la revisión final de Copilot

Copilot recibe este encargo, autorización de Niko, informe Antigravity, correcciones Codex y hashes de la versión final. No modifica archivos ni implementa.
Revisar H01–H16, perímetro, pruebas negativas, falsos verdes, privacidad/coste, separación real/simulado, despliegue e instrucciones. Reportar severidad, archivo/línea, reproducción/evidencia, impacto y recomendación. Sin hallazgos no significa aceptación humana; Niko decide el gate 15.7/C.18.

