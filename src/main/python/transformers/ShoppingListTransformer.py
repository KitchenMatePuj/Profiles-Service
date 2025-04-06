from pydantic import BaseModel
from typing import Optional

class ShoppingListRequest(BaseModel):
    """Pydantic model for Shopping List creation and update requests."""
    profile_id: int
    recipe_name: str
    recipe_photo: Optional[str] = None

class ShoppingListResponse(BaseModel):
    """Pydantic model for Shopping List response."""
    shopping_list_id: int
    profile_id: int
    recipe_name: str
    recipe_photo: Optional[str]

    class Config:
        orm_mode = True
