"""Pruebas exhaustivas para el modulo app.demo_plan_review (PZ-003B SIMULADA).

Cubre todos los criterios de aceptacion CB-01 a CB-14, validando
la puerta de decision local, huellas exactas, expiracion, idempotencia,
atomicidad, esquemas de aprobacion y checkpoint, integridad referencial y CLI.
"""

import copy
import builtins
import importlib.util
import io
import json
import os
import socket
import subprocess
import sys
import unittest
from contextlib import ExitStack, contextmanager, redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import jsonschema
from jsonschema import Draft202012Validator

import app.demo_plan_review as demo_plan_review

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTRACTS_CORE_DIR = PROJECT_ROOT / "contracts" / "core"
DEFAULT_FIXTURE_PATH = PROJECT_ROOT / "examples" / "demo_mission.json"


class TestDemoPlanReview(unittest.TestCase):
    """Suite de pruebas para la puerta local de decision del plan PZ-003B."""

    def setUp(self) -> None:
        with open(DEFAULT_FIXTURE_PATH, "r", encoding="utf-8") as f:
            self.base_fixture = json.load(f)

        (
            self.mission_schema,
            self.event_schema,
            self.error_schema,
            self.approval_schema,
            self.checkpoint_schema,
            self.state_machine,
        ) = demo_plan_review.load_all_contracts()

        self.format_checker = demo_plan_review.demo_intake.get_format_checker()
        self.mission_validator = Draft202012Validator(self.mission_schema, format_checker=self.format_checker)
        self.event_validator = Draft202012Validator(self.event_schema, format_checker=self.format_checker)
        self.error_validator = Draft202012Validator(self.error_schema, format_checker=self.format_checker)
        self.approval_validator = Draft202012Validator(self.approval_schema, format_checker=self.format_checker)
        self.checkpoint_validator = Draft202012Validator(self.checkpoint_schema, format_checker=self.format_checker)

    def test_cb01_default_inspection_mode(self) -> None:
        """CB-01: Modo predeterminado: solicitud PENDIENTE, decision null, PLAN_EN_REVISION, 4 tareas pendientes, codigo 3."""
        session = demo_plan_review.PlanReviewSession()
        exit_code, env = session.init_from_intake(raw_data=self.base_fixture)

        self.assertEqual(exit_code, 3)
        self.assertEqual(env["simulation_status"], "SIMULADA")
        self.assertEqual(env["mission"]["current_state"], "PLAN_EN_REVISION")
        self.assertEqual(env["mission"]["record_version"], 4)
        self.assertEqual(len(env["events"]), 4)

        # Aprobacion PENDIENTE
        self.assertEqual(len(env["approvals"]), 1)
        app_req = env["approvals"][0]
        self.assertEqual(app_req["status"], "PENDIENTE")
        self.assertIsNone(app_req["decision"])
        self.assertEqual(app_req["comment"], "")
        self.assertTrue(app_req["version_or_fingerprint"].startswith("sha256:"))

        # Checkpoints vacio
        self.assertEqual(env["checkpoints"], [])
        self.assertEqual(len(env["plan"]["tasks"]), 4)
        for t in env["plan"]["tasks"]:
            self.assertEqual(t["status"], "PENDIENTE")

        # Metadata de review
        self.assertEqual(env["review"]["identity_scope"], "IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA")
        self.assertFalse(env["review"]["durable"])

        # Validacion estricta de schemas
        self.mission_validator.validate(env["mission"])
        self.approval_validator.validate(app_req)
        for ev in env["events"]:
            self.event_validator.validate(ev)

    def test_cb02_explicit_approval_flow(self) -> None:
        """CB-02: Aprobacion explicita: CONSUMIDA/APROBAR, MT-005, mision v5 AUTORIZADA_PARA_EJECUTAR, checkpoint valido."""
        fixed_dt = datetime(2026, 8, 30, 14, 0, 0, tzinfo=timezone.utc)
        seq = 0

        def deterministic_id(p: str) -> str:
            nonlocal seq
            seq += 1
            return f"{p}-{seq:03d}"

        session = demo_plan_review.PlanReviewSession(
            now_fn=lambda: fixed_dt,
            id_generator=deterministic_id,
            monotonic_time_fn=lambda: 12.5,
        )
        exit_code, env_init = session.init_from_intake(raw_data=self.base_fixture)
        self.assertEqual(exit_code, 3)

        app_req = env_init["approvals"][0]
        fp = app_req["version_or_fingerprint"]
        app_id = app_req["approval_id"]

        command = {
            "approval_id": app_id,
            "version_or_fingerprint": fp,
            "decision": "APROBAR",
            "comment": "Aprobacion conforme del plan de prueba",
            "idempotency_key": app_req["idempotency_key"],
        }
        actor_context = {
            "user_id": env_init["mission"]["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
            "identity_scope": "IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA",
        }

        exit_code_dec, env_final = session.process_decision(command, actor_context)

        self.assertEqual(exit_code_dec, 0)
        self.assertEqual(env_final["mission"]["current_state"], "AUTORIZADA_PARA_EJECUTAR")
        self.assertEqual(env_final["mission"]["record_version"], 5)
        self.assertIsNone(env_final["mission"]["active_task"])
        self.assertEqual(len(env_final["events"]), 5)

        # Aprobacion CONSUMIDA
        consumed_app = env_final["approvals"][0]
        self.assertEqual(consumed_app["status"], "CONSUMIDA")
        self.assertEqual(consumed_app["decision"], "APROBAR")
        self.assertEqual(consumed_app["comment"], "Aprobacion conforme del plan de prueba")

        # Checkpoint generado
        self.assertEqual(len(env_final["checkpoints"]), 1)
        chk = env_final["checkpoints"][0]
        self.assertEqual(chk["mission_id"], env_final["mission"]["mission_id"])
        self.assertEqual(chk["mission_version"], 5)
        self.assertEqual(chk["authorizations"], [app_id])
        self.assertEqual(chk["state"], "AUTORIZADA_PARA_EJECUTAR")
        self.assertEqual(len(chk["tasks"]), 4)
        self.assertEqual(env_final["mission"]["last_checkpoint_id"], chk["checkpoint_id"])

        # Validaciones de esquema
        self.mission_validator.validate(env_final["mission"])
        self.approval_validator.validate(consumed_app)
        self.checkpoint_validator.validate(chk)
        for ev in env_final["events"]:
            self.event_validator.validate(ev)

    def test_cb03_reject_and_request_changes_flow(self) -> None:
        """CB-03: RECHAZAR y SOLICITAR_CAMBIOS consumen con motivo y mantienen PLAN_EN_REVISION; comentario vacio se rechaza."""
        for dec in ["RECHAZAR", "SOLICITAR_CAMBIOS"]:
            with self.subTest(decision=dec):
                session = demo_plan_review.PlanReviewSession()
                session.init_from_intake(raw_data=self.base_fixture)
                app_req = session.approvals[0]

                # 1. Comentario vacio debe rechazarse
                cmd_no_comment = {
                    "approval_id": app_req["approval_id"],
                    "version_or_fingerprint": app_req["version_or_fingerprint"],
                    "decision": dec,
                    "comment": "   ",
                    "idempotency_key": app_req["idempotency_key"],
                }
                actor_ctx = {
                    "user_id": session.mission["user_id"],
                    "actor": "usuario_local_demo",
                    "actor_role": "usuario_humano",
                    "source": "terminal_local_autorizada",
                    "identity_scope": "IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA",
                }
                err_code, err_env = session.process_decision(cmd_no_comment, actor_ctx)
                self.assertEqual(err_code, 1)
                self.assertEqual(session.approvals[0]["status"], "PENDIENTE")

                # 2. Con motivo valido: consume la solicitud y mantiene PLAN_EN_REVISION
                cmd_valid = {
                    "approval_id": app_req["approval_id"],
                    "version_or_fingerprint": app_req["version_or_fingerprint"],
                    "decision": dec,
                    "comment": f"Motivo explicito para {dec}",
                    "idempotency_key": app_req["idempotency_key"],
                }
                dec_code, dec_env = session.process_decision(cmd_valid, actor_ctx)
                self.assertEqual(dec_code, 3)
                self.assertEqual(dec_env["mission"]["current_state"], "PLAN_EN_REVISION")
                self.assertEqual(dec_env["mission"]["record_version"], 5)
                self.assertEqual(dec_env["approvals"][0]["status"], "CONSUMIDA")
                self.assertEqual(dec_env["approvals"][0]["decision"], dec)
                self.assertEqual(dec_env["checkpoints"], [])

                self.mission_validator.validate(dec_env["mission"])
                self.approval_validator.validate(dec_env["approvals"][0])

    def test_cb04_actor_and_injection_rejections(self) -> None:
        """CB-04: Actor no humano, otro usuario, origen ajeno e inyecciones de campos se rechazan."""
        session = demo_plan_review.PlanReviewSession()
        session.init_from_intake(raw_data=self.base_fixture)
        app_req = session.approvals[0]

        valid_cmd = {
            "approval_id": app_req["approval_id"],
            "version_or_fingerprint": app_req["version_or_fingerprint"],
            "decision": "APROBAR",
            "comment": "ok",
            "idempotency_key": app_req["idempotency_key"],
        }

        # 1. Actor no humano
        bad_role_ctx = {
            "user_id": session.mission["user_id"],
            "actor": "chief_of_staff_simulado",
            "actor_role": "chief_of_staff",
            "source": "terminal_local_autorizada",
        }
        c1, e1 = session.process_decision(valid_cmd, bad_role_ctx)
        self.assertEqual(c1, 1)
        self.assertEqual(e1["errors"][-1]["error_code"], "PERMISSION_DENIED")

        # 2. Usuario no propietario
        bad_user_ctx = {
            "user_id": "USR-OTRO-999",
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
        }
        c2, e2 = session.process_decision(valid_cmd, bad_user_ctx)
        self.assertEqual(c2, 1)
        self.assertEqual(e2["errors"][-1]["error_code"], "PERMISSION_DENIED")

        # 3. Origen no autorizado
        bad_source_ctx = {
            "user_id": session.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "api_externa",
        }
        c3, e3 = session.process_decision(valid_cmd, bad_source_ctx)
        self.assertEqual(c3, 1)
        self.assertEqual(e3["errors"][-1]["error_code"], "PERMISSION_DENIED")

        # 4. Inyeccion de campos prohibidos en comando
        injected_cmd = copy.deepcopy(valid_cmd)
        injected_cmd["current_state"] = "AUTORIZADA_PARA_EJECUTAR"
        actor_ok = {
            "user_id": session.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
        }
        c4, e4 = session.process_decision(injected_cmd, actor_ok)
        self.assertEqual(c4, 1)
        self.assertEqual(e4["errors"][-1]["error_code"], "INVALID_INPUT")

    def test_cb05_fingerprint_mismatch_and_key_order_invariance(self) -> None:
        """CB-05: Huella alterada no autoriza; reordenar claves de diccionario produce la misma huella."""
        # Invarianza ante orden de claves
        fp1 = demo_plan_review.compute_plan_fingerprint(
            "M1", "U1", 1, 1, {"a": 1, "b": 2}, {"title": "T", "tasks": []}
        )
        fp2 = demo_plan_review.compute_plan_fingerprint(
            "M1", "U1", 1, 1, {"b": 2, "a": 1}, {"tasks": [], "title": "T"}
        )
        self.assertEqual(fp1, fp2)

        # Alteracion de un campo altera la huella
        fp_alt = demo_plan_review.compute_plan_fingerprint(
            "M1", "U1", 1, 1, {"a": 1, "b": 3}, {"title": "T", "tasks": []}
        )
        self.assertNotEqual(fp1, fp_alt)

        # Rechazo por huella incorrecta
        session = demo_plan_review.PlanReviewSession()
        session.init_from_intake(raw_data=self.base_fixture)
        app_req = session.approvals[0]

        bad_fp_cmd = {
            "approval_id": app_req["approval_id"],
            "version_or_fingerprint": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
            "decision": "APROBAR",
            "comment": "ok",
            "idempotency_key": app_req["idempotency_key"],
        }
        actor_ok = {
            "user_id": session.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
        }
        c_bad, e_bad = session.process_decision(bad_fp_cmd, actor_ok)
        self.assertEqual(c_bad, 1)
        self.assertEqual(e_bad["errors"][-1]["error_code"], "INVALID_INPUT")
        self.assertEqual(session.mission["current_state"], "PLAN_EN_REVISION")

    def test_cb06_idempotency_and_double_response_prevention(self) -> None:
        """CB-06: Duplicado exacto devuelve original; clave con contenido distinto y segunda respuesta se rechazan."""
        session = demo_plan_review.PlanReviewSession()
        session.init_from_intake(raw_data=self.base_fixture)
        app_req = session.approvals[0]

        cmd = {
            "approval_id": app_req["approval_id"],
            "version_or_fingerprint": app_req["version_or_fingerprint"],
            "decision": "APROBAR",
            "comment": "aprobado",
            "idempotency_key": app_req["idempotency_key"],
        }
        actor = {
            "user_id": session.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
        }

        # 1. Primera ejecucion
        c1, env1 = session.process_decision(cmd, actor)
        self.assertEqual(c1, 0)
        self.assertEqual(env1["mission"]["record_version"], 5)

        # 2. Duplicado exacto con misma clave
        c2, env2 = session.process_decision(cmd, actor)
        self.assertEqual(c2, 0)
        self.assertEqual(env2["mission"]["record_version"], 5)
        self.assertEqual(len(env2["events"]), 5)

        # 3. Misma clave con contenido distinto (conflicto)
        cmd_conflict = copy.deepcopy(cmd)
        cmd_conflict["comment"] = "comentario diferente"
        c3, env3 = session.process_decision(cmd_conflict, actor)
        self.assertEqual(c3, 1)
        self.assertEqual(env3["errors"][-1]["error_code"], "INVALID_INPUT")

        # 4. Segunda respuesta con distinta clave sobre solicitud ya consumida
        cmd_second = {
            "approval_id": app_req["approval_id"],
            "version_or_fingerprint": app_req["version_or_fingerprint"],
            "decision": "RECHAZAR",
            "comment": "segundo intento",
            "idempotency_key": "IDEMP-DISTINTA-002",
        }
        c4, env4 = session.process_decision(cmd_second, actor)
        self.assertEqual(c4, 1)
        self.assertEqual(env4["errors"][-1]["error_code"], "PERMISSION_DENIED")

    def test_cb07_expiration_lifecycle_and_boundaries(self) -> None:
        """CB-07: Responde antes de 300s; al vencimiento aplica AT-002 (EXPIRADA); terminal."""
        base_time = datetime(2026, 8, 30, 10, 0, 0, tzinfo=timezone.utc)
        current_time = base_time

        session = demo_plan_review.PlanReviewSession(now_fn=lambda: current_time)
        session.init_from_intake(raw_data=self.base_fixture)
        app_req = session.approvals[0]

        actor = {
            "user_id": session.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
        }

        # Justo en t = 300s (expirado)
        current_time = base_time + timedelta(seconds=300)
        cmd_exp = {
            "approval_id": app_req["approval_id"],
            "version_or_fingerprint": app_req["version_or_fingerprint"],
            "decision": "APROBAR",
            "comment": "tarde",
            "idempotency_key": app_req["idempotency_key"],
        }
        c_exp, env_exp = session.process_decision(cmd_exp, actor)
        self.assertEqual(c_exp, 1)
        self.assertEqual(session.approvals[0]["status"], "EXPIRADA")
        self.assertIsNone(session.approvals[0]["decision"])
        self.assertEqual(session.mission["current_state"], "PLAN_EN_REVISION")
        self.assertEqual(env_exp["errors"][-1]["error_code"], "PERMISSION_DENIED")

        self.approval_validator.validate(session.approvals[0])

    def test_cb08_manipulated_contracts_stop_flow(self) -> None:
        """CB-08: Maquina de estados alterada en memoria (sin MT-005 o AT-001) detiene el flujo."""
        bad_sm = copy.deepcopy(self.state_machine)
        # Eliminar MT-005
        bad_sm["mission_transitions"] = [
            t for t in bad_sm["mission_transitions"] if t["id"] != "MT-005"
        ]

        override = (
            self.mission_schema,
            self.event_schema,
            self.error_schema,
            self.approval_schema,
            self.checkpoint_schema,
            bad_sm,
        )
        session = demo_plan_review.PlanReviewSession(contracts_override=override)
        session.init_from_intake(raw_data=self.base_fixture)
        app_req = session.approvals[0]

        cmd = {
            "approval_id": app_req["approval_id"],
            "version_or_fingerprint": app_req["version_or_fingerprint"],
            "decision": "APROBAR",
            "comment": "ok",
            "idempotency_key": app_req["idempotency_key"],
        }
        actor = {
            "user_id": session.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
        }

        before = session.build_envelope()
        code, env = session.process_decision(cmd, actor)
        self.assertEqual(code, 1)
        self.assertEqual(env["errors"][0]["error_code"], "SYSTEM_ERROR")
        self.assertEqual(session.build_envelope(), before)

    def test_cb09_schemas_and_referential_integrity(self) -> None:
        """CB-09: Validacion de todos los registros producidos y verificacion de integridad referencial."""
        session = demo_plan_review.PlanReviewSession()
        session.init_from_intake(raw_data=self.base_fixture)
        app_req = session.approvals[0]

        cmd = {
            "approval_id": app_req["approval_id"],
            "version_or_fingerprint": app_req["version_or_fingerprint"],
            "decision": "APROBAR",
            "comment": "ok",
            "idempotency_key": app_req["idempotency_key"],
        }
        actor = {
            "user_id": session.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
        }
        session.process_decision(cmd, actor)

        # Validacion cruzada de integridad
        mission = session.mission
        approval = session.approvals[0]
        checkpoint = session.checkpoints[0]

        # RI-001: mission.approval_refs[] -> approval.approval_id
        self.assertIn(approval["approval_id"], mission["approval_refs"])

        # RI-002: mission.last_checkpoint_id -> checkpoint.checkpoint_id
        self.assertEqual(mission["last_checkpoint_id"], checkpoint["checkpoint_id"])

        # RI-003: checkpoint.authorizations[] -> approval.approval_id
        self.assertIn(approval["approval_id"], checkpoint["authorizations"])

    def test_cb10_atomicity_and_isolation(self) -> None:
        """CB-10: Modificar outputs no altera la sesion interna; sesiones nuevas estan aisladas."""
        session1 = demo_plan_review.PlanReviewSession()
        exit_code1, env1 = session1.init_from_intake(raw_data=self.base_fixture)

        # Modificar diccionario devuelto
        env1["mission"]["title"] = "CORRUPTO"
        env1["approvals"][0]["status"] = "CONSUMIDA"

        self.assertNotEqual(session1.mission["title"], "CORRUPTO")
        self.assertEqual(session1.approvals[0]["status"], "PENDIENTE")

        # Sesion 2 independiente
        session2 = demo_plan_review.PlanReviewSession()
        exit_code2, env2 = session2.init_from_intake(raw_data=self.base_fixture)
        self.assertNotEqual(session1.mission["mission_id"], session2.mission["mission_id"])
        self.assertNotEqual(session1.approvals[0]["approval_id"], session2.approvals[0]["approval_id"])

    def test_cb11_incomplete_brief_and_disabled_approvals(self) -> None:
        """CB-11: Brief incompleto no abre aprobacion; APROBAR_CON_EXCEPCION se rechaza."""
        # 1. Brief incompleto
        data_inc = copy.deepcopy(self.base_fixture)
        del data_inc["constraints"]

        session = demo_plan_review.PlanReviewSession()
        exit_code, env = session.init_from_intake(raw_data=data_inc)
        self.assertEqual(exit_code, 3)
        self.assertEqual(env["mission"]["current_state"], "ACLARACION_REQUERIDA")
        self.assertEqual(env["approvals"], [])
        self.assertIsNone(env["review"])

        # 2. APROBAR_CON_EXCEPCION rechazada
        session_valid = demo_plan_review.PlanReviewSession()
        session_valid.init_from_intake(raw_data=self.base_fixture)
        app_req = session_valid.approvals[0]

        cmd_exc = {
            "approval_id": app_req["approval_id"],
            "version_or_fingerprint": app_req["version_or_fingerprint"],
            "decision": "APROBAR_CON_EXCEPCION",
            "comment": "con excepcion",
            "idempotency_key": app_req["idempotency_key"],
        }
        actor = {
            "user_id": session_valid.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
        }
        c_exc, e_exc = session_valid.process_decision(cmd_exc, actor)
        self.assertEqual(c_exc, 1)
        self.assertEqual(e_exc["errors"][-1]["error_code"], "INVALID_INPUT")
        self.assertEqual(session_valid.approvals[0]["status"], "PENDIENTE")

    def test_cb12_cli_interactive_branches_simulated(self) -> None:
        """CB-12: CLI: contexto en stderr, un JSON en stdout, maneja EOF, SALIR, longitud y no-TTY."""
        # 1. Modo interactivo sin TTY produce PERMISSION_DENIED
        buf_out = io.StringIO()
        with redirect_stdout(buf_out):
            exit_code = demo_plan_review.main(["--interactive"])
        self.assertEqual(exit_code, 1)
        data = json.loads(buf_out.getvalue())
        self.assertEqual(data["errors"][0]["error_code"], "PERMISSION_DENIED")

        # 2. Simulacion interactiva con TTY mockeado: SALIR
        session = demo_plan_review.PlanReviewSession()
        session.init_from_intake(raw_data=self.base_fixture)

        buf_err = io.StringIO()
        with redirect_stderr(buf_err):
            with patch("sys.stdin.isatty", return_value=True), patch.object(sys.stderr, "isatty", return_value=True):
                with patch("sys.stdin.readline", return_value="SALIR\n"):
                    code_exit, env_exit = demo_plan_review.run_interactive_cli(session)
        self.assertEqual(code_exit, 3)
        self.assertEqual(session.approvals[0]["status"], "PENDIENTE")
        self.assertIn("REVISION LOCAL DE PLAN", buf_err.getvalue())

        # 3. Simulacion interactiva: APROBAR <huella>
        fp = session.approvals[0]["version_or_fingerprint"]
        buf_err2 = io.StringIO()
        with redirect_stderr(buf_err2):
            with patch("sys.stdin.isatty", return_value=True), patch.object(sys.stderr, "isatty", return_value=True):
                with patch("sys.stdin.readline", return_value=f"APROBAR {fp}\n"):
                    code_app, env_app = demo_plan_review.run_interactive_cli(session)
        self.assertEqual(code_app, 0)
        self.assertEqual(env_app["mission"]["current_state"], "AUTORIZADA_PARA_EJECUTAR")

    def test_cb13_no_network_no_subprocess_no_side_effects(self) -> None:
        """CB-13: Comprueba que no hay llamadas de red, subprocesos ni tareas ejecutadas."""
        session = demo_plan_review.PlanReviewSession()
        session.init_from_intake(raw_data=self.base_fixture)
        app_req = session.approvals[0]

        cmd = {
            "approval_id": app_req["approval_id"],
            "version_or_fingerprint": app_req["version_or_fingerprint"],
            "decision": "APROBAR",
            "comment": "aprobado",
            "idempotency_key": app_req["idempotency_key"],
        }
        actor = {
            "user_id": session.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
        }

        # Interceptar intentos de red o procesos
        with patch("socket.socket", side_effect=RuntimeError("Red no permitida")), patch(
            "subprocess.Popen", side_effect=RuntimeError("Subprocesos no permitidos")
        ):
            code, env = session.process_decision(cmd, actor)

        self.assertEqual(code, 0)
        self.assertEqual(env["mission"]["counters"]["task_reasoning_attempts"], 0)
        self.assertEqual(env["mission"]["counters"]["agent_requests"], 0)


class TestReviewCorrection(unittest.TestCase):
    """H1-H6: interacciones SIMULADAS; validadores y decisiones reales del demo."""

    setUp = TestDemoPlanReview.setUp

    def new_session(self, **kwargs):
        self.clock = [datetime(2026, 8, 30, 10, tzinfo=timezone.utc)]
        kwargs.setdefault("now_fn", lambda: self.clock[0])
        session = demo_plan_review.PlanReviewSession(**kwargs)
        code, env = session.init_from_intake(raw_data=self.base_fixture)
        self.assertEqual(code, 3)
        self.assertEqual(env["approvals"][0]["status"], "PENDIENTE")
        return session

    def command_actor(self, session, decision="APROBAR", comment=""):
        request = session.approvals[0]
        return ({"approval_id": request["approval_id"], "version_or_fingerprint": request["version_or_fingerprint"],
                 "decision": decision, "comment": comment, "idempotency_key": request["idempotency_key"]},
                {"user_id": session.mission["user_id"], "actor": "usuario_local_demo", "actor_role": "usuario_humano",
                 "source": "terminal_local_autorizada", "identity_scope": "IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA"})

    def snapshot(self, session):
        return (session.build_envelope(), copy.deepcopy(session.processed_idempotency_keys))

    def assert_records(self, env):
        self.assertEqual(env["simulation_status"], "SIMULADA")
        if env["mission"] is not None:
            self.mission_validator.validate(env["mission"])
            self.assertIsNone(env["mission"]["active_task"])
            self.assertEqual(env["mission"]["counters"]["agent_requests"], 0)
            self.assertEqual(env["mission"]["counters"]["task_reasoning_attempts"], 0)
        for key, validator in (("approvals", self.approval_validator), ("approval_history", self.approval_validator),
                               ("events", self.event_validator), ("checkpoints", self.checkpoint_validator),
                               ("errors", self.error_validator)):
            for record in env[key]:
                validator.validate(record)
        if env["plan"]:
            self.assertEqual([t["status"] for t in env["plan"]["tasks"]], ["PENDIENTE"] * 4)
        for cp in env["checkpoints"]:
            self.assertEqual(cp["budgets_consumed"]["budget_usd_spent"], 0)

    def assert_denied(self, session, command, actor, error="INVALID_INPUT", code=1):
        before = self.snapshot(session)
        actual, env = session.process_decision(command, actor)
        self.assertEqual(actual, code)
        self.assertEqual([e["error_code"] for e in env["errors"]], [error])
        self.assertIsNone(env["mission"])
        self.assertEqual(env["approvals"], [])
        self.assertEqual(env["checkpoints"], [])
        self.assert_records(env)
        self.assertEqual(self.snapshot(session), before)

    def test_h1_pending_decision_rejects_every_other_mission_state(self):
        for state in self.state_machine["mission_states"]:
            if state == "PLAN_EN_REVISION":
                continue
            with self.subTest(state=state):
                s = self.new_session()
                cmd, actor = self.command_actor(s)
                s.mission["current_state"] = state
                if state in ("BLOQUEADA", "PAUSADA"):
                    s.mission["resumable_state"] = "PLAN_EN_REVISION"
                self.assert_denied(s, cmd, actor)

    def test_h1_missing_and_crossed_references_owners_and_versions(self):
        cases = [
            (lambda s: s.mission["approval_refs"].append("ausente"), "NOT_FOUND", 2),
            (lambda s: s.mission.update(approval_refs=[]), "NOT_FOUND", 2),
            (lambda s: s.mission.update(last_checkpoint_id="ausente"), "NOT_FOUND", 2),
            (lambda s: s.approvals.clear(), "NOT_FOUND", 2),
            (lambda s: s.approvals[0].update(user_id="otro"), "PERMISSION_DENIED", 1),
            (lambda s: s.brief.update(user_id="otro"), "PERMISSION_DENIED", 1),
            (lambda s: s.plan.update(mission_id="otra"), "INVALID_INPUT", 1),
            (lambda s: s.plan.update(brief_version=2), "INVALID_INPUT", 1),
            (lambda s: s.plan.update(plan_version=2), "INVALID_INPUT", 1),
            (lambda s: s.mission.update(brief_version=2), "INVALID_INPUT", 1),
            (lambda s: s.mission.update(record_version=5), "INVALID_INPUT", 1),
            (lambda s: s.approvals[0].update(action_approved="otra mision"), "INVALID_INPUT", 1),
            (lambda s: s.approval_history[0].update(idempotency_key="otra"), "INVALID_INPUT", 1),
            (lambda s: s.events[-1].update(mission_id="otra"), "INVALID_INPUT", 1),
            (lambda s: s.events[-1].update(related_approval_id="ausente"), "NOT_FOUND", 2),
        ]
        for index, (mutate, error, code) in enumerate(cases):
            with self.subTest(case=index):
                s = self.new_session()
                cmd, actor = self.command_actor(s)
                mutate(s)
                self.assert_denied(s, cmd, actor, error, code)

    def test_h1_checkpoint_references_checked_even_before_idempotent_replay(self):
        cases = [
            (lambda s: s.mission.update(last_checkpoint_id="ausente"), "NOT_FOUND", 2),
            (lambda s: s.checkpoints[0].update(authorizations=["ausente"]), "NOT_FOUND", 2),
            (lambda s: s.checkpoints[0].update(mission_id="otra"), "INVALID_INPUT", 1),
            (lambda s: s.checkpoints[0].update(mission_version=4), "INVALID_INPUT", 1),
            (lambda s: s.checkpoints[0].update(artifacts=["brief", "otro_plan"]), "NOT_FOUND", 2),
            (lambda s: s.checkpoints[0]["tasks"][0].update(task_id="otra"), "INVALID_INPUT", 1),
            (lambda s: s.checkpoints[0].update(fingerprint="sha256:alterada"), "INVALID_INPUT", 1),
        ]
        for index, (mutate, error, code) in enumerate(cases):
            with self.subTest(case=index):
                s = self.new_session()
                cmd, actor = self.command_actor(s)
                self.assertEqual(s.process_decision(cmd, actor)[0], 0)
                mutate(s)
                self.assert_denied(s, cmd, actor, error, code)

    def test_h1_all_cb05_fingerprint_fields_reject_tampering(self):
        mutations = [
            lambda s: s.brief.update(context="Contexto diferente"),
            lambda s: s.plan["risks"].append("Riesgo nuevo"),
            lambda s: s.plan["tasks"][0].update(objective="Objetivo distinto"),
            lambda s: s.plan["tasks"][1].update(dependencies=[]),
            lambda s: s.plan["tasks"][0]["acceptance_criteria"].append("Otro criterio"),
            lambda s: s.plan["tasks"][0].update(allowed_tool_categories=["web"]),
            lambda s: s.plan["tasks"][0]["limits"].update(max_budget_usd=1),
            lambda s: s.plan["tasks"][0].update(expected_output="Otro entregable"),
            lambda s: s.approvals[0].update(version_or_fingerprint="sha256:otra"),
        ]
        for i, mutate in enumerate(mutations):
            with self.subTest(field=i):
                s = self.new_session()
                cmd, actor = self.command_actor(s)
                mutate(s)
                self.assert_denied(s, cmd, actor)

    def test_h2_transition_matrix_before_decision_and_expiration(self):
        for transition_id in ("MT-005", "AT-001", "AT-002"):
            for change in ("missing", "duplicate", "from", "to", "authority"):
                for expired in (False, True):
                    with self.subTest(transition=transition_id, change=change, expired=expired):
                        s = self.new_session()
                        s.state_machine = copy.deepcopy(s.state_machine)
                        rows = s.state_machine["mission_transitions"] if transition_id == "MT-005" else s.state_machine["approval_lifecycle"]["transitions"]
                        row = next(t for t in rows if t["id"] == transition_id)
                        if change == "missing":
                            rows.remove(row)
                        elif change == "duplicate":
                            rows.append(copy.deepcopy(row))
                        else:
                            row[change] = "incompatible"
                        if expired:
                            self.clock[0] += timedelta(seconds=301)
                        self.assert_denied(s, *self.command_actor(s), "SYSTEM_ERROR")

    def test_h2_strict_booleans_and_idempotency_policies(self):
        for value in (False, "false", "true", 0, 1, None, [], {}):
            with self.subTest(boolean=value):
                s = self.new_session()
                next(t for t in s.state_machine["mission_transitions"] if t["id"] == "MT-005")["requires_human_approval"] = value
                self.assert_denied(s, *self.command_actor(s), "SYSTEM_ERROR")
        for key, field, value in (("same_key_same_content", "action", "permitir"),
                                  ("same_key_different_content", "action", "no_second_effect"),
                                  ("same_key_different_content", "error_code", "SYSTEM_ERROR")):
            with self.subTest(policy=key, field=field):
                s = self.new_session()
                s.state_machine["idempotency_rules"][key][field] = value
                self.assert_denied(s, *self.command_actor(s), "SYSTEM_ERROR")

    def test_h4_atomic_faults_in_decision_checkpoint_and_expiration(self):
        for decision, failed_prefix in (("APROBAR", "EVT-APP-DECISION"), ("APROBAR", "CHK"),
                                       ("APROBAR", "IDEMP-CHK"), ("RECHAZAR", "EVT-APP-DECISION"),
                                       ("EXPIRAR", "EVT-APP-EXP"), ("EXPIRAR", "IDEMP-EVT-EXP")):
            with self.subTest(decision=decision, failure=failed_prefix):
                s = self.new_session()
                original_generator = s.id_generator
                # Inyeccion permitida de IDs: falla un schema real despues de preparar cambios.
                s.id_generator = lambda prefix: "" if prefix == failed_prefix else original_generator(prefix)
                cmd, actor = self.command_actor(s, "RECHAZAR" if decision == "RECHAZAR" else "APROBAR", "Motivo")
                if decision == "EXPIRAR":
                    self.clock[0] += timedelta(seconds=300)
                self.assert_denied(s, cmd, actor, "SYSTEM_ERROR")
                self.assertEqual(s.approvals[0]["status"], "PENDIENTE")
                self.assertEqual(s.mission["record_version"], 4)
                self.assertEqual(len(s.events), 4)
                self.assertEqual(s.processed_idempotency_keys, {})

    def test_h4_initialization_fault_is_atomic(self):
        for prefix in ("APP", "EVT-APP-REQ"):
            with self.subTest(prefix=prefix):
                s = demo_plan_review.PlanReviewSession(id_generator=lambda p: "" if p == prefix else p)
                before = self.snapshot(s)
                code, env = s.init_from_intake(raw_data=self.base_fixture)
                self.assertEqual(code, 1)
                self.assertEqual(env["errors"][0]["error_code"], "SYSTEM_ERROR")
                self.assertEqual(self.snapshot(s), before)
                self.assert_records(env)

    def test_h4_expiration_before_at_and_after_boundary(self):
        for seconds, expected in ((299.999, 0), (300, 1), (300.001, 1)):
            with self.subTest(seconds=seconds):
                s = self.new_session()
                cmd, actor = self.command_actor(s)
                self.clock[0] += timedelta(seconds=seconds)
                code, env = s.process_decision(cmd, actor)
                self.assertEqual(code, expected)
                self.assert_records(env)
                self.assertEqual(env["mission"]["record_version"], 5)
                self.assertEqual(len(env["events"]), 5)
                if expected:
                    self.assertEqual(env["errors"][0]["error_code"], "PERMISSION_DENIED")
                    self.assertEqual(env["approvals"][0]["status"], "EXPIRADA")
                    self.assertEqual(env["mission"]["current_state"], "PLAN_EN_REVISION")
                    self.assertEqual(env["checkpoints"], [])
                    self.assert_denied(s, cmd, actor, "PERMISSION_DENIED")
                else:
                    self.assertEqual(env["approvals"][0]["decision"], "APROBAR")

    def test_h4_full_idempotent_result_context_check_and_session_isolation(self):
        for decision, expected in (("APROBAR", 0), ("RECHAZAR", 3), ("SOLICITAR_CAMBIOS", 3)):
            with self.subTest(decision=decision):
                s = self.new_session()
                cmd, actor = self.command_actor(s, decision, "Motivo")
                result = s.process_decision(cmd, actor)
                self.assertEqual(result[0], expected)
                before = self.snapshot(s)
                self.clock[0] += timedelta(seconds=500)
                duplicate = s.process_decision(cmd, actor)
                self.assertEqual(duplicate, result)
                self.assertEqual(self.snapshot(s), before)
                duplicate[1]["approvals"][0]["comment"] = "alterado"
                self.assertEqual(self.snapshot(s), before)
                self.assertEqual(s.process_decision(cmd, actor), result)
                self.assert_denied(s, dict(cmd, comment="conflicto"), actor)
                self.assert_denied(s, dict(cmd, idempotency_key="otra"), actor, "PERMISSION_DENIED")
                self.assert_denied(s, cmd, dict(actor, user_id="otro"), "PERMISSION_DENIED")
                self.assert_denied(s, cmd, dict(actor, source="agente"), "PERMISSION_DENIED")
                self.assert_denied(s, cmd, dict(actor, identity_scope="otro_contexto"))
                other = self.new_session()
                self.assertNotEqual(s.mission["mission_id"], other.mission["mission_id"])
                self.assert_denied(other, cmd, actor, "NOT_FOUND", 2)
                self.assertEqual(other.processed_idempotency_keys, {})

    def test_h5_exact_command_fields_types_lengths_and_request_key(self):
        s = self.new_session()
        cmd, actor = self.command_actor(s)
        for field in cmd:
            with self.subTest(missing=field):
                bad = dict(cmd)
                del bad[field]
                self.assert_denied(s, bad, actor)
            for value in (None, False, 1, [], {}, "x" * 4001):
                with self.subTest(field=field, value_type=type(value).__name__):
                    self.assert_denied(s, dict(cmd, **{field: value}), actor)
        for key in (42, None, "actor_role", "approved", "internal_reasoning"):
            with self.subTest(extra_key=key):
                bad = dict(cmd)
                bad[key] = "SYNTHETIC_TEST_SENTINEL"
                self.assert_denied(s, bad, actor)
        self.assert_denied(s, dict(cmd, idempotency_key="otra"), actor)
        for decision in ("RECHAZAR", "SOLICITAR_CAMBIOS"):
            for comment in ("", "   ", None):
                with self.subTest(decision=decision, comment=comment):
                    self.assert_denied(s, dict(cmd, decision=decision, comment=comment), actor)
        code, env = s.process_decision(dict(cmd, comment="x" * 4000), actor)
        self.assertEqual(code, 0)
        self.assertEqual(len(env["approvals"][0]["comment"]), 4000)

    def test_h6_real_default_and_advancing_injected_monotonic_clock(self):
        s = self.new_session()
        self.assertIs(s.monotonic_time_fn, demo_plan_review.time.monotonic)
        ticks = iter((100.0, 112.75))
        s = self.new_session(monotonic_time_fn=lambda: next(ticks))
        code, env = s.process_decision(*self.command_actor(s))
        self.assertEqual(code, 0)
        self.assertEqual(env["checkpoints"][0]["budgets_consumed"]["elapsed_mission_seconds"], 12.75)
        self.assert_records(env)

    def terminal_exchange(self, session, lines, check_context=False):
        stderr = io.StringIO()
        reads = []
        test = self

        class Terminal(io.StringIO):
            def isatty(self):
                return True

            def readline(self, size=-1):
                test.assertGreater(size, 0, "La lectura debe estar acotada desde el inicio")
                test.assertLessEqual(size, 4097)
                reads.append(size)
                if check_context:
                    text = stderr.getvalue()
                    for label, expected in (("Mision", session.mission), ("Brief completo", session.brief), ("Plan completo", session.plan)):
                        test.assertIn(label + ":\n", text)
                        actual = text.split(label + ":\n", 1)[1].splitlines()[0]
                        test.assertEqual(json.loads(actual), expected)
                    test.assertIn(session.approvals[0]["approval_id"], text)
                    test.assertIn(session.approvals[0]["version_or_fingerprint"], text)
                    test.assertIn(session.approvals[0]["expiration"], text)
                    test.assertIn("IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA", text)
                    test.assertIn("Ninguna tarea sera ejecutada", text)
                    test.assertNotIn("\x1b", text)
                    test.assertNotIn("\x85", text)
                value = lines.pop(0) if lines else ""
                if isinstance(value, BaseException):
                    raise value
                # La frontera simulada respeta el limite solicitado al sistema.
                return value[:size]

        stdout = io.StringIO()
        with patch.object(sys, "stdin", Terminal()), redirect_stderr(stderr), redirect_stdout(stdout), patch.object(stderr, "isatty", return_value=True):
            result = demo_plan_review.run_interactive_cli(session)
        self.assertEqual(stdout.getvalue(), "")
        self.assert_records(result[1])
        return result, reads, stderr.getvalue()

    def test_h3_full_safe_context_before_first_read(self):
        self.base_fixture["context"] = "Contexto con control \x1b[31m y \x85 de prueba"
        self.base_fixture["plan_template"]["tasks"][0]["expected_output"] = "Entregable con \x1b[2J"
        s = self.new_session()
        before = self.snapshot(s)
        result, reads, stderr = self.terminal_exchange(s, ["SALIR\n"], check_context=True)
        self.assertEqual(result[0], 3)
        self.assertEqual(reads, [4097])
        self.assertEqual(s.approvals, before[0]["approvals"])
        self.assertEqual(s.events, before[0]["events"])

    def test_h5_eof_and_interrupt_at_decision_or_comment(self):
        for at_comment in (False, True):
            for ending in ("", EOFError(), KeyboardInterrupt()):
                with self.subTest(comment=at_comment, ending=type(ending).__name__):
                    s = self.new_session()
                    lines = [ending]
                    if at_comment:
                        lines.insert(0, "RECHAZAR " + s.approvals[0]["version_or_fingerprint"] + "\n")
                    before = self.snapshot(s)
                    result, reads, _ = self.terminal_exchange(s, lines)
                    self.assertEqual(result[0], 3)
                    self.assertEqual(len(reads), 2 if at_comment else 1)
                    self.assertEqual(s.approvals, before[0]["approvals"])
                    self.assertEqual(s.mission, before[0]["mission"])
                    self.assertEqual(s.events, before[0]["events"])
                    self.assertEqual(s.checkpoints, [])
                    self.assertEqual(s.processed_idempotency_keys, {})

    def test_h5_bounded_line_and_comment_limits_exact_and_exceeded(self):
        for length, expected in ((4096, 0), (4097, 1), (100000, 1)):
            with self.subTest(line_length=length):
                s = self.new_session()
                command = "APROBAR " + s.approvals[0]["version_or_fingerprint"]
                line = command + " " * (length - len(command) - 1) + "\n"
                result, reads, _ = self.terminal_exchange(s, [line])
                self.assertEqual(result[0], expected)
                self.assertEqual(reads, [4097])
                if expected:
                    self.assertEqual(result[1]["errors"][-1]["error_code"], "INVALID_INPUT")
                    self.assertEqual(s.approvals[0]["status"], "PENDIENTE")
                    self.assertEqual(s.mission["record_version"], 4)
                    self.assertEqual(s.processed_idempotency_keys, {})
        for length, expected in ((4000, 3), (4001, 1), (4097, 1), (100000, 1)):
            with self.subTest(comment_length=length):
                s = self.new_session()
                command = "RECHAZAR " + s.approvals[0]["version_or_fingerprint"] + "\n"
                result, reads, _ = self.terminal_exchange(s, [command, "x" * length + "\n"])
                self.assertEqual(result[0], expected)
                self.assertEqual(reads, [4097, 4097])
                if expected == 1:
                    self.assertEqual(result[1]["errors"][-1]["error_code"], "INVALID_INPUT")
                    self.assertEqual(s.approvals[0]["status"], "PENDIENTE")
                    self.assertEqual(s.mission["record_version"], 4)
                    self.assertEqual(s.processed_idempotency_keys, {})
                else:
                    self.assertEqual(len(s.approvals[0]["comment"]), 4000)

    def test_h5_cli_rejects_unknown_syntax_and_wrong_fingerprint(self):
        for command in ("", "\n", "si\n", "aprobar sha256:otra\n", "APROBAR sha256:otra\n", "SALIR extra\n"):
            with self.subTest(command=command):
                s = self.new_session()
                result, reads, _ = self.terminal_exchange(s, [command])
                self.assertEqual(result[0], 3 if command == "" else 1)
                if command:
                    self.assertEqual(result[1]["errors"][-1]["error_code"], "INVALID_INPUT")
                self.assertEqual(s.approvals[0]["status"], "PENDIENTE")
                self.assertEqual(s.mission["record_version"], 4)
                self.assertEqual(len(s.events), 4)
                self.assertEqual(s.processed_idempotency_keys, {})

    def call_main(self, argv, stdin=None, module=demo_plan_review):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr), patch.object(sys, "stdin", stdin or io.StringIO()):
            code = module.main(argv)
        env = json.loads(stdout.getvalue())
        self.assert_records(env)
        return code, env, stderr.getvalue()

    def test_h5_default_never_reads_no_tty_and_unknown_arguments(self):
        class NeverRead(io.StringIO):
            def readline(self, size=-1):
                raise AssertionError("No debe leer stdin")

        code, env, stderr = self.call_main([], NeverRead())
        self.assertEqual(code, 3)
        self.assertEqual(env["approvals"][0]["status"], "PENDIENTE")
        self.assertEqual(stderr, "")
        code, env, _ = self.call_main(["--interactive"], NeverRead())
        self.assertEqual(code, 1)
        self.assertEqual(env["errors"][-1]["error_code"], "PERMISSION_DENIED")
        self.assertEqual(env["approvals"][0]["status"], "PENDIENTE")
        for args in (["--approve"], ["--yes"], ["--interactive", "--yes"], ["--interactive", "--interactive"], ["otra.json"]):
            with self.subTest(args=args):
                code, env, stderr = self.call_main(args, NeverRead())
                self.assertEqual(code, 1)
                self.assertEqual(env["errors"][0]["error_code"], "INVALID_INPUT")
                self.assertEqual(env["approvals"], [])
                self.assertIsNone(env["mission"])

    def test_h3_h5_complete_interactive_cli_uses_request_key(self):
        for decision in ("APROBAR", "RECHAZAR", "SOLICITAR_CAMBIOS"):
            with self.subTest(decision=decision):
                stdout, stderr = io.StringIO(), io.StringIO()
                read_sizes = []
                test = self

                class Terminal(io.StringIO):
                    def isatty(self):
                        return True

                    def readline(self, size=-1):
                        test.assertEqual(size, 4097)
                        read_sizes.append(size)
                        context = stderr.getvalue()
                        test.assertIn("Brief completo:", context)
                        test.assertIn("Plan completo:", context)
                        if len(read_sizes) == 1:
                            fp = context.split("Huella exacta:  ")[1].splitlines()[0]
                            return decision + " " + fp + "\n"
                        return "Motivo SIMULADA con Unicode: \u00e1\n"

                with redirect_stdout(stdout), redirect_stderr(stderr), patch.object(stderr, "isatty", return_value=True), patch.object(sys, "stdin", Terminal()):
                    code = demo_plan_review.main(["--interactive"])
                env = json.loads(stdout.getvalue())
                self.assertEqual(code, 0 if decision == "APROBAR" else 3)
                self.assert_records(env)
                self.assertEqual(env["approvals"][0]["decision"], decision)
                self.assertEqual(env["events"][-1]["idempotency_key"], env["approval_history"][0]["idempotency_key"])
                self.assertEqual(len(read_sizes), 1 if decision == "APROBAR" else 2)

    def fresh_module(self, name="plan_review_probe"):
        spec = importlib.util.spec_from_file_location(name, demo_plan_review.__file__)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_h4_dependency_absent_and_contract_io_errors_are_json(self):
        with patch.dict(sys.modules, {"jsonschema": None}):
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                module = self.fresh_module()
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(stderr.getvalue(), "")
            code, env, stderr = self.call_main([], module=module)
            self.assertEqual(code, 1)
            self.assertEqual(env["errors"][0]["error_code"], "SYSTEM_ERROR")
            self.assertIn("no se realizo validacion", env["errors"][0]["message"])
            self.assertEqual(env["approvals"], [])
            with redirect_stdout(io.StringIO()) as out, redirect_stderr(io.StringIO()) as err, patch.object(sys, "argv", ["app.demo_plan_review"]):
                with self.assertRaises(SystemExit) as raised:
                    self.fresh_module("__main__")
            self.assertEqual(raised.exception.code, 1)
            self.assertEqual(err.getvalue(), "")
            self.assertEqual(json.loads(out.getvalue())["errors"][0]["error_code"], "SYSTEM_ERROR")
        original_open = builtins.open
        for fault, code, category in ((FileNotFoundError("SYNTHETIC_TEST_SENTINEL"), 2, "NOT_FOUND"),
                                       (PermissionError("SYNTHETIC_TEST_SENTINEL"), 1, "SYSTEM_ERROR")):
            with self.subTest(error=type(fault).__name__):
                def fail_contract(file, *args, **kwargs):
                    if Path(file).name == "approval.schema.json":
                        raise fault
                    return original_open(file, *args, **kwargs)
                with patch("builtins.open", side_effect=fail_contract):
                    actual, env, stderr = self.call_main([])
                self.assertEqual(actual, code)
                self.assertEqual(env["errors"][0]["error_code"], category)
                self.assertNotIn("SYNTHETIC_TEST_SENTINEL", json.dumps(env))
                self.assertEqual(env["approvals"], [])
                self.assertEqual(stderr, "")

    @contextmanager
    def prohibit_effects(self):
        attempts = []

        def forbidden(*args, **kwargs):
            attempts.append("efecto_prohibido")
            raise AssertionError("Efecto prohibido interceptado")

        def read_only(original):
            def guarded(file, mode="r", *args, **kwargs):
                if any(flag in mode for flag in "wax+"):
                    return forbidden()
                return original(file, mode, *args, **kwargs)
            return guarded

        original_os_open = os.open

        def guarded_os_open(path, flags, *args, **kwargs):
            if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
                return forbidden()
            return original_os_open(path, flags, *args, **kwargs)

        with ExitStack() as stack:
            for target in ("socket.socket", "socket.create_connection", "socket.getaddrinfo", "urllib.request.urlopen",
                           "subprocess.Popen", "subprocess.run", "os.system", "os.popen", "os.mkdir", "os.remove",
                           "os.unlink", "os.rename", "os.replace", "os.rmdir"):
                stack.enter_context(patch(target, side_effect=forbidden))
            for name in ("startfile", "spawnl", "spawnle", "spawnv", "spawnve", "execv", "execve", "fork", "posix_spawn"):
                if hasattr(os, name):
                    stack.enter_context(patch.object(os, name, side_effect=forbidden))
            stack.enter_context(patch("builtins.open", side_effect=read_only(builtins.open)))
            stack.enter_context(patch("io.open", side_effect=read_only(io.open)))
            stack.enter_context(patch("os.open", side_effect=guarded_os_open))
            yield attempts

    def test_h4_no_attempted_network_writes_processes_or_tasks(self):
        with self.prohibit_effects() as attempts:
            with redirect_stdout(io.StringIO()) as out, redirect_stderr(io.StringIO()) as err:
                module = self.fresh_module()
            self.assertEqual(out.getvalue(), "")
            self.assertEqual(err.getvalue(), "")
            self.assertEqual(self.call_main([], module=module)[0], 3)
            for decision in ("APROBAR", "RECHAZAR", "SOLICITAR_CAMBIOS", "EXPIRAR", "INVALIDA"):
                s = self.new_session()
                cmd, actor = self.command_actor(s, "APROBAR" if decision == "EXPIRAR" else decision, "Motivo")
                if decision == "EXPIRAR":
                    self.clock[0] += timedelta(seconds=301)
                code, env = s.process_decision(cmd, actor)
                self.assertEqual(code, {"APROBAR": 0, "RECHAZAR": 3, "SOLICITAR_CAMBIOS": 3, "EXPIRAR": 1, "INVALIDA": 1}[decision])
                self.assert_records(env)
                self.assertNotEqual(s.mission["current_state"], "EN_EJECUCION")
                self.assertEqual([t["status"] for t in s.plan["tasks"]], ["PENDIENTE"] * 4)
            with patch.dict(sys.modules, {"jsonschema": None}):
                unavailable = self.fresh_module()
                self.assertEqual(self.call_main([], module=unavailable)[0], 1)
        # Tambien falla si la aplicacion capturo la excepcion del intento prohibido.
        self.assertEqual(attempts, [])


if __name__ == "__main__":
    unittest.main()
