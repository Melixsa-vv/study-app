from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Any

from app.core.security import get_password_hash
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy import select, or_

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreate) -> User:

        user_data = obj_in.model_dump(exclude={"password"})
        
        hashed_password = get_password_hash(obj_in.password)

        db_obj = User(
            **user_data,
            hashed_password=hashed_password
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    

    def get_by_email(self, db: Session, email: str) -> User | None:
        stmt = select(User).where(User.email == email, User.is_deleted.is_(False))
        return db.scalars(stmt).first()

    def get_by_username(self, db: Session, user_name: str) -> User | None:
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

    def get_by_id(self, db: Session, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id, User.is_deleted.is_(False))
        return db.scalars(stmt).first()

    def is_email_taken(self, db: Session, email: str) -> bool:
        stmt = select(User.id).where(User.email == email, User.is_deleted.is_(False))
        return db.scalars(stmt).first() is not None

    def remove(self, db: Session, *, id: Any) -> None:
        raise NotImplementedError(
            "Hard delete is strictly forbidden for User model. Use soft_delete() instead."
        )

    def soft_delete(self, db: Session, *, user_id: int) -> User | None:
        user = self.get_by_id(db, user_id)
        if user:
            user.is_deleted = True
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    def search(
        self, db: Session, *, query: str, skip: int = 0, limit: int = 20
    ) -> list[User]:
        stmt = (
            select(User)
            .where(
                User.is_deleted.is_(False),
                or_(
                    User.user_name.ilike(f"%{query}%"),
                    User.email.ilike(f"%{query}%"),
                ),
            )
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

crud_user = CRUDUser(User)