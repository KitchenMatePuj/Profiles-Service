from sqlalchemy.orm import Session
from src.main.python.models.Ingredient import Ingredient

def create_ingredient(db: Session, ingredient: Ingredient) -> Ingredient:
    """Creates a new ingredient entry."""
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient

def get_ingredient_by_id(db: Session, ingredient_id: int) -> Ingredient:
    """Retrieves an ingredient by its ID."""
    return db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()

def list_ingredients_by_shopping_list(db: Session, shopping_list_id: int):
    """Retrieves all ingredients associated with a given shopping list."""
    return db.query(Ingredient).filter(Ingredient.shopping_list_id == shopping_list_id).all()

def update_ingredient(db: Session, ingredient: Ingredient) -> Ingredient:
    """Updates an existing ingredient entry."""
    db.commit()
    db.refresh(ingredient)
    return ingredient

def delete_ingredient(db: Session, ingredient: Ingredient) -> None:
    """Deletes an ingredient entry."""
    db.delete(ingredient)
    db.commit()