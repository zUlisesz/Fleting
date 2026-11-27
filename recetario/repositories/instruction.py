from database import execute, fetch_all
from domain import Instruction


class InstructionRepository:
    def create(self, instruction: Instruction) -> None:
        execute(
            "INSERT INTO recipe_instructions (id, recipe_id, step_number, instruction) "
            "VALUES (%s, %s, %s, %s)",
            (
                instruction.id,
                instruction.recipe_id,
                instruction.step_number,
                instruction.instruction,
            ),
        )

    def list_for_recipe(self, recipe_id: str) -> list[Instruction]:
        rows = fetch_all(
            "SELECT id, recipe_id, step_number, instruction FROM recipe_instructions "
            "WHERE recipe_id = %s ORDER BY step_number ASC",
            (recipe_id,),
        )
        return [Instruction(**row) for row in rows]

    def delete(self, instruction_id: str) -> bool:
        return execute("DELETE FROM recipe_instructions WHERE id = %s", (instruction_id,)) > 0
