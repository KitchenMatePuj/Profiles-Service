from sqlalchemy.orm import Session
from src.main.python.models.Follow_model  import Follow

def create_follow(db: Session, follow: Follow) -> Follow:
    """Creates a new follow relationship."""
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow

def get_follow(db: Session, follower_id: int, followed_id: int) -> Follow:
    """Retrieves a follow relationship by follower and followed IDs."""
    return db.query(Follow).filter(
        Follow.follower_id == follower_id,
        Follow.followed_id == followed_id
    ).first()

def list_followers(db: Session, profile_id: int):
    """Retrieves the list of followers for a given profile."""
    return db.query(Follow).filter(Follow.followed_id == profile_id).all()

def list_followed(db: Session, profile_id: int):
    """Retrieves the list of profiles that a given profile is following."""
    return db.query(Follow).filter(Follow.follower_id == profile_id).all()

def delete_follow(db: Session, follow: Follow) -> None:
    """Deletes a follow relationship."""
    db.delete(follow)
    db.commit()
