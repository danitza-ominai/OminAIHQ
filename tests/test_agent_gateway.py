"""Pruebas exhaustivas para el Adaptador Gateway y control de presupuesto de modelos (PZ-004A).

Valida escenarios de exito, schema invalido, reintentos en 429 transitorio,
rechazo de secretos en prompts, rechazo de Chain-of-Thought en respuestas,
control de umbrales 70/90/100, techo de 15 solicitudes y aislamiento offline.
"""

import json
import os
import unittest
from unittest.mock import patch

import app.agent_gateway as agent_gateway
import app.runtime_config as runtime_config


class TestAgentGateway(unittest.TestCase):
    """Suite de pruebas para PZ-004A."""

    def setUp(self) -> None:
        self.config = runtime_config.RuntimeConfig(
            model_id="gemini-2.5-pro",
            max_budget_usd=25.0,
            max_agent_requests=15,
            timeout_seconds=300,
            max_retries=2,
        )

    def test_ac01_mock_provider_success_and_error_modes(self) -> None:
        """AC-01: Probar respuestas de exito, schema invalido, timeout y 429 transitorio."""
        # 1. Caso de exito
        mock_provider = agent_gateway.MockModelClientProvider()
        gateway = agent_gateway.AgentGateway(config=self.config, provider=mock_provider)

        ok, result, err = gateway.execute_agent_call(
            system_instruction="Eres un asistente.",
            prompt="Genera el resumen de la mision.",
        )
        self.assertTrue(ok)
        self.assertIsNotNone(result)
        self.assertIn("summary", result["content"])
        self.assertEqual(result["attempts"], 1)

        # 2. Caso de salida JSON no parseable (SCHEMA_INVALID)
        mock_provider_bad_json = agent_gateway.MockModelClientProvider(
            responses=[
                agent_gateway.ModelCallResponse(
                    content="Esto no es un json valido",
                    input_tokens=100,
                    output_tokens=50,
                    status_code=200,
                )
            ]
        )
        gw_bad = agent_gateway.AgentGateway(config=self.config, provider=mock_provider_bad_json)
        ok_j, res_j, err_j = gw_bad.execute_agent_call(
            system_instruction="Sistema",
            prompt="Prompt",
        )
        self.assertFalse(ok_j)
        self.assertEqual(err_j["error_code"], "SCHEMA_INVALID")

        # 3. Caso 429 transitorio recuperado en segundo intento
        mock_provider_retry = agent_gateway.MockModelClientProvider(
            responses=[
                agent_gateway.ModelCallResponse(
                    content="",
                    input_tokens=0,
                    output_tokens=0,
                    status_code=429,
                    error_message="Cuota saturada",
                    is_transient=True,
                ),
                agent_gateway.ModelCallResponse(
                    content='{"status": "recuperado"}',
                    input_tokens=120,
                    output_tokens=40,
                    status_code=200,
                ),
            ]
        )
        gw_retry = agent_gateway.AgentGateway(config=self.config, provider=mock_provider_retry)
        ok_r, res_r, err_r = gw_retry.execute_agent_call(
            system_instruction="Sistema",
            prompt="Prompt con reintento",
        )
        self.assertTrue(ok_r)
        self.assertEqual(res_r["attempts"], 2)

    def test_ac02_credentials_check_and_permission_denied(self) -> None:
        """AC-02: Comprobar deteccion de credenciales y manejo de error 401/403."""
        # 1. Sin variables de entorno -> has_valid_credentials() es False
        with patch.dict(os.environ, {}, clear=True):
            cfg = runtime_config.RuntimeConfig()
            self.assertFalse(cfg.has_valid_credentials())

        # 2. Con variable de entorno -> has_valid_credentials() es True
        with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_test_key_123"}, clear=True):
            cfg = runtime_config.RuntimeConfig()
            self.assertTrue(cfg.has_valid_credentials())

        # 3. Respuesta 401 de proveedor produce PERMISSION_DENIED
        mock_provider_401 = agent_gateway.MockModelClientProvider(
            responses=[
                agent_gateway.ModelCallResponse(
                    content="",
                    input_tokens=0,
                    output_tokens=0,
                    status_code=401,
                    error_message="Clave no valida",
                )
            ]
        )
        gw = agent_gateway.AgentGateway(config=self.config, provider=mock_provider_401)
        ok, res, err = gw.execute_agent_call("Sys", "Prompt")
        self.assertFalse(ok)
        self.assertEqual(err["error_code"], "PERMISSION_DENIED")

    def test_ac03_budget_thresholds_and_request_limits(self) -> None:
        """AC-03: Comprobar alertas en 70%, 90%, 100% y bloqueo al superar 15 solicitudes."""
        low_cfg=runtime_config.RuntimeConfig(max_budget_usd=1, max_agent_requests=3,
            pricing_table={"gemini-2.5-pro":(1,1)})
        low_cfg.max_input_tokens=720000;low_cfg.max_output_tokens=0
        provider=agent_gateway.MockModelClientProvider([
            agent_gateway.ModelCallResponse("{}",720000,0),
            agent_gateway.ModelCallResponse("{}",200000,0)])
        gw=agent_gateway.AgentGateway(config=low_cfg,provider=provider)
        self.assertTrue(gw.execute_agent_call("Sys","P1")[0])
        self.assertIn(.70,gw.alerts_emitted)
        low_cfg.max_input_tokens=200000
        self.assertTrue(gw.execute_agent_call("Sys","P2")[0])
        self.assertIn(.90,gw.alerts_emitted)
        self.assertFalse(gw.execute_agent_call("Sys","P3")[0])
        self.assertEqual(len(provider.call_history),2)
        self.assertEqual(low_cfg.check_threshold_alert(1),1.0)
        # Contract pauses at 90 percent; an actual overspend is NOT a success fixture.

    def test_ac04_outbound_sanitization_and_cot_rejection(self) -> None:
        """AC-04: Rechazar secretos en el prompt saliente y rechazar etiquetas CoT en la respuesta."""
        mock_provider = agent_gateway.MockModelClientProvider()
        gw = agent_gateway.AgentGateway(config=self.config, provider=mock_provider)

        # 1. Prompt con secreto inyectado
        ok_sec, _, err_sec = gw.execute_agent_call(
            system_instruction="Sistema",
            prompt="Mi clave secreta es api_key = 'AIzaSyD982347289347289347293472934'",
        )
        self.assertFalse(ok_sec)
        self.assertEqual(err_sec["error_code"], "PERMISSION_DENIED")

        # 2. Respuesta que contiene <thought>
        mock_provider_cot = agent_gateway.MockModelClientProvider(
            responses=[
                agent_gateway.ModelCallResponse(
                    content="<thought>Razonamiento interno que debe rechazarse</thought>{\"res\": 1}",
                    input_tokens=100,
                    output_tokens=50,
                    status_code=200,
                )
            ]
        )
        gw_cot = agent_gateway.AgentGateway(config=self.config, provider=mock_provider_cot)
        ok_c, _, err_c = gw_cot.execute_agent_call("Sys", "Prompt normal")
        self.assertFalse(ok_c)
        self.assertEqual(err_c["error_code"], "SCHEMA_INVALID")
        self.assertIn("Chain-of-Thought", err_c["message"])

    def test_ac05_real_integration_status_flag(self) -> None:
        """AC-05: Sin clave real o ejecucion opt-in explicita, la integracion se reporta como REAL_NO_VERIFICADA."""
        with patch.dict(os.environ, {}, clear=True):
            cfg = runtime_config.RuntimeConfig()
            status = "REAL_VERIFICADA" if cfg.has_valid_credentials() else "REAL_NO_VERIFICADA"
            self.assertEqual(status, "REAL_NO_VERIFICADA")


class TestDurableBudget(unittest.TestCase):
    def test_configured_integrated_instances_reopen_and_concurrent_reservations(self):
        import os, tempfile
        from pathlib import Path
        from unittest.mock import patch
        from concurrent.futures import ThreadPoolExecutor
        from app.hq_runtime import HQRuntime
        from app.local_repository import LocalRepository
        with tempfile.TemporaryDirectory() as td:
            path=str(Path(td)/'shared.db')
            with patch.dict(os.environ, {'OMINAI_LOCAL_DEMO':'1','OMINAI_LOCAL_DB':path}):
                a=HQRuntime();b=HQRuntime();g=agent_gateway.AgentGateway()
                self.assertEqual(a.repository.db_path,b.repository.db_path)
                self.assertEqual(g.repository.db_path,b.repository.db_path)
                key=a.repository.reserve_call('A','T0',2);a.repository.reconcile_call(key,2)
                def reserve(repo):
                    try:repo.reserve_call('B','T1',20);return True
                    except ValueError:return False
                with ThreadPoolExecutor(max_workers=2) as pool:
                    results=list(pool.map(reserve,[a.repository,b.repository]))
                self.assertEqual(sum(results),1)
                self.assertEqual(a.repository.budget_snapshot(),b.repository.budget_snapshot())
                a.repository.close();b.repository.close();g.repository.close()
                c=HQRuntime()
                self.assertEqual(c.repository.budget_snapshot()['spent_usd'],2)
                self.assertEqual(c.repository.budget_snapshot()['reserved_usd'],20)
                before=list(c.repository._conn.iterdump())
                with self.assertRaises(ValueError):c.repository.reserve_call('C','T2',4)
                self.assertEqual(list(c.repository._conn.iterdump()),before)
                c.repository.close()
            with patch.dict(os.environ, {'OMINAI_LOCAL_DEMO':'1','OMINAI_LOCAL_DB':''}):
                with self.assertRaises(ValueError):HQRuntime()
                isolated=LocalRepository(':memory:');isolated.close()
    def test_retry_counts_before_each_call_and_two_attempts(self):
        from app.local_repository import LocalRepository
        repo=LocalRepository();self.addCleanup(repo.close)
        cfg=runtime_config.RuntimeConfig(max_agent_requests=1,max_retries=20)
        provider=agent_gateway.MockModelClientProvider([agent_gateway.ModelCallResponse("",0,0,status_code=429)])
        gw=agent_gateway.AgentGateway(cfg,provider,repository=repo)
        self.assertFalse(gw.execute_agent_call("s","p",task_id="T")[0])
        self.assertEqual(len(provider.call_history),1);self.assertEqual(repo.get_object("usage",gw.mission_id)["requests"],1)
        repo2=LocalRepository();self.addCleanup(repo2.close)
        gw2=agent_gateway.AgentGateway(repository=repo2)
        for _ in range(2):self.assertTrue(gw2.execute_agent_call("s","p",task_id="T")[0])
        self.assertFalse(gw2.execute_agent_call("s","p",task_id="T")[0])
        self.assertEqual(len(gw2.provider.call_history),2)
    def test_budget_shared_between_connections_and_restart(self):
        import tempfile
        from pathlib import Path
        from app.local_repository import LocalRepository
        with tempfile.TemporaryDirectory() as td:
            path=str(Path(td)/"budget.db")
            a=LocalRepository(path);b=LocalRepository(path)
            key=a.reserve_call("A","A",17.5);a.reconcile_call(key,17.5)
            key=b.reserve_call("B","B",5);b.reconcile_call(key,5)
            with self.assertRaises(ValueError):a.reserve_call("A","C",.01)
            a.close();b.close();c=LocalRepository(path)
            self.assertEqual(c.budget_snapshot()["spent_usd"],22.5)
            with self.assertRaises(ValueError):c.reserve_call("C","C",.01)
            c.close()
    def test_simultaneous_reservations_never_overcommit(self):
        from concurrent.futures import ThreadPoolExecutor
        from app.local_repository import LocalRepository
        repo=LocalRepository();self.addCleanup(repo.close)
        def reserve(i):
            try:repo.reserve_call(str(i),str(i),20);return True
            except ValueError:return False
        with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(reserve,range(2)))
        self.assertEqual(sum(results),1);self.assertEqual(repo.budget_snapshot()["reserved_usd"],20)
    def test_unknown_call_retains_reservation_and_never_retries(self):
        from unittest.mock import patch
        gw=agent_gateway.AgentGateway()
        with patch.object(gw.provider,"call_model",side_effect=TimeoutError("SIMULADA")) as provider:
            self.assertFalse(gw.execute_agent_call("s","p",task_id="T")[0]);self.assertEqual(provider.call_count,1)
        self.assertGreater(gw.repository.budget_snapshot()["reserved_usd"],0)


class FakeRealProvider(agent_gateway.ModelClientProvider):
    provider_kind = "ADK_REAL"

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def has_credentials(self):
        return True

    def preflight(self):
        return True, None

    def call_model(self, model_name, system_instruction, prompt, timeout_seconds,
                   *, max_output_tokens=4096, response_schema=None):
        self.calls.append({"model": model_name, "timeout": timeout_seconds,
                           "max_output_tokens": max_output_tokens,
                           "schema": response_schema})
        return self.responses.pop(0)


class PersistedAuthorityValidator(agent_gateway.RealExecutionAuthorizationValidator):
    """Adaptador offline: valida referencias contra un registro durable de prueba."""

    def __init__(self, repository, *, mission_id, task_id, owner_id, approval_id,
                 current=True, decision="APROBAR"):
        self.repository = repository
        self.calls = []
        repository.put_object("test_real_mandate", approval_id, {
            "mission_id": mission_id,
            "task_id": task_id,
            "owner_id": owner_id,
            "approval_id": approval_id,
            "decision": decision,
            "persisted": True,
            "is_current": current,
        })

    def validate(self, *, mission_id, task_id, owner_id, approval_id):
        self.calls.append((mission_id, task_id, owner_id, approval_id))
        record = self.repository.get_object("test_real_mandate", approval_id)
        if not record:
            return None
        return agent_gateway.ValidatedRealExecutionMandate(**record)


class RepositoryIdempotencyStore(agent_gateway.DurableCallIdempotencyStore):
    """Adaptador durable de prueba sobre el repositorio; no es cache del gateway."""

    KIND = "test_real_idempotency"

    def __init__(self, repository):
        self.repository = repository

    @staticmethod
    def _key(mission_id, task_id):
        return mission_id + "::" + task_id

    def begin(self, *, mission_id, task_id):
        key = self._key(mission_id, task_id)
        with self.repository.transaction():
            record = self.repository.get_object(self.KIND, key)
            if record is None:
                self.repository.put_object(self.KIND, key, {"state": "IN_PROGRESS"})
                return "NEW", None
            if record["state"] == "TERMINAL":
                value = record["outcome"]
                return "REPLAY", agent_gateway.PersistedCallOutcome(
                    value["ok"], value["result"], value["error"]
                )
            return "IN_PROGRESS", None

    def complete(self, *, mission_id, task_id, outcome):
        key = self._key(mission_id, task_id)
        with self.repository.transaction():
            record = self.repository.get_object(self.KIND, key)
            if not record or record["state"] != "IN_PROGRESS":
                raise ValueError("Clave no reclamada o ya terminal.")
            self.repository.put_object(self.KIND, key, {
                "state": "TERMINAL",
                "outcome": {
                    "ok": outcome.ok,
                    "result": outcome.result,
                    "error": outcome.error,
                },
            })


class TestRealGatewayBoundary(unittest.TestCase):
    MISSION = "MSN-REAL-001"
    TASK = "TSK-REAL-001"
    OWNER = "USR-NIKO"
    APPROVAL = "APR-REAL-001"

    def make_config(self, **kwargs):
        return runtime_config.RuntimeConfig(execution_mode="REAL", **kwargs)

    def controls(self, repo, **kwargs):
        validator = PersistedAuthorityValidator(
            repo,
            mission_id=self.MISSION,
            task_id=self.TASK,
            owner_id=self.OWNER,
            approval_id=self.APPROVAL,
            **kwargs,
        )
        return validator, RepositoryIdempotencyStore(repo)

    def execute_real(self, gateway, **kwargs):
        values = {
            "mission_id": self.MISSION,
            "task_id": self.TASK,
            "owner_id": self.OWNER,
            "approval_id": self.APPROVAL,
        }
        values.update(kwargs)
        return gateway.execute_agent_call("s", "p", **values)

    def test_boolean_alone_cannot_authorize_real_call_and_has_no_effect(self):
        from app.local_repository import LocalRepository
        repo = LocalRepository(); self.addCleanup(repo.close)
        provider = FakeRealProvider([
            agent_gateway.ModelCallResponse('{"status":"ok"}', 10, 20)
        ])
        gateway = agent_gateway.AgentGateway(
            self.make_config(), provider, repository=repo,
            real_execution_authorized=True,
        )
        before = repo.budget_snapshot()
        ok, _, error = self.execute_real(gateway)
        self.assertFalse(ok)
        self.assertEqual(error["error_code"], "PERMISSION_DENIED")
        self.assertEqual(provider.calls, [])
        self.assertEqual(repo.budget_snapshot(), before)

    def test_stale_or_mismatched_persisted_mandate_has_no_effect(self):
        from app.local_repository import LocalRepository
        for controls_kwargs, changed_owner in (({"current": False}, False), ({}, True)):
            with self.subTest(controls_kwargs=controls_kwargs, changed_owner=changed_owner):
                repo = LocalRepository()
                provider = FakeRealProvider([
                    agent_gateway.ModelCallResponse('{"status":"ok"}', 10, 20)
                ])
                validator, store = self.controls(repo, **controls_kwargs)
                gateway = agent_gateway.AgentGateway(
                    self.make_config(), provider, repository=repo,
                    real_authorization_validator=validator,
                    idempotency_store=store,
                )
                before = repo.budget_snapshot()
                owner = "USR-OTRO" if changed_owner else self.OWNER
                ok, _, error = self.execute_real(gateway, owner_id=owner)
                self.assertFalse(ok)
                self.assertEqual(error["error_code"], "PERMISSION_DENIED")
                self.assertEqual(provider.calls, [])
                self.assertEqual(repo.budget_snapshot(), before)
                repo.close()

    def test_authorized_real_call_is_labeled_unverified_and_reconciled(self):
        from app.local_repository import LocalRepository
        repo = LocalRepository(); self.addCleanup(repo.close)
        provider = FakeRealProvider([
            agent_gateway.ModelCallResponse('{"status":"ok"}', 100, 60)
        ])
        validator, store = self.controls(repo)
        gateway = agent_gateway.AgentGateway(
            self.make_config(), provider, repository=repo,
            real_execution_authorized=True,
            real_authorization_validator=validator,
            idempotency_store=store,
        )
        schema = {
            "type": "object",
            "required": ["status"],
            "properties": {"status": {"const": "ok"}},
            "additionalProperties": False,
        }
        ok, result, error = self.execute_real(gateway, response_schema=schema)
        self.assertTrue(ok, error)
        self.assertEqual(result["execution_evidence"], "REAL_NO_VERIFICADA")
        self.assertEqual(result["cost_kind"], "REAL_ESTIMADA")
        self.assertEqual(result["cost_usd"], 0.00069)
        self.assertEqual(provider.calls[0]["timeout"], 45)
        self.assertEqual(provider.calls[0]["max_output_tokens"], 4096)
        self.assertEqual(repo.budget_snapshot()["reserved_usd"], 0)

    def test_missing_model_tariff_schema_or_oversize_fails_before_call(self):
        from app.local_repository import LocalRepository
        cases = [
            (self.make_config(model_id="gemini-otra"), "s", "p", None),
            (self.make_config(pricing_table={}), "s", "p", None),
            (self.make_config(), "s", "p", []),
            (self.make_config(max_input_tokens=1), "ss", "p", None),
        ]
        for index, (config, system, prompt, schema) in enumerate(cases):
            with self.subTest(index=index):
                repo = LocalRepository()
                provider = FakeRealProvider([
                    agent_gateway.ModelCallResponse("{}", 0, 0)
                ])
                validator, store = self.controls(repo)
                gateway = agent_gateway.AgentGateway(
                    config, provider, repository=repo,
                    real_execution_authorized=True,
                    real_authorization_validator=validator,
                    idempotency_store=store,
                )
                ok, _, _ = gateway.execute_agent_call(
                    system, prompt,
                    mission_id=self.MISSION, task_id=self.TASK,
                    owner_id=self.OWNER, approval_id=self.APPROVAL,
                    response_schema=schema,
                )
                self.assertFalse(ok)
                self.assertEqual(provider.calls, [])
                self.assertEqual(repo.budget_snapshot()["requests"], 0)
                repo.close()

    def test_unknown_usage_retains_reservation_and_replay_makes_no_second_call(self):
        from app.local_repository import LocalRepository
        repo = LocalRepository(); self.addCleanup(repo.close)
        provider = FakeRealProvider([
            agent_gateway.ModelCallResponse(
                "", 0, 0, status_code=503, is_transient=True,
                usage_confirmed=False,
            )
        ])
        validator, store = self.controls(repo)
        gateway = agent_gateway.AgentGateway(
            self.make_config(), provider, repository=repo,
            real_execution_authorized=True,
            real_authorization_validator=validator,
            idempotency_store=store,
        )
        self.assertFalse(self.execute_real(gateway)[0])
        self.assertGreater(repo.budget_snapshot()["reserved_usd"], 0)
        self.assertFalse(self.execute_real(gateway)[0])
        self.assertEqual(len(provider.calls), 1)

    def test_unknown_401_is_permission_denied_retains_reservation_and_never_retries(self):
        from app.local_repository import LocalRepository
        repo = LocalRepository(); self.addCleanup(repo.close)
        provider = FakeRealProvider([
            agent_gateway.ModelCallResponse(
                "", 0, 0, status_code=401,
                error_message="key=credencial-secreta",
                usage_confirmed=False,
            )
        ])
        validator, store = self.controls(repo)
        gateway = agent_gateway.AgentGateway(
            self.make_config(), provider, repository=repo,
            real_authorization_validator=validator,
            idempotency_store=store,
        )
        ok, _, error = self.execute_real(gateway)
        self.assertFalse(ok)
        self.assertEqual(error["error_code"], "PERMISSION_DENIED")
        self.assertNotIn("credencial", str(error).lower())
        self.assertEqual(len(provider.calls), 1)
        self.assertEqual(repo.budget_snapshot()["requests"], 1)
        self.assertGreater(repo.budget_snapshot()["reserved_usd"], 0)
        self.assertFalse(self.execute_real(gateway)[0])
        self.assertEqual(len(provider.calls), 1)

    def test_confirmed_transient_gets_one_retry_and_each_attempt_is_counted(self):
        from app.local_repository import LocalRepository
        repo = LocalRepository(); self.addCleanup(repo.close)
        provider = FakeRealProvider([
            agent_gateway.ModelCallResponse(
                "", 0, 0, status_code=429, is_transient=True
            ),
            agent_gateway.ModelCallResponse('{"status":"ok"}', 2, 3),
        ])
        validator, store = self.controls(repo)
        gateway = agent_gateway.AgentGateway(
            self.make_config(), provider, repository=repo,
            real_execution_authorized=True,
            real_authorization_validator=validator,
            idempotency_store=store,
        )
        ok, result, error = self.execute_real(gateway)
        self.assertTrue(ok, error)
        self.assertEqual(result["attempts"], 2)
        self.assertEqual(len(provider.calls), 2)
        self.assertEqual(repo.budget_snapshot()["requests"], 2)
        self.assertEqual(repo.budget_snapshot()["reserved_usd"], 0)

    def test_invalid_schema_tool_and_sensitive_output_are_rejected_after_usage(self):
        from app.local_repository import LocalRepository
        outputs = [
            '{"status":"wrong"}',
            '{"tool_calls":[{"name":"send"}]}',
            '{"status":"AIza12345678901234567890123456789012345"}',
        ]
        schema = {
            "type": "object", "required": ["status"],
            "properties": {"status": {"const": "ok"}},
        }
        for index, output in enumerate(outputs):
            with self.subTest(index=index):
                repo = LocalRepository()
                provider = FakeRealProvider([
                    agent_gateway.ModelCallResponse(output, 2, 3)
                ])
                validator, store = self.controls(repo)
                gateway = agent_gateway.AgentGateway(
                    self.make_config(), provider, repository=repo,
                    real_execution_authorized=True,
                    real_authorization_validator=validator,
                    idempotency_store=store,
                )
                ok, _, error = self.execute_real(gateway, response_schema=schema)
                self.assertFalse(ok)
                self.assertEqual(error["error_code"], "SCHEMA_INVALID")
                self.assertEqual(repo.budget_snapshot()["requests"], 1)
                self.assertEqual(repo.budget_snapshot()["reserved_usd"], 0)
                repo.close()

    def test_successful_external_replay_after_restart_returns_persisted_result(self):
        import tempfile
        from pathlib import Path
        from app.local_repository import LocalRepository

        with tempfile.TemporaryDirectory() as td:
            path = str(Path(td) / "gateway-idempotency.db")
            provider = FakeRealProvider([
                agent_gateway.ModelCallResponse('{"status":"ok"}', 2, 3)
            ])
            repo1 = LocalRepository(path)
            validator1, store1 = self.controls(repo1)
            gateway1 = agent_gateway.AgentGateway(
                self.make_config(), provider, repository=repo1,
                real_authorization_validator=validator1,
                idempotency_store=store1,
            )
            first = self.execute_real(gateway1)
            self.assertTrue(first[0], first[2])
            snapshot = repo1.budget_snapshot()
            repo1.close()

            repo2 = LocalRepository(path)
            validator2 = PersistedAuthorityValidator(
                repo2, mission_id=self.MISSION, task_id=self.TASK,
                owner_id=self.OWNER, approval_id=self.APPROVAL,
            )
            gateway2 = agent_gateway.AgentGateway(
                self.make_config(), provider, repository=repo2,
                real_authorization_validator=validator2,
                idempotency_store=RepositoryIdempotencyStore(repo2),
            )
            second = self.execute_real(gateway2)
            self.assertEqual(second, first)
            self.assertEqual(len(provider.calls), 1)
            self.assertEqual(repo2.budget_snapshot(), snapshot)
            repo2.close()

if __name__ == "__main__":
    unittest.main()
