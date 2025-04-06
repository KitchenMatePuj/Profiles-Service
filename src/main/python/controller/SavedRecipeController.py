from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi import Query

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.service.SavedRecipeService import (
    create_new_saved_recipe,
    get_saved_recipe,
    list_saved_recipes,
    modify_saved_recipe,
    remove_saved_recipe, most_saved_recipes
)
from src.main.python.transformers.SavedRecipeTransformer import SavedRecipeRequest, SavedRecipeResponse
from src.main.python.service.SavedRecipeService import get_saved_recipes_by_keycloak_id


router = APIRouter(prefix="/saved_recipes", tags=["Saved Recipe"])

@router.get("/most_saved")
def get_most_saved_recipes(limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    """Returns the most saved recipes by users."""
    return most_saved_recipes(db, limit)
@router.post("/", response_model=SavedRecipeResponse)
def create_saved_recipe_endpoint(data: SavedRecipeRequest, db: Session = Depends(get_db)):
    """Creates a new saved recipe."""
    return create_new_saved_recipe(db, data.dict())

@router.get("/{saved_recipe_id}", response_model=SavedRecipeResponse)
def get_saved_recipe_endpoint(saved_recipe_id: int, db: Session = Depends(get_db)):
    """Retrieves a saved recipe by ID."""
    return get_saved_recipe(db, saved_recipe_id)

@router.get("/", response_model=List[SavedRecipeResponse])
def list_saved_recipes_endpoint(db: Session = Depends(get_db)):
    """Retrieves all saved recipes."""
    return list_saved_recipes(db)

@router.put("/{saved_recipe_id}", response_model=SavedRecipeResponse)
def update_saved_recipe_endpoint(saved_recipe_id: int, data: dict, db: Session = Depends(get_db)):
    """Updates a saved recipe."""
    return modify_saved_recipe(db, saved_recipe_id, data)

@router.delete("/{saved_recipe_id}", status_code=204)
def delete_saved_recipe_endpoint(saved_recipe_id: int, db: Session = Depends(get_db)):
    """Deletes a saved recipe."""
    remove_saved_recipe(db, saved_recipe_id)
    return {}

@router.get("/saved-recipes/keycloak/{keycloak_user_id}")
def get_saved_recipes_by_user(keycloak_user_id: str, db: Session = Depends(get_db)):
    return get_saved_recipes_by_keycloak_id(db, keycloak_user_id)