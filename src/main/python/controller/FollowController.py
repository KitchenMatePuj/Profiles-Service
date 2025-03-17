from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.service.FollowService import (
    create_new_follow,
    list_profile_followers,
    list_profile_followed,
    remove_follow
)
from src.main.python.transformers.FollowTransformer import FollowResponse, FollowRequest

router = APIRouter(prefix="/follows", tags=["Follow"])

@router.post("/", response_model=FollowResponse)
def create_follow_endpoint(follow_data: FollowRequest, db: Session = Depends(get_db)):
    return create_new_follow(db, follow_data)

@router.get("/followers/{profile_id}", response_model=List[FollowResponse])
def list_followers_endpoint(profile_id: int, db: Session = Depends(get_db)):
    """Retrieves the list of followers for a given profile."""
    return list_profile_followers(db, profile_id)

@router.get("/followed/{profile_id}", response_model=List[FollowResponse])
def list_followed_endpoint(profile_id: int, db: Session = Depends(get_db)):
    """Retrieves the list of profiles a given profile is following."""
    return list_profile_followed(db, profile_id)

@router.delete("/", status_code=204)
def delete_follow_endpoint(follower_id: int, followed_id: int, db: Session = Depends(get_db)):
    """Deletes a follow relationship."""
    remove_follow(db, follower_id, followed_id)
    return {}
