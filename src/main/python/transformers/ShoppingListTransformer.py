from pydantic import BaseModel
from typing import Optional

class ShoppingListResponse(BaseModel):
    """Pydantic model for Shopping List response."""
    shopping_list_id: int
    profile_id: int
    recipe_name: str
    recipe_photo: Optional[str]

    class Config:
        orm_mode = True