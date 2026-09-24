from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.models.session import SessionType, SessionVisibility

class SessionBase(BaseModel):
    title: str = Field(
        default="Study Session",
        min_length=1,
        max_length=100,
        description="Título de la sesión de estudio"
    )
    visibility: SessionVisibility = SessionVisibility.EVERYONE
    session_type: SessionType = SessionType.SOLO
    subject_id: int

class SessionCreate(SessionBase):
    pass

class SessionRead(SessionBase):
    id: int
    created_by: int
    completed: bool
    completed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class SessionUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    visibility: SessionVisibility | None = None
    session_type: SessionType | None = None
    subject_id: int | None = None
    completed: bool | None = None