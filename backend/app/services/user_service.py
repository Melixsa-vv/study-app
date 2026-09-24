class UserService:
    def register_user(self, data: UserCreate):
        # 1. Comprobar username y email.
        # 2. Hashear la contraseña.
        # 3. Crear objeto User ORM.
        # 4. Guardarlo en PostgreSQL.
        # 5. Crear la materia por defecto.
        # 6. Devolver User.
        ...

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def create_user(db: Session, user_in: UserCreate) -> User:
    # 1. Comprobar si existe
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        return None
    
    # 2. Hashear password y crear modelo ORM
    hashed_password = get_password_hash(user_in.password)
    db_user = User(email=user_in.email, hashed_password=hashed_password)
    
    # 3. Guardar en base de datos
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user