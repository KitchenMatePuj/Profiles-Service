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


def get_profile_by_keycloak_id(db: Session, keycloak_user_id: str):
    profile = db.query(Profile).filter(Profile.keycloak_user_id == keycloak_user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
    return ProfileTransformer.to_response_model(profile)


def list_profiles(db: Session):
    profiles = db.query(Profile).all()
    return [ProfileTransformer.to_response_model(profile) for profile in profiles]


def update_profile_by_keycloak_id(db: Session, keycloak_user_id: str, profile_data: dict):
    profile = db.query(Profile).filter(Profile.keycloak_user_id == keycloak_user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
    for key, value in profile_data.items():
        if hasattr(profile, key) and value is not None:
            setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return ProfileTransformer.to_response_model(profile)


def delete_profile_by_keycloak_id(db: Session, keycloak_user_id: str):
    profile = db.query(Profile).filter(Profile.keycloak_user_id == keycloak_user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
    db.delete(profile)
    db.commit()
    return {"message": "Profile deleted successfully"}

def get_profile_summary_by_keycloak_id(db: Session, keycloak_user_id: str):
    from src.main.python.models.Profile import Profile

    profile = db.query(Profile).filter(Profile.keycloak_user_id == keycloak_user_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")

    return {
        "keycloak_user_id": profile.keycloak_user_id,
        "saved_recipes": [r.recipe_id for r in profile.saved_recipes],
        "ingredient_allergies": [a.allergy_name for a in profile.ingredient_allergies]
    }

