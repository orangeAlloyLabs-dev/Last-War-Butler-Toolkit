"""Utility functions for the Discord bot."""

from datetime import datetime, timezone


def format_timestamp(dt: datetime | None = None) -> str:
    """Format a datetime as a Discord timestamp."""
    if dt is None:
        dt = datetime.now(timezone.utc)
    return f"<t:{int(dt.timestamp())}:F>"


def truncate_text(text: str, max_length: int = 2000) -> str:
    """Truncate text to fit within Discord's message limit."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
