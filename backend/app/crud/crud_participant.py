from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session as dbSession

from app.crud.base import CRUDBase
from app.schemas.participant import ParticipantCreate, ParticipantUpdate
from app.models.participant import Participant

class CRUDParticipant(CRUDBase[Participant, ParticipantCreate, ParticipantUpdate]):

    def add_participant(
        self, db: dbSession, *, obj_in: ParticipantCreate, session_id: int
    ) -> Participant:
        
        participant_data = obj_in.model_dump()
        participant_data["session_id"] = session_id
 
        db_obj = Participant(**participant_data)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user_and_session(
        self, db: dbSession, *, session_id: int, user_id: int
    ) -> Participant | None:
        stmt = select(Participant).where(
            Participant.session_id == session_id,
            Participant.user_id == user_id,
        )
        return db.scalars(stmt).first()

    def get_multi_by_session_id(
        self, db: dbSession, *, session_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Participant]:

        stmt = (
            select(Participant)
            .where(Participant.session_id == session_id)
            .offset(skip)
            .limit(limit)
        )
        return db.scalars(stmt).all()

    def update_status(
        self,
        db: dbSession,
        *,
        db_obj: Participant,
        obj_in: ParticipantUpdate,
    ) -> Participant:
        update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_participant(
        self, db: dbSession, *, session_id: int, user_id: int
    ) -> Participant | None:
        participant = self.get_by_user_and_session(db, session_id=session_id, user_id=user_id)
        if participant:
            db.delete(participant)
            db.commit()
        return participant

crud_participant = CRUDParticipant(Participant)