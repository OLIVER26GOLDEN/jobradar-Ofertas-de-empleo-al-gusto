from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./jobradar.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Solo necesario para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependencia para obtener sesión de BD en cada request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
