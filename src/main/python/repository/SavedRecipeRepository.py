from sqlalchemy import func
from sqlalchemy.orm import Session
from src.main.python.models.savedRecipe import SavedRecipe

def create_saved_recipe(db: Session, saved_recipe: SavedRecipe) -> SavedRecipe:
    """Creates a new saved recipe entry."""
    db.add(saved_recipe)
    db.commit()
    db.refresh(saved_recipe)
    return saved_recipe

def get_saved_recipe_by_id(db: Session, saved_recipe_id: int) -> SavedRecipe:
    """Retrieves a saved recipe by its ID."""
    return db.query(SavedRecipe).filter(SavedRecipe.saved_recipe_id == saved_recipe_id).first()

def list_all_saved_recipes(db: Session):
    """Retrieves all saved recipes."""
    return db.query(SavedRecipe).all()

def update_saved_recipe(db: Session, saved_recipe: SavedRecipe) -> SavedRecipe:
    """Updates an existing saved recipe entry."""
    db.commit()
    db.refresh(saved_recipe)
    return saved_recipe

def delete_saved_recipe(db: Session, saved_recipe: SavedRecipe) -> None:
    """Deletes a saved recipe entry."""
    db.delete(saved_recipe)
    db.commit()

def get_most_saved_recipes(db: Session, limit: int = 10):
    return (
        db.query(SavedRecipe.recipe_id, func.count(SavedRecipe.recipe_id).label("count"))
        .group_by(SavedRecipe.recipe_id)
        .order_by(func.count(SavedRecipe.recipe_id).desc())
        .limit(limit)
        .all()
    )

