from pydantic import BaseModel


class RecipeIngredient(BaseModel):
    """Vínculo entre una receta y un ingrediente del catálogo, con su cantidad."""

    id: str
    recipe_id: str
    ingredient_id: str
    amount: str | None = None


class IngredientLine(BaseModel):
    """Ingrediente tal como se muestra en una receta (vínculo + datos del catálogo)."""

    link_id: str
    ingredient_id: str
    name: str
    unit: str | None = None
    amount: str | None = None

    @property
    def quantity(self) -> str:
        """Cantidad con unidad (``"2 piezas"``); solo la unidad si no hay cantidad."""
        if self.amount:
            return f"{self.amount} {self.unit}" if self.unit else self.amount
        return self.unit or ""
