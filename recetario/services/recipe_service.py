import uuid
from typing import List, Optional, Dict, Any

from domain.recipe import Recipe
from domain.ingredient import Ingredient
from domain.instruction import Instruction
from domain.recipe_ingredient import RecipeIngredient

from repositories.recipe import RecipeRepository
from repositories.ingredient import IngredientRepository
from repositories.instruction import IntructionRepository
from repositories.recipe_ingredient import RecipeIngredientRepository


def _required_text(value: str, field_name: str, maximum_length: int) -> str:
    """Normalize required user text before it reaches the persistence layer."""
    if not isinstance(value, str):
        raise ValueError(f"{field_name} debe ser texto.")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} no puede estar vacío.")
    if len(normalized) > maximum_length:
        raise ValueError(f"{field_name} no puede superar {maximum_length} caracteres.")
    return normalized


def _optional_text(value: Optional[str], maximum_length: int) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("El texto debe ser válido.")
    normalized = value.strip()
    if not normalized:
        return None
    if len(normalized) > maximum_length:
        raise ValueError(f"El texto no puede superar {maximum_length} caracteres.")
    return normalized


class RecipeService:
    @staticmethod
    def create_recipe(title: str, recipe_id: Optional[str] = None) -> Recipe:
        title = _required_text(title, "El título", 120)
        rid = recipe_id or str(uuid.uuid4())
        recipe = Recipe(id=rid, title=title)
        RecipeRepository.createRecipe(recipe)
        return recipe

    @staticmethod
    def get_all_recipes() -> List[Dict[str, Any]]:
        return RecipeRepository.readRecipes()

    @staticmethod
    def get_recipe_detail(recipe_id: str) -> Optional[Dict[str, Any]]:
        return RecipeRepository.getFullRecipe(recipe_id)

    @staticmethod
    def delete_recipe(recipe_id: str) -> bool:
        return RecipeRepository.deleteRecipe(recipe_id)

    @staticmethod
    def update_recipe_title(recipe_id: str, new_title: str) -> bool:
        title = _required_text(new_title, "El título", 120)
        return RecipeRepository.updateRecipe(recipe_id, title)


    @staticmethod
    def register_ingredient(name: str, unit: Optional[str] = None, ingredient_id: Optional[str] = None) -> Ingredient:
        name = _required_text(name, "El ingrediente", 120)
        unit = _optional_text(unit, 40)
        existing = IngredientRepository.getByName(name)
        if existing:
            return Ingredient(id=existing["id"], name=existing["name"], unit=existing.get("unit"))
        
        iid = ingredient_id or str(uuid.uuid4())
        ingredient = Ingredient(id=iid, name=name, unit=unit)
        IngredientRepository.createIngredient(ingredient)
        return ingredient

    @staticmethod
    def get_all_ingredients() -> List[Dict[str, Any]]:
        return IngredientRepository.readData()

    @staticmethod
    def add_ingredient_to_recipe(recipe_id: str, ingredient_name: str, amount: Optional[str] = None, unit: Optional[str] = None) -> RecipeIngredient:
        """
        Reuses an existing ingredient by name or creates it if not found, then attaches it to the recipe.
        """
        ingredient_name = _required_text(ingredient_name, "El ingrediente", 120)
        amount = _optional_text(amount, 40)
        unit = _optional_text(unit, 40)
        ingredient = IngredientRepository.getByName(ingredient_name)
        if not ingredient:
            ingredient_obj = RecipeService.register_ingredient(name=ingredient_name, unit=unit)
            ing_id = ingredient_obj.id
        else:
            ing_id = ingredient["id"]

        link = RecipeIngredient(
            id=str(uuid.uuid4()),
            recipe_id=recipe_id,
            ingredient_id=ing_id,
            amount=amount
        )
        RecipeIngredientRepository.addIngredientToRecipe(link)
        return link

    @staticmethod
    def remove_ingredient_from_recipe(recipe_ingredient_id: str) -> bool:
        return RecipeIngredientRepository.removeIngredientFromRecipe(recipe_ingredient_id)


    @staticmethod
    def add_step(recipe_id: str, step_number: int, instruction_text: str, step_id: Optional[str] = None) -> Instruction:
        if type(step_number) is not int or step_number < 1:
            raise ValueError("El número de paso debe ser un entero mayor que cero.")
        instruction_text = _required_text(instruction_text, "La instrucción", 500)
        step = Instruction(
            id=step_id or str(uuid.uuid4()),
            recipe_id=recipe_id,
            step_number=step_number,
            instruction=instruction_text
        )
        IntructionRepository.createInstruction(step)
        return step

    @staticmethod
    def get_steps_for_recipe(recipe_id: str) -> List[Dict[str, Any]]:
        return IntructionRepository.readInstructions(recipe_id)

    @staticmethod
    def delete_step(instruction_id: str) -> bool:
        return IntructionRepository.deleteInstruction(instruction_id)
