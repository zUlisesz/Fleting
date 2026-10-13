from typing import Optional
from pydantic import BaseModel

class Ingredient(BaseModel):
    id: str
    name: str 
    unit: Optional[str] = None
