# contracts/core — Contratos nucleares de OminAI HQ

**Version de schemas:** 1.0.0  
**Contrato rector:** `CONTRATO-MVP-v1.md`, version `1.2-aprobada`  
**Pieza:** PZ-001A — Contratos nucleares y maquina de estados  
**Fecha:** 29 de agosto de 2026 (correccion 3)

## Alcance

Este directorio contiene los contratos estructurados que definen la identidad de una mision, sus eventos, aprobaciones, checkpoints, errores y transiciones de estado.

Estos archivos son la **referencia de los estados nucleares** pero **no reemplazan la autoridad normativa** de `CONTRATO-MVP-v1.md`. En caso de discrepancia, prevalece el contrato aprobado.

## Declaracion expresa

Estos contratos **no implementan ni prueban**:

- Runtime o servicio de ejecucion.
- Persistencia o base de datos.
- Agentes internos ni sus contratos individuales.
- Interfaz de usuario.
- Despliegue en nube o infraestructura.
- Memoria de largo plazo.

## Integridad referencial y ciclo de vida

Los campos `approval_refs`, `last_checkpoint_id`, `artifacts` y `authorizations` contienen **identificadores** cuya existencia real **requiere validacion determinista entre registros** implementada por el runtime correspondiente (pieza futura). Una referencia no nula ausente produce `NOT_FOUND` y detiene la transicion dependiente.

JSON Schema valida **formato, tipo, enumeraciones y clave de idempotencia** de estos registros. La prevencion de doble respuesta sobre un registro `CONSUMIDA` y la reanudacion con estados previos se aplican mediante el **ciclo de vida determinista entre registros** fuera de JSON Schema.

## Archivos

| Archivo | Contenido |
|---|---|
| `mission.schema.json` | Schema Draft 2020-12 para la identidad de una mision. Cuando BLOQUEADA o PAUSADA, exige `resumable_state` no null. |
| `event.schema.json` | Schema Draft 2020-12 para eventos de trazabilidad. |
| `approval.schema.json` | Schema Draft 2020-12 para aprobaciones humanas. `actor_role` restringido a `usuario_humano`. Incluye `idempotency_key`. `EXPIRADA` exige `expiration` no null. Codifica reglas de comentario y condiciones segun decision. |
| `checkpoint.schema.json` | Schema Draft 2020-12 para puntos de control reanudables. `resumable_state` siempre requerido. |
| `error.schema.json` | Schema Draft 2020-12 para errores tipados. Codifica mediante `oneOf` las diez combinaciones exactas de categoria, intento, permiso de reintento y accion exigidas por 11.3. |
| `state-machine.json` | Maquina de estados declarativa con 15 estados de mision, 8 de tarea, 76 transiciones de mision y 13 de tarea expandidas. Incluye reglas de integridad referencial, ciclo de vida de aprobaciones e idempotencia. |
| `examples/` | Ejemplos positivos y negativos para validacion. |

## Estados

### Mision (15)

`BORRADOR`, `ACLARACION_REQUERIDA`, `LISTA_PARA_PLAN`, `PLAN_EN_REVISION`, `AUTORIZADA_PARA_EJECUTAR`, `EN_EJECUCION`, `BLOQUEADA`, `PAUSADA`, `EN_CONSOLIDACION`, `EN_EVALUACION`, `VBP_EN_REVISION`, `VBP_RECHAZADO`, `VBP_APROBADO`, `FINALIZADA`, `CANCELADA`

Terminales: `FINALIZADA`, `CANCELADA`.

### Tarea (8)

`PENDIENTE`, `LISTA`, `EN_CURSO`, `COMPLETA`, `PARCIAL`, `BLOQUEADA`, `FALLIDA`, `CANCELADA`

Terminales: `COMPLETA`, `PARCIAL`, `FALLIDA`, `CANCELADA`.

### Aprobacion (3)

`PENDIENTE`, `CONSUMIDA`, `EXPIRADA`

Terminales: `CONSUMIDA`, `EXPIRADA`.

## Invariantes (seccion 4.3)

1. Cada transicion registra `mission_id`, estado anterior, estado nuevo, evento, actor, fecha/hora, version, motivo y referencia.
2. `AUTORIZADA_PARA_EJECUTAR`, `VBP_APROBADO`, `FINALIZADA` y `CANCELADA` nunca se alcanzan por inferencia de un modelo.
3. Una solicitud duplicada con la misma clave de idempotencia y mismo contenido no produce segundo efecto; misma clave y contenido diferente genera conflicto y rechazo (`INVALID_INPUT`).
4. Cancelar o rechazar no elimina evidencia ni auditoria.
5. Reanudar usa el ultimo punto de control valido y no repite acciones confirmadas.

## Politica finita de errores (seccion 11.3)

Los errores sin reintento (`INVALID_INPUT`, `NOT_FOUND`, `PERMISSION_DENIED`, `DEPENDENCY_FAILED`, `BUDGET_EXHAUSTED` y `SYSTEM_ERROR`) exigen `max_retries=0`, `current_attempt=0`, `retry_allowed=false` y una accion exclusiva de su categoria.

Las dos categorias reintentables dependen del numero de intento:

| Categoria | Intento | `retry_allowed` | `required_action` |
|---|---:|---:|---|
| `TRANSIENT_FAILURE` | 0 | `true` | `reintentar_una_vez` |
| `TRANSIENT_FAILURE` | 1 | `false` | `guardar_checkpoint_y_bloquear` |
| `SCHEMA_INVALID` | 0 | `true` | `solicitar_una_regeneracion` |
| `SCHEMA_INVALID` | 1 | `false` | `bloquear_mision` |

En ambos casos `max_retries=1`. No existe intento 2, no se reinicia el contador y una accion de otra categoria o de otro numero de intento es invalida.

## Compatibilidad

- **Dialecto JSON Schema:** Draft 2020-12 (`https://json-schema.org/draft/2020-12/schema`)
- **Version de schemas:** `1.0.0`
- **Cambios incompatibles:** requieren nueva version y migracion o rechazo explicito (RNF-013).

## Validacion

Los schemas pueden validarse con cualquier validador compatible con JSON Schema Draft 2020-12. Ejemplo con Python:

```python
import json
from jsonschema import Draft202012Validator

with open("mission.schema.json") as f:
    schema = json.load(f)

Draft202012Validator.check_schema(schema)  # metavalidacion
validator = Draft202012Validator(schema)
validator.validate(instance)  # validacion de datos
```

No se requiere instalar dependencias adicionales si `jsonschema >= 4.18` ya esta disponible.
