from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.main.python.models.ShoppingList import ShoppingList
from src.main.python.repository.ShoppingListRepository import (
    create_shopping_list,
    get_shopping_list_by_id,
    list_shopping_lists_by_profile,
    update_shopping_list,
    delete_shopping_list
)
from src.main.python.transformers.ShoppingListTransformer import ShoppingListResponse

def create_new_shopping_list(db: Session, shopping_list_data: dict) -> ShoppingListResponse:
    """Creates a new shopping list entry."""
    try:
        shopping_list_entity = ShoppingList(**shopping_list_data)
        created_shopping_list = create_shopping_list(db, shopping_list_entity)

        return ShoppingListResponse(
            shopping_list_id=created_shopping_list.shopping_list_id,
            profile_id=created_shopping_list.profile_id,
            recipe_name=created_shopping_list.recipe_name,
            recipe_photo=created_shopping_list.recipe_photo
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

def get_shopping_list(db: Session, shopping_list_id: int) -> ShoppingListResponse:
    """Retrieves a shopping list by ID."""
    shopping_list = get_shopping_list_by_id(db, shopping_list_id)
    if not shopping_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Shopping list not found."}
        )
    return ShoppingListResponse(
        shopping_list_id=shopping_list.shopping_list_id,
        profile_id=shopping_list.profile_id,
        recipe_name=shopping_list.recipe_name,
        recipe_photo=shopping_list.recipe_photo
    )

def list_shopping_lists(db: Session, profile_id: int):
    """Retrieves all shopping lists for a given profile."""
    shopping_lists = list_shopping_lists_by_profile(db, profile_id)
    return [
        ShoppingListResponse(
            shopping_list_id=s.shopping_list_id,
            profile_id=s.profile_id,
            recipe_name=s.recipe_name,
            recipe_photo=s.recipe_photo
        ) for s in shopping_lists
    ]

def modify_shopping_list(db: Session, shopping_list_id: int, data: dict) -> ShoppingListResponse:
    """Updates a shopping list entry."""
    shopping_list = get_shopping_list_by_id(db, shopping_list_id)
    if not shopping_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Shopping list not found."}
        )
    for key, value in data.items():
        if hasattr(shopping_list, key) and value is not None:
            setattr(shopping_list, key, value)
    try:
        updated = update_shopping_list(db, shopping_list)
        return ShoppingListResponse(
            shopping_list_id=updated.shopping_list_id,
            profile_id=updated.profile_id,
            recipe_name=updated.recipe_name,
            recipe_photo=updated.recipe_photo
        )
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Database constraint error", "details": str(e.__cause__)}
        )

def remove_shopping_list(db: Session, shopping_list_id: int):
    """Deletes a shopping list entry."""
    shopping_list = get_shopping_list_by_id(db, shopping_list_id)
    if not shopping_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Shopping list not found."}
        )
    try:
        delete_shopping_list(db, shopping_list)
        return {"message": "Shopping list successfully deleted."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "An error occurred while deleting the shopping list.", "details": str(e)}
        )
