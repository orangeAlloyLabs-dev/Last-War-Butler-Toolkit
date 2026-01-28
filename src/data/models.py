"""Data models for Last War tracking."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from typing import List


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class Player(Base):
    """Player information and stats."""

    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    alliance_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rank: Mapped[int] = mapped_column(Integer, default=1)  # 1-5
    officer_role: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # Leader, Warlord, Recruiter, Muse, Butler
    power: Mapped[float] = mapped_column(Float, default=0.0)  # e.g., 145.2 means 145.2M
    level: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
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


class DuelCycle(Base):
    """A 4-week duel cycle."""

    __tablename__ = "duel_cycles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cycle_number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    weeks: Mapped["List[DuelWeek]"] = relationship("DuelWeek", back_populates="cycle")
    stats: Mapped["List[DuelCycleStats]"] = relationship(
        "DuelCycleStats", back_populates="cycle", cascade="all, delete-orphan"
    )


class DuelWeek(Base):
    """Duel VS week tracking."""

    __tablename__ = "duel_weeks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    week_number: Mapped[int] = mapped_column(Integer, nullable=False)  # e.g., 1, 2, 3...
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    opponent_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    result: Mapped[str | None] = mapped_column(String(10), nullable=True)  # win/loss/draw
    cycle_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("duel_cycles.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    cycle: Mapped["DuelCycle | None"] = relationship("DuelCycle", back_populates="weeks")
    stats: Mapped["List[DuelWeeklyStats]"] = relationship(
        "DuelWeeklyStats", back_populates="week", cascade="all, delete-orphan"
    )
    days: Mapped["List[DuelDay]"] = relationship(
        "DuelDay", back_populates="week", cascade="all, delete-orphan"
    )


class DuelWeeklyStats(Base):
    """Player stats for a specific duel week."""

    __tablename__ = "duel_weekly_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    week_id: Mapped[int] = mapped_column(Integer, ForeignKey("duel_weeks.id"), nullable=False)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"), nullable=False)
    raw_points: Mapped[float] = mapped_column(Float, default=0.0)
    days_participated: Mapped[int] = mapped_column(Integer, default=0)  # 0-6
    normalized_points: Mapped[float] = mapped_column(Float, default=0.0)  # calculated
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    week: Mapped["DuelWeek"] = relationship("DuelWeek", back_populates="stats")
    player: Mapped["Player"] = relationship("Player")


# Day themes for Duel VS (Monday=1 through Saturday=6)
DUEL_DAY_THEMES = {
    1: "Radar Training",
    2: "Base Expansion",
    3: "Age of Science",
    4: "Train Heroes",
    5: "Total Mobilization",
    6: "Enemy Buster",
}


class DuelDay(Base):
    """A single day within a duel week."""

    __tablename__ = "duel_days"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    week_id: Mapped[int] = mapped_column(Integer, ForeignKey("duel_weeks.id"), nullable=False)
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-6 (Mon-Sat)
    theme: Mapped[str] = mapped_column(String(50), nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    week: Mapped["DuelWeek"] = relationship("DuelWeek", back_populates="days")
    daily_stats: Mapped["List[DuelDailyStats]"] = relationship(
        "DuelDailyStats", back_populates="day", cascade="all, delete-orphan"
    )


class DuelDailyStats(Base):
    """Player stats for a specific day within a duel week."""

    __tablename__ = "duel_daily_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day_id: Mapped[int] = mapped_column(Integer, ForeignKey("duel_days.id"), nullable=False)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"), nullable=False)
    points: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    day: Mapped["DuelDay"] = relationship("DuelDay", back_populates="daily_stats")
    player: Mapped["Player"] = relationship("Player")


class DuelCycleStats(Base):
    """Player stats aggregated over a 4-week cycle."""

    __tablename__ = "duel_cycle_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cycle_id: Mapped[int] = mapped_column(Integer, ForeignKey("duel_cycles.id"), nullable=False)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"), nullable=False)
    total_points: Mapped[float] = mapped_column(Float, default=0.0)
    weeks_participated: Mapped[int] = mapped_column(Integer, default=0)
    avg_weekly_points: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    cycle: Mapped["DuelCycle"] = relationship("DuelCycle", back_populates="stats")
    player: Mapped["Player"] = relationship("Player")
