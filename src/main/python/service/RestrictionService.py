from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.main.python.models.Restriction import Restriction
from src.main.python.repository.RestrictionRepository import (
    create_restriction,
    get_restriction_by_id,
    list_restrictions_by_profile,
    update_restriction,
    delete_restriction
)
from src.main.python.transformers.RestrictionTransformer import RestrictionResponse

def create_new_restriction(db: Session, restriction_data: dict) -> RestrictionResponse:
    """Creates a new restriction entry."""
    try:
        restriction_entity = Restriction(**restriction_data)
        created_restriction = create_restriction(db, restriction_entity)

        return RestrictionResponse(
            restriction_id=created_restriction.restriction_id,
            profile_id=created_restriction.profile_id,
            restriction_name=created_restriction.restriction_name
        )
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Database integrity error", "details": str(e.__cause__)}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Unexpected error occurred", "details": str(e)}
        )

def get_restriction(db: Session, restriction_id: int) -> RestrictionResponse:
    """Retrieves a restriction by ID."""
    restriction = get_restriction_by_id(db, restriction_id)
    if not restriction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Restriction not found."}
        )
    return RestrictionResponse(
        restriction_id=restriction.restriction_id,
        profile_id=restriction.profile_id,
        restriction_name=restriction.restriction_name
    )

def list_restrictions(db: Session, profile_id: int):
    """Retrieves all restrictions for a given profile."""
    restrictions = list_restrictions_by_profile(db, profile_id)
    return [
        RestrictionResponse(
            restriction_id=r.restriction_id,
            profile_id=r.profile_id,
            restriction_name=r.restriction_name
        ) for r in restrictions
    ]

def modify_restriction(db: Session, restriction_id: int, data: dict) -> RestrictionResponse:
    """Updates a restriction entry."""
    restriction = get_restriction_by_id(db, restriction_id)
    if not restriction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Restriction not found."}
        )
    for key, value in data.items():
        if hasattr(restriction, key) and value is not None:
            setattr(restriction, key, value)
    try:
        updated = update_restriction(db, restriction)
        return RestrictionResponse(
            restriction_id=updated.restriction_id,
            profile_id=updated.profile_id,
            restriction_name=updated.restriction_name
        )
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Database constraint error", "details": str(e.__cause__)}
        )

def remove_restriction(db: Session, restriction_id: int):
    """Deletes a restriction entry."""
    restriction = get_restriction_by_id(db, restriction_id)
    if not restriction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Restriction not found."}
        )
    try:
        delete_restriction(db, restriction)
        return {"message": "Restriction successfully deleted."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "An error occurred while deleting the restriction.", "details": str(e)}
        )
