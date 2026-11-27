from database import execute, fetch_all, fetch_one
from domain import Recipe


class RecipeRepository:
    def create(self, recipe: Recipe) -> None:
        execute("INSERT INTO recipes (id, title) VALUES (%s, %s)", (recipe.id, recipe.title))

    def list_all(self) -> list[Recipe]:
        rows = fetch_all("SELECT id, title, created_at FROM recipes ORDER BY created_at DESC")
        return [Recipe(**row) for row in rows]

    def get(self, recipe_id: str) -> Recipe | None:
        row = fetch_one("SELECT id, title, created_at FROM recipes WHERE id = %s", (recipe_id,))
        return Recipe(**row) if row else None

    def update_title(self, recipe_id: str, title: str) -> bool:
        return execute("UPDATE recipes SET title = %s WHERE id = %s", (title, recipe_id)) > 0

    def delete(self, recipe_id: str) -> bool:
        return execute("DELETE FROM recipes WHERE id = %s", (recipe_id,)) > 0
