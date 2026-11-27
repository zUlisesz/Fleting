"""Construye la interfaz con una página simulada y ejercita los eventos principales."""

import os
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

import flet as ft

from organizador.main import main


def walk(control):
    """Recorre un árbol de controles ya construido."""
    yield control
    for name in ("content", "controls"):
        child = getattr(control, name, None)
        for item in child if isinstance(child, list) else [child]:
            if isinstance(item, ft.Control):
                yield from walk(item)


class MainTests(unittest.TestCase):
    def setUp(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        env = patch.dict(os.environ, {"FLET_CURSO_DATA_DIR": tmp.name})
        env.start()
        self.addCleanup(env.stop)

        self.page = MagicMock()
        main(self.page)
        self.controls = [c for root in self.page.add.call_args.args for c in walk(root)]

    def find(self, kind, **attrs):
        return next(
            c for c in self.controls
            if isinstance(c, kind) and all(getattr(c, k, None) == v for k, v in attrs.items())
        )

    def test_builds_the_form_with_its_defaults(self):
        self.page.add.assert_called_once()
        self.assertEqual(self.find(ft.Dropdown, label="Prioridad").value, "Media")
        self.assertEqual(self.find(ft.Dropdown, label="Mostrar").value, "Todas")
        self.assertEqual(self.find(ft.Button).content, "Agregar tarea")

    def test_an_empty_title_shows_an_error_on_the_field(self):
        titulo = self.find(ft.TextField, label="¿Qué necesitas hacer?")

        self.find(ft.Button).on_click(None)

        self.assertEqual(titulo.error, "Escribe entre 1 y 80 caracteres.")

    def test_saving_a_task_clears_the_form_and_the_error(self):
        titulo = self.find(ft.TextField, label="¿Qué necesitas hacer?")
        boton = self.find(ft.Button)
        boton.on_click(None)  # primero queda el error
        titulo.value = "Preparar exposición"

        boton.on_click(None)

        self.assertIsNone(titulo.error)
        self.assertEqual(titulo.value, "")
        self.assertEqual(self.find(ft.Button).content, "Agregar tarea")

    def test_the_theme_switch_toggles_dark_mode(self):
        interruptor = self.find(ft.Switch, label="Modo oscuro")

        interruptor.on_change(MagicMock(control=MagicMock(value=True)))
        self.assertEqual(self.page.theme_mode, ft.ThemeMode.DARK)
        interruptor.on_change(MagicMock(control=MagicMock(value=False)))
        self.assertEqual(self.page.theme_mode, ft.ThemeMode.LIGHT)


if __name__ == "__main__":
    unittest.main()
