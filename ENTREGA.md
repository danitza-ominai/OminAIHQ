# OminAI HQ - Estado de entrega técnica v0.1.0

Fecha de corte: 2026-09-02.

## 1. Resumen ejecutivo

OminAI HQ transforma una misión empresarial en un Venture Build Package (VBP)
canónico, auditable y exportable. La evidencia actual demuestra un recorrido
local en modo `SIMULADA`; no demuestra una operación productiva ni una
integración real con servicios externos.

La suite completa más reciente pasa `308/308` pruebas en el entorno funcional
local. Este resultado es evidencia automatizada de la versión evaluada, no una
aceptación humana integral del MVP.

## 2. Verificado localmente en `SIMULADA`

- Runtime HTTP restringido a loopback e interfaz web local.
- Persistencia SQLite de misiones, decisiones, eventos, checkpoints y presupuesto.
- Dos puertas de aprobación humana separadas para Plan y VBP.
- Flujo secuencial simulado, pausa/reanudación, auditoría y memoria local.
- Evaluación automatizada reproducible y controles adversariales.
- Validación de integridad y exportación Markdown del VBP aprobado.

Estado de esta evidencia: `VERIFICADO_EN_SIMULADA`.

## 3. Adaptadores presentes, sin verificación real

- `app.adk_provider` implementa el límite de integración con Google ADK/Gemini,
  pero las pruebas usan credenciales sintéticas y ejecutores inyectados; no hubo
  llamada a Gemini en vivo.
- `app.cloud_http_api` es un punto de entrada existente orientado a Cloud Run;
  ejecutar o importar ese módulo no prueba que exista un despliegue.
- `app.firestore_repository` y `app.cloud_storage` exponen adaptadores, pero la
  implementación y las pruebas observadas usan almacenamiento en memoria; no
  prueban Firestore ni Google Cloud Storage reales.
- El `Dockerfile` y la configuración de ejemplo son artefactos de empaquetado, no
  evidencia de una imagen publicada o de un servicio operativo.

Estado de estas integraciones: `PENDIENTE_DE_EVIDENCIA_REAL`.

## 4. Pendiente antes de release o despliegue

- Demostrar de forma reproducible una llamada autorizada a Gemini mediante ADK.
- Construir y verificar la imagen, y demostrar un despliegue real en Cloud Run.
- Verificar persistencia y recuperación con Firestore y Cloud Storage reales.
- Mantener una matriz ejecutable de cobertura para los RF, RNF y CT aplicables.
- Completar revisión independiente y aceptación humana integral del MVP.

Estado global de entrega: `NO_CERRADO`. No se declara listo para producción,
despliegue ni presentación final.

## 5. Ejecución local segura

Elegir una ruta absoluta nueva o expresamente autorizada para la base de demo:

```powershell
$env:OMINAI_LOCAL_DEMO = '1'
$env:OMINAI_LOCAL_DB = 'C:\ruta\autorizada\demo-simulada.db'
python -B -m app.http_api
```

El servidor local escucha exclusivamente en `127.0.0.1:8000`. El comando
`python -B -m app.cloud_http_api` identifica un entrypoint técnico existente;
no debe presentarse como instrucción ni evidencia de despliegue real.

Para repetir la verificación automatizada:

```powershell
python -B -m unittest discover -s tests -v
```

## 6. Alcance de la aceptación

Las aprobaciones humanas registradas durante la construcción corresponden a
piezas concretas. No equivalen a la aceptación integral del producto, a un
release autorizado ni a autorización para usar servicios externos.
