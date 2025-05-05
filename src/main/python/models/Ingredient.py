from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from src.main.python.models import Base

class Ingredient(Base):
    __tablename__ = "ingredient"

    ingredient_id = Column(Integer, primary_key=True, index=True)
    shopping_list_id = Column(Integer, ForeignKey("shopping_list.shopping_list_id", ondelete="CASCADE"), nullable=False)
    ingredient_name = Column(String(255), nullable=False)
    measurement_unit = Column(String(50), nullable=False)

    # Many-to-one with ShoppingList
    shopping_list = relationship('ShoppingList', back_populates='ingredients')