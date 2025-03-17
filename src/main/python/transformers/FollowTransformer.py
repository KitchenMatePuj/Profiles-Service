from pydantic import BaseModel
from src.main.python.models.Follow_model import Follow

# Request Model: Define el esquema para recibir datos en el request
class FollowRequest(BaseModel):
    follower_id: int
    followed_id: int

# Response Model: Define el esquema para responder datos
class FollowResponse(BaseModel):
    follower_id: int
    followed_id: int

    class Config:
        orm_mode = True  # Permite convertir desde un objeto SQLAlchemy

class FollowTransformer:
    @staticmethod
    def to_entity(data: FollowRequest) -> Follow:
        """Convierte un modelo Pydantic en una entidad SQLAlchemy"""
        return Follow(follower_id=data.follower_id, followed_id=data.followed_id)

    @staticmethod
    def to_response_model(follow: Follow) -> FollowResponse:
        """Convierte una entidad SQLAlchemy en un modelo de respuesta Pydantic"""
        return FollowResponse(
            follower_id=follow.follower_id,
            followed_id=follow.followed_id
        )
