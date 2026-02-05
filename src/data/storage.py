"""Database storage and connection management."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, sessionmaker

from .models import Base, Setting

load_dotenv()


# Default reliability threshold (7.2M points per day)
DEFAULT_RELIABILITY_THRESHOLD = 7_200_000

# Default event types for alliance scheduling
DEFAULT_EVENT_TYPES = [
    "Duel VS",
    "Kill Event",
    "Alliance War",
    "Rally",
    "Resource Event",
    "Training Event",
    "Custom",
]


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
                conn.execute(text("ALTER TABLE duel_weeks ADD COLUMN cycle_id INTEGER"))
                conn.commit()

    # Migration: Add name column to duel_cycles if it doesn't exist
    if "duel_cycles" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("duel_cycles")]
        if "name" not in columns:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE duel_cycles ADD COLUMN name VARCHAR(100)"))
                conn.commit()

    # Migration: Add is_active column to players if it doesn't exist (default True)
    if "players" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("players")]
        if "is_active" not in columns:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE players ADD COLUMN is_active BOOLEAN DEFAULT 1"))
                # Set all existing players to active
                conn.execute(text("UPDATE players SET is_active = 1 WHERE is_active IS NULL"))
                conn.commit()

    # Migration: Add kill_count columns to players
    if "players" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("players")]
        if "kill_count" not in columns:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE players ADD COLUMN kill_count INTEGER DEFAULT 0"))
                conn.execute(text("ALTER TABLE players ADD COLUMN kill_count_updated_at DATETIME"))
                conn.commit()

    # Migration: Add kills_snapshot column to duel_weekly_stats
    if "duel_weekly_stats" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("duel_weekly_stats")]
        if "kills_snapshot" not in columns:
            with engine.connect() as conn:
                conn.execute(
                    text("ALTER TABLE duel_weekly_stats ADD COLUMN kills_snapshot INTEGER")
                )
                conn.commit()

    # Migration: Create settings table and insert default reliability threshold
    if "settings" in inspector.get_table_names():
        # Check if reliability_threshold setting exists
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT id FROM settings WHERE key = 'reliability_threshold'")
            )
            if result.fetchone() is None:
                conn.execute(
                    text(
                        "INSERT INTO settings (key, value, description) VALUES "
                        "('reliability_threshold', :value, :description)"
                    ),
                    {
                        "value": str(DEFAULT_RELIABILITY_THRESHOLD),
                        "description": "Min daily points for a reliable VS day",
                    },
                )
                conn.commit()

    # Migration: Add import_id column to kill_history table
    if "kill_history" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("kill_history")]
        if "import_id" not in columns:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE kill_history ADD COLUMN import_id INTEGER"))
                conn.commit()

    # Migration: Remove alliance_total column from duel_weeks (no longer in model)
    if "duel_weeks" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("duel_weeks")]
        if "alliance_total" in columns:
            with engine.connect() as conn:
                conn.execute(text(
                    "CREATE TABLE duel_weeks_new ("
                    "id INTEGER NOT NULL PRIMARY KEY, "
                    "week_number INTEGER NOT NULL, "
                    "start_date DATETIME NOT NULL, "
                    "opponent_name VARCHAR(100), "
                    "result VARCHAR(10), "
                    "cycle_id INTEGER REFERENCES duel_cycles(id), "
                    "created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)"
                ))
                conn.execute(text(
                    "INSERT INTO duel_weeks_new "
                    "(id, week_number, start_date, opponent_name, result, cycle_id, created_at) "
                    "SELECT id, week_number, start_date, opponent_name, result, cycle_id, "
                    "created_at FROM duel_weeks"
                ))
                conn.execute(text("DROP TABLE duel_weeks"))
                conn.execute(text("ALTER TABLE duel_weeks_new RENAME TO duel_weeks"))
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


def get_setting(key: str, default: str | None = None, session: Session | None = None) -> str | None:
    """Fetch a setting value by key.

    Args:
        key: The setting key to look up
        default: Default value if setting not found
        session: Optional existing session

    Returns:
        The setting value or default if not found
    """
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        setting = session.query(Setting).filter(Setting.key == key).first()
        if setting:
            return setting.value
        return default
    finally:
        if close_session:
            session.close()


def set_setting(
    key: str, value: str, description: str | None = None, session: Session | None = None
) -> Setting:
    """Insert or update a setting.

    Args:
        key: The setting key
        value: The setting value
        description: Optional description of the setting
        session: Optional existing session

    Returns:
        The created or updated Setting object
    """
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        setting = session.query(Setting).filter(Setting.key == key).first()
        if setting:
            setting.value = value
            if description is not None:
                setting.description = description
        else:
            setting = Setting(key=key, value=value, description=description)
            session.add(setting)
        session.commit()
        session.refresh(setting)
        return setting
    finally:
        if close_session:
            session.close()


def get_reliability_threshold(session: Session | None = None) -> float:
    """Get the reliability threshold setting.

    Returns:
        The threshold as a float (default: 7,200,000)
    """
    value = get_setting("reliability_threshold", session=session)
    if value is None:
        return float(DEFAULT_RELIABILITY_THRESHOLD)
    return float(value)


def set_reliability_threshold(threshold: float, session: Session | None = None) -> Setting:
    """Set the reliability threshold.

    Args:
        threshold: The threshold value in points
        session: Optional existing session

    Returns:
        The updated Setting object
    """
    return set_setting(
        "reliability_threshold",
        str(threshold),
        description="Minimum daily points to count as a reliable day for VS combat",
        session=session,
    )


def get_event_types(session: Session | None = None) -> list[str]:
    """Get configured event types from settings.

    Args:
        session: Optional existing session

    Returns:
        List of event type strings
    """
    value = get_setting("event_types", json.dumps(DEFAULT_EVENT_TYPES), session=session)
    return json.loads(value)


def set_event_types(event_types: list[str], session: Session | None = None) -> Setting:
    """Save event types to settings.

    Args:
        event_types: List of event type strings
        session: Optional existing session

    Returns:
        The updated Setting object
    """
    return set_setting(
        "event_types",
        json.dumps(event_types),
        description="Event type options for alliance scheduling",
        session=session,
    )
