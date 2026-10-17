from fastapi import HTTPException, status
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.crud.crud_session import crud_session
from app.schemas.session import SessionCreate, SessionUpdate
from app.models.session import Session as StudySession
from app.models.period import PeriodType, SessionPeriod 
from app.services.period_service import period_service

class SessionService:
    def __init__(self):
        self.period_service = period_service

    def create_study_session(self, db: Session, user_id: int, session_in: SessionCreate) -> StudySession:
        now = datetime.now(timezone.utc)

        is_scheduled = (
            session_in.scheduled_at is not None and session_in.scheduled_at > now
        )

        if not is_scheduled:
            active_session = self.get_active_by_user(db, user_id=user_id)
            if active_session:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="There is other session active",
                )
            

        session = crud_session.create(db, obj_in=session_in, user_id=user_id)

        if not is_scheduled:
            self.period_service.start_study_period(db, session_id=session.id)
            db.refresh(session)

        return session
        
    def pause_session(self, db: Session, *, user_id: int, session_id: int) -> StudySession:
        session = self.get_by_id_and_owner(db=db, user_id=user_id, session_id=session_id)
        return self._pause_session_logic(db, session=session)

    def pause_active_session(self, db: Session, *, user_id: int) -> StudySession:
        active_session = self.get_active_by_user(db=db, user_id=user_id)

        if not active_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active session found for this user."
            )

        return self._pause_session_logic(db, session=active_session)

    def _pause_session_logic(self, db: Session, *, session: StudySession) -> StudySession:
        if self.is_session_closed(session=session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session is already closed."
            )
        if not session.periods:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session have not started yet"
            )
        current_period: SessionPeriod = session.periods[-1]

        if current_period.period_type == PeriodType.BREAK:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session is already paused."
            )
        if current_period.ended_at is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current study period is already closed."
            )


        self.period_service.end_period(db, period_id=current_period.id)
        self.period_service.start_break_period(db, session_id=session.id)
        
        db.refresh(session)
        return session


    def resume_session(self, db: Session, *, user_id: int, session_id: int) -> StudySession:
        session: StudySession = self.get_by_id_and_owner(db=db, user_id=user_id, session_id=session_id)
        return self._resume_session_logic(db, session=session)

    def resume_active_session(self, db: Session, *, user_id: int) -> StudySession:
        paused_session = self.get_active_by_user(db=db, user_id=user_id)

        if not paused_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active session found for this user.",
            )

        return self._resume_session_logic(db, session=paused_session)

    def _resume_session_logic(self, db: Session, *, session: StudySession) -> StudySession:

        if self.is_session_closed(session=session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session is already closed."
            )
        if not session.periods:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot resume a session without periods.",
            )

        current_period = session.periods[-1]

        if current_period.period_type != PeriodType.BREAK:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session is not paused."
            )
            
        if current_period.ended_at is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current study period is already closed."
            )

        self.period_service.end_period(db, period_id=current_period.id)
        self.period_service.start_study_period(db, session_id=session.id)

        db.refresh(session)
        return session

    def end_study_session(self, db: Session, *, user_id:int, session_id: int) -> StudySession:
        session = self.get_by_id_and_owner(
            db, session_id=session_id, user_id=user_id
        )
        
        if self.is_session_closed(session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session already closed"
            )
        
        if not session.periods:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session has not been started"
            )
        current_period: SessionPeriod = session.periods[-1]
        if current_period.ended_at is None:
            self.period_service.end_period(db,current_period.id)
        
        session.is_completed_flag = True
        db.commit()
        db.refresh(session)
        return session
    
    def cancel_study_session(self, db: Session, *, user_id:int, session_id: int) -> StudySession:

        session = self.get_by_id_and_owner(
            db, session_id=session_id, user_id=user_id
        )
        
        if self.is_session_closed(session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session already closed"
            )

        if not session.periods:
            self.hard_remove_session(db, session=session)
            return session

        current_period: SessionPeriod = session.periods[-1]
        if current_period.ended_at is None:
            self.period_service.end_period(db, current_period.id)

        session.is_cancelled_flag = True
        db.commit()
        db.refresh(session)
        return session
    
    def hard_remove_session(self, db:Session, *, session:StudySession) -> None:
        if session.periods is None:
            crud_session.hard_remove(db, session=session)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove started session"
            )

    def plan_new_session(
        self, db: Session, *, user_id: int, session_in: SessionCreate
    ) -> StudySession:
        now = datetime.now(timezone.utc)

        if session_in.scheduled_at is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A scheduled_at datetime is required to plan a new session."
            )

        if session_in.scheduled_at <= now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scheduled time must be in the future."
            )

        return self.create_study_session(db=db, user_id=user_id, session_in=session_in)

    def edit_session_details(
        self,
        db: Session,
        *,
        user_id: int,
        session_id: int,
        session_in: SessionUpdate,
    ) -> StudySession:
        
        session = session_service.get_by_id_and_owner(
            db, session_id=session_id, user_id=user_id
        )
    
        if self.is_session_closed(session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot edit details of a closed session.",
            )
            
        update_data = session_in.model_dump(exclude_unset=True)

        if "scheduled_at" in update_data and update_data["scheduled_at"] is not None:
            now = datetime.now(timezone.utc)
            if update_data["scheduled_at"] <= now:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Scheduled time must be in the future.",
                )

        updated_session = crud_session.update(
            db, db_obj=session, obj_in=update_data
        )
        return updated_session
    
    #UTILS
    def get_by_id(self, db: Session, *, session_id: int) -> StudySession | None:
        return crud_session.get(db, id=session_id)

    def get_by_id_and_owner(self, db: Session, *, session_id: int, user_id: int) -> StudySession:
        session = crud_session.get_by_id_and_user(db, session_id=session_id, user_id=user_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found or does not belong to user.",
            )
        return session
    
    def is_session_closed(self, session: Session) -> bool:
        return  session.is_cancelled or session.is_completed

    def get_active_by_user(self, db: Session, user_id: int) -> Session:
        return crud_session.get_active_by_user(db, user_id=user_id)


session_service = SessionService()

    
