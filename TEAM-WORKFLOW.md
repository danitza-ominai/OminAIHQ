# Flujo operativo del equipo constructor de OminAI HQ

## Configuracion aprobada

| Participante | Funcion | Puede modificar codigo |
|---|---|---:|
| Usuario humano (Niko, A0) | Direccion y aprobacion humana final | Solo si lo decide |
| NotebookLM | Conocimiento interno con citas | No |
| Gemini | Investigacion externa | No |
| Chipi/Codex | Coordinacion, arquitectura, integracion, revision y correcciones autorizadas | Solo para una correccion con autorizacion humana y archivos exactos |
| Antigravity | Construccion inicial de cada pieza | Si, solo dentro de la ficha aprobada |
| GitHub Copilot | Revision independiente | No |
| Claude | Excluido | No |

## Estados de una pieza

`PENDIENTE -> EVIDENCIA_LISTA -> FICHA_LISTA -> APROBADA_PARA_CONSTRUIR -> CONSTRUIDA -> VERIFICADA_O_CORREGIDA -> REVISADA_INDEPENDIENTE -> ACEPTADA`

Solo el usuario humano puede mover una pieza a `APROBADA_PARA_CONSTRUIR` o `ACEPTADA`.

## Flujo

1. El usuario humano elige la siguiente pieza.
2. NotebookLM entrega evidencia interna y Gemini verifica lo externo cuando sea necesario.
3. Chipi reconcilia ambas fuentes y prepara la ficha.
4. El usuario humano aprueba la ficha.
5. El usuario humano copia el prompt en Antigravity.
6. Antigravity construye y devuelve evidencia.
7. Chipi verifica el resultado real.
8. Si Chipi encuentra defectos, prepara una correccion cerrada. El usuario humano autoriza expresamente a Codex y enumera los archivos exactos que puede modificar.
9. Codex corrige solo esos hallazgos y archivos, sin ampliar el alcance, y vuelve a ejecutar las pruebas.
10. El usuario humano solicita a Copilot una revision independiente final. Copilot solo reporta hallazgos y nunca edita.
11. Si Copilot encuentra un defecto, Chipi lo consolida y el usuario humano puede autorizar otra correccion de Codex; despues se repite la revision independiente.
12. Se permiten como maximo dos rondas de correccion en total. Una tercera requiere una nueva decision humana.
13. El usuario humano acepta o rechaza la pieza antes de pasar a la siguiente.

## Plantilla de ficha de pieza

```text
ID:
Nombre:
Objetivo:
Problema que resuelve:
Fuentes obligatorias:
Decisiones ya aprobadas:
Archivos permitidos:
Archivos prohibidos:
Entradas:
Salida esperada:
Criterios de aceptacion:
Pruebas obligatorias:
Evidencias que debe devolver:
Limites de tiempo, costo e iteraciones:
Condiciones para detenerse y preguntar:
```

## Encargo para Antigravity

```text
Actua como constructor inicial de la pieza indicada. Lee primero la ficha completa y las fuentes obligatorias. Modifica solamente los archivos permitidos. No amplíes el alcance ni agregues tecnologias no solicitadas.

Antes de editar, informa tu plan y los archivos previstos. Despues implementa, ejecuta las pruebas y verifica visualmente cuando exista interfaz. Si falta una decision que cambia el producto, detente y pregunta.

Devuelve: resumen, archivos modificados, pruebas y resultados, capturas o recorrido visual, supuestos, errores, riesgos y asuntos pendientes. No declares exito si una prueba no fue ejecutada.
```

## Encargo para una correccion de Codex

```text
Autorizo explicitamente a Codex a corregir los hallazgos enumerados de la pieza indicada. Puede modificar exclusivamente los archivos listados en este encargo.

No puede crear capacidades nuevas, modificar archivos no enumerados, instalar dependencias, tocar contratos aceptados ni ampliar el alcance. Debe inspeccionar primero, aplicar la correccion minima, ejecutar las pruebas indicadas y devolver evidencia verificable.

Si la correccion requiere otro archivo, una decision de producto o una accion prohibida, debe detenerse y solicitar una nueva decision humana antes de editar.
```

## Encargo para Copilot

```text
Actua exclusivamente como revisor independiente. No modifiques archivos, no abras un PR de correccion y no implementes soluciones.

Compara el cambio con la ficha aprobada. Revisa alcance, comportamiento, pruebas, regresiones, seguridad, permisos, persistencia, idempotencia, limites de costo o reintentos y etiquetado de simulaciones.

Reporta cada hallazgo con: severidad, evidencia, archivo o ubicacion, impacto y correccion recomendada. Si no encuentras problemas, indica que revisaste y que evidencia verificaste; no afirmes mas de lo demostrado.
```

## Paquete que el usuario humano devuelve a Chipi

```text
ID de pieza:
Herramienta usada: Antigravity
Resumen del constructor:
Archivos modificados:
Pruebas ejecutadas:
Resultados:
Capturas o video:
Errores o bloqueos:
Decisiones tomadas durante la ejecucion:
Correcciones autorizadas a Codex:
Revision de Copilot:
```

## Regla central

Antigravity crea la version inicial. Codex coordina, inspecciona y aplica solo las correcciones autorizadas. Copilot revisa de forma independiente sin editar. El usuario humano decide y aprueba.
