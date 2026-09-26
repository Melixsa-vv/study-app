from app.crud.base import CRUDBase
from sqlalchemy.orm import Session as dbSession
from app.schemas.subject import SubjectCreate, SubjectUpdate
from app.models.subject import Subject


class CRUDSubject(CRUDBase[Subject, SubjectCreate, SubjectUpdate]):

    def get_subjects_by_user(self, db: dbSession, *, user_id: str, skip: int = 0, limit: int = 100) -> list[Subject]:
        return (
            db.query(Subject)
            .filter(
                Subject.user_id == user_id
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id_and_user(self, db: dbSession, *, user_id: str, subject_id: str) -> Subject | None:
        return (
            db.query(Subject)
            .filter(
                Subject.user_id == user_id,
                Subject.id == subject_id
            ).first()
        )
        

    def get_default_by_user(self, db: dbSession, *, user_id: str) -> Subject | None :
        return(
            db.query(Subject)
            .filter(
                Subject.user_id == user_id,
                Subject.is_default
            ).first()
        )

    def get_by_name_and_user(self, db: dbSession, *, name: str, user_id: str) -> Subject | None:
        return (
            db.query(Subject)
            .filter(
                Subject.user_id == user_id,
                Subject.name == name
            )
            .first()
        )

    def unset_default_subject(self, db: dbSession, *, user_id: str) -> None:
        db.query(Subject).filter(
            Subject.user_id == user_id,
            Subject.is_default.is_(True)
        ).update({"is_default": False}, synchronize_session=False)
    

    def set_new_default(self, db: dbSession, *, subject_id: str, user_id: str) -> Subject | None:
        
        subject = self.get_by_id_and_user(db, subject_id=subject_id, user_id=user_id)
        if not subject:
            return None

        self.unset_default_subject(db, user_id=user_id)

        subject.is_default = True
        db.commit()
        db.refresh(subject)

        return subject