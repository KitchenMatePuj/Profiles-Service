from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship
from src.main.python.models import Base


class Restriction(Base):
    __tablename__ = "restriction"

    restriction_id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("profile.profile_id", ondelete="CASCADE"), nullable=False)
    restriction_name = Column(String(255), nullable=False)

    # Many-to-one with Profile
    profile = relationship('Profile', back_populates='restrictions')