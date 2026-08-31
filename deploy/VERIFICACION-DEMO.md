# OminAI HQ - Protocolo de Verificación de Despliegue en la Nube (PZ-014B)

Este protocolo define las pruebas de verificación operativa para la demo pública y el control de límites en Google Cloud Run.

---

## 1. Estado de la Verificación Real

- **Verificación Local / Sintética:** COMPLETADA (100% pruebas de políticas, cuotas y contratos aprobadas).
- **Despliegue Real en Google Cloud:** PENDIENTE_DE_AUTORIZACION_EXPRESA_Y_GASTO (A0).

---

## 2. Checklist de Criterios de Aceptación (AC)

| Criterio | Control Verificado | Estado Offline | Estado en Vivo (Cloud) |
|---|---|---|---|
| **AC-01** | `GET /health` responde 200 y `GET /` sirve la interfaz pública saneada | VERIFICADO | PENDIENTE DE DESPLIEGUE REAL |
| **AC-02** | Contenedor no-root, sin bases SQLite de usuario ni secretos en imagen | VERIFICADO | PENDIENTE DE DESPLIEGUE REAL |
| **AC-03** | Cuota de 5 ejecuciones diarias: 5ta admitida, 6ta pasa a solo lectura | VERIFICADO | PENDIENTE DE DESPLIEGUE REAL |
| **AC-04** | Presupuesto global acotado a USD 25 y alertas por umbrales | VERIFICADO | PENDIENTE DE DESPLIEGUE REAL |
| **AC-05** | Endpoints administrativos y decisiones protegidos contra llamadas públicas | VERIFICADO | PENDIENTE DE DESPLIEGUE REAL |

---

## 3. Pruebas de Verificación sobre Endpoint Activo

Una vez autorizado y completado el despliegue:

```bash
# 1. Comprobar salud del servicio
curl -i https://[SERVICE_URL]/health

# 2. Comprobar que endpoint de decision rechaza actores no autorizados
curl -i -X POST https://[SERVICE_URL]/api/v1/missions/MSN-TEST/decisions \
  -H "Content-Type: application/json" \
  -H "X-Ominai-Actor-Role: product_architect" \
  -d '{"decision": "APROBAR"}'
# Esperado: HTTP 403 Forbidden (PERMISSION_DENIED)

# 3. Comprobar limite de tamano de payload (> 50KB)
# Esperado: HTTP 413 Payload Too Large
```
