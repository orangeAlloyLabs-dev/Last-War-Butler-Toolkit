"""Database storage and connection management."""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base

load_dotenv()


def get_database_url() -> str:
    """Get the database URL from environment or default to SQLite."""
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    # Default to SQLite in the data directory
    data_dir = Path(__file__).parent.parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    return f"sqlite:///{data_dir}/lastwar.db"


def get_engine():
    """Create and return a database engine."""
    return create_engine(get_database_url(), echo=False)


def init_database():
    """Initialize the database and create all tables."""
    engine = get_engine()
    Base.metadata.create_all(engine)
    return engine


def get_session() -> Session:
    """Get a database session."""
    engine = get_engine()
    session_factory = sessionmaker(bind=engine)
    return session_factory()
