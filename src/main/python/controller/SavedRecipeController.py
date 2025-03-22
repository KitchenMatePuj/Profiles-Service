from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.service.SavedRecipeService import (
    create_new_saved_recipe,
    get_saved_recipe,
    list_saved_recipes,
    modify_saved_recipe,
    remove_saved_recipe
)
from src.main.python.transformers.SavedRecipeTransformer import SavedRecipeRequest, SavedRecipeResponse

router = APIRouter(prefix="/saved_recipes", tags=["Saved Recipe"])

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
