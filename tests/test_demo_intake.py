"""Pruebas para el modulo app.demo_intake (PZ-003A SIMULADA).

Cubre exhaustivamente los criterios de aceptacion CA-01 a CA-11, validando
el flujo determinista, schemas, maquina de estados, deteccion de faltantes,
rechazos estructurados, aislamiento de memoria y ejecucion CLI.
"""

import copy
import builtins
import importlib.util
import io
import json
import os
import sys
import unittest
from contextlib import ExitStack, contextmanager, redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import jsonschema
from jsonschema import Draft202012Validator

import app.demo_intake as demo_intake

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTRACTS_CORE_DIR = PROJECT_ROOT / "contracts" / "core"
DEFAULT_FIXTURE_PATH = PROJECT_ROOT / "examples" / "demo_mission.json"


class TestDemoIntake(unittest.TestCase):
    """Suite de pruebas para el ensayo determinista de intake PZ-003A."""

    def setUp(self) -> None:
        """Carga la fixture base valida para pruebas dirigidas."""
        with open(DEFAULT_FIXTURE_PATH, "r", encoding="utf-8") as f:
            self.base_fixture = json.load(f)

        self.mission_schema, self.event_schema, self.error_schema, self.state_machine = (
            demo_intake.load_core_contracts()
        )
        self.format_checker = demo_intake.get_format_checker()
        self.mission_validator = Draft202012Validator(
            self.mission_schema, format_checker=self.format_checker
        )
        self.event_validator = Draft202012Validator(
            self.event_schema, format_checker=self.format_checker
        )
        self.error_validator = Draft202012Validator(
            self.error_schema, format_checker=self.format_checker
        )

    def test_ca01_complete_case_flow_and_events(self) -> None:
        """CA-01: Caso completo produce BORRADOR, LISTA_PARA_PLAN y PLAN_EN_REVISION en orden con 3 eventos."""
        fixed_dt = datetime(2026, 8, 30, 12, 0, 0, tzinfo=timezone.utc)
        seq = 0

        def deterministic_id(prefix: str) -> str:
            nonlocal seq
            seq += 1
            return f"{prefix}-{seq:03d}"

        exit_code, envelope = demo_intake.run_demo_intake(
            raw_data=self.base_fixture,
            now_fn=lambda: fixed_dt,
            id_generator=deterministic_id,
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(envelope["simulation_status"], "SIMULADA")
        self.assertEqual(envelope["pending_fields"], [])
        self.assertEqual(envelope["errors"], [])
        self.assertIn("Plan SIMULADA presentado para revision", envelope["next_action"])

        # Mision
        mission = envelope["mission"]
        self.assertIsNotNone(mission)
        self.assertEqual(mission["current_state"], "PLAN_EN_REVISION")
        self.assertEqual(mission["record_version"], 3)
        self.assertEqual(mission["approval_refs"], [])
        self.assertIsNone(mission["active_task"])
        self.assertIsNone(mission["resumable_state"])
        self.assertIsNone(mission["last_checkpoint_id"])
        self.assertTrue(mission["title"].startswith("[SIMULADA]"))

        # 3 Eventos en secuencia
        events = envelope["events"]
        self.assertEqual(len(events), 3)

        # Evento 1: Creacion
        self.assertIsNone(events[0]["previous_state"])
        self.assertEqual(events[0]["new_state"], "BORRADOR")
        self.assertEqual(events[0]["actor_role"], "sistema")
        self.assertEqual(events[0]["action"], "creacion_de_mision")
        self.assertEqual(events[0]["version"], 1)

        # Evento 2: MT-002a
        self.assertEqual(events[1]["previous_state"], "BORRADOR")
        self.assertEqual(events[1]["new_state"], "LISTA_PARA_PLAN")
        self.assertEqual(events[1]["actor_role"], "chief_of_staff")
        self.assertEqual(events[1]["action"], "validacion_de_brief")
        self.assertEqual(events[1]["version"], 2)

        # Evento 3: MT-004
        self.assertEqual(events[2]["previous_state"], "LISTA_PARA_PLAN")
        self.assertEqual(events[2]["new_state"], "PLAN_EN_REVISION")
        self.assertEqual(events[2]["actor_role"], "chief_of_staff")
        self.assertEqual(events[2]["action"], "presentacion_de_plan")
        self.assertEqual(events[2]["version"], 3)

        # Validacion estricta de schemas
        self.mission_validator.validate(mission)
        for ev in events:
            self.event_validator.validate(ev)

        # Plan generado
        plan = envelope["plan"]
        self.assertIsNotNone(plan)
        self.assertEqual(plan["simulation_status"], "SIMULADA")
        self.assertEqual(len(plan["tasks"]), 4)

    def test_ca02_missing_fields_produce_clarification_required(self) -> None:
        """CA-02: Cada campo formal faltante produce ACLARACION_REQUERIDA, identifica el campo y no genera plan."""
        fields_to_test = ["objective", "context", "expected_result", "constraints"]

        for field in fields_to_test:
            with self.subTest(missing_field=field):
                data = copy.deepcopy(self.base_fixture)
                if field == "constraints":
                    del data["constraints"]
                else:
                    data[field] = ""  # Cadena vacia

                exit_code, envelope = demo_intake.run_demo_intake(raw_data=data)

                self.assertEqual(exit_code, 3)
                self.assertIn(field, envelope["pending_fields"])
                self.assertIsNone(envelope["plan"])

                mission = envelope["mission"]
                self.assertIsNotNone(mission)
                self.assertEqual(mission["current_state"], "ACLARACION_REQUERIDA")
                self.assertEqual(mission["counters"]["clarification_cycles"], 1)
                self.assertEqual(mission["record_version"], 2)

                # Eventos: exactamente 2
                events = envelope["events"]
                self.assertEqual(len(events), 2)
                self.assertEqual(events[1]["previous_state"], "BORRADOR")
                self.assertEqual(events[1]["new_state"], "ACLARACION_REQUERIDA")
                self.assertEqual(events[1]["actor_role"], "chief_of_staff")

                self.mission_validator.validate(mission)
                for ev in events:
                    self.event_validator.validate(ev)

    def test_ca03_assumptions_or_decisions_prevent_lista_para_plan(self) -> None:
        """CA-03: Supuestos o decisiones pendientes impiden LISTA_PARA_PLAN; no se fabrican aprobaciones."""
        # Caso con supuestos
        data_assumptions = copy.deepcopy(self.base_fixture)
        data_assumptions["assumptions"] = ["Se asume disponibilidad de API de pagos"]

        exit_code, envelope = demo_intake.run_demo_intake(raw_data=data_assumptions)
        self.assertEqual(exit_code, 3)
        self.assertEqual(envelope["mission"]["current_state"], "ACLARACION_REQUERIDA")
        self.assertEqual(envelope["mission"]["approval_refs"], [])
        self.assertIsNone(envelope["plan"])

        # Caso con decisiones pendientes
        data_decisions = copy.deepcopy(self.base_fixture)
        data_decisions["pending_decisions"] = ["Elegir entre arquitectura monolito o modular"]

        exit_code2, envelope2 = demo_intake.run_demo_intake(raw_data=data_decisions)
        self.assertEqual(exit_code2, 3)
        self.assertEqual(envelope2["mission"]["current_state"], "ACLARACION_REQUERIDA")
        self.assertEqual(envelope2["mission"]["approval_refs"], [])
        self.assertIsNone(envelope2["plan"])

    def test_ca04_invalid_inputs_and_exceeded_limits_rejected(self) -> None:
        """CA-04: JSON invalido, tipo incorrecto, claves desconocidas, limites excedidos y fixture ausente se rechazan."""
        # 1. Archivo ausente
        exit_code, env = demo_intake.run_demo_intake(fixture_path="archivo_inexistente_12345.json")
        self.assertEqual(exit_code, 2)
        self.assertEqual(env["errors"][0]["error_code"], "NOT_FOUND")

        # 2. Raiz no dict
        exit_code, env = demo_intake.run_demo_intake(raw_data=["no_es_objeto"])
        self.assertEqual(exit_code, 1)
        self.assertEqual(env["errors"][0]["error_code"], "INVALID_INPUT")

        # 3. Claves desconocidas / inyeccion de campos prohibidos
        forbidden_keys = ["current_state", "actor_role", "approval_refs", "approved", "thought", "chain_of_thought"]
        for key in forbidden_keys:
            with self.subTest(forbidden_key=key):
                data = copy.deepcopy(self.base_fixture)
                data[key] = "inyeccion"
                exit_code, env = demo_intake.run_demo_intake(raw_data=data)
                self.assertEqual(exit_code, 1)
                self.assertEqual(env["errors"][0]["error_code"], "INVALID_INPUT")

        # 4. simulation_status distinto de SIMULADA
        data_sim = copy.deepcopy(self.base_fixture)
        data_sim["simulation_status"] = "REAL"
        exit_code, env = demo_intake.run_demo_intake(raw_data=data_sim)
        self.assertEqual(exit_code, 1)
        self.assertEqual(env["errors"][0]["error_code"], "INVALID_INPUT")

        # 5. user_id o title vacios o no cadenas
        data_user = copy.deepcopy(self.base_fixture)
        data_user["user_id"] = "   "
        exit_code, env = demo_intake.run_demo_intake(raw_data=data_user)
        self.assertEqual(exit_code, 1)

        # 6. Limite de longitud de cadenas (> 4000 caracteres)
        data_long_str = copy.deepcopy(self.base_fixture)
        data_long_str["objective"] = "x" * 4001
        exit_code, env = demo_intake.run_demo_intake(raw_data=data_long_str)
        self.assertEqual(exit_code, 1)
        self.assertIn("excede el limite", env["errors"][0]["message"])

        # 7. Limite de coleccion (> 20 elementos)
        data_long_list = copy.deepcopy(self.base_fixture)
        data_long_list["constraints"] = [f"constraint_{i}" for i in range(21)]
        exit_code, env = demo_intake.run_demo_intake(raw_data=data_long_list)
        self.assertEqual(exit_code, 1)
        self.assertIn("excede el limite", env["errors"][0]["message"])

    def test_ca05_schemas_validation_and_invalid_date_format_check(self) -> None:
        """CA-05: Mision y eventos reales pasan schemas; una fecha invalida de prueba es rechazada."""
        exit_code, envelope = demo_intake.run_demo_intake(raw_data=self.base_fixture)
        self.assertEqual(exit_code, 0)

        mission = envelope["mission"]
        self.mission_validator.validate(mission)
        for ev in envelope["events"]:
            self.event_validator.validate(ev)

        # Verificar que el validador rechaza fechas no conformes a ISO 8601 date-time
        bad_mission = copy.deepcopy(mission)
        bad_mission["created_at"] = "2026-08-30 12:00:00"  # formato no ISO date-time valido
        with self.assertRaises(jsonschema.ValidationError):
            self.mission_validator.validate(bad_mission)

        bad_event = copy.deepcopy(envelope["events"][0])
        bad_event["timestamp"] = "fecha_invalida"
        with self.assertRaises(jsonschema.ValidationError):
            self.event_validator.validate(bad_event)

    def test_ca06_plan_template_structural_validation(self) -> None:
        """CA-06: Plantilla con campo obligatorio ausente, ID duplicado, rol ajeno, dependencia ausente/propia/circular no alcanza PLAN_EN_REVISION."""
        # 1. Campo obligatorio ausente en tarea
        data_missing_field = copy.deepcopy(self.base_fixture)
        del data_missing_field["plan_template"]["tasks"][1]["expected_output"]
        exit_code, env = demo_intake.run_demo_intake(raw_data=data_missing_field)
        self.assertEqual(exit_code, 1)
        self.assertEqual(env["mission"]["current_state"], "LISTA_PARA_PLAN")

        # 2. task_id duplicado
        data_dup_id = copy.deepcopy(self.base_fixture)
        data_dup_id["plan_template"]["tasks"][1]["task_id"] = data_dup_id["plan_template"]["tasks"][0]["task_id"]
        exit_code, env = demo_intake.run_demo_intake(raw_data=data_dup_id)
        self.assertEqual(exit_code, 1)

        # 3. Rol ajeno o fuera de orden
        data_wrong_role = copy.deepcopy(self.base_fixture)
        data_wrong_role["plan_template"]["tasks"][0]["agent_role"] = "product_architect"
        exit_code, env = demo_intake.run_demo_intake(raw_data=data_wrong_role)
        self.assertEqual(exit_code, 1)

        # 4. Tarea 0 con dependencias indebidas
        data_dep0 = copy.deepcopy(self.base_fixture)
        data_dep0["plan_template"]["tasks"][0]["dependencies"] = ["TSK-EXT"]
        exit_code, env = demo_intake.run_demo_intake(raw_data=data_dep0)
        self.assertEqual(exit_code, 1)

        # 5. Auto-dependencia
        data_self_dep = copy.deepcopy(self.base_fixture)
        t1_id = data_self_dep["plan_template"]["tasks"][1]["task_id"]
        data_self_dep["plan_template"]["tasks"][1]["dependencies"] = [t1_id]
        exit_code, env = demo_intake.run_demo_intake(raw_data=data_self_dep)
        self.assertEqual(exit_code, 1)

        # 6. Herramientas no vacias en esta pieza
        data_tools = copy.deepcopy(self.base_fixture)
        data_tools["plan_template"]["tasks"][0]["allowed_tool_categories"] = ["web_search"]
        exit_code, env = demo_intake.run_demo_intake(raw_data=data_tools)
        self.assertEqual(exit_code, 1)

        # 7. Limites no permitidos
        data_budget = copy.deepcopy(self.base_fixture)
        data_budget["plan_template"]["tasks"][0]["limits"]["max_budget_usd"] = 100
        exit_code, env = demo_intake.run_demo_intake(raw_data=data_budget)
        self.assertEqual(exit_code, 1)

    def test_ca07_immutability_and_state_isolation(self) -> None:
        """CA-07: La copia de la plantilla no modifica la entrada; ejecuciones independientes no comparten estado."""
        input_data = copy.deepcopy(self.base_fixture)
        input_copy = copy.deepcopy(input_data)

        exit_code1, env1 = demo_intake.run_demo_intake(raw_data=input_data)
        self.assertEqual(exit_code1, 0)

        # Modificar objetos devueltos no afecta la entrada original
        env1["plan"]["tasks"][0]["objective"] = "MODIFICADO"
        env1["mission"]["title"] = "MODIFICADO"

        self.assertEqual(input_data, input_copy)

        # Segunda ejecucion independiente no comparte IDs ni referencias
        exit_code2, env2 = demo_intake.run_demo_intake(raw_data=input_data)
        self.assertEqual(exit_code2, 0)
        self.assertNotEqual(env1["mission"]["mission_id"], env2["mission"]["mission_id"])
        self.assertIsNot(env1["plan"]["tasks"], env2["plan"]["tasks"])

    def test_ca08_simulada_tags_and_no_real_agents(self) -> None:
        """CA-08: Etiqueta SIMULADA visible en sobre, titulo, plan, tareas y eventos simulados."""
        exit_code, env = demo_intake.run_demo_intake(raw_data=self.base_fixture)
        self.assertEqual(exit_code, 0)

        self.assertEqual(env["simulation_status"], "SIMULADA")
        self.assertTrue(env["mission"]["title"].startswith("[SIMULADA]"))
        self.assertEqual(env["plan"]["simulation_status"], "SIMULADA")

        for task in env["plan"]["tasks"]:
            self.assertEqual(task["simulation_status"], "SIMULADA")

        for ev in env["events"]:
            self.assertIn("SIMULADA", ev["result_summary"])
            if ev["actor_role"] == "chief_of_staff":
                self.assertEqual(ev["actor"], "chief_of_staff_simulado")

    def test_ca09_no_forced_reserved_states(self) -> None:
        """CA-09: Ninguna entrada puede forzar AUTORIZADA_PARA_EJECUTAR, EN_EJECUCION, VBP_APROBADO o FINALIZADA."""
        reserved_states = ["AUTORIZADA_PARA_EJECUTAR", "EN_EJECUCION", "VBP_APROBADO", "FINALIZADA", "CANCELADA"]
        for st in reserved_states:
            with self.subTest(reserved_state=st):
                data = copy.deepcopy(self.base_fixture)
                data["current_state"] = st
                exit_code, env = demo_intake.run_demo_intake(raw_data=data)
                self.assertEqual(exit_code, 1)
                self.assertEqual(env["errors"][0]["error_code"], "INVALID_INPUT")

    def test_ca10_no_side_effects_on_import_or_execution(self) -> None:
        """CA-10: Importacion limpia, sin llamadas de red, modelos ni subprocesos."""
        self.assertEqual(demo_intake.EXPECTED_AGENT_ROLES_SEQUENCE, [
            "research_evidence_analyst",
            "product_architect",
            "delivery_planner",
            "governance_risk",
        ])
        exit_code, env = demo_intake.run_demo_intake(raw_data=self.base_fixture)
        self.assertEqual(exit_code, 0)
        self.assertEqual(env["mission"]["counters"]["task_reasoning_attempts"], 0)
        self.assertEqual(env["mission"]["counters"]["agent_requests"], 0)

    def test_ca11_cli_execution_and_exit_codes(self) -> None:
        """CA-11: CLI ejecutable, JSON parseable y codigos de salida correctos."""
        # 1. Ejecucion normal sobre DEFAULT_FIXTURE_PATH
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = demo_intake.main()

        self.assertEqual(exit_code, 0)
        raw_output = buffer.getvalue().strip()
        parsed = json.loads(raw_output)
        self.assertEqual(parsed["simulation_status"], "SIMULADA")
        self.assertEqual(parsed["mission"]["current_state"], "PLAN_EN_REVISION")

        # 2. Ejecucion con fixture ausente
        with patch.object(demo_intake, "DEFAULT_FIXTURE_PATH", Path("inexistente.json")):
            buf_err = io.StringIO()
            with redirect_stdout(buf_err):
                exit_code_err = demo_intake.main()
            self.assertEqual(exit_code_err, 2)
            parsed_err = json.loads(buf_err.getvalue().strip())
            self.assertEqual(parsed_err["errors"][0]["error_code"], "NOT_FOUND")


class TestCorrection1(unittest.TestCase):
    """Regresiones de la correccion 1, sin sustituir validadores ni crear fixtures."""

    setUp = TestDemoIntake.setUp

    def assert_valid_records(self, envelope):
        self.assertEqual(envelope["simulation_status"], "SIMULADA")
        if envelope["mission"] is not None:
            self.mission_validator.validate(envelope["mission"])
            self.assertEqual(envelope["mission"]["approval_refs"], [])
            self.assertIsNone(envelope["mission"]["active_task"])
        for event in envelope["events"]:
            self.event_validator.validate(event)
            self.assertIsNone(event["related_approval_id"])
        for error in envelope["errors"]:
            self.error_validator.validate(error)
            self.assertFalse(error["retry_allowed"])

    def assert_rejected(self, result, error_code="INVALID_INPUT"):
        code, envelope = result
        self.assertNotEqual(code, 0)
        self.assertNotEqual(code, 3)
        self.assertTrue(envelope["errors"])
        self.assertEqual({err["error_code"] for err in envelope["errors"]}, {error_code})
        self.assertIsNone(envelope["plan"])
        self.assertNotIn("PLAN_EN_REVISION", [ev["new_state"] for ev in envelope["events"]])
        if envelope["mission"] is not None:
            self.assertNotEqual(envelope["mission"]["current_state"], "PLAN_EN_REVISION")
        self.assert_valid_records(envelope)
        return envelope

    @contextmanager
    def fixture_bytes(self, payload):
        """Sustituir solo la lectura de fixture; contratos y validacion siguen reales."""
        original_open = builtins.open

        def read_fixture(file, mode="r", *args, **kwargs):
            if Path(file) == DEFAULT_FIXTURE_PATH:
                self.assertIn(mode, ("r", "rb"))
                if isinstance(payload, Exception):
                    raise payload
                return io.BytesIO(payload) if "b" in mode else io.StringIO(payload.decode("utf-8"))
            self.assertFalse(any(flag in mode for flag in "wax+"))
            return original_open(file, mode, *args, **kwargs)

        with patch("builtins.open", side_effect=read_fixture):
            yield

    def call_cli(self, payload=None, module=demo_intake):
        stdout, stderr = io.StringIO(), io.StringIO()
        with ExitStack() as stack:
            if payload is not None:
                stack.enter_context(self.fixture_bytes(payload))
            stack.enter_context(redirect_stdout(stdout))
            stack.enter_context(redirect_stderr(stderr))
            code = module.main()
        self.assertEqual(stderr.getvalue(), "")
        # json.loads rechaza banners, trazas y un segundo documento JSON.
        envelope = json.loads(stdout.getvalue())
        self.assertIsInstance(envelope, dict)
        self.assert_valid_records(envelope)
        return code, envelope

    def fresh_module(self, name="demo_intake_correction_probe"):
        spec = importlib.util.spec_from_file_location(name, demo_intake.__file__)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_input_refs_reject_mixed_types_objects_and_unknown_references(self):
        sentinel = "SYNTHETIC_TEST_SENTINEL"
        invalid = [
            ["brief", 123], ["brief", {"internal_reasoning": sentinel}],
            ["brief", None], ["brief", False], ["brief", ["brief"]],
            ["brief", "plan"], ["brief", "TSK-001-RESEARCH"],
            ["brief", "https://example.invalid/private"], ["brief", ""],
            [], "brief", None, {"brief": sentinel}, [123],
        ]
        for idx in range(4):
            for refs in invalid:
                with self.subTest(position=idx, refs=refs):
                    data = copy.deepcopy(self.base_fixture)
                    data["plan_template"]["tasks"][idx]["input_refs"] = refs
                    template, errors = demo_intake.validate_plan_template(data["plan_template"])
                    self.assertIsNone(template)
                    self.assertTrue(errors)
                    envelope = self.assert_rejected(demo_intake.run_demo_intake(raw_data=data))
                    self.assertNotIn(sentinel, json.dumps(envelope))

    def test_optional_lists_absent_and_empty_are_accepted(self):
        for field in ("assumptions", "pending_decisions"):
            for absent in (True, False):
                with self.subTest(field=field, absent=absent):
                    data = copy.deepcopy(self.base_fixture)
                    if absent:
                        del data[field]
                    else:
                        data[field] = []
                    code, envelope = demo_intake.run_demo_intake(raw_data=data)
                    self.assertEqual(code, 0)
                    self.assertEqual(envelope["brief"][field], [])
                    self.assertEqual(envelope["mission"]["current_state"], "PLAN_EN_REVISION")
                    self.assert_valid_records(envelope)

    def test_optional_lists_null_and_wrong_types_are_rejected(self):
        for field in ("assumptions", "pending_decisions"):
            for value in (None, False, 0, "", {}, [123], ["valido", None]):
                with self.subTest(field=field, value=value):
                    data = copy.deepcopy(self.base_fixture)
                    data[field] = value
                    env = self.assert_rejected(demo_intake.run_demo_intake(raw_data=data))
                    self.assertIsNone(env["mission"])
                    self.assertIsNone(env["brief"])

    def test_optional_lists_nonempty_require_clarification(self):
        for fields in (("assumptions",), ("pending_decisions",), ("assumptions", "pending_decisions")):
            with self.subTest(fields=fields):
                data = copy.deepcopy(self.base_fixture)
                for field in fields:
                    data[field] = ["Pendiente de decision del usuario"]
                code, env = demo_intake.run_demo_intake(raw_data=data)
                self.assertEqual(code, 3)
                self.assertIsNone(env["plan"])
                self.assertEqual([e["new_state"] for e in env["events"]], ["BORRADOR", "ACLARACION_REQUERIDA"])
                self.assertEqual(env["mission"]["counters"]["clarification_cycles"], 1)
                for field in fields:
                    self.assertEqual(env["brief"][field], data[field])
                self.assert_valid_records(env)

    def test_task_limits_reject_boolean_wrong_types_and_values(self):
        invalid = {
            "max_attempts": [False, True, 2.0, "2", None, [], {}, 0, 1, 3],
            "max_seconds": [False, True, 300.0, "300", None, [], {}, 0, 299, 301],
            "max_budget_usd": [False, True, "0", None, [], {}, -1, 1, float("nan"), float("inf")],
        }
        for idx in range(4):
            for field, values in invalid.items():
                for value in values:
                    with self.subTest(position=idx, field=field, value=value):
                        data = copy.deepcopy(self.base_fixture)
                        data["plan_template"]["tasks"][idx]["limits"][field] = value
                        self.assert_rejected(demo_intake.run_demo_intake(raw_data=data))

    def test_task_limits_accept_integer_and_float_zero_budget(self):
        for budget in (0, 0.0):
            with self.subTest(budget=budget):
                data = copy.deepcopy(self.base_fixture)
                for task in data["plan_template"]["tasks"]:
                    task["limits"]["max_budget_usd"] = budget
                code, env = demo_intake.run_demo_intake(raw_data=data)
                self.assertEqual(code, 0)
                self.assertEqual([t["status"] for t in env["plan"]["tasks"]], ["PENDIENTE"] * 4)
                self.assert_valid_records(env)

    def test_closed_objects_and_required_limit_fields_remain_enforced(self):
        for level in ("plan", "task", "limits"):
            with self.subTest(level=level):
                data = copy.deepcopy(self.base_fixture)
                plan = data["plan_template"]
                target = {"plan": plan, "task": plan["tasks"][0], "limits": plan["tasks"][0]["limits"]}[level]
                target["internal_reasoning"] = "SYNTHETIC_TEST_SENTINEL"
                env = self.assert_rejected(demo_intake.run_demo_intake(raw_data=data))
                self.assertNotIn("SYNTHETIC_TEST_SENTINEL", json.dumps(env))
        for field in ("max_attempts", "max_seconds", "max_budget_usd"):
            with self.subTest(missing=field):
                data = copy.deepcopy(self.base_fixture)
                del data["plan_template"]["tasks"][0]["limits"][field]
                self.assert_rejected(demo_intake.run_demo_intake(raw_data=data))

    def test_nonobject_tasks_are_rejected_at_every_position(self):
        for idx in range(4):
            for value in (None, False, 0, 1.5, "tarea", [], ["tarea"]):
                with self.subTest(position=idx, value=value):
                    data = copy.deepcopy(self.base_fixture)
                    data["plan_template"]["tasks"][idx] = value
                    template, errors = demo_intake.validate_plan_template(data["plan_template"])
                    self.assertIsNone(template)
                    self.assertTrue(errors)
                    self.assert_rejected(demo_intake.run_demo_intake(raw_data=data))

    def run_with_policy_change(self, transition_id, field, value, remove=False):
        contracts = copy.deepcopy((self.mission_schema, self.event_schema, self.error_schema, self.state_machine))
        transition = next(t for t in contracts[3]["mission_transitions"] if t["id"] == transition_id)
        if remove:
            del transition[field]
        else:
            transition[field] = value
        data = copy.deepcopy(self.base_fixture)
        if transition_id == "MT-001":
            data["objective"] = ""
        with patch.object(demo_intake, "load_core_contracts", return_value=contracts):
            result = demo_intake.run_demo_intake(raw_data=data)
        return result

    def assert_transition_stopped(self, result, transition_id, error_code):
        env = self.assert_rejected(result, error_code)
        states = ["BORRADOR", "LISTA_PARA_PLAN"] if transition_id == "MT-004" else ["BORRADOR"]
        self.assertEqual([e["new_state"] for e in env["events"]], states)
        self.assertEqual(env["mission"]["current_state"], states[-1])
        self.assertEqual(env["mission"]["record_version"], len(states))
        self.assertEqual(env["mission"]["counters"]["clarification_cycles"], 0)

    def test_transition_authority_absent_unknown_incompatible_is_rejected(self):
        for transition_id in ("MT-001", "MT-002a", "MT-004"):
            for value in (None, "", "desconocida", "solo_usuario_humano", "governance_risk", "accion_determinista", [], {}):
                with self.subTest(transition=transition_id, authority=value):
                    result = self.run_with_policy_change(transition_id, "authority", value)
                    self.assert_transition_stopped(result, transition_id, "PERMISSION_DENIED")
            with self.subTest(transition=transition_id, authority="ausente"):
                result = self.run_with_policy_change(transition_id, "authority", None, remove=True)
                self.assert_transition_stopped(result, transition_id, "PERMISSION_DENIED")

    def test_transition_human_approval_true_or_undefined_is_rejected(self):
        for transition_id in ("MT-001", "MT-002a", "MT-004"):
            for value in (True, None, 0, 1, "false", [], {}):
                with self.subTest(transition=transition_id, approval=value):
                    result = self.run_with_policy_change(transition_id, "requires_human_approval", value)
                    self.assert_transition_stopped(result, transition_id, "PERMISSION_DENIED")
            with self.subTest(transition=transition_id, approval="ausente"):
                result = self.run_with_policy_change(transition_id, "requires_human_approval", None, remove=True)
                self.assert_transition_stopped(result, transition_id, "PERMISSION_DENIED")

    def test_transition_missing_or_inconsistent_pair_is_rejected(self):
        for transition_id in ("MT-001", "MT-002a", "MT-004"):
            for field, value in (("id", "MT-AUSENTE"), ("from", "FINALIZADA"), ("to", "VBP_APROBADO")):
                with self.subTest(transition=transition_id, field=field):
                    result = self.run_with_policy_change(transition_id, field, value)
                    self.assert_transition_stopped(result, transition_id, "SYSTEM_ERROR")

    def test_cli_complete_and_incomplete_exit_codes(self):
        data = copy.deepcopy(self.base_fixture)
        for complete in (True, False):
            with self.subTest(complete=complete):
                if not complete:
                    del data["context"]
                code, env = self.call_cli(json.dumps(data).encode("utf-8"))
                self.assertEqual(code, 0 if complete else 3)
                states = ["BORRADOR", "LISTA_PARA_PLAN", "PLAN_EN_REVISION"] if complete else ["BORRADOR", "ACLARACION_REQUERIDA"]
                self.assertEqual([e["new_state"] for e in env["events"]], states)
                self.assertEqual(env["mission"]["current_state"], states[-1])

    def test_cli_malformed_json_and_nonobject_roots_return_one_json(self):
        for payload in (b'{"title":', b'{"x":1} trailing', b"null", b"[]", b'"cadena"', b"false", b"123", b"\xff", b"NaN"):
            with self.subTest(payload=payload):
                env = self.assert_rejected(self.call_cli(payload))
                self.assertIsNone(env["mission"])
                self.assertEqual(env["events"], [])

    def test_cli_size_limit_counts_bytes_and_accepts_exactly_64_kib(self):
        data = copy.deepcopy(self.base_fixture)
        data["title"] = "Ensayo con acentos: " + "\u00e1" * 100
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
        exact = encoded + b" " * (65536 - len(encoded))
        self.assertEqual(len(exact), 65536)
        self.assertLess(len(exact.decode("utf-8")), 65536)
        code, env = self.call_cli(exact)
        self.assertEqual(code, 0)
        self.assertEqual(env["mission"]["current_state"], "PLAN_EN_REVISION")
        self.assert_rejected(self.call_cli(exact + b" "))

    def test_cli_nonobject_task_is_controlled(self):
        for idx in range(4):
            with self.subTest(position=idx):
                data = copy.deepcopy(self.base_fixture)
                data["plan_template"]["tasks"][idx] = None
                self.assert_rejected(self.call_cli(json.dumps(data).encode("utf-8")))

    def test_cli_deep_json_and_oversized_integer_are_controlled(self):
        for payload in (b"[" * 1500 + b"0" + b"]" * 1500, b"9" * 5000):
            with self.subTest(kind=payload[:1]):
                self.assert_rejected(self.call_cli(payload))

    def test_missing_dependency_import_and_module_entrypoint_are_controlled(self):
        # El import real falla; no se desinstala ni se simula un validador exitoso.
        with patch.dict(sys.modules, {"jsonschema": None}):
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                module = self.fresh_module()
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(stderr.getvalue(), "")
            env = self.assert_rejected(self.call_cli(module=module), "SYSTEM_ERROR")
            self.assertIn("jsonschema", env["errors"][0]["message"])
            self.assertIn("no se realizo validacion", env["errors"][0]["message"])
            self.assertIsNone(env["mission"])
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as raised:
                    self.fresh_module("__main__")
            self.assertNotEqual(raised.exception.code, 0)
            self.assertEqual(stderr.getvalue(), "")
            self.assert_rejected((raised.exception.code, json.loads(stdout.getvalue())), "SYSTEM_ERROR")

    def test_cli_read_failure_is_sanitized_and_nonzero(self):
        marker = "SYNTHETIC_TEST_SENTINEL"
        env = self.assert_rejected(self.call_cli(PermissionError(marker)), "SYSTEM_ERROR")
        self.assertNotIn(marker, json.dumps(env))
        self.assertIsNone(env["mission"])

    def test_contract_load_failure_is_controlled_without_private_diagnostics(self):
        marker = "SYNTHETIC_TEST_SENTINEL"
        for error in (FileNotFoundError(marker), ValueError(marker), RuntimeError(marker)):
            with self.subTest(error=type(error).__name__):
                with patch.object(demo_intake, "load_core_contracts", side_effect=error):
                    env = self.assert_rejected(self.call_cli(), "SYSTEM_ERROR")
                self.assertNotIn(marker, json.dumps(env))
                self.assertIsNone(env["mission"])

    def test_real_schema_failure_is_not_success_or_sensitive_json(self):
        # No mock del validador: la fecha invalida es rechazada por el schema real.
        code, env = demo_intake.run_demo_intake(
            raw_data=self.base_fixture,
            now_fn=lambda: datetime(2026, 8, 30, 12, 0, 0),
        )
        self.assert_rejected((code, env), "SYSTEM_ERROR")
        self.assertNotIn(self.base_fixture["objective"], json.dumps(env))
        self.assertIsNone(env["mission"])

    def test_raw_null_nonstring_keys_and_cyclic_input_are_rejected(self):
        cyclic = copy.deepcopy(self.base_fixture)
        cyclic["assumptions"] = [cyclic]
        for data in (None, {123: "valor"}, {123: "valor", "otra": "valor"}, cyclic):
            with self.subTest(kind=type(data).__name__, cyclic=data is cyclic):
                self.assert_rejected(demo_intake.run_demo_intake(raw_data=data))

    @contextmanager
    def forbid_effects(self):
        """Interceptar fronteras reales y registrar cualquier intento prohibido."""
        attempts = []

        def blocked(*args, **kwargs):
            attempts.append("efecto_prohibido")
            raise AssertionError("Efecto prohibido interceptado")

        def read_only(original):
            def checked(file, mode="r", *args, **kwargs):
                if any(flag in mode for flag in "wax+"):
                    return blocked()
                return original(file, mode, *args, **kwargs)
            return checked

        original_os_open = os.open

        def checked_os_open(path, flags, *args, **kwargs):
            if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
                return blocked()
            return original_os_open(path, flags, *args, **kwargs)

        with ExitStack() as stack:
            for target in (
                "socket.socket", "socket.create_connection", "socket.getaddrinfo",
                "urllib.request.urlopen", "subprocess.Popen", "subprocess.run",
                "os.system", "os.popen", "os.mkdir", "os.remove", "os.unlink",
                "os.rename", "os.replace", "os.rmdir",
            ):
                stack.enter_context(patch(target, side_effect=blocked))
            for name in ("startfile", "spawnl", "spawnle", "spawnv", "spawnve", "execv", "execve", "fork", "posix_spawn"):
                if hasattr(os, name):
                    stack.enter_context(patch.object(os, name, side_effect=blocked))
            stack.enter_context(patch("builtins.open", side_effect=read_only(builtins.open)))
            stack.enter_context(patch("io.open", side_effect=read_only(io.open)))
            stack.enter_context(patch("os.open", side_effect=checked_os_open))
            yield attempts

    def test_no_network_processes_or_writes_on_import_and_all_outcomes(self):
        with self.forbid_effects() as attempts:
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                module = self.fresh_module()
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(stderr.getvalue(), "")
            code, env = self.call_cli(module=module)
            self.assertEqual(code, 0)
            self.assertEqual([t["status"] for t in env["plan"]["tasks"]], ["PENDIENTE"] * 4)
            data = copy.deepcopy(self.base_fixture)
            data["objective"] = ""
            code, env = self.call_cli(json.dumps(data).encode("utf-8"), module=module)
            self.assertEqual(code, 3)
            self.assertIsNone(env["plan"])
            self.assert_rejected(self.call_cli(b'{"title":', module=module))
            self.assert_rejected(self.call_cli(b" " * 65537, module=module))
            with patch.dict(sys.modules, {"jsonschema": None}):
                unavailable = self.fresh_module()
                self.assert_rejected(self.call_cli(module=unavailable), "SYSTEM_ERROR")
        # Detecta incluso un intento cuya excepcion haya sido capturada por el demo.
        self.assertEqual(attempts, [])


if __name__ == "__main__":
    unittest.main()
