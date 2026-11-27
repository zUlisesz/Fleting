from database import execute, fetch_one
from domain import Ingredient


class IngredientRepository:
    def get_by_name(self, name: str) -> Ingredient | None:
        """Busca en el catálogo sin distinguir mayúsculas."""
        row = fetch_one(
            "SELECT id, name, unit FROM ingredients WHERE LOWER(name) = LOWER(%s)", (name,)
        )
        return Ingredient(**row) if row else None

    def create(self, ingredient: Ingredient) -> None:
        execute(
            "INSERT INTO ingredients (id, name, unit) VALUES (%s, %s, %s)",
            (ingredient.id, ingredient.name, ingredient.unit),
        )
