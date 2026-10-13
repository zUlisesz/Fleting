from typing import List, Dict, Any
from database.config import get_connection
from domain.instruction import Instruction

class IntructionRepository:
    @staticmethod
    def createInstruction(instruction: Instruction) -> None:
        vals = (
            instruction.id,
            instruction.recipe_id,
            instruction.step_number,
            instruction.instruction
        )
        query = '''
            INSERT INTO recipe_instructions (id, recipe_id, step_number, instruction)
            VALUES (%s, %s, %s, %s)
        '''
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, vals)
            conn.commit()

    @staticmethod
    def readInstructions(id_recipe: str) :
        query = '''
            SELECT id, recipe_id, step_number, instruction 
            FROM recipe_instructions 
            WHERE recipe_id = %s 
            ORDER BY step_number ASC
        '''
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, (id_recipe,))
                return cursor.fetchall()

    @staticmethod
    def updateInstruction(instruction_id: str, step_number: int, instruction: str) -> bool:
        query = '''
            UPDATE recipe_instructions 
            SET step_number = %s, instruction = %s 
            WHERE id = %s
        '''
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (step_number, instruction, instruction_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def deleteInstruction(instruction_id: str) -> bool:
        query = 'DELETE FROM recipe_instructions WHERE id = %s'
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (instruction_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def deleteByRecipeId(recipe_id: str) -> int:
        query = 'DELETE FROM recipe_instructions WHERE recipe_id = %s'
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (recipe_id,))
            conn.commit()
            return cursor.rowcount
