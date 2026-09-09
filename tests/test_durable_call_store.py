"""REAL-01: recuperacion durable ligada a autoridad persistida vigente.

Las aprobaciones se generan con HumanApprovalEngine a traves de HQRuntime. El
proveedor ADK_REAL de este modulo es un doble controlado exclusivamente local.
"""

import copy
import hashlib
import tempfile
import threading
import unittest
from pathlib import Path

import app.agent_gateway as agent_gateway
import app.runtime_config as runtime_config
from app.durable_call_store import RepositoryDurableCallStore
from app.local_repository import LocalRepository
from app.real_execution_authority import LocalApprovalRecordValidator
from app.vbp_validation import task_from_plan
from tests.test_real_execution_authority import (
    MISSION_ID,
    PROFILE,
    TASK_ID,
    create_approved_plan,
)


_CALL_KIND = "real_call_idempotency"
_CALL_KEY = MISSION_ID + "::" + TASK_ID
_TEST_SCHEMA = {
    "type": "object",
    "properties": {"status": {"type": "string"}},
    "required": ["status"],
    "additionalProperties": False,
}
_OK_RESPONSE_JSON = '{"status":"ok"}'


def fingerprint(label):
    return "sha256:" + hashlib.sha256(label.encode("utf-8")).hexdigest()


def approved_environment(repo):
    runtime, context, request, response, mission = create_approved_plan(repo)
    validator = LocalApprovalRecordValidator(repo)
    store = RepositoryDurableCallStore(
        repo,
        authorized_content_fingerprint=request["fingerprint"],
        authorization_validator=validator,
    )
    return runtime, context, request, response, mission, validator, store


def approve_changed_plan(repo, runtime, context, label="contenido cambiado"):
    """Crea una segunda aprobacion real y coherente mediante HumanApprovalEngine."""
    mission = repo.get_mission(MISSION_ID)
    mission.update(status="PLAN_EN_REVISION", current_state="PLAN_EN_REVISION")
    ok, error = repo.save_mission(mission)
    if not ok:
        raise AssertionError(error)

    mission = repo.get_mission(MISSION_ID)
    mission["plan"]["tasks"][0]["objective"] = label
    mission["tasks"] = [
        task_from_plan(plan_task, mission["nuclear"])
        for plan_task in mission["plan"]["tasks"]
    ]
    ok, error = repo.save_mission(mission)
    if not ok:
        raise AssertionError(error)

    mission = repo.get_mission(MISSION_ID)
    candidate = {"brief": mission["brief"], "plan": mission["plan"]}
    ok, request, error = runtime.approvals.create_approval_request(
        MISSION_ID, "GATE_1_PLAN", candidate
    )
    if not ok:
        raise AssertionError(error)
    mission = repo.get_mission(MISSION_ID)
    mission.update(
        plan_fingerprint=request["fingerprint"],
        approval_id=request["approval_id"],
        idempotency_key=request["idempotency_key"],
    )
    ok, error = repo.save_mission(mission)
    if not ok:
        raise AssertionError(error)
    ok, _, error = runtime.approvals.submit_human_decision(
        request, "APROBAR", context=context
    )
    if not ok:
        raise AssertionError(error)
    return request


class ControlledRealProvider(agent_gateway.ModelClientProvider):
    """Doble determinista local; nunca constituye evidencia real de Gemini."""

    provider_kind = "ADK_REAL"

    def __init__(self, responses):
        self.responses = list(responses)
        self.call_count = 0

    def has_credentials(self):
        return True

    def preflight(self):
        return True, None

    def call_model(
        self,
        model_name,
        system_instruction,
        prompt,
        timeout_seconds,
        *,
        max_output_tokens=4096,
        response_schema=None,
    ):
        self.call_count += 1
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


class BlockingRealProvider(ControlledRealProvider):
    def __init__(self, response):
        super().__init__([response])
        self.entered = threading.Event()
        self.release = threading.Event()

    def call_model(self, *args, **kwargs):
        self.entered.set()
        if not self.release.wait(5):
            raise RuntimeError("El test no libero al proveedor controlado.")
        return super().call_model(*args, **kwargs)


class StoreTestCase(unittest.TestCase):
    def make_repo(self, path=":memory:"):
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        return repo

    @staticmethod
    def outcome():
        return agent_gateway.PersistedCallOutcome(
            ok=True,
            result={"content": {"status": "ok"}, "model": "controlled"},
            error=None,
        )

    @staticmethod
    def make_gateway(repo, provider, request):
        validator = LocalApprovalRecordValidator(repo)
        store = RepositoryDurableCallStore(
            repo,
            authorized_content_fingerprint=request["fingerprint"],
            authorization_validator=validator,
        )
        gateway = agent_gateway.AgentGateway(
            runtime_config.RuntimeConfig(execution_mode="REAL"),
            provider,
            repository=repo,
            real_authorization_validator=validator,
            idempotency_store=store,
        )
        return gateway, store

    @staticmethod
    def call(gateway, approval_id):
        return gateway.execute_agent_call(
            "s",
            "p",
            mission_id=MISSION_ID,
            task_id=TASK_ID,
            owner_id=PROFILE["user_id"],
            approval_id=approval_id,
            response_schema=_TEST_SCHEMA,
        )


class TestRepositoryDurableCallStore(StoreTestCase):
    def setUp(self):
        self.repo = self.make_repo()
        (
            self.runtime,
            self.context,
            self.request,
            _,
            _,
            self.validator,
            self.store,
        ) = approved_environment(self.repo)

    def test_same_plan_replays_identically_and_preserves_original_record(self):
        self.assertEqual(
            self.store.begin(mission_id=MISSION_ID, task_id=TASK_ID),
            ("NEW", None),
        )
        expected = self.outcome()
        self.store.complete(mission_id=MISSION_ID, task_id=TASK_ID, outcome=expected)
        original = self.repo.get_object(_CALL_KIND, _CALL_KEY)

        state, recovered = self.store.begin(mission_id=MISSION_ID, task_id=TASK_ID)

        self.assertEqual((state, recovered), ("REPLAY", expected))
        self.assertEqual(self.repo.get_object(_CALL_KIND, _CALL_KEY), original)
        self.assertEqual(original["mission_id"], MISSION_ID)
        self.assertEqual(original["task_id"], TASK_ID)
        self.assertEqual(original["authorized_fp"], self.request["fingerprint"])

    def test_in_progress_and_unknown_states_fail_closed_without_reset(self):
        self.assertEqual(
            self.store.begin(mission_id=MISSION_ID, task_id=TASK_ID)[0], "NEW"
        )
        original = self.repo.get_object(_CALL_KIND, _CALL_KEY)
        self.assertEqual(
            self.store.begin(mission_id=MISSION_ID, task_id=TASK_ID),
            ("IN_PROGRESS", None),
        )
        self.assertEqual(self.repo.get_object(_CALL_KIND, _CALL_KEY), original)

        corrupt = copy.deepcopy(original)
        corrupt["state"] = "DESCONOCIDO"
        self.repo.put_object(_CALL_KIND, _CALL_KEY, corrupt)
        self.assertEqual(
            self.store.begin(mission_id=MISSION_ID, task_id=TASK_ID),
            ("ERROR", None),
        )
        self.assertEqual(self.repo.get_object(_CALL_KIND, _CALL_KEY), corrupt)

    def test_terminal_result_cannot_be_overwritten(self):
        self.store.begin(mission_id=MISSION_ID, task_id=TASK_ID)
        original = self.outcome()
        self.store.complete(mission_id=MISSION_ID, task_id=TASK_ID, outcome=original)
        record = self.repo.get_object(_CALL_KIND, _CALL_KEY)

        with self.assertRaises(ValueError):
            self.store.complete(
                mission_id=MISSION_ID,
                task_id=TASK_ID,
                outcome=agent_gateway.PersistedCallOutcome(
                    ok=False, result=None, error={"error_code": "ALTERADO"}
                ),
            )
        self.assertEqual(self.repo.get_object(_CALL_KIND, _CALL_KEY), record)

    def test_complete_does_not_replace_acquired_identity(self):
        self.store.begin(mission_id=MISSION_ID, task_id=TASK_ID)
        record = self.repo.get_object(_CALL_KIND, _CALL_KEY)
        record["task_id"] = "TSK-ALTERADA"
        self.repo.put_object(_CALL_KIND, _CALL_KEY, record)

        with self.assertRaises(ValueError):
            self.store.complete(
                mission_id=MISSION_ID, task_id=TASK_ID, outcome=self.outcome()
            )

        self.assertEqual(self.repo.get_object(_CALL_KIND, _CALL_KEY), record)

    def test_complete_without_begin_is_rejected(self):
        with self.assertRaises(ValueError):
            self.store.complete(
                mission_id=MISSION_ID, task_id=TASK_ID, outcome=self.outcome()
            )
        self.assertIsNone(self.repo.get_object(_CALL_KIND, _CALL_KEY))

    def test_missing_malformed_or_unapproved_fingerprint_never_acquires(self):
        for value in (None, "", "sha256:no-es-hash", "SHA256:" + "a" * 64):
            with self.subTest(source="constructor", value=value):
                store = RepositoryDurableCallStore(
                    self.repo,
                    authorized_content_fingerprint=value,
                    authorization_validator=self.validator,
                )
                self.assertEqual(
                    store.begin(mission_id=MISSION_ID, task_id=TASK_ID),
                    ("ERROR", None),
                )
                self.assertIsNone(self.repo.get_object(_CALL_KIND, _CALL_KEY))

        never_approved = fingerprint("nunca aprobado")
        store = RepositoryDurableCallStore(
            self.repo,
            authorized_content_fingerprint=never_approved,
            authorization_validator=self.validator,
        )
        self.assertEqual(
            store.begin(mission_id=MISSION_ID, task_id=TASK_ID),
            ("CONTENT_CHANGED", None),
        )
        self.assertIsNone(self.repo.get_object(_CALL_KIND, _CALL_KEY))

        empty_repo = self.make_repo()
        store = RepositoryDurableCallStore(
            empty_repo, authorized_content_fingerprint=never_approved
        )
        self.assertEqual(
            store.begin(mission_id=MISSION_ID, task_id=TASK_ID),
            ("ERROR", None),
        )
        self.assertIsNone(empty_repo.get_object(_CALL_KIND, _CALL_KEY))

    def test_missing_or_malformed_persisted_fingerprint_never_acquires(self):
        for value in (None, "sha256:malformada"):
            with self.subTest(value=value):
                repo = self.make_repo()
                _, _, request, _, _, _, store = approved_environment(repo)
                envelope = repo.get_object("approval_request", request["approval_id"])
                envelope["request"]["fingerprint"] = value
                repo.put_object("approval_request", request["approval_id"], envelope)
                self.assertEqual(
                    store.begin(mission_id=MISSION_ID, task_id=TASK_ID),
                    ("ERROR", None),
                )
                self.assertIsNone(repo.get_object(_CALL_KIND, _CALL_KEY))

    def test_absent_or_incoherent_authority_never_acquires(self):
        def mission_absent(repo, request):
            with repo.transaction():
                repo._conn.execute("DELETE FROM missions WHERE mission_id=?", (MISSION_ID,))

        def task_absent(repo, request):
            mission = repo.get_mission(MISSION_ID)
            mission["tasks"] = []
            self.assertTrue(repo.save_mission(mission)[0])

        def task_incoherent(repo, request):
            mission = repo.get_mission(MISSION_ID)
            mission["tasks"][0]["objective"] = "runtime incoherente"
            self.assertTrue(repo.save_mission(mission)[0])

        def approval_absent(repo, request):
            mission = repo.get_mission(MISSION_ID)
            mission["approval_id"] = "APP-AUSENTE"
            self.assertTrue(repo.save_mission(mission)[0])

        def approval_incoherent(repo, request):
            envelope = repo.get_object("approval_request", request["approval_id"])
            envelope["request"]["mission_id"] = "MSN-CRUZADA"
            repo.put_object("approval_request", request["approval_id"], envelope)

        def mission_not_executable(repo, request):
            mission = repo.get_mission(MISSION_ID)
            mission.update(status="CANCELADA", current_state="CANCELADA")
            self.assertTrue(repo.save_mission(mission)[0])

        scenarios = {
            "mission_absent": mission_absent,
            "task_absent": task_absent,
            "task_incoherent": task_incoherent,
            "approval_absent": approval_absent,
            "approval_incoherent": approval_incoherent,
            "mission_not_executable": mission_not_executable,
        }
        for name, mutate in scenarios.items():
            with self.subTest(name=name):
                repo = self.make_repo()
                _, _, request, _, _, _, store = approved_environment(repo)
                mutate(repo, request)
                self.assertEqual(
                    store.begin(mission_id=MISSION_ID, task_id=TASK_ID),
                    ("ERROR", None),
                )
                self.assertIsNone(repo.get_object(_CALL_KIND, _CALL_KEY))

    def test_invalid_identity_and_repository_are_rejected(self):
        self.assertEqual(
            self.store.begin(mission_id="", task_id=TASK_ID), ("ERROR", None)
        )
        self.assertEqual(
            self.store.begin(mission_id=MISSION_ID, task_id=" "), ("ERROR", None)
        )
        with self.assertRaises(ValueError):
            RepositoryDurableCallStore(
                None, authorized_content_fingerprint=self.request["fingerprint"]
            )


class TestPlanValidityAndGateway(StoreTestCase):
    def test_different_approved_plan_blocks_old_and_new_instances(self):
        repo = self.make_repo()
        runtime, context, request, _, _, _, _ = approved_environment(repo)
        provider = ControlledRealProvider(
            [agent_gateway.ModelCallResponse(_OK_RESPONSE_JSON, 10, 20)]
        )
        old_gateway, _ = self.make_gateway(repo, provider, request)
        first = self.call(old_gateway, request["approval_id"])
        self.assertTrue(first[0], first[2])
        original_record = repo.get_object(_CALL_KIND, _CALL_KEY)
        original_budget = repo.budget_snapshot()

        new_request = approve_changed_plan(repo, runtime, context)
        old_result = self.call(old_gateway, new_request["approval_id"])
        new_provider = ControlledRealProvider([])
        new_gateway, _ = self.make_gateway(repo, new_provider, new_request)
        new_result = self.call(new_gateway, new_request["approval_id"])

        self.assertFalse(old_result[0])
        self.assertFalse(new_result[0])
        self.assertEqual(old_result[2]["error_code"], "SYSTEM_ERROR")
        self.assertEqual(new_result[2]["error_code"], "SYSTEM_ERROR")
        self.assertEqual(provider.call_count, 1)
        self.assertEqual(new_provider.call_count, 0)
        self.assertEqual(repo.budget_snapshot(), original_budget)
        self.assertEqual(repo.get_object(_CALL_KIND, _CALL_KEY), original_record)

    def test_change_or_cancel_during_provider_call_blocks_completion(self):
        for action in ("change_plan", "cancel"):
            with self.subTest(action=action):
                repo = self.make_repo()
                runtime, context, request, _, _, _, _ = approved_environment(repo)
                provider = BlockingRealProvider(
                    agent_gateway.ModelCallResponse(_OK_RESPONSE_JSON, 10, 20)
                )
                gateway, _ = self.make_gateway(repo, provider, request)
                result = []
                worker = threading.Thread(
                    target=lambda: result.append(
                        self.call(gateway, request["approval_id"])
                    )
                )
                worker.start()
                self.assertTrue(provider.entered.wait(5))
                acquired = repo.get_object(_CALL_KIND, _CALL_KEY)
                try:
                    if action == "change_plan":
                        approve_changed_plan(repo, runtime, context, action)
                    else:
                        ok, _, error = runtime.control_local_mission(
                            MISSION_ID, "cancel", context, "cancelacion controlada"
                        )
                        self.assertTrue(ok, error)
                finally:
                    provider.release.set()
                    worker.join(5)

                self.assertFalse(worker.is_alive())
                self.assertEqual(len(result), 1)
                self.assertFalse(result[0][0])
                self.assertEqual(result[0][2]["error_code"], "SYSTEM_ERROR")
                self.assertEqual(provider.call_count, 1)
                self.assertEqual(repo.budget_snapshot()["requests"], 1)
                calls = repo._conn.execute(
                    "SELECT payload FROM durable_objects WHERE kind='call'"
                ).fetchall()
                self.assertEqual(len(calls), 1)
                self.assertEqual(repo.get_object(_CALL_KIND, _CALL_KEY), acquired)

    def test_same_plan_recovery_has_no_second_call_or_reservation(self):
        repo = self.make_repo()
        _, _, request, _, _, _, _ = approved_environment(repo)
        provider = ControlledRealProvider(
            [agent_gateway.ModelCallResponse(_OK_RESPONSE_JSON, 10, 20)]
        )
        gateway, _ = self.make_gateway(repo, provider, request)

        first = self.call(gateway, request["approval_id"])
        snapshot = repo.budget_snapshot()
        second = self.call(gateway, request["approval_id"])

        self.assertTrue(first[0], first[2])
        self.assertEqual(second, first)
        self.assertEqual(provider.call_count, 1)
        self.assertEqual(repo.budget_snapshot(), snapshot)

    def test_uncertain_state_is_never_retried_automatically(self):
        repo = self.make_repo()
        _, _, request, _, _, _, _ = approved_environment(repo)
        provider = ControlledRealProvider([RuntimeError("resultado incierto")])
        gateway, _ = self.make_gateway(repo, provider, request)

        first = self.call(gateway, request["approval_id"])
        snapshot = repo.budget_snapshot()
        record = repo.get_object(_CALL_KIND, _CALL_KEY)
        second = self.call(gateway, request["approval_id"])

        self.assertFalse(first[0])
        self.assertFalse(second[0])
        self.assertEqual(first[2]["error_code"], "SYSTEM_ERROR")
        self.assertEqual(second[2]["error_code"], "SYSTEM_ERROR")
        self.assertEqual(provider.call_count, 1)
        self.assertEqual(repo.budget_snapshot(), snapshot)
        self.assertEqual(repo.get_object(_CALL_KIND, _CALL_KEY), record)
        self.assertEqual(record["state"], "IN_PROGRESS")

    def test_gateway_rejection_before_provider_adds_no_call_or_reservation(self):
        repo = self.make_repo()
        _, _, request, _, _, _, _ = approved_environment(repo)
        provider = ControlledRealProvider([])
        gateway, store = self.make_gateway(repo, provider, request)
        initial_snapshot = repo.budget_snapshot()

        missing_approval = self.call(gateway, "APP-AUSENTE")

        self.assertFalse(missing_approval[0])
        self.assertEqual(missing_approval[2]["error_code"], "PERMISSION_DENIED")
        self.assertEqual(provider.call_count, 0)
        self.assertEqual(repo.budget_snapshot(), initial_snapshot)
        self.assertIsNone(repo.get_object(_CALL_KIND, _CALL_KEY))

        self.assertEqual(store.begin(mission_id=MISSION_ID, task_id=TASK_ID)[0], "NEW")
        snapshot = repo.budget_snapshot()

        result = self.call(gateway, request["approval_id"])

        self.assertFalse(result[0])
        self.assertEqual(provider.call_count, 0)
        self.assertEqual(repo.budget_snapshot(), snapshot)


class TestSQLiteDurabilityAndConcurrency(StoreTestCase):
    def test_reopen_preserves_result_and_consumption(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "gateway-replay.db")
            repo1 = LocalRepository(path)
            _, _, request, _, _, _, _ = approved_environment(repo1)
            provider1 = ControlledRealProvider(
                [agent_gateway.ModelCallResponse(_OK_RESPONSE_JSON, 5, 10)]
            )
            gateway1, _ = self.make_gateway(repo1, provider1, request)
            first = self.call(gateway1, request["approval_id"])
            snapshot = repo1.budget_snapshot()
            repo1.close()

            repo2 = LocalRepository(path)
            try:
                stored_request = repo2.get_object(
                    "approval_request", request["approval_id"]
                )["request"]
                provider2 = ControlledRealProvider([])
                gateway2, _ = self.make_gateway(repo2, provider2, stored_request)
                second = self.call(gateway2, stored_request["approval_id"])

                self.assertTrue(first[0], first[2])
                self.assertEqual(second, first)
                self.assertEqual(provider2.call_count, 0)
                self.assertEqual(repo2.budget_snapshot(), snapshot)
            finally:
                repo2.close()

    def test_two_connections_to_same_file_only_acquire_once(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "concurrent.db")
            repo1 = LocalRepository(path)
            _, _, request, _, _, _, _ = approved_environment(repo1)
            repo2 = LocalRepository(path)
            try:
                store1 = RepositoryDurableCallStore(
                    repo1,
                    authorized_content_fingerprint=request["fingerprint"],
                    authorization_validator=LocalApprovalRecordValidator(repo1),
                )
                store2 = RepositoryDurableCallStore(
                    repo2,
                    authorized_content_fingerprint=request["fingerprint"],
                    authorization_validator=LocalApprovalRecordValidator(repo2),
                )
                barrier = threading.Barrier(2)
                results = []
                result_lock = threading.Lock()

                def acquire(store):
                    barrier.wait()
                    value = store.begin(mission_id=MISSION_ID, task_id=TASK_ID)
                    with result_lock:
                        results.append(value[0])

                threads = [
                    threading.Thread(target=acquire, args=(store1,)),
                    threading.Thread(target=acquire, args=(store2,)),
                ]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join(5)

                self.assertTrue(all(not thread.is_alive() for thread in threads))
                self.assertCountEqual(results, ["NEW", "IN_PROGRESS"])
            finally:
                repo1.close()
                repo2.close()


if __name__ == "__main__":
    unittest.main()
