from app.db.session import engine
from app.db.base import Base 

def reset_db() -> None:
    print("Dropping old tables...")
    Base.metadata.drop_all(bind=engine)

    print("Creating tables with the new structure (TimestampMixin)...")
    Base.metadata.create_all(bind=engine)

    print("Database reset successfully.")


if __name__ == "__main__":
    reset_db()

