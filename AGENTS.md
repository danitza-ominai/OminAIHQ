# OminAI HQ - Instrucciones del equipo constructor

## Alcance

Estas instrucciones aplican a todo el trabajo dentro de `OminAIHQ`.

OminAI HQ es una oficina agentic para convertir una mision en un `Venture Build Package`. Mantener separados:

- Ominai: compania paraguas.
- OminAI HQ: producto actual y participante del hackathon.
- OminAI Business OS: producto independiente.
- Omi: exclusivo de Business OS.
- OminaiTech Engine: integracion futura, fuera del MVP.

## Autoridad y roles

- **Usuario humano (Niko) - A0 humana:** define la mision, decide prioridades y ejerce la aprobacion humana de alcance, construccion, despliegue y entrega.
- **NotebookLM - fuente interna:** extrae requisitos, practicas y contradicciones de las fuentes cargadas. No decide producto ni modifica codigo.
- **Gemini - investigador:** verifica informacion externa y fuentes oficiales vigentes. No modifica codigo.
- **Chipi/Codex - coordinador, arquitecto, integrador y corrector autorizado:** inspecciona, reconcilia evidencia, divide el trabajo, redacta instrucciones, define criterios de aceptacion y revisa resultados. Puede corregir codigo solo despues de una autorizacion humana explicita que enumere los archivos y el alcance exactos.
- **Antigravity - constructor inicial:** crea la version inicial de cada pieza aprobada. No realiza las correcciones posteriores salvo una nueva decision humana que cambie expresamente este flujo.
- **GitHub Copilot - revisor:** revisa diffs, pruebas, seguridad y cumplimiento. No implementa correcciones ni modifica archivos.
- **Claude:** excluido del equipo y del flujo de trabajo.

Chipi/Codex no debe realizar la construccion inicial de una pieza. Solo puede modificar codigo de producto como corrector, despues de una autorizacion humana explicita para una tarea concreta, con una lista cerrada de archivos y sin ampliar el alcance. Puede crear o actualizar documentacion de coordinacion cuando el usuario humano lo solicite.

## Forma de trabajo

1. Trabajar una pieza pequena por vez.
2. Leer las fuentes aplicables antes de proponer cambios.
3. Separar hechos confirmados, practicas de clase, decisiones, propuestas y pendientes.
4. Chipi prepara una ficha de pieza y el prompt para Antigravity.
5. El usuario humano aprueba el encargo y lo ejecuta en Antigravity.
6. Antigravity devuelve archivos modificados, pruebas, capturas, errores y decisiones.
7. Chipi inspecciona el resultado contra los criterios de aceptacion.
8. Si existen hallazgos, Chipi prepara una correccion cerrada y el usuario humano autoriza expresamente los archivos exactos; Codex aplica la correccion y vuelve a ejecutar las pruebas.
9. Copilot realiza una revision independiente final y solo reporta hallazgos.
10. Si Copilot encuentra un defecto, Chipi lo consolida y el usuario humano puede autorizar otra correccion de Codex; Copilot vuelve a revisar el resultado corregido.
11. Se permiten como maximo dos rondas de correccion en total. Una tercera ronda requiere una nueva decision humana.
12. El usuario humano acepta o rechaza la pieza antes de pasar a la siguiente.

## Reglas de construccion

- Antigravity es el unico constructor inicial de cada pieza; Codex solo actua despues como corrector autorizado.
- Una correccion de Codex debe indicar los hallazgos que resuelve y la lista exacta de archivos que puede modificar.
- Codex no puede crear capacidades nuevas ni aprovechar una correccion para ampliar el alcance aprobado.
- No permitir ediciones simultaneas de los mismos archivos.
- Toda tarea debe indicar objetivo, fuentes, archivos permitidos, archivos prohibidos, salida, pruebas y criterios de aceptacion.
- Usar funciones para trabajo determinista y agentes solo cuando se necesite razonamiento.
- Limitar iteraciones, tiempo, profundidad, tokens, reintentos y costo.
- No exponer ni guardar Chain-of-Thought. Registrar acciones, herramientas, fuentes, decisiones resumidas, resultados y aprobaciones.
- Mantener correos, pagos, compras, publicaciones, eliminaciones, despliegues y escrituras externas bajo aprobacion humana explicita.
- No afirmar que una capacidad esta implementada o lista para produccion sin evidencia ejecutable.
- No convertir MCP, A2A, Agent Engine, BigQuery, AlloyDB, Cloud SQL u otras tecnologias opcionales en requisitos sin necesidad demostrada.

## Reglas de revision

Copilot y Chipi deben revisar, como minimo:

- Correspondencia con la ficha aprobada.
- Cambios fuera de alcance.
- Errores funcionales y regresiones.
- Pruebas faltantes o que no demuestran el comportamiento.
- Riesgos de seguridad, permisos y datos.
- Acciones no idempotentes o estados no reanudables.
- Costos, bucles o reintentos sin limites.
- Capacidades simuladas que no esten etiquetadas.

Los revisores reportan hallazgos con severidad, evidencia, archivo o ubicacion, impacto y correccion recomendada. Durante la revision no modifican el codigo. Codex solo puede pasar de revisor a corrector despues de recibir la autorizacion humana explicita correspondiente.

## Orden inicial de construccion

1. Requisitos y decisiones vigentes.
2. Contratos y estados.
3. Estructura minima del proyecto.
4. Recorrido `Mision -> Venture Build Package`.
5. Coordinador.
6. Un agente especializado por vez.
7. Evidencia y trazabilidad.
8. Persistencia y memoria.
9. Evaluacion y aprobacion humana.
10. Interfaz, pruebas integrales, despliegue y demo.
