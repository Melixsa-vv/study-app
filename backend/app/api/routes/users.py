from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.services import user_service
from app.db.base import get_db

router = APIRouter()

@router.post("/", response_model=UserRead)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db, user_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    return user