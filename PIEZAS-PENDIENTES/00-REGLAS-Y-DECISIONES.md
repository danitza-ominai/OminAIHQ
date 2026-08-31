# Reglas y decisiones para las piezas restantes

Estado: FICHAS_APROBADAS_PARA_CONSTRUCCION_SECUENCIAL_POR_ANTIGRAVITY
Version del paquete: 1
Fecha de preparacion: 30 de agosto de 2026
Fecha de aprobacion humana: 30 de agosto de 2026
Contrato rector: CONTRATO-MVP-v1.md, 1.2-aprobada

## 1. Autoridad y alcance de este paquete

El usuario aprobo expresamente las 29 fichas version 1 de PZ-003C a PZ-015B enumeradas en MAPA-PIEZAS-RESTANTES.md, manteniendo Antigravity como constructor inicial.
Referencia literal del 30 de agosto de 2026: "todas las fichas quedan aprobadas y lo hare con el antigravity mas a eso me referia".
La aprobacion cubre el alcance y la lista cerrada de archivos de cada ficha; no se pide nuevamente para esos mismos encargos. La ejecucion sigue siendo secuencial y condicionada a sus dependencias aceptadas y requisitos previos.
Las 29 subpiezas son una descomposicion aprobada de los bloques 3 a 15 del contrato, no 29 productos nuevos. Registrar su aprobacion no construye funcionalidades.
No se cambia el contrato, las decisiones DN/PT, AGENTS.md, TEAM-WORKFLOW.md ni fichas aceptadas.

Antigravity construye inicialmente una sola pieza expresamente aprobada. Codex coordina y revisa; solo corrige con nueva autorizacion que enumere archivos exactos. Copilot revisa sin editar. El usuario humano acepta la pieza.
Maximo dos rondas de correccion por pieza, no dos intentos automaticos sin autorizacion. No delegacion ni edicion simultanea.
PZ-003B fue aceptada posteriormente por el usuario humano mediante "registra la aprobacion de la pieza faltante", el 30 de agosto de 2026; ver seccion 15 de su ficha. El recorrido manual sigue pendiente. Esta decision no acepta piezas futuras ni concede los permisos sensibles que cada ficha reserva expresamente.

## 2. Fuentes y jerarquia

Leer AGENTS.md y TEAM-WORKFLOW.md completos; CONTRATO-MVP-v1.md (0-4, 6, 7, 8/8A, 10-13, 15.7 y Anexo C), esta guia, la ficha concreta y sus secciones especificas.
Leer contratos/core/README.md, state-machine.json y los schemas/ejemplos que corresponden antes de escribir codigo.
Releer interfaces, pruebas y decisiones finales de las dependencias; un nombre propuesto aqui no prueba que ese archivo exista.
La evidencia ejecutable acredita implementacion; las decisiones humanas gobiernan alcance; el contrato gobierna requisitos; las clases son guia, no reglas oficiales del concurso.

Las decisiones aprobadas se conservan. Las rutas enumeradas y opciones tecnicas explicitamente descritas en las fichas quedan aprobadas; los valores no definidos se concretan antes de construir y las interfaces se verifican contra la evidencia de dependencias aceptadas.
Si una API, dependencia o archivo requerido no coincide con lo aprobado, detenerse antes de editar y pedir una ficha ajustada. No convertir esta lista en permiso abierto para adaptar cualquier archivo.

## 3. Hechos de partida y precision del informe PZ-003B

- PZ-001A, PZ-002A y PZ-003A figuran COMPLETADA_Y_ACEPTADA en sus fichas.
- PZ-003B: COMPLETADA_Y_ACEPTADA por el usuario humano; construida y corregida una vez, con revision tecnica y dictamen Copilot previos favorables. Recorrido manual humano pendiente; CT-009 no cerrado.
- Ultima suite ejecutada por Chipi: 82 pruebas (2 smoke + 14 contratos + 33 intake + 33 revision). Se realizaron ademas 18 comprobaciones independientes en memoria.
- La correccion 1 cambio solo app/demo_plan_review.py y tests/test_demo_plan_review.py. README corresponde a la construccion inicial, no a esa correccion.
- El intake genera tres eventos; la solicitud pendiente agrega el cuarto. jsonschema ausente devuelve SYSTEM_ERROR/codigo 1; codigo 2 corresponde a NOT_FOUND.
- El informe de Copilot mezcla conteos y fases. Esta aclaracion no reemplaza ni edita su original.
- Los 13 contratos nucleares y los 83 archivos preexistentes a ese log conservaban sus hashes en la comprobacion previa.
- test_output.log fue eliminado con autorizacion expresa; era salida de pruebas, no fuente de producto. Puede regenerarse, pero no se crea nuevamente como residuo.
- Persistencia, recuperacion y memoria NO estan fuera del MVP: CT-003/CT-008 y la politica de CT-004 siguen pendientes de evidencia.
- La comparacion de huellas sirve para el perimetro, no sustituye pruebas funcionales ni aceptacion humana.

## 4. Reglas funcionales invariables

1. OminAI HQ es el producto; Business OS puede ser iniciativa cliente, no se fusiona. Omi y OminaiTech Engine no se incorporan.
2. Un unico perfil humano persistente local: user_id, nombre, correo opcional. No login/password/equipos/sincronizacion entre dispositivos.
3. Plan y VBP tienen aprobaciones humanas distintas, de version/huella exacta. Nunca autoaprobacion ni autoridad basada en texto del modelo.
4. Un VBP canonico Markdown con manifest y 18 secciones. Los objetos estructurados internos no son otro VBP descargable JSON/PDF.
5. Producto en espanol; demo clave ES/EN. Traducciones materiales se revisan y versionan antes de aprobar; no alterar lo aprobado al exportar.
6. Cinco roles reales y separados en secuencia fija, no agentes dinamicos/paralelos. SIMULADA en pruebas no acredita una llamada real.
7. Ausencia de fuente no es evidencia. Una afirmacion critica sin sustento bloquea aprobacion ordinaria; contradicciones permanecen visibles.
8. Original ausente antes de aprobar: detener y mostrar EVIDENCIA_NO_DISPONIBLE. Usar PAUSADA/BLOQUEADA con motivo EVIDENCIA_REQUERIDA segun la transicion aplicable; esos mensajes no crean estados ni errores nucleares nuevos. No saltar este bloqueo con una excepcion.
9. Original eliminado despues de aprobar: conservar VBP/aprobacion historica y marcar verificabilidad incompleta. No prometer que sigue comprobable.
10. Memoria de sesion automatica; memoria entre misiones solo con confirmacion. Chief consulta completa; otros solo contexto minimo.
11. Memoria contradictoria, vencida o de impacto material no entra al prompt hasta confirmacion/correccion/descarte. Se muestra toda memoria usada en el plan.
12. Cancelar conserva; archivar oculta; eliminar exige confirmacion de objetivo exacto. Memoria eliminada no sobrevive como texto en auditoria.
13. No guardar Chain-of-Thought, secretos, credenciales ni conversaciones completas. Trazas = acciones, fuentes, decisiones resumidas, resultados, errores y checkpoints.
14. Datos privados permanecen locales; solo expediente saneado y autorizado se utiliza en cloud. Antes de cada llamada externa se valida el contenido saliente.
15. Permisos, estados, conteos, dependencias, empaquetado e idempotencia son deterministas; el modelo razona dentro del contrato, no decide autoridad.
16. La v0 termina en VBP: no construye ni ejecuta la iniciativa cliente, no correos/pagos/compras/publicaciones externas. Despliegue de HQ y entrega al concurso son encargos sensibles separados.

## 5. Limites del producto, no nuevos presupuestos por ficha

| Dimension | Limite heredado |
|---|---|
| Aclaraciones | 3 por version de brief |
| Intentos de razonamiento | 2 totales por tarea, incluida regeneracion |
| Reintento transitorio | 1, sin sumar capas ocultas de SDK |
| Correcciones del VBP | 2; ampliar requiere decision humana |
| Simultaneidad | 1 mision activa y 1 especialista; recursividad 0 |
| Agente / mision | 300 / 1200 segundos |
| Solicitudes | 15 totales por mision |
| Gasto | USD 25 total del proyecto; no renovar al cambiar pieza o reiniciar |
| Umbrales | aviso 70 %, pausa 90 %, detencion 100 % |
| Archivos / enlaces | 5 archivos, 20 MB cada uno, 50 MB total y 10 enlaces por mision |
| Formatos | PDF, DOCX, TXT, MD, PNG, JPG/JPEG y enlaces publicos |
| Cloud Run demo | minimo 0, maximo 1 instancia |
| Demo publica | 5 ejecuciones diarias globales; luego ejemplo solo lectura |
| Demo preparada / video | objetivo 150 segundos / maximo 240 segundos |

Tiempo activo, espera humana y duracion de llamada deben distinguirse de acuerdo con el encargo antes de medir. No ocultar latencia ni afirmar SLA.
Los limites de tokens/precios, pixeles, puertos y timeouts de herramientas aun no numerados aqui se fijan en el registro tecnico ANTES de iniciar las piezas afectadas. Ausencia implica bloqueo, no infinito.

## 6. Registro de decisiones tecnicas previas a construir

Estas decisiones no reabren DN/PT. Concretan implementacion sin declarar disponibilidad actual de proveedores. La aprobacion de fichas no inventa valores faltantes; solo se requiere nueva decision humana cuando falta una eleccion material, cambia el alcance o corresponde un permiso especifico.

| ID | Requisito previo | Pieza | Estado |
|---|---|---|---|
| DT-R01 | Aceptacion de PZ-003B y constancia de recorrido manual o pendiente declarado | PZ-003C | SATISFECHO: ACEPTACION REGISTRADA; MANUAL PENDIENTE DECLARADO |
| DT-R02 | Dominio exacto de huella y contratos complementarios sin autorreferencia | PZ-003C/E/F | DETALLES_PENDIENTES_DE_CONCRETAR |
| DT-R03 | SDK/versiones, ID real de modelo Gemini del perfil aprobado, region/modo de credenciales | PZ-004A | PENDIENTE_VERIFICACION_OFICIAL |
| DT-R04 | Tokens entrada/salida, coste verificado, timeouts y presupuesto de ensayo; no exponer secretos | PZ-004A | PENDIENTE |
| DT-R05 | Fuentes, dominios y datos saneados autorizados; limites de respuesta/redirecciones | PZ-005A | PENDIENTE |
| DT-R06 | Parsers/versiones, pixeles de imagen y ubicacion privada de originales | PZ-009B/C | PENDIENTE |
| DT-R07 | SQLite local, raiz privada, migracion y purga | PZ-010A/D | SQLITE_APROBADO; RUTA_Y_POLITICAS_PENDIENTES |
| DT-R08 | Eleccion/custodia privada de dos holdout por evaluador y datos esperados no expuestos | PZ-011A | PENDIENTE |
| DT-R09 | Adaptador HTTP/framework/versiones, puerto y origen autorizado, control de operador | PZ-013A | PENDIENTE |
| DT-R10 | HTML/CSS/JS ligero, vistas y fidelidad ES/EN versionada | PZ-013B/C | BASE_HTML_CSS_JS_APROBADA; DETALLES_PENDIENTES |
| DT-R11 | Proyecto/region/IAM/exposicion de demo y control global de gasto/cuota; permisos externos | PZ-014A/B | PENDIENTE |
| DT-R12 | Reglas/plazo oficiales actuales, grabacion, repo/video publicos y envio | PZ-015B | PENDIENTE_VERIFICACION_Y_PERMISO |

El contrato registra un perfil de competencia y fechas verificadas en agosto de 2026. No se consultaron fuentes externas durante esta preparacion documental. Antes de gastar/desplegar/presentar hay que verificar las fuentes oficiales del Anexo A.4 y registrar divergencias, no suponer vigencia.
Credenciales: el usuario las configura en el mecanismo seguro correspondiente; nunca se solicitan ni copian en chat o documentos.

## 7. Perimetro de una construccion

Cada ficha enumera todos los archivos de fuente autorizados para crear/modificar por Antigravity, una vez satisfechas sus condiciones previas. Un archivo no listado esta prohibido. La aprobacion conjunta no fusiona las listas ni permite modificar archivos de otra pieza desde el encargo actual.
Los 13 contratos/core, las demos PZ-003A/B y sus pruebas se conservan salvo nueva autorizacion exacta que los incluya; este paquete no la concede.
No reemplazar archivos de usuario. Si un destino "crear" ya existe, detenerse y reconciliar. Si un destino "modificar" aun no existe, revisar dependencias; no crearlo por iniciativa.
Toda dependencia nueva/version se declara y aprueba antes de instalar. Modificar pyproject en una ficha no autoriza cualquier dependencia.
No modificar README por cada pieza: solo se incluye expresamente al cerrar PZ-015B. Las instrucciones de prueba se entregan en conversacion.

Separar fuentes de datos de ejecucion:
- Las fichas sin IO autorizado trabajan en memoria, sin logs ni caches.
- Las que prueban persistencia/archivos usan solo raiz temporal aislada aprobada y datos sinteticos; enumerar ruta absoluta y manifest antes/despues.
- Ninguna prueba borra archivos reales del usuario, mata procesos ajenos ni limpia directorios amplios.
- Artefactos privados de ejecucion se guardan solo en raiz aprobada externa al repo publico, no en REQUISITOS o attachments.
- Subprocesos, servidor loopback, modelos, cloud y publicacion requieren permiso especifico del encargo; simulaciones no acreditan ejecucion real.
- Usar python -B. Capturar resultados en memoria/conversacion. Nada de tee a test_output.log.

## 8. Pruebas y evidencia comun

Antes de editar capturar inventario de rutas, SHA-256, tamanos y fechas. Al terminar comparar todos los preexistentes por ruta, no solo conteos.
Ejecutar las pruebas propias y python -B -m unittest discover -s tests -v. Conservar las 82 iniciales y todas las agregadas por dependencias aceptadas.
Conservar smoke: python -B -m app (0), python -B -m app.demo_intake (0 con fixture completa) y python -B -m app.demo_plan_review (3 pendiente, no error).
Cada rechazo debe tener una asercion ejecutable del codigo/estado y ausencia de efectos; no "testear" buscando palabras en codigo.
Usar validadores reales. Mocks solo para fronteras IO/proveedor/tiempo/IDs/contratos de prueba, no sustituir la funcion que se desea demostrar.
Probar limites justos y excedidos, fallos antes/despues de confirmar, duplicados y referencias cruzadas.
Una llamada no intentada no se declara validada. Un modelo simulado no se cuenta como real. Un TTY mockeado no es aprobacion humana.
UI: recorrer navegador real cuando se construya, con teclado y casos de error. Las capturas se autorizan y saneean antes de guardarse.
Rendimiento/coste: distinguir objetivo, estimacion y medicion; no declarar 150 segundos sin corrida cronometrada.

Salida del constructor en conversacion: archivos y diff, comandos/codigos, pruebas y subcasos reales, cobertura de criterios, hashes, residuos, limites, errores y pendientes.
Nunca marcar CT/P0/P1 completo porque existe esta ficha. La matriz planifica evidencia; la aceptacion requiere evidence_id real.

## 9. Puertas y detenciones

Orden para las 29 fichas ya aprobadas: verificar dependencia aceptada -> concretar decisiones tecnicas y permisos pendientes -> Antigravity -> revision Chipi -> correccion autorizada si hace falta -> Copilot -> aceptacion humana.
La aprobacion humana del encargo ya esta registrada; no se vuelve a pedir mientras se mantengan alcance, lista de archivos y condiciones aprobadas. Cada pieza se acepta antes de continuar a la siguiente. No confundir aprobacion de ficha con aceptacion del resultado.
Objetivo de trabajo por encargo: una conversacion y hasta 45 minutos; si no alcanza, detener y proponer division/replanificacion, sin prometer fecha final.
No crear mas piezas automaticamente dentro del encargo para evadir el limite. Este mapa puede revisarse por el usuario; no es una estimacion de entrega el mismo dia.

## 10. Prompt comun para revisar y aceptar

Copilot: revisar la ficha aprobada, evidencias, diff y pruebas sin editar; reportar severidad, ubicacion, reproduccion, impacto y correccion recomendada. No asumir baseline inexistente.
Codex: si hay defectos, formular correccion cerrada con archivos exactos y esperar autorizacion.
Usuario humano: aceptar o rechazar la pieza; la aprobacion de construccion no es aceptacion final ni aprobacion de la mision del producto.
