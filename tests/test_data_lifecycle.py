"""Pruebas exhaustivas para el Ciclo de Vida de Datos, Archivo y Eliminacion (PZ-010D).

Valida archivo sin perdida de datos, eliminacion segura con confirmacion humana expresa,
prevencion de path traversal, efectos pre/post aprobacion en evidencias e integracion en HQRuntime.
"""

import tempfile
import unittest
from pathlib import Path

import app.approved_memory as approved_memory
import app.data_lifecycle as data_lifecycle
import app.evidence_registry as evidence_registry
import app.hq_runtime as hq_runtime
import app.local_repository as local_repository


class TestDataLifecycle(unittest.TestCase):
    """Suite de pruebas para PZ-010D (Data Lifecycle)."""

    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmp_dir.name) / "test_lifecycle.db")
        self.repo = local_repository.LocalRepository(db_path=self.db_path)
        self.memory = approved_memory.ApprovedMemoryManager()
        self.evidence_reg = evidence_registry.EvidenceRegistry()
        self.manager = data_lifecycle.DataLifecycleManager(
            repository=self.repo,
            memory_manager=self.memory,
            evidence_reg=self.evidence_reg,
        )
        self.runtime = hq_runtime.HQRuntime(
            repository=self.repo,
            memory_manager=self.memory,
            lifecycle_manager=self.manager,
        )

    def tearDown(self) -> None:
        self.repo.close()
        self.tmp_dir.cleanup()

    def test_ac01_archive_preserves_records_and_frees_active_slot(self) -> None:
        """AC-01: Archivar oculta la mision sin borrar y permite crear una nueva mision activa."""
        # 1. Crear mision activa
        self.repo.save_mission({
            "mission_id": "MSN-ARCHIVE-001",
            "title": "Mision a archivar",
            "status": "BORRADOR",
            "version": 1,
        })

        # 2. Archivar
        ok_arch, arch_rec, _ = self.manager.archive_mission("MSN-ARCHIVE-001")
        self.assertTrue(ok_arch)
        self.assertEqual(arch_rec["status"], "ARCHIVADA")

        # 3. Comprobar que los datos siguen en base de datos
        persisted = self.repo.get_mission("MSN-ARCHIVE-001")
        self.assertIsNotNone(persisted)
        self.assertEqual(persisted["status"], "ARCHIVADA")

        # 4. Ahora se puede crear otra mision activa porque el cupo fue liberado
        ok_new, err_new = self.repo.save_mission({
            "mission_id": "MSN-ACTIVE-002",
            "title": "Nueva Mision Activa",
            "status": "BORRADOR",
        })
        self.assertTrue(ok_new, f"No se pudo crear nueva mision: {err_new}")

    def test_ac02_delete_requires_human_confirmation_and_blocks_path_traversal(self) -> None:
        """AC-02: Eliminar sin confirmacion expresa o con intento de path traversal es bloqueado."""
        self.repo.save_mission({
            "mission_id": "MSN-DEL-001",
            "title": "Mision a eliminar",
            "status": "BORRADOR",
            "version": 1,
        })

        # 1. Intento sin confirmacion humana
        ok_no_conf, err_no_conf = self.manager.delete_mission("MSN-DEL-001", target_version=1, human_confirmed=False)
        self.assertFalse(ok_no_conf)
        self.assertIn("ELIMINACION_REQUIERE_CONFIRMACION_HUMANA", err_no_conf)

        # 2. Intento de path traversal
        ok_pt, err_pt = self.manager.delete_mission("../MSN-DEL-001", target_version=1, human_confirmed=True)
        self.assertFalse(ok_pt)
        self.assertIn("PATH_TRAVERSAL_DETECTADO", err_pt)

        # 3. Eliminacion autorizada con version correcta
        ok_del, _ = self.manager.delete_mission("MSN-DEL-001", target_version=1, human_confirmed=True)
        self.assertTrue(ok_del)

        # Comprobar que no existe en DB
        self.assertIsNone(self.repo.get_mission("MSN-DEL-001"))

    def test_ac03_evidence_deletion_pre_and_post_approval_effects(self) -> None:
        """AC-03: Original desaparecido antes de aprobacion bloquea puerta; post-aprobacion degrada verificabilidad."""
        # 1. Preaprobacion: Bloquea y genera EVIDENCIA_NO_DISPONIBLE
        ok_pre, rec_pre, err_pre = self.manager.handle_evidence_deletion_event("MSN-001", "EVI-PRE-001", is_post_approval=False)
        self.assertFalse(ok_pre)
        self.assertIn("EVIDENCIA_NO_DISPONIBLE", err_pre)
        self.assertTrue(rec_pre["gate_blocked"])

        # 2. Postaprobacion: Preserva VBP historico y marca VERIFICABILIDAD_INCOMPLETA
        ok_post, rec_post, _ = self.manager.handle_evidence_deletion_event("MSN-001", "EVI-POST-001", is_post_approval=True)
        self.assertTrue(ok_post)
        self.assertEqual(rec_post["verifiability"], "VERIFICABILIDAD_INCOMPLETA")
        self.assertTrue(rec_post["historical_vbp_preserved"])

    def test_ac05_runtime_integration(self) -> None:
        """AC-05: El DataLifecycleManager se encuentra accesible en HQRuntime."""
        self.assertIsNotNone(self.runtime.lifecycle)
        self.assertIsInstance(self.runtime.lifecycle, data_lifecycle.DataLifecycleManager)


if __name__ == "__main__":
    unittest.main()
