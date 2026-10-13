from typing import List, Optional, Dict, Any
from database.config import get_connection
from domain.recipe import Recipe

class RecipeRepository:
    @staticmethod
    def createRecipe(recipe: Recipe) -> None:
        vals = (recipe.id, recipe.title)
        query = 'INSERT INTO recipes (id, title) VALUES (%s, %s)'
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, vals)
            conn.commit()

    @staticmethod
    def readRecipes():
        query = 'SELECT id, title, created_at FROM recipes ORDER BY created_at DESC'
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    @staticmethod
    def getById(recipe_id: str) :
        query = 'SELECT id, title, created_at FROM recipes WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, (recipe_id,))
                return cursor.fetchone()

    @staticmethod
    def updateRecipe(recipe_id: str, title: str) -> bool:
        query = 'UPDATE recipes SET title = %s WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (title, recipe_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def deleteRecipe(recipe_id: str) -> bool:
        query = 'DELETE FROM recipes WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (recipe_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def getFullRecipe(recipe_id: str):
        """
        Retrieves the recipe along with its ingredients and ordered instructions.
        """
        recipe = RecipeRepository.getById(recipe_id)
        if not recipe:
            return None

        query_ingredients = '''
            SELECT 
                ri.id AS link_id,
                ri.ingredient_id,
                i.name,
                i.unit,
                ri.amount
            FROM recipe_ingredients ri
            JOIN ingredients i ON ri.ingredient_id = i.id
            WHERE ri.recipe_id = %s
            ORDER BY i.name ASC
        '''

        query_instructions = '''
            SELECT id, step_number, instruction
            FROM recipe_instructions
            WHERE recipe_id = %s
            ORDER BY step_number ASC
        '''

        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query_ingredients, (recipe_id,))
                ingredients = cursor.fetchall()

                cursor.execute(query_instructions, (recipe_id,))
                instructions = cursor.fetchall()

        return {
            "id": recipe["id"],
            "title": recipe["title"],
            "created_at": recipe.get("created_at"),
            "ingredients": ingredients,
            "instructions": instructions
        }
