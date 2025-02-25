from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from src.main.python.config.DatabasesConfig import get_db
from src.main.python.service.ProfileService import (
    create_new_profile,
    get_profile,
    modify_profile,
    remove_profile,
    list_profiles
)

from src.main.python.transformers.ProfileTransformer import ProfileResponse

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/", response_model=ProfileResponse)
def create_profile(profile_data: dict, db: Session = Depends(get_db)):
    return create_new_profile(db, profile_data)

@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile_endpoint(profile_id: int, db: Session = Depends(get_db)):
    return get_profile(db, profile_id)

@router.get("/", response_model=List[ProfileResponse])
def list_all_profiles(db: Session = Depends(get_db)):
    return list_profiles(db)

@router.put("/{profile_id}", response_model=ProfileResponse)
def update_profile(profile_id: int, profile_data: dict, db: Session = Depends(get_db)):
    return modify_profile(db, profile_id, profile_data)

@router.delete("/{profile_id}", status_code=204)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    remove_profile(db, profile_id)
