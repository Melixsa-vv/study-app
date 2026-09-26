from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_deleted = Column(Boolean, server_default="false", default=False)

    subjects = relationship("Subject", back_populates="owner", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="owner")