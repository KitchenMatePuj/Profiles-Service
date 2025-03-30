from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.main.python.models.savedRecipe import SavedRecipe
from src.main.python.repository.SavedRecipeRepository import (
    create_saved_recipe,
    get_saved_recipe_by_id,
    list_all_saved_recipes,
    update_saved_recipe,
    delete_saved_recipe, get_most_saved_recipes
)
from src.main.python.transformers.SavedRecipeTransformer import SavedRecipeResponse


def create_new_saved_recipe(db: Session, recipe_data: dict) -> SavedRecipeResponse:
    """Creates a new saved recipe entry."""
    try:
        saved_recipe_entity = SavedRecipe(**recipe_data)
        created = create_saved_recipe(db, saved_recipe_entity)

        return SavedRecipeResponse(
            saved_recipe_id=created.saved_recipe_id,
            profile_id=created.profile_id,
            recipe_id=created.recipe_id
        )
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Database integrity error", "details": str(e.__cause__)}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Unexpected error occurred", "details": str(e)}
        )


def get_saved_recipe(db: Session, saved_recipe_id: int) -> SavedRecipeResponse:
    """Retrieves a saved recipe by ID."""
    recipe = get_saved_recipe_by_id(db, saved_recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved recipe not found."
        )
    return SavedRecipeResponse(
        saved_recipe_id=recipe.saved_recipe_id,
        profile_id=recipe.profile_id,
        recipe_id=recipe.recipe_id
    )


def list_saved_recipes(db: Session):
    """Retrieves all saved recipes."""
    recipes = list_all_saved_recipes(db)
    return [
        SavedRecipeResponse(
            saved_recipe_id=r.saved_recipe_id,
            profile_id=r.profile_id,
            recipe_id=r.recipe_id
        ) for r in recipes
    ]


def modify_saved_recipe(db: Session, saved_recipe_id: int, data: dict) -> SavedRecipeResponse:
    """Updates a saved recipe entry."""
    recipe = get_saved_recipe_by_id(db, saved_recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved recipe not found."
        )

    for key, value in data.items():
        if hasattr(recipe, key) and value is not None:
            setattr(recipe, key, value)

    try:
        updated = update_saved_recipe(db, recipe)
        return SavedRecipeResponse(
            saved_recipe_id=updated.saved_recipe_id,
            profile_id=updated.profile_id,
            recipe_id=updated.recipe_id
        )
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Database constraint error", "details": str(e.__cause__)}
        )


def remove_saved_recipe(db: Session, saved_recipe_id: int):
    """Deletes a saved recipe entry."""
    recipe = get_saved_recipe_by_id(db, saved_recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved recipe not found."
        )

    try:
        delete_saved_recipe(db, recipe)
        return {"message": "Saved recipe successfully deleted."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "An error occurred while deleting the saved recipe.", "details": str(e)}
        )


def most_saved_recipes(db: Session, limit: int = 10):
    results = get_most_saved_recipes(db, limit)
    return [{"recipe_id": recipe_id, "count": count} for recipe_id, count in results]
