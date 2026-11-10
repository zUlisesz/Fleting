"""Pruebas del aislamiento de movimientos entre perfiles locales."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from finanzas.modelo import Repositorio


class ProfileRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.repo = Repositorio(Path(self.temporary_directory.name) / "finanzas.sqlite3")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_profiles_only_list_their_own_movements(self) -> None:
        ana_id = self.repo.crear_perfil("Ana")
        self.repo.agregar("2026-11-10", "Despensa", "Comida", "Gasto", "150")

        self.repo.seleccionar_perfil(ana_id)

        self.assertEqual(self.repo.listar(), [])
        self.repo.agregar("2026-11-10", "Honorarios", "Trabajo", "Ingreso", "900")
        self.assertEqual([item.concepto for item in self.repo.listar()], ["Honorarios"])

        self.repo.seleccionar_perfil(1)
        self.assertEqual([item.concepto for item in self.repo.listar()], ["Despensa"])

    def test_rejects_invalid_profile_values(self) -> None:
        for name in (None, 12, True):
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    self.repo.crear_perfil(name)

        for profile_id in (True, "1", None):
            with self.subTest(profile_id=profile_id):
                with self.assertRaises(ValueError):
                    self.repo.seleccionar_perfil(profile_id)


if __name__ == "__main__":
    unittest.main()
