from sqlalchemy import Column, Integer, ForeignKey
from src.main.python.models import Base

class SavedRecipe(Base):
    __tablename__ = "saved_recipe"

    saved_recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("profile.profile_id"), nullable=False)
    recipe_id = Column(Integer, nullable=False)
