from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.service.IngredientService import (
    create_new_ingredient,
    get_ingredient,
    list_ingredients,
    modify_ingredient,
    remove_ingredient
)
from src.main.python.transformers.IngredientTransformer import IngredientResponse

router = APIRouter(prefix="/ingredients", tags=["Ingredient"])

@router.post("/", response_model=IngredientResponse)
def create_ingredient_endpoint(data: dict, db: Session = Depends(get_db)):
    """Creates a new ingredient entry."""
    return create_new_ingredient(db, data)

@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient_endpoint(ingredient_id: int, db: Session = Depends(get_db)):
    """Retrieves an ingredient by ID."""
    return get_ingredient(db, ingredient_id)

@router.get("/shopping_list/{shopping_list_id}", response_model=List[IngredientResponse])
def list_ingredients_endpoint(shopping_list_id: int, db: Session = Depends(get_db)):
    """Retrieves all ingredients for a given shopping list."""
    return list_ingredients(db, shopping_list_id)

@router.put("/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient_endpoint(ingredient_id: int, data: dict, db: Session = Depends(get_db)):
    """Updates an ingredient entry."""
    return modify_ingredient(db, ingredient_id, data)

@router.delete("/{ingredient_id}", status_code=204)
def delete_ingredient_endpoint(ingredient_id: int, db: Session = Depends(get_db)):
    """Deletes an ingredient entry."""
    remove_ingredient(db, ingredient_id)
    return {}
