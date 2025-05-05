from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.main.python.models import Base

class Profile(Base):
    __tablename__ = "profile"

    profile_id = Column(Integer, primary_key=True, autoincrement=True)
    keycloak_user_id = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(100))
    profile_photo = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    account_status = Column(String(50))
    cooking_time = Column(Integer)
    description = Column(String(255))

    ingredient_allergies = relationship("IngredientAllergy", back_populates="profile", cascade="all, delete")

    shopping_lists = relationship(
        'ShoppingList',
        back_populates='profile',
        cascade='all, delete-orphan'
    )

    followed = relationship(
        'Follow',
        foreign_keys='Follow.follower_id',
        back_populates='follower',
        cascade='all, delete-orphan'
    )
    followers = relationship(
        'Follow',
        foreign_keys='Follow.followed_id',
        back_populates='followed',
        cascade='all, delete-orphan'
    )

    saved_recipes = relationship(
        'SavedRecipe',
        cascade='all, delete-orphan'
    )
