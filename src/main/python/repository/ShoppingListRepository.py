from sqlalchemy.orm import Session
from src.main.python.models.ShoppingList import ShoppingList

def create_shopping_list(db: Session, shopping_list: ShoppingList) -> ShoppingList:
    """Creates a new shopping list entry."""
    db.add(shopping_list)
    db.commit()
    db.refresh(shopping_list)
    return shopping_list

def get_shopping_list_by_id(db: Session, shopping_list_id: int) -> ShoppingList:
    """Retrieves a shopping list by its ID."""
    return db.query(ShoppingList).filter(ShoppingList.shopping_list_id == shopping_list_id).first()

def list_shopping_lists_by_profile(db: Session, profile_id: int):
    """Retrieves all shopping lists associated with a given profile."""
    return db.query(ShoppingList).filter(ShoppingList.profile_id == profile_id).all()

def update_shopping_list(db: Session, shopping_list: ShoppingList) -> ShoppingList:
    """Updates an existing shopping list entry."""
    db.commit()
    db.refresh(shopping_list)
    return shopping_list

def delete_shopping_list(db: Session, shopping_list: ShoppingList) -> None:
    """Deletes a shopping list entry."""
    db.delete(shopping_list)
    db.commit()
