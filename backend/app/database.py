"""
database.py
============
Sets up the SQLite database connection for the Predictive Intelligence Engine.

Why SQLite?
-----------
For a hackathon-scale project SQLite is perfect: zero setup, no separate
server process, and the whole database lives in one file
(`backend/data/app.db`). If you later need Postgres/MySQL for production,
you only need to change the `DATABASE_URL` value below — every route and
model in this project uses SQLAlchemy, so nothing else has to change.
"""

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = Path(__file__).resolve().parent.parent  # -> backend/
DB_DIR = BASE_DIR / "data"
DB_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_DIR / 'app.db'}")

# check_same_thread=False is required for SQLite when FastAPI uses it
# across multiple worker threads/requests.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables if they don't exist yet. Called on app startup."""
    from app import models  # noqa: F401  (ensures models are registered)
    Base.metadata.create_all(bind=engine)
