"""OminAI HQ - Modulo de ensayo de intake de mision y propuesta de plan controlado (SIMULADA).

Implementa el tramo BORRADOR -> LISTA_PARA_PLAN -> PLAN_EN_REVISION (o ACLARACION_REQUERIDA)
de forma determinista, efimera y en memoria, sin agentes reales, sin persistencia
y sin aprobacion automatica. Cumple con la Ficha PZ-003A y CONTRATO-MVP-v1.md.
"""

from __future__ import annotations

import copy
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    # No sustituir el validador: el arranque devolvera un error sin continuar.
    Draft202012Validator = None
    FormatChecker = None

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTRACTS_CORE_DIR = PROJECT_ROOT / "contracts" / "core"
DEFAULT_FIXTURE_PATH = PROJECT_ROOT / "examples" / "demo_mission.json"

MAX_FILE_BYTES = 65536  # 64 KiB
MAX_STRING_LENGTH = 4000
MAX_COLLECTION_ITEMS = 20
_UNSET = object()
SIMULATED_ACTOR_ROLE = "chief_of_staff"

RFC3339_DATE_TIME_PATTERN = re.compile(
    r"^[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])"
    r"T(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]"
    r"(?:\.[0-9]+)?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])$"
)

ALLOWED_FIXTURE_KEYS = {
    "simulation_status",
    "user_id",
    "title",
    "objective",
    "context",
    "expected_result",
    "constraints",
    "assumptions",
    "pending_decisions",
    "plan_template",
}

ALLOWED_TASK_KEYS = {
    "task_id",
    "objective",
    "agent_role",
    "input_refs",
    "expected_output",
    "acceptance_criteria",
    "dependencies",
    "allowed_tool_categories",
    "limits",
    "status",
    "simulation_status",
}

ALLOWED_TASK_LIMIT_KEYS = {
    "max_attempts",
    "max_seconds",
    "max_budget_usd",
}

ALLOWED_PLAN_TEMPLATE_KEYS = {
    "title",
    "tasks",
    "risks",
}

EXPECTED_AGENT_ROLES_SEQUENCE = [
    "research_evidence_analyst",
    "product_architect",
    "delivery_planner",
    "governance_risk",
]


def is_rfc3339_date_time(value: Any) -> bool:
    """Valida date-time RFC 3339 de forma determinista sin dependencias externas."""
    if not isinstance(value, str):
        return True
    if RFC3339_DATE_TIME_PATTERN.fullmatch(value) is None:
        return False
    try:
        normalized = f"{value[:-1]}+00:00" if value.endswith("Z") else value
        datetime.fromisoformat(normalized)
        return True
    except (ValueError, TypeError):
        return False


def get_format_checker() -> FormatChecker:
    """Retorna un FormatChecker con validacion efectiva de date-time."""
    fc = FormatChecker()
    fc.checks("date-time", raises=ValueError)(is_rfc3339_date_time)
    return fc


def load_core_contracts() -> Tuple[dict, dict, dict, dict]:
    """Carga los schemas nucleares y la maquina de estados desde contracts/core."""
    mission_schema_path = CONTRACTS_CORE_DIR / "mission.schema.json"
    event_schema_path = CONTRACTS_CORE_DIR / "event.schema.json"
    error_schema_path = CONTRACTS_CORE_DIR / "error.schema.json"
    state_machine_path = CONTRACTS_CORE_DIR / "state-machine.json"

    with open(mission_schema_path, "r", encoding="utf-8") as f:
        mission_schema = json.load(f)
    with open(event_schema_path, "r", encoding="utf-8") as f:
        event_schema = json.load(f)
    with open(error_schema_path, "r", encoding="utf-8") as f:
        error_schema = json.load(f)
    with open(state_machine_path, "r", encoding="utf-8") as f:
        state_machine = json.load(f)

    return mission_schema, event_schema, error_schema, state_machine


def make_error_payload(error_code: str, message: str) -> dict:
    """Construye un error estructurado segun error.schema.json y matriz 11.3."""
    if error_code == "INVALID_INPUT":
        return {
            "schema_version": "1.0.0",
            "error_code": "INVALID_INPUT",
            "message": message,
            "retry_allowed": False,
            "max_retries": 0,
            "current_attempt": 0,
            "recoverable": True,
            "required_action": "solicitar_correccion",
        }
    elif error_code == "NOT_FOUND":
        return {
            "schema_version": "1.0.0",
            "error_code": "NOT_FOUND",
            "message": message,
            "retry_allowed": False,
            "max_retries": 0,
            "current_attempt": 0,
            "recoverable": True,
            "required_action": "solicitar_verificacion_o_fuente_alternativa",
        }
    elif error_code == "SCHEMA_INVALID":
        return {
            "schema_version": "1.0.0",
            "error_code": "SCHEMA_INVALID",
            "message": message,
            "retry_allowed": True,
            "max_retries": 1,
            "current_attempt": 0,
            "recoverable": True,
            "required_action": "solicitar_una_regeneracion",
        }
    elif error_code == "SYSTEM_ERROR":
        return {
            "schema_version": "1.0.0",
            "error_code": "SYSTEM_ERROR",
            "message": message,
            "retry_allowed": False,
            "max_retries": 0,
            "current_attempt": 0,
            "recoverable": True,
            "required_action": "conservar_diagnostico_y_checkpoint",
        }
    else:
        return {
            "schema_version": "1.0.0",
            "error_code": error_code,
            "message": message,
            "retry_allowed": False,
            "max_retries": 0,
            "current_attempt": 0,
            "recoverable": False,
            "required_action": "detener_y_escalar",
        }


def _check_string_and_collection_limits(obj: Any, path: str = "") -> Optional[str]:
    """Valida recursivamente que ninguna cadena exceda 4000 caracteres ni coleccion 20 items."""
    if isinstance(obj, str):
        if len(obj) > MAX_STRING_LENGTH:
            return f"Cadena en '{path}' excede el limite de {MAX_STRING_LENGTH} caracteres (longitud: {len(obj)})."
    elif isinstance(obj, list):
        if len(obj) > MAX_COLLECTION_ITEMS:
            return f"Coleccion en '{path}' excede el limite de {MAX_COLLECTION_ITEMS} elementos (tamano: {len(obj)})."
        for i, item in enumerate(obj):
            err = _check_string_and_collection_limits(item, f"{path}[{i}]")
            if err:
                return err
    elif isinstance(obj, dict):
        if len(obj) > MAX_COLLECTION_ITEMS:
            return f"Objeto en '{path}' excede el limite de {MAX_COLLECTION_ITEMS} claves."
        for k, v in obj.items():
            if not isinstance(k, str):
                return "Las claves de los objetos deben ser cadenas."
            if len(k) > MAX_STRING_LENGTH:
                return f"Una clave excede el limite de {MAX_STRING_LENGTH} caracteres."
            # No reflejar claves desconocidas que puedan contener datos sensibles.
            safe_key = k if k in (ALLOWED_FIXTURE_KEYS | ALLOWED_PLAN_TEMPLATE_KEYS |
                                  ALLOWED_TASK_KEYS | ALLOWED_TASK_LIMIT_KEYS) else "clave_no_permitida"
            err = _check_string_and_collection_limits(v, f"{path}.{safe_key}" if path else safe_key)
            if err:
                return err
    return None


def validate_raw_fixture_data(data: Any) -> Tuple[Optional[dict], List[dict]]:
    """Valida estructura general, tipos y limites del objeto de entrada."""
    errors: List[dict] = []

    if not isinstance(data, dict):
        errors.append(make_error_payload("INVALID_INPUT", "La raiz de la entrada debe ser un objeto JSON."))
        return None, errors

    unknown_keys = set(data.keys()) - ALLOWED_FIXTURE_KEYS
    if unknown_keys:
        errors.append(
            make_error_payload(
                "INVALID_INPUT",
                "La entrada contiene claves no permitidas.",
            )
        )
        return None, errors

    try:
        limits_error = _check_string_and_collection_limits(data)
    except RecursionError:
        limits_error = "La entrada contiene una estructura anidada no procesable."
    if limits_error:
        errors.append(make_error_payload("INVALID_INPUT", limits_error))
        return None, errors

    # simulation_status
    sim_status = data.get("simulation_status")
    if sim_status != "SIMULADA":
        errors.append(
            make_error_payload(
                "INVALID_INPUT",
                "simulation_status debe ser exactamente 'SIMULADA'.",
            )
        )

    # user_id
    user_id = data.get("user_id")
    if not isinstance(user_id, str) or not user_id.strip():
        errors.append(make_error_payload("INVALID_INPUT", "user_id es obligatorio y debe ser una cadena no vacia."))

    # title
    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append(make_error_payload("INVALID_INPUT", "title es obligatorio y debe ser una cadena no vacia."))

    # Type validation for optional/evaluable brief fields
    for field in ["objective", "context", "expected_result"]:
        if field in data and data[field] is not None and not isinstance(data[field], str):
            errors.append(
                make_error_payload(
                    "INVALID_INPUT",
                    f"El campo '{field}' debe ser una cadena o null.",
                )
            )

    if "constraints" in data and data["constraints"] is not None:
        if not isinstance(data["constraints"], list):
            errors.append(make_error_payload("INVALID_INPUT", "El campo 'constraints' debe ser una lista de cadenas."))
        else:
            for item in data["constraints"]:
                if not isinstance(item, str):
                    errors.append(
                        make_error_payload("INVALID_INPUT", "Todos los elementos de 'constraints' deben ser cadenas.")
                    )
                    break

    for field in ["assumptions", "pending_decisions"]:
        if field in data:
            if not isinstance(data[field], list):
                errors.append(make_error_payload("INVALID_INPUT", f"El campo '{field}' debe ser una lista de cadenas."))
            else:
                for item in data[field]:
                    if not isinstance(item, str):
                        errors.append(
                            make_error_payload("INVALID_INPUT", f"Todos los elementos de '{field}' deben ser cadenas.")
                        )
                        break

    if "plan_template" in data and data["plan_template"] is not None:
        if not isinstance(data["plan_template"], dict):
            errors.append(make_error_payload("INVALID_INPUT", "El campo 'plan_template' debe ser un objeto."))

    if errors:
        return None, errors

    return data, []


def evaluate_brief_fields(data: dict) -> Tuple[List[str], List[str], List[str]]:
    """Evalua campos minimos del brief y detecta faltantes o supuestos/decisiones pendientes.
    
    Retorna (pending_fields, assumptions, pending_decisions).
    """
    pending_fields: List[str] = []

    for field in ["objective", "context", "expected_result"]:
        val = data.get(field)
        if val is None or (isinstance(val, str) and not val.strip()):
            pending_fields.append(field)

    constraints = data.get("constraints")
    if constraints is None:
        pending_fields.append("constraints")

    assumptions = data.get("assumptions", [])
    pending_decisions = data.get("pending_decisions", [])

    return pending_fields, assumptions, pending_decisions


def validate_plan_template(template: Any) -> Tuple[Optional[dict], List[dict]]:
    """Valida la plantilla de plan preescrito y sus cuatro tareas secuenciales."""
    errors: List[dict] = []

    if not isinstance(template, dict):
        errors.append(make_error_payload("INVALID_INPUT", "plan_template debe ser un objeto."))
        return None, errors

    unknown_keys = set(template.keys()) - ALLOWED_PLAN_TEMPLATE_KEYS
    if unknown_keys:
        errors.append(
            make_error_payload(
                "INVALID_INPUT",
                "plan_template contiene claves no permitidas.",
            )
        )
        return None, errors

    title = template.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append(make_error_payload("INVALID_INPUT", "plan_template.title debe ser una cadena no vacia."))

    risks = template.get("risks")
    if risks is None or not isinstance(risks, list):
        errors.append(make_error_payload("INVALID_INPUT", "plan_template.risks debe ser una lista de cadenas."))
    else:
        for r in risks:
            if not isinstance(r, str):
                errors.append(make_error_payload("INVALID_INPUT", "Cada elemento de risks debe ser una cadena."))
                break

    tasks = template.get("tasks")
    if not isinstance(tasks, list):
        errors.append(make_error_payload("INVALID_INPUT", "plan_template.tasks debe ser una lista de 4 tareas."))
        return None, errors

    if len(tasks) != 4:
        errors.append(
            make_error_payload(
                "INVALID_INPUT",
                f"plan_template.tasks debe contener exactamente 4 tareas secuenciales, contiene: {len(tasks)}",
            )
        )
        return None, errors

    # Comprobar todos los objetos antes de consultar dependencias entre tareas.
    for idx, task in enumerate(tasks):
        if not isinstance(task, dict):
            errors.append(make_error_payload("INVALID_INPUT", f"Tarea en indice {idx} debe ser un objeto."))
    if errors:
        return None, errors

    seen_task_ids: Set[str] = set()
    validated_tasks: List[dict] = []

    for idx, task in enumerate(tasks):

        task_unknown_keys = set(task.keys()) - ALLOWED_TASK_KEYS
        if task_unknown_keys:
            errors.append(
                make_error_payload(
                    "INVALID_INPUT",
                    f"Tarea {idx} contiene claves no permitidas.",
                )
            )

        task_id = task.get("task_id")
        if not isinstance(task_id, str) or not task_id.strip():
            errors.append(make_error_payload("INVALID_INPUT", f"task_id invalido en tarea {idx}."))
        elif task_id in seen_task_ids:
            errors.append(make_error_payload("INVALID_INPUT", f"task_id duplicado en tarea {idx}."))
        else:
            seen_task_ids.add(task_id)

        objective = task.get("objective")
        if not isinstance(objective, str) or not objective.strip():
            errors.append(make_error_payload("INVALID_INPUT", f"objective no valido en tarea {idx}."))

        expected_role = EXPECTED_AGENT_ROLES_SEQUENCE[idx]
        agent_role = task.get("agent_role")
        if agent_role != expected_role:
            errors.append(
                make_error_payload(
                    "INVALID_INPUT",
                    f"agent_role en tarea {idx} debe ser '{expected_role}'.",
                )
            )

        input_refs = task.get("input_refs")
        if (not isinstance(input_refs, list) or not input_refs or
                any(not isinstance(ref, str) or ref != "brief" for ref in input_refs)):
            errors.append(
                make_error_payload(
                    "INVALID_INPUT",
                    f"input_refs en tarea {idx} debe ser una lista no vacia con solo la referencia 'brief'.",
                )
            )

        expected_output = task.get("expected_output")
        if not isinstance(expected_output, str) or not expected_output.strip():
            errors.append(make_error_payload("INVALID_INPUT", f"expected_output no valido en tarea {idx}."))

        acceptance_criteria = task.get("acceptance_criteria")
        if not isinstance(acceptance_criteria, list) or len(acceptance_criteria) == 0:
            errors.append(
                make_error_payload(
                    "INVALID_INPUT",
                    f"acceptance_criteria en tarea {idx} debe ser una lista no vacia de cadenas.",
                )
            )
        else:
            for ac in acceptance_criteria:
                if not isinstance(ac, str) or not ac.strip():
                    errors.append(
                        make_error_payload(
                            "INVALID_INPUT",
                            f"acceptance_criteria en tarea {idx} contiene elementos no validos.",
                        )
                    )
                    break

        dependencies = task.get("dependencies")
        if not isinstance(dependencies, list):
            errors.append(make_error_payload("INVALID_INPUT", f"dependencies en tarea {idx} debe ser una lista."))
        else:
            if idx == 0:
                if len(dependencies) != 0:
                    errors.append(
                        make_error_payload(
                            "INVALID_INPUT",
                            "La primera tarea no debe tener dependencias.",
                        )
                    )
            else:
                prev_task_id = tasks[idx - 1].get("task_id")
                if dependencies != [prev_task_id]:
                    errors.append(
                        make_error_payload(
                            "INVALID_INPUT",
                            f"Tarea {idx} debe depender exclusivamente de la tarea anterior.",
                        )
                    )

        allowed_tools = task.get("allowed_tool_categories")
        if not isinstance(allowed_tools, list) or len(allowed_tools) != 0:
            errors.append(
                make_error_payload(
                    "INVALID_INPUT",
                    f"allowed_tool_categories en tarea {idx} debe ser una lista vacia [] en esta pieza.",
                )
            )

        limits = task.get("limits")
        if not isinstance(limits, dict):
            errors.append(make_error_payload("INVALID_INPUT", f"limits en tarea {idx} debe ser un objeto."))
        else:
            limit_unknown = set(limits.keys()) - ALLOWED_TASK_LIMIT_KEYS
            if limit_unknown:
                errors.append(
                    make_error_payload(
                        "INVALID_INPUT",
                        f"limits de tarea {idx} contiene claves no permitidas.",
                    )
                )
            if type(limits.get("max_attempts")) is not int or limits["max_attempts"] != 2:
                errors.append(make_error_payload("INVALID_INPUT", f"max_attempts en tarea {idx} debe ser el entero 2, sin booleanos."))
            if type(limits.get("max_seconds")) is not int or limits["max_seconds"] != 300:
                errors.append(make_error_payload("INVALID_INPUT", f"max_seconds en tarea {idx} debe ser el entero 300, sin booleanos."))
            if type(limits.get("max_budget_usd")) not in (int, float) or limits["max_budget_usd"] != 0:
                errors.append(make_error_payload("INVALID_INPUT", f"max_budget_usd en tarea {idx} debe ser el numero 0, sin booleanos."))

        status = task.get("status")
        if status != "PENDIENTE":
            errors.append(
                make_error_payload(
                    "INVALID_INPUT",
                    f"status en tarea {idx} debe ser 'PENDIENTE'.",
                )
            )

        sim_status = task.get("simulation_status")
        if sim_status != "SIMULADA":
            errors.append(
                make_error_payload(
                    "INVALID_INPUT",
                    f"simulation_status en tarea {idx} debe ser 'SIMULADA'.",
                )
            )

        validated_tasks.append(copy.deepcopy(task))

    if errors:
        return None, errors

    clean_template = {
        "title": title,
        "risks": copy.deepcopy(risks),
        "tasks": validated_tasks,
    }
    return clean_template, []


def make_event(
    event_id: str,
    mission_id: str,
    actor: str,
    actor_role: str,
    action: str,
    timestamp: str,
    version: int,
    previous_state: Optional[str],
    new_state: str,
    result_summary: str,
    idempotency_key: str,
    task_id: Optional[str] = None,
    tool_or_category: Optional[str] = None,
    source_or_artifact: Optional[str] = None,
    typed_error: Optional[dict] = None,
    attempt: int = 0,
    budget_consumed: Optional[dict] = None,
    related_approval_id: Optional[str] = None,
) -> dict:
    """Crea un registro de evento conforme a contracts/core/event.schema.json."""
    return {
        "schema_version": "1.0.0",
        "event_id": event_id,
        "mission_id": mission_id,
        "task_id": task_id,
        "actor": actor,
        "actor_role": actor_role,
        "action": action,
        "timestamp": timestamp,
        "version": version,
        "previous_state": previous_state,
        "new_state": new_state,
        "tool_or_category": tool_or_category,
        "source_or_artifact": source_or_artifact,
        "result_summary": result_summary,
        "typed_error": typed_error,
        "attempt": attempt,
        "budget_consumed": budget_consumed,
        "related_approval_id": related_approval_id,
        "idempotency_key": idempotency_key,
    }


def _empty_envelope() -> dict:
    """Sobre sin datos ni efectos, incluso cuando falla el arranque."""
    return {
        "simulation_status": "SIMULADA",
        "mission": None,
        "brief": None,
        "plan": None,
        "events": [],
        "pending_fields": [],
        "errors": [],
        "next_action": "",
    }


def _system_failure(message: str) -> Tuple[int, dict]:
    """Diagnostico minimo; no afirma validacion si el validador no esta disponible."""
    envelope = _empty_envelope()
    envelope["errors"] = [make_error_payload("SYSTEM_ERROR", message)]
    envelope["next_action"] = "Detener el ensayo y solicitar revision; no se guardo ningun checkpoint."
    return 1, envelope


def _transition_policy_error(
    state_machine: dict, transition_id: str, previous_state: str, new_state: str,
) -> Optional[dict]:
    """Guardas explicitas del actor simulado; nunca interpreta guard como codigo."""
    transitions = state_machine.get("mission_transitions")
    if not isinstance(transitions, list):
        return make_error_payload("SYSTEM_ERROR", "La lista de transiciones no es valida.")
    matches = [t for t in transitions if isinstance(t, dict) and t.get("id") == transition_id]
    if (len(matches) != 1 or matches[0].get("from") != previous_state or
            matches[0].get("to") != new_state):
        return make_error_payload("SYSTEM_ERROR", f"Transicion {transition_id} ausente o inconsistente.")
    transition = matches[0]
    authority = transition.get("authority")
    # Son las unicas politicas comprendidas por este tramo del demo.
    if authority == "chief_of_staff":
        actor_allowed = SIMULATED_ACTOR_ROLE == "chief_of_staff"
    elif authority == "regla_determinista_o_chief_of_staff":
        actor_allowed = SIMULATED_ACTOR_ROLE == "chief_of_staff"
    else:
        actor_allowed = False
    if not actor_allowed:
        return make_error_payload("PERMISSION_DENIED", f"Autoridad ausente, desconocida o incompatible en {transition_id}.")
    if transition.get("requires_human_approval") is not False:
        return make_error_payload(
            "PERMISSION_DENIED",
            f"{transition_id} exige aprobacion humana o no declara una politica valida; el demo no puede continuar.",
        )
    return None


def _reject_non_json_constant(value: str) -> None:
    raise ValueError("Constante numerica no permitida en JSON.")


def run_demo_intake(
    fixture_path: Optional[Path | str] = None,
    raw_data: Any = _UNSET,
    now_fn: Optional[Callable[[], datetime]] = None,
    id_generator: Optional[Callable[[str], str]] = None,
) -> Tuple[int, dict]:
    """Frontera del ensayo: fallos de arranque o internos siempre son no exitosos."""
    if Draft202012Validator is None or FormatChecker is None:
        return _system_failure("jsonschema no esta disponible; no se realizo validacion ni se ejecuto el ensayo.")
    try:
        return _run_demo_intake(fixture_path, raw_data, now_fn, id_generator)
    except Exception:
        # No mostrar instancias del validador, trazas, rutas ni texto de excepciones.
        # Los rechazos previstos de entrada y permisos se resuelven en su frontera.
        return _system_failure("Fallo interno o de contratos; el ensayo se detuvo sin resultado valido.")


def _run_demo_intake(
    fixture_path: Optional[Path | str] = None,
    raw_data: Any = _UNSET,
    now_fn: Optional[Callable[[], datetime]] = None,
    id_generator: Optional[Callable[[str], str]] = None,
) -> Tuple[int, dict]:
    """Ejecuta el ensayo determinista de intake de mision.
    
    Retorna (exit_code, envelope_dict).
    Codigos de salida:
      0: Brief completo, plan SIMULADA generado y presentado en PLAN_EN_REVISION.
      3: Brief incompleto o con supuestos/decisiones pendientes (ACLARACION_REQUERIDA).
      1: Error de validacion de entrada o plantilla (INVALID_INPUT / SCHEMA_INVALID).
      2: Archivo no encontrado (NOT_FOUND).
    """
    mission_schema, event_schema, error_schema, state_machine = load_core_contracts()
    format_checker = get_format_checker()
    mission_validator = Draft202012Validator(mission_schema, format_checker=format_checker)
    event_validator = Draft202012Validator(event_schema, format_checker=format_checker)
    error_validator = Draft202012Validator(error_schema, format_checker=format_checker)

    now_dt = now_fn() if now_fn else datetime.now(timezone.utc)
    now_iso = now_dt.isoformat()

    def gen_id(prefix: str) -> str:
        if id_generator:
            return id_generator(prefix)
        return f"{prefix}-{uuid.uuid4().hex[:8]}"

    envelope = _empty_envelope()

    def reject_transition(transition_id: str, target_state: str) -> bool:
        err = _transition_policy_error(state_machine, transition_id, mission["current_state"], target_state)
        if err is None:
            return False
        error_validator.validate(err)
        envelope["errors"].append(err)
        envelope["next_action"] = "Transicion detenida; solicitar revision de la politica y aprobacion humana cuando corresponda."
        return True

    # 1. Carga de datos
    data: Any = None
    if raw_data is not _UNSET:
        try:
            data = copy.deepcopy(raw_data)
        except RecursionError:
            err = make_error_payload("INVALID_INPUT", "La entrada contiene una estructura anidada no procesable.")
            error_validator.validate(err)
            envelope["errors"].append(err)
            envelope["next_action"] = "Corregir la estructura de la entrada."
            return 1, envelope
    else:
        target_path = Path(fixture_path) if fixture_path else DEFAULT_FIXTURE_PATH
        try:
            # Limitar los bytes leidos, incluso si el archivo cambia de tamano.
            with open(target_path, "rb") as f:
                file_data = f.read(MAX_FILE_BYTES + 1)
            if len(file_data) > MAX_FILE_BYTES:
                err = make_error_payload(
                    "INVALID_INPUT",
                    f"El archivo excede el tamano maximo de {MAX_FILE_BYTES} bytes.",
                )
                error_validator.validate(err)
                envelope["errors"].append(err)
                envelope["next_action"] = "Reducir el tamano del archivo de entrada a menos de 64 KiB."
                return 1, envelope

            data = json.loads(file_data.decode("utf-8"), parse_constant=_reject_non_json_constant)
        except FileNotFoundError:
            err = make_error_payload("NOT_FOUND", "Archivo de fixture no encontrado.")
            error_validator.validate(err)
            envelope["errors"].append(err)
            envelope["next_action"] = "Proporcionar un archivo de fixture existente."
            return 2, envelope
        except (ValueError, RecursionError):
            err = make_error_payload("INVALID_INPUT", "La fixture no contiene JSON UTF-8 valido o su estructura no es procesable.")
            error_validator.validate(err)
            envelope["errors"].append(err)
            envelope["next_action"] = "Corregir la sintaxis JSON del archivo."
            return 1, envelope
        except OSError:
            err = make_error_payload("SYSTEM_ERROR", "No se pudo leer el archivo de entrada.")
            error_validator.validate(err)
            envelope["errors"].append(err)
            envelope["next_action"] = "Verificar permisos y accesibilidad del archivo."
            return 1, envelope

    # 2. Validacion de tipos y claves de entrada
    valid_data, validation_errors = validate_raw_fixture_data(data)
    if validation_errors:
        for err in validation_errors:
            error_validator.validate(err)
        envelope["errors"].extend(validation_errors)
        envelope["next_action"] = "Corregir los campos invalidos de la entrada."
        return 1, envelope

    assert valid_data is not None

    user_id = valid_data["user_id"]
    raw_title = valid_data["title"]
    mission_title = raw_title if raw_title.startswith("[SIMULADA]") else f"[SIMULADA] {raw_title}"
    mission_id = gen_id("MSN-SIM")

    # 3. Creacion de la mision en BORRADOR
    mission: dict = {
        "schema_version": "1.0.0",
        "mission_id": mission_id,
        "user_id": user_id,
        "title": mission_title,
        "brief_version": 1,
        "current_state": "BORRADOR",
        "resumable_state": None,
        "active_task": None,
        "counters": {
            "clarification_cycles": 0,
            "task_reasoning_attempts": 0,
            "transient_retries": 0,
            "vbp_correction_rounds": 0,
            "agent_requests": 0,
        },
        "limits": {
            "max_clarification_cycles": 3,
            "max_task_reasoning_attempts": 2,
            "max_transient_retries": 1,
            "max_vbp_correction_rounds": 2,
            "max_concurrent_missions": 1,
            "max_concurrent_agents": 1,
            "max_recursive_decomposition": 0,
            "max_agent_execution_seconds": 300,
            "max_mission_seconds": 1200,
            "max_agent_requests_per_mission": 15,
            "max_budget_usd": 25,
        },
        "approval_refs": [],
        "last_checkpoint_id": None,
        "created_at": now_iso,
        "updated_at": now_iso,
        "record_version": 1,
    }

    # Validar schema de mision inicial
    mission_validator.validate(mission)

    # Evento 1: Creacion de la mision
    creation_event = make_event(
        event_id=gen_id("EVT-CREATION"),
        mission_id=mission_id,
        actor="sistema",
        actor_role="sistema",
        action="creacion_de_mision",
        timestamp=now_iso,
        version=1,
        previous_state=None,
        new_state="BORRADOR",
        result_summary="Mision creada en estado BORRADOR (SIMULADA)",
        idempotency_key=gen_id("IDEMP-CREATION"),
    )
    event_validator.validate(creation_event)
    envelope["events"].append(creation_event)
    envelope["mission"] = mission

    # Construir representacion del brief
    brief: dict = {
        "simulation_status": "SIMULADA",
        "user_id": user_id,
        "title": raw_title,
        "objective": valid_data.get("objective"),
        "context": valid_data.get("context"),
        "expected_result": valid_data.get("expected_result"),
        "constraints": valid_data.get("constraints"),
        "assumptions": valid_data.get("assumptions", []),
        "pending_decisions": valid_data.get("pending_decisions", []),
    }
    envelope["brief"] = brief

    # 4. Evaluacion del brief
    pending_fields, assumptions, pending_decisions = evaluate_brief_fields(valid_data)
    envelope["pending_fields"] = pending_fields

    has_pending = bool(pending_fields or assumptions or pending_decisions)

    if has_pending:
        # Transicion MT-001 hacia ACLARACION_REQUERIDA
        if reject_transition("MT-001", "ACLARACION_REQUERIDA"):
            return 1, envelope

        mission["current_state"] = "ACLARACION_REQUERIDA"
        mission["counters"]["clarification_cycles"] = 1
        mission["record_version"] = 2
        mission["updated_at"] = now_iso
        mission_validator.validate(mission)

        clarification_event = make_event(
            event_id=gen_id("EVT-CLARIFICATION"),
            mission_id=mission_id,
            actor="chief_of_staff_simulado",
            actor_role=SIMULATED_ACTOR_ROLE,
            action="solicitud_de_aclaracion",
            timestamp=now_iso,
            version=2,
            previous_state="BORRADOR",
            new_state="ACLARACION_REQUERIDA",
            result_summary="Aclaracion requerida por campos faltantes o supuestos pendientes (SIMULADA)",
            idempotency_key=gen_id("IDEMP-CLARIFICATION"),
        )
        event_validator.validate(clarification_event)
        envelope["events"].append(clarification_event)

        envelope["mission"] = mission
        envelope["plan"] = None
        envelope["next_action"] = "Aclaracion humana requerida sobre campos faltantes o supuestos pendientes."
        return 3, envelope

    # 5. Brief completo: Transicion MT-002a hacia LISTA_PARA_PLAN
    if reject_transition("MT-002a", "LISTA_PARA_PLAN"):
        return 1, envelope

    mission["current_state"] = "LISTA_PARA_PLAN"
    mission["record_version"] = 2
    mission["updated_at"] = now_iso
    mission_validator.validate(mission)

    ready_event = make_event(
        event_id=gen_id("EVT-READY"),
        mission_id=mission_id,
        actor="chief_of_staff_simulado",
        actor_role=SIMULATED_ACTOR_ROLE,
        action="validacion_de_brief",
        timestamp=now_iso,
        version=2,
        previous_state="BORRADOR",
        new_state="LISTA_PARA_PLAN",
        result_summary="Brief completo validado por Chief of Staff simulado (SIMULADA)",
        idempotency_key=gen_id("IDEMP-READY"),
    )
    event_validator.validate(ready_event)
    envelope["events"].append(ready_event)

    # 6. Validar plantilla de plan
    raw_template = valid_data.get("plan_template")
    if raw_template is None:
        err = make_error_payload("INVALID_INPUT", "plan_template es obligatorio cuando el brief esta completo.")
        error_validator.validate(err)
        envelope["errors"].append(err)
        envelope["mission"] = mission
        envelope["next_action"] = "Proporcionar una plantilla de plan valida."
        return 1, envelope

    validated_template, template_errors = validate_plan_template(raw_template)
    if template_errors:
        for err in template_errors:
            error_validator.validate(err)
        envelope["errors"].extend(template_errors)
        envelope["mission"] = mission
        envelope["next_action"] = "Corregir los errores estructurales de plan_template."
        return 1, envelope

    assert validated_template is not None

    # Comprobar la politica antes de publicar el plan o cambiar el estado.
    if reject_transition("MT-004", "PLAN_EN_REVISION"):
        return 1, envelope

    # Construir objeto plan vinculado a la mision
    plan_title = validated_template["title"]
    if not plan_title.startswith("[SIMULADA]"):
        plan_title = f"[SIMULADA] {plan_title}"

    plan = {
        "simulation_status": "SIMULADA",
        "mission_id": mission_id,
        "brief_version": 1,
        "plan_version": 1,
        "title": plan_title,
        "tasks": copy.deepcopy(validated_template["tasks"]),
        "risks": copy.deepcopy(validated_template["risks"]),
    }
    envelope["plan"] = plan

    # 7. Transicion MT-004 hacia PLAN_EN_REVISION
    mission["current_state"] = "PLAN_EN_REVISION"
    mission["record_version"] = 3
    mission["updated_at"] = now_iso
    mission_validator.validate(mission)

    plan_review_event = make_event(
        event_id=gen_id("EVT-PLAN-REVIEW"),
        mission_id=mission_id,
        actor="chief_of_staff_simulado",
        actor_role=SIMULATED_ACTOR_ROLE,
        action="presentacion_de_plan",
        timestamp=now_iso,
        version=3,
        previous_state="LISTA_PARA_PLAN",
        new_state="PLAN_EN_REVISION",
        result_summary="Plan SIMULADA presentado para revision. No aprobado y no ejecutado.",
        idempotency_key=gen_id("IDEMP-PLAN-REVIEW"),
    )
    event_validator.validate(plan_review_event)
    envelope["events"].append(plan_review_event)

    envelope["mission"] = mission
    envelope["next_action"] = "Plan SIMULADA presentado para revision. No aprobado y no ejecutado."

    return 0, envelope


def main() -> int:
    """Punto de entrada CLI para el modulo demo_intake."""
    exit_code, envelope = run_demo_intake()
    # JSON ASCII tambien representa Unicode valido sin depender de la consola.
    sys.stdout.write(json.dumps(envelope, indent=2, ensure_ascii=True, allow_nan=False) + "\n")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
