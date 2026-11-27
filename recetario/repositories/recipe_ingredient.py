from database import execute, fetch_all
from domain import IngredientLine, RecipeIngredient


class RecipeIngredientRepository:
    def add(self, link: RecipeIngredient) -> None:
        execute(
            "INSERT INTO recipe_ingredients (id, recipe_id, ingredient_id, amount) "
            "VALUES (%s, %s, %s, %s)",
            (link.id, link.recipe_id, link.ingredient_id, link.amount),
        )

    def list_for_recipe(self, recipe_id: str) -> list[IngredientLine]:
        rows = fetch_all(
            "SELECT ri.id AS link_id, ri.ingredient_id, ri.amount, i.name, i.unit "
            "FROM recipe_ingredients ri "
            "JOIN ingredients i ON ri.ingredient_id = i.id "
            "WHERE ri.recipe_id = %s ORDER BY i.name ASC",
            (recipe_id,),
        )
        return [IngredientLine(**row) for row in rows]

    def remove(self, link_id: str) -> bool:
        return execute("DELETE FROM recipe_ingredients WHERE id = %s", (link_id,)) > 0
