from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.crud_period import crud_period 
from app.models.period import SessionPeriod, PeriodType   
from app.schemas.period import SessionPeriodCreate

class PeriodService:

    def start_study_period(self, db: Session, session_id: int) -> SessionPeriod:
        active_period: SessionPeriod = crud_period.get_active_period_by_session(db, session_id=session_id)

        if active_period:
            if active_period.period_type == PeriodType.STUDY:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="There is already a study period active for this session."
                )
            self.end_period(db, period_id=active_period.id)
        
        period_in = SessionPeriodCreate(
            session_id=session_id,
            period_type=PeriodType.STUDY,
            started_at=datetime.now(timezone.utc)
        )

        return crud_period.create(db, obj_in=period_in)

    def start_break_period(self, db: Session, session_id: int) -> SessionPeriod:
        active_period: SessionPeriod = crud_period.get_active_period_by_session(db, session_id=session_id)

        if active_period:
            if active_period.period_type == PeriodType.BREAK:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="There is already a break period active for this session."
                )
            self.end_period(db, period_id=active_period.id)
        
        period_in = SessionPeriodCreate(
            session_id=session_id,
            period_type=PeriodType.BREAK,
            started_at=datetime.now(timezone.utc)
        )
        return crud_period.create(db, obj_in=period_in)

    def end_period(self, db: Session, period_id: int) -> SessionPeriod:
        period = self.get_by_id(db, period_id=period_id)
        if not period or period.ended_at is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active period not found."
            )
        return crud_period.close_active_period(db, db_obj=period)

    def get_by_id(self, db: Session, period_id: int) -> SessionPeriod | None:
        return crud_period.get(db, id=period_id)

    def is_period_active(self, db: Session, session_id: int) -> bool:
        return crud_period.get_active_period_by_session(db, session_id=session_id) is not None

period_service = PeriodService()