from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.main.python.dto.ProfileDto import ProfileCreateDTO
from src.main.python.repository.ProfileRepository import (
    create_profile,
    get_profile_by_username,
    get_profile_by_id,
    update_profile,
    delete_profile, list_all_profiles,
)
from src.main.python.models.Profile import Profile

def create_new_profile(db: Session, profile_data: ProfileCreateDTO) -> Profile:
    existing = get_profile_by_username(db, profile_data.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    profile = create_profile(db, profile_data)
    return profile


def get_profile(db: Session, profile_id: int) -> Profile:
    profile = get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile

def list_profiles(db: Session) -> List[Profile]:
    profiles = list_all_profiles(db)
    return profiles

def modify_profile(db: Session, profile_id: int, data: dict) -> Profile:
    profile = get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return update_profile(db, profile, data)

def remove_profile(db: Session, profile_id: int) -> None:
    profile = get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    delete_profile(db, profile)
