from pydantic import BaseModel


class Instruction(BaseModel):
    """Paso de preparación de una receta."""

    id: str
    recipe_id: str
    step_number: int
    instruction: str
