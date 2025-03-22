from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.main.python.models.IngredientAllergy import IngredientAllergy
from src.main.python.repository.IngredientAllergyRepository import (
    create_allergy,
    get_allergy_by_id,
    list_allergies_by_profile,
    update_allergy,
    delete_allergy
)
from src.main.python.transformers.IngredientAllergyTransformer import IngredientAllergyResponse

def create_new_allergy(db: Session, allergy_data: dict) -> IngredientAllergyResponse:
    try:
        allergy_entity = IngredientAllergy(**allergy_data)
        created = create_allergy(db, allergy_entity)
        return IngredientAllergyResponse(**created.__dict__)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__cause__))

def get_allergy(db: Session, allergy_id: int) -> IngredientAllergyResponse:
    allergy = get_allergy_by_id(db, allergy_id)
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found.")
    return IngredientAllergyResponse(**allergy.__dict__)

def list_allergies(db: Session, profile_id: int):
    allergies = list_allergies_by_profile(db, profile_id)
    return [IngredientAllergyResponse(**a.__dict__) for a in allergies]

def modify_allergy(db: Session, allergy_id: int, data: dict) -> IngredientAllergyResponse:
    allergy = get_allergy_by_id(db, allergy_id)
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found.")
    for key, value in data.items():
        if hasattr(allergy, key) and value is not None:
            setattr(allergy, key, value)
    updated = update_allergy(db, allergy)
    return IngredientAllergyResponse(**updated.__dict__)

def remove_allergy(db: Session, allergy_id: int):
    allergy = get_allergy_by_id(db, allergy_id)
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found.")
    delete_allergy(db, allergy)
    return {"message": "Allergy successfully deleted."}
