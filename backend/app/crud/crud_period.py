from sqlalchemy import select
from sqlalchemy.orm import Session

from datetime import datetime, timezone

from app.crud.base import CRUDBase
from app.models.period import SessionPeriod, PeriodType
from app.schemas.period import SessionPeriodCreate, SessionPeriodUpdate

class CRUDPeriod(CRUDBase[SessionPeriod, SessionPeriodCreate,SessionPeriodUpdate]):

    def get_active_period_by_session(
        self, db: Session, *, session_id: int
    ) -> SessionPeriod | None:
        stmt = select(SessionPeriod).where(
            SessionPeriod.session_id == session_id,
            SessionPeriod.ended_at.is_(None),
        )
        return db.scalars(stmt).first()
    
    def get_first_period(self, db: Session, *, session_id: int) -> SessionPeriod | None:
        stmt = (
            select(SessionPeriod)
            .where(SessionPeriod.session_id == session_id)
            .order_by(SessionPeriod.started_at.asc())
        )
        return db.scalars(stmt).first()

    def get_last_period(self, db:Session,*, session_id: int) -> SessionPeriod | None:
        stmt = (
            select(SessionPeriod)
            .where(SessionPeriod.session_id == session_id)
            .order_by(SessionPeriod.started_at.desc())
        )
        return db.scalars(stmt).first()

    def get_periods_by_session(self, db:Session,*, session_id: int) -> list[SessionPeriod]:
        stmt = (
            select(SessionPeriod)
            .where(SessionPeriod.session_id == session_id)
            .order_by(SessionPeriod.started_at.asc())
        )
        return list(db.scalars(stmt).all())

    def get_breaks_by_session(self, db:Session,*, session_id: int) -> list[SessionPeriod]:
        stmt = (
            select(SessionPeriod)
            .where(
                SessionPeriod.session_id == session_id,
                SessionPeriod.period_type == PeriodType.BREAK
            )
            .order_by(SessionPeriod.started_at.asc())
        )

        return list(db.scalars(stmt).all())

    def get_studies_by_session(self, db:Session,*, session_id: int) -> list[SessionPeriod]:
        stmt = (
            select(SessionPeriod)
            .where(
                SessionPeriod.session_id == session_id,
                SessionPeriod.period_type == PeriodType.STUDY
            )
            .order_by(SessionPeriod.started_at.asc())
        )

        return list(db.scalars(stmt).all())

    def close_active_period(
        self, db: Session, *, db_obj: SessionPeriod, ended_at: datetime | None = None
    ) -> SessionPeriod:
        db_obj.ended_at = ended_at or datetime.now(timezone.utc)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


period = CRUDPeriod(SessionPeriod)