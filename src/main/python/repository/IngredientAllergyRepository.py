from sqlalchemy.orm import Session
from src.main.python.models.IngredientAllergy import IngredientAllergy

def create_allergy(db: Session, allergy: IngredientAllergy) -> IngredientAllergy:
    db.add(allergy)
    db.commit()
    db.refresh(allergy)
    return allergy

def get_allergy_by_id(db: Session, allergy_id: int) -> IngredientAllergy:
    return db.query(IngredientAllergy).filter(IngredientAllergy.allergy_id == allergy_id).first()

def list_allergies_by_profile(db: Session, profile_id: int):
    return db.query(IngredientAllergy).filter(IngredientAllergy.profile_id == profile_id).all()

def update_allergy(db: Session, allergy: IngredientAllergy) -> IngredientAllergy:
    db.commit()
    db.refresh(allergy)
    return allergy

def delete_allergy(db: Session, allergy: IngredientAllergy) -> None:
    db.delete(allergy)
    db.commit()
