"""Regression fixtures use explicit synthetic authority, never wire identity."""
import copy
import json
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import patch
from app import hq_runtime, human_approvals, local_repository

PROFILE = {"user_id":"USR-SIM", "display_name":"SIMULADA", "actor_role":"usuario_humano"}
def fixture(db=":memory:", stage="plan"):
    repo=local_repository.LocalRepository(db)
    runtime=hq_runtime.HQRuntime(repository=repo)
    ctx=runtime.approvals.bind_local_profile(PROFILE)
    ok, mission, err=runtime.create_local_mission(dict(mission_id="MSN-SIM", title="SIMULADA B2B",
        objective="Portal de compras industrial", context="Distribuidora B2B SIMULADA", expected_result="VBP SIMULADA"),ctx)
    assert ok, err
    request=repo.get_object("approval_request",mission["approval_id"])["request"]
    if stage in ("vbp","approved","exception"):
        ok, _, err=runtime.approvals.submit_human_decision(request,"APROBAR",context=ctx)
        assert ok, err
        ok, mission, err=runtime.execute_local_simulation("MSN-SIM",ctx)
        assert ok, err
        request=mission["approval_request"]
    if stage=="approved":
        assert mission["evaluation_report"]["integrity"]["valid"]
        ok, _, err=runtime.approvals.submit_human_decision(request,"APROBAR",context=ctx)
        assert ok, err
    if stage=="exception":
        ok, _, err=runtime.approvals.submit_human_decision(request,"APROBAR_CON_EXCEPCION",context=ctx,
            comment="Excepcion SINTETICA de prueba", conditions=["Solo demostracion"],risks=["No validado para entrega real"])
        assert ok, err
    return runtime, repo, ctx, request

class TestHumanApprovals(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.db=str(Path(self.tmp.name)/"approvals.db")
        self.runtime,self.repo,self.ctx,self.req=fixture(self.db)
        self.engine=self.runtime.approvals
    def tearDown(self):
        self.repo.close(); self.tmp.cleanup()
    def submit(self, req=None, decision="APROBAR", **kwargs):
        return self.engine.submit_human_decision(req or self.req,decision,context=self.ctx,**kwargs)
    def assert_unconsumed(self):
        self.assertEqual(self.repo.list_approvals("MSN-SIM"),[])
        self.assertEqual(self.repo.get_mission("MSN-SIM")["status"],"PLAN_EN_REVISION")
    def test_ac01_agent_self_approval_is_denied(self):
        for kwargs in ({}, {"actor_role":"chief_of_staff","actor_user_id":"agent"}):
            ok,_,_=self.engine.submit_human_decision(self.req,"APROBAR",**kwargs)
            self.assertFalse(ok); self.assert_unconsumed()
        self.assertFalse(self.submit(actor_role="chief_of_staff")[0]); self.assert_unconsumed()
    def test_ac02_expiration_and_idempotent_replay(self):
        for offset in (299.999,300,300.001):
            with self.subTest(offset=offset):
                runtime,repo,ctx,req=fixture()
                runtime.approvals.now_fn=lambda: datetime.fromisoformat(req["created_at"])+timedelta(seconds=offset)
                result=runtime.approvals.submit_human_decision(req,"APROBAR",context=ctx,check_expiration=False)
                self.assertEqual(result[0],offset<300)
                self.assertEqual(len(repo.list_approvals("MSN-SIM")),int(offset<300));repo.close()
        ok,original,err=self.submit();self.assertTrue(ok,err)
        self.repo.close()
        self.repo=local_repository.LocalRepository(self.db)
        self.engine=human_approvals.HumanApprovalEngine(repository=self.repo)
        self.ctx=self.engine.bind_local_profile(PROFILE)
        self.assertEqual(self.submit()[1],original)
        self.assertFalse(self.submit(decision="RECHAZAR",comment="No")[0])
        self.assertEqual(len(self.repo.list_approvals("MSN-SIM")),1)
        self.assertFalse(self.engine.submit_human_decision(self.req,"APROBAR")[0])
    def test_ac03_gate_separation_and_conditional_approval_validation(self):
        self.assertFalse(self.submit(decision="APROBAR_CON_CONDICIONES",conditions=["x"])[0])
        self.assertFalse(self.submit(decision="APROBAR_CON_EXCEPCION",comment="x",conditions=["x"],risks=["x"])[0])
        self.assert_unconsumed()
        self.assertTrue(self.submit()[0])
        self.assertIsNone(self.repo.get_mission("MSN-SIM").get("pending_GATE_2_VBP"))
    def test_ac04_rejection_preserves_records(self):
        self.assertTrue(self.submit(decision="RECHAZAR",comment="Faltan requisitos")[0])
        self.assertEqual(self.repo.list_approvals("MSN-SIM")[0]["decision"],"RECHAZAR")
        self.assertEqual(self.repo.get_mission("MSN-SIM")["status"],"PLAN_EN_REVISION")
        self.assertGreater(len(self.repo.list_events("MSN-SIM")),1)

    def test_plan_approval_advances_and_aligns_all_active_references(self):
        before = self.repo.get_mission("MSN-SIM")
        old_version = before["version"]
        ok, response, error = self.submit()
        self.assertTrue(ok, error)
        after = self.repo.get_mission("MSN-SIM")
        self.assertEqual(after["version"], old_version + 1)
        self.assertEqual(after["nuclear"]["record_version"], after["version"])
        self.assertEqual(after["nuclear"]["current_state"], after["status"])
        self.assertEqual(response["new_mission_status"], "AUTORIZADA_PARA_EJECUTAR")
        self.assertTrue(after["tasks"])
        self.assertTrue(all(t["mission_version"] == after["version"] for t in after["tasks"]))
        events = self.repo.list_events("MSN-SIM")
        self.assertEqual(events[-1]["version"], after["version"])
        checkpoints = self.repo.list_checkpoints("MSN-SIM")
        checkpoint = json.loads(checkpoints[-1]["state_snapshot_json"])
        self.assertEqual(checkpoint["mission_version"], after["version"])
        self.assertEqual(checkpoint["state"], after["status"])
        self.assertEqual(after["nuclear"]["last_checkpoint_id"], checkpoint["checkpoint_id"])
        self.assertEqual(after["nuclear"]["approval_refs"], [self.req["approval_id"]])
    def test_ac05_runtime_integration(self):
        self.assertIs(self.runtime.approvals,self.engine)
    def test_forged_crossed_stale_requests_no_effects(self):
        for field,value in {"approval_id":"INVENTADA","mission_id":"MSN-OTRA","gate_type":"GATE_2_VBP",
            "fingerprint":"sha256:inventada","idempotency_key":"otra","version":99,"expiration":"2020-01-01T00:00:00Z"}.items():
            with self.subTest(field=field):
                req={**self.req,field:value}
                self.assertFalse(self.submit(req)[0]);self.assert_unconsumed()
        ok,new,err=self.engine.create_approval_request("MSN-SIM","GATE_1_PLAN",{"new":"version"})
        self.assertTrue(ok,err);self.assertFalse(self.submit()[0]);self.assert_unconsumed()
        self.assertFalse(self.engine.create_approval_request("MSN-NO","GATE_1_PLAN",{})[0])
        self.assertIsNone(self.repo.get_mission("MSN-NO"))
    def test_atomic_rollback_every_write(self):
        for method in ("save_approval_atomic","save_event","save_checkpoint","save_ledger"):
            with self.subTest(method=method):
                before=list(self.repo._conn.iterdump())
                with patch.object(self.repo,method,side_effect=RuntimeError("synthetic")):
                    ok,_,error=self.submit()
                self.assertFalse(ok);self.assertIn("SYSTEM_ERROR",error)
                self.assertEqual(list(self.repo._conn.iterdump()),before)
    def test_vbp_no_pasa_exception_and_missing_evidence(self):
        runtime,repo,ctx,request=fixture(stage="vbp")
        try:
            m=repo.get_mission("MSN-SIM");m["evaluation_report"]["verdict"]="NO_PASA";repo.save_mission(m)
            decide=lambda decision,**kw:runtime.approvals.submit_human_decision(request,decision,context=ctx,**kw)
            self.assertFalse(decide("APROBAR")[0])
            for kwargs in ({"comment":"motivo"},{"comment":"motivo","conditions":["x"]},{"conditions":["x"],"risks":["x"]}):
                self.assertFalse(decide("APROBAR_CON_EXCEPCION",**kwargs)[0])
            self.assertEqual(len(repo.list_approvals("MSN-SIM")),1)
            ev=m["evidence_ids"][0];original=repo.get_object("evidence_original",ev)
            repo.put_object("evidence_original",ev,{})
            result=decide("APROBAR_CON_EXCEPCION",comment="motivo",conditions=["x"],risks=["x"])
            self.assertFalse(result[0]);self.assertIn("EVIDENCIA_NO_DISPONIBLE",result[2])
            self.assertEqual(len(repo.list_approvals("MSN-SIM")),1)
            repo.put_object("evidence_original",ev,original)
            self.assertTrue(decide("APROBAR_CON_EXCEPCION",comment="motivo",conditions=["x"],risks=["x"])[0])
        finally: repo.close()

if __name__=="__main__": unittest.main()
