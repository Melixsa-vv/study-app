from pydantic import BaseModel, ConfigDict, Field

class SubjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Subject's name"
    )

    description: str
    color: str = Field(
        min_length=8,
        max_length=8
    )

    is_default: bool

class SubjectCreate(SubjectBase):
    pass

class SubjectRead(SubjectBase):
    id: int
    user_id: int
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)

class SubjectUpdate(BaseModel):
    user_id: int | None = None
    name: str | None = Field(
        None,
        min_length=1,
        max_length=50,
        description="Subject's name"
    )
    description: str | None = None
    is_default: bool | None = None