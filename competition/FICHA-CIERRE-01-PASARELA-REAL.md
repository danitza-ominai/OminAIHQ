# CIERRE-01 — Primera implementación del proveedor real ADK/Gemini

> ACTUALIZACIÓN 31-08-2026: Niko solicitó un encargo integral para Antigravity, después correcciones Codex y solo revisión final Copilot. Esta ficha queda como antecedente técnico, NO como encargo separado que deba ejecutarse antes. Usar `competition/ENCARGO-INTEGRAL-ANTIGRAVITY-2026-08-31.md` y su prompt integral. No extrapolar automáticamente sus permisos.

Fecha: 2026-08-31. Versión: 1.
Estado: FICHA_LISTA_PARA_DECISION_HUMANA. Construcción: NO_AUTORIZADA_POR_ESTE_DOCUMENTO.
Constructor propuesto: Antigravity. Revisor independiente: GitHub Copilot. Coordinador: Codex. Aceptación: Niko.

## 1. Resultado y límite

Completar por primera vez el transporte real ADK/Gemini detrás de la pasarela existente, con selección explícita de modo, errores seguros, consumo observado y reserva durable. Preservar íntegra la demo SIMULADA por defecto.

Esta pieza NO conecta todavía los cinco especialistas, NO modifica el recorrido HTTP, NO despliega, NO produce la demo final y NO acredita calidad del VBP. Preparar código real con pruebas offline deja REAL_NO_VERIFICADA hasta un ensayo externo expresamente autorizado.

No es una corrección para cambiar estados/aprobaciones: es construcción inicial de una capacidad pendiente del perfil aprobado. Los defectos preexistentes ajenos se reportan sin corregir. No reinicia los contadores de correcciones de otras piezas.

## 2. Por qué requiere un nuevo encargo exacto

PZ-004A aprobaba crear `app/agent_gateway.py`, `app/runtime_config.py` y `tests/test_agent_gateway.py`, deteniéndose si existían. Ya existen y han recibido correcciones. No se puede ejecutar otra vez aquel prompt como autorización de sobrescritura.

Esta ficha propone una integración aditiva en ocho archivos. Solo una decisión humana que apruebe este alcance y lista habilita su construcción. El mensaje «listo dale» de esta conversación habilitó preparar el encargo; no se registra como aceptación de esta lista todavía no presentada.

PZ-003F continúa siendo dependencia del encargo original. Antes de construir, localizar su aceptación y las revisiones vigentes de interfaces compartidas. Si no hay constancia, reportar la ausencia; no aceptarla por tests ni inventar un registro. Niko puede resolver expresamente esta precondición. No reabrir decisiones ya documentadas.

## 3. Fuentes de lectura obligatoria

1. `AGENTS.md`, `TEAM-WORKFLOW.md`, `CONTRATO-MVP-v1.md`, secciones 0–5, 10, 11.3–11.4, 11.9 y gate 15.7.
2. `PIEZAS-PENDIENTES/00-REGLAS-Y-DECISIONES.md`, `FICHA-PZ-004A.md`, `FICHA-PZ-003F.md` y filas CT-002/CT-007/CT-015 de la matriz existente.
3. Los ocho archivos del perímetro y, solo lectura, `app/hq_runtime.py`, los cinco especialistas, `app/human_approvals.py`, `app/runtime_contracts.py` y los contratos aceptados.
4. REQUISITOS: `a5aaf8a8-fe07-4a6a-8f9a-fc29a5baa691_11_de_agosto_de_2026_2308.pdf`, p. 1, separación función/agente; `T-DEVAGENTOPT-I-m1-l1-es-file-2.es.pdf`, pp. 1 y 4, instrucciones y límites; `T-DEVAGENTOPT-I-m2-l0-es-file-3.es.pdf`, p. 1, salidas estructuradas; `T-DEVAGENTMEM-B-m3-l0-es-file-5.es.pdf`, pp. 1–2, alcance del estado.
5. Fuentes oficiales verificadas al preparar esta ficha: [modelo Gemini 3.5 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash), [precios Gemini API](https://ai.google.dev/gemini-api/docs/pricing), [google-adk 2.8.0](https://pypi.org/project/google-adk/2.8.0/), [agentes ADK](https://google.github.io/adk-docs/agents/llm-agents/) y [thinking y uso](https://ai.google.dev/gemini-api/docs/thinking).

Los ejemplos educativos de Gemini 2.5 y exposición de razonamiento no sustituyen el perfil vigente ni autorizan almacenar Chain-of-Thought.

## 4. Configuración técnica propuesta para esta pieza

| Elemento | Valor / condición |
|---|---|
| Python | 3.11 o posterior, en entorno aislado. Registrar ejecutable y versión efectivos. |
| Dependencia nueva | Extra opcional `agents` con `google-adk==2.8.0`; conservar los extras existentes. Registrar versiones transitivas resueltas en el informe, sin instalar el extra `all`. |
| Modelo | ID oficial `gemini-3.5-flash`, explícito en modo real. Disponibilidad en la cuenta: NO_VERIFICADA. |
| API propuesta | Gemini Developer API. Clave solo desde entorno seguro; no leerla, imprimirla ni enviarla al chat. Vertex AI/ADC queda para una decisión posterior si se requiere. |
| Precio de referencia | API estándar, texto: USD 1.50 por millón de tokens de entrada y USD 9.00 por millón de salida, incluidos tokens de pensamiento. Consultado el 31-08-2026. No usar tarifas de Batch/Flex/Priority ni asumir gratuidad. |
| Datos de esta pieza | Texto sintético mínimo y autorizado; sin documentos de negocio privados, archivos, grounding, búsqueda, caché explícita ni herramientas externas. |
| Límites propuestos | Hasta 4096 tokens de entrada total y 4096 tokens generados facturables, incluido pensamiento. El constructor debe demostrar cómo el SDK aplica esos topes; no confundir caracteres con tokens ni salida visible con consumo total. |
| Tiempo / intentos | Hasta 45 segundos por intento para esta pieza; un reintento transitorio como máximo, dos intentos totales por tarea. Reintentos automáticos internos desactivados o contabilizados por la misma reserva. |
| Presupuesto heredado | Máximo USD 25 total del proyecto; hasta 15 solicitudes por misión; aviso al 70 %, pausa al 90 %. No renueva saldo ni contadores. |
| Reserva estimada | Con ambos topes de 4096 aplicados realmente: USD 0.043008 por intento. Usar redondeo conservador a microdólares. No es coste medido ni permiso de gasto. |
| Ejecución de modelo | Deshabilitada por defecto. Ningún test de discovery ordinario llama a red. |

ADK 2.8.0 y el ID anterior se verificaron en fuentes públicas, no se instalaron ni se probaron aquí. Validar imports y APIs contra la versión instalada; no inventar un método del SDK. La cotización es específica de Gemini Developer API y no se traslada automáticamente a Vertex AI.

## 5. Ocho archivos propuestos — lista cerrada

Raíz de todas las rutas: `C:\Users\Nivez\Desktop\08_Ominai\OminAIHQ`.

| Acción | Archivo | Alcance exacto |
|---|---|---|
| Crear | `app/adk_provider.py` | Implementación de `ModelClientProvider` mediante agente y runtime ADK. Configuración, respuesta final normalizada, metadatos de uso y errores saneados. Sin herramientas ni bucles agentic en esta pieza. |
| Crear | `tests/test_adk_provider.py` | Pruebas del límite SDK/proveedor mediante transporte inyectado sin red; comprobación de imports/configuración; ensayo real separado por opt-in explícito, nunca dentro de discovery ordinario. |
| Modificar | `app/agent_gateway.py` | Incorporar selección explícita del proveedor real sin debilitar modo offline; conservar firma existente y añadir únicamente parámetros opcionales necesarios para límites, esquema y autorización de transporte. Validación, reserva, contabilización y etiquetado correctos. |
| Modificar | `app/runtime_config.py` | Perfil real explícito, configuración no secreta y precios fechados separados de tarifas sintéticas; topes efectivos; falta de configuración produce rechazo. Conservar defaults de la demo local. |
| Modificar | `app/local_repository.py` | Solo `budget_snapshot`, `reserve_call`, `reconcile_call` y metadatos de llamadas necesarios para distinguir consumo simulado y real estimado. Conservar atomicidad, registros previos y límites. Prohibido modificar persistencia de misión, revisión nuclear, aprobaciones, eventos o checkpoints. |
| Modificar | `tests/test_agent_gateway.py` | Agregar y ajustar únicamente pruebas del transporte, consentimiento de red, presupuesto y compatibilidad. No borrar negativos ni reducir exigencias. |
| Modificar | `tests/test_local_repository.py` | Agregar únicamente regresiones de metadatos de consumo, reapertura y reservas; conservar todas las pruebas de misión/versionado/atomicidad. |
| Modificar | `pyproject.toml` | Añadir únicamente el extra opcional `agents` fijado arriba, conservando requisitos de Python y extras existentes. No instalar por editar este archivo. |

Todo otro archivo queda prohibido: especialmente `app/hq_runtime.py`, especialistas, `app/http_api.py`, UI, Dockerfile, despliegue, README, contratos y esta documentación. No crear auxiliares para eludir la lista. Si un archivo a crear aparece, comparar y detenerse antes de sobrescribirlo.

## 6. Comportamiento obligatorio

1. Instanciar configuración, importar módulos o ejecutar la suite offline nunca inicia llamadas, autentica una cuenta ni consulta modelos.
2. El modo real necesita proveedor explícito, dependencia disponible, credencial segura, permiso de ejecución, modelo permitido, datos autorizados y repositorio durable explícito. Una clave presente por sí sola no prueba autorización ni integración verificada. No aceptar modo/permisos enviados por un cliente HTTP.
3. Usar ADK realmente. Importarlo sin ejecutar su agente/runtime no cuenta como integración. En este tramo se permite un único razonamiento por intento, sin herramientas, delegación, redirecciones de endpoint ni llamadas ocultas.
4. Preservar `ModelClientProvider.call_model`/`ModelCallResponse` y la tupla de resultado de la pasarela para consumidores existentes; extensiones solo compatibles. El adaptador recibe contexto mínimo, no exporta base de datos ni conversaciones completas.
5. Reservar antes de cada intento. Credenciales/configuración/entrada inválidas se rechazan antes de llamar y sin consumos indebidos. Timeout después de enviar conserva reserva y no se reintenta automáticamente; errores con consumo incierto tampoco se convierten en cero.
6. Contabilizar entrada y toda salida facturable, incluido pensamiento sin guardar su contenido. Si el proveedor no ofrece una cota y metadatos fiables, bloquear modo real; no inventar tokens ni coste. Coste calculado a partir de uso es estimación, no factura certificada.
7. Los registros de prueba continúan `SIMULADA`; los de llamadas reales distinguen uso observado y coste estimado. No reclasificar historia. Totales mixtos no se presentan como gasto real puro y conservan la reserva compartida sin reiniciar el techo.
8. Rechazar salidas inválidas contra el esquema solicitado y rechazar acciones/herramientas no admitidas. Nunca transformar texto arbitrario en éxito por envolverlo en JSON.
9. No pedir ni persistir pensamientos, resúmenes de pensamiento, firmas, payloads crudos, claves o trazas automáticas del SDK. Filtrar eventos antes de registrar; guardar solo respuesta final autorizada y metadatos mínimos. No desactivar el conteo de tokens internos para ocultar coste.
10. Error real visible; jamás fallback automático al mock o al modelo 2.5. El modo real no modifica estados de misión, aprueba VBP ni afecta permisos humanos.

## 7. Pruebas de aceptación

| AC | Comportamiento demostrado | Efecto que debe comprobarse |
|---|---|---|
| 01 | Defaults SIMULADA y SDK ausente no rompen el modo offline. | Cero llamadas de red, sin autorización ni coste real implícito. |
| 02 | Clave, permiso, modelo, tarifa, límites, esquema o contexto requerido ausentes/inválidos. | Rechazo antes del transporte; estado/ledger sin cambios indebidos. |
| 03 | Transporte inyectado produce respuesta válida con tokens de pensamiento >0. | Salida final limpia, importe incluye todos los tokens; reserva reconciliada exactamente una vez. |
| 04 | Timeout tras envío o consumo indeterminado. | Reserva retenida, una sola invocación, ningún reintento al repetir la tarea. |
| 05 | Error transitorio inequívocamente reintentable. | Hasta dos intentos totales; cada uno reservado/contado; SDK no añade intentos ocultos. |
| 06 | Umbrales, solicitud 16 e intento 3 de tarea. | Rechazo sin llamada adicional; dos conexiones y reapertura conservan el mismo ledger. |
| 07 | Salida mal formada, intento de tool, secreto o pensamiento en respuesta/evento. | Rechazo/control, sin almacenar ni imprimir el contenido protegido. |
| 08 | Modos simulado/real comparten historial de reservas. | Etiquetas fieles, historia inalterada y ningún reinicio de saldo por cambiar modo. |
| 09 | Importación y construcción de objeto ADK fijado, con transporte bloqueado. | Demuestra compatibilidad SDK en el entorno declarado; no se reporta como llamada real. |
| 10 | Ensayo externo posterior autorizado por Niko. | ID de modelo, hora, estado, uso observado, coste estimado y respuesta sintética; REAL_VERIFICADA solo para este transporte. |

AC-10 está PENDIENTE_DE_AUTORIZACION; no se ejecuta como parte de la construcción offline. Una prueba opt-in omitida se informa por separado, no se cuenta como éxito. Una variable de entorno con nombre de autorización no reemplaza la autorización humana.

Comandos de regresión, desde la raíz y con entorno de pruebas correcto:

```text
python -B -m unittest discover -s tests -p test_adk_provider.py -v
python -B -m unittest discover -s tests -p test_agent_gateway.py -v
python -B -m unittest discover -s tests -p test_local_repository.py -v
python -B -m unittest discover -s tests -v
```

Registrar ejecutable y versión: el comando `python` de este equipo resuelve actualmente a un entorno de otra aplicación. No modificar ese entorno ni instalar globalmente. Hubo errores de permisos en temporales de Windows en la revisión previa; no atribuirlos a producto ni suprimir tests para obtener verde. Solicitar permiso de ejecución apropiado o usar una raíz aislada autorizada; no crear un wrapper fuera de la lista ni modificar ACL amplias.

## 8. Instalación, datos y gastos separados

Esta ficha solo propone cambios de fuente y pruebas offline. Si no existe un entorno con las dependencias fijadas, preparar y presentar el comando y ruta exactos antes de instalar; no instalar en la sesión de otra aplicación. No se solicitan claves en chat.

Propuesta de recursos para una autorización posterior, NO creada ni usada por esta ficha: entorno `.venv-cierre-01` y temporales `.review-cierre-01` dentro de la raíz del proyecto, solo si no existen. No son archivos fuente nuevos permitidos automáticamente. La aprobación debe cubrir instalación/descarga y esas raíces; excluirlos de toda publicación. Si existe alguno, no sobrescribirlo.

Ensayo real posterior propuesto: solo texto «Devuelve un objeto JSON con la clave status y el valor ok», sin datos privados; máximo dos solicitudes, 4096 tokens de entrada y 4096 generados facturables por solicitud, 45 s por intento, máximo USD 0.10 adicional dentro del saldo global restante. Estos parámetros NO autorizan gasto; requieren decisión y verificación de la cuenta y del ledger. No usar bases existentes del usuario.

## 9. Entrega y revisión

Objetivo de trabajo: 45 minutos; una conversación de construcción, sin delegación. Si la pieza requiere ampliar alcance, reportar antes de continuar. No abrir nuevas rondas de corrección por iniciativa.

Devolver en conversación: archivos exactos, inventario/hash antes y después, diff o descripción verificable, comportamiento por AC, comandos/códigos/resultados, versiones efectivas, residuos y limitaciones. Sin logs adicionales fuera de lista. Copilot revisa la versión estable y no edita. Niko acepta o rechaza.

No afirmar: cinco agentes reales, UI conectada, nube lista, factura limitada a USD 25 o MVP aceptado. Esas afirmaciones requieren las etapas siguientes.

## 10. Baseline orientativo de los seis archivos existentes

Capturado el 31-08-2026 durante la preparación. El constructor debe recapturarlo antes de editar; una diferencia exige revisar trabajo concurrente, no revertirlo.

```text
app/agent_gateway.py         4C093EE3EE2CD7008E5E94723034655F861467BB961A774A9BB9B6E2DD227C86
app/runtime_config.py        0DD1CE3E063572FF537D4FDE8440DC2C47BF450FFBCB74FE72567883FA440329
app/local_repository.py      0E0B0EDC688AF276C618F8A1D2C031AAEA5607302BA611F43C6AE0B1FC9D7CAE
tests/test_agent_gateway.py  15359F541321D300B3924FEE3EB6F2266DE0B2A01673A7113DAA0E2DC8A892D5
tests/test_local_repository.py 195D2D7FD11116A3F432FA9B1A5713B5A0489BB14021C0231CA65BACD7E3EF65
pyproject.toml              77B639BA40550CB67753120ED9F4AA952FC39D08E1CFB87090EAAD12D6041392
```

## 11. Registro pendiente

- Preparación documental: solicitada por Niko en esta conversación.
- Construcción CIERRE-01 y ocho archivos: PENDIENTE_DE_DECISION_HUMANA.
- Dependencias aceptadas: PENDIENTE_DE_LOCALIZAR_CONSTANCIA.
- Instalación/raíces de ejecución: SIN_AUTORIZACION_NUEVA.
- Llamadas/gasto/cloud/publicación: SIN_AUTORIZACION_NUEVA.
- Revisión Copilot / aceptación: PENDIENTES.
