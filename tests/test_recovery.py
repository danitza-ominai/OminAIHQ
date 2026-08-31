"""Recovery regression uses actual canonical checkpoints and synthetic authority."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from test_human_approvals import fixture, PROFILE
from app import hq_runtime, local_repository, recovery

class TestRecovery(unittest.TestCase):
    def setUp(self):
        self.tmp_dir=tempfile.TemporaryDirectory()
        self.db_path=str(Path(self.tmp_dir.name)/"recovery.db")
        self.runtime,self.repo,self.ctx,self.req=fixture(self.db_path)
        self.manager=self.runtime.recovery
    def tearDown(self):
        self.repo.close()
        self.tmp_dir.cleanup()

    def test_ac01_and_ac02_clean_recovery_from_checkpoint(self):
        self.assertTrue(self.runtime.approvals.submit_human_decision(self.req,"APROBAR",context=self.ctx)[0])
        self.assertTrue(self.runtime.execute_local_simulation("MSN-SIM",self.ctx,one_step=True)[0])
        before=self.repo.get_mission("MSN-SIM")
        self.repo.close()
        self.repo=local_repository.LocalRepository(self.db_path)
        manager=recovery.RecoveryManager(repository=self.repo)
        ok,state,error=manager.recover_mission("MSN-SIM")
        self.assertTrue(ok,error)
        for key in ("tasks","task_results","agent_requests","cost_usd","active_seconds","version"):
            self.assertEqual(state[key],before[key])
        self.assertEqual(state["tasks"][0]["status"],"COMPLETA")

    def test_ac03_corrupt_checkpoint_or_invalid_approval_blocks_recovery(self):
        cp=self.repo.list_checkpoints("MSN-SIM")[-1]
        original=json.loads(cp["state_snapshot_json"])
        cases=[{}, {**original,"mission_id":"MSN-OTHER"}, {**original,"mission_version":999},
               {**original,"artifacts":["MISSING"]}, {**original,"authorizations":["APP-MISSING"]},
               {**original,"fingerprint":"sha256:tampered"}]
        for bad in cases:
            with self.subTest(bad=bad):
                self.repo._conn.execute("UPDATE checkpoints SET state_snapshot_json=? WHERE checkpoint_id=?",
                                        (json.dumps(bad),cp["checkpoint_id"]))
                self.repo._conn.commit()
                before=list(self.repo._conn.iterdump())
                ok,state,error=self.manager.recover_mission("MSN-SIM")
                self.assertFalse(ok);self.assertIsNone(state);self.assertIn("CHECKPOINT_CORRUPTO",error)
                self.assertEqual(list(self.repo._conn.iterdump()),before)

    def test_ac04_interrupted_in_progress_task_pauses_in_indeterminate_state(self):
        from unittest.mock import Mock
        self.assertTrue(self.runtime.approvals.submit_human_decision(self.req,"APROBAR",context=self.ctx)[0])
        provider=Mock()
        provider.execute_task.side_effect=TimeoutError("SINTETICA")
        self.runtime.simulation_provider=provider
        self.assertFalse(self.runtime.execute_local_simulation("MSN-SIM",self.ctx)[0])
        before=self.repo.budget_snapshot()
        ok,state,error=self.manager.recover_mission("MSN-SIM")
        self.assertTrue(ok,error)
        self.assertEqual(state["status"],"PAUSADA")
        self.assertTrue(state["inflight"])
        self.assertFalse(self.runtime.execute_local_simulation("MSN-SIM",self.ctx)[0])
        self.assertEqual(provider.execute_task.call_count,1)
        self.assertEqual(self.repo.budget_snapshot(),before)

    def test_ac05_runtime_integration(self):
        self.assertIs(self.runtime.recovery,self.manager)

    def test_invalid_writes_reject_without_effects_and_schemas_are_real(self):
        for event in self.repo.list_events("MSN-SIM"):
            self.repo.validate_core("event",event)
        cp=self.repo.list_checkpoints("MSN-SIM")[-1]
        self.repo.validate_core("checkpoint",json.loads(cp["state_snapshot_json"]))
        before=list(self.repo._conn.iterdump())
        with self.assertRaises(ValueError):
            self.repo.save_event({"event_id":"INCOMPLETE","mission_id":"MSN-SIM"})
        self.assertFalse(self.repo.save_checkpoint({})[0])
        self.assertEqual(list(self.repo._conn.iterdump()),before)

if __name__=="__main__": unittest.main()
