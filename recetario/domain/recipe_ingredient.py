from typing import Optional
from pydantic import BaseModel

class RecipeIngredient(BaseModel):
    id: str
    recipe_id: str
    ingredient_id: str
    amount: Optional[str] = None
