from typing import Any
from sqlalchemy.orm import Session as dbSession
from fastapi import APIRouter, Depends,  status

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.session import SessionRead, SessionDetailRead, SessionCreate, SessionUpdate

from app.services.session_service import session_service


router = APIRouter()

@router.post("", 
             response_model=SessionRead,
             status_code=status.HTTP_201_CREATED)
def create_study_session(
    *,
    db: dbSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    session_in: SessionCreate,
) -> Any:
    current_user_id = current_user.id
    return session_service.create_study_session(db, user_id=current_user_id,session_in=session_in)

@router.post("/{session_id}/pause",
             response_model=SessionDetailRead)
def pause_session(
    session_id: int,
    db: dbSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return session_service.pause_session(
        db, user_id=current_user.id, session_id=session_id
    )

@router.post("/{session_id}/resume",
             response_model=SessionDetailRead)
def resume_session(
    session_id: int,
    db: dbSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return session_service.resume_session(
        db, user_id=current_user.id, session_id=session_id
    )

@router.patch("/{session_id}/edit", response_model=SessionDetailRead)
def edit_session_details(
    session_id: int,
    session_in: SessionUpdate,
    db: dbSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return session_service.edit_session_details(
        db,user_id=current_user.id, session_id=session_id, session_in=session_in
    )

@router.post("/active/pause", response_model=SessionDetailRead)
def pause_active_session(
    db: dbSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return session_service.pause_active_session(db, user_id=current_user.id)


@router.post("/active/resume", response_model=SessionDetailRead)
def resume_active_session(
    db: dbSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return session_service.resume_active_session(db, user_id=current_user.id)


@router.post("/{session_id}/end", response_model=SessionDetailRead)
def end_study_session(
    session_id: int,
    db: dbSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return session_service.end_study_session(db, user_id=current_user.id, session_id=session_id)

@router.post("/{session_id}/cancel", response_model=SessionDetailRead)
def cancel_study_session(
    session_id: int,
    db: dbSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return session_service.cancel_study_session(db, user_id=current_user.id, session_id=session_id)


@router.post("/plan", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def plan_new_session(
    session_in: SessionCreate,
    db: dbSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return session_service.plan_new_session(
        db, user_id=current_user.id, session_in=session_in
    )