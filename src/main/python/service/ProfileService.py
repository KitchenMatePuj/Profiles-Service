from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.main.python.models.Profile import Profile
from src.main.python.transformers.ProfileTransformer import ProfileTransformer


def create_profile(db: Session, profile_data: dict):
    existing_profile = db.query(Profile).filter(Profile.keycloak_user_id == profile_data["keycloak_user_id"]).first()

    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile with this keycloak_user_id already exists.")

    profile_entity = ProfileTransformer.to_entity(profile_data)
    db.add(profile_entity)
    db.commit()
    db.refresh(profile_entity)

    return ProfileTransformer.to_response_model(profile_entity)


def get_profile_by_id(db: Session, profile_id: int):
    profile = db.query(Profile).filter(Profile.profile_id == profile_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")

    return ProfileTransformer.to_response_model(profile)


def list_profiles(db: Session):
    profiles = db.query(Profile).all()
    return [ProfileTransformer.to_response_model(profile) for profile in profiles]


def update_profile(db: Session, profile_data: dict, profile_id: int):
    profile = db.query(Profile).filter(Profile.profile_id == profile_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")

    for key, value in profile_data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    return ProfileTransformer.to_response_model(profile)


def delete_profile(db: Session, profile_id: int):
    profile = db.query(Profile).filter(Profile.profile_id == profile_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")

    db.delete(profile)
    db.commit()

    return {"message": "Profile deleted successfully"}
