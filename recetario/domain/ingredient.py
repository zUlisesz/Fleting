from pydantic import BaseModel


class Ingredient(BaseModel):
    """Ingrediente del catálogo (se reutiliza entre recetas)."""

    id: str
    name: str
    unit: str | None = None
