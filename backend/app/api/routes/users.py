from typing import Any
from fastapi import APIRouter, Depends,  status, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, PasswordUpdate, UserRead
from app.services.user_service import user_service

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:

    return user_service.register_user(db, user_in=user_in)


@router.get("/me", response_model=UserRead)
def read_user_me(
    current_user: User = Depends(get_current_user),
) -> Any:

    return current_user


@router.patch("/me", response_model=UserRead)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:

    updated_user = user_service.update_user(db, user_id=current_user.id, user_in=user_in)
    return updated_user


@router.delete("/me", response_model=UserRead)
def delete_user_me(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:

    return user_service.delete_user(db, user_id=current_user.id)


@router.post("/me/password", status_code=status.HTTP_200_OK)
def update_password_me(
    *,
    db: Session = Depends(get_db),
    password_in: PasswordUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:

    user_service.update_password(
        db,
        user=current_user,
        current_password=password_in.current_password,
        new_password=password_in.new_password,
    )
    return {"message": "Password updated successfully"}


@router.get("/search", response_model=list[UserRead])
def search_users(
    *,
    db: Session = Depends(get_db),
    q: str = Query(..., min_length=1, description="Search term for username or email"),
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
) -> Any:

    return user_service.search_users(db, query=q, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserRead, dependencies=[Depends(get_current_user)])
def read_user_by_id(
    *,
    db: Session = Depends(get_db),
    user_id: int,
) -> Any:

    return user_service.get_by_id(db, user_id=user_id)