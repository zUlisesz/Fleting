import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from finanzas.dominio import Filtros
from finanzas.repositorio import Repositorio, ruta_por_defecto


class RepositorioTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.ruta = Path(self._tmp.name) / "finanzas.sqlite3"
        self.repo = Repositorio(self.ruta)


class PerfilesTests(RepositorioTestCase):
    def test_profiles_only_list_their_own_movements(self) -> None:
        ana = self.repo.crear_perfil("Ana")
        self.repo.agregar(1, "2026-11-10", "Despensa", "Comida", "Gasto", "150")

        self.assertEqual(self.repo.listar(ana), [])
        self.repo.agregar(ana, "2026-11-10", "Honorarios", "Trabajo", "Ingreso", "900")
        self.assertEqual([m.concepto for m in self.repo.listar(ana)], ["Honorarios"])
        self.assertEqual([m.concepto for m in self.repo.listar(1)], ["Despensa"])

    def test_rejects_invalid_profile_values(self) -> None:
        for nombre in (None, 12, True, "", "  "):
            with self.subTest(nombre=nombre):
                with self.assertRaises(ValueError):
                    self.repo.crear_perfil(nombre)
        for perfil_id in (True, "1", None):
            with self.subTest(perfil_id=perfil_id):
                with self.assertRaises(ValueError):
                    self.repo.existe_perfil(perfil_id)
                with self.assertRaises(ValueError):
                    self.repo.listar(perfil_id)

    def test_duplicate_profile_names_are_rejected_ignoring_case(self) -> None:
        self.repo.crear_perfil("Ana")

        with self.assertRaises(ValueError):
            self.repo.crear_perfil("ana")

    def test_unknown_profile_cannot_receive_movements(self) -> None:
        self.assertFalse(self.repo.existe_perfil(99))
        with self.assertRaises(ValueError):
            self.repo.agregar(99, "2026-11-10", "X", "Comida", "Gasto", "1")


class MovimientosTests(RepositorioTestCase):
    def test_rejects_invalid_movements(self) -> None:
        validos = ("2026-11-10", "Despensa", "Comida", "Gasto", "150")
        invalidos = (
            ("2026-13-01", "Despensa", "Comida", "Gasto", "150"),
            ("2026-11-10", None, "Comida", "Gasto", "150"),
            ("2026-11-10", "Despensa", "Nada", "Gasto", "150"),
            ("2026-11-10", "Despensa", "Comida", "Otro", "150"),
            ("2026-11-10", "Despensa", "Comida", "Gasto", "1.005"),
        )
        self.repo.agregar(1, *validos)
        for datos in invalidos:
            with self.subTest(datos=datos):
                with self.assertRaises(ValueError):
                    self.repo.agregar(1, *datos)
        self.assertEqual(len(self.repo.listar(1)), 1)

    def test_filters_by_category_month_and_type(self) -> None:
        self.repo.agregar(1, "2026-09-05", "Taxi", "Transporte", "Gasto", "80")
        self.repo.agregar(1, "2026-10-05", "Nómina", "Trabajo", "Ingreso", "1000")
        self.repo.agregar(1, "2026-10-06", "Cine", "Ocio", "Gasto", "120")

        def conceptos(**kw):
            return [m.concepto for m in self.repo.listar(1, Filtros(**kw))]

        self.assertEqual(conceptos(), ["Cine", "Nómina", "Taxi"])
        self.assertEqual(conceptos(tipo="Ingreso"), ["Nómina"])
        self.assertEqual(conceptos(mes="2026-10", tipo="Gasto"), ["Cine"])
        self.assertEqual(conceptos(categoria="Transporte"), ["Taxi"])
        with self.assertRaises(ValueError):
            conceptos(mes="2026-13")

    def test_delete_only_affects_the_owner_profile(self) -> None:
        ana = self.repo.crear_perfil("Ana")
        movimiento_id = self.repo.agregar(1, "2026-11-10", "Despensa", "Comida", "Gasto", "150")

        with self.assertRaises(ValueError):
            self.repo.eliminar(ana, movimiento_id)
        self.repo.eliminar(1, movimiento_id)
        self.assertEqual(self.repo.listar(1), [])
        with self.assertRaises(ValueError):
            self.repo.eliminar(1, movimiento_id)

    def test_data_persists_between_repositories(self) -> None:
        self.repo.agregar(1, "2026-11-10", "Despensa", "Comida", "Gasto", "150.25")

        otro = Repositorio(self.ruta)

        self.assertEqual(otro.listar(1)[0].centavos, 15025)


class MigracionTests(unittest.TestCase):
    def test_legacy_expenses_table_is_migrated_to_the_initial_profile(self) -> None:
        with TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "finanzas.sqlite3"
            con = sqlite3.connect(ruta)
            con.execute(
                "CREATE TABLE gastos (id INTEGER PRIMARY KEY, fecha TEXT, concepto TEXT, "
                "categoria TEXT, centavos INTEGER)"
            )
            con.execute("INSERT INTO gastos VALUES (1, '2026-01-02', 'Libro', 'Estudio', 5000)")
            con.commit()
            con.close()

            repo = Repositorio(ruta)

            [movimiento] = repo.listar(1)
            self.assertEqual((movimiento.concepto, movimiento.tipo, movimiento.centavos), ("Libro", "Gasto", 5000))


class RutaTests(unittest.TestCase):
    def test_data_dir_can_be_overridden_with_an_environment_variable(self) -> None:
        with patch.dict("os.environ", {"FLET_DATA_DIR": "/datos"}):
            self.assertEqual(ruta_por_defecto(), Path("/datos/finanzas.sqlite3"))

    def test_default_directory_is_fletBD_in_home(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(ruta_por_defecto(), Path.home() / ".fletBD" / "finanzas.sqlite3")


if __name__ == "__main__":
    unittest.main()
