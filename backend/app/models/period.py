from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base, TimestampMixin
import enum

class PeriodType(str, enum.Enum):
    STUDY = "study"
    BREAK = "break"


class SessionPeriod(Base, TimestampMixin):
    __tablename__ = "session_periods"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)

    period_type = Column(
        SQLEnum(PeriodType), 
        default=PeriodType.STUDY, 
        nullable=False
    )

    started_at = Column(DateTime(timezone=True), nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=True)

    session = relationship("Session", back_populates="periods")