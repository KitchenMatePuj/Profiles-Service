from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProfileCreateDTO(BaseModel):
    keycloak_user_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    restricted_foods: Optional[str] = None
    profile_photo: Optional[str] = None

    class Config:
        orm_mode = True


class ProfileResponseDTO(BaseModel):
    profile_id: int
    keycloak_user_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    restricted_foods: Optional[str] = None
    profile_photo: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
