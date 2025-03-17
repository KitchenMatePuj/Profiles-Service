from pydantic import BaseModel

class RestrictionResponse(BaseModel):
    """Pydantic model for Restriction response."""
    restriction_id: int
    profile_id: int
    restriction_name: str

    class Config:
        orm_mode = True