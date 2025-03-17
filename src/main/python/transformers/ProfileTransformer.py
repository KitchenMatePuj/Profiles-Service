from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.main.python.models.Profile import Profile


class ProfileResponse(BaseModel):
    profile_id: int
    keycloak_user_id: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    phone: Optional[str]
    profile_photo: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    account_status: Optional[str]
    cooking_time: Optional[int]


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
            profile_photo=profile.profile_photo,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
            account_status=profile.account_status,
            cooking_time=profile.cooking_time
        )
