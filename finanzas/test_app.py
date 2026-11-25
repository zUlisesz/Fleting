"""Regresión del cambio de perfil desde los controles de Flet."""

from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from finanzas.app import main
from finanzas.modelo import Repositorio


class ProfileSelectionTests(TestCase):
    def test_selection_refreshes_and_saves_to_the_selected_profile(self):
        with TemporaryDirectory() as directory:
            repo = Repositorio(Path(directory) / "finanzas.sqlite3")
            ana_id = repo.crear_perfil("Ana")
            repo.agregar("2026-11-10", "Despensa", "Comida", "Gasto", "150")
            page = SimpleNamespace(window=SimpleNamespace(), update=lambda: None)
            page.add = lambda *controls: setattr(page, "controls", controls)

            with patch.dict("os.environ", {"FLET_DATA_DIR": directory}):
                main(page)

            profile = page.controls[1].controls[0]
            form = page.controls[3].content.content.controls
            fields = form[1].controls
            table = page.controls[-2].controls[0]
            self.assertEqual(table.rows[0].cells[1].content.value, "Despensa")

            profile.value = str(ana_id)
            self.assertIsNotNone(profile.on_select)
            profile.on_select(SimpleNamespace(control=profile))
            self.assertFalse(table.visible)

            fields[0].value = "Honorarios"
            fields[1].value = "900"
            form[2].on_click(None)
            self.assertEqual(table.rows[0].cells[1].content.value, "Honorarios")

            profile.value = "1"
            profile.on_select(SimpleNamespace(control=profile))
            self.assertEqual(table.rows[0].cells[1].content.value, "Despensa")
            repo.seleccionar_perfil(ana_id)
            self.assertEqual([item.concepto for item in repo.listar()], ["Honorarios"])
