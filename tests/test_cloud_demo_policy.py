"""Pruebas exhaustivas para la Politica de Demo Publica Cloud (PZ-014A).

Valida cuota diaria de 5 ejecuciones (quinta admitida, sexta rechazada),
preservacion del contador tras reinicio, exclusion de archivos privados en .dockerignore
y configuracion minScale 0 / maxScale 1 para Cloud Run.
"""

import tempfile
import unittest
from pathlib import Path

import app.cloud_demo_repository as cloud_demo_repository
import app.local_repository as local_repository


class TestCloudDemoPolicy(unittest.TestCase):
    """Suite de pruebas para PZ-014A (Cloud Demo Policy)."""

    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.db_path = str(Path(self.tmp_dir.name) / "test_demo.db")
        self.repo = local_repository.LocalRepository(db_path=self.db_path)
        self.policy = cloud_demo_repository.CloudDemoPolicyManager(repository=self.repo, daily_limit=5)

    def tearDown(self) -> None:
        try:
            self.repo.close()
        except Exception:
            pass
        try:
            self.tmp_dir.cleanup()
        except Exception:
            pass

    def test_ac01_dockerignore_excludes_private_and_sensitive_data(self) -> None:
        """AC-01: El archivo .dockerignore excluye explicitamente bases de datos, .env*, .pyc y carpetas privadas."""
        dockerignore_path = Path(".dockerignore")
        self.assertTrue(dockerignore_path.exists(), ".dockerignore debe existir.")
        content = dockerignore_path.read_text(encoding="utf-8")

        required_patterns = [".env*", "*.db", "*.pyc", "__pycache__/", "tests/"]
        for pat in required_patterns:
            self.assertIn(pat, content, f"Patron de exclusion ausente: {pat}")

    def test_ac02_and_ac03_daily_limit_quota_and_persistence_across_restarts(self) -> None:
        """AC-02 & AC-03: Admite exactamente 5 ejecuciones por dia; la 6ta es rechazada. Reinicio preserva contador."""
        today = "2026-08-30"

        # Ejecutar 4 veces -> todas exitosas
        for i in range(1, 5):
            ok, count, _ = self.policy.try_acquire_demo_execution(today_str=today)
            self.assertTrue(ok)
            self.assertEqual(count, i)

        # 5ta ejecucion -> permitida (limite maximo)
        ok_5, count_5, err_5 = self.policy.try_acquire_demo_execution(today_str=today)
        self.assertTrue(ok_5)
        self.assertEqual(count_5, 5)
        self.assertIsNone(err_5)

        # 6ta ejecucion -> rechazada por cuota agotada
        ok_6, count_6, err_6 = self.policy.try_acquire_demo_execution(today_str=today)
        self.assertFalse(ok_6)
        self.assertEqual(count_6, 5)
        self.assertIn("CUOTA_DEMO_DIARIA_AGOTADA", err_6)

        # Simular reinicio creando nueva instancia sobre la misma DB
        restarted_policy = cloud_demo_repository.CloudDemoPolicyManager(repository=self.repo, daily_limit=5)
        restarted_count = restarted_policy.get_today_executions_count(today_str=today)
        self.assertEqual(restarted_count, 5)

        # Reintento tras reinicio sigue bloqueado
        ok_after_restart, _, _ = restarted_policy.try_acquire_demo_execution(today_str=today)
        self.assertFalse(ok_after_restart)

    def test_ac04_cloudrun_config_has_min_scale_0_and_max_scale_1(self) -> None:
        """AC-04: El manifiesto de Cloud Run declara minScale: 0, maxScale: 1 y limite de memoria 512Mi."""
        cloudrun_path = Path("deploy/cloudrun.example.yaml")
        self.assertTrue(cloudrun_path.exists(), "deploy/cloudrun.example.yaml debe existir.")
        content = cloudrun_path.read_text(encoding="utf-8")

        self.assertIn('minScale: "0"', content)
        self.assertIn('maxScale: "1"', content)
        self.assertIn('memory: "512Mi"', content)

    def test_ac05_dockerfile_uses_non_root_user_and_exposes_8080(self) -> None:
        """AC-05: El Dockerfile ejecuta con usuario no-root (appuser) y expone el puerto 8080."""
        dockerfile_path = Path("Dockerfile")
        self.assertTrue(dockerfile_path.exists(), "Dockerfile debe existir.")
        content = dockerfile_path.read_text(encoding="utf-8")

        self.assertIn("USER appuser", content)
        self.assertIn("EXPOSE 8080", content)

class TestCloudDemoResources(unittest.TestCase):
    """Verificaciones aisladas de recursos requeridos por la demo Cloud."""

    def test_ac06_dockerfile_copies_required_demo_fixture(self) -> None:
        """AC-06: Docker incluye exactamente el fixture local requerido por la demo."""
        fixture_path = Path("examples/demo_mission.json")
        self.assertTrue(fixture_path.is_file(), "examples/demo_mission.json debe existir como archivo.")

        dockerfile_path = Path("Dockerfile")
        content = dockerfile_path.read_text(encoding="utf-8")
        expected_copy = "COPY examples/demo_mission.json examples/demo_mission.json"
        matching_lines = [line for line in content.splitlines() if line == expected_copy]
        self.assertEqual(matching_lines, [expected_copy])


if __name__ == "__main__":
    unittest.main()
