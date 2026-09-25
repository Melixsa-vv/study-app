from typing import Any, Generic, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


