from sqlalchemy.orm import Session
from src.main.python.models.Restriction import Restriction

def create_restriction(db: Session, restriction: Restriction) -> Restriction:
    """Creates a new restriction entry."""
    db.add(restriction)
    db.commit()
    db.refresh(restriction)
    return restriction

def get_restriction_by_id(db: Session, restriction_id: int) -> Restriction:
    """Retrieves a restriction by its ID."""
    return db.query(Restriction).filter(Restriction.restriction_id == restriction_id).first()

def list_restrictions_by_profile(db: Session, profile_id: int):
    """Retrieves all restrictions associated with a given profile."""
    return db.query(Restriction).filter(Restriction.profile_id == profile_id).all()

def update_restriction(db: Session, restriction: Restriction) -> Restriction:
    """Updates an existing restriction entry."""
    db.commit()
    db.refresh(restriction)
    return restriction

def delete_restriction(db: Session, restriction: Restriction) -> None:
    """Deletes a restriction entry."""
    db.delete(restriction)
    db.commit()
