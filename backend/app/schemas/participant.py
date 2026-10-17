from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.models.participant import InvitationStatus

class ParticipantBase(BaseModel):
    invitation_status: InvitationStatus = InvitationStatus.PENDING

class ParticipantCreate(ParticipantBase):
    user_id: int

class ParticipantUpdate(ParticipantBase):
    invitation_status: InvitationStatus | None = None

class ParticipantInDBBase(ParticipantBase):

    session_id: int
    created_at: datetime
    updated_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class UserBasicRead(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class ParticipantRead(ParticipantBase):
    session_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None
    user: UserBasicRead | None = None

    model_config = ConfigDict(from_attributes=True)