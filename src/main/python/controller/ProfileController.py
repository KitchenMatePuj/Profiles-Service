from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.service.ProfileService import (
    create_profile,
    get_profile_by_id,
    list_profiles,
    update_profile,
    delete_profile
)
from src.main.python.transformers.ProfileTransformer import ProfileResponse

router = APIRouter(prefix="/profiles", tags=["Profile"])

@router.post("/", response_model=ProfileResponse)
def create_profile_endpoint(data: dict, db: Session = Depends(get_db)):
    return create_profile(db, data)

@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile_endpoint(profile_id: int, db: Session = Depends(get_db)):
    """Retrieves a profile by ID."""
    profile = get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
    return profile

@router.get("/", response_model=List[ProfileResponse])
def list_profiles_endpoint(db: Session = Depends(get_db)):
    """Retrieves all profiles."""
    return list_profiles(db)

@router.put("/{profile_id}", response_model=ProfileResponse)
def update_profile_endpoint(profile_id: int, data: dict, db: Session = Depends(get_db)):
    """Updates a profile entry."""
    return update_profile(db, profile_id, data)

@router.delete("/{profile_id}", status_code=204)
def delete_profile_endpoint(profile_id: int, db: Session = Depends(get_db)):
    """Deletes a profile entry."""
    delete_profile(db, profile_id)
    return {}
