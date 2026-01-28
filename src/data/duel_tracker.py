"""Duel VS tracking and reporting functions."""

import csv
from datetime import datetime, timedelta
from io import StringIO

from sqlalchemy import desc
from sqlalchemy.orm import Session

from .models import (
    DUEL_DAY_THEMES,
    DuelCycle,
    DuelCycleStats,
    DuelDailyStats,
    DuelDay,
    DuelWeek,
    DuelWeeklyStats,
    Player,
)
from .storage import get_session, init_database

# Tier thresholds (configurable)
TIER_THRESHOLDS = {
    "Core": {"min_reliability": 0.90, "min_avg_normalized": 150},
    "Strong": {"min_reliability": 0.75, "min_avg_normalized": 100},
    "Standard": {"min_reliability": 0.50, "min_avg_normalized": 50},
    "Probation": {"min_reliability": 0.0, "min_avg_normalized": 0},
}

ROLLING_WEEKS = 4  # Number of weeks for rolling calculations
ARCHIVE_WEEKS = 8  # Weeks before archiving


def calculate_normalized_points(raw_points: float, days_participated: int) -> float:
    """Normalize points by days participated."""
    return raw_points / max(1, days_participated)


def calculate_reliability(weeks_participated: int, total_weeks: int) -> float:
    """Calculate participation reliability over rolling window."""
    return weeks_participated / max(1, total_weeks)


def assign_tier(avg_normalized: float, reliability: float) -> str:
    """Assign tier based on thresholds. Player must meet BOTH criteria."""
    for tier, thresholds in TIER_THRESHOLDS.items():
        if (
            reliability >= thresholds["min_reliability"]
            and avg_normalized >= thresholds["min_avg_normalized"]
        ):
            return tier
    return "Probation"


# ============ Week Management ============


def create_week(
    week_number: int,
    start_date: datetime,
    opponent_name: str | None = None,
    session: Session | None = None,
) -> DuelWeek:
    """Create a new duel week."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        week = DuelWeek(
            week_number=week_number,
            start_date=start_date,
            opponent_name=opponent_name,
        )
        session.add(week)
        session.commit()
        session.refresh(week)
        return week
    finally:
        if close_session:
            session.close()


def set_week_result(
    week_id: int,
    result: str,
    session: Session | None = None,
) -> DuelWeek:
    """Set the result for a duel week."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        week = session.query(DuelWeek).filter(DuelWeek.id == week_id).first()
        if not week:
            raise ValueError(f"Week with id {week_id} not found")

        week.result = result.lower()
        session.commit()
        session.refresh(week)
        return week
    finally:
        if close_session:
            session.close()


def get_week(week_id: int, session: Session | None = None) -> DuelWeek | None:
    """Get a duel week by ID."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        return session.query(DuelWeek).filter(DuelWeek.id == week_id).first()
    finally:
        if close_session:
            session.close()


def get_recent_weeks(count: int = 4, session: Session | None = None) -> list[DuelWeek]:
    """Get the most recent duel weeks."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        return session.query(DuelWeek).order_by(desc(DuelWeek.week_number)).limit(count).all()
    finally:
        if close_session:
            session.close()


def get_latest_week(session: Session | None = None) -> DuelWeek | None:
    """Get the most recent duel week."""
    weeks = get_recent_weeks(count=1, session=session)
    return weeks[0] if weeks else None


# ============ Day Management ============


def create_days_for_week(
    week_id: int,
    themes: dict[int, str] | None = None,
    session: Session | None = None,
) -> list[DuelDay]:
    """Create all 6 days for a duel week with themes.

    Args:
        week_id: The week to create days for
        themes: Optional dict mapping day_number (1-6) to theme name.
                Defaults to DUEL_DAY_THEMES.
    """
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    if themes is None:
        themes = DUEL_DAY_THEMES

    try:
        week = session.query(DuelWeek).filter(DuelWeek.id == week_id).first()
        if not week:
            raise ValueError(f"Week {week_id} not found")

        # Check if days already exist
        existing = session.query(DuelDay).filter(DuelDay.week_id == week_id).count()
        if existing > 0:
            return session.query(DuelDay).filter(DuelDay.week_id == week_id).all()

        days = []
        for day_num in range(1, 7):  # Monday=1 through Saturday=6
            day_date = week.start_date + timedelta(days=day_num - 1)
            day = DuelDay(
                week_id=week_id,
                day_number=day_num,
                theme=themes.get(day_num, f"Day {day_num}"),
                date=day_date,
            )
            session.add(day)
            days.append(day)

        session.commit()
        for day in days:
            session.refresh(day)
        return days
    finally:
        if close_session:
            session.close()


def get_day(week_id: int, day_number: int, session: Session | None = None) -> DuelDay | None:
    """Get a specific day from a week."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        return (
            session.query(DuelDay)
            .filter(DuelDay.week_id == week_id, DuelDay.day_number == day_number)
            .first()
        )
    finally:
        if close_session:
            session.close()


def get_days_for_week(week_id: int, session: Session | None = None) -> list[DuelDay]:
    """Get all days for a week, ordered by day number."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        return (
            session.query(DuelDay)
            .filter(DuelDay.week_id == week_id)
            .order_by(DuelDay.day_number)
            .all()
        )
    finally:
        if close_session:
            session.close()


# ============ Daily Stats Recording ============


def record_daily_stats(
    day_id: int,
    player_id: int,
    points: float,
    session: Session | None = None,
) -> DuelDailyStats:
    """Record or update player stats for a single day."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        # Check if stats already exist for this player/day
        existing = (
            session.query(DuelDailyStats)
            .filter(
                DuelDailyStats.day_id == day_id,
                DuelDailyStats.player_id == player_id,
            )
            .first()
        )

        if existing:
            existing.points = points
            session.commit()
            session.refresh(existing)
            return existing
        else:
            stats = DuelDailyStats(
                day_id=day_id,
                player_id=player_id,
                points=points,
            )
            session.add(stats)
            session.commit()
            session.refresh(stats)
            return stats
    finally:
        if close_session:
            session.close()


def import_daily_csv(csv_content: str, session: Session | None = None) -> tuple[int, list[str]]:
    """Import daily stats from CSV content.

    CSV Format: Week,Day,PlayerName,Points
    - Week: week number (1, 2, 3...)
    - Day: day number (1-6, Mon-Sat) OR day name (Monday, Tuesday, etc.)
    - PlayerName: must match existing player
    - Points: score for that day

    Returns: (imported_count, list of errors)
    """
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    errors: list[str] = []
    records: list[dict] = []

    # Map day names to numbers
    day_name_map = {
        "monday": 1,
        "mon": 1,
        "1": 1,
        "tuesday": 2,
        "tue": 2,
        "2": 2,
        "wednesday": 3,
        "wed": 3,
        "3": 3,
        "thursday": 4,
        "thu": 4,
        "4": 4,
        "friday": 5,
        "fri": 5,
        "5": 5,
        "saturday": 6,
        "sat": 6,
        "6": 6,
    }

    try:
        reader = csv.DictReader(StringIO(csv_content))

        # Check required columns
        required_cols = {"Week", "Day", "PlayerName", "Points"}
        if reader.fieldnames is None:
            return 0, ["CSV has no headers"]

        missing_cols = required_cols - set(reader.fieldnames)
        if missing_cols:
            return 0, [f"Missing columns: {', '.join(missing_cols)}"]

        # First pass: validate all data
        player_name_cache: dict[str, int | None] = {}
        unknown_players: set[str] = set()
        day_cache: dict[tuple[int, int], int | None] = {}  # (week_num, day_num) -> day_id

        for row_num, row in enumerate(reader, start=2):
            try:
                week_number = int(row["Week"])
                day_input = row["Day"].strip().lower()
                player_name = row["PlayerName"].strip()
                points = float(row["Points"])

                # Parse day number
                day_number = day_name_map.get(day_input)
                if day_number is None:
                    errors.append(f"Row {row_num}: Invalid day '{row['Day']}'. Use 1-6 or Mon-Sat.")
                    continue

                if points < 0:
                    errors.append(f"Row {row_num}: Points cannot be negative")
                    continue

                # Check player exists (active players only)
                if player_name not in player_name_cache:
                    player = (
                        session.query(Player)
                        .filter(Player.name == player_name, Player.is_active == True)  # noqa: E712
                        .first()
                    )
                    player_name_cache[player_name] = player.id if player else None

                if player_name_cache[player_name] is None:
                    unknown_players.add(player_name)
                    continue

                # Check/get day
                cache_key = (week_number, day_number)
                if cache_key not in day_cache:
                    week = (
                        session.query(DuelWeek).filter(DuelWeek.week_number == week_number).first()
                    )
                    if not week:
                        errors.append(
                            f"Row {row_num}: Week {week_number} not found. Create the week first."
                        )
                        day_cache[cache_key] = None
                        continue

                    day = get_day(week.id, day_number, session=session)
                    if not day:
                        # Auto-create days for the week
                        create_days_for_week(week.id, session=session)
                        day = get_day(week.id, day_number, session=session)

                    day_cache[cache_key] = day.id if day else None

                if day_cache.get(cache_key) is None:
                    continue

                records.append(
                    {
                        "day_id": day_cache[cache_key],
                        "player_id": player_name_cache[player_name],
                        "points": points,
                    }
                )

            except ValueError as e:
                errors.append(f"Row {row_num}: Invalid data format - {e}")
                continue

        # Fail entire import if any unknown players
        if unknown_players:
            errors.insert(
                0,
                f"Unknown or inactive players (add/reactivate them first): "
                f"{', '.join(sorted(unknown_players))}",
            )
            return 0, errors

        # If we have parse errors, don't import
        if errors:
            return 0, errors

        # Second pass: import all records
        imported = 0
        for record in records:
            record_daily_stats(
                day_id=record["day_id"],
                player_id=record["player_id"],
                points=record["points"],
                session=session,
            )
            imported += 1

        return imported, []

    finally:
        if close_session:
            session.close()


def import_daily_simple_csv(
    week_id: int,
    day_number: int,
    csv_content: str,
    session: Session | None = None,
) -> tuple[int, list[str]]:
    """Import daily stats from simplified CSV for a specific week and day.

    CSV Format: PlayerName,Points
    - PlayerName: must match existing player
    - Points: score for that day

    Returns: (imported_count, list of errors)
    """
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    errors: list[str] = []
    records: list[dict] = []

    try:
        # Get or create the day
        week = session.query(DuelWeek).filter(DuelWeek.id == week_id).first()
        if not week:
            return 0, [f"Week with id {week_id} not found"]

        day = get_day(week_id, day_number, session=session)
        if not day:
            # Auto-create days for the week
            create_days_for_week(week_id, session=session)
            day = get_day(week_id, day_number, session=session)

        if not day:
            return 0, [f"Could not create day {day_number} for week {week_id}"]

        reader = csv.DictReader(StringIO(csv_content))

        # Check required columns (strip whitespace from headers)
        required_cols = {"PlayerName", "Points"}
        if reader.fieldnames is None:
            return 0, ["CSV has no headers"]

        # Strip whitespace from fieldnames to handle copy/paste issues
        fieldnames = [f.strip() for f in reader.fieldnames]
        missing_cols = required_cols - set(fieldnames)
        if missing_cols:
            return 0, [f"Missing columns: {', '.join(missing_cols)}"]

        # Create mapping from stripped names to original names
        original_names = {f.strip(): f for f in reader.fieldnames}

        # First pass: validate all data
        player_name_cache: dict[str, int | None] = {}
        unknown_players: set[str] = set()

        for row_num, row in enumerate(reader, start=2):
            try:
                player_name = row[original_names["PlayerName"]].strip()
                points = float(row[original_names["Points"]])

                if points < 0:
                    errors.append(f"Row {row_num}: Points cannot be negative")
                    continue

                # Check player exists (active players only)
                if player_name not in player_name_cache:
                    player = (
                        session.query(Player)
                        .filter(Player.name == player_name, Player.is_active == True)  # noqa: E712
                        .first()
                    )
                    player_name_cache[player_name] = player.id if player else None

                if player_name_cache[player_name] is None:
                    unknown_players.add(player_name)
                    continue

                records.append(
                    {
                        "player_id": player_name_cache[player_name],
                        "points": points,
                    }
                )

            except ValueError as e:
                errors.append(f"Row {row_num}: Invalid data format - {e}")
                continue

        # Fail entire import if any unknown players
        if unknown_players:
            errors.insert(
                0,
                f"Unknown or inactive players (add/reactivate them first): "
                f"{', '.join(sorted(unknown_players))}",
            )
            return 0, errors

        # If we have parse errors, don't import
        if errors:
            return 0, errors

        # Second pass: import all records
        imported = 0
        for record in records:
            record_daily_stats(
                day_id=day.id,
                player_id=record["player_id"],
                points=record["points"],
                session=session,
            )
            imported += 1

        return imported, []

    finally:
        if close_session:
            session.close()


def get_daily_stats_for_day(day_id: int, session: Session | None = None) -> list[dict]:
    """Get all stats for a day with player names for editing.

    Returns list of {player_id, player_name, points} sorted by player name.
    """
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        stats = session.query(DuelDailyStats).filter(DuelDailyStats.day_id == day_id).all()

        result = []
        for stat in stats:
            player = session.query(Player).filter(Player.id == stat.player_id).first()
            result.append(
                {
                    "player_id": stat.player_id,
                    "player_name": player.name if player else "Unknown",
                    "points": stat.points,
                }
            )

        # Sort by player name
        result.sort(key=lambda x: x["player_name"])
        return result
    finally:
        if close_session:
            session.close()


def delete_daily_stats_for_day(day_id: int, session: Session | None = None) -> int:
    """Delete all daily stats for a specific day.

    Returns count of records deleted.
    """
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        count = session.query(DuelDailyStats).filter(DuelDailyStats.day_id == day_id).delete()
        session.commit()
        return count
    finally:
        if close_session:
            session.close()


def parse_daily_simple_csv(
    week_id: int,
    day_number: int,
    csv_content: str,
    session: Session | None = None,
) -> tuple[list[dict], list[str]]:
    """Parse and validate CSV without importing.

    Returns (records, errors) where records is list of {player_id, player_name, points}.
    Use this for preview before actual import.
    """
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    errors: list[str] = []
    records: list[dict] = []

    try:
        # Get or create the day
        week = session.query(DuelWeek).filter(DuelWeek.id == week_id).first()
        if not week:
            return [], [f"Week with id {week_id} not found"]

        day = get_day(week_id, day_number, session=session)
        if not day:
            # Auto-create days for the week
            create_days_for_week(week_id, session=session)
            day = get_day(week_id, day_number, session=session)

        if not day:
            return [], [f"Could not create day {day_number} for week {week_id}"]

        reader = csv.DictReader(StringIO(csv_content))

        # Check required columns (strip whitespace from headers)
        required_cols = {"PlayerName", "Points"}
        if reader.fieldnames is None:
            return [], ["CSV has no headers"]

        # Strip whitespace from fieldnames to handle copy/paste issues
        fieldnames = [f.strip() for f in reader.fieldnames]
        missing_cols = required_cols - set(fieldnames)
        if missing_cols:
            return [], [f"Missing columns: {', '.join(missing_cols)}"]

        # Create mapping from stripped names to original names
        original_names = {f.strip(): f for f in reader.fieldnames}

        # Validate all data
        player_name_cache: dict[str, int | None] = {}
        unknown_players: set[str] = set()

        for row_num, row in enumerate(reader, start=2):
            try:
                player_name = row[original_names["PlayerName"]].strip()
                points = float(row[original_names["Points"]])

                if points < 0:
                    errors.append(f"Row {row_num}: Points cannot be negative")
                    continue

                # Check player exists (active players only)
                if player_name not in player_name_cache:
                    player = (
                        session.query(Player)
                        .filter(Player.name == player_name, Player.is_active == True)  # noqa: E712
                        .first()
                    )
                    player_name_cache[player_name] = player.id if player else None

                if player_name_cache[player_name] is None:
                    unknown_players.add(player_name)
                    continue

                records.append(
                    {
                        "player_id": player_name_cache[player_name],
                        "player_name": player_name,
                        "points": points,
                    }
                )

            except ValueError as e:
                errors.append(f"Row {row_num}: Invalid data format - {e}")
                continue

        # Report unknown players
        if unknown_players:
            errors.insert(
                0,
                f"Unknown or inactive players (add/reactivate them first): "
                f"{', '.join(sorted(unknown_players))}",
            )

        return records, errors

    finally:
        if close_session:
            session.close()


def aggregate_daily_to_weekly(week_id: int, session: Session | None = None) -> int:
    """Aggregate daily stats into weekly stats for a week.

    Sums points across all days and counts days participated.
    Returns number of players aggregated.
    """
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        days = get_days_for_week(week_id, session=session)
        if not days:
            return 0

        day_ids = [d.id for d in days]

        # Get all daily stats for this week
        daily_stats = session.query(DuelDailyStats).filter(DuelDailyStats.day_id.in_(day_ids)).all()

        # Aggregate by player
        player_totals: dict[int, dict] = {}
        for stat in daily_stats:
            if stat.player_id not in player_totals:
                player_totals[stat.player_id] = {"points": 0, "days": 0}
            player_totals[stat.player_id]["points"] += stat.points
            player_totals[stat.player_id]["days"] += 1

        # Update or create weekly stats
        for player_id, totals in player_totals.items():
            record_player_stats(
                week_id=week_id,
                player_id=player_id,
                raw_points=totals["points"],
                days_participated=totals["days"],
                session=session,
            )

        return len(player_totals)
    finally:
        if close_session:
            session.close()


# ============ Daily Reports ============


def get_daily_report(week_id: int, day_number: int, session: Session | None = None) -> dict:
    """Get a detailed report for a single day."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        day = get_day(week_id, day_number, session=session)
        if not day:
            return {"error": f"Day {day_number} not found for week {week_id}"}

        stats = session.query(DuelDailyStats).filter(DuelDailyStats.day_id == day.id).all()

        player_stats = []
        for stat in stats:
            player = session.query(Player).filter(Player.id == stat.player_id).first()
            player_stats.append(
                {
                    "player_id": stat.player_id,
                    "player_name": player.name if player else "Unknown",
                    "points": stat.points,
                }
            )

        # Sort by points descending
        player_stats.sort(key=lambda x: x["points"], reverse=True)

        week = session.query(DuelWeek).filter(DuelWeek.id == week_id).first()

        return {
            "week_id": week_id,
            "week_number": week.week_number if week else 0,
            "day_number": day.day_number,
            "theme": day.theme,
            "date": day.date,
            "player_count": len(player_stats),
            "total_points": sum(s["points"] for s in player_stats),
            "players": player_stats,
        }
    finally:
        if close_session:
            session.close()


def get_week_daily_breakdown(week_id: int, session: Session | None = None) -> dict:
    """Get a breakdown of all days in a week with player performance per day."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        week = session.query(DuelWeek).filter(DuelWeek.id == week_id).first()
        if not week:
            return {"error": f"Week {week_id} not found"}

        days = get_days_for_week(week_id, session=session)
        if not days:
            return {
                "week_id": week_id,
                "week_number": week.week_number,
                "days": [],
                "players": [],
            }

        # Get all daily stats for this week
        day_ids = [d.id for d in days]
        all_stats = session.query(DuelDailyStats).filter(DuelDailyStats.day_id.in_(day_ids)).all()

        # Build day info
        day_info = []
        for day in days:
            day_stats = [s for s in all_stats if s.day_id == day.id]
            day_info.append(
                {
                    "day_number": day.day_number,
                    "theme": day.theme,
                    "date": day.date,
                    "total_points": sum(s.points for s in day_stats),
                    "participant_count": len(day_stats),
                }
            )

        # Build player breakdown (player -> day -> points)
        player_ids = set(s.player_id for s in all_stats)
        player_breakdown = []

        for player_id in player_ids:
            player = session.query(Player).filter(Player.id == player_id).first()
            player_data = {
                "player_id": player_id,
                "player_name": player.name if player else "Unknown",
                "days": {},
                "total": 0,
                "days_participated": 0,
            }

            for day in days:
                stat = next(
                    (s for s in all_stats if s.day_id == day.id and s.player_id == player_id),
                    None,
                )
                if stat:
                    player_data["days"][day.day_number] = stat.points
                    player_data["total"] += stat.points
                    player_data["days_participated"] += 1
                else:
                    player_data["days"][day.day_number] = None

            player_breakdown.append(player_data)

        # Sort by total points
        player_breakdown.sort(key=lambda x: x["total"], reverse=True)

        return {
            "week_id": week_id,
            "week_number": week.week_number,
            "opponent_name": week.opponent_name,
            "result": week.result,
            "days": day_info,
            "players": player_breakdown,
        }
    finally:
        if close_session:
            session.close()


def get_player_daily_averages(
    player_id: int, weeks: int = ROLLING_WEEKS, session: Session | None = None
) -> dict:
    """Get a player's average performance by day theme over recent weeks."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        recent_weeks = get_recent_weeks(count=weeks, session=session)
        if not recent_weeks:
            return {"error": "No weeks found"}

        player = session.query(Player).filter(Player.id == player_id).first()
        if not player:
            return {"error": f"Player {player_id} not found"}

        # Get all days for recent weeks
        week_ids = [w.id for w in recent_weeks]
        days = session.query(DuelDay).filter(DuelDay.week_id.in_(week_ids)).all()

        day_ids = [d.id for d in days]

        # Get player's daily stats
        stats = (
            session.query(DuelDailyStats)
            .filter(
                DuelDailyStats.player_id == player_id,
                DuelDailyStats.day_id.in_(day_ids),
            )
            .all()
        )

        # Group by day number/theme
        day_totals: dict[int, list[float]] = {i: [] for i in range(1, 7)}
        for stat in stats:
            day = next((d for d in days if d.id == stat.day_id), None)
            if day:
                day_totals[day.day_number].append(stat.points)

        # Calculate averages
        day_averages = {}
        for day_num in range(1, 7):
            scores = day_totals[day_num]
            theme = DUEL_DAY_THEMES.get(day_num, f"Day {day_num}")
            day_averages[day_num] = {
                "theme": theme,
                "avg_points": sum(scores) / len(scores) if scores else 0,
                "times_participated": len(scores),
                "total_opportunities": len(recent_weeks),
            }

        return {
            "player_id": player_id,
            "player_name": player.name,
            "weeks_analyzed": len(recent_weeks),
            "day_averages": day_averages,
        }
    finally:
        if close_session:
            session.close()


# ============ Stats Recording ============


def record_player_stats(
    week_id: int,
    player_id: int,
    raw_points: float,
    days_participated: int,
    session: Session | None = None,
) -> DuelWeeklyStats:
    """Record or update player stats for a week."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        # Check if stats already exist for this player/week
        existing = (
            session.query(DuelWeeklyStats)
            .filter(
                DuelWeeklyStats.week_id == week_id,
                DuelWeeklyStats.player_id == player_id,
            )
            .first()
        )

        normalized = calculate_normalized_points(raw_points, days_participated)

        if existing:
            existing.raw_points = raw_points
            existing.days_participated = days_participated
            existing.normalized_points = normalized
            session.commit()
            session.refresh(existing)
            return existing
        else:
            stats = DuelWeeklyStats(
                week_id=week_id,
                player_id=player_id,
                raw_points=raw_points,
                days_participated=days_participated,
                normalized_points=normalized,
            )
            session.add(stats)
            session.commit()
            session.refresh(stats)
            return stats
    finally:
        if close_session:
            session.close()


def import_weekly_csv(csv_content: str, session: Session | None = None) -> tuple[int, list[str]]:
    """Import weekly stats from CSV content.

    CSV Format: Week,PlayerName,Points,DaysParticipated

    Returns: (imported_count, list of errors)

    Note: Validates ALL player names exist first; fails entire import if any unknown.
    """
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    errors: list[str] = []
    records: list[dict] = []

    try:
        reader = csv.DictReader(StringIO(csv_content))

        # Check required columns
        required_cols = {"Week", "PlayerName", "Points", "DaysParticipated"}
        if reader.fieldnames is None:
            return 0, ["CSV has no headers"]

        missing_cols = required_cols - set(reader.fieldnames)
        if missing_cols:
            return 0, [f"Missing columns: {', '.join(missing_cols)}"]

        # First pass: validate all data and player names
        player_name_cache: dict[str, int | None] = {}
        unknown_players: set[str] = set()
        week_cache: dict[int, int | None] = {}  # week_number -> week_id

        for row_num, row in enumerate(reader, start=2):
            try:
                week_number = int(row["Week"])
                player_name = row["PlayerName"].strip()
                points = float(row["Points"])
                days = int(row["DaysParticipated"])

                if days < 0 or days > 7:
                    errors.append(f"Row {row_num}: DaysParticipated must be 0-7")
                    continue

                if points < 0:
                    errors.append(f"Row {row_num}: Points cannot be negative")
                    continue

                # Check player exists (active players only)
                if player_name not in player_name_cache:
                    player = (
                        session.query(Player)
                        .filter(Player.name == player_name, Player.is_active == True)  # noqa: E712
                        .first()
                    )
                    player_name_cache[player_name] = player.id if player else None

                if player_name_cache[player_name] is None:
                    unknown_players.add(player_name)
                    continue

                # Check/create week
                if week_number not in week_cache:
                    week = (
                        session.query(DuelWeek).filter(DuelWeek.week_number == week_number).first()
                    )
                    week_cache[week_number] = week.id if week else None

                if week_cache[week_number] is None:
                    errors.append(
                        f"Row {row_num}: Week {week_number} not found. Create the week first."
                    )
                    continue

                records.append(
                    {
                        "week_id": week_cache[week_number],
                        "player_id": player_name_cache[player_name],
                        "raw_points": points,
                        "days_participated": days,
                    }
                )

            except ValueError as e:
                errors.append(f"Row {row_num}: Invalid data format - {e}")
                continue

        # Fail entire import if any unknown players
        if unknown_players:
            errors.insert(
                0,
                f"Unknown or inactive players (add/reactivate them first): "
                f"{', '.join(sorted(unknown_players))}",
            )
            return 0, errors

        # If we have parse errors, don't import
        if errors:
            return 0, errors

        # Second pass: import all records
        imported = 0
        for record in records:
            record_player_stats(
                week_id=record["week_id"],
                player_id=record["player_id"],
                raw_points=record["raw_points"],
                days_participated=record["days_participated"],
                session=session,
            )
            imported += 1

        return imported, []

    finally:
        if close_session:
            session.close()


# ============ Report Generation ============


def get_weekly_report(week_id: int, session: Session | None = None) -> dict:
    """Get a detailed report for a single week."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        week = session.query(DuelWeek).filter(DuelWeek.id == week_id).first()
        if not week:
            return {"error": f"Week {week_id} not found"}

        stats = session.query(DuelWeeklyStats).filter(DuelWeeklyStats.week_id == week_id).all()

        player_stats = []
        for stat in stats:
            player = session.query(Player).filter(Player.id == stat.player_id).first()
            player_stats.append(
                {
                    "player_id": stat.player_id,
                    "player_name": player.name if player else "Unknown",
                    "raw_points": stat.raw_points,
                    "days_participated": stat.days_participated,
                    "normalized_points": stat.normalized_points,
                }
            )

        # Sort by normalized points descending
        player_stats.sort(key=lambda x: x["normalized_points"], reverse=True)

        return {
            "week_id": week.id,
            "week_number": week.week_number,
            "start_date": week.start_date,
            "opponent_name": week.opponent_name,
            "result": week.result,
            "player_count": len(player_stats),
            "players": player_stats,
        }
    finally:
        if close_session:
            session.close()


def get_rolling_report(
    weeks: int = ROLLING_WEEKS, active_only: bool = True, session: Session | None = None
) -> list[dict]:
    """Get rolling report with averages, reliability, and tier for all players."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        recent_weeks = get_recent_weeks(count=weeks, session=session)
        if not recent_weeks:
            return []

        week_ids = [w.id for w in recent_weeks]
        total_weeks = len(week_ids)

        # Get players (active only by default)
        query = session.query(Player)
        if active_only:
            query = query.filter(Player.is_active == True)  # noqa: E712
        players = query.all()

        result = []
        for player in players:
            # Get stats for this player in recent weeks
            stats = (
                session.query(DuelWeeklyStats)
                .filter(
                    DuelWeeklyStats.player_id == player.id,
                    DuelWeeklyStats.week_id.in_(week_ids),
                )
                .all()
            )

            weeks_participated = len(stats)
            if weeks_participated == 0:
                # Player didn't participate in any recent weeks
                result.append(
                    {
                        "player_id": player.id,
                        "player_name": player.name,
                        "weeks_participated": 0,
                        "total_weeks": total_weeks,
                        "avg_raw_points": 0.0,
                        "avg_normalized_points": 0.0,
                        "reliability": 0.0,
                        "tier": "Probation",
                    }
                )
                continue

            avg_raw = sum(s.raw_points for s in stats) / weeks_participated
            avg_normalized = sum(s.normalized_points for s in stats) / weeks_participated
            reliability = calculate_reliability(weeks_participated, total_weeks)
            tier = assign_tier(avg_normalized, reliability)

            result.append(
                {
                    "player_id": player.id,
                    "player_name": player.name,
                    "weeks_participated": weeks_participated,
                    "total_weeks": total_weeks,
                    "avg_raw_points": round(avg_raw, 1),
                    "avg_normalized_points": round(avg_normalized, 1),
                    "reliability": round(reliability, 2),
                    "tier": tier,
                }
            )

        # Sort by tier priority, then by avg_normalized descending
        tier_order = {"Core": 0, "Strong": 1, "Standard": 2, "Probation": 3}
        result.sort(key=lambda x: (tier_order.get(x["tier"], 99), -x["avg_normalized_points"]))

        return result
    finally:
        if close_session:
            session.close()


def get_text_summary(week_id: int | None = None, session: Session | None = None) -> str:
    """Generate a formatted text summary for a week."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        if week_id is None:
            week = get_latest_week(session=session)
            if not week:
                return "No duel weeks found."
            week_id = week.id

        report = get_weekly_report(week_id, session=session)
        if "error" in report:
            return report["error"]

        lines = []

        # Header
        opponent = report["opponent_name"] or "Unknown"
        lines.append(f"=== Week {report['week_number']} vs {opponent} ===")

        # Result
        result = report["result"]
        if result:
            lines.append(f"Result: {result.upper()}")
        else:
            lines.append("Result: Pending")

        lines.append("")

        # Top 5 contributors
        players = report["players"]
        lines.append("Top 5 Contributors:")
        for i, p in enumerate(players[:5], 1):
            lines.append(
                f"{i}. {p['player_name']} - {p['raw_points']:.0f} pts "
                f"({p['normalized_points']:.1f} norm)"
            )

        lines.append("")

        # Under minimum threshold (< 50 normalized)
        under_minimum = [p for p in players if p["normalized_points"] < 50]
        if under_minimum:
            lines.append("Under Minimum (< 50 norm):")
            for p in under_minimum:
                lines.append(f"- {p['player_name']} ({p['normalized_points']:.1f} norm)")
        else:
            lines.append("No players under minimum threshold.")

        return "\n".join(lines)
    finally:
        if close_session:
            session.close()


# ============ Archiving ============


def clear_all_duel_data(session: Session | None = None) -> dict[str, int]:
    """Clear all Duel VS data from the database.

    Returns dict with counts of deleted records per table.
    """
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        counts = {}
        # Delete in order respecting foreign key constraints
        counts["daily_stats"] = session.query(DuelDailyStats).delete()
        counts["days"] = session.query(DuelDay).delete()
        counts["weekly_stats"] = session.query(DuelWeeklyStats).delete()
        counts["cycle_stats"] = session.query(DuelCycleStats).delete()
        counts["weeks"] = session.query(DuelWeek).delete()
        counts["cycles"] = session.query(DuelCycle).delete()
        session.commit()
        return counts
    finally:
        if close_session:
            session.close()


def archive_old_weeks(older_than_weeks: int = ARCHIVE_WEEKS, session: Session | None = None) -> int:
    """Archive (delete) weeks older than the specified threshold.

    Returns the number of archived weeks.
    """
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        # Get all weeks ordered by week_number descending
        all_weeks = session.query(DuelWeek).order_by(desc(DuelWeek.week_number)).all()

        if len(all_weeks) <= older_than_weeks:
            return 0

        # Delete weeks beyond the threshold
        weeks_to_delete = all_weeks[older_than_weeks:]
        archived_count = len(weeks_to_delete)

        for week in weeks_to_delete:
            session.delete(week)

        session.commit()
        return archived_count
    finally:
        if close_session:
            session.close()


# ============ Cycle Management ============


def create_cycle(
    cycle_number: int,
    start_date: datetime,
    name: str | None = None,
    session: Session | None = None,
) -> DuelCycle:
    """Create a new duel cycle."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        cycle = DuelCycle(
            cycle_number=cycle_number,
            start_date=start_date,
            name=name,
        )
        session.add(cycle)
        session.commit()
        session.refresh(cycle)
        return cycle
    finally:
        if close_session:
            session.close()


def get_all_cycles(session: Session | None = None) -> list[DuelCycle]:
    """Get all duel cycles ordered by cycle number descending."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        return session.query(DuelCycle).order_by(desc(DuelCycle.cycle_number)).all()
    finally:
        if close_session:
            session.close()


def get_cycle(cycle_id: int, session: Session | None = None) -> DuelCycle | None:
    """Get a duel cycle by ID."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        return session.query(DuelCycle).filter(DuelCycle.id == cycle_id).first()
    finally:
        if close_session:
            session.close()


def assign_week_to_cycle(
    week_id: int,
    cycle_id: int | None,
    session: Session | None = None,
) -> DuelWeek:
    """Assign a week to a cycle. Pass cycle_id=None to unassign."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        week = session.query(DuelWeek).filter(DuelWeek.id == week_id).first()
        if not week:
            raise ValueError(f"Week with id {week_id} not found")

        week.cycle_id = cycle_id
        session.commit()
        session.refresh(week)
        return week
    finally:
        if close_session:
            session.close()


def aggregate_cycle_stats(cycle_id: int, session: Session | None = None) -> int:
    """Calculate and store aggregate stats for a cycle from weekly stats.

    Returns number of players aggregated.
    """
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        cycle = session.query(DuelCycle).filter(DuelCycle.id == cycle_id).first()
        if not cycle:
            raise ValueError(f"Cycle with id {cycle_id} not found")

        # Get all weeks in this cycle
        weeks = session.query(DuelWeek).filter(DuelWeek.cycle_id == cycle_id).all()
        if not weeks:
            return 0

        week_ids = [w.id for w in weeks]

        # Get all weekly stats for these weeks
        weekly_stats = (
            session.query(DuelWeeklyStats).filter(DuelWeeklyStats.week_id.in_(week_ids)).all()
        )

        # Aggregate by player
        player_totals: dict[int, dict] = {}
        for stat in weekly_stats:
            if stat.player_id not in player_totals:
                player_totals[stat.player_id] = {"points": 0.0, "weeks": 0}
            player_totals[stat.player_id]["points"] += stat.raw_points
            player_totals[stat.player_id]["weeks"] += 1

        # Clear existing cycle stats
        session.query(DuelCycleStats).filter(DuelCycleStats.cycle_id == cycle_id).delete()

        # Create new cycle stats
        for player_id, totals in player_totals.items():
            avg_weekly = totals["points"] / totals["weeks"] if totals["weeks"] > 0 else 0
            cycle_stats = DuelCycleStats(
                cycle_id=cycle_id,
                player_id=player_id,
                total_points=totals["points"],
                weeks_participated=totals["weeks"],
                avg_weekly_points=avg_weekly,
            )
            session.add(cycle_stats)

        session.commit()
        return len(player_totals)
    finally:
        if close_session:
            session.close()


def get_cycle_days_with_data_count(cycle_id: int, session: Session | None = None) -> int:
    """Count DuelDay records in a cycle that have at least one DuelDailyStats entry."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        weeks = (
            session.query(DuelWeek)
            .filter(DuelWeek.cycle_id == cycle_id)
            .all()
        )
        if not weeks:
            return 0

        week_ids = [w.id for w in weeks]
        days_with_data = (
            session.query(DuelDay)
            .filter(DuelDay.week_id.in_(week_ids))
            .filter(DuelDay.daily_stats.any())
            .count()
        )
        return days_with_data
    finally:
        if close_session:
            session.close()


def get_cycle_report(cycle_id: int, session: Session | None = None) -> dict:
    """Get a detailed report for a cycle including player performance."""
    close_session = session is None
    if session is None:
        init_database()
        session = get_session()

    try:
        cycle = session.query(DuelCycle).filter(DuelCycle.id == cycle_id).first()
        if not cycle:
            return {"error": f"Cycle {cycle_id} not found"}

        # Get weeks in this cycle
        weeks = (
            session.query(DuelWeek)
            .filter(DuelWeek.cycle_id == cycle_id)
            .order_by(DuelWeek.week_number)
            .all()
        )

        week_info = [
            {
                "week_id": w.id,
                "week_number": w.week_number,
                "opponent_name": w.opponent_name,
                "result": w.result,
            }
            for w in weeks
        ]

        # Get cycle stats
        stats = session.query(DuelCycleStats).filter(DuelCycleStats.cycle_id == cycle_id).all()

        player_stats = []
        for stat in stats:
            player = session.query(Player).filter(Player.id == stat.player_id).first()
            player_stats.append(
                {
                    "player_id": stat.player_id,
                    "player_name": player.name if player else "Unknown",
                    "total_points": stat.total_points,
                    "weeks_participated": stat.weeks_participated,
                    "avg_weekly_points": round(stat.avg_weekly_points, 1),
                }
            )

        # Sort by total points descending
        player_stats.sort(key=lambda x: x["total_points"], reverse=True)

        # Calculate cycle totals
        wins = sum(1 for w in weeks if w.result == "win")
        losses = sum(1 for w in weeks if w.result == "loss")

        return {
            "cycle_id": cycle.id,
            "cycle_number": cycle.cycle_number,
            "name": cycle.name,
            "start_date": cycle.start_date,
            "weeks": week_info,
            "week_count": len(weeks),
            "wins": wins,
            "losses": losses,
            "player_count": len(player_stats),
            "players": player_stats,
        }
    finally:
        if close_session:
            session.close()
