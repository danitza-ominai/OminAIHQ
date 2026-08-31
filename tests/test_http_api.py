"""Real router regression; synthetic decisions are not human acceptance."""
import copy
import json
import unittest
from test_human_approvals import fixture
from app.http_api import LocalAPIRouter

class TestHTTPAPI(unittest.TestCase):
    def setUp(self):
        self.runtime,self.repo,self.ctx,self.req=fixture()
        self.router=LocalAPIRouter(self.runtime,local_context=self.ctx)
        self.headers={"Host":"localhost:8000","Origin":"http://localhost:8000",
            "Content-Type":"application/json","X-Ominai-CSRF":self.router.csrf_token}
        self.base="/api/v1/missions/MSN-SIM"
    def tearDown(self):self.repo.close()
    def call(self,method,path,body=None,headers=None):
        return self.router.dispatch(method,path,headers or self.headers,
            b"" if body is None else json.dumps(body).encode())
    def decide(self,req=None,decision="APROBAR",**kw):
        return self.call("POST",self.base+"/decisions",{"approval_request":req or self.req,"decision":decision,**kw})
    def test_ac01_health_and_payload_size_limits(self):
        self.assertEqual(self.call("GET","/health")[0],200)
        self.assertEqual(self.router.dispatch("POST",self.base,self.headers,b"x"*51201)[0],413)
    def test_ac02_cross_origin_and_agent_actor_rejection(self):
        before=list(self.repo._conn.iterdump())
        for headers in ({**self.headers,"Origin":"http://evil.test"},{**self.headers,"Host":"evil.test"},
            {**self.headers,"X-Ominai-Actor-Role":"usuario_humano"},{**self.headers,"X-Ominai-CSRF":"wrong"}):
            self.assertEqual(self.call("POST",self.base+"/decisions",{},headers)[0],403)
        for field in ("user_id","actor_role","actor_user_id"):
            self.assertEqual(self.call("POST",self.base+"/decisions",{field:"usuario_humano"})[0],403)
        router=LocalAPIRouter(self.runtime)
        self.assertEqual(router.dispatch("GET","/api/v1/profile",self.headers)[0],403)
        self.assertEqual(list(self.repo._conn.iterdump()),before)
    def test_ac03_mission_crud_and_not_found(self):
        self.assertEqual(self.call("GET",self.base)[0],200)
        self.assertEqual(self.call("GET","/api/v1/missions/MSN-NONE")[0],404)
        before=self.repo.get_mission("MSN-SIM")
        self.assertEqual(self.decide()[0],200)
        after=self.repo.get_mission("MSN-SIM")
        for key in ("title","objective","context","expected_result"):self.assertEqual(before[key],after[key])
        self.assertEqual(after["nuclear"]["mission_id"],after["mission_id"])
    def test_ac04_pause_and_cancel_endpoints(self):
        self.assertEqual(self.decide()[0],200)
        self.assertEqual(self.call("POST",self.base+"/pause",{"reason":"SIMULADA"})[0],200)
        self.assertEqual(json.loads(self.call("GET",self.base)[2])["data"]["status"],"PAUSADA")
        self.assertEqual(self.call("POST",self.base+"/execute-step")[0],403)
        self.assertEqual(self.call("POST",self.base+"/resume")[0],200)
        self.assertEqual(self.call("POST",self.base+"/cancel")[0],200)
        self.assertEqual(self.call("POST",self.base+"/execute-step")[0],403)
        self.assertGreaterEqual(self.call("POST",self.base+"/resume")[0],400)
        self.assertEqual(self.repo.get_mission("MSN-SIM")["agent_requests"],0)
    def test_ac05_static_i18n_serving(self):
        for path in ("/","/app.js","/styles.css","/i18n.js"):self.assertEqual(self.call("GET",path)[0],200)
    def test_ac06_full_mission_flow_and_vbp_download_via_http(self):
        self.assertEqual(self.call("GET",self.base+"/vbp/export")[0],404)
        self.assertEqual(self.decide()[0],200)
        code,_,body=self.call("POST",self.base+"/execute");self.assertEqual(code,200,body)
        mission=json.loads(body)["data"]
        self.assertEqual(mission["status"],"VBP_EN_REVISION");self.assertEqual(mission["agent_requests"],4)
        self.assertEqual(self.call("GET",self.base+"/vbp/export")[0],409)
        self.assertTrue(mission["evaluation_report"]["integrity"]["valid"])
        self.assertEqual(self.decide(mission["approval_request"])[0],200)
        self.assertEqual(self.repo.get_mission("MSN-SIM")["status"],"VBP_APROBADO")
        a=self.call("GET",self.base+"/vbp/export");self.assertEqual(a[0],200,a[2])
        b=self.call("GET",self.base+"/vbp/export");self.assertEqual(a[2],b[2])
        self.assertEqual(self.repo.get_mission('MSN-SIM')['status'], 'VBP_APROBADO')
        self.assertTrue(a.on_delivered())  # synthetic adapter completion, not browser evidence
        self.assertEqual(self.repo.get_mission("MSN-SIM")["status"],"FINALIZADA")
        self.assertIn(b"```english",a[2]);self.assertIn(b"SIMULADA",a[2])
    def test_invalid_requests_rejected_without_effect(self):
        before=list(self.repo._conn.iterdump())
        for field in ("approval_id","mission_id","fingerprint","idempotency_key","gate_type"):
            code,_,_=self.decide({**self.req,field:"INVENTADA"})
            self.assertGreaterEqual(code,400)
        self.assertEqual(list(self.repo._conn.iterdump()),before)
        self.assertEqual(self.call("POST",self.base+"/execute-step")[0],403)
    def test_profile_memory_audit_and_no_autoapproval(self):
        for path in ("/api/v1/profile","/api/v1/memory",self.base+"/audit"):
            code,_,body=self.call("GET",path);self.assertEqual(code,200,body)
        code,_,body=self.call("POST","/api/v1/memory",{"mission_id":"MSN-SIM","category":"PREFERENCIA","fact_text":"SIMULADA"})
        self.assertEqual(code,201,body)
        memories=list(self.runtime.memory.memories.values());self.assertEqual(len(memories),1)
        self.assertNotEqual(memories[0]["status"],"APROBADA")

    def test_step_current_mission_and_cancel_canonical_rollback(self):
        from unittest.mock import patch
        self.assertEqual(json.loads(self.call('GET','/api/v1/missions/current')[2])['data']['mission_id'],'MSN-SIM')
        before = list(self.repo._conn.iterdump())
        for method in ('save_mission','save_event','save_checkpoint','put_object'):
            with patch.object(self.repo, method, side_effect=RuntimeError('SIMULADA')):
                self.assertEqual(self.call('POST',self.base+'/cancel')[0],500)
            self.assertEqual(list(self.repo._conn.iterdump()),before)
        self.assertEqual(self.decide()[0],200)
        self.assertEqual(self.call('POST',self.base+'/execute-step')[0],200)
        self.assertEqual(self.repo.get_mission('MSN-SIM')['agent_requests'],1)
        self.assertEqual(self.call('POST',self.base+'/cancel')[0],200)
        for event in self.repo.list_events('MSN-SIM'):
            self.repo.validate_core('event',event)
        before = list(self.repo._conn.iterdump())
        self.assertEqual(self.call('POST',self.base+'/execute')[0],403)
        self.assertEqual(list(self.repo._conn.iterdump()),before)

    def test_memory_versioned_http_lifecycle(self):
        path='/api/v1/memory'
        value=json.loads(self.call('POST',path,{'mission_id':'MSN-SIM','fact_text':'SINTETICA confidencial','conflict':True})[2])['data']
        mid=value['memory_id']; item=path+'/'+mid
        before=list(self.repo._conn.iterdump())
        self.assertEqual(self.call('POST',item+'/approve',{'version':1})[0],409)
        self.assertEqual(list(self.repo._conn.iterdump()),before)
        self.assertEqual(self.call('POST',item+'/approve',{'version':1,'resolve_blockers':True})[0],200)
        self.assertEqual(self.call('PUT',item,{'version':1,'fact_text':'SINTETICA nueva'})[0],200)
        self.assertFalse(self.runtime.memory.memories[mid]['human_approved'])
        before=list(self.repo._conn.iterdump())
        self.assertEqual(self.call('DELETE',item,{'confirm_memory_id':mid,'version':1})[0],400)
        self.assertEqual(list(self.repo._conn.iterdump()),before)
        self.assertEqual(self.call('DELETE',item,{'confirm_memory_id':mid,'version':2})[0],200)
        self.assertNotIn('SINTETICA',repr(list(self.repo._conn.iterdump())))
        self.assertEqual(json.loads(self.call('GET',path)[2])['data'],[])

    def test_delivery_failure_preparation_and_persistence_are_recoverable(self):
        import io
        from unittest.mock import Mock, patch
        from app.http_api import OminAIHTTPRequestHandler
        self.assertEqual(self.decide()[0],200)
        body=json.loads(self.call('POST',self.base+'/execute')[2])['data']
        self.assertEqual(self.decide(body['approval_request'])[0],200)
        prepared=self.call('GET',self.base+'/vbp/export')
        before=list(self.repo._conn.iterdump())
        for failure in ('write','flush','headers'):
            handler=object.__new__(OminAIHTTPRequestHandler)
            handler.router=Mock();handler.router.dispatch.return_value=prepared
            handler.path=self.base+'/vbp/export';handler.headers={}
            handler._read_bounded_body=lambda:b''
            handler.send_response=Mock();handler.send_header=Mock();handler.end_headers=Mock()
            handler.wfile=Mock();handler.wfile.write.return_value=len(prepared[2])
            target=handler.end_headers if failure=='headers' else getattr(handler.wfile,failure)
            target.side_effect=BrokenPipeError('SIMULADA')
            handler._handle_request('GET')
            self.assertEqual(list(self.repo._conn.iterdump()),before)
        for method in ('save_mission','save_event','save_checkpoint','put_object'):
            with patch.object(self.repo,method,side_effect=RuntimeError('SIMULADA')):
                self.assertFalse(prepared.on_delivered())
            self.assertEqual(list(self.repo._conn.iterdump()),before)
        with patch('app.vbp_export.export_canonical_vbp_bytes',side_effect=ValueError('SIMULADA')):
            self.assertEqual(self.call('GET',self.base+'/vbp/export')[0],500)
        self.assertEqual(list(self.repo._conn.iterdump()),before)
        self.assertTrue(prepared.on_delivered())
        fresh=self.call('GET',self.base+'/vbp/export')
        self.assertEqual(fresh[0],200)
        self.assertTrue(fresh.on_delivered())
        after_fresh=list(self.repo._conn.iterdump())
        self.assertTrue(fresh.on_delivered())
        self.assertEqual(list(self.repo._conn.iterdump()),after_fresh)
        self.assertEqual(self.call('GET',self.base+'/vbp/export')[2],fresh[2])

class TestBoundedHTTPBody(unittest.TestCase):
    def test_invalid_lengths_never_read_payload(self):
        from email.message import Message
        from unittest.mock import Mock
        from app.http_api import OminAIHTTPRequestHandler
        for value,error in (("51201",OverflowError),("-1",ValueError),("abc",ValueError),("9"*30,ValueError)):
            handler=object.__new__(OminAIHTTPRequestHandler);handler.headers=Message()
            handler.headers["Content-Length"]=value;handler.rfile=Mock();handler.connection=Mock()
            with self.assertRaises(error):handler._read_bounded_body()
            handler.rfile.read1.assert_not_called()
    def test_slow_read_is_bounded_and_no_success(self):
        from email.message import Message
        from unittest.mock import Mock
        from app.http_api import OminAIHTTPRequestHandler
        handler=object.__new__(OminAIHTTPRequestHandler);handler.headers=Message()
        handler.headers["Content-Length"]="1";handler.rfile=Mock();handler.connection=Mock()
        handler.rfile.read1.side_effect=TimeoutError()
        with self.assertRaises(TimeoutError):handler._read_bounded_body()
        handler.connection.settimeout.assert_called_once_with(.5)

if __name__=="__main__": unittest.main()
