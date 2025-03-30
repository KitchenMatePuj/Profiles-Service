from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.service.ProfileService import (

    create_profile, get_profile_by_keycloak_id, list_profiles, update_profile_by_keycloak_id,
    delete_profile_by_keycloak_id, get_profile_summary_by_keycloak_id, get_profiles_by_account_status,
    search_profiles_service)
from src.main.python.transformers.ProfileTransformer import ProfileResponse, ProfileCreateRequest, ProfileUpdateRequest, \
    ProfileSearchRequest

router = APIRouter(prefix="/profiles", tags=["Profile"])

@router.post("/", response_model=ProfileResponse)
def create_profile_endpoint(data: ProfileCreateRequest, db: Session = Depends(get_db)):
    return create_profile(db, data.dict())

@router.get("/search", response_model=List[str])
def search_profiles_endpoint(
params: ProfileSearchRequest = Depends(),
    db: Session = Depends(get_db)
):
    return search_profiles_service(db, params.first_name, params.last_name, params.email, params.account_status, params.allergy_name)

@router.get("/{keycloak_user_id}", response_model=ProfileResponse)
def get_profile_by_keycloak(keycloak_user_id: str, db: Session = Depends(get_db)):
    return get_profile_by_keycloak_id(db, keycloak_user_id)

@router.get("/", response_model=List[ProfileResponse])
def list_profiles_endpoint(db: Session = Depends(get_db)):
    """Retrieves all profiles."""
    return list_profiles(db)

@router.put("/{keycloak_user_id}", response_model=ProfileResponse)
def update_profile_by_keycloak(keycloak_user_id: str, data: ProfileUpdateRequest, db: Session = Depends(get_db)):
    return update_profile_by_keycloak_id(db, keycloak_user_id, data.dict())

@router.delete("/{keycloak_user_id}")
def delete_profile_by_keycloak(keycloak_user_id: str, db: Session = Depends(get_db)):
    return delete_profile_by_keycloak_id(db, keycloak_user_id)

@router.get("/summary/{keycloak_user_id}")
def get_profile_summary_by_keycloak_user_id(keycloak_user_id: str, db: Session = Depends(get_db)):
    return get_profile_summary_by_keycloak_id(db, keycloak_user_id)

@router.get("/status/{status}", response_model=List[ProfileResponse])
def get_profiles_by_status_endpoint(status: str, db: Session = Depends(get_db)):
    return get_profiles_by_account_status(db, status)

