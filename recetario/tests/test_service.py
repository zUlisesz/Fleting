import unittest
from datetime import datetime
from unittest.mock import create_autospec

from domain import Ingredient, IngredientLine, Instruction, Recipe
from repositories import (
    IngredientRepository,
    InstructionRepository,
    RecipeIngredientRepository,
    RecipeRepository,
)
from services import RecipeService


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.recipes = create_autospec(RecipeRepository, instance=True)
        self.ingredients = create_autospec(IngredientRepository, instance=True)
        self.instructions = create_autospec(InstructionRepository, instance=True)
        self.links = create_autospec(RecipeIngredientRepository, instance=True)
        self.service = RecipeService(self.recipes, self.ingredients, self.instructions, self.links)


class RecipeTests(ServiceTestCase):
    def test_create_recipe_normalizes_the_title_and_persists_it(self):
        recipe = self.service.create_recipe("  Sopa  ", recipe_id="recipe-1")

        self.assertEqual(recipe, Recipe(id="recipe-1", title="Sopa"))
        self.recipes.create.assert_called_once_with(recipe)

    def test_create_recipe_generates_an_id(self):
        self.assertTrue(self.service.create_recipe("Sopa").id)

    def test_update_and_delete_delegate_to_the_repository(self):
        self.recipes.update_title.return_value = True
        self.recipes.delete.return_value = True

        self.assertTrue(self.service.update_recipe_title("recipe-1", " Sopa verde "))
        self.assertTrue(self.service.delete_recipe("recipe-1"))

        self.recipes.update_title.assert_called_once_with("recipe-1", "Sopa verde")
        self.recipes.delete.assert_called_once_with("recipe-1")

    def test_detail_gathers_the_recipe_its_ingredients_and_its_steps(self):
        created = datetime(2026, 1, 2, 3, 4)
        self.recipes.get.return_value = Recipe(id="r1", title="Sopa", created_at=created)
        line = IngredientLine(link_id="l1", ingredient_id="i1", name="Sal", amount="5", unit="g")
        step = Instruction(id="s1", recipe_id="r1", step_number=1, instruction="Hervir")
        self.links.list_for_recipe.return_value = [line]
        self.instructions.list_for_recipe.return_value = [step]

        detail = self.service.get_recipe_detail(" r1 ")

        self.assertEqual((detail.id, detail.title, detail.created_at), ("r1", "Sopa", created))
        self.assertEqual(detail.ingredients, [line])
        self.assertEqual(detail.instructions, [step])
        self.recipes.get.assert_called_once_with("r1")

    def test_detail_of_a_missing_recipe_is_none_and_skips_the_other_queries(self):
        self.recipes.get.return_value = None

        self.assertIsNone(self.service.get_recipe_detail("missing"))
        self.links.list_for_recipe.assert_not_called()
        self.instructions.list_for_recipe.assert_not_called()


class IngredientTests(ServiceTestCase):
    def test_adding_a_new_ingredient_creates_the_catalog_entry_and_the_link(self):
        self.ingredients.get_by_name.return_value = None
        self.links.list_for_recipe.return_value = []

        link = self.service.add_ingredient_to_recipe("recipe-1", " Jitomate ", amount="2", unit="piezas")

        created = self.ingredients.create.call_args.args[0]
        self.assertEqual((created.name, created.unit), ("Jitomate", "piezas"))
        self.assertEqual((link.recipe_id, link.ingredient_id, link.amount), ("recipe-1", created.id, "2"))
        self.links.add.assert_called_once_with(link)

    def test_adding_a_known_ingredient_reuses_the_catalog_entry(self):
        self.ingredients.get_by_name.return_value = Ingredient(id="i1", name="Sal", unit="g")
        self.links.list_for_recipe.return_value = []

        link = self.service.add_ingredient_to_recipe("recipe-1", "sal", amount="5", unit="kg")

        self.ingredients.create.assert_not_called()
        self.assertEqual(link.ingredient_id, "i1")
        self.ingredients.get_by_name.assert_called_once_with("sal")  # una sola consulta

    def test_rejects_an_ingredient_already_in_the_recipe(self):
        self.ingredients.get_by_name.return_value = Ingredient(id="i1", name="Sal")
        self.links.list_for_recipe.return_value = [
            IngredientLine(link_id="l1", ingredient_id="i1", name="Sal")
        ]

        with self.assertRaisesRegex(ValueError, "ya está agregado"):
            self.service.add_ingredient_to_recipe("recipe-1", "Sal")

        self.links.add.assert_not_called()

    def test_blank_amount_and_unit_are_stored_as_none(self):
        self.ingredients.get_by_name.return_value = None
        self.links.list_for_recipe.return_value = []

        link = self.service.add_ingredient_to_recipe("recipe-1", "Sal", amount="  ", unit="")

        self.assertIsNone(link.amount)
        self.assertIsNone(self.ingredients.create.call_args.args[0].unit)

    def test_register_ingredient_returns_the_existing_one(self):
        existing = Ingredient(id="i1", name="Sal")
        self.ingredients.get_by_name.return_value = existing

        self.assertIs(self.service.register_ingredient("Sal"), existing)
        self.ingredients.create.assert_not_called()

    def test_remove_ingredient_delegates_to_the_repository(self):
        self.links.remove.return_value = True

        self.assertTrue(self.service.remove_ingredient_from_recipe("link-1"))
        self.links.remove.assert_called_once_with("link-1")


class StepTests(ServiceTestCase):
    def test_add_and_delete_step(self):
        step = self.service.add_step("recipe-1", 1, " Cortar los vegetales ", step_id="step-1")

        self.assertEqual(
            step,
            Instruction(id="step-1", recipe_id="recipe-1", step_number=1, instruction="Cortar los vegetales"),
        )
        self.instructions.create.assert_called_once_with(step)

        self.instructions.delete.return_value = True
        self.assertTrue(self.service.delete_step("step-1"))
        self.instructions.delete.assert_called_once_with("step-1")


class ValidationTests(ServiceTestCase):
    def test_rejects_blank_text_and_invalid_step_numbers(self):
        invalid_calls = [
            lambda: self.service.create_recipe("   "),
            lambda: self.service.register_ingredient(" "),
            lambda: self.service.add_step("recipe-1", 0, "Mezclar"),
            lambda: self.service.add_step("recipe-1", True, "Mezclar"),
            lambda: self.service.add_step("recipe-1", 1, " "),
        ]
        for call in invalid_calls:
            with self.subTest(call=call):
                with self.assertRaises(ValueError):
                    call()

    def test_rejects_text_over_the_limits(self):
        with self.assertRaisesRegex(ValueError, "120"):
            self.service.create_recipe("x" * 121)
        with self.assertRaisesRegex(ValueError, "500"):
            self.service.add_step("recipe-1", 1, "x" * 501)
        with self.assertRaisesRegex(ValueError, "40"):
            self.service.add_ingredient_to_recipe("recipe-1", "Sal", amount="x" * 41)

    def test_rejects_non_text_values_with_a_validation_error(self):
        for value in (None, 12, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.service.create_recipe(value)
        with self.assertRaises(ValueError):
            self.service.register_ingredient("Sal", unit=5)

    def test_rejects_missing_identifiers_before_touching_the_repositories(self):
        for identifier in (None, "   "):
            with self.subTest(identifier=identifier):
                for call in (
                    lambda: self.service.add_step(identifier, 1, "Mezclar"),
                    lambda: self.service.add_ingredient_to_recipe(identifier, "Sal"),
                    lambda: self.service.get_recipe_detail(identifier),
                    lambda: self.service.delete_step(identifier),
                ):
                    with self.assertRaises(ValueError):
                        call()

        self.instructions.create.assert_not_called()
        self.ingredients.create.assert_not_called()


if __name__ == "__main__":
    unittest.main()
