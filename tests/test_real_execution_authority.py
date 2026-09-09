"""REAL-01: autorizacion persistida para llamadas de especialistas.

Las decisiones de prueba se generan con HumanApprovalEngine. No se fabrican
approval_record ni approval_request manualmente y no se realizan llamadas
externas.
"""

import copy
import unittest

from app.hq_runtime import HQRuntime
from app.local_repository import LocalRepository
from app.real_execution_authority import LocalApprovalRecordValidator


PROFILE = {
    "user_id": "USR-NIKO-REAL01",
    "display_name": "Niko REAL-01",
    "actor_role": "usuario_humano",
}
MISSION_ID = "MSN-REAL-01"
TASK_ID = "TSK-001-RESEARCH"


def create_plan_request(repo):
    runtime = HQRuntime(repository=repo)
    context = runtime.approvals.bind_local_profile(PROFILE)
    ok, mission, error = runtime.create_local_mission(
        {
            "mission_id": MISSION_ID,
            "title": "REAL-01 controlada",
            "objective": "Validar autoridad persistida",
            "context": "Prueba local sin llamadas externas",
            "expected_result": "Mandato verificable",
        },
        context,
    )
    if not ok:
        raise AssertionError(error)
    envelope = repo.get_object("approval_request", mission["approval_id"])
    return runtime, context, envelope["request"]


def create_approved_plan(repo):
    runtime, context, request = create_plan_request(repo)
    ok, response, error = runtime.approvals.submit_human_decision(
        request, "APROBAR", context=context
    )
    if not ok:
        raise AssertionError(error)
    mission = repo.get_mission(MISSION_ID)
    return runtime, context, request, response, mission


class TestLocalApprovalRecordValidator(unittest.TestCase):
    def setUp(self):
        self.repo = LocalRepository(":memory:")
        self.addCleanup(self.repo.close)
        (
            self.runtime,
            self.context,
            self.request,
            self.response,
            self.mission,
        ) = create_approved_plan(self.repo)
        self.validator = LocalApprovalRecordValidator(self.repo)

    def validate(self, **overrides):
        values = {
            "mission_id": MISSION_ID,
            "task_id": TASK_ID,
            "owner_id": PROFILE["user_id"],
            "approval_id": self.request["approval_id"],
        }
        values.update(overrides)
        return self.validator.validate(**values)

    def test_valid_engine_approval_returns_current_mandate(self):
        record = self.repo.get_object("approval_record", self.request["approval_id"])
        self.assertNotIn("mission_id", record)
        self.assertNotIn("gate_type", record)

        mandate = self.validate()

        self.assertIsNotNone(mandate)
        self.assertEqual(mandate.mission_id, MISSION_ID)
        self.assertEqual(mandate.task_id, TASK_ID)
        self.assertEqual(mandate.owner_id, PROFILE["user_id"])
        self.assertEqual(mandate.approval_id, self.request["approval_id"])
        self.assertEqual(mandate.decision, "APROBAR")
        self.assertTrue(mandate.persisted)
        self.assertTrue(mandate.is_current)

    def test_wrong_owner_mission_or_approval_is_rejected(self):
        self.assertIsNone(self.validate(owner_id="USR-OTRO"))
        self.assertIsNone(self.validate(mission_id="MSN-OTRA"))
        self.assertIsNone(self.validate(approval_id="APP-INEXISTENTE"))

    def test_task_membership_is_mandatory(self):
        self.assertIsNone(self.validate(task_id="TSK-FUERA-DEL-PLAN"))

        mission = self.repo.get_mission(MISSION_ID)
        mission["tasks"] = [
            task for task in mission["tasks"] if task["task_id"] != TASK_ID
        ]
        self.assertTrue(self.repo.save_mission(mission)[0])
        self.assertIsNone(self.validate())

    def test_changed_current_plan_is_rejected_without_validation_writes(self):
        mission = self.repo.get_mission(MISSION_ID)
        mission["plan"]["tasks"][0]["objective"] = "Contenido cambiado despues de aprobar"
        self.assertTrue(self.repo.save_mission(mission)[0])
        before = list(self.repo._conn.iterdump())

        self.assertIsNone(self.validate())

        self.assertEqual(list(self.repo._conn.iterdump()), before)

    def test_changed_runtime_task_is_rejected(self):
        mission = self.repo.get_mission(MISSION_ID)
        runtime_task = next(
            task for task in mission["tasks"] if task["task_id"] == TASK_ID
        )
        runtime_task["objective"] = "Objetivo no aprobado"
        self.assertTrue(self.repo.save_mission(mission)[0])
        self.assertIsNone(self.validate())

    def test_inconsistent_request_and_record_are_rejected(self):
        approval_id = self.request["approval_id"]
        envelope = self.repo.get_object("approval_request", approval_id)
        envelope["request"]["mission_id"] = "MSN-CRUZADA"
        self.repo.put_object("approval_request", approval_id, envelope)
        self.assertIsNone(self.validate())

        envelope = copy.deepcopy(envelope)
        envelope["request"]["mission_id"] = MISSION_ID
        envelope["record"]["decision"] = "RECHAZAR"
        self.repo.put_object("approval_request", approval_id, envelope)
        self.assertIsNone(self.validate())

    def test_obsolete_plan_approval_is_rejected(self):
        old_approval_id = self.request["approval_id"]
        mission = self.repo.get_mission(MISSION_ID)
        mission.update(status="PLAN_EN_REVISION", current_state="PLAN_EN_REVISION")
        self.assertTrue(self.repo.save_mission(mission)[0])
        current = self.repo.get_mission(MISSION_ID)
        ok, new_request, error = self.runtime.approvals.create_approval_request(
            MISSION_ID,
            "GATE_1_PLAN",
            {"brief": current["brief"], "plan": current["plan"]},
        )
        self.assertTrue(ok, error)
        self.assertNotEqual(new_request["approval_id"], old_approval_id)
        self.assertIsNone(self.validate(approval_id=old_approval_id))

    def test_rejections_cause_zero_writes(self):
        before = list(self.repo._conn.iterdump())

        self.assertIsNone(self.validate(owner_id="USR-OTRO"))
        self.assertIsNone(self.validate(task_id="TSK-FUERA"))
        self.assertIsNone(self.validate(approval_id="APP-AUSENTE"))

        self.assertEqual(list(self.repo._conn.iterdump()), before)

    def test_invalid_input_is_rejected(self):
        for field in ("mission_id", "task_id", "owner_id", "approval_id"):
            with self.subTest(field=field):
                self.assertIsNone(self.validate(**{field: ""}))
                self.assertIsNone(self.validate(**{field: " con-espacios "}))

    def test_none_repository_is_rejected(self):
        with self.assertRaises(ValueError):
            LocalApprovalRecordValidator(None)


class TestNonAuthorizingApprovalStates(unittest.TestCase):
    def test_pending_plan_request_does_not_authorize(self):
        repo = LocalRepository(":memory:")
        self.addCleanup(repo.close)
        _, _, request = create_plan_request(repo)
        validator = LocalApprovalRecordValidator(repo)

        self.assertIsNone(
            validator.validate(
                mission_id=MISSION_ID,
                task_id=TASK_ID,
                owner_id=PROFILE["user_id"],
                approval_id=request["approval_id"],
            )
        )

    def test_rejected_plan_does_not_authorize(self):
        repo = LocalRepository(":memory:")
        self.addCleanup(repo.close)
        runtime, context, request = create_plan_request(repo)
        ok, _, error = runtime.approvals.submit_human_decision(
            request,
            "RECHAZAR",
            comment="No autorizado",
            context=context,
        )
        self.assertTrue(ok, error)
        validator = LocalApprovalRecordValidator(repo)

        self.assertIsNone(
            validator.validate(
                mission_id=MISSION_ID,
                task_id=TASK_ID,
                owner_id=PROFILE["user_id"],
                approval_id=request["approval_id"],
            )
        )

    def _assert_vbp_decision_does_not_authorize(self, decision, **decision_kwargs):
        repo = LocalRepository(":memory:")
        self.addCleanup(repo.close)
        runtime, context, _, _, _ = create_approved_plan(repo)
        ok, mission, error = runtime.execute_local_simulation(MISSION_ID, context)
        self.assertTrue(ok, error)
        vbp_request = mission["approval_request"]
        ok, _, error = runtime.approvals.submit_human_decision(
            vbp_request,
            decision,
            context=context,
            **decision_kwargs,
        )
        self.assertTrue(ok, error)
        validator = LocalApprovalRecordValidator(repo)

        self.assertIsNone(
            validator.validate(
                mission_id=MISSION_ID,
                task_id=TASK_ID,
                owner_id=PROFILE["user_id"],
                approval_id=vbp_request["approval_id"],
            )
        )

    def test_vbp_approval_does_not_authorize_specialists(self):
        self._assert_vbp_decision_does_not_authorize("APROBAR")

    def test_vbp_exception_does_not_authorize_specialists(self):
        self._assert_vbp_decision_does_not_authorize(
            "APROBAR_CON_EXCEPCION",
            comment="Excepcion controlada de prueba",
            conditions=["Solo prueba local"],
            risks=["No es ejecucion real verificada"],
        )


if __name__ == "__main__":
    unittest.main()
