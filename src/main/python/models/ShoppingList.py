from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship
from src.main.python.models import Base

class ShoppingList(Base):
    __tablename__ = "shopping_list"

    shopping_list_id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profile.profile_id"), nullable=False)
    recipe_name = Column(String(255), nullable=False)
    recipe_photo = Column(String(255), nullable=True)

    # Many-to-one with Profile
    profile = relationship('Profile', back_populates='shopping_lists')

    # One-to-many with Ingredient
    ingredients = relationship(
        'Ingredient',
        back_populates='shopping_list',
        cascade='all, delete-orphan'
    )