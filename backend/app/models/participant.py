import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum
from app.db.base_class import Base

class InvitationStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class Participant(Base):
    __tablename__ = "session_participants"

    session_id = Column(Integer, ForeignKey("sessions.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    status = Column(Enum(InvitationStatus), default=InvitationStatus.PENDING, nullable=False)