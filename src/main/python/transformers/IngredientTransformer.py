from pydantic import BaseModel

class IngredientResponse(BaseModel):
    """Pydantic model for Ingredient response."""
    ingredient_id: int
    shopping_list_id: int
    ingredient_name: str
    measurement_unit: str
    quantity: str

    class Config:
        orm_mode = True