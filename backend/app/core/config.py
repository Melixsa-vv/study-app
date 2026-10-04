from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
   
    PROJECT_NAME: str = "StudyApp"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SQLALCHEMY_DATABASE_URI: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()