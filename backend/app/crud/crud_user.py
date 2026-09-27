from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_user_by_email(self, db: Session, email: str) -> User | None:
        stmt = select(User).where(User.email == email, User.is_deleted.is_(False))
        return db.scalars(stmt).first()

    def get_user_by_username(self, db: Session, user_name: str) -> User | None:
        stmt = select(User).where(User.user_name == user_name, User.is_deleted.is_(False))
        return db.scalars(stmt).first()

    def get_multi_active(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[User]:
        stmt = (
            select(User)
            .where(User.is_deleted.is_(False))
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())


user = CRUDUser(User)