from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.service.ShoppingListService import (
    create_new_shopping_list,
    get_shopping_list,
    list_shopping_lists,
    modify_shopping_list,
    remove_shopping_list
)
from src.main.python.transformers.ShoppingListTransformer import ShoppingListResponse

router = APIRouter(prefix="/shopping_lists", tags=["Shopping List"])

@router.post("/", response_model=ShoppingListResponse)
def create_shopping_list_endpoint(data: dict, db: Session = Depends(get_db)):
    """Creates a new shopping list entry."""
    return create_new_shopping_list(db, data)

@router.get("/{shopping_list_id}", response_model=ShoppingListResponse)
def get_shopping_list_endpoint(shopping_list_id: int, db: Session = Depends(get_db)):
    """Retrieves a shopping list by ID."""
    shopping_list = get_shopping_list(db, shopping_list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found.")
    return shopping_list

@router.get("/profile/{profile_id}", response_model=List[ShoppingListResponse])
def list_shopping_lists_endpoint(profile_id: int, db: Session = Depends(get_db)):
    """Retrieves all shopping lists for a given profile."""
    return list_shopping_lists(db, profile_id)

@router.put("/{shopping_list_id}", response_model=ShoppingListResponse)
def update_shopping_list_endpoint(shopping_list_id: int, data: dict, db: Session = Depends(get_db)):
    """Updates a shopping list entry."""
    return modify_shopping_list(db, shopping_list_id, data)

@router.delete("/{shopping_list_id}", status_code=204)
def delete_shopping_list_endpoint(shopping_list_id: int, db: Session = Depends(get_db)):
    """Deletes a shopping list entry."""
    remove_shopping_list(db, shopping_list_id)
    return {}