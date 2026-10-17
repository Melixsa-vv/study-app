from typing import Any, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session as dbSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.participant import ParticipantRead, ParticipantCreate
from app.services.participant_service import participant_service

router = APIRouter()

@router.get("", response_model=List[ParticipantRead])
def get_session_participants(
    session_id: int,
    db: dbSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return participant_service.get_participants_by_session(
        db, user_id=current_user.id, session_id=session_id
    )

@router.post("", response_model=ParticipantRead, status_code=status.HTTP_201_CREATED)
def add_participant_to_session(
    session_id: int,
    participant_in: ParticipantCreate,
    db: dbSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return participant_service.add_participant(
        db, user_id=current_user.id, session_id=session_id, participant_in=participant_in
    )

@router.delete("/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_participant_from_session(
    session_id: int,
    participant_id: int,
    db: dbSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    participant_service.remove_participant(
        db, user_id=current_user.id, session_id=session_id, participant_id=participant_id
    )