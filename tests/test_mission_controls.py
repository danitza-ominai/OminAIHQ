"""Pruebas exhaustivas para Controles de Mision (PZ-012B).

Valida transiciones de pausa/cancelacion/reanudacion, inmutabilidad de estados terminales,
rechazo de cancelacion por agentes sin rol humano, bloqueo de reanudacion por limites o falta de evidencia,
idempotencia de controles y versionado de cambios de alcance.
"""

import tempfile
import unittest
from pathlib import Path

import app.hq_runtime as hq_runtime
import app.local_repository as local_repository
import app.mission_controls as mission_controls
import app.recovery as recovery
import app.runtime_config as runtime_config


class TestMissionControls(unittest.TestCase):
    """Suite de pruebas para PZ-012B (Mission Controls)."""

    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.db_path = str(Path(self.tmp_dir.name) / "test_controls.db")
        self.repo = local_repository.LocalRepository(db_path=self.db_path)
        self.config = runtime_config.RuntimeConfig(max_budget_usd=25.0)
        self.recovery = recovery.RecoveryManager(repository=self.repo, config=self.config)
        self.manager = mission_controls.MissionControlManager(
            repository=self.repo,
            recovery_mgr=self.recovery,
            config=self.config,
        )
        self.runtime = hq_runtime.HQRuntime(
            repository=self.repo,
            recovery_manager=self.recovery,
            controls_manager=self.manager,
        )

    def tearDown(self) -> None:
        try:
            self.runtime.repository.close()
        except Exception:
            pass
        try:
            self.repo.close()
        except Exception:
            pass
        try:
            self.tmp_dir.cleanup()
        except Exception:
            pass

    def test_ac01_pause_and_cancel_in_non_terminal_and_terminal_immutability(self) -> None:
        """AC-01: Pausar y cancelar en estados no terminales; estados terminales rechazan transiciones."""
        # 1. Crear mision en BORRADOR y pausar
        self.repo.save_mission({
            "mission_id": "MSN-CTRL-001",
            "status": "BORRADOR",
            "version": 1,
        })

        ok_pause, p_rec, _ = self.manager.pause_mission("MSN-CTRL-001", reason="Revision de costos")
        self.assertTrue(ok_pause)
        self.assertEqual(p_rec["status"], "PAUSADA")
        self.assertEqual(p_rec["resumable_state"], "BORRADOR")

        # 2. Cancelar la mision
        ok_canc, c_rec, _ = self.manager.cancel_mission("MSN-CTRL-001", reason="Cancelada por operador humano")
        self.assertTrue(ok_canc)
        self.assertEqual(c_rec["status"], "CANCELADA")

        # 3. Intentar pausar una mision ya cancelada -> error de estado terminal
        ok_pause_term, _, err_term = self.manager.pause_mission("MSN-CTRL-001", reason="Intento invalido")
        self.assertFalse(ok_pause_term)
        self.assertIn("ESTADO_TERMINAL_INMUTABLE", err_term)

    def test_ac02_agent_cancellation_denied(self) -> None:
        """AC-02: Un agente intentando cancelar es bloqueado con PERMISSION_DENIED."""
        self.repo.save_mission({
            "mission_id": "MSN-AGENT-CANC",
            "status": "EN_EJECUCION",
            "version": 1,
        })

        ok_agent, _, err_agent = self.manager.cancel_mission(
            "MSN-AGENT-CANC",
            reason="Intento IA",
            actor_role="product_architect",
        )
        self.assertFalse(ok_agent)
        self.assertIn("PERMISSION_DENIED", err_agent)

    def test_ac03_resume_blocked_on_budget_exhaustion(self) -> None:
        """AC-03 presupuesto: fixture independiente respeta una mision activa."""
        # 1. Mision con presupuesto agotado
        ok_saved, error_saved = self.repo.save_mission({
            "mission_id": "MSN-BUDGET-EXH",
            "status": "PAUSADA",
            "resumable_state": "EN_EJECUCION",
            "cumulative_cost_usd": 25.0,
            "version": 1,
        })
        self.assertTrue(ok_saved, error_saved)
        before = list(self.repo._conn.iterdump())

        ok_res_b, _, err_res_b = self.manager.resume_mission("MSN-BUDGET-EXH")
        self.assertFalse(ok_res_b)
        self.assertIn("PRESUPUESTO_AGOTADO", err_res_b)
        self.assertEqual(list(self.repo._conn.iterdump()), before)

    def test_ac03_resume_blocked_on_missing_evidence(self) -> None:
        """AC-03 evidencia: no confundir mision inexistente con evidencia ausente."""
        # 2. Mision pausada con evidencia faltante
        ok_saved, error_saved = self.repo.save_mission({
            "mission_id": "MSN-EVI-MISS",
            "status": "PAUSADA",
            "resumable_state": "PLAN_EN_REVISION",
            "cumulative_cost_usd": 5.0,
            "version": 1,
        })
        self.assertTrue(ok_saved, error_saved)
        before = list(self.repo._conn.iterdump())

        ok_res_e, _, err_res_e = self.manager.resume_mission("MSN-EVI-MISS", missing_evidence=True)
        self.assertFalse(ok_res_e)
        self.assertIn("EVIDENCIA_NO_DISPONIBLE", err_res_e)
        self.assertEqual(list(self.repo._conn.iterdump()), before)

    def test_ac04_idempotent_pause_and_cancellation(self) -> None:
        """AC-04: Pausar una mision ya pausada es idempotente y no incrementa la version."""
        self.repo.save_mission({
            "mission_id": "MSN-IDEMP-PAUSE",
            "status": "PAUSADA",
            "resumable_state": "EN_CONSOLIDACION",
            "version": 2,
        })

        ok_p, p_rec, _ = self.manager.pause_mission("MSN-IDEMP-PAUSE", reason="Pausa repetida")
        self.assertTrue(ok_p)
        self.assertEqual(p_rec["version"], 2)
        self.assertEqual(p_rec["status"], "PAUSADA")

    def test_ac05_scope_change_increments_version_and_sets_plan_review(self) -> None:
        """AC-05: Un cambio de alcance incrementa la version y devuelve la mision a PLAN_EN_REVISION."""
        self.repo.save_mission({
            "mission_id": "MSN-SCOPE-001",
            "status": "AUTORIZADA_PARA_EJECUTAR",
            "version": 1,
        })

        ok_sc, sc_rec, _ = self.manager.request_scope_change(
            "MSN-SCOPE-001",
            change_summary="Ampliar alcance para incluir integracion con API tributaria",
            actor_role="usuario_humano",
        )
        self.assertTrue(ok_sc)
        self.assertEqual(sc_rec["version"], 2)
        self.assertEqual(sc_rec["status"], "PLAN_EN_REVISION")

        # Comprobar integracion con runtime
        self.assertIsNotNone(self.runtime.controls)
        self.assertIsInstance(self.runtime.controls, mission_controls.MissionControlManager)


if __name__ == "__main__":
    unittest.main()
