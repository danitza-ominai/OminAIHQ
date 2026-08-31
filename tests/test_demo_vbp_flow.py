"""Pruebas exhaustivas para el recorrido completo Mision a VBP SIMULADA (PZ-003F).

Valida el happy path end-to-end con ambas puertas humanas (Plan y VBP),
detencion en cada puerta por defecto, manejo de rechazos, integridad de huellas
y exportacion del Markdown canonico final con estado FINALIZADA.
"""

import copy
import json
import unittest
from pathlib import Path

import app.demo_vbp_flow as demo_vbp_flow

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FIXTURE_PATH = PROJECT_ROOT / "examples" / "demo_mission.json"


class TestDemoVBPFlow(unittest.TestCase):
    """Suite de pruebas para el recorrido completo SIMULADA PZ-003F."""

    def setUp(self) -> None:
        with open(DEFAULT_FIXTURE_PATH, "r", encoding="utf-8") as f:
            self.fixture = json.load(f)

    def test_ac01_full_happy_path_with_both_human_gates(self) -> None:
        """AC-01: Happy path SIMULADA completo con ambas puertas hasta FINALIZADA y Markdown exportado."""
        runner = demo_vbp_flow.CompleteVBPFlowRunner()

        # 1. Intake -> PLAN_EN_REVISION
        code1, env1 = runner.init_flow(raw_data=self.fixture)
        self.assertEqual(code1, 3)
        self.assertEqual(env1["mission"]["current_state"], "PLAN_EN_REVISION")
        self.assertEqual(len(env1["approvals"]), 1)
        self.assertEqual(env1["approvals"][0]["status"], "PENDIENTE")

        # 2. Puerta 1: Decision humana sobre el plan (APROBAR)
        plan_app_req = env1["approvals"][0]
        cmd1 = {
            "approval_id": plan_app_req["approval_id"],
            "version_or_fingerprint": plan_app_req["version_or_fingerprint"],
            "decision": "APROBAR",
            "comment": "Plan conforme",
            "idempotency_key": plan_app_req["idempotency_key"],
        }
        actor = {
            "user_id": env1["mission"]["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
            "identity_scope": "IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA",
        }
        code2, env2 = runner.process_plan_decision(cmd1, actor)
        self.assertEqual(code2, 0)
        self.assertEqual(env2["mission"]["current_state"], "AUTORIZADA_PARA_EJECUTAR")

        # 3. Ejecucion de tareas y ensamblaje de VBP -> VBP_EN_REVISION (Puerta 2)
        code3, env3 = runner.execute_tasks_and_assemble_vbp()
        self.assertEqual(code3, 3)
        self.assertEqual(env3["mission"]["current_state"], "VBP_EN_REVISION")
        self.assertEqual(env3["evaluation_report"]["verdict"], "PASA")
        self.assertIsNotNone(runner.vbp_approval_req)
        self.assertEqual(runner.vbp_approval_req["status"], "PENDIENTE")

        # 4. Puerta 2: Decision humana sobre el VBP (APROBAR)
        vbp_app_req = runner.vbp_approval_req
        cmd2 = {
            "approval_id": vbp_app_req["approval_id"],
            "version_or_fingerprint": vbp_app_req["version_or_fingerprint"],
            "decision": "APROBAR",
            "comment": "VBP final formalmente aprobado",
            "idempotency_key": vbp_app_req["idempotency_key"],
        }
        code4, env4 = runner.process_vbp_decision(cmd2, actor)
        self.assertEqual(code4, 0)
        self.assertEqual(env4["mission"]["current_state"], "FINALIZADA")
        self.assertEqual(env4["vbp_data"]["approval_status"], "APROBADO")
        self.assertEqual(env4["vbp_data"]["human_approval_ref"], vbp_app_req["approval_id"])

        # Verificar que el Markdown canonico contiene el manifest y las 18 secciones
        md = env4["canonical_markdown"]
        self.assertIn("# Venture Build Package", md)
        self.assertIn("## 1. Mision", md)
        self.assertIn("## 18. Historial de trazabilidad", md)
        self.assertIn(vbp_app_req["approval_id"], md)

    def test_ac02_default_inspection_stops_at_each_gate(self) -> None:
        """AC-02: Por defecto el flujo se detiene en cada puerta sin avanzar indebidamente."""
        runner = demo_vbp_flow.CompleteVBPFlowRunner()

        # Detencion en Puerta 1
        code, env = runner.init_flow(raw_data=self.fixture)
        self.assertEqual(code, 3)
        self.assertEqual(env["mission"]["current_state"], "PLAN_EN_REVISION")
        self.assertIsNone(runner.vbp_data)

    def test_ac03_vbp_rejection_flow(self) -> None:
        """AC-03: Rechazo del VBP en Puerta 2 transiciona a VBP_RECHAZADO con motivo y sin pasar a FINALIZADA."""
        runner = demo_vbp_flow.CompleteVBPFlowRunner()
        runner.init_flow(raw_data=self.fixture)

        # Aprobar plan
        plan_app = runner.plan_session.approvals[0]
        cmd1 = {
            "approval_id": plan_app["approval_id"],
            "version_or_fingerprint": plan_app["version_or_fingerprint"],
            "decision": "APROBAR",
            "comment": "OK",
            "idempotency_key": plan_app["idempotency_key"],
        }
        actor = {
            "user_id": runner.plan_session.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
            "identity_scope": "IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA",
        }
        runner.process_plan_decision(cmd1, actor)
        runner.execute_tasks_and_assemble_vbp()

        # Rechazar VBP con motivo
        vbp_app = runner.vbp_approval_req
        cmd_rej = {
            "approval_id": vbp_app["approval_id"],
            "version_or_fingerprint": vbp_app["version_or_fingerprint"],
            "decision": "RECHAZAR",
            "comment": "Falta incluir analisis de competidor X",
            "idempotency_key": vbp_app["idempotency_key"],
        }
        code, env = runner.process_vbp_decision(cmd_rej, actor)
        self.assertEqual(code, 0)
        self.assertEqual(env["mission"]["current_state"], "VBP_RECHAZADO")
        self.assertEqual(env["vbp_data"]["approval_status"], "RECHAZADO")

    def test_ac04_fingerprint_mismatch_at_vbp_gate(self) -> None:
        """AC-04: Huella alterada en la solicitud de decision del VBP es rechazada."""
        runner = demo_vbp_flow.CompleteVBPFlowRunner()
        runner.init_flow(raw_data=self.fixture)

        plan_app = runner.plan_session.approvals[0]
        cmd1 = {
            "approval_id": plan_app["approval_id"],
            "version_or_fingerprint": plan_app["version_or_fingerprint"],
            "decision": "APROBAR",
            "comment": "OK",
            "idempotency_key": plan_app["idempotency_key"],
        }
        actor = {
            "user_id": runner.plan_session.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
            "identity_scope": "IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA",
        }
        runner.process_plan_decision(cmd1, actor)
        runner.execute_tasks_and_assemble_vbp()

        # Comando con huella incorrecta
        bad_cmd = {
            "approval_id": runner.vbp_approval_req["approval_id"],
            "version_or_fingerprint": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
            "decision": "APROBAR",
            "comment": "OK",
            "idempotency_key": runner.vbp_approval_req["idempotency_key"],
        }
        code, env = runner.process_vbp_decision(bad_cmd, actor)
        self.assertEqual(code, 1)
        self.assertEqual(env["mission"]["current_state"], "VBP_EN_REVISION")

    def test_ac05_cli_entrypoint(self) -> None:
        """AC-05: El punto de entrada CLI ejecuta e imprime JSON estructurado con retorno 3 por defecto."""
        code = demo_vbp_flow.main(argv=[])
        self.assertEqual(code, 3)


if __name__ == "__main__":
    unittest.main()
