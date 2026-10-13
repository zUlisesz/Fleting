from pydantic import BaseModel

class Instruction(BaseModel):
    id: str
    recipe_id: str
    step_number: int
    instruction: str