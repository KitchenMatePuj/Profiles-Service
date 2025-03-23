from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.service.IngredientAllergyService import (
    create_new_allergy,
    get_allergy,
    list_allergies,
    modify_allergy,
    remove_allergy
)
from src.main.python.transformers.IngredientAllergyTransformer import IngredientAllergyResponse

router = APIRouter(prefix="/ingredient_allergies", tags=["Ingredient Allergy"])

@router.post("/", response_model=IngredientAllergyResponse)
def create_allergy_endpoint(data: dict, db: Session = Depends(get_db)):
    return create_new_allergy(db, data)

@router.get("/{allergy_id}", response_model=IngredientAllergyResponse)
def get_allergy_endpoint(allergy_id: int, db: Session = Depends(get_db)):
    return get_allergy(db, allergy_id)

@router.get("/profile/{profile_id}", response_model=List[IngredientAllergyResponse])
def list_allergies_endpoint(profile_id: int, db: Session = Depends(get_db)):
    return list_allergies(db, profile_id)

@router.put("/{allergy_id}", response_model=IngredientAllergyResponse)
def update_allergy_endpoint(allergy_id: int, data: dict, db: Session = Depends(get_db)):
    return modify_allergy(db, allergy_id, data)

@router.delete("/{allergy_id}", status_code=204)
def delete_allergy_endpoint(allergy_id: int, db: Session = Depends(get_db)):
    remove_allergy(db, allergy_id)
    return {}
