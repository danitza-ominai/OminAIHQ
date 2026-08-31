# OminAI HQ - Manual de Operación y Despliegue de Demo Pública (PZ-014B)

Este manual documenta el procedimiento reproducible para la operación y control del servicio demo en Google Cloud Run, conforme a CONTRATO-MVP-v1.md seccion 11.4, 11.9 y PT-007/008.

---

## 1. Requisitos Previos y Autorización Humana

> **IMPORTANTE:** El despliegue a la nube, el gasto asociado y la apertura pública requieren autorización humana expresa (A0). La existencia de este documento no autoriza despliegues automáticos no aprobados.

- Proyecto Google Cloud configurado con facturación habilitada.
- Secret Manager configurado para credenciales del modelo (`GEMINI_API_KEY`), sin incrustar secretos en la imagen.
- Service Account con mínimos privilegios (`roles/run.invoker`, `roles/secretmanager.secretAccessor`).

---

## 2. Parámetros Operativos del Servicio

| Parámetro | Valor Requerido | Justificación |
|---|---|---|
| **Servicio** | `ominai-hq` | Nombre canónico de la instancia |
| **minScale** | `0` | Escala a cero para evitar consumo inactivo |
| **maxScale** | `1` | Máximo 1 contenedor activo concurrente |
| **CPU / Memoria** | `1 CPU / 512Mi` | Límite acotado de recursos |
| **Timeout** | `300s` | Plazo contractual por solicitud |
| **Cuota Diaria** | `5 ejecuciones` | Límite global para demo pública |
| **Presupuesto Máximo** | `$25.00 USD` | Techo absoluto de gasto |

---

## 3. Comandos de Construcción y Despliegue

### 3.1 Construcción Segura de Contenedor
```bash
# Construir imagen utilizando Cloud Build respetando .dockerignore
gcloud builds submit --tag gcr.io/${GCP_PROJECT_ID}/ominai-hq:latest .
```

### 3.2 Despliegue en Cloud Run
```bash
# Desplegar servicio con configuracion controlada
gcloud run deploy ominai-hq \
  --image gcr.io/${GCP_PROJECT_ID}/ominai-hq:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 1 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --set-env-vars OMINAI_MODE=DEMO,OMINAI_DAILY_DEMO_LIMIT=5,OMINAI_MAX_BUDGET_USD=25.0 \
  --set-secrets GEMINI_API_KEY=ominai-gemini-key:latest
```

---

## 4. Procedimiento de Parada y Reversión Inmediata (Teardown)

En caso de detección de anomalías, superación de cuotas o revocación de autorización:

```bash
# 1. Detener tráfico inmediatamente
gcloud run services update ominai-hq --region=us-central1 --no-allow-unauthenticated

# 2. Eliminación completa del servicio si es requerido
gcloud run services delete ominai-hq --region=us-central1 --quiet
```
