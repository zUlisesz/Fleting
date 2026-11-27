"""Persistencia: una clase por tabla, solo SQL."""

from .ingredient import IngredientRepository
from .instruction import InstructionRepository
from .recipe import RecipeRepository
from .recipe_ingredient import RecipeIngredientRepository

__all__ = [
    "IngredientRepository",
    "InstructionRepository",
    "RecipeIngredientRepository",
    "RecipeRepository",
]
