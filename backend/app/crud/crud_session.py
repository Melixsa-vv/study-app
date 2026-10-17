from sqlalchemy import select
from sqlalchemy.orm import Session as dbSession
from typing import Optional

from app.crud.base import CRUDBase

from app.models.session import Session
from app.models.period import SessionPeriod

from app.schemas.session import SessionCreate, SessionUpdate


class CRUDSession(CRUDBase[Session, SessionCreate, SessionUpdate]):
    def create(
        self, db: dbSession, *, obj_in: SessionCreate, user_id: int
    ) -> Session:
        obj_in_data = obj_in.model_dump()
        obj_in_data["created_by"] = user_id
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_latest_by_user(self, db: dbSession, *, user_id: int) -> Session | None:
        stmt = (
            select(Session)
            .where(Session.created_by == user_id)
            .order_by(Session.created_at.desc())
        )
        return db.scalars(stmt).first()

    def get_active_by_user(
        self, db: dbSession, *, user_id: int
    ) -> Optional[Session]:
        stmt = (
            select(Session)
            .join(Session.periods)
            .where(
                Session.created_by == user_id,
                Session.is_completed_flag.is_(False),
                Session.is_cancelled_flag.is_(False),
                SessionPeriod.ended_at.is_(None), 
            )
            .order_by(SessionPeriod.started_at.desc())
        )

        return db.scalars(stmt).first()

    def get_by_id_and_user(
        self, db: dbSession, *, user_id: int, session_id: int
    ) -> Session | None:
        stmt = select(Session).where(
            Session.id == session_id,
            Session.created_by == user_id,
        )
        return db.scalars(stmt).first()

    def get_multi_by_user(
        self, db: dbSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Session]:
        stmt = (
            select(Session)
            .where(Session.created_by == user_id)
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())


    def get_by_id(self, db: dbSession, *, session_id: int) -> Session:
        return db.get(Session, session_id)
    
    def hard_remove(self, db: dbSession, *, session: Session) -> None:
        db.delete(session)
        db.commit()

    def get_stats_by_user(self, db: dbSession, *, user_id: int) -> dict:
        ...

crud_session = CRUDSession(Session)