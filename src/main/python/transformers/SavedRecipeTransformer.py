from pydantic import BaseModel
from src.main.python.models.savedRecipe import SavedRecipe

# Response model
class SavedRecipeResponse(BaseModel):
    saved_recipe_id: int
    profile_id: int
    recipe_id: int

    class Config:
        orm_mode = True


# Request model
class SavedRecipeRequest(BaseModel):
    profile_id: int
    recipe_id: int


# Transformer class
class SavedRecipeTransformer:
    @staticmethod
    def to_entity(data: SavedRecipeRequest) -> SavedRecipe:
        """Converts a Pydantic request model to a SQLAlchemy entity."""
        return SavedRecipe(
            profile_id=data.profile_id,
            recipe_id=data.recipe_id
        )

    @staticmethod
    def to_response_model(recipe: SavedRecipe) -> SavedRecipeResponse:
        """Converts a SQLAlchemy entity to a Pydantic response model."""
        return SavedRecipeResponse(
            saved_recipe_id=recipe.saved_recipe_id,
            profile_id=recipe.profile_id,
            recipe_id=recipe.recipe_id
        )
