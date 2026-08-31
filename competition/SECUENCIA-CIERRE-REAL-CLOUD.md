# Secuencia de integración real y nube

> ACTUALIZACIÓN 31-08-2026: el flujo vigente solicitado para este cierre es un encargo integral Antigravity → inspección/corrección autorizada Codex → revisión final Copilot. La secuencia técnica inferior sirve de referencia; no exige nuevos encargos CIERRE-01 por separado ni revisiones Copilot intermedias. Ver `competition/ENCARGO-INTEGRAL-ANTIGRAVITY-2026-08-31.md`.

Fecha: 2026-08-31. Estado: COORDINACION_PROPUESTA. No concede permisos de construcción, red, gasto ni despliegue.

## 1. Evidencia que determina la secuencia

- `AgentGateway.execute_agent_call` rechaza proveedores que no sean mock.
- La búsqueda de llamadas a ese método en `app` solo encuentra su definición: los especialistas no lo invocan actualmente.
- `HQRuntime.execute_local_simulation` usa `SimulatedSpecialistRunner` y conserva etiquetas de simulación. Chief of Staff también construye propuestas sintéticas.
- Por tanto, terminar un proveedor no completa el recorrido. Deben verificarse por separado transporte, agentes, orquestación y despliegue.
- El contenedor actual ejecuta un servidor local de 127.0.0.1:8000; no es todavía un adaptador cloud. La política cloud inspeccionada usa SQLite, no acredita Firestore/Storage.

## 2. Orden de piezas, sin ejecución simultánea sobre los mismos archivos

| Paso | Encargo | Evidencia de salida | Estado |
|---|---|---|---|
| 1 | CIERRE-01: proveedor real y pasarela controlada. | Pruebas offline del límite SDK; ensayo externo posterior explícito. | Ficha y prompt preparados; aprobación/condiciones pendientes. |
| 2 | Construcción inicial pendiente de razonamiento real de los roles, uno por vez: Chief, Research, Architect, Delivery, Governance. Integrarlos en el recorrido tras validar cada interfaz. | Salidas variables según entrada real y fuentes; cinco roles separados; no fixtures ocultos; controles humanos intactos. | Encargos exactos se cierran sobre el resultado aceptado de CIERRE-01. No autorizados por esta tabla. |
| 3 | Adaptador de demo cloud, identidad del operador, Firestore/Storage, cuotas y recuperación. | Contenedor compatible; UI/API reales; datos saneados; cuotas y estado durables. | Reconciliar PZ-014A con archivos actuales antes de emitir lista cerrada. |
| 4 | Despliegue y ensayo en Google Cloud. | URL, revisión desplegada, logs saneados y prueba visible para video. | Depende de aceptación de 3, proyecto/identidad/entorno y autorización de gasto/despliegue. |
| 5 | Copilot final, aceptación humana y documentación/video/envío. | Gate 15.7/C.18 con evidencia; entrega reproducible. | No sustituir controles pendientes por un conteo de tests. |

Antigravity construye las capacidades iniciales pendientes. Codex no usa «corrección» para introducir capacidades nuevas. Un defecto en comportamiento ya construido se consolida para corrección autorizada y Copilot revisa sin editar. No resetear rondas existentes.

## 3. Puntos de integración para el siguiente encargo, solo lectura por ahora

- `app/chief_of_staff.py`: aclaración y propuesta vinculadas al brief vigente; el plan no se aprueba por una respuesta del modelo.
- `app/research_analyst.py`: fuentes originales autorizadas, fechas reales o desconocidas, evidencia atribuida; no inferir confiabilidad porque una URL contiene `gov` o porque hay dos documentos cualesquiera.
- `app/product_architect.py` y `app/delivery_planner.py`: quitar dependencia de propuestas fijas solo mediante construcción real aprobada; requisitos y cronograma deben derivarse de misión/evidencia.
- `app/governance_risk.py`: razonamiento separado más bloqueadores deterministas; dictamen nunca equivale a aprobación humana.
- `app/hq_runtime.py`: las llamadas reales fuera de transacciones de larga duración; persistir reserva/intención antes de enviar; reconciliar resultados con versión vigente; no duplicar tras timeout/reinicio.
- `app/human_approvals.py`, contratos, memoria y exportador: interfaces que deben respetarse, no permiso para editarlos.
- La vista ES/EN debe representar contenido real congelado antes de aprobación; no reutilizar traducciones de un escenario sintético para otra salida.

## 4. Preparación cloud que puede revisarse antes de gastar

1. Identificar proyecto, región, cuenta operadora y cuenta de servicio mediante evidencia no secreta. Aquí no se verificó una cuenta cloud ni credenciales; `gcloud` no apareció en el PATH consultado. Eso no prueba que el usuario carezca de Cloud Shell u otro entorno.
2. Definir el adaptador cloud sin exponer autoridad del perfil local. Visitante no aprueba decisiones administrativas ni activa gasto ilimitado; no usar body/header como autoridad.
3. Escuchar en la interfaz/puerto exigidos por Cloud Run; conservar loopback y controles del adaptador local. [Contrato Cloud Run](https://docs.cloud.google.com/run/docs/container-contract).
4. Persistir estado y cuota fuera del filesystem efímero del contenedor. Implementar el perfil Firestore/Cloud Storage ya aprobado, con transacciones y objetos saneados, sin sincronizar bases privadas.
5. Reconciliar el presupuesto de modelos con costes de infraestructura y restricciones operativas; máximo una instancia y cinco demos/día son límites del proyecto, no garantía de factura total.
6. Ejecutar pruebas locales/emuladas en raíces aprobadas y revisar con Copilot. Solo después solicitar la autorización concreta para APIs, recursos, datos, acceso público y despliegue.
7. Conservar acceso de evaluación para jueces y ejemplo de solo lectura al agotar cuota; verificar procedimiento sin dejar un bypass público de gasto.

## 5. Prompt de revisión para Copilot — después de la construcción

```text
Actúa únicamente como revisor independiente de CIERRE-01. No modifiques archivos ni implementes soluciones.

Lee competition/FICHA-CIERRE-01-PASARELA-REAL.md y la autorización humana correspondiente. Compara inventarios/hashes, diff, comandos y salidas contra sus ocho archivos y límites.

Revisa: proveedor ADK auténtico; ausencia de llamadas al importar o en modo offline; configuración/credenciales/permiso insuficientes rechazados; no fallback ficticio; reserva antes de cada intento; tokens de pensamiento incluidos en coste sin registrar contenido; no reintentos SDK ocultos; timeout conserva reserva; reapertura y concurrencia no reinician contadores; etiquetas real/simulado sin reescribir historia; no cambios de estados/aprobaciones; compatibilidad de todos los tests previos.

Distingue prueba con transporte simulado, importación real del SDK, llamada real y flujo completo. Tener clave o instalar ADK no acredita llamada. No declares aceptación humana ni MVP listo.

Reporta cada hallazgo con severidad, archivo/línea, evidencia, impacto y recomendación; añade límites de lo que pudiste verificar. Si no hay hallazgos, indica versión revisada y pruebas verificadas, sin asumir cumplimiento de etapas siguientes.
```

## 6. Decisiones concretas pendientes, no preguntas sobre el alcance ya aprobado

- Aprobar o ajustar CIERRE-01 y sus ocho archivos; localizar/ratificar dependencia requerida sin inventar aceptación.
- Si falta entorno: autorizar ruta y comando de instalación aislada antes de ejecutar; no modificar entornos ajenos.
- Para la primera llamada: cuenta/mecanismo seguro, datos sintéticos, base nueva, saldo compartido y gasto máximo propuesto de USD 0.10, dentro del total de USD 25.
- Para nube: proyecto/región, IAM, servicios, exposición, cuota y aprobación de gasto/despliegue. No pedir claves en chat.

La preparación de estos documentos no marca ninguna decisión pendiente como concedida. Las autorizaciones anteriores válidas se conservan y no se vuelven a pedir.
