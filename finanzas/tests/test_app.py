"""Renderiza la interfaz sin abrir una ventana."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import flet as ft

from finanzas.app import App, cargar
from finanzas.dominio import Filtros
from finanzas.main import main
from finanzas.repositorio import Repositorio

from .render import render


class AppRenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.repo = Repositorio(Path(self._tmp.name) / "finanzas.sqlite3")

    def textos(self) -> list[str]:
        return [c.value for c in render(App, self.repo) if isinstance(c, ft.Text)]

    def test_empty_profile_shows_empty_states(self) -> None:
        textos = self.textos()

        self.assertIn("No hay movimientos para estos filtros.", textos)
        self.assertIn("Las proporciones aparecerán al registrar movimientos.", textos)

    def test_saved_movements_appear_in_the_table_and_summary(self) -> None:
        self.repo.agregar(1, "2026-11-10", "Nómina", "Trabajo", "Ingreso", "1000")
        self.repo.agregar(1, "2026-11-11", "Despensa", "Comida", "Gasto", "125.50")

        textos = self.textos()

        self.assertIn("Despensa", textos)
        self.assertIn("$874.50", textos)  # saldo
        self.assertIn("-$125.50", textos)

    def test_cargar_reports_invalid_filters_without_raising(self) -> None:
        movimientos, error = cargar(self.repo, 1, Filtros(mes="2026-13"))

        self.assertEqual(movimientos, [])
        self.assertEqual(error, "Mes inválido.")

    def test_main_is_callable(self) -> None:
        self.assertTrue(callable(main))


if __name__ == "__main__":
    unittest.main()
