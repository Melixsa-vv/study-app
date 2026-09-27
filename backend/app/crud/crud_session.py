from sqlalchemy import select
from sqlalchemy.orm import Session as dbSession

from app.crud.base import CRUDBase
from app.models.session import Session, SessionStatus
from app.schemas.session import SessionCreate, SessionUpdate


class CRUDSession(CRUDBase[Session, SessionCreate, SessionUpdate]):

    def get_latest_by_user(self, db: dbSession, *, user_id: int) -> Session | None:
        stmt = (
            select(Session)
            .where(Session.created_by == user_id)
            .order_by(Session.created_at.desc())
        )
        return db.scalars(stmt).first()

    def get_in_progress_by_user(self, db: dbSession, *, user_id: int) -> Session | None:
        stmt = select(Session).where(
            Session.status == SessionStatus.IN_PROGRESS,
            Session.created_by == user_id,  # Corregido: de owner a created_by
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

    def get_stats_by_user(self, db: dbSession, *, user_id: int) -> dict:
        ...

session = CRUDSession(Session)