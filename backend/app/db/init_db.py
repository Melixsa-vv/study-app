from app.db.session import engine
from app.db.base import Base 

def init_db() -> None:
    print("Connecting to PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    print("Database tables verified and created successfully!")

if __name__ == "__main__":
    init_db()