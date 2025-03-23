from pydantic import BaseModel

class IngredientAllergyResponse(BaseModel):
    allergy_id: int
    profile_id: int
    allergy_name: str

    class Config:
        orm_mode = True
