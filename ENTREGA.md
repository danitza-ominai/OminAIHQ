# OminAI HQ - Entrega Integral del Producto y Expediente de Competencia

## 1. Resumen Ejecutivo

OminAI HQ es la oficina digital agentica desarrollada para convertir una mision empresarial en un Venture Build Package (VBP) canonico, auditable y exportable.

El producto ha sido construido y verificado bajo los mas estrictos estandares de gobernanza:
- Autorizacion humana expresa en dos puertas obligatorias (Puerta 1: Plan, Puerta 2: VBP).
- Trazabilidad inmutable con huellas SHA-256 y saneamiento de Chain-of-Thought (CoT) y secretos.
- Proveedor real Gemini 3.5 Flash / Google ADK y modo SIMULADA controlado sin fallbacks silenciosos.
- Interfaz bilingue (ES / EN) con preservacion de identificadores estables.
- Despliegue listo para Google Cloud Run y Cloud Firestore.

## 2. Resultados de Verificacion

La suite completa de pruebas ha sido ejecutada exitosamente:
- **Pruebas Totales:** 294
- **Pasadas:** 294
- **Fallos:** 0
- **Errores;ª* 0

## 3. Estructura del Proyecto

- `app/`: Nucleo del runtime, especialistas y adaptadores de red/almacenamiento.
- `contracts/`: Esquemas JSON Schema Draft 2020-12 para contratos core y runtime.
- `evaluation/`: Harness y casos de evaluacion adversarial.
- `tests/`: Suite exhaustiva de pruebas unitarias e integrales.
- `web/`: Centro de gestion web bilingue (ES / EN) con proteccion ASR/XSS.
- `deploy/`: Artefactos y dependencias bloqueadas para despliegue.

## 4. Instrucciones de Ejecucion

```bash
# Ejecutar la suite completa de pruebas
python -B -m unittest discover -s tests -v

# Iniciar el servidor local de demo
python -B -m app.http_api

# Iniciar en entorno Cloud Run
python -B -m app.cloud_http_api
```
