from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.crud_session import crud_session


class AdminService():


    def hard_remove_session(
        self,
        db: Session,
        *,
        session_id: int,
    ):
        s = crud_session.get_by_id(db, session_id=session_id)
        if not s:
            raise HTTPException(
                
            )
        crud_session.hard_remove(db, session= s)


admin_service = AdminService()