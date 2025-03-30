from sqlalchemy.orm import Session
from src.main.python.models.Profile import Profile

def create_profile(db: Session, profile: Profile) -> Profile:
    """
    Crea un perfil a partir de un objeto Profile y lo guarda en la BD.
    """
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_profile_by_id(db: Session, profile_id: int) -> Profile:
    """Obtiene un perfil por ID."""
    return db.query(Profile).filter(Profile.profile_id == profile_id).first()


def list_all_profiles(db: Session):
    """Lista todos los perfiles en la base de datos."""
    return db.query(Profile).all()


def get_profile_by_username(db: Session, username: str) -> Profile:
    """Obtiene un perfil por nombre de usuario."""
    return db.query(Profile).filter(Profile.keycloak_user_id == username).first()


def update_profile(db: Session, profile: Profile) -> Profile:
    """
    Actualiza un perfil existente en la BD.
    """
    db.commit()
    db.refresh(profile)
    return profile


def delete_profile(db: Session, profile: Profile) -> None:
    """Elimina un perfil de la base de datos."""
    db.delete(profile)
    db.commit()

def get_profiles_by_status(db: Session, status: str):
    return db.query(Profile).filter(Profile.account_status == status).all()

