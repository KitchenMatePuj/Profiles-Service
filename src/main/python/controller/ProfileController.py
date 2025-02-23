from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from src.main.python.config.DatabasesConfig import get_db
from src.main.python.dto.ProfileDto import ProfileCreateDTO, ProfileResponseDTO
from src.main.python.service.ProfileService import (
    create_profile as create_profile_service,
    get_profile as get_profile_service,
    update_profile as update_profile_service,
    remove_profile as remove_profile_service, list_profiles,
)

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/", response_model=ProfileResponseDTO)
def create_profile(profile_data: ProfileCreateDTO, db: Session = Depends(get_db)):
    return create_profile_service(db, profile_data)

@router.get("/{profile_id}", response_model=ProfileResponseDTO)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    return get_profile_service(db, profile_id)

@router.get("/", response_model=List[ProfileResponseDTO])
def list_all_profiles(db: Session = Depends(get_db)):
    return list_profiles(db)

@router.put("/{profile_id}", response_model=ProfileResponseDTO)
def update_profile(profile_id: int, profile_data: ProfileCreateDTO, db: Session = Depends(get_db)):
    return update_profile_service(db, profile_id, profile_data)

@router.delete("/{profile_id}", status_code=204)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    remove_profile_service(db, profile_id)
    return