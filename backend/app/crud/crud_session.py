from app.crud.base import CRUDBase
from sqlalchemy.orm import Session as dbSession
from app.schemas.session import SessionUpdate, SessionCreate
from app.models.session import Session
from app.models.session import SessionStatus

class CRUDSession(CRUDBase[Session, SessionCreate, SessionUpdate]):

    def get_latest_by_user(self, db: dbSession, *, user_id: str) -> Session | None:
        return (
            db.query(Session)
            .filter(Session.created_by == user_id)
            .order_by(Session.created_at.desc())
            .first()
        )

    def get_in_progress_by_user(self, db: dbSession, *, user_id: str) -> Session | None:
        return (
            db.query(Session)
            .filter(
                Session.status == SessionStatus.IN_PROGRESS,
                Session.owner == user_id,
            )
            .first()
        )

    def get_by_id_and_user(self, db: dbSession, *, user_id: str, session_id: str) -> Session | None:
        return (
            db.query(Session)
            .filter(
                Session.id == session_id,
                Session.created_by == user_id 
            ).first()
        )

    def get_stats_by_user(self, db: dbSession, *, user_id: str) -> dict:
        ...

    def get_multi_by_user(self, db: dbSession, *, user_id: str) -> list[Session]:
        return (
            db.query(Session)
            .filter(
                Session.created_by == user_id 
            ).all()
        )
