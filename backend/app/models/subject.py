from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class Subject(Base):
    __tablename__ = "subjects"
    __tableargs__ = (
        UniqueConstraint(
            "user_id", "name", name="uq_user_subject_name"
        )
    )
    
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    name = Column(
        String(50),
        nullable=False
    )

    description = Column(String)
    color = Column(String)

    is_default = Column(
        Boolean,
        default=False,
        server_default="false"
    )

    is_deleted = Column(
        Boolean,
        default=False,
        server_default="false"
    )

    owner = relationship("User", back_populates="subjects")
    sessions = relationship("Session", back_populates="subject")