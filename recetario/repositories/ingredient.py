from typing import List, Optional, Dict, Any
from database.config import get_connection
from domain.ingredient import Ingredient

class IngredientRepository:
    @staticmethod
    def readData():
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = 'SELECT id, name, unit FROM ingredients ORDER BY name ASC'
                cursor.execute(query)
                return cursor.fetchall()

    @staticmethod
    def getById(ingredient_id: str):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = 'SELECT id, name, unit FROM ingredients WHERE id = %s'
                cursor.execute(query, (ingredient_id,))
                return cursor.fetchone()

    @staticmethod
    def getByName(name: str) :
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = 'SELECT id, name, unit FROM ingredients WHERE LOWER(name) = LOWER(%s)'
                cursor.execute(query, (name,))
                return cursor.fetchone()

    @staticmethod
    def createIngredient(ingredient: Ingredient) -> None:
        vals = (ingredient.id, ingredient.name, ingredient.unit)
        query = 'INSERT INTO ingredients (id, name, unit) VALUES (%s, %s, %s)'
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, vals)
            conn.commit()

    @staticmethod
    def updateIngredient(ingredient_id: str, name: str, unit: Optional[str] = None) -> bool:
        query = 'UPDATE ingredients SET name = %s, unit = %s WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (name, unit, ingredient_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def deleteIngrediente(id: str) -> bool:
        query = 'DELETE FROM ingredients WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (id,))
            conn.commit()
            return cursor.rowcount > 0
