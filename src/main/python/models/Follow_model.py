from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from src.main.python.models import Base

class Follow(Base):
    __tablename__ = "follow"

    follower_id = Column(Integer, ForeignKey("profile.profile_id"), primary_key=True)
    followed_id = Column(Integer, ForeignKey("profile.profile_id"), primary_key=True)
    __table_args__ = (
        PrimaryKeyConstraint("follower_id", "followed_id"),
    )

    follower = relationship("Profile", foreign_keys=[follower_id], back_populates="followed")
    followed = relationship("Profile", foreign_keys=[followed_id], back_populates="followers")
