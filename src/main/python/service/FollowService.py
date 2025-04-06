from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.main.python.repository.ProfileRepository import get_profile_by_id
import logging

logging.basicConfig(level=logging.DEBUG)

from src.main.python.repository.FollowRepository import (
    create_follow,
    get_follow,
    list_followers,
    list_followed,
    delete_follow
)
from src.main.python.transformers.FollowTransformer import (
    FollowTransformer,
    FollowRequest,
    FollowResponse
)

def create_new_follow(db: Session, follow_data: FollowRequest) -> FollowResponse:
    """
    Creates a new follow relationship between two profiles.
    :param db: Database session
    :param follow_data: Pydantic model (FollowRequest) containing follower_id and followed_id
    :return: Pydantic model (FollowResponse) representing the created follow relationship
    """
    try:
        if follow_data.follower_id == follow_data.followed_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A profile cannot follow itself."
            )

        existing_follow = get_follow(db, follow_data.follower_id, follow_data.followed_id)
        if existing_follow:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This follow relationship already exists."
            )

        follow_entity = FollowTransformer.to_entity(follow_data)
        created_follow = create_follow(db, follow_entity)

        return FollowTransformer.to_response_model(created_follow)

    except IntegrityError as e:
        db.rollback()
        logging.error(f"[create_new_follow] IntegrityError: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database integrity error: {str(e.__cause__)}"
        )
    except Exception as e:
        db.rollback()
        logging.error(f"[create_new_follow] Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred"
        )

def list_profile_followers(db: Session, profile_id: int):
    followers = list_followers(db, profile_id)
    return [FollowTransformer.to_response_model(f) for f in followers]

def list_profile_followed(db: Session, profile_id: int):
    followed = list_followed(db, profile_id)
    return [FollowTransformer.to_response_model(f) for f in followed]

def remove_follow(db: Session, follower_id: int, followed_id: int):
    follow = get_follow(db, follower_id, followed_id)
    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Follow relationship not found."
        )
    try:
        delete_follow(db, follow)
        return {"message": "Follow relationship successfully deleted."}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the follow relationship."
        )

def get_followed_keycloak_ids(db: Session, profile_id: int) -> list[str]:
    followed = list_followed(db, profile_id)
    keycloak_ids = []
    for follow in followed:
        profile = get_profile_by_id(db, follow.followed_id)
        if profile:
            keycloak_ids.append(profile.keycloak_user_id)
    return keycloak_ids
