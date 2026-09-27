from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(
        description="JWT access token string for authenticating API requests"
    )
    token_type: str = Field(
        default="bearer",
        description="Type of the token (always 'bearer' for JWT HTTP authentication)",
    )


class TokenPayload(BaseModel):
    sub: int | None = Field(
        default=None,
        description="Subject claim of the JWT (corresponde al ID del usuario en la base de datos)",
    )