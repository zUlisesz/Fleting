import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from organizador.modelo import PRIORIDADES, Repositorio, Tarea, validar


class ValidarTests(unittest.TestCase):
    def test_trims_the_title(self):
        self.assertEqual(validar("  Estudiar  ", "Alta"), "Estudiar")

    def test_accepts_the_length_limits(self):
        self.assertEqual(validar("a", "Baja"), "a")
        self.assertEqual(validar("a" * 80, "Baja"), "a" * 80)

    def test_rejects_empty_blank_and_too_long_titles(self):
        for titulo in ("", "   ", "a" * 81):
            with self.subTest(titulo=len(titulo)):
                with self.assertRaisesRegex(ValueError, "entre 1 y 80"):
                    validar(titulo, "Media")

    def test_rejects_unknown_priorities(self):
        for prioridad in ("", "alta", "Urgente", None):
            with self.subTest(prioridad=prioridad):
                with self.assertRaisesRegex(ValueError, "prioridad"):
                    validar("Tarea", prioridad)

    def test_priorities_are_ordered_from_low_to_high(self):
        self.assertEqual(PRIORIDADES, ("Baja", "Media", "Alta"))


class RepositorioTests(unittest.TestCase):
    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.ruta = Path(self._tmp.name) / "datos" / "organizador.sqlite3"
        self.repo = Repositorio(self.ruta)

    def test_creates_the_database_and_its_parent_folder(self):
        self.assertTrue(self.ruta.exists())
        self.assertEqual(self.repo.listar(), [])

    def test_add_returns_the_id_and_stores_a_pending_task(self):
        id_ = self.repo.agregar("  Preparar exposición ", "Alta")

        self.assertEqual(self.repo.listar(), [Tarea(id_, "Preparar exposición", "Alta", False)])

    def test_tasks_are_listed_newest_first(self):
        primera = self.repo.agregar("Primera", "Baja")
        segunda = self.repo.agregar("Segunda", "Baja")

        self.assertEqual([t.id for t in self.repo.listar()], [segunda, primera])

    def test_invalid_tasks_are_not_stored(self):
        with self.assertRaises(ValueError):
            self.repo.agregar("  ", "Media")
        with self.assertRaises(ValueError):
            self.repo.agregar("Tarea", "Inexistente")

        self.assertEqual(self.repo.listar(), [])

    def test_edit_changes_title_and_priority(self):
        id_ = self.repo.agregar("Leer", "Baja")

        self.repo.editar(id_, "Leer capítulo", "Alta")

        self.assertEqual(self.repo.listar(), [Tarea(id_, "Leer capítulo", "Alta", False)])

    def test_edit_validates_before_writing(self):
        id_ = self.repo.agregar("Leer", "Baja")

        with self.assertRaises(ValueError):
            self.repo.editar(id_, "", "Baja")

        self.assertEqual(self.repo.listar()[0].titulo, "Leer")

    def test_complete_and_reopen(self):
        id_ = self.repo.agregar("Leer", "Baja")

        self.repo.completar(id_, True)
        self.assertTrue(self.repo.listar()[0].completada)
        self.repo.completar(id_, False)
        self.assertFalse(self.repo.listar()[0].completada)

    def test_delete_removes_only_that_task(self):
        borrar = self.repo.agregar("Borrar", "Baja")
        conservar = self.repo.agregar("Conservar", "Baja")

        self.repo.eliminar(borrar)

        self.assertEqual([t.id for t in self.repo.listar()], [conservar])

    def test_operations_on_missing_ids_report_it(self):
        for operacion in (
            lambda: self.repo.editar(99, "Tarea", "Baja"),
            lambda: self.repo.completar(99, True),
            lambda: self.repo.eliminar(99),
        ):
            with self.assertRaisesRegex(ValueError, "ya no existe"):
                operacion()

    def test_search_ignores_case_and_surrounding_spaces(self):
        self.repo.agregar("Preparar EXPOSICIÓN", "Alta")
        self.repo.agregar("Leer capítulo", "Media")

        self.assertEqual([t.titulo for t in self.repo.listar(" exposición ")], ["Preparar EXPOSICIÓN"])
        self.assertEqual(len(self.repo.listar("")), 2)
        self.assertEqual(self.repo.listar("zzz"), [])

    def test_status_filters(self):
        hecha = self.repo.agregar("Hecha", "Baja")
        self.repo.agregar("Pendiente", "Baja")
        self.repo.completar(hecha, True)

        self.assertEqual([t.titulo for t in self.repo.listar(estado="Completadas")], ["Hecha"])
        self.assertEqual([t.titulo for t in self.repo.listar(estado="Pendientes")], ["Pendiente"])
        self.assertEqual(len(self.repo.listar(estado="Todas")), 2)

    def test_search_and_status_filters_combine(self):
        a = self.repo.agregar("Leer uno", "Baja")
        self.repo.agregar("Leer dos", "Baja")
        self.repo.completar(a, True)

        self.assertEqual([t.titulo for t in self.repo.listar("leer", "Pendientes")], ["Leer dos"])

    def test_unknown_status_filter_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Filtro desconocido"):
            self.repo.listar(estado="Archivadas")

    def test_tasks_survive_reopening_the_database(self):
        id_ = self.repo.agregar("Persistente", "Media")
        self.repo.completar(id_, True)

        reabierto = Repositorio(self.ruta)

        self.assertEqual(reabierto.listar(), [Tarea(id_, "Persistente", "Media", True)])

    def test_database_constraints_reject_invalid_rows_even_without_the_validator(self):
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repo.conexion() as con:
                con.execute("INSERT INTO tareas(titulo, prioridad) VALUES ('x', 'Urgente')")


if __name__ == "__main__":
    unittest.main()
