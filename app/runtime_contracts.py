"""PZ-003C: contratos complementarios, sin ejecucion ni almacenamiento.

Interfaces: validate_task/agent_result/evidence/vbp_assembly(data, context=...)
validan estructura e integridad contra registros suministrados en memoria. Sin
contexto devuelven NOT_FOUND; validate_structure(kind, data) SOLO prueba estructura,
limites intrinsecos y huella, nunca existencia de referencias ni autoridad real.

Contexto cerrado: mission (schema nuclear) y listas tasks, evidence, approvals,
inputs, decisions, claims, artifacts (omitidas equivalen a listas vacias).
Las ultimas cuatro listas son descriptores de referencias, no contenido inventado:
ref_id, mission_id, mission_version; decisions agrega approval_ref. Se comprueba
existencia en estas listas, pertenencia y version exacta, no existencia fisica de
archivos, verdad de fuentes ni autenticacion. Una ausencia nunca se da por valida.

Huellas: JSON con sort_keys=True, separators=(',', ':'), ensure_ascii=True,
allow_nan=False, codificado UTF-8; SHA-256 hexadecimal minusculo precedido por
sha256:. No se ordenan arrays ni se normalizan textos. Evidence y agent-result
cubren TODOS los campos excepto fingerprint. VBP cubre TODOS excepto fingerprint,
approval_status y human_approval_ref: estos dos ultimos son metadatos de decision
validados contra approval nuclear y no contenido sometido. Esto evita el ciclo
VBP -> approval -> fingerprint del VBP. Identidad, versiones y las 18 secciones
permanecen en el dominio; no se genera un segundo VBP publico JSON.

Compatibilidad: schemas 1.0.0 / contrato rector 1.2-aprobada. Las firmas semanticas
fijan esta correccion aun no aceptada; overrides deben coincidir. No se permite
reemplazar contratos por schemas vacios. Los $ref se resuelven SOLO con un registro
local precargado; una referencia desconocida se rechaza sin intentar red.
"""

import copy
import hashlib
import json
import math
from collections import deque
from datetime import datetime
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
    from referencing import Registry, Resource
    from referencing.exceptions import Unresolvable
except ImportError:
    Draft202012Validator = None

import app.demo_intake as demo_intake

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTRACTS_RUNTIME_DIR = PROJECT_ROOT / "contracts" / "runtime"
DIALECT = "https://json-schema.org/draft/2020-12/schema"
KINDS = ("task", "agent-result", "evidence", "vbp")
SCHEMA_DIGESTS = (
    "fbcda50d2646f3e5a6bb5f96b1d60622f7f39e0fcaf72132de5b686f672d2fc3",
    "48e8777b55e6285a2977bbf3ebc9a5391929abd88378f3d7c8ea1c68a12c192a",
    "a7d59e662259910e27cf4ec09f2aa9fd1bbd8c1138a375d11d385e7d21be2e5c",
    "2d99eb72757007585410e036c9215abb20403ad2c7d4f016a9b0e390973e8f54",
)
VBP_SECTION_NAMES = [
    "Mision", "Problema y oportunidad", "Usuario objetivo", "Propuesta de valor",
    "Evidencia", "Supuestos", "Alcance incluido", "Alcance excluido",
    "Requisitos funcionales", "Requisitos no funcionales", "Recorrido principal",
    "Fases, tareas y dependencias", "Riesgos, mitigaciones y disparadores",
    "Metricas", "Decisiones tomadas", "Decisiones pendientes", "Aprobaciones",
    "Historial de trazabilidad",
]
MISSION_LIMITS = {
    "max_clarification_cycles": 3, "max_task_reasoning_attempts": 2,
    "max_transient_retries": 1, "max_vbp_correction_rounds": 2,
    "max_concurrent_missions": 1, "max_concurrent_agents": 1,
    "max_recursive_decomposition": 0, "max_agent_execution_seconds": 300,
    "max_mission_seconds": 1200, "max_agent_requests_per_mission": 15,
    "max_budget_usd": 25,
}


class ContractError(Exception):
    """Error tipado propio; nunca incorpora datos rechazados ni excepciones crudas."""

    def __init__(self, code, message):
        super().__init__(message)
        self.payload = demo_intake.make_error_payload(code, message)


def require(condition, message, code="INVALID_INPUT"):
    if not condition:
        raise ContractError(code, message)


def _json_value(data):
    """Comprueba JSON estricto y finito antes de schemas, sets o serializacion.

    Recorrido iterativo: detecta ciclos sin recursion ni coercion de tipos.
    """
    active = set()
    stack = [(data, False)]
    while stack:
        value, leaving = stack.pop()
        if leaving:
            active.remove(id(value))
        elif type(value) in (dict, list):
            require(id(value) not in active, "Entrada JSON ciclica no permitida.")
            active.add(id(value))
            stack.append((value, True))
            if type(value) is dict:
                require(all(type(k) is str for k in value), "Las claves JSON deben ser textuales.")
                stack.extend((v, False) for v in value.values())
            else:
                stack.extend((v, False) for v in value)
        else:
            require(value is None or type(value) in (str, bool, int, float), "Tipo no compatible con JSON.")
            if type(value) is float:
                require(math.isfinite(value), "Numero no finito no permitido.")


def canonical_json_dumps(data):
    _json_value(data)
    try:
        return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
    except (ValueError, RecursionError):
        raise ContractError("INVALID_INPUT", "JSON fuera de la capacidad de serializacion segura.") from None


def _fingerprint(data, excluded):
    require(type(data) is dict, "La huella requiere un objeto JSON.")
    _json_value(data)
    return "sha256:" + hashlib.sha256(canonical_json_dumps(
        {k: v for k, v in data.items() if k not in excluded}).encode("utf-8")).hexdigest()


def compute_evidence_fingerprint(data):
    return _fingerprint(data, {"fingerprint"})


def compute_agent_result_fingerprint(data):
    return _fingerprint(data, {"fingerprint"})


def compute_vbp_manifest_fingerprint(data):
    return _fingerprint(data, {"fingerprint", "approval_status", "human_approval_ref"})


def _load(path):
    try:
        with open(path, "r", encoding="utf-8") as stream:
            return json.load(stream)
    except FileNotFoundError:
        raise ContractError("NOT_FOUND", "Archivo de contrato local ausente.") from None
    except (OSError, UnicodeError, ValueError, RecursionError):
        raise ContractError("SYSTEM_ERROR", "No se pudo leer el contrato local.") from None


def load_runtime_contracts():
    return tuple(_load(CONTRACTS_RUNTIME_DIR / (kind + ".schema.json")) for kind in KINDS)


class RuntimeContractsValidator:
    """Fachada sin efectos; devuelve (valido, errores nucleares) y no altera datos."""

    def __init__(self, schemas_override=None):
        self._startup_error = None
        try:
            require(Draft202012Validator is not None and demo_intake.Draft202012Validator is not None,
                    "Dependencia de validacion no disponible.", "SYSTEM_ERROR")
            schemas = load_runtime_contracts() if schemas_override is None else schemas_override
            require(type(schemas) in (list, tuple) and len(schemas) == 4,
                    "Se requieren los cuatro contratos compatibles.", "SYSTEM_ERROR")
            self._schemas = copy.deepcopy(list(schemas))
            for schema, expected, kind in zip(self._schemas, SCHEMA_DIGESTS, KINDS):
                self._compatible(schema, expected, kind)
            core = PROJECT_ROOT / "contracts" / "core"
            self._core = {kind: _load(core / (kind + ".schema.json")) for kind in ("mission", "approval", "error")}
            for kind, schema in self._core.items():
                require(type(schema) is dict and schema.get("$schema") == DIALECT and
                        schema.get("$id") == f"https://ominai.dev/contracts/core/{kind}.schema.json" and
                        schema.get("$defs", {}).get("schema_version", {}).get("const") == "1.0.0" and
                        schema.get("additionalProperties") is False and schema.get("required"),
                        "Contrato nuclear incompatible.", "SYSTEM_ERROR")
                Draft202012Validator.check_schema(schema)
            resources = self._schemas + list(self._core.values())
            registry = Registry().with_resources((s["$id"], Resource.from_contents(s)) for s in resources)
            self.format_checker = demo_intake.get_format_checker()
            self._validators = {kind: Draft202012Validator(schema, format_checker=self.format_checker, registry=registry)
                                for kind, schema in zip(KINDS, self._schemas)}
            self._core_validators = {kind: Draft202012Validator(schema, format_checker=self.format_checker, registry=registry)
                                     for kind, schema in self._core.items()}
            self.task_schema, self.agent_result_schema, self.evidence_schema, self.vbp_schema = self._schemas
            self.task_validator, self.agent_result_validator, self.evidence_validator, self.vbp_validator = (
                self._validators[kind] for kind in KINDS)
        except ContractError as exc:
            self._startup_error = exc.payload
        except (SchemaError, RecursionError):
            self._startup_error = demo_intake.make_error_payload("SYSTEM_ERROR", "Schema local invalido; validacion no disponible.")

    def _compatible(self, schema, expected, kind, *, metavalidate=True):
        try:
            _json_value(schema)
            require(type(schema) is dict and schema.get("$schema") == DIALECT,
                    "Dialecto de contrato incompatible.", "SYSTEM_ERROR")
            if metavalidate:
                Draft202012Validator.check_schema(schema)
            require(hashlib.sha256(canonical_json_dumps(schema).encode()).hexdigest() == expected,
                    "Contrato incompatible con PZ-003C correccion 1; no se valida permisivamente.", "SYSTEM_ERROR")
        except ContractError:
            raise ContractError("SYSTEM_ERROR", "Contrato incompatible con PZ-003C correccion 1.") from None

    def _check_schema(self, validator, data, label):
        _json_value(data)
        try:
            error = next(validator.iter_errors(data), None)
        except Unresolvable:
            raise ContractError("SYSTEM_ERROR", "Referencia de schema no disponible en registro local.") from None
        except RecursionError:
            raise ContractError("INVALID_INPUT", "Entrada demasiado anidada para validar con seguridad.") from None
        if error is not None:
            # Ruta del SCHEMA, no ruta/valor de la instancia ni error.message.
            path = "/".join(str(p) for p in error.absolute_schema_path)
            if error.validator == "required" and type(error.instance) is dict:
                missing = [key for key in error.validator_value if key not in error.instance]
                path += " (campos requeridos: " + ", ".join(missing) + ")"
            raise ContractError("INVALID_INPUT", f"{label}: incumple regla de schema {path}.")

    def _structure(self, kind, data):
        require(kind in KINDS, "Tipo de contrato no admitido.")
        self._check_schema(self._validators[kind], data, kind)
        if kind == "task":
            require(data["attempt"] <= data["limits"]["max_attempts"], "attempt supera max_attempts.")
            require(data["task_id"] not in data["dependencies"], "La tarea tiene una autodependencia.")
        elif kind == "vbp":
            sections = data["sections"]
            require({s["section_number"] for s in sections} == set(range(1, 19)), "Seccion obligatoria ausente o duplicada.")
            require(all(data["functional_leads"][s["section_name"]] == s["responsible_role"] for s in sections),
                    "Responsable de seccion no corresponde al manifest.")
        compute = {"agent-result": compute_agent_result_fingerprint, "evidence": compute_evidence_fingerprint,
                   "vbp": compute_vbp_manifest_fingerprint}.get(kind)
        if compute:
            require(data["fingerprint"] == compute(data), "La huella no coincide con el contenido.")

    def _boundary(self, operation):
        if self._startup_error is not None:
            return False, [copy.deepcopy(self._startup_error)]
        try:
            for schema, expected, kind in zip(self._schemas, SCHEMA_DIGESTS, KINDS):
                self._compatible(schema, expected, kind, metavalidate=False)
            operation()
            return True, []
        except ContractError as exc:
            return False, [copy.deepcopy(exc.payload)]
        except (SchemaError, RecursionError):
            return False, [demo_intake.make_error_payload("SYSTEM_ERROR", "Schema incompatible durante validacion.")]

    def validate_structure(self, kind, data):
        """SOLO estructura/huella: no afirma integridad referencial ni aprueba."""
        return self._boundary(lambda: self._structure(kind, data))

    def _index(self, rows, key):
        require(type(rows) is list, "El conjunto de registros debe ser una lista.")
        index = {}
        for row in rows:
            require(type(row) is dict and type(row.get(key)) is str and row[key].strip(),
                    "Registro de contexto sin identificador valido.")
            require(row[key] not in index, "Identificador de contexto duplicado.")
            index[row[key]] = row
        return index

    def _context(self, context, data):
        require(context is not None, "Falta contexto; integridad referencial no verificada.", "NOT_FOUND")
        _json_value(context)
        groups = ("tasks", "evidence", "approvals", "inputs", "decisions", "claims", "artifacts")
        require(type(context) is dict and set(context) <= {"mission", *groups}, "Campos de contexto no admitidos.")
        require("mission" in context, "Mision contextual ausente.", "NOT_FOUND")
        mission = context["mission"]
        self._check_schema(self._core_validators["mission"], mission, "mission")
        require(data["mission_id"] == mission["mission_id"], "Registro de otra mision.", "PERMISSION_DENIED")
        require(data["mission_version"] == mission["record_version"], "Version de mision incompatible.")
        require(len(mission["approval_refs"]) == len(set(mission["approval_refs"])), "Referencias de aprobacion duplicadas.")
        for field, maximum in MISSION_LIMITS.items():
            require(mission["limits"][field] <= maximum, "Limite contextual supera contrato rector.")
        for counter, limit in (("clarification_cycles", "max_clarification_cycles"),
                               ("task_reasoning_attempts", "max_task_reasoning_attempts"),
                               ("transient_retries", "max_transient_retries"),
                               ("vbp_correction_rounds", "max_vbp_correction_rounds"),
                               ("agent_requests", "max_agent_requests_per_mission")):
            require(mission["counters"][counter] <= mission["limits"][limit], "Contador contextual supera su limite.")
        indexes = {}
        for group in groups:
            key = {"tasks": "task_id", "evidence": "evidence_id", "approvals": "approval_id"}.get(group, "ref_id")
            indexes[group] = self._index(context.get(group, []), key)
            for row in indexes[group].values():
                if group == "approvals":
                    self._check_schema(self._core_validators["approval"], row, "approval")
                    require(row["user_id"] == mission["user_id"], "Aprobacion de otro propietario.", "PERMISSION_DENIED")
                    continue
                if group in ("tasks", "evidence"):
                    self._structure("task" if group == "tasks" else "evidence", row)
                else:
                    keys = {"ref_id", "mission_id", "mission_version"}
                    if group == "decisions":
                        keys.add("approval_ref")
                    require(set(row) == keys, "Descriptor de referencia con campos incompatibles.")
                    require(type(row["mission_version"]) is int and row["mission_version"] >= 1,
                            "Version de descriptor invalida.")
                    require(all(type(row[k]) is str and row[k].strip() for k in keys - {"mission_version"}),
                            "Identidad de descriptor invalida.")
                require(row["mission_id"] == mission["mission_id"], "Referencia de otra mision.", "PERMISSION_DENIED")
                require(row["mission_version"] == mission["record_version"], "Referencia de version obsoleta.")
        for ref in mission["approval_refs"]:
            self._resolve(indexes, "approvals", ref)
        for evidence in indexes["evidence"].values():
            self._resolve(indexes, "claims", evidence["claim_id"])
            self._resolve(indexes, "inputs", evidence["source_locator"])
        # No se afirma RI-002 de checkpoint: este contexto no valida reanudacion.
        self._graph(indexes["tasks"])
        return mission, indexes

    def _resolve(self, indexes, group, ref):
        require(ref in indexes[group], f"Referencia ausente en {group}.", "NOT_FOUND")
        return indexes[group][ref]

    def _graph(self, tasks):
        indegree = {key: 0 for key in tasks}
        children = {key: [] for key in tasks}
        for key, row in tasks.items():
            for dependency in row["dependencies"]:
                require(dependency in tasks, "Dependencia inexistente.", "NOT_FOUND")
                children[dependency].append(key)
                indegree[key] += 1
        ready = deque(key for key, degree in indegree.items() if degree == 0)
        visited = 0
        while ready:
            key = ready.popleft()
            visited += 1
            for child in children[key]:
                indegree[child] -= 1
                if indegree[child] == 0:
                    ready.append(child)
        require(visited == len(tasks), "Ciclo de dependencias detectado.")

    def _decision_refs(self, refs, mission, indexes):
        for ref in refs:
            decision = self._resolve(indexes, "decisions", ref)
            approval = self._resolve(indexes, "approvals", decision["approval_ref"])
            require(approval["approval_id"] in mission["approval_refs"] and approval["status"] == "CONSUMIDA" and
                    approval["decision"] in ("APROBAR", "APROBAR_CON_EXCEPCION"),
                    "Decision sin aprobacion humana vinculada.", "PERMISSION_DENIED")

    def _task_context(self, task, mission, indexes):
        require(self._resolve(indexes, "tasks", task["task_id"]) == task, "Tarea distinta del registro contextual.")
        require(task["authorized_context"]["brief_version"] == mission["brief_version"], "Version de brief incompatible.")
        if "schema_ref" in task["expected_output"]:
            known = {schema["$id"] for schema in self._schemas + list(self._core.values())}
            require(task["expected_output"]["schema_ref"] in known,
                    "Schema de salida no disponible en registro local.", "NOT_FOUND")
        for field, limit in (("max_attempts", "max_task_reasoning_attempts"), ("max_seconds", "max_agent_execution_seconds"),
                             ("max_budget_usd", "max_budget_usd")):
            require(task["limits"][field] <= mission["limits"][limit], "Limite de tarea supera el autorizado en la mision.")
        for group, refs in (("inputs", task["authorized_context"]["input_refs"]),
                            ("evidence", task["authorized_context"]["evidence_refs"])):
            for ref in refs:
                self._resolve(indexes, group, ref)
        self._decision_refs(task["approved_decisions"], mission, indexes)

    def _validate(self, kind, data, context):
        self._structure(kind, data)
        mission, indexes = self._context(context, data)
        for task in indexes["tasks"].values():
            self._task_context(task, mission, indexes)
        if kind == "task":
            self._task_context(data, mission, indexes)
        elif kind == "evidence":
            existing = indexes["evidence"].get(data["evidence_id"])
            require(existing is None or existing == data, "Evidencia distinta del registro contextual.")
            self._resolve(indexes, "claims", data["claim_id"])
            self._resolve(indexes, "inputs", data["source_locator"])
        elif kind == "agent-result":
            task = self._resolve(indexes, "tasks", data["task_id"])
            require(data["agent_role"] == task["agent_role"], "Resultado de otro agente.", "PERMISSION_DENIED")
            require(data["attempt_count"] == task["attempt"] and data["attempt_count"] <= task["limits"]["max_attempts"],
                    "attempt_count incompatible con la tarea.")
            require(set(data["approved_decisions_used"]) <= set(task["approved_decisions"]), "Decision ajena al contexto autorizado.", "PERMISSION_DENIED")
            self._decision_refs(data["approved_decisions_used"], mission, indexes)
            for group, refs in (("evidence", data["evidence_refs"]), ("artifacts", data["artifacts"])):
                for ref in refs:
                    self._resolve(indexes, group, ref)
        else:
            for ref in data["included_components"]:
                self._resolve(indexes, "artifacts", ref)
            if data["human_approval_ref"] is not None:
                approval = self._resolve(indexes, "approvals", data["human_approval_ref"])
                expected = {"APROBADO": "APROBAR", "APROBADO_CON_EXCEPCION": "APROBAR_CON_EXCEPCION", "RECHAZADO": "RECHAZAR"}
                require(approval["approval_id"] in mission["approval_refs"] and approval["status"] == "CONSUMIDA" and
                        approval["decision"] == expected[data["approval_status"]], "Estado de aprobacion incompatible.", "PERMISSION_DENIED")
                require(approval["version_or_fingerprint"] == data["fingerprint"] and
                        approval["action_approved"] == f"Aprobacion del VBP {data['vbp_id']} v{data['version']} de la mision {data['mission_id']}",
                        "Aprobacion no corresponde al VBP y version exactos.", "PERMISSION_DENIED")
                if data["approval_status"] == "APROBADO_CON_EXCEPCION":
                    require(bool(approval["comment"].strip()), "La excepcion requiere motivo humano.", "PERMISSION_DENIED")
                require(datetime.fromisoformat(approval["timestamp"]) >= datetime.fromisoformat(data["created_at"]),
                        "Decision anterior al contenido del VBP.")
                if approval["expiration"] is not None:
                    require(datetime.fromisoformat(approval["timestamp"]) < datetime.fromisoformat(approval["expiration"]),
                            "Decision fuera de la vigencia de la solicitud.", "PERMISSION_DENIED")

    def validate_task(self, data, *, context=None):
        return self._boundary(lambda: self._validate("task", data, context))

    def validate_agent_result(self, data, *, context=None):
        return self._boundary(lambda: self._validate("agent-result", data, context))

    def validate_evidence(self, data, *, context=None):
        return self._boundary(lambda: self._validate("evidence", data, context))

    def validate_vbp_assembly(self, data, *, context=None):
        return self._boundary(lambda: self._validate("vbp", data, context))
