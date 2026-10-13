from typing import List, Optional, Dict, Any
from database.config import get_connection
from domain.recipe_ingredient import RecipeIngredient

class RecipeIngredientRepository:
    @staticmethod
    def addIngredientToRecipe(recipe_ingredient: RecipeIngredient) -> None:
        vals = (
            recipe_ingredient.id,
            recipe_ingredient.recipe_id,
            recipe_ingredient.ingredient_id,
            recipe_ingredient.amount
        )
        query = '''
            INSERT INTO recipe_ingredients (id, recipe_id, ingredient_id, amount)
            VALUES (%s, %s, %s, %s)
        '''
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, vals)
            conn.commit()

    @staticmethod
    def getIngredientsByRecipe(recipe_id: str) -> List[Dict[str, Any]]:
        query = '''
            SELECT 
                ri.id AS link_id,
                ri.recipe_id,
                ri.ingredient_id,
                ri.amount,
                i.name,
                i.unit
            FROM recipe_ingredients ri
            JOIN ingredients i ON ri.ingredient_id = i.id
            WHERE ri.recipe_id = %s
            ORDER BY i.name ASC
        '''
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, (recipe_id,))
                return cursor.fetchall()

    @staticmethod
    def removeIngredientFromRecipe(recipe_ingredient_id: str) -> bool:
        query = 'DELETE FROM recipe_ingredients WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (recipe_ingredient_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def updateAmount(recipe_ingredient_id: str, new_amount: Optional[str]) -> bool:
        query = 'UPDATE recipe_ingredients SET amount = %s WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (new_amount, recipe_ingredient_id))
            conn.commit()
            return cursor.rowcount > 0
