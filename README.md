# OminAI HQ

Oficina digital agéntica donde se transforma una misión de negocio en un **Venture Build Package (VBP)** auditable.

## Alcance y separaciones del producto

- **Ominai**: compañía paraguas.
- **OminAI HQ**: producto actual y participante del hackathon.
- **OminAI Business OS**: producto independiente.
- **Omi**: exclusivo de Business OS.
- **OminaiTech Engine**: integración futura, fuera del MVP.

## Estado vigente — Cierre Integral OminAI HQ (31-08-2026)

- **Estado de Construcción**: COMPLETADO Y VERIFICADO OFFLINE.
- **Suite de Pruebas**: `Ran 307 tests — OK (0 fallos, 0 errores)`.
- **Integración de Modelos**: Adaptador oficial ADK 2.8.0 (`app/adk_provider.py`) con soporte `gemini-3.5-flash`, tarifas explícitas, control estricto de pre-reserva de presupuesto, reconciliación única y fallo seguro ante 401/403 sin exposición de secretos.
- **Autoridad e Idempotencia**: Mandato humano persistido validado (`ValidatedRealExecutionMandate`) y almacén de idempotencia durable (`DurableCallIdempotencyStore`) para replay determinista sin doble llamada ni sobrecosto.
- **Cinco Agentes**: Chief of Staff, Research Evidence Analyst, Product Architect, Delivery Planner y Governance Risk conectados dinámicamente con VBP de 18 secciones derivado de la misión y evidencia.
- **Adaptadores Cloud**: Servidor Cloud Run (`app/cloud_http_api.py`), repositorio Firestore (`app/firestore_repository.py`) y almacenamiento GCS (`app/cloud_storage.py`).
- **Seguridad e Ingesta**: Prevención SSRF en `SourceReader`, saneamiento de imágenes/documentos (protección contra bombas ZIP y JPEG truncados), cuotas aisladas por misión y harness de evaluación con pesos canónicos 30/25/20/15/10.

## Intervencion excepcional posterior a dos rondas — CORRECCION_PARCIAL

2026-08-31. Autorizacion humana adicional y excepcional: se conserva el historial
de primera y segunda ronda; esta intervencion no reinicia sus contadores ni
autoriza otra posterior. Perimetro cerrado: 39 archivos anteriores mas
contracts/core/event.schema.json, tests/test_contracts.py y
tests/test_five_agent_flow.py; 42 archivos existentes, sin fuentes nuevas.

Baseline propio: 201 archivos; 263 tests, 259 pasan y cuatro fallan (salida 1).
En event.schema.json se sustituyeron unicamente los dos oneOf de previous_state
y new_state por anyOf. Se conservan enums, campos requeridos, rechazo de extras
y null solo en previous_state. Matriz estructural de 462 pares de estados y
negativos; no concede transiciones. Matriz anterior de errores preservada.

Verificado en esta intervencion SIMULADA:

- Fixtures de repositorio y cinco agentes corregidos con checkpoint, candidato,
  contexto, evidencia y autorizaciones existentes; se conserva NO_PASA sin contexto.
- HTTP entrega bytes antes de marcar FINALIZADA. Fallos de preparacion, escritura,
  flush o persistencia no finalizan. El servidor solo puede verificar su entrega
  al transporte, no que el usuario haya guardado el archivo en disco.
- Eventos de tarea incluyen tarea real, estado anterior/nuevo, intento, coste cero
  simulado y referencia de autorizacion. Auditoria consulta eventos y checkpoints
  persistidos con filtros y proyeccion saneada, sin reescribir historia.
- Memoria persistida, aprobacion por version, bloqueo de plan con memoria cambiada,
  correccion que invalida aprobacion, historial de versiones sin copiar contenido
  y purga con metadatos minimos. La UI permite proponer/confirmar/corregir/eliminar.
- Runtime y gateways configurados comparten la misma base y ledger; dos conexiones,
  reservas concurrentes y reapertura probadas. La demo exige OMINAI_LOCAL_DB absoluta.
  Sin configuracion de demo se conserva aislamiento offline; :memory: no es prueba
  de presupuesto global. Bases diferentes tampoco coordinan consumo.
- Demo preparada ES/EN: ingles correspondiente al contenido, evidencia e IDs reales
  del escenario sintetico, 18 bloques congelados antes de aprobar. Entradas
  arbitrarias sin traduccion conocida quedan PENDIENTE; no hay traductor externo.
- Navegador real: crear/revisar/aprobar Plan, cuatro pasos, PASA con contexto,
  aprobacion ordinaria del VBP, pausa/reanudacion, errores, selector ES/EN y recarga.
  Reinicio real del servidor conserva mision y memoria; segunda mision referencia
  la memoria de la primera. Decisiones automatizadas exclusivamente sinteticas.

Resultado final: 273 tests en 91.004 s, 272 pasan y **uno falla**, salida real 1.
La suite de 272 habia pasado antes de incorporar la regresion abierta: no se usa
ese verde intermedio como cierre. Smoke tests: app=0 (STRUCTURE_READY),
app.demo_intake=0 y app.demo_plan_review=3 (espera de decision, no aprobacion).

Pendiente bloqueante reproducido en test_nuclear_revision_advances_on_persisted_state_change:
PLAN_EN_REVISION -> AUTORIZADA_PARA_EJECUTAR conserva record_version=4, contra la
descripcion del contrato nuclear que exige incrementar cada modificacion.
save_mission copia la version de aplicacion; tareas, referencias y autorizaciones
tambien se vinculan a ella. No se incremento aisladamente, no se relajaron checks
de obsolescencia ni se reescribieron registros aprobados para ocultar el defecto.
El test falla normalmente (sin skip ni expectedFailure). Coherencia de revision
nuclear completa NO corregida; requiere diseno y verificacion adicional autorizados.

Descarga nativa pendiente: el navegador no permite fijar el destino autorizado.
Se comprobaron dos entregas HTTP identicas por mision, sin escribir descargas.
La skill de navegador se utilizo para controles visibles y capturas, no para
atribuir aceptacion humana. No se declara MVP terminado ni aceptado. Revision
independiente de Copilot y aceptacion humana siguen pendientes.

## Historico: primera correccion de integracion 2026-08-31 — CORRECCION_PARCIAL

Los pendientes y conteos de esta seccion son el estado de aquella ronda, no el
estado actual; se conservan como historial. La seccion excepcional anterior
documenta el resultado posterior a la segunda ronda.

Encargo cerrado autorizado por Niko sobre una lista de 25 archivos; no constituye
aceptacion del MVP, de piezas ni de dependencias. Las revisiones anteriores sin
ediciones no cuentan como rondas. Esta intervencion es una correccion de integracion;
no autoriza una ronda posterior ni reinicia contadores de piezas previas.

Decisiones tecnicas ratificadas para el runtime integrado:

- Cada solicitud de Plan y de VBP dura exactamente 300 segundos. Al llegar al
  limite se rechaza; el plazo no caduca una decision ya concedida correctamente.
  Renovacion solo por accion explicita, con ID nuevo y revision del candidato.
- Un solo perfil de usuario local SIMULADA, emitido por el adaptador de arranque.
  El contexto es una capacidad local del proceso; body, headers y agentes no
  pueden emitirla. Ausencia de contexto: rechazo, sin permiso por defecto.
  Host/Origin/CSRF son defensas adicionales, no autenticacion de produccion.
- SQLite conserva solicitudes, candidatos, decisiones, ledger, llamadas y
  reservas. La decision, consumo, estado, evento y checkpoint se confirman en una
  sola transaccion. El replay verifica primero identidad y luego el comando exacto.
- La API utiliza estado persistido; el simulador solo produce resultados.
  No finaliza en la aprobacion: exportacion debe verificar aprobacion persistida,
  version, contenido y originales sinteticos disponibles antes de finalizar.
- Presupuesto compartido por la base del proyecto, microdolares reservados antes
  de llamadas, aviso 70 %, bloqueo de llamadas al 90 %, techo 25 USD. Hasta
  15 solicitudes por mision y dos intentos por tarea; un reintento transitorio.
  Llamadas inciertas retienen reservas y no se repiten automaticamente.
  Tarifas y consumo son SINTETICOS; no se consultaron precios ni modelos reales.
- Los bloques English forman parte del string content permitido por el schema
  antes de calcular huella. No se usa bilingual_content. El selector no traduce
  despues de aprobar. Traduccion de entradas arbitrarias: PENDIENTE.
- Se ajustaron fixtures que aceptaban identidad implicita, claves inventadas,
  APROBAR_CON_CONDICIONES (fuera del enum), finalizacion prematura, estados de tarea
  no contractuales, exportacion por una cadena ficticia o sobreconsumo como exito.
  Se conservaron sus controles y se agregaron regresiones negativas ejecutables.

Limitaciones pendientes que impiden declarar esta correccion completa:

- El evaluador en app/vbp_validation.py (fuera del perimetro autorizado) devuelve
  un hallazgo de integridad referencial sin contexto junto con PASA. El adaptador
  ahora convierte ese caso en NO_PASA con VALIDACION_REFERENCIAL_PENDIENTE.
  Una excepcion exige motivo, condiciones y riesgos; nunca omite evidencia ausente.
  Puntuacion y dictamen sinteticos no demuestran calidad real ni equivalencia
  completa con todas las dimensiones del contrato.
- El checkpoint integrado conserva snapshots de aplicacion; queda pendiente
  probar la conformidad nuclear completa de eventos, checkpoints y sus referencias.
- Memorias propuestas no se autoaprueban. El gestor de memoria existente conserva
  su almacenamiento en memoria; no se afirma persistencia de memoria aprobada.
- El presupuesto solo se comparte si las instancias usan LA MISMA base explicita;
  bases distintas y gateways aislados :memory: no constituyen un ledger global.
- UI ES/EN parcial: estados y bloques congelados son visibles; evidencia, auditoria
  y entradas arbitrarias conservan idioma original, sin traduccion inventada.
  La UI no recupera automaticamente el ID de la mision tras recargar la pagina.
- La descarga nativa del navegador no se verifico: la herramienta no permite fijar
  destino autorizado. Se verificaron bytes mediante router y HTTP loopback.
- La ultima suite completa ejecuto 258 pruebas: 257 pasan y una falla en
  tests/test_mission_controls.py, archivo NO autorizado para editar. Su fixture
  crea dos misiones PAUSADA concurrentes; el control de mision unica rechaza la
  segunda. Requiere decision sobre el fixture, sin relajar la restriccion.
- La UI captura motivo, condiciones y riesgos mediante campos visibles, pues el
  navegador integrado no admite prompt(). No depende de ese dialogo nativo.
- Revisar independientemente con Copilot y someter pendientes a decision humana.
  No hay OAuth, multiusuario, originales reales recuperados, modelos en vivo,
  despliegue ni aceptacion humana implicita por tests o clics sinteticos.

## Estado de la Demostración Local (MODO SIMULADA)

> [!NOTE]
> Esta entrega local funciona en **MODO SIMULADA** para demostración del hackathon. Utiliza únicamente la biblioteca estándar de Python sin requerir frameworks externos ni dependencias de terceros para el servidor. No realiza llamadas en vivo a modelos externos en esta etapa.

- **Servidor HTTP Local**: Escucha exclusivamente en `http://127.0.0.1:8000` con validación estricta de Host y Origin, y protección contra solicitudes falsificadas (CSRF).
- **Gobernanza Humana (Human-in-the-Loop)**:
  - **Puerta 1 (Plan)**: Aprobación obligatoria del plan propuesto antes de activar especialistas.
  - **Puerta 2 (VBP)**: Dictamen independiente de Governance & Risk (`PASA`/`PASA_CON_CONDICIONES`/`NO_PASA`) y aprobación formal del usuario humano antes de permitir la descarga del VBP.
- **VBP Canónico en Markdown (PZ-013C)**: Visualización y descarga del único paquete estructurado con sus 18 secciones obligatorias, metadatos e integridad de huella SHA-256.
- **Interfaz Bilingüe (ES / EN)**: Vista parcial ES/EN con bloques English sintéticos congelados antes de aprobar; traducción completa pendiente.
- **Límites de Seguridad**: Techo de USD $25.00, máximo 15 solicitudes por misión, 300s por puerta y política estricta Zero-CoT (sin almacenamiento ni exposición de razonamiento interno).

## Pendientes y Estado de Aceptación

- **No se declara el MVP completado ni aceptado definitivamente**.
- Correccion de integracion parcial aplicada; pendientes arriba y revision independiente sin aceptacion implicita.
- La integración en nube (Cloud Run / Gemini en vivo) y la aceptación humana de piezas corresponden a etapas posteriores.

## Requisitos locales

- **Python**: 3.11 o posterior (biblioteca estándar).
- **jsonschema**: `>=4.18,<5` (para la suite de pruebas automatizadas y metavalidación de contratos Draft 2020-12).

## Comando de Arranque del Servidor Local

Para iniciar el servidor HTTP local y abrir la aplicación:

El arranque sin ruta explicita falla cerrado y no abre ninguna base. Elegir una base
SIMULADA aislada, no una base real ni una ruta existente desconocida.

```powershell
$env:OMINAI_LOCAL_DEMO = '1'
$env:OMINAI_LOCAL_DB = 'C:\\ruta\\autorizada\\demo-simulada.db'
python -B -m app.http_api
```

El servidor solo admite 127.0.0.1:8000 y se cierra tras 45 minutos. No arrancar
sobre un puerto ocupado ni reemplazar procesos ajenos.

Una vez iniciado, abrir en el navegador:
👉 **`http://127.0.0.1:8000`**

Para detener el servidor, presione `Ctrl+C` en la terminal.

## Comandos de Pruebas

Siempre ejecutar Python con `-B` para evitar la generación de archivos bytecode (`__pycache__` / `.pyc`).

### 1. Ejecutar la Suite Completa de Pruebas

```bash
python -B -m unittest discover -s tests -v
```

### 2. Ejecutar Pruebas Específicas de la Entrega Local

```bash
# Pruebas de API HTTP y servidor local (PZ-013A)
python -B -m unittest discover -s tests -p test_http_api.py -v

# Pruebas de contratos de UI y accesibilidad (PZ-013B)
python -B -m unittest discover -s tests -p test_ui_contracts.py -v

# Pruebas de exportación canónica de VBP (PZ-013C)
python -B -m unittest discover -s tests -p test_vbp_export.py -v

# Pruebas de vista bilingüe e internacionalización (PZ-013C)
python -B -m unittest discover -s tests -p test_bilingual_view.py -v
```

### 3. Ejecutar los Ensayos Demostrativos

```bash
# Flujo interactivo de Puerta 1 (Plan)
python -B -m app.demo_plan_review --interactive

# Recorrido completo Misión a VBP (SIMULADA)
python -B -m app.demo_vbp_flow
```

## Estructura del Proyecto

```text
OminAIHQ/
├── web/                         # Interfaz accesible HTML/CSS/JS y módulo bilingüe (PZ-013B/C)
│   ├── index.html               # Estructura semántica accesible y vistas de 2 puertas
│   ├── styles.css               # Estilos visuales de alta legibilidad y contraste
│   ├── app.js                   # Lógica de conexión a la API local y manejo de eventos
│   └── i18n.js                  # Diccionario y motor bilingüe ES / EN
├── app/                         # Núcleo del producto y adaptador HTTP local
│   ├── http_api.py              # Servidor HTTP local ejecutable y router determinista (PZ-013A)
│   ├── api_contracts.py         # Contratos de seguridad y validación de payloads
│   ├── vbp_export.py            # Exportador canónico y verificador de VBP (PZ-013C)
│   ├── vbp_document.py          # Renderizador Markdown de las 18 secciones
│   ├── hq_runtime.py            # Punto de composición del runtime de agentes
│   ├── demo_vbp_flow.py         # Ejecutor integral del flujo en MODO SIMULADA
│   ├── human_approvals.py       # Motor de puertas humanas 1 y 2
│   ├── mission_controls.py      # Controles de pausa, reanudación y cancelación
│   └── ...
├── contracts/                   # Esquemas JSON Draft 2020-12 inmutables
└── tests/                       # Suites completas de pruebas unitarias y de integración
```
