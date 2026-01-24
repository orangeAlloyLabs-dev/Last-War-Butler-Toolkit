"""Data models for Last War tracking."""

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class Player(Base):
    """Player information and stats."""

    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    alliance_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    power: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


class Alliance(Base):
    """Alliance information."""

    __tablename__ = "alliances"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    tag: Mapped[str] = mapped_column(String(10), nullable=True)
    total_power: Mapped[int] = mapped_column(Integer, default=0)
    member_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


class WarResult(Base):
    """War result tracking."""

    __tablename__ = "war_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    war_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    alliance_id: Mapped[int] = mapped_column(Integer, nullable=False)
    opponent_name: Mapped[str] = mapped_column(String(100), nullable=False)
    our_score: Mapped[float] = mapped_column(Float, default=0.0)
    opponent_score: Mapped[float] = mapped_column(Float, default=0.0)
    result: Mapped[str] = mapped_column(String(10), nullable=False)  # win/loss/draw
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
