from sqlalchemy import select, update
from sqlalchemy.orm import Session as dbSession

from app.crud.base import CRUDBase
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate, SubjectUpdate


class CRUDSubject(CRUDBase[Subject, SubjectCreate, SubjectUpdate]):

    def get_subjects_by_user(
        self, db: dbSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Subject]:
        stmt = (
            select(Subject)
            .where(Subject.user_id == user_id, Subject.is_deleted.is_(False))
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

    def get_by_id_and_user(
        self, db: dbSession, *, user_id: int, subject_id: int
    ) -> Subject | None:
        stmt = select(Subject).where(
            Subject.user_id == user_id,
            Subject.id == subject_id,
            Subject.is_deleted.is_(False),
        )
        return db.scalars(stmt).first()

    def get_default_by_user(self, db: dbSession, *, user_id: int) -> Subject | None:
        stmt = select(Subject).where(
            Subject.user_id == user_id,
            Subject.is_default.is_(True),
            Subject.is_deleted.is_(False),
        )
        return db.scalars(stmt).first()

    def get_by_name_and_user(
        self, db: dbSession, *, name: str, user_id: int
    ) -> Subject | None:
        stmt = select(Subject).where(
            Subject.user_id == user_id,
            Subject.name == name,
            Subject.is_deleted.is_(False),
        )
        return db.scalars(stmt).first()

    def unset_default_subject(self, db: dbSession, *, user_id: int) -> None:
        """Sintaxis 2.0 con update() explícito."""
        stmt = (
            update(Subject)
            .where(Subject.user_id == user_id, Subject.is_default.is_(True))
            .values(is_default=False)
        )
        db.execute(stmt)
        db.commit()

    def set_new_default(
        self, db: dbSession, *, subject_id: int, user_id: int
    ) -> Subject | None:
        subject = self.get_by_id_and_user(db, subject_id=subject_id, user_id=user_id)
        if not subject:
            return None

        self.unset_default_subject(db, user_id=user_id)

        subject.is_default = True
        db.commit()
        db.refresh(subject)
        return subject


subject = CRUDSubject(Subject)