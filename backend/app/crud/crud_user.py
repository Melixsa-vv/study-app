from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.schemas.user import UserUpdate, UserCreate
from app.models.user import User

class CRUDUser(CRUDBase[User,UserCreate,UserUpdate]):

    def get_user_by_email(self, db:Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def is_active(self, user: User) -> bool:
        return user.is_active

    def get_multi_active(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[User]:
        return (
            db.query(User)
            .filter(User.is_active)
            .offset(skip)
            .limit(limit)
            .all()
        )

user_crud = CRUDUser(User)
