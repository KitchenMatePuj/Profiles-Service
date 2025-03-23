from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.main.python.models import Base

class IngredientAllergy(Base):
    __tablename__ = "ingredient_allergy"

    allergy_id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("profile.profile_id", ondelete="CASCADE"), nullable=False)
    allergy_name = Column(String(255), nullable=False)

    profile = relationship("Profile", back_populates="ingredient_allergies")
