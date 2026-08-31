"""Synthetic approved-memory regression; consent is a trusted local capability."""
import tempfile
import unittest
from pathlib import Path
from test_human_approvals import fixture, PROFILE
from app import approved_memory, hq_runtime, local_repository

class TestApprovedMemory(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=str(Path(self.tmp.name)/"memory.db")
        self.runtime,self.repo,self.ctx,self.req=fixture(self.path)
        self.memory=self.runtime.memory
    def tearDown(self):
        self.repo.close()
        self.tmp.cleanup()
    def propose(self, **kw):
        ok,rec,error=self.memory.propose_memory("PREFERENCIA","SINTETICA: texto uno. Texto privado dos.","MSN-SIM",context=self.ctx,**kw)
        self.assertTrue(ok,error)
        return rec
    def query(self, role="chief_of_staff", **kw):
        return self.memory.query_memories_for_role(role,context=self.ctx,**kw)
    def approve(self, rec, **kw):
        return self.memory.approve_memory(rec["memory_id"],context=self.ctx,version=rec["version"],**kw)

    def test_ac01_no_memory_without_human_confirmation(self):
        before=list(self.repo._conn.iterdump())
        self.assertFalse(self.memory.propose_memory("PREFERENCIA","SINTETICA","MSN-SIM",human_approved=True,context=self.ctx)[0])
        self.assertEqual(list(self.repo._conn.iterdump()),before)
        rec=self.propose()
        self.assertEqual(self.query(),[])
        self.assertFalse(self.memory.approve_memory(rec["memory_id"],version=1))
        self.assertTrue(self.approve(rec))
        self.assertEqual(len(self.query()),1)

    def test_ac02_cross_mission_retrieval(self):
        rec=self.propose();self.assertTrue(self.approve(rec))
        self.assertTrue(self.runtime.control_local_mission("MSN-SIM","cancel",self.ctx)[0])
        self.repo.close()
        self.repo=local_repository.LocalRepository(self.path)
        self.runtime=hq_runtime.HQRuntime(repository=self.repo)
        self.ctx=self.runtime.approvals.bind_local_profile(PROFILE)
        self.memory=self.runtime.memory
        ok,mission,error=self.runtime.create_local_mission(dict(mission_id="MSN-SECOND",title="SIMULADA",
            objective="Segunda mision",context="SINTETICA",expected_result="VBP"),self.ctx)
        self.assertTrue(ok,error)
        self.assertEqual(mission["plan"]["memory_refs"],[{"memory_id":rec["memory_id"],"version":1}])
        self.assertEqual(self.query()[0]["content"],rec["content"])

    def test_ac04_role_based_access_control(self):
        rec=self.propose();self.assertTrue(self.approve(rec))
        self.assertEqual(len(self.query()),1)
        self.assertEqual(self.query("product_architect"),[])
        fragment=self.query("product_architect",fragments={rec["memory_id"]:(0,10)})[0]
        self.assertEqual(fragment["content"],rec["content"][:10])
        self.assertNotIn("origin_mission_id",fragment)
        governance=self.query("governance_risk")[0]
        self.assertNotIn("content",governance)
        self.assertEqual(governance["approved_version"],1)
        with self.assertRaises(approved_memory.MemoryAccessError):
            self.query("unknown")

    def test_ac05_versioning_and_safe_purging(self):
        rec=self.propose();self.assertTrue(self.approve(rec))
        ok,updated,error=self.memory.update_memory(rec["memory_id"],"TEXTO NUEVO SINTETICO",context=self.ctx,version=1)
        self.assertTrue(ok,error);self.assertEqual(updated["version"],2)
        self.assertEqual(updated['version_history'][0]['status'],'INACTIVA')
        self.assertNotIn('content',updated['version_history'][0])
        self.assertEqual(self.query(),[])
        before=list(self.repo._conn.iterdump())
        self.assertFalse(self.approve(rec))
        self.assertFalse(self.memory.delete_memory(rec["memory_id"],context=self.ctx,version=1))
        self.assertEqual(list(self.repo._conn.iterdump()),before)
        self.assertTrue(self.memory.delete_memory(rec["memory_id"],context=self.ctx,version=2))
        tombstone=self.memory.memories[rec["memory_id"]]
        self.assertEqual(set(tombstone),{"memory_id","user_id","origin_mission_id","deleted_at"})
        dump="".join(self.repo._conn.iterdump())
        self.assertNotIn("TEXTO NUEVO SINTETICO",dump)
        self.assertNotIn(rec["content"],dump)
        self.assertEqual(self.query(),[])

    def test_conflict_temporal_review_material_impact_and_foreign_owner_block(self):
        for flags in ({"conflict":True},{"material_impact":True},{"review_required":True},
                      {"review_at":"2020-01-01T00:00:00+00:00"}):
            rec=self.propose(**flags)
            self.assertFalse(self.approve(rec));self.assertEqual(self.query(),[])
        rec=self.propose()
        foreign={**rec,"user_id":"FOREIGN"}
        self.repo.put_object("memory",rec["memory_id"],foreign)
        before=list(self.repo._conn.iterdump())
        self.assertFalse(self.approve(rec))
        self.assertFalse(self.memory.update_memory(rec["memory_id"],"x",context=self.ctx,version=1)[0])
        self.assertFalse(self.memory.delete_memory(rec["memory_id"],context=self.ctx,version=1))
        self.assertEqual(list(self.repo._conn.iterdump()),before)

    def test_runtime_integration(self):
        self.assertIs(self.memory.repository,self.repo)
        self.assertIs(self.memory.authority,self.runtime.approvals)

    def test_changed_memory_blocks_old_plan_and_purge_preserves_historical_vbp(self):
        rec=self.propose();self.assertTrue(self.approve(rec))
        self.assertTrue(self.runtime.control_local_mission('MSN-SIM','cancel',self.ctx)[0])
        ok,mission,error=self.runtime.create_local_mission(dict(mission_id='MSN-NEXT',title='SIMULADA',objective='Prueba',context='SINTETICA',expected_result='VBP'),self.ctx)
        self.assertTrue(ok,error)
        req=self.repo.get_object('approval_request',mission['approval_id'])['request']
        self.assertTrue(self.runtime.approvals.submit_human_decision(req,'APROBAR',context=self.ctx)[0])
        self.assertTrue(self.memory.update_memory(rec['memory_id'],'SINTETICA NUEVA',context=self.ctx,version=1)[0])
        before=list(self.repo._conn.iterdump())
        self.assertFalse(self.runtime.execute_local_simulation('MSN-NEXT',self.ctx)[0])
        self.assertEqual(list(self.repo._conn.iterdump()),before)
        runtime,repo,ctx,request=fixture(stage='approved');self.addCleanup(repo.close)
        historical=repo.get_object('candidate','MSN-SIM:GATE_2_VBP')
        ok,record,error=runtime.memory.propose_memory('PREFERENCIA','SINTETICA PARA PURGA','MSN-SIM',context=ctx)
        self.assertTrue(ok,error)
        self.assertTrue(runtime.memory.approve_memory(record['memory_id'],context=ctx,version=1))
        self.assertTrue(runtime.memory.delete_memory(record['memory_id'],context=ctx,version=1))
        self.assertEqual(repo.get_object('candidate','MSN-SIM:GATE_2_VBP'),historical)
        self.assertNotIn('SINTETICA PARA PURGA',repr(list(repo._conn.iterdump())))

if __name__=="__main__": unittest.main()
