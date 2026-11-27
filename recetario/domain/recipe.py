from datetime import datetime

from pydantic import BaseModel, Field

from .instruction import Instruction
from .recipe_ingredient import IngredientLine


class Recipe(BaseModel):
    id: str
    title: str
    created_at: datetime | None = None


class RecipeDetail(Recipe):
    """Receta con sus ingredientes (por nombre) y sus pasos (por número)."""

    ingredients: list[IngredientLine] = Field(default_factory=list)
    instructions: list[Instruction] = Field(default_factory=list)

    @property
    def next_step_number(self) -> int:
        return max((step.step_number for step in self.instructions), default=0) + 1
