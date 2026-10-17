from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base, TimestampMixin
import enum

class SessionVisibility(str, enum.Enum):
    EVERYONE = "everyone"
    FRIENDS = "friends"
    NONE = "none"

class SessionType(str, enum.Enum):
    SOLO = "solo"
    GROUP = "group"

class Session(Base, TimestampMixin):
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

    """subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False
    )"""

    visibility = Column(
        SQLEnum(
            SessionVisibility, 
            values_callable=lambda x: [e.value for e in x]
        ),
        default=SessionVisibility.EVERYONE,
        server_default=SessionVisibility.EVERYONE.value,
        nullable=False
    )

    session_type = Column(
        SQLEnum(
            SessionType, 
            values_callable=lambda x: [e.value for e in x]
        ),
        default=SessionType.SOLO,
        server_default=SessionType.SOLO.value,
        nullable=False
    )

    is_completed_flag = Column("is_completed", Boolean, default=False, nullable=False)
    is_cancelled_flag = Column("is_cancelled", Boolean, default=False, nullable=False)

    
    scheduled_at = Column(DateTime(timezone=True), nullable=True)


    # Extraordinary database safety measure for referential integrity (e.g., system purge or tests).
    # Under normal application workflow, deletion of periods is not permitted 
    # as session records rely on soft deletes (is_deleted) to preserve study history.
    periods = relationship(
        "SessionPeriod",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="SessionPeriod.started_at",
    )
    owner = relationship("User", 
    back_populates="sessions")

    """subject = relationship("Subject", back_populates="sessions")"""


    @property
    def is_completed(self) -> bool:
        return self.is_completed_flag 
        
    @property
    def is_cancelled(self) -> bool:
        return self.is_cancelled_flag
    

    @property
    def started_at(self) -> DateTime | None:
        return self.periods[0].started_at if self.periods else None

    @property
    def completed_at(self) -> DateTime | None:

        if self.is_completed and self.periods:
            return self.periods[-1].ended_at
        return None