from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.main.python.models.Ingredient import Ingredient
from src.main.python.repository.IngredientRepository import (
    create_ingredient,
    get_ingredient_by_id,
    list_ingredients_by_shopping_list,
    update_ingredient,
    delete_ingredient
)
from src.main.python.transformers.IngredientTransformer import IngredientResponse

def create_new_ingredient(db: Session, ingredient_data: dict) -> IngredientResponse:
    """Creates a new ingredient entry."""
    try:
        ingredient_entity = Ingredient(**ingredient_data)
        created_ingredient = create_ingredient(db, ingredient_entity)

        return IngredientResponse(
            ingredient_id=created_ingredient.ingredient_id,
            shopping_list_id=created_ingredient.shopping_list_id,
            ingredient_name=created_ingredient.ingredient_name,
            measurement_unit=created_ingredient.measurement_unit
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

def get_ingredient(db: Session, ingredient_id: int) -> IngredientResponse:
    """Retrieves an ingredient by ID."""
    ingredient = get_ingredient_by_id(db, ingredient_id)
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ingredient not found."}
        )
    return IngredientResponse(
        ingredient_id=ingredient.ingredient_id,
        shopping_list_id=ingredient.shopping_list_id,
        ingredient_name=ingredient.ingredient_name,
        measurement_unit=ingredient.measurement_unit
    )

def list_ingredients(db: Session, shopping_list_id: int):
    """Retrieves all ingredients for a given shopping list."""
    ingredients = list_ingredients_by_shopping_list(db, shopping_list_id)
    return [
        IngredientResponse(
            ingredient_id=i.ingredient_id,
            shopping_list_id=i.shopping_list_id,
            ingredient_name=i.ingredient_name,
            measurement_unit=i.measurement_unit,
        ) for i in ingredients
    ]

def modify_ingredient(db: Session, ingredient_id: int, data: dict) -> IngredientResponse:
    """Updates an ingredient entry."""
    ingredient = get_ingredient_by_id(db, ingredient_id)
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ingredient not found."}
        )
    for key, value in data.items():
        if hasattr(ingredient, key) and value is not None:
            setattr(ingredient, key, value)
    try:
        updated = update_ingredient(db, ingredient)
        return IngredientResponse(
            ingredient_id=updated.ingredient_id,
            shopping_list_id=updated.shopping_list_id,
            ingredient_name=updated.ingredient_name,
            measurement_unit=updated.measurement_unit,
        )
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Database constraint error", "details": str(e.__cause__)}
        )

def remove_ingredient(db: Session, ingredient_id: int):
    """Deletes an ingredient entry."""
    ingredient = get_ingredient_by_id(db, ingredient_id)
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ingredient not found."}
        )
    try:
        delete_ingredient(db, ingredient)
        return {"message": "Ingredient successfully deleted."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "An error occurred while deleting the ingredient.", "details": str(e)}
        )
