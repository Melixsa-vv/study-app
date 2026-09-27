from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class SubjectBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=50,
        description="Subject's name"
    )

    description: str | None = Field(
        default=None,
        max_length=255,
        description="Optional subject description",
    )

    color: str = Field(
        default="#80C0F5",
        min_length=4,
        max_length=9,
        description="HEX color code for UI display",
    )

    is_default: bool = False

class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Subject's name"
    )
    description: str | None = Field(default=None, max_length=255)
    color: str | None = Field(default=None, min_length=4, max_length=9)

    is_default: bool | None = None

class SubjectInDBBase(SubjectBase):
    id: int
    user_id: int
    is_deleted: bool = False

    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class SubjectRead(SubjectInDBBase):
    pass