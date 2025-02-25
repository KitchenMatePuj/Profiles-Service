from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.main.python.models.Profile import Profile


class ProfileResponse(BaseModel):
    profile_id: int
    keycloak_user_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    restricted_foods: Optional[str] = None
    profile_photo: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ProfileTransformer:
    @staticmethod
    def to_entity(data: dict) -> Profile:
        """Convierte un diccionario en una instancia de Profile."""
        return Profile(**data)

    @staticmethod
    def to_response_model(profile: Profile) -> ProfileResponse:
        """Convierte una instancia de Profile (SQLAlchemy) a un modelo Pydantic."""
        return ProfileResponse(
            profile_id=profile.profile_id,
            keycloak_user_id=profile.keycloak_user_id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            email=profile.email,
            phone=profile.phone,
            restricted_foods=profile.restricted_foods,
            profile_photo=profile.profile_photo,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )

