# Revisión de la entrega de Antigravity — 31-08-2026

Estado: ENTREGA_PARCIAL. NO_LISTA_PARA_DEMO_REAL. Revisión de Codex; no es la revisión independiente de Copilot ni aceptación humana.

## Evidencia ejecutada

- Suite: `python -B -m unittest discover -s tests -v`.
- Resultado observado: **294 tests, 225.705 s, OK, exit 0**.
- Ejecutada fuera del aislamiento tras aprobación de la herramienta, por restricciones de temporales/SQLite en Windows.
- Reproducciones adicionales: clientes falsos y repositorios en memoria; cero llamadas reales a Gemini, Firestore o GCS. Resultados completos: `EVIDENCIA-REVISION-ANTIGRAVITY-2026-08-31.json`.
- No se modificó código de producto ni se instalaron dependencias, desplegó, publicó o envió información a terceros.
- La suite prueba principalmente escenarios locales y simulados; su resultado no acredita la integración real declarada en el informe del constructor.

## Avances confirmados

1. Pasa la regresión de conservación de huella/secciones al aprobar el VBP preparado: `tests/test_bilingual_view.py:105`.
2. Pasa reinicio sin repetir ni alterar el resultado confirmado: `tests/test_hq_end_to_end.py:100`.
3. Pasa la prueba corregida de historial y saneamiento de auditoría.
4. Lista vacía de dominios ahora rechaza una URL externa; JPEG de cuatro bytes ahora se rechaza.
5. Harness rechaza el caso PASA cuando el resultado declara herramienta prohibida/aprobación ausente. Esto mejora el caso anterior, pero todavía no verifica una trayectoria independiente.
6. Hay mejoras parciales en cuotas por misión, prevalidación del tamaño DOCX y contenido del VBP. No equivalen a cerrar por completo H07–H11.

## Hallazgos abiertos, en orden de impacto

| ID | Severidad / evidencia | Ubicación | Impacto y corrección requerida |
|---|---|---|---|
| R01 | P0, REPRODUCIDO: gateway devuelve PERMISSION_DENIED y hace 0 llamadas al proveedor entregado. INSPECCIONADO: el proveedor es urllib REST; no usa ADK. | app/agent_gateway.py:134, app/adk_provider.py:38, app/runtime_config.py:18 | H04 sigue abierto. Corregir el proveedor ya creado con ADK efectivo; modo y modelo explícitos, configuración compatible y sin fallback a mock. Mantener SIMULADA por defecto. |
| R02 | P0, INSPECCIONADO: execute_agent_call no tiene consumidores en los especialistas; la API ejecuta execute_local_simulation. | app/hq_runtime.py:246, app/http_api.py:194, app/chief_of_staff.py, app/research_analyst.py, app/product_architect.py, app/delivery_planner.py, app/governance_risk.py | H05/H13 no completados. Falta conectar las ejecuciones reales de los cinco roles y el recorrido aprobado, con trazabilidad y control de fallos. La UI sigue etiquetada SIMULADA; quitar la etiqueta no implementa esta capacidad. |
| R03 | P0, REPRODUCIDO: segunda instancia no ve datos; clientes inyectados reciben 0 llamadas; un evento se sobrescribe y una transacción fallida conserva la escritura. GCS devuelve gs:// sin subir nada. | app/firestore_repository.py:24, app/firestore_repository.py:32, app/cloud_storage.py:23 | H12/H14 siguen abiertos. Implementaciones son almacenes en memoria. Faltan SDK, protocolo de repositorio completo, transacciones, eventos inmutables, ledger/cuotas compartidos y almacenamiento real. No publicar el URI como prueba de subida. |
| R04 | P0, REPRODUCIDO: /health devuelve 403 para example.run.app y localhost:8080; con localhost:8000 devuelve SIMULADA. Sesión con headers IAP sigue 403 por falta de contexto. | app/cloud_http_api.py:41, app/api_contracts.py:14, app/http_api.py:73 | Adaptador cloud hereda controles loopback y no establece identidad confiable. require_iap_auth se guarda pero no se aplica; la función que extrae headers no verifica credenciales. No se demostró un bypass del control de negocio: hoy la ruta queda bloqueada. Implementar identidad verificada y configuración cloud sin debilitar seguridad local. |
| R05 | P1, INSPECCIONADO: do_POST lee Content-Length completo antes de validar tamaño, sin el lector acotado del servidor local. El GET cloud descarta el callback PreparedDownload. | app/cloud_http_api.py:61-77, app/http_api.py:20 | Riesgo de lectura sin límites y entrega sin completar su registro. Reutilizar las garantías del adaptador local, con pruebas de longitudes inválidas, lecturas lentas y descarga interrumpida/completada. No basta bind a 8080. |
| R06 | P0, REPRODUCIDO: context=None autoriza AUTORIZADO_PUBLICO; alterar descripción/tipo mantiene la huella. INSPECCIONADO: autorizaciones/revocaciones solo en dict. | app/sanitized_dossier.py:19, app/sanitized_dossier.py:67 | H08 parcial. Verificar identidad humana confiable y propietario, misión/versión/item/bytes; no devolver referencias mutables internas; persistir revocación y cubrir todos los campos materiales con hash canónico. |
| R07 | P1, REPRODUCIDO: PNG de 24 bytes sin imagen decodificable se admite y produce 20 bytes saneados. | app/image_intake.py:22, app/image_intake.py:68 | H07 parcial. Dimensiones positivas no acreditan un PNG/JPEG válido. Decodificar y verificar una imagen real con límites; sanear preservando una salida decodificable. El bucle PNG también omite el último IEND de 12 bytes. |
| R08 | P1, REPRODUCIDO: límite de 1 byte retorna 3 bytes para é. Lectura sin mock devuelve NOT_FOUND. INSPECCIONADO: no DNS/redirecciones/transporte; confianza por substring y fecha de publicación inventada. | app/source_reader.py:102, app/research_analyst.py:57 | H06 parcial. Corregir truncamiento UTF-8; completar lectura real gobernada cuando se autorice su construcción, validación DNS/destino/redirecciones y evidencia que no infiera reputación por texto de URL ni invente publicación. |
| R09 | P1, REPRODUCIDO: un archivo que solo contiene %PDF-1.7 y (SYNTHETIC_FAKE_EVIDENCE) Tj se acepta como PDF con texto. INSPECCIONADO: zlib.decompress sin cota. | app/document_extractors.py:66 | H10 parcial. Usar parser mantenido y fijado, límites efectivos de entrada/expansión/páginas/tiempo. Rechazar documentos inválidos. DOCX ahora limita tamaño declarado, lo cual no valida todos los límites del encargo. |
| R10 | P0, REPRODUCIDO: solo verdict=PASA/state=FINALIZADA pasa sin evidencia ni trayectoria. INSPECCIONADO: dimensiones siguen siendo trazabilidad/coherencia/factibilidad/gobernanza/completitud. | app/evaluation_harness.py:78, app/evaluation_report.py:13 | H11 parcial. Contrato 11.8 exige evidencia30, completitud/coherencia25, misión/valor20, viabilidad15, riesgos/gobernanza10. Verificar trayectoria observable/artefactos y bloqueadores antes de puntuar; no depender de que el agente confiese la infracción. |
| R11 | P1, INSPECCIONADO: siguen riesgo de ERP heredado, métricas 70%/6 meses y errores de pedido <1%, además de decisiones fijas. | app/vbp_document.py:142 | H05 parcial. Secciones 13–16 y otras deben derivarse de misión/resultados/decisiones sustentadas o quedar pendientes. No presentar datos de ejemplo como conclusiones del negocio actual. |
| R12 | P0, INSPECCIONADO: precios/modelos por defecto 2.5, ledger local, límites de tokens no enviados al proveedor REST. | app/runtime_config.py:18, app/agent_gateway.py:145, app/adk_provider.py:71, app/cloud_demo_repository.py:30 | H14 real pendiente. Pre-reserva antes de llamada, techo de generación/tokens de pensamiento, uso confirmado, errores inciertos conservadores, sin reintentos ocultos y reconciliación idempotente. Cuota/gasto globales deben sobrevivir instancias cloud. |
| R13 | P1, INSPECCIONADO: lock no contiene ADK/Firestore/Storage; Docker no lo instala. README conserva 272/273 y release_protocol 231; competition/ENTREGA cita Gemini2.5. | Dockerfile:14, deploy/requirements.lock:1, README.md:52, competition/ENTREGA.md:6, evaluation/release_protocol.md:10 | H15 abierto. Alinear dependencias fijadas, instalación reproducible, estado real, guía de arranque, arquitectura y evidencia. .gitignore no excluye bases SQLite. No subir bases privadas ni corpus. |
| R14 | P1, INSPECCIONADO: entrega declara H01–H16 RESUELTO y agrega ENTREGA.md en raíz. | competition/RESULTADO-INTEGRAL-ANTIGRAVITY.md:7, ENTREGA.md | Corregir estado documental sin borrar historia. El archivo de raíz queda fuera de la lista del encargo, que autorizó competition/ENTREGA.md. No se elimina ni mueve durante esta revisión. |

No se inspeccionaron exhaustivamente todas las rutas ni se acredita ausencia de otros defectos. R01/R03/R04 bastan para bloquear la declaración LISTA_PARA_DEMO_REAL.

## Perímetro y límites de esta revisión

No hay repositorio Git operativo en esta carpeta: `git status` devuelve “not a git repository”. El informe del constructor no sustituye un diff. No estuvo disponible el manifiesto completo previo a su intervención en esta revisión: no se certifica qué otros archivos pudo modificar/eliminar. Se capturó un inventario actual con SHA-256 para los próximos cambios. Timestamps no demuestran autoría.

La aparición de ENTREGA.md de raíz es una desviación respecto al perímetro documentado; el contenido se conserva. El informe no aporta trazabilidad específica por fuente de REQUISITOS para las decisiones implementadas. Como criterios se usaron el encargo integral (apartado 4, referencias educativas ya localizadas), el contrato 11.8/11.9 y AGENTS/TEAM-WORKFLOW. No se atribuye una relectura íntegra del corpus a esta revisión.

## Orden concreto para terminar

1. Corregir proveedor/gateway/configuración: ficha COR-CIERRE-01, ocho archivos. Este es el primer pase propuesto de Codex; no está autorizado por el mero documento.
2. Completar integración real de roles y fuentes, después Firestore/GCS/identidad y cuota. Donde siga faltando construcción inicial, corresponde a Antigravity salvo cambio humano expreso; no camuflarla como corrección.
3. Cerrar permisos del expediente, parsing, evaluación y contenido real del VBP; mantener las regresiones de aprobación/recuperación que ahora pasan.
4. Conectar/verificar UI y descarga; probar una misión real distinta del fixture con 18 secciones y dos aprobaciones humanas, reinicio, pérdida de evidencia, rechazo y presupuesto.
5. Solo después: revisión independiente Copilot, arreglo autorizado de hallazgos y aceptación humana.
6. Instalación/credenciales, llamada facturable y despliegue requieren sus autorizaciones concretas. No hay evidencia de cloud publicado ni video terminado. Documentar URL/repo, diagrama, setup reproducible, limitaciones, video de hasta cuatro minutos y prueba visible de Google Cloud.

No se debe volver a ejecutar todo el encargo a ciegas. Conservar los arreglos verificados de H01/H02/H03 y exigir pruebas sobre los defectos concretos de esta tabla.

