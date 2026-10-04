from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.crud_user import crud_user
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User


class UserService:
    def register_user(self, db: Session, user_in: UserCreate) -> User:

        if crud_user.get_by_email(db, email=user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists in the system.",
            )

        if hasattr(user_in, "user_name") and user_in.user_name:
            if crud_user.get_by_username(db, user_name=user_in.user_name):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This username is already taken.",
                )

        hashed_password = get_password_hash(user_in.password)

        return crud_user.create(
            db, obj_in=user_in, hashed_password=hashed_password
        )

    def get_user_by_id(self, db: Session, user_id: int) -> User:
        user = crud_user.get_by_id(db, user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    def delete_user(self, db: Session, user_id: int) -> User:
        user = crud_user.soft_delete(db,  user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
    
    def authenticate(
        self, db: Session, username_or_email: str, password: str
    ) -> User:

        user = crud_user.get_by_email(db, email=username_or_email)

        if not user:
            user = crud_user.get_by_username(db, user_name=username_or_email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username, email, or password",
            )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username, email, or password",
            )

        return user

    def update_user(self, db: Session, user_id: int, user_in: UserUpdate) -> User:

        user = self.get_user_by_id(db, user_id)

        if user_in.email and user_in.email != user.email:
            if self.is_email_taken(db, user_in.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use",
                )

        if user_in.user_name and user_in.user_name != user.user_name:
            if crud_user.get_by_username(db, user_name=user_in.user_name):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already in use",
                )

        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data:
            raw_password = update_data.pop("password")
            update_data["hashed_password"] = get_password_hash(raw_password)

        return crud_user.update(db, db_obj=user, obj_in=update_data)

    def search_users(
        self, db: Session, query: str, skip: int = 0, limit: int = 20
    ) -> list[User]:
        
        if not query or not query.strip():
            return []
        return crud_user.search(db, query=query, skip=skip, limit=limit)

    def update_password(
        self, db: Session, user: User, current_password: str, new_password: str
    ) -> User:

        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect current password",
            )

        hashed_password = get_password_hash(new_password)
        return crud_user.update(
            db, db_obj=user, obj_in={"hashed_password": hashed_password}
        )

    def is_email_taken(self, db: Session, email: str) -> bool:
        return crud_user.is_email_taken(db, email)

user_service = UserService()