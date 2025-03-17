from sqlalchemy import Column, Integer, String, DateTime
from src.main.python.models import Base

from sqlalchemy.orm import relationship

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

    # One-to-many with Restriction
    restrictions = relationship("Restriction", back_populates="profile", cascade="all, delete")

    # One-to-many with ShoppingList
    shopping_lists = relationship(
        'ShoppingList',
        back_populates='profile',
        cascade='all, delete-orphan'
    )

    # Self many-to-many for Follow
    # "followed" are the people I follow
    followed = relationship(
        'Follow',
        foreign_keys='Follow.follower_id',
        back_populates='follower',
        cascade='all, delete-orphan'
    )
    # "followers" are the people that follow me
    followers = relationship(
        'Follow',
        foreign_keys='Follow.followed_id',
        back_populates='followed',
        cascade='all, delete-orphan'
    )

