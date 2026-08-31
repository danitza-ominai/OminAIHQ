"""Suite de pruebas y regresion para los contratos nucleares (PZ-001A).

Verifica sintaxis, metavalidacion, ejemplos positivos, casos negativos,
maquina de estados, integridad referencial, ciclo de vida de aprobaciones,
idempotencia, matriz exhaustiva de errores, rechazo de Chain-of-Thought
y ausencia de terminos prohibidos.
"""

import json
import copy
import pathlib
import re
import unittest
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Set, Tuple

import jsonschema
from jsonschema import Draft202012Validator

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
CONTRACTS_DIR = ROOT_DIR / "contracts" / "core"
EXAMPLES_DIR = CONTRACTS_DIR / "examples"

FORBIDDEN_FIELDS = [
    "chain_of_thought",
    "scratchpad",
    "internal_reasoning",
    "reasoning_trace",
]

FORBIDDEN_TERMS = [
    "OminAI Business OS",
    "OminaiTech Engine",
    "Firestore",
    "Cloud Run",
    "Cloud Storage",
    "BigQuery",
    "AlloyDB",
    "Vertex AI Memory Bank",
    "ADK Web",
]

FORBIDDEN_WHOLE_WORD_TERMS = [
    "UI",
    "Gemini",
    "Claude",
    "OpenAI",
    "Anthropic",
    "Vertex",
]

EXPECTED_10_ERROR_COMBINATIONS = {
    ("INVALID_INPUT", False, 0, 0, "solicitar_correccion"),
    ("NOT_FOUND", False, 0, 0, "solicitar_verificacion_o_fuente_alternativa"),
    ("PERMISSION_DENIED", False, 0, 0, "detener_y_escalar"),
    ("TRANSIENT_FAILURE", True, 1, 0, "reintentar_una_vez"),
    ("TRANSIENT_FAILURE", False, 1, 1, "guardar_checkpoint_y_bloquear"),
    ("SCHEMA_INVALID", True, 1, 0, "solicitar_una_regeneracion"),
    ("SCHEMA_INVALID", False, 1, 1, "bloquear_mision"),
    ("DEPENDENCY_FAILED", False, 0, 0, "bloquear_tareas_descendientes_y_notificar"),
    ("BUDGET_EXHAUSTED", False, 0, 0, "pausar_y_pedir_decision_humana"),
    ("SYSTEM_ERROR", False, 0, 0, "conservar_diagnostico_y_checkpoint"),
}

RFC3339_DATE_TIME_PATTERN = re.compile(
    r"^[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])"
    r"T(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]"
    r"(?:\.[0-9]+)?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])$"
)


def is_rfc3339_date_time(value: Any) -> bool:
    """Valida date-time RFC 3339 sin dependencias opcionales externas."""
    if not isinstance(value, str):
        return True
    if RFC3339_DATE_TIME_PATTERN.fullmatch(value) is None:
        return False
    normalized = f"{value[:-1]}+00:00" if value.endswith("Z") else value
    datetime.fromisoformat(normalized)
    return True


FORMAT_CHECKER = jsonschema.FormatChecker()
FORMAT_CHECKER.checks("date-time", raises=ValueError)(is_rfc3339_date_time)


def load_json(path: pathlib.Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class TestContractsCore(unittest.TestCase):
    """Regresion automatica de los contratos nucleares."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.schema_files = {
            "mission": CONTRACTS_DIR / "mission.schema.json",
            "event": CONTRACTS_DIR / "event.schema.json",
            "approval": CONTRACTS_DIR / "approval.schema.json",
            "checkpoint": CONTRACTS_DIR / "checkpoint.schema.json",
            "error": CONTRACTS_DIR / "error.schema.json",
        }
        cls.schemas: Dict[str, Dict[str, Any]] = {
            k: load_json(p) for k, p in cls.schema_files.items()
        }
        cls.validators: Dict[str, Draft202012Validator] = {
            k: Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
            for k, schema in cls.schemas.items()
        }
        cls.state_machine = load_json(CONTRACTS_DIR / "state-machine.json")

    def test_01_json_files_count_and_parsing(self) -> None:
        """Verifica que existan exactamente 12 archivos JSON y 1 README en contracts/core y que todos parseen."""
        all_files = list(CONTRACTS_DIR.rglob("*"))
        json_files = [p for p in all_files if p.is_file() and p.suffix == ".json"]
        self.assertEqual(len(json_files), 12)

        readme_file = CONTRACTS_DIR / "README.md"
        self.assertTrue(readme_file.exists())
        self.assertEqual(len([p for p in all_files if p.is_file()]), 13)

        for jf in json_files:
            try:
                data = load_json(jf)
                self.assertIsNotNone(data)
            except Exception as e:
                self.fail(f"Fallo al parsear {jf}: {e}")

    def test_02_schemas_metadata_and_metavalidation(self) -> None:
        """Verifica que los 5 schemas declaran Draft 2020-12, $id, title, version y pasan metavalidacion."""
        for name, schema in self.schemas.items():
            self.assertEqual(
                schema.get("$schema"),
                "https://json-schema.org/draft/2020-12/schema",
                f"{name} no declara Draft 2020-12",
            )
            self.assertTrue(
                schema.get("$id", "").startswith("https://ominai.dev/contracts/core/"),
                f"{name} tiene $id invalido",
            )
            self.assertTrue(len(schema.get("title", "")) > 0, f"{name} no tiene title")
            self.assertEqual(
                schema["$defs"]["schema_version"]["const"],
                "1.0.0",
                f"{name} no exige schema_version 1.0.0",
            )

            # Metavalidacion formal
            try:
                Draft202012Validator.check_schema(schema)
            except Exception as e:
                self.fail(f"Metavalidacion fallo para schema {name}: {e}")

        format_probe = dict(
            load_json(EXAMPLES_DIR / "approval.valid.json")["test_cases"][0][
                "test_data"
            ]
        )
        format_probe["timestamp"] = "fecha-no-iso-8601"
        format_errors = list(self.validators["approval"].iter_errors(format_probe))
        self.assertTrue(
            any(error.validator == "format" for error in format_errors),
            "FormatChecker no rechazo un date-time invalido",
        )

    def test_03_positive_examples_validation(self) -> None:
        """Verifica que todos los ejemplos positivos sean aceptados por sus respectivos schemas y reglas."""
        # 1. Mission valid
        mission_valid_doc = load_json(EXAMPLES_DIR / "mission.valid.json")
        mission_data = mission_valid_doc["test_data"]
        errors = list(self.validators["mission"].iter_errors(mission_data))
        self.assertEqual(len(errors), 0, f"mission.valid.json fallo: {errors}")

        # 2. Approval valid (todos los casos)
        approval_valid_doc = load_json(EXAMPLES_DIR / "approval.valid.json")
        for case in approval_valid_doc["test_cases"]:
            case_id = case["id"]
            app_data = case["test_data"]
            errors = list(self.validators["approval"].iter_errors(app_data))
            self.assertEqual(
                len(errors), 0, f"approval.valid.json caso {case_id} fallo: {errors}"
            )

        # 3. Transitions valid
        trans_valid_doc = load_json(EXAMPLES_DIR / "transitions.valid.json")
        t_data = trans_valid_doc["test_data"]
        matched = [
            t
            for t in self.state_machine["mission_transitions"]
            if t["id"] == t_data["transition_id"]
            and t["from"] == t_data["from"]
            and t["to"] == t_data["to"]
        ]
        self.assertEqual(len(matched), 1)

    def test_04_negative_examples_mission_and_checkpoint_rejected(self) -> None:
        """Verifica que todos los casos de mission.invalid.json sean rechazados por sus schemas."""
        mission_invalid_doc = load_json(EXAMPLES_DIR / "mission.invalid.json")
        for case in mission_invalid_doc["test_cases"]:
            case_id = case["id"]
            schema_name = case["schema"]
            data = case["test_data"]
            validator = self.validators[schema_name]
            errors = list(validator.iter_errors(data))
            self.assertGreater(
                len(errors),
                0,
                f"Caso invalido {case_id} no fue rechazado por schema {schema_name}",
            )

    def test_05_negative_examples_approval_rejected(self) -> None:
        """Verifica que todos los casos de approval.invalid.json sean rechazados por approval.schema.json."""
        approval_invalid_doc = load_json(EXAMPLES_DIR / "approval.invalid.json")
        for case in approval_invalid_doc["test_cases"]:
            case_id = case["id"]
            data = case["test_data"]
            errors = list(self.validators["approval"].iter_errors(data))
            self.assertGreater(
                len(errors),
                0,
                f"Caso invalido {case_id} no fue rechazado por approval.schema.json",
            )

    def test_06_negative_examples_transitions_rejected(self) -> None:
        """Verifica que los casos negativos de transitions.invalid.json sean rechazados segun su tipo."""
        trans_inv_doc = load_json(EXAMPLES_DIR / "transitions.invalid.json")
        for case in trans_inv_doc["test_cases"]:
            case_id = case["id"]
            test_type = case["test_type"]
            rejected = False

            if test_type == "transition":
                from_st = case["from"]
                to_st = case["to"]
                is_human = case["is_human_actor"]
                # Buscar transiciones validas que coincidan
                matching = [
                    t
                    for t in self.state_machine["mission_transitions"]
                    if t["from"] == from_st and t["to"] == to_st
                ]
                rejected = not matching or all(
                    not is_human
                    and (
                        transition.get("requires_human_approval", False)
                        or transition.get("authority") == "solo_usuario_humano"
                    )
                    for transition in matching
                )

            elif test_type == "error_schema":
                data = case["test_data"]
                errors = list(self.validators["error"].iter_errors(data))
                rejected = bool(errors)

            elif test_type == "approval_lifecycle":
                setup_status = case["setup"]["existing_record"]["status"]
                # Ciclo de vida: CONSUMIDA y EXPIRADA son terminales y no admiten segunda decision ni transicion
                lifecycle = self.state_machine["approval_lifecycle"]
                rejected = (
                    setup_status in lifecycle["states"]
                    and lifecycle["states"][setup_status]["terminal"]
                    and not any(
                        transition["from"] == setup_status
                        for transition in lifecycle["transitions"]
                    )
                )

            elif test_type == "referential_integrity":
                # Verificacion de regla de integridad referencial
                known_appr = set(case["setup"]["known_approvals"])
                known_cp = set(case["setup"]["known_checkpoints"])
                m = case["mission_under_test"]
                missing_appr = [
                    ref for ref in m.get("approval_refs", []) if ref not in known_appr
                ]
                missing_cp = (
                    m.get("last_checkpoint_id")
                    if m.get("last_checkpoint_id") not in known_cp
                    else None
                )
                rejected = bool(missing_appr or missing_cp)

            elif test_type == "idempotency":
                existing = case["setup"]["existing_record"]
                attempted = case["attempted_record"]
                rejected = (
                    existing["idempotency_key"] == attempted["idempotency_key"]
                    and existing != attempted
                )

            else:
                self.fail(f"Caso {case_id} tiene test_type desconocido: {test_type}")

            self.assertTrue(
                rejected,
                f"Caso negativo {case_id} termino sin un rechazo explicito",
            )

    def test_07_state_machine_counts(self) -> None:
        """Verifica conteo exacto de 15 estados de mision, 8 de tarea, 76 transiciones de mision y 13 de tarea."""
        sm = self.state_machine
        mission_states = sm["mission_states"]
        self.assertEqual(len(mission_states), 15)
        self.assertEqual(len(sm["non_terminal_mission_states"]), 13)
        self.assertEqual(len(sm["terminal_mission_states"]), 2)
        self.assertEqual(len(sm["mission_transitions"]), 76)

        task_states = sm["task_states"]
        self.assertEqual(len(task_states), 8)
        self.assertEqual(len(sm["non_terminal_task_states"]), 4)
        self.assertEqual(len(sm["terminal_task_states"]), 4)
        self.assertEqual(len(sm["task_transitions"]), 13)

    def test_08_table_4_2_representation_and_terminal_invariants(self) -> None:
        """Verifica que las 16 filas de 4.2 estan representadas y los terminales no tienen transiciones salientes."""
        transitions = self.state_machine["mission_transitions"]

        # Terminales de mision no tienen salidas
        for t in transitions:
            self.assertNotIn(
                t["from"],
                ["FINALIZADA", "CANCELADA"],
                f"Estado terminal {t['from']} no puede tener transicion de salida",
            )

        # Terminales de tarea no tienen salidas
        task_transitions = self.state_machine["task_transitions"]
        for tt in task_transitions:
            self.assertNotIn(
                tt["from"],
                ["COMPLETA", "PARCIAL", "FALLIDA", "CANCELADA"],
                f"Estado terminal de tarea {tt['from']} no puede tener transicion de salida",
            )

        row_counts: Counter[int] = Counter()
        row_pattern = re.compile(r"4\.2 fila ([0-9]+)")
        for transition in transitions:
            contract_ref = transition.get("contract_ref", "")
            row_matches = row_pattern.findall(contract_ref)
            self.assertEqual(
                len(row_matches),
                1,
                f"Referencia 4.2 invalida o ambigua: {contract_ref!r}",
            )
            row_counts[int(row_matches[0])] += 1

        expected_row_counts = {
            1: 1,
            2: 4,
            3: 1,
            4: 1,
            5: 1,
            6: 12,
            7: 12,
            8: 24,
            9: 1,
            10: 1,
            11: 1,
            12: 1,
            13: 1,
            14: 1,
            15: 1,
            16: 13,
        }
        self.assertEqual(set(row_counts), set(range(1, 17)))
        self.assertEqual(dict(row_counts), expected_row_counts)

    def test_09_reserved_routes_and_human_evidence(self) -> None:
        """Verifica que rutas directas reservadas exigen solo_usuario_humano o accion determinista."""
        sm = self.state_machine
        never_model = set(sm["never_by_model_inference"])
        self.assertEqual(
            never_model,
            {"AUTORIZADA_PARA_EJECUTAR", "VBP_APROBADO", "FINALIZADA", "CANCELADA"},
        )

        transitions_by_id = {t["id"]: t for t in sm["mission_transitions"]}

        # MT-005 (PLAN_EN_REVISION -> AUTORIZADA_PARA_EJECUTAR)
        t_005 = transitions_by_id["MT-005"]
        self.assertEqual(t_005["authority"], "solo_usuario_humano")
        self.assertTrue(t_005["requires_human_approval"])

        # MT-012 (VBP_EN_REVISION -> VBP_APROBADO)
        t_012 = transitions_by_id["MT-012"]
        self.assertEqual(t_012["authority"], "solo_usuario_humano")
        self.assertTrue(t_012["requires_human_approval"])

        # MT-010 (VBP_EN_REVISION -> VBP_RECHAZADO)
        t_010 = transitions_by_id["MT-010"]
        self.assertEqual(t_010["authority"], "solo_usuario_humano")
        self.assertTrue(t_010["requires_human_approval"])

        # MT-011 (VBP_RECHAZADO -> EN_CONSOLIDACION)
        t_011 = transitions_by_id["MT-011"]
        self.assertEqual(t_011["authority"], "solo_usuario_humano")
        self.assertTrue(t_011["requires_human_approval"])

        # MT-013 (VBP_APROBADO -> FINALIZADA)
        t_013 = transitions_by_id["MT-013"]
        self.assertEqual(t_013["authority"], "accion_determinista")
        self.assertEqual(t_013["from"], "VBP_APROBADO")
        self.assertEqual(t_013["to"], "FINALIZADA")

        # MT-038 a MT-050 (* -> CANCELADA)
        for i in range(38, 51):
            t_id = f"MT-{i:03d}"
            t_cancel = transitions_by_id[t_id]
            self.assertEqual(t_cancel["authority"], "solo_usuario_humano")
            self.assertTrue(t_cancel["requires_human_approval"])
            self.assertEqual(t_cancel["to"], "CANCELADA")

        # Variantes de supuestos aceptados (MT-002b y MT-003b)
        self.assertTrue(transitions_by_id["MT-002b"].get("human_evidence_required"))
        self.assertTrue(transitions_by_id["MT-003b"].get("human_evidence_required"))

    def test_10_approval_lifecycle_and_idempotency(self) -> None:
        """Verifica el ciclo de vida de aprobaciones e invariantes de idempotencia."""
        al = self.state_machine["approval_lifecycle"]
        self.assertEqual(set(al["states"].keys()), {"PENDIENTE", "CONSUMIDA", "EXPIRADA"})
        self.assertFalse(al["states"]["PENDIENTE"]["terminal"])
        self.assertTrue(al["states"]["CONSUMIDA"]["terminal"])
        self.assertTrue(al["states"]["EXPIRADA"]["terminal"])

        trans_ids = {t["id"]: t for t in al["transitions"]}
        self.assertEqual(set(trans_ids.keys()), {"AT-001", "AT-002"})
        self.assertEqual(trans_ids["AT-001"]["from"], "PENDIENTE")
        self.assertEqual(trans_ids["AT-001"]["to"], "CONSUMIDA")
        self.assertEqual(trans_ids["AT-002"]["from"], "PENDIENTE")
        self.assertEqual(trans_ids["AT-002"]["to"], "EXPIRADA")

        # Reglas de idempotencia
        idem = self.state_machine["idempotency_rules"]
        self.assertEqual(idem["same_key_same_content"]["action"], "no_second_effect")
        self.assertEqual(idem["same_key_different_content"]["action"], "conflict_rejection")
        self.assertEqual(idem["same_key_different_content"]["error_code"], "INVALID_INPUT")

    def test_11_referential_integrity_rules(self) -> None:
        """Verifica la presencia y definicion de RI-001, RI-002 y RI-003."""
        ri_rules = self.state_machine["referential_integrity_rules"]["rules"]
        self.assertEqual(len(ri_rules), 3)
        rule_ids = {r["id"] for r in ri_rules}
        self.assertEqual(rule_ids, {"RI-001", "RI-002", "RI-003"})

        for r in ri_rules:
            self.assertEqual(r["on_missing_non_null"]["error_code"], "NOT_FOUND")

    def test_12_exhaustive_error_matrix_1440_combinations(self) -> None:
        """Verifica exhaustivamente 1440 combinaciones de error y acepta exactamente 10."""
        error_codes = [
            "INVALID_INPUT",
            "NOT_FOUND",
            "PERMISSION_DENIED",
            "TRANSIENT_FAILURE",
            "SCHEMA_INVALID",
            "DEPENDENCY_FAILED",
            "BUDGET_EXHAUSTED",
            "SYSTEM_ERROR",
        ]
        retry_options = [True, False]
        max_retries_options = [0, 1, 2]
        attempt_options = [0, 1, 2]
        required_actions = [
            "solicitar_correccion",
            "solicitar_verificacion_o_fuente_alternativa",
            "detener_y_escalar",
            "reintentar_una_vez",
            "guardar_checkpoint_y_bloquear",
            "solicitar_una_regeneracion",
            "bloquear_mision",
            "bloquear_tareas_descendientes_y_notificar",
            "pausar_y_pedir_decision_humana",
            "conservar_diagnostico_y_checkpoint",
        ]

        total_tested = 0
        accepted_combinations: Set[Tuple[str, bool, int, int, str]] = set()

        validator = self.validators["error"]

        for code in error_codes:
            for retry in retry_options:
                for max_r in max_retries_options:
                    for att in attempt_options:
                        for action in required_actions:
                            total_tested += 1
                            instance = {
                                "schema_version": "1.0.0",
                                "error_code": code,
                                "message": "Test de matriz exhaustiva",
                                "retry_allowed": retry,
                                "max_retries": max_r,
                                "current_attempt": att,
                                "recoverable": True,
                                "required_action": action,
                            }
                            if validator.is_valid(instance):
                                accepted_combinations.add(
                                    (code, retry, max_r, att, action)
                                )

        self.assertEqual(total_tested, 1440)
        self.assertEqual(
            len(accepted_combinations),
            10,
            f"Se esperaban exactamente 10 combinaciones validas, se obtuvieron {len(accepted_combinations)}: {accepted_combinations}",
        )
        self.assertEqual(accepted_combinations, EXPECTED_10_ERROR_COMBINATIONS)

    def test_13_rejection_of_chain_of_thought_fields(self) -> None:
        """Verifica que campos de razonamiento interno / Chain-of-Thought sean rechazados en todos los schemas."""
        mission_base = load_json(EXAMPLES_DIR / "mission.valid.json")["test_data"]
        approval_base = load_json(EXAMPLES_DIR / "approval.valid.json")["test_cases"][0][
            "test_data"
        ]

        for forbidden in FORBIDDEN_FIELDS:
            # Probar en mission
            bad_mission = dict(mission_base)
            bad_mission[forbidden] = "Razonamiento interno prohibido"
            errors = list(self.validators["mission"].iter_errors(bad_mission))
            self.assertGreater(
                len(errors),
                0,
                f"mission.schema.json no rechazo campo prohibido {forbidden}",
            )

            # Probar en approval
            bad_approval = dict(approval_base)
            bad_approval[forbidden] = "Razonamiento interno prohibido"
            errors = list(self.validators["approval"].iter_errors(bad_approval))
            self.assertGreater(
                len(errors),
                0,
                f"approval.schema.json no rechazo campo prohibido {forbidden}",
            )

    def test_event_states_structural_cartesian_matrix(self):
        # Structural validity does NOT grant transition authority.
        from test_human_approvals import fixture
        runtime, repo, ctx, req = fixture()
        self.addCleanup(repo.close)
        event = repo.list_events('MSN-SIM')[0]
        states = set(self.schemas['event']['$defs']['mission_state']['enum']) | set(self.schemas['event']['$defs']['task_state']['enum'])
        self.assertEqual(len(states), 21)
        count = 0
        for previous in [None, *sorted(states)]:
            for new in sorted(states):
                with self.subTest(previous=previous, new=new):
                    value = {**event, 'previous_state': previous, 'new_state': new}
                    self.assertTrue(self.validators['event'].is_valid(value))
                    count += 1
        self.assertEqual(count, 462)
        self.assertFalse(any(t['from']=='CANCELADA' and t['to']=='BORRADOR'
                             for t in self.state_machine['mission_transitions']))
        # Every required field and closed nested object remains enforced.
        for field in self.schemas['event']['required']:
            value = copy.deepcopy(event); del value[field]
            self.assertFalse(self.validators['event'].is_valid(value), field)
        for field in ('previous_state', 'new_state'):
            for bad in ('INVENTADO', '', 0, True, [], {}):
                self.assertFalse(self.validators['event'].is_valid({**event, field: bad}))
        self.assertFalse(self.validators['event'].is_valid({**event, 'new_state': None}))
        self.assertFalse(self.validators['event'].is_valid({**event, 'extra': 1}))
        for field, valid in [('typed_error', {'error_code':'SYSTEM_ERROR','message':'SIMULADA'}),
                             ('budget_consumed', {'dimension':'usd','amount':0})]:
            self.assertTrue(self.validators['event'].is_valid({**event, field:valid}))
            self.assertFalse(self.validators['event'].is_valid({**event, field:{**valid, 'extra':1}}))
            for key in valid:
                bad = dict(valid); del bad[key]
                self.assertFalse(self.validators['event'].is_valid({**event, field:bad}))

    def test_14_absence_of_forbidden_terms_in_contracts_core(self) -> None:
        """Verifica que no aparezcan terminos prohibidos dentro de los trece archivos de contracts/core."""
        all_core_files = list(CONTRACTS_DIR.rglob("*"))
        self.assertEqual(len([f for f in all_core_files if f.is_file()]), 13)

        # Patron para verificar "Omi" como palabra aislada (no como prefijo de Ominai)
        omi_pattern = re.compile(r"\bOmi\b")
        whole_word_patterns = {
            term: re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
            for term in FORBIDDEN_WHOLE_WORD_TERMS
        }

        for file_path in all_core_files:
            if not file_path.is_file():
                continue
            text = file_path.read_text(encoding="utf-8")
            for term in FORBIDDEN_TERMS:
                self.assertNotIn(
                    term,
                    text,
                    f"Termino prohibido '{term}' encontrado en {file_path.relative_to(ROOT_DIR)}",
                )
            self.assertFalse(
                omi_pattern.search(text),
                f"Termino prohibido 'Omi' encontrado como palabra en {file_path.relative_to(ROOT_DIR)}",
            )
            for term, pattern in whole_word_patterns.items():
                self.assertIsNone(
                    pattern.search(text),
                    f"Termino prohibido '{term}' encontrado como palabra en {file_path.relative_to(ROOT_DIR)}",
                )


if __name__ == "__main__":
    unittest.main()
