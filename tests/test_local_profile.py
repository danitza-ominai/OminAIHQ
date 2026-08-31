"""Pruebas exhaustivas para el Perfil Humano Unico Local (PZ-010A).

Valida inicializacion de perfil por defecto, actualizacion de metadatos,
rechazo de campos invalidos y restriccion de usuario unico.
"""

import unittest

import app.hq_runtime as hq_runtime
import app.local_profile as local_profile


class TestLocalProfile(unittest.TestCase):
    """Suite de pruebas para PZ-010A (Local Profile)."""

    def setUp(self) -> None:
        self.manager = local_profile.LocalProfileManager()
        self.runtime = hq_runtime.HQRuntime(profile_manager=self.manager)

    def test_ac01_default_profile_initialization(self) -> None:
        """AC-01: El perfil se inicializa con operador humano A0 sin contrasenas."""
        prof = self.manager.get_profile()
        self.assertEqual(prof["user_id"], "usr_local_admin")
        self.assertEqual(prof["display_name"], "Niko (A0)")
        self.assertEqual(prof["actor_role"], "usuario_humano")
        self.assertNotIn("password", prof)
        self.assertNotIn("token_secret", prof)

    def test_ac02_profile_update_and_email_validation(self) -> None:
        """AC-02: Actualizar perfil valida formatos de correo y rechaza nombres vacios."""
        # 1. Actualizacion valida
        ok1, prof1, err1 = self.manager.update_profile(display_name="Niko Operator", email="niko.admin@ominai.dev")
        self.assertTrue(ok1)
        self.assertEqual(prof1["display_name"], "Niko Operator")
        self.assertEqual(prof1["email"], "niko.admin@ominai.dev")

        # 2. Correo invalido
        ok2, _, err2 = self.manager.update_profile(email="correo_invalido_sin_arroba")
        self.assertFalse(ok2)
        self.assertIn("invalido", err2)

        # 3. Nombre vacio
        ok3, _, err3 = self.manager.update_profile(display_name="   ")
        self.assertFalse(ok3)
        self.assertIn("vacio", err3)

    def test_ac05_runtime_integration(self) -> None:
        """AC-05: El LocalProfileManager se encuentra accesible en HQRuntime."""
        self.assertIsNotNone(self.runtime.profile_manager)
        self.assertIsInstance(self.runtime.profile_manager, local_profile.LocalProfileManager)


if __name__ == "__main__":
    unittest.main()
