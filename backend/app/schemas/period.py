from pydantic import BaseModel, Field, ConfigDict
from app.models.period import PeriodType
from datetime import datetime

class SessionPeriodBase(BaseModel):

    period_type: PeriodType = Field(
        default=PeriodType.STUDY,
        description="Type of period: 'study' for active work or 'break' for rest",
    )

    started_at: datetime | None = Field(
        default=None,
        description="Timestamp when the period started. If omitted on create, backend sets UTC now",
    )
    ended_at: datetime | None = Field(
        default=None,
        description="Timestamp when the period ended (None if currently active)",
    )

class SessionPeriodCreate(SessionPeriodBase):

    session_id: int = Field(
        description="ID of the parent session to attach this period to"
    )

class SessionPeriodUpdate(BaseModel):

    period_type: PeriodType | None = Field(
        default=None,
        description="Update the period type (e.g., convert study block to break)",
    )

    ended_at: datetime | None = Field(
        default=None,
        description="Timestamp to close or manually adjust the end time",
    )

class SessionPeriodInDBBase(SessionPeriodBase):
    id: int
    session_id: int
    started_at: datetime
    
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class SessionPeriodRead(SessionPeriodInDBBase):
    pass