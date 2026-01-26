"""Database storage and connection management."""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
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


def run_migrations(engine):
    """Run database migrations for schema updates."""
    inspector = inspect(engine)

    # Migration: Add cycle_id column to duel_weeks if it doesn't exist
    if "duel_weeks" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("duel_weeks")]
        if "cycle_id" not in columns:
            with engine.connect() as conn:
                conn.execute(
                    text("ALTER TABLE duel_weeks ADD COLUMN cycle_id INTEGER")
                )
                conn.commit()

    # Migration: Add name column to duel_cycles if it doesn't exist
    if "duel_cycles" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("duel_cycles")]
        if "name" not in columns:
            with engine.connect() as conn:
                conn.execute(
                    text("ALTER TABLE duel_cycles ADD COLUMN name VARCHAR(100)")
                )
                conn.commit()

    # Migration: Add is_active column to players if it doesn't exist (default True)
    if "players" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("players")]
        if "is_active" not in columns:
            with engine.connect() as conn:
                conn.execute(
                    text("ALTER TABLE players ADD COLUMN is_active BOOLEAN DEFAULT 1")
                )
                # Set all existing players to active
                conn.execute(text("UPDATE players SET is_active = 1 WHERE is_active IS NULL"))
                conn.commit()


def init_database():
    """Initialize the database and create all tables."""
    engine = get_engine()
    # Create new tables
    Base.metadata.create_all(engine)
    # Run migrations for existing tables
    run_migrations(engine)
    return engine


def get_session() -> Session:
    """Get a database session."""
    engine = get_engine()
    session_factory = sessionmaker(bind=engine)
    return session_factory()
