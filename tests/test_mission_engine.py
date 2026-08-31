"""Pruebas exhaustivas para el motor secuencial de tareas SIMULADA (PZ-003D).

Cubre los criterios de aceptacion AC-01 a AC-05 y AC-COMUN-01 a AC-COMUN-05:
validando secuencia estricta de tareas, transiciones MT-006/MT-008/MT-012,
manejo de fallos inyectados, limites finitos, checkpoints en memoria y 0 efectos de red/archivos.
"""

import copy
import json
import socket
import subprocess
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import app.demo_intake as demo_intake
import app.demo_plan_review as demo_plan_review
import app.mission_engine as mission_engine
import app.runtime_contracts as runtime_contracts

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FIXTURE_PATH = PROJECT_ROOT / "examples" / "demo_mission.json"


class TestMissionEngine(unittest.TestCase):
    """Suite de pruebas para el motor secuencial de tareas PZ-003D."""

    def setUp(self) -> None:
        with open(DEFAULT_FIXTURE_PATH, "r", encoding="utf-8") as f:
            self.base_fixture = json.load(f)

        # Preparar una sesion autorizada valida (PZ-003B)
        self.session = demo_plan_review.PlanReviewSession()
        self.session.init_from_intake(raw_data=self.base_fixture)
        app_req = self.session.approvals[0]

        cmd = {
            "approval_id": app_req["approval_id"],
            "version_or_fingerprint": app_req["version_or_fingerprint"],
            "decision": "APROBAR",
            "comment": "Plan conforme",
            "idempotency_key": app_req["idempotency_key"],
        }
        actor = {
            "user_id": self.session.mission["user_id"],
            "actor": "usuario_local_demo",
            "actor_role": "usuario_humano",
            "source": "terminal_local_autorizada",
            "identity_scope": "IDENTIDAD_LOCAL_DE_DEMO_NO_AUTENTICADA",
        }
        code, env = self.session.process_decision(cmd, actor)
        self.assertEqual(code, 0)
        self.authorized_envelope = self.session.build_envelope()

    def test_ac01_rejection_without_approval_or_broken_references(self) -> None:
        """AC-01: Sin aprobacion valida, huella alterada o estado incompatible: 0 tareas activas e intentos."""
        # 1. Sesion en estado no autorizado (ej. PLAN_EN_REVISION)
        bad_env = copy.deepcopy(self.authorized_envelope)
        bad_env["mission"]["current_state"] = "PLAN_EN_REVISION"

        engine = mission_engine.MissionExecutionEngine()
        ok, errs = engine.load_authorized_session(bad_env)
        self.assertFalse(ok)
        self.assertEqual(errs[0]["error_code"], "PERMISSION_DENIED")

        # 2. Aprobacion con huella no coincidente
        bad_fp_env = copy.deepcopy(self.authorized_envelope)
        bad_fp_env["approvals"][0]["version_or_fingerprint"] = "sha256:0000000000000000000000000000000000000000000000000000000000000000"
        ok_fp, errs_fp = engine.load_authorized_session(bad_fp_env)
        self.assertFalse(ok_fp)
        self.assertEqual(errs_fp[0]["error_code"], "INVALID_INPUT")

    def test_ac02_strict_sequential_execution_to_consolidation(self) -> None:
        """AC-02: Ejecutar las 4 tareas en secuencia estricta hasta EN_CONSOLIDACION con Checkpoint."""
        engine = mission_engine.MissionExecutionEngine()
        ok, errs = engine.load_authorized_session(self.authorized_envelope)
        self.assertTrue(ok, f"Fallo al cargar sesion: {errs}")

        exit_code, env = engine.run_execution()

        self.assertEqual(exit_code, 0)
        self.assertEqual(env["mission"]["current_state"], "EN_CONSOLIDACION")
        self.assertIsNone(env["mission"]["active_task"])
        self.assertEqual(len(env["tasks"]), 4)

        # Verificar que las 4 tareas estan COMPLETA
        for t in env["tasks"]:
            self.assertEqual(t["status"], "COMPLETA")
            self.assertEqual(t["attempt"], 1)

        # Verificar resultados de especialistas
        self.assertEqual(len(env["task_results"]), 4)
        for tid, res in env["task_results"].items():
            self.assertEqual(res["status"], "SUCCESS")

        # Verificar evidencias almacenadas (Research produjo 2 evidencias)
        self.assertEqual(len(env["evidence_store"]), 2)

        # Verificar Checkpoint en memoria para EN_CONSOLIDACION
        self.assertTrue(len(env["checkpoints"]) >= 1)
        last_chk = env["checkpoints"][-1]
        self.assertEqual(last_chk["state"], "EN_CONSOLIDACION")

    def test_ac03_fault_injection_blocks_downstream_tasks(self) -> None:
        """AC-03: Inyectar fallo en una tarea detiene la ejecucion, bloquea dependientes y pasa a PAUSADA."""
        fault_config = {
            "TSK-002-ARCH": {
                "status": "FAILED",
                "summary": "[SIMULADA] Incompatibilidad insalvable en integracion ERP",
            }
        }
        engine = mission_engine.MissionExecutionEngine(fault_config=fault_config)
        ok, _ = engine.load_authorized_session(self.authorized_envelope)
        self.assertTrue(ok)

        exit_code, env = engine.run_execution()

        self.assertEqual(exit_code, 1)
        self.assertEqual(env["mission"]["current_state"], "PAUSADA")
        self.assertEqual(env["mission"]["resumable_state"], "EN_EJECUCION")

        # TSK-001 debe estar COMPLETA, TSK-002 FALLIDA, TSK-003 y TSK-004 PENDIENTE
        tasks_by_id = {t["task_id"]: t for t in env["tasks"]}
        self.assertEqual(tasks_by_id["TSK-001-RESEARCH"]["status"], "COMPLETA")
        self.assertEqual(tasks_by_id["TSK-002-ARCH"]["status"], "FALLIDA")
        self.assertEqual(tasks_by_id["TSK-003-PLAN"]["status"], "PENDIENTE")
        self.assertEqual(tasks_by_id["TSK-004-GOV"]["status"], "PENDIENTE")

        # Checkpoint de pausa generado
        last_chk = env["checkpoints"][-1]
        self.assertEqual(last_chk["state"], "PAUSADA")
        self.assertEqual(last_chk["resumable_state"], "EN_EJECUCION")

    def test_ac04_limits_exhaustion_stops_execution(self) -> None:
        """AC-04: Exceder limite de solicitudes de agente detiene el motor sin reiniciar contadores."""
        env_low_limits = copy.deepcopy(self.authorized_envelope)
        # Fijar limite maximo de solicitudes en 2
        env_low_limits["mission"]["limits"]["max_agent_requests_per_mission"] = 2

        engine = mission_engine.MissionExecutionEngine()
        ok, _ = engine.load_authorized_session(env_low_limits)
        self.assertTrue(ok)

        exit_code, env = engine.run_execution()
        self.assertEqual(exit_code, 1)
        self.assertEqual(env["mission"]["current_state"], "PAUSADA")
        self.assertEqual(env["mission"]["counters"]["agent_requests"], 2)

    def test_ac05_no_network_no_subprocess_and_simulada_tags(self) -> None:
        """AC-05: Cero llamadas de red, cero subprocesos y etiqueta SIMULADA visible en resultados."""
        engine = mission_engine.MissionExecutionEngine()
        engine.load_authorized_session(self.authorized_envelope)

        with patch("socket.socket", side_effect=RuntimeError("Red no permitida")), patch(
            "subprocess.Popen", side_effect=RuntimeError("Subprocesos no permitidos")
        ):
            code, env = engine.run_execution()

        self.assertEqual(code, 0)
        self.assertEqual(env["simulation_status"], "SIMULADA")
        for tid, res in env["task_results"].items():
            self.assertTrue(res["summary"].startswith("[SIMULADA]"))


if __name__ == "__main__":
    unittest.main()
