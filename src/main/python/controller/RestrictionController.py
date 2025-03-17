from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.service.RestrictionService import (
    create_new_restriction,
    get_restriction,
    list_restrictions,
    modify_restriction,
    remove_restriction
)
from src.main.python.transformers.RestrictionTransformer import RestrictionResponse

router = APIRouter(prefix="/restrictions", tags=["Restriction"])

@router.post("/", response_model=RestrictionResponse)
def create_restriction_endpoint(data: dict, db: Session = Depends(get_db)):
    """Creates a new restriction entry."""
    return create_new_restriction(db, data)

@router.get("/{restriction_id}", response_model=RestrictionResponse)
def get_restriction_endpoint(restriction_id: int, db: Session = Depends(get_db)):
    """Retrieves a restriction by ID."""
    restriction = get_restriction(db, restriction_id)
    if not restriction:
        raise HTTPException(status_code=404, detail="Restriction not found.")
    return restriction

@router.get("/profile/{profile_id}", response_model=List[RestrictionResponse])
def list_restrictions_endpoint(profile_id: int, db: Session = Depends(get_db)):
    """Retrieves all restrictions for a given profile."""
    return list_restrictions(db, profile_id)

@router.put("/{restriction_id}", response_model=RestrictionResponse)
def update_restriction_endpoint(restriction_id: int, data: dict, db: Session = Depends(get_db)):
    """Updates a restriction entry."""
    return modify_restriction(db, restriction_id, data)

@router.delete("/{restriction_id}", status_code=204)
def delete_restriction_endpoint(restriction_id: int, db: Session = Depends(get_db)):
    """Deletes a restriction entry."""
    remove_restriction(db, restriction_id)
    return {}