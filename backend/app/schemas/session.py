from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.models.session import SessionType, SessionVisibility, SessionStatus
from app.schemas.period import SessionPeriod


class SessionBase(BaseModel):
    title: str = Field(
        default="Study Session",
        min_length=1,
        max_length=100,
        description="Título de la sesión de estudio"
    )
    visibility: SessionVisibility = SessionVisibility.EVERYONE
    session_type: SessionType = SessionType.SOLO
    status: SessionStatus = SessionStatus.IN_PROGRESS
    scheduled_at: datetime | None = None


class SessionCreate(SessionBase):
    subject_id: int

class SessionUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    visibility: SessionVisibility | None = None
    session_type: SessionType | None = None
    status: SessionStatus | None = None
    scheduled_at: datetime | None = None
    subject_id: int | None = None


class SessionInDBBase(SessionBase):
    id: int
    created_by: int
    subject_id: int

    started_at: datetime | None = None
    completed_at: datetime | None = None
    
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class SessionRead(SessionInDBBase):
    pass


class SessionDetailRead(SessionInDBBase):
    periods: list[SessionPeriod] = []