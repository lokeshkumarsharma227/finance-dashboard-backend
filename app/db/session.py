from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from typing import Generator
# Sets up the database connection.
# engine is created once at startup — reused for every request.
# get_db() is a FastAPI dependency — yields a session per request, always closes it.

engine=create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
    )# One engine for the entire app lifetime
SessionLocal=sessionmaker(autocommit=False,
                          autoflush=False,
                          bind=engine)
def get_db()->Generator:
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()