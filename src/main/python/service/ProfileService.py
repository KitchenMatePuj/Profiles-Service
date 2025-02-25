from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.main.python.transformers.ProfileTransformer import (
    ProfileTransformer,
    ProfileResponse
)
from src.main.python.repository.ProfileRepository import (
    create_profile,
    get_profile_by_username,
    get_profile_by_id,
    update_profile,
    delete_profile,
    list_all_profiles
)
from src.main.python.models.Profile import Profile


def create_new_profile(db: Session, profile_data: dict) -> ProfileResponse:
    """Creates a new profile, ensuring uniqueness and handling exceptions."""
    try:
        existing_profile = get_profile_by_username(db, profile_data.get("keycloak_user_id"))
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "A profile with this keycloak_user_id already exists"}
            )


        profile_entity = Profile(**profile_data)
        created_profile = create_profile(db, profile_entity)

        return ProfileTransformer.to_response_model(created_profile)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "A profile with this keycloak_user_id already exists",
                "details": str(e.__cause__)
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "An unexpected error occurred", "details": str(e)}
        )


def get_profile(db: Session, profile_id: int) -> ProfileResponse:
    """Retrieves a profile by ID, ensuring proper exception handling."""
    try:
        profile = get_profile_by_id(db, profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Profile not found"}
            )
        return ProfileTransformer.to_response_model(profile)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "An error occurred while retrieving the profile", "details": str(e)}
        )


def list_profiles(db: Session) -> List[ProfileResponse]:
    """Lists all profiles, ensuring valid responses."""
    try:
        profiles = list_all_profiles(db)
        return [ProfileTransformer.to_response_model(profile) for profile in profiles]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "An error occurred while fetching profiles", "details": str(e)}
        )


def modify_profile(db: Session, profile_id: int, data: dict) -> ProfileResponse:
    """Updates a profile with new data, ensuring data validity."""
    try:
        profile = get_profile_by_id(db, profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Profile not found"}
            )

        for key, value in data.items():
            if value is not None:
                setattr(profile, key, value)

        updated_profile = update_profile(db, profile)

        return ProfileTransformer.to_response_model(updated_profile)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Database constraint error",
                "details": str(e.__cause__)
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "An error occurred while updating the profile",
                "details": str(e)
            }
        )


def remove_profile(db: Session, profile_id: int) -> dict:
    """Deletes a profile, ensuring proper exception handling."""
    try:
        profile = get_profile_by_id(db, profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Profile not found"}
            )
        delete_profile(db, profile)
        return {"message": "Profile successfully deleted"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "An error occurred while deleting the profile", "details": str(e)}
        )
