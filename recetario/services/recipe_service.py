"""Casos de uso del recetario: validan y normalizan antes de persistir.

``RecipeService`` recibe sus repositorios, así que se prueba con dobles sin
necesidad de MySQL. Las entradas inválidas lanzan ``ValueError`` con un mensaje
apto para mostrarse al usuario.
"""

import uuid

from domain import (
    Ingredient,
    Instruction,
    Recipe,
    RecipeDetail,
    RecipeIngredient,
)
from repositories import (
    IngredientRepository,
    InstructionRepository,
    RecipeIngredientRepository,
    RecipeRepository,
)

MAX_TITLE = 120
MAX_INGREDIENT_NAME = 120
MAX_SHORT_TEXT = 40  # cantidad y unidad
MAX_INSTRUCTION = 500


def _new_id() -> str:
    return str(uuid.uuid4())


def _required_text(value: str, field_name: str, maximum_length: int) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} debe ser texto.")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} no puede estar vacío.")
    if len(normalized) > maximum_length:
        raise ValueError(f"{field_name} no puede superar {maximum_length} caracteres.")
    return normalized


def _optional_text(value: str | None, field_name: str, maximum_length: int) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field_name} debe ser texto.")
    normalized = value.strip()
    if not normalized:
        return None
    if len(normalized) > maximum_length:
        raise ValueError(f"{field_name} no puede superar {maximum_length} caracteres.")
    return normalized


def _required_identifier(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} debe ser un identificador válido.")
    return value.strip()


class RecipeService:
    def __init__(
        self,
        recipes: RecipeRepository,
        ingredients: IngredientRepository,
        instructions: InstructionRepository,
        links: RecipeIngredientRepository,
    ) -> None:
        self._recipes = recipes
        self._ingredients = ingredients
        self._instructions = instructions
        self._links = links

    # Recetas

    def create_recipe(self, title: str, recipe_id: str | None = None) -> Recipe:
        recipe = Recipe(id=recipe_id or _new_id(), title=_required_text(title, "El título", MAX_TITLE))
        self._recipes.create(recipe)
        return recipe

    def get_all_recipes(self) -> list[Recipe]:
        return self._recipes.list_all()

    def get_recipe_detail(self, recipe_id: str) -> RecipeDetail | None:
        """Receta con ingredientes y pasos ordenados; ``None`` si no existe."""
        recipe_id = _required_identifier(recipe_id, "La receta")
        recipe = self._recipes.get(recipe_id)
        if recipe is None:
            return None
        return RecipeDetail(
            **recipe.model_dump(),
            ingredients=self._links.list_for_recipe(recipe_id),
            instructions=self._instructions.list_for_recipe(recipe_id),
        )

    def update_recipe_title(self, recipe_id: str, new_title: str) -> bool:
        title = _required_text(new_title, "El título", MAX_TITLE)
        return self._recipes.update_title(_required_identifier(recipe_id, "La receta"), title)

    def delete_recipe(self, recipe_id: str) -> bool:
        return self._recipes.delete(_required_identifier(recipe_id, "La receta"))

    # Ingredientes

    def register_ingredient(
        self, name: str, unit: str | None = None, ingredient_id: str | None = None
    ) -> Ingredient:
        """Devuelve el ingrediente del catálogo con ese nombre, o lo crea."""
        name = _required_text(name, "El ingrediente", MAX_INGREDIENT_NAME)
        unit = _optional_text(unit, "La unidad", MAX_SHORT_TEXT)
        existing = self._ingredients.get_by_name(name)
        if existing:
            return existing
        ingredient = Ingredient(id=ingredient_id or _new_id(), name=name, unit=unit)
        self._ingredients.create(ingredient)
        return ingredient

    def add_ingredient_to_recipe(
        self,
        recipe_id: str,
        ingredient_name: str,
        amount: str | None = None,
        unit: str | None = None,
    ) -> RecipeIngredient:
        """Vincula un ingrediente (reutilizado del catálogo o nuevo) a la receta."""
        recipe_id = _required_identifier(recipe_id, "La receta")
        amount = _optional_text(amount, "La cantidad", MAX_SHORT_TEXT)
        ingredient = self.register_ingredient(ingredient_name, unit)

        current = self._links.list_for_recipe(recipe_id)
        if any(line.ingredient_id == ingredient.id for line in current):
            raise ValueError("El ingrediente ya está agregado a la receta.")

        link = RecipeIngredient(
            id=_new_id(), recipe_id=recipe_id, ingredient_id=ingredient.id, amount=amount
        )
        self._links.add(link)
        return link

    def remove_ingredient_from_recipe(self, link_id: str) -> bool:
        return self._links.remove(_required_identifier(link_id, "El ingrediente"))

    # Pasos

    def add_step(
        self,
        recipe_id: str,
        step_number: int,
        instruction_text: str,
        step_id: str | None = None,
    ) -> Instruction:
        recipe_id = _required_identifier(recipe_id, "La receta")
        if type(step_number) is not int or step_number < 1:
            raise ValueError("El número de paso debe ser un entero mayor que cero.")
        step = Instruction(
            id=step_id or _new_id(),
            recipe_id=recipe_id,
            step_number=step_number,
            instruction=_required_text(instruction_text, "La instrucción", MAX_INSTRUCTION),
        )
        self._instructions.create(step)
        return step

    def delete_step(self, instruction_id: str) -> bool:
        return self._instructions.delete(_required_identifier(instruction_id, "La instrucción"))


def create_service() -> RecipeService:
    """Servicio conectado a los repositorios MySQL."""
    return RecipeService(
        RecipeRepository(),
        IngredientRepository(),
        InstructionRepository(),
        RecipeIngredientRepository(),
    )
