"""Pruebas Integrales Extremo a Extremo para OminAI HQ (PZ-015A, PZ-013A/B/C).

Valida el flujo integral completo desde la admision de mision (Intake),
revision y aprobacion del plan (Puerta 1), ejecucion secuencial de los 5 especialistas,
ensamblaje del VBP, dictamen de gobernanza, aprobacion del VBP (Puerta 2),
exportacion y descarga fiel del Markdown canonico (.md), y auditoria en tiempo real.
"""

import tempfile
import json
import unittest
from pathlib import Path

import app.hq_runtime as hq_runtime
import app.local_repository as local_repository
import app.runtime_contracts as runtime_contracts
import app.vbp_document as vbp_document
import app.vbp_export as vbp_export


class TestHQEndToEnd(unittest.TestCase):
    """Suite de pruebas de integracion integral extremo a extremo (E2E)."""

    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.db_path = str(Path(self.tmp_dir.name) / "test_e2e.db")
        self.repo = local_repository.LocalRepository(db_path=self.db_path)
        self.runtime = hq_runtime.HQRuntime(repository=self.repo)

    def tearDown(self) -> None:
        try:
            self.repo.close()
        except Exception:
            pass
        try:
            self.tmp_dir.cleanup()
        except Exception:
            pass

    def test_ac01_full_e2e_two_gates_and_vbp_export(self) -> None:
        """AC-01: Recorrido completo de mision desde intake hasta VBP aprobado y exportado (PZ-013C)."""
        from test_human_approvals import fixture
        runtime,repo,ctx,req=fixture(stage="approved")
        self.addCleanup(repo.close)
        mission=repo.get_mission("MSN-SIM")
        self.assertEqual(mission["status"],"VBP_APROBADO")
        self.assertEqual(mission["agent_requests"],4)
        self.assertEqual(len(mission["task_results"]),4)
        for task in mission["tasks"]:
            self.assertEqual(task["status"],"COMPLETA")
            self.assertEqual(task["mission_id"],"MSN-SIM")
        vbp=repo.get_object("candidate","MSN-SIM:GATE_2_VBP")
        self.assertEqual(mission["version"], mission["nuclear"]["record_version"])
        self.assertTrue(all(t["mission_version"] <= mission["version"] for t in mission["tasks"]))
        self.assertTrue(all(result["mission_version"] <= mission["version"]
                            for result in mission["task_results"].values()))
        self.assertTrue(all(repo.get_object("evidence", eid)["mission_version"] <= mission["version"]
                            for eid in mission["evidence_ids"]))
        self.assertTrue(vbp["mission_version"] <= mission["version"])
        self.assertEqual(repo.list_events("MSN-SIM")[-1]["version"], mission["version"])
        latest_checkpoint=json.loads(repo.list_checkpoints("MSN-SIM")[-1]["state_snapshot_json"])
        self.assertEqual(latest_checkpoint["mission_version"], mission["version"])
        valid,errors=runtime_contracts.RuntimeContractsValidator().validate_structure("vbp",vbp)
        self.assertTrue(valid,errors)
        ok,raw,meta,error=vbp_export.export_canonical_vbp_bytes(vbp,repository=repo)
        self.assertTrue(ok,error);self.assertIn(b"```english",raw)
        self.assertEqual(meta["mission_id"],"MSN-SIM")
        self.assertEqual(len(repo.list_approvals("MSN-SIM")),2)
        self.assertGreater(len(repo.list_events("MSN-SIM")),10)

    def test_ac02_fault_recovery_and_budget_limits_preserved(self) -> None:
        """AC-02: Interrupcion y reanudacion preserva el gasto acumulado y detecta limites excedidos."""
        self.repo.save_mission({
            "mission_id": "MSN-E2E-FAULT",
            "title": "Mision con fallo",
            "status": "PAUSADA",
            "resumable_state": "EN_EJECUCION",
            "cumulative_cost_usd": 24.50,
            "version": 1,
        })

        # Reanudar con presupuesto restante ($0.50 disponibles) -> permitido
        ok_res, r_rec, _ = self.runtime.controls.resume_mission("MSN-E2E-FAULT")
        self.assertTrue(ok_res)
        self.assertEqual(r_rec["status"], "EN_EJECUCION")

        # Pausar y gastar hasta alcanzar $25.00
        self.runtime.controls.pause_mission("MSN-E2E-FAULT", reason="Alerta de techo")
        updated_m = self.repo.get_mission("MSN-E2E-FAULT")
        updated_m["cumulative_cost_usd"] = 25.00
        self.repo.save_mission(updated_m)

        # Reintentar reanudar -> bloqueado por PRESUPUESTO_AGOTADO
        ok_res_block, _, err_b = self.runtime.controls.resume_mission("MSN-E2E-FAULT")
        self.assertFalse(ok_res_block)
        self.assertIn("PRESUPUESTO_AGOTADO", err_b)


class TestIntegratedRecovery(unittest.TestCase):
    def test_restart_does_not_repeat_confirmed_task(self):
        from test_human_approvals import fixture,PROFILE
        with tempfile.TemporaryDirectory() as td:
            path=str(Path(td)/"restart.db")
            runtime,repo,ctx,req=fixture(path)
            try:
                self.assertTrue(runtime.approvals.submit_human_decision(req,"APROBAR",context=ctx)[0])
                self.assertTrue(runtime.execute_local_simulation("MSN-SIM",ctx,one_step=True)[0])
                first=repo.get_mission("MSN-SIM")["task_results"]
            finally:
                repo.close()
            repo=local_repository.LocalRepository(path)
            try:
                runtime=hq_runtime.HQRuntime(repository=repo);ctx=runtime.approvals.bind_local_profile(PROFILE)
                result=runtime.execute_local_simulation("MSN-SIM",ctx)
                self.assertTrue(result[0],result[2])
                mission=repo.get_mission("MSN-SIM")
                self.assertEqual(mission["agent_requests"],4)
                for key,value in first.items():self.assertEqual(mission["task_results"][key],value)
            finally:
                repo.close()
    def test_unknown_step_blocks_reexecution(self):
        from test_human_approvals import fixture
        from unittest.mock import Mock
        runtime,repo,ctx,req=fixture();self.addCleanup(repo.close)
        runtime.approvals.submit_human_decision(req,"APROBAR",context=ctx)
        runtime.simulation_provider=Mock()
        runtime.simulation_provider.execute_task.side_effect=TimeoutError("SIMULADA")
        self.assertFalse(runtime.execute_local_simulation("MSN-SIM",ctx)[0])
        self.assertFalse(runtime.execute_local_simulation("MSN-SIM",ctx)[0])
        self.assertEqual(runtime.simulation_provider.execute_task.call_count,1)
        self.assertEqual(repo.get_mission("MSN-SIM")["agent_requests"],1)

if __name__ == "__main__":
    unittest.main()
