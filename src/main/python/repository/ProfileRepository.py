from sqlalchemy.orm import Session

from src.main.python.dto.ProfileDto import ProfileCreateDTO
from src.main.python.models.Profile import Profile

def create_profile(db: Session, profile_data: ProfileCreateDTO) -> Profile:
    new_profile = Profile(**profile_data.dict())
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

def get_profile_by_id(db: Session, profile_id: int) -> Profile:
    return db.query(Profile).filter(Profile.profile_id == profile_id).first()

def list_all_profiles(db: Session):
    return db.query(Profile).all()

def get_profile_by_username(db: Session, username: str) -> Profile:
    return db.query(Profile).filter(Profile.username == username).first()

def update_profile(db: Session, profile_id: int, profile_data: ProfileCreateDTO) -> Profile:

    profile = db.query(Profile).filter(Profile.profile_id == profile_id).first()
    update_data = profile_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile

def delete_profile(db: Session, profile: Profile) -> None:
    db.delete(profile)
    db.commit()
