from fastapi import HTTPException, status
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.session import Session as StudySession, SessionType
from app.models.participant import Participant, InvitationStatus
from app.crud.crud_participant import crud_participant

class ParticipantService():
    #GROUP STUFF
    def invite_user_to_session(
        self,
        db: Session,
        *,
        session: StudySession,
        user_to_invite_id: int,
    ) -> Participant:

        if self.is_session_closed(session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot invite users to a closed session.",
            )

        if session.session_type != SessionType.GROUP:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot invite users to a solo session.",
            )

        existing_participant = crud_participant.get_by_user_and_session(
            db, session_id=session.id, user_id=user_to_invite_id
        )
        if existing_participant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User already invited with status: {existing_participant.status}",
            )

        participant = crud_participant.create(
            db,
            obj_in={
                "session_id": session.id,
                "user_id": user_to_invite_id,
                "status": InvitationStatus.PENDING,
            },
        )
        return participant

    def respond_to_invitation(
        self,
        db: Session,
        *,
        session_id: int,
        user_id: int,
        accept: bool,
    ) -> Participant:

        participant = crud_participant.get_by_user_and_session(db, session_id=session_id, user_id=user_id)

        if not participant or participant.status != InvitationStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No pending invitation found for this session.",
            )

        new_status = InvitationStatus.ACCEPTED if accept else InvitationStatus.REJECTED
        updated_participant = crud_participant.update_status(
            db, db_obj=participant, obj_in={"invitation_status": new_status}
        )
        return updated_participant

    def remove_user_from_session(
        self,
        db: Session,
        *,
        session: StudySession,
        user_to_remove_id: int,
    ) -> None:

        if user_to_remove_id == session.created_by:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove the owner from the session.",
            )

        participant = crud_participant.get_by_user_and_session(
            db, session_id=session.id, user_id=user_to_remove_id
        )
        if not participant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is not a participant or invited to this session.",
            )

        crud_participant.remove_participant(db, db_obj=participant)

participant_service = ParticipantService()