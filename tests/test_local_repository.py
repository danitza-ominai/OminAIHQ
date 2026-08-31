"""Pruebas exhaustivas para el Repositorio Transaccional SQLite (PZ-010A).

Valida persistencia duradera, recuperacion tras cierre de conexion, rollback atomico,
idempotencia durable, bloqueo de misiones activas concurrentes y pruebas en DB temporal aislada.
"""

import os
import json
import tempfile
import unittest
from pathlib import Path

import app.hq_runtime as hq_runtime
import app.local_repository as local_repository


class TestLocalRepository(unittest.TestCase):
    """Suite de pruebas para PZ-010A (Local Repository)."""

    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmp_dir.name) / "test_ominai.db")
        self.repo = local_repository.LocalRepository(db_path=self.db_path)
        self.runtime = hq_runtime.HQRuntime(repository=self.repo)

    def tearDown(self) -> None:
        self.repo.close()
        self.tmp_dir.cleanup()

    def test_ac01_persistence_and_reopen_preserves_all_data(self) -> None:
        """AC-01: Cerrar y reabrir conexion SQLite conserva perfil, mision, checkpoints y aprobaciones."""
        # 1. Guardar perfil
        self.repo.save_profile({
            "user_id": "usr_local_admin",
            "display_name": "Niko (A0)",
            "email": "niko@ominai.dev",
        })

        # 2. Guardar mision nuclear valida; el fixture anterior omitia el contrato.
        import json
        nuclear = json.loads((Path(__file__).resolve().parent.parent / 'contracts/core/examples/mission.valid.json').read_text())['test_data']
        nuclear.update(mission_id='MSN-SQL-001', current_state='BORRADOR')
        ok, error = self.repo.save_mission({
            "mission_id": "MSN-SQL-001",
            "title": "Mision SQLite",
            "status": "BORRADOR",
            "version": nuclear['record_version'],
            "nuclear": nuclear,
            "user_id": nuclear['user_id'],
        })
        self.assertTrue(ok, error)

        # 3. Guardar checkpoint
        mission = self.repo.get_mission('MSN-SQL-001')
        self.repo.save_runtime_checkpoint(mission, 'CHK-001', '2026-08-31T15:00:00Z')
        checkpoints_before = self.repo.list_checkpoints('MSN-SQL-001')
        self.assertEqual(len(checkpoints_before), 1)

        # 4. Guardar aprobacion
        self.repo.save_approval_atomic({
            "approval_id": "APP-001",
            "mission_id": "MSN-SQL-001",
            "approval_type": "PLAN_REVIEW",
            "status": "CONSUMIDA",
            "decision": "APROBAR",
            "idempotency_key": "IDEMP-001",
            "fingerprint": "sha256:1111111111111111111111111111111111111111111111111111111111111111",
        })

        # Cerrar conexion
        self.repo.close()

        # Reabrir nueva instancia sobre el mismo archivo DB
        reopened_repo = local_repository.LocalRepository(db_path=self.db_path)
        try:
            prof = reopened_repo.get_profile("usr_local_admin")
            self.assertIsNotNone(prof)
            self.assertEqual(prof["display_name"], "Niko (A0)")

            mis = reopened_repo.get_mission("MSN-SQL-001")
            self.assertIsNotNone(mis)
            self.assertEqual(mis["title"], "Mision SQLite")

            chks = reopened_repo.list_checkpoints("MSN-SQL-001")
            self.assertEqual(len(chks), 1)
            self.assertEqual(chks, checkpoints_before)

            apps = reopened_repo.list_approvals("MSN-SQL-001")
            self.assertEqual(len(apps), 1)
            self.assertEqual(apps[0]["decision"], "APROBAR")
        finally:
            reopened_repo.close()

    def test_ac02_atomic_rollback_on_fault(self) -> None:
        """AC-02: Si ocurre un fallo en la transaccion, se revierte todo (rollback) sin estados parciales."""
        self.repo.save_mission({
            "mission_id": "MSN-ATOMIC-001",
            "title": "Mision Atomica",
            "status": "PLAN_EN_REVISION",
            "version": 1,
        })

        # Intentar aprobacion con fallo simulado
        ok, err = self.repo.save_approval_atomic(
            approval_data={
                "approval_id": "APP-FAIL-001",
                "mission_id": "MSN-ATOMIC-001",
                "decision": "APROBAR",
                "idempotency_key": "IDEMP-FAIL-001",
                "fingerprint": "sha256:2222222222222222222222222222222222222222222222222222222222222222",
            },
            mission_update={
                "mission_id": "MSN-ATOMIC-001",
                "status": "AUTORIZADA_PARA_EJECUTAR",
            },
            simulated_fault=True,
        )

        self.assertFalse(ok)
        self.assertIn("Fallo transaccional", err)

        # Verificar que la aprobacion no existe y la mision no cambio de estado
        apps = self.repo.list_approvals("MSN-ATOMIC-001")
        self.assertEqual(len(apps), 0)

        mis = self.repo.get_mission("MSN-ATOMIC-001")
        self.assertEqual(mis["status"], "PLAN_EN_REVISION")
        self.assertEqual(mis["version"], 1)

    def test_ac02b_transition_version_and_rollback_include_nuclear_references(self) -> None:
        from test_human_approvals import fixture
        runtime, repo, context, request = fixture()
        try:
            before = repo.get_mission("MSN-SIM")
            ok, _, error = runtime.approvals.submit_human_decision(request, "APROBAR", context=context)
            self.assertTrue(ok, error)
            after = repo.get_mission("MSN-SIM")
            self.assertEqual(after["version"], before["version"] + 1)
            self.assertEqual(after["nuclear"]["record_version"], after["version"])
            self.assertTrue(all(t["mission_version"] == after["version"] for t in after["tasks"]))
            self.assertEqual(repo.list_events("MSN-SIM")[-1]["version"], after["version"])
            checkpoint = json.loads(repo.list_checkpoints("MSN-SIM")[-1]["state_snapshot_json"])
            self.assertEqual(checkpoint["mission_version"], after["version"])
        finally:
            repo.close()

    def test_ac03_idempotent_replay_does_not_duplicate(self) -> None:
        """AC-03: Reenviar aprobacion con misma clave de idempotencia no duplica registros."""
        app_data = {
            "approval_id": "APP-IDEMP-001",
            "mission_id": "MSN-IDEMP-001",
            "decision": "APROBAR",
            "idempotency_key": "IDEMP-SAME-KEY-001",
            "fingerprint": "sha256:3333333333333333333333333333333333333333333333333333333333333333",
        }
        ok1, _ = self.repo.save_approval_atomic(app_data)
        self.assertTrue(ok1)

        # Segunda llamada con misma idempotency_key
        ok2, _ = self.repo.save_approval_atomic(app_data)
        self.assertTrue(ok2)

        apps = self.repo.list_approvals("MSN-IDEMP-001")
        self.assertEqual(len(apps), 1)

    def test_ac04_second_concurrent_active_mission_is_blocked(self) -> None:
        """AC-04: Intentar crear una segunda mision activa simultanea es bloqueado (MAX_CONCURRENT_MISSIONS_EXCEEDED)."""
        # 1. Crear primera mision activa en BORRADOR
        ok1, err1 = self.repo.save_mission({
            "mission_id": "MSN-ACTIVA-001",
            "title": "Primera Mision",
            "status": "BORRADOR",
        })
        self.assertTrue(ok1)

        # 2. Intentar crear segunda mision activa
        ok2, err2 = self.repo.save_mission({
            "mission_id": "MSN-ACTIVA-002",
            "title": "Segunda Mision Concurrente",
            "status": "BORRADOR",
        })
        self.assertFalse(ok2)
        self.assertIn("MAX_CONCURRENT_MISSIONS_EXCEEDED", err2)

        # 3. Finalizar primera mision -> permite crear nueva mision
        self.repo.save_mission({
            "mission_id": "MSN-ACTIVA-001",
            "title": "Primera Mision",
            "status": "FINALIZADA",
        })

        ok3, err3 = self.repo.save_mission({
            "mission_id": "MSN-ACTIVA-002",
            "title": "Segunda Mision Concurrente",
            "status": "BORRADOR",
        })
        self.assertTrue(ok3)

    def test_ac05_runtime_integration(self) -> None:
        """AC-05: El LocalRepository se encuentra accesible en HQRuntime."""
        self.assertIsNotNone(self.runtime.repository)
        self.assertIsInstance(self.runtime.repository, local_repository.LocalRepository)

    def test_nuclear_revision_advances_on_persisted_state_change(self) -> None:
        """Regresion abierta: mission.record_version incrementa cada modificacion.

        No usar expectedFailure: la suite debe seguir roja mientras este requisito
        contractual no se cumpla, aunque el recorrido y los schemas sean validos.
        """
        from test_human_approvals import fixture
        runtime, repo, context, request = fixture()
        try:
            before = repo.get_mission('MSN-SIM')
            ok, _, error = runtime.approvals.submit_human_decision(
                request, 'APROBAR', context=context)
            self.assertTrue(ok, error)
            after = repo.get_mission('MSN-SIM')
            self.assertNotEqual(before['status'], after['status'])
            self.assertEqual(after['nuclear']['current_state'], after['status'])
            self.assertGreater(after['nuclear']['record_version'],
                               before['nuclear']['record_version'])
        finally:
            repo.close()


if __name__ == "__main__":
    unittest.main()
