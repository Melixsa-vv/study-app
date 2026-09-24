from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class SessionVisibility(str, enum.Enum):
    EVERYONE = "everyone"
    FRIENDS = "friends"
    NONE = "none"

class SessionType(str, enum.Enum):
    SOLO = "solo"
    GROUP = "group"

class Session(Base):
    __tablename__ = "sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        server_default="Study Session",
        default="Study Session"
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False
    )

    visibility = Column(
        SQLEnum(SessionVisibility),
        default=SessionVisibility.EVERYONE,
        server_default=SessionVisibility.EVERYONE.value,
        nullable=False
    )

    session_type = Column(
        SQLEnum(SessionType),
        default=SessionType.SOLO,
        server_default=SessionType.SOLO.value,
        nullable=False
    )

    completed = Column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False
    )

    completed_at = Column(
        DateTime(timezone=True)
    )


    owner = relationship("User", back_populates="sessions")
    subject = relationship("Subject", back_populates="sessions")
    


