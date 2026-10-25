import unittest
from unittest.mock import patch

from repositories.ingredient import IngredientRepository
from repositories.instruction import IntructionRepository
from repositories.recipe import RecipeRepository
from repositories.recipe_ingredient import RecipeIngredientRepository
from services.recipe_service import RecipeService


class RecipeServiceTests(unittest.TestCase):
    def test_create_recipe_persists_and_returns_recipe(self):
        with patch.object(RecipeRepository, "createRecipe") as create_recipe:
            recipe = RecipeService.create_recipe("Sopa", recipe_id="recipe-1")

        self.assertEqual(recipe.id, "recipe-1")
        self.assertEqual(recipe.title, "Sopa")
        create_recipe.assert_called_once_with(recipe)

    def test_update_and_delete_recipe_delegate_to_repository(self):
        with patch.object(RecipeRepository, "updateRecipe", return_value=True) as update_recipe:
            self.assertTrue(RecipeService.update_recipe_title("recipe-1", "Sopa verde"))
        update_recipe.assert_called_once_with("recipe-1", "Sopa verde")

        with patch.object(RecipeRepository, "deleteRecipe", return_value=True) as delete_recipe:
            self.assertTrue(RecipeService.delete_recipe("recipe-1"))
        delete_recipe.assert_called_once_with("recipe-1")

    def test_add_ingredient_creates_catalog_entry_and_recipe_link(self):
        with patch.object(IngredientRepository, "getByName", side_effect=[None, None]), \
             patch.object(IngredientRepository, "createIngredient") as create_ingredient, \
             patch.object(RecipeIngredientRepository, "addIngredientToRecipe") as attach_ingredient:
            link = RecipeService.add_ingredient_to_recipe(
                "recipe-1", "Jitomate", amount="2", unit="piezas"
            )

        ingredient = create_ingredient.call_args.args[0]
        self.assertEqual(ingredient.name, "Jitomate")
        self.assertEqual(ingredient.unit, "piezas")
        self.assertEqual(link.recipe_id, "recipe-1")
        self.assertEqual(link.ingredient_id, ingredient.id)
        self.assertEqual(link.amount, "2")
        attach_ingredient.assert_called_once_with(link)

    def test_add_ingredient_reuses_existing_catalog_entry(self):
        existing = {"id": "ingredient-1", "name": "Sal", "unit": "g"}
        with patch.object(IngredientRepository, "getByName", return_value=existing), \
             patch.object(IngredientRepository, "createIngredient") as create_ingredient, \
             patch.object(RecipeIngredientRepository, "addIngredientToRecipe") as attach_ingredient:
            link = RecipeService.add_ingredient_to_recipe(
                "recipe-1", "Sal", amount="5", unit="g"
            )

        create_ingredient.assert_not_called()
        self.assertEqual(link.ingredient_id, "ingredient-1")
        self.assertEqual(link.amount, "5")
        attach_ingredient.assert_called_once_with(link)

    def test_remove_ingredient_link_delegates_to_repository(self):
        with patch.object(
            RecipeIngredientRepository, "removeIngredientFromRecipe", return_value=True
        ) as remove_ingredient:
            self.assertTrue(RecipeService.remove_ingredient_from_recipe("link-1"))
        remove_ingredient.assert_called_once_with("link-1")

    def test_add_and_delete_instruction_step(self):
        with patch.object(IntructionRepository, "createInstruction") as create_instruction:
            step = RecipeService.add_step(
                "recipe-1", step_number=1, instruction_text="Cortar los vegetales", step_id="step-1"
            )

        self.assertEqual(step.id, "step-1")
        self.assertEqual(step.recipe_id, "recipe-1")
        self.assertEqual(step.step_number, 1)
        self.assertEqual(step.instruction, "Cortar los vegetales")
        create_instruction.assert_called_once_with(step)

        with patch.object(
            IntructionRepository, "deleteInstruction", return_value=True
        ) as delete_instruction:
            self.assertTrue(RecipeService.delete_step("step-1"))
        delete_instruction.assert_called_once_with("step-1")


if __name__ == "__main__":
    unittest.main()
