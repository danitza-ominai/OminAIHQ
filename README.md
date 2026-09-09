# OminAI HQ

Oficina digital agéntica donde se transforma una misión de negocio en un **Venture Build Package (VBP)** auditable.

## Alcance y separaciones del producto

- **Ominai**: compañía paraguas.
- **OminAI HQ**: producto actual y participante del hackathon.
- **OminAI Business OS**: producto independiente.
- **Omi**: exclusivo de Business OS.
- **OminaiTech Engine**: integración futura, fuera del MVP.

## Estado técnico vigente (2026-09-02)

- **Versión técnica:** `0.1.0`, coincidente en `pyproject.toml`, el paquete Python y `/health`.
- **Suite automatizada más reciente:** `308/308` pruebas pasan en el entorno funcional local.
- **Alcance demostrado:** recorrido local etiquetado `SIMULADA`; las pruebas no constituyen aceptación humana integral del MVP.
- **Verificado localmente:** runtime HTTP de loopback, interfaz web, persistencia SQLite, puertas de aprobación humana controladas, ejecución secuencial simulada, auditoría, memoria local, evaluación automatizada y exportación canónica del VBP.
- **Adaptadores presentes:** Google ADK, entrada HTTP orientada a Cloud Run, repositorio Firestore y almacenamiento Cloud Storage. Su código y sus pruebas offline usan ejecutores inyectados, dobles o almacenamiento en memoria; no demuestran una integración real ni un despliegue.
- **Estado de entrega:** `NO_CERRADO`. No se declara el MVP completo, listo para producción ni aceptado integralmente.

`app/__main__.py` conserva su salida mínima `STRUCTURE_READY` con
`implemented_capabilities=[]`; esa salida es un smoke test de estructura y no un
inventario de las capacidades verificadas por otras pruebas.

### Capacidades verificadas en modo local `SIMULADA`

- Creación y recuperación de misiones en SQLite con estado, eventos, checkpoints y controles de reanudación.
- Revisión del plan y del VBP mediante dos puertas humanas separadas, vinculadas a identidad, versión y huella.
- Flujo secuencial de especialistas con resultados sintéticos, límites finitos y bloqueo seguro ante errores.
- Consulta de evidencia, memoria y auditoría sin exponer Chain-of-Thought.
- Generación, validación de integridad y exportación Markdown del VBP de 18 secciones.
- Harness de evaluación reproducible con casos adversariales, checksum del dataset y separación declarada del holdout.

### Adaptadores existentes sin evidencia real

- `app/adk_provider.py` contiene el límite de integración para Google ADK y Gemini; sus pruebas son offline y emplean eventos o ejecutores inyectados. **No hay evidencia de una llamada Gemini en vivo.**
- `app/cloud_http_api.py` contiene un punto de entrada HTTP compatible con el entorno esperado de Cloud Run. **No hay evidencia de un servicio desplegado en Cloud Run.**
- `app/firestore_repository.py` acepta un cliente, pero su implementación actual conserva datos en diccionarios del proceso. **No hay evidencia de persistencia real en Firestore.**
- `app/cloud_storage.py` acepta un cliente, pero guarda bytes en memoria. **No hay evidencia de escritura real en Google Cloud Storage.**
- El `Dockerfile` y los manifiestos de ejemplo describen un empaquetado posible; no son evidencia de build publicado, despliegue ni operación real.

### Pendientes principales

- `PENDIENTE_DE_EVIDENCIA_REAL`: ejecución controlada con Gemini/ADK y credenciales autorizadas.
- `PENDIENTE_DE_EVIDENCIA_REAL`: build y despliegue observables en Cloud Run.
- `PENDIENTE_DE_EVIDENCIA_REAL`: persistencia y recuperación contra Firestore y Cloud Storage reales.
- `PENDIENTE`: matriz ejecutable que relacione todos los RF, RNF y CT aplicables con evidencia reproducible.
- `PENDIENTE`: revisión independiente y aceptación humana integral; las aceptaciones registradas hasta ahora corresponden a piezas concretas.

## Historial de verificaciones — no representa el estado actual

Los conteos siguientes se conservan únicamente como trazabilidad de ejecuciones
anteriores. Fueron superados por la suite vigente de `308/308` y no deben usarse
para describir el estado técnico actual:

- 2026-08-30: `231` pruebas pasaban en el corte de protocolo de release de esa fecha.
- 2026-08-31: una ejecución de `258` pruebas terminó con 257 aprobadas y una falla.
- 2026-08-31: una ejecución de `273` pruebas terminó con 272 aprobadas y una falla.
- 2026-08-31: una entrega intermedia registró `294/294` pruebas.
- 2026-08-31: el cierre técnico previo registró `307/307` pruebas.

<details>
<summary><strong>Detalle técnico histórico del 2026-08-31 — no vigente</strong></summary>

> **Advertencia:** este bloque resume cortes anteriores del 2026-08-31. No
> describe defectos actuales confirmados, no reemplaza el resultado vigente de
> `308/308` y no constituye una declaración de cierre o aceptación del MVP.

### Perímetro y carácter de las correcciones

- La primera corrección de integración tuvo un perímetro cerrado de 25 archivos.
  No constituyó aceptación del MVP, de sus piezas ni de sus dependencias.
- Una intervención posterior fue autorizada excepcionalmente después de dos
  rondas. Conservó los contadores anteriores y se limitó a 42 archivos existentes:
  los 39 del perímetro previo más `contracts/core/event.schema.json`,
  `tests/test_contracts.py` y `tests/test_five_agent_flow.py`, sin fuentes nuevas.
  Esa autorización no reinició rondas ni autorizó otra intervención.

### Decisiones técnicas registradas en esos cortes

- Las solicitudes de aprobación de Plan y VBP tenían TTL de 300 segundos. Al
  vencer se rechazaban; renovarlas exigía una nueva acción humana, un ID nuevo y
  revisar nuevamente el candidato. Una decisión ya concedida correctamente no
  caducaba de forma retroactiva.
- El contexto humano local era emitido por el adaptador de arranque y no podía
  otorgarse mediante el body, headers o agentes. Host, Origin y CSRF eran defensas
  adicionales, no autenticación de producción.
- SQLite conservaba solicitudes, candidatos, decisiones, ledger, llamadas y
  reservas. Decisión, consumo, estado, evento y checkpoint se confirmaban en una
  transacción, y el replay validaba identidad y comando antes de devolver efectos.
- El presupuesto histórico usaba un techo de USD 25, aviso al 70 %, bloqueo de
  nuevas llamadas al 90 %, máximo de 15 solicitudes por misión, dos intentos por
  tarea y un reintento transitorio. Las llamadas inciertas retenían la reserva y
  no se repetían automáticamente. Tarifas y consumo seguían siendo sintéticos.
- La entrega HTTP de bytes se distinguía de una descarga nativa: una escritura,
  flush o persistencia fallida no finalizaba la misión. Las verificaciones de ese
  corte demostraron bytes repetibles por HTTP, no que el usuario hubiera guardado
  el archivo mediante una descarga nativa del navegador.

### Limitaciones y resultados que pertenecían a esos cortes

- La evaluación referencial podía recibir de `app/vbp_validation.py` un hallazgo
  de integridad junto con `PASA`; el adaptador lo convertía en `NO_PASA` con
  `VALIDACION_REFERENCIAL_PENDIENTE`. Los puntajes sintéticos no demostraban
  calidad real ni cobertura completa del contrato.
- Se documentó que faltaba demostrar la conformidad nuclear completa de eventos,
  checkpoints y referencias. Un corte también registró memoria en proceso sin
  prueba de persistencia; otro corte posterior registró pruebas de versionado y
  persistencia. Estas observaciones cronológicas no describen el estado vigente.
- La vista ES/EN era parcial: las entradas arbitrarias sin traducción conocida
  quedaban pendientes, no existía traductor externo y la interfaz no recuperaba
  automáticamente el ID de misión al recargar, aunque otro recorrido documentó
  conservación de misión y memoria tras reiniciar el servidor.
- La descarga nativa continuó sin demostrarse en esos cortes; solo se verificaron
  los bytes mediante router y HTTP loopback.
- Una suite de 258 pruebas terminó con 257 aprobadas y una falla porque un fixture
  intentaba mantener dos misiones `PAUSADA` activas simultáneamente.
- Una suite posterior de 273 pruebas terminó con 272 aprobadas y una falla porque
  la transición `PLAN_EN_REVISION -> AUTORIZADA_PARA_EJECUTAR` no incrementaba
  `record_version` como exigía el contrato nuclear de ese corte.
- Pruebas verdes, controles visibles o clics sintéticos nunca se consideraron
  aceptación humana. La revisión independiente y la decisión humana se mantenían
  separadas de la evidencia automatizada.

</details>

Estos resultados históricos no significan cierre integral, preparación para
producción, despliegue real ni aceptación humana del MVP completo.

## Estado de la Demostración Local (MODO SIMULADA)

> [!NOTE]
> Esta entrega local funciona en **MODO SIMULADA** para demostración del hackathon.
> La capa de transporte HTTP local usa la biblioteca estándar de Python; el
> runtime y la validación requieren Python 3.11 o posterior y
> `jsonschema>=4.18,<5`. La demostración local no realiza llamadas en vivo a
> modelos externos.

- **Servidor HTTP Local**: Escucha exclusivamente en `http://127.0.0.1:8000` con validación estricta de Host y Origin, y protección contra solicitudes falsificadas (CSRF).
- **Gobernanza Humana (Human-in-the-Loop)**:
  - **Puerta 1 (Plan)**: Aprobación obligatoria del plan propuesto antes de activar especialistas.
  - **Puerta 2 (VBP)**: Dictamen independiente de Governance & Risk (`PASA`/`PASA_CON_CONDICIONES`/`NO_PASA`) y aprobación formal del usuario humano antes de permitir la descarga del VBP.
- **VBP Canónico en Markdown (PZ-013C)**: Visualización y descarga del único paquete estructurado con sus 18 secciones obligatorias, metadatos e integridad de huella SHA-256.
- **Interfaz Bilingüe (ES / EN)**: Vista parcial ES/EN con bloques English sintéticos congelados antes de aprobar; traducción completa pendiente.
- **Límites de Seguridad**: Techo de USD $25.00, máximo 15 solicitudes por misión, 300s por puerta y política estricta Zero-CoT (sin almacenamiento ni exposición de razonamiento interno).

## Pendientes y Estado de Aceptación

- **No se declara el MVP completado ni aceptado definitivamente**.
- La evidencia vigente es local y `SIMULADA`; los pendientes técnicos se enumeran arriba.
- La integración real en nube (Gemini/ADK, Cloud Run, Firestore y Cloud Storage) y la aceptación humana integral corresponden a etapas posteriores; las aceptaciones existentes son por pieza.

## Requisitos locales

- **Python**: 3.11 o posterior.
- **jsonschema**: `>=4.18,<5` (requerido por el runtime, la validación y la suite de pruebas automatizadas para los contratos Draft 2020-12).

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

