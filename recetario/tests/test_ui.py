"""Estado y componentes de la interfaz, renderizados sin ventana."""

import unittest
from unittest.mock import create_autospec, patch

import flet as ft

from database import StorageError
from domain import IngredientLine, Instruction, Recipe, RecipeDetail
from main import main
from services import RecipeService
from ui.app import App, filter_recipes, load, resolve_selection
from ui.dialogs import ConfirmDeleteDialog, IngredientDialog, RecipeTitleDialog, StepDialog
from ui.detail import ErrorMessage, NoSelection, RecipeDetailView
from ui.sidebar import Sidebar

from .render import render

RECIPES = [Recipe(id="1", title="Sopa de tomate"), Recipe(id="2", title="Pastel")]
NOOP = lambda *_: None


def texts(controls) -> list[str]:
    return [c.value for c in controls if isinstance(c, ft.Text)]


class StateHelpersTests(unittest.TestCase):
    def test_filter_recipes_ignores_case_and_surrounding_spaces(self):
        self.assertEqual(filter_recipes(RECIPES, " SOPA "), [RECIPES[0]])
        self.assertEqual(filter_recipes(RECIPES, ""), RECIPES)
        self.assertEqual(filter_recipes(RECIPES, "pizza"), [])

    def test_resolve_selection_keeps_a_valid_choice_or_falls_back_to_the_first(self):
        self.assertEqual(resolve_selection(RECIPES, "2"), "2")
        self.assertEqual(resolve_selection(RECIPES, "gone"), "1")
        self.assertEqual(resolve_selection(RECIPES, None), "1")
        self.assertIsNone(resolve_selection([], "1"))

    def test_load_reports_expected_errors_without_raising(self):
        def fail():
            raise StorageError("sin conexión")

        self.assertEqual(load(lambda: [1], []), ([1], None))
        self.assertEqual(load(fail, []), ([], "sin conexión"))
        with self.assertRaises(KeyError):  # los errores inesperados no se ocultan
            load(lambda: {}["x"], None)


class SidebarTests(unittest.TestCase):
    def build(self, recipes, selected=None, query=""):
        return render(Sidebar, recipes, selected_id=selected, query=query,
                      on_query=NOOP, on_select=NOOP, on_new=NOOP)

    def test_lists_recipes_and_marks_the_selected_one(self):
        controls = self.build(RECIPES, selected="2")

        self.assertIn("Sopa de tomate", texts(controls))
        self.assertIn("Pastel", texts(controls))
        selected = [c for c in controls if isinstance(c, ft.Container) and c.bgcolor == ft.Colors.TEAL_50]
        self.assertEqual(len(selected), 1)

    def test_empty_states_depend_on_whether_there_is_a_query(self):
        self.assertIn("Aún no tienes recetas registradas", texts(self.build([])))
        self.assertIn("No se encontraron recetas", texts(self.build([], query="pizza")))


class DetailTests(unittest.TestCase):
    def detail(self, **kwargs) -> RecipeDetail:
        return RecipeDetail(id="abcdefghij", title="Sopa", **kwargs)

    def build(self, detail):
        return render(RecipeDetailView, detail, on_edit=NOOP, on_delete=NOOP, on_add_ingredient=NOOP,
                      on_remove_ingredient=NOOP, on_add_step=NOOP, on_delete_step=NOOP)

    def test_empty_recipe_shows_hints(self):
        shown = texts(self.build(self.detail()))

        self.assertIn("Sopa", shown)
        self.assertIn("ID: abcdefgh...", shown)
        self.assertIn("No has agregado ingredientes aún.", shown)
        self.assertIn("No has agregado pasos o instrucciones aún.", shown)

    def test_ingredients_and_steps_are_listed(self):
        detail = self.detail(
            ingredients=[IngredientLine(link_id="l", ingredient_id="i", name="Sal", amount="5", unit="g")],
            instructions=[Instruction(id="s", recipe_id="r", step_number=3, instruction="Hervir")],
        )

        shown = texts(self.build(detail))

        self.assertIn("Sal", shown)
        self.assertIn("— 5 g", shown)
        self.assertIn("3", shown)
        self.assertIn("Hervir", shown)
        self.assertNotIn("No has agregado ingredientes aún.", shown)

    def test_placeholder_and_error_screens(self):
        self.assertIn("Selecciona o crea una receta", texts(render(NoSelection, on_create=NOOP)))
        self.assertIn("MySQL caído", texts(render(ErrorMessage, "MySQL caído", on_retry=NOOP)))


class DialogTests(unittest.TestCase):
    """``ft.use_dialog`` necesita una página: se captura el diálogo que recibiría."""

    def open(self, component, *args, **kwargs) -> ft.AlertDialog:
        shown = []
        with patch("flet.use_dialog", side_effect=shown.append):
            render(component, *args, **kwargs)
        return shown[-1]

    def test_title_dialog_submits_the_initial_text_and_cancel_closes(self):
        calls = []
        dialog = self.open(
            RecipeTitleDialog, "Editar receta", confirm_label="Actualizar", initial="Sopa",
            on_submit=calls.append, on_close=lambda: calls.append("close"),
        )

        self.assertEqual(dialog.title.value, "Editar receta")
        dialog.actions[1].on_click(None)
        dialog.actions[0].on_click(None)

        self.assertEqual(calls, ["Sopa", "close"])

    def test_step_dialog_suggests_the_next_number(self):
        calls = []
        dialog = self.open(StepDialog, 4, on_submit=lambda n, t: calls.append((n, t)), on_close=NOOP)

        dialog.actions[1].on_click(None)

        self.assertEqual(calls, [(4, "")])

    def test_step_dialog_rejects_a_non_numeric_number_without_calling_on_submit(self):
        calls = []
        dialog = self.open(StepDialog, "abc", on_submit=lambda n, t: calls.append(n), on_close=NOOP)

        dialog.actions[1].on_click(None)

        self.assertEqual(calls, [])

    def test_form_errors_keep_the_dialog_open(self):
        closed = []

        def reject(*_):
            raise ValueError("El ingrediente no puede estar vacío.")

        dialog = self.open(IngredientDialog, on_submit=reject, on_close=lambda: closed.append(1))

        dialog.actions[1].on_click(None)  # no debe propagar la excepción

        self.assertEqual(closed, [])

    def test_confirm_dialog_runs_the_action(self):
        calls = []
        dialog = self.open(
            ConfirmDeleteDialog, "Eliminar receta", "¿Seguro?",
            on_confirm=lambda: calls.append("delete"), on_close=lambda: calls.append("close"),
        )

        dialog.actions[1].on_click(None)

        self.assertEqual(calls, ["delete"])


class AppTests(unittest.TestCase):
    def service(self, recipes, detail=None):
        service = create_autospec(RecipeService, instance=True)
        service.get_all_recipes.return_value = recipes
        service.get_recipe_detail.return_value = detail
        return service

    def test_first_recipe_is_selected_and_its_detail_loaded(self):
        detail = RecipeDetail(id="1", title="Sopa de tomate")
        service = self.service(RECIPES, detail)

        shown = texts(render(App, service))

        service.get_recipe_detail.assert_called_once_with("1")
        self.assertIn("Ingredientes", shown)
        self.assertIn("Pastel", shown)

    def test_without_recipes_it_invites_to_create_one(self):
        service = self.service([])

        shown = texts(render(App, service))

        service.get_recipe_detail.assert_not_called()
        self.assertIn("Selecciona o crea una receta", shown)
        self.assertIn("Aún no tienes recetas registradas", shown)

    def test_storage_errors_are_shown_instead_of_crashing(self):
        service = self.service([])
        service.get_all_recipes.side_effect = StorageError("Error de base de datos: sin servidor")

        shown = texts(render(App, service))

        self.assertIn("No se pudo cargar el recetario: Error de base de datos: sin servidor", shown)

    def test_main_is_callable(self):
        self.assertTrue(callable(main))


if __name__ == "__main__":
    unittest.main()
