"""Example usage of the Duel VS tracking system with sample data."""

from datetime import datetime, timedelta

from src.data.duel_tracker import (
    TIER_THRESHOLDS,
    archive_old_weeks,
    create_week,
    get_rolling_report,
    get_text_summary,
    get_weekly_report,
    import_weekly_csv,
    set_week_result,
)
from src.data.models import Player
from src.data.storage import get_session, init_database


def setup_sample_players(session) -> dict[str, int]:
    """Create sample players and return name->id mapping."""
    players = [
        {"name": "DragonSlayer", "rank": 5, "power": 180.5, "level": 45},
        {"name": "IronFist", "rank": 5, "power": 165.2, "level": 42},
        {"name": "ShadowBlade", "rank": 4, "power": 145.0, "level": 40},
        {"name": "ThunderBolt", "rank": 4, "power": 138.7, "level": 38},
        {"name": "FrostMage", "rank": 4, "power": 132.1, "level": 37},
        {"name": "StormRider", "rank": 3, "power": 120.5, "level": 35},
        {"name": "BlazeFury", "rank": 3, "power": 115.0, "level": 34},
        {"name": "NightHawk", "rank": 3, "power": 105.2, "level": 32},
        {"name": "SilverWolf", "rank": 2, "power": 95.8, "level": 30},
        {"name": "CrimsonTide", "rank": 2, "power": 88.3, "level": 28},
    ]

    player_ids = {}
    for p in players:
        existing = session.query(Player).filter(Player.name == p["name"]).first()
        if existing:
            player_ids[p["name"]] = existing.id
        else:
            player = Player(**p)
            session.add(player)
            session.flush()
            player_ids[p["name"]] = player.id

    session.commit()
    return player_ids


def generate_sample_csv(weeks: int = 4) -> str:
    """Generate sample CSV data for multiple weeks."""
    # Simulated performance data (some players are consistent, some aren't)
    player_data = {
        "DragonSlayer": {"base_pts": 1200, "variance": 100, "days_range": (6, 7)},
        "IronFist": {"base_pts": 1100, "variance": 150, "days_range": (5, 7)},
        "ShadowBlade": {"base_pts": 900, "variance": 200, "days_range": (5, 7)},
        "ThunderBolt": {"base_pts": 850, "variance": 100, "days_range": (4, 7)},
        "FrostMage": {"base_pts": 800, "variance": 150, "days_range": (4, 6)},
        "StormRider": {"base_pts": 650, "variance": 200, "days_range": (3, 6)},
        "BlazeFury": {"base_pts": 600, "variance": 100, "days_range": (4, 7)},
        "NightHawk": {"base_pts": 500, "variance": 150, "days_range": (2, 5)},
        "SilverWolf": {"base_pts": 400, "variance": 100, "days_range": (3, 5)},
        "CrimsonTide": {"base_pts": 350, "variance": 200, "days_range": (1, 4)},
    }

    import random

    random.seed(42)  # Reproducible results

    lines = ["Week,PlayerName,Points,DaysParticipated"]
    for week in range(1, weeks + 1):
        for name, data in player_data.items():
            # Skip some players some weeks to simulate absences
            if random.random() < 0.1:  # 10% absence rate
                continue

            pts = data["base_pts"] + random.randint(-data["variance"], data["variance"])
            days = random.randint(*data["days_range"])
            lines.append(f"{week},{name},{pts},{days}")

    return "\n".join(lines)


def main():
    """Run the example demonstration."""
    print("=" * 60)
    print("DUEL VS TRACKING SYSTEM - EXAMPLE USAGE")
    print("=" * 60)

    # Initialize database
    init_database()
    session = get_session()

    try:
        # 1. Setup sample players
        print("\n1. Creating sample players...")
        player_ids = setup_sample_players(session)
        print(f"   Created/found {len(player_ids)} players")

        # 2. Create weeks
        print("\n2. Creating duel weeks...")
        opponents = ["Alpha Legion", "Dark Knights", "Storm Riders", "Iron Wolves"]
        results = ["win", "loss", "win", "win"]
        totals = [8500, 7200, 9100, 8800]

        base_date = datetime.now() - timedelta(weeks=4)
        week_ids = []

        for i, (opp, res, total) in enumerate(zip(opponents, results, totals), start=1):
            week = create_week(
                week_number=i,
                start_date=base_date + timedelta(weeks=i - 1),
                opponent_name=opp,
                session=session,
            )
            set_week_result(week.id, res, total, session=session)
            week_ids.append(week.id)
            print(f"   Week {i}: vs {opp} - {res.upper()} ({total:,} pts)")

        # 3. Import CSV data
        print("\n3. Importing weekly stats from CSV...")
        csv_data = generate_sample_csv(weeks=4)
        print("   Sample CSV preview:")
        for line in csv_data.split("\n")[:5]:
            print(f"   {line}")
        print("   ...")

        imported, errors = import_weekly_csv(csv_data, session=session)
        if errors:
            print(f"   Errors: {errors}")
        else:
            print(f"   Successfully imported {imported} records")

        # 4. Weekly Report
        print("\n4. WEEKLY REPORT (Week 4)")
        print("-" * 40)
        report = get_weekly_report(week_ids[3], session=session)
        print(f"   Week {report['week_number']} vs {report['opponent_name']}")
        print(f"   Result: {report['result'].upper()}")
        print(f"   Alliance Total: {report['alliance_total']:,} pts")
        print(f"   Participants: {report['player_count']}")
        print("\n   Player Rankings:")
        for i, p in enumerate(report["players"][:5], 1):
            print(
                f"   {i}. {p['player_name']:15} {p['raw_points']:>6.0f} pts "
                f"({p['days_participated']} days) = {p['normalized_points']:.1f} norm"
            )

        # 5. Rolling Report
        print("\n5. ROLLING 4-WEEK REPORT")
        print("-" * 40)
        rolling = get_rolling_report(weeks=4, session=session)
        print(f"   {'Player':<15} {'Weeks':<6} {'Avg Pts':<8} {'Avg Norm':<9} {'Rel%':<6} Tier")
        print("   " + "-" * 55)
        for p in rolling:
            print(
                f"   {p['player_name']:<15} {p['weeks_participated']}/{p['total_weeks']:<4} "
                f"{p['avg_raw_points']:>7.0f}  {p['avg_normalized_points']:>8.1f}  "
                f"{p['reliability'] * 100:>5.0f}%  {p['tier']}"
            )

        # 6. Text Summary
        print("\n6. TEXT SUMMARY (Latest Week)")
        print("-" * 40)
        summary = get_text_summary(session=session)
        for line in summary.split("\n"):
            print(f"   {line}")

        # 7. Show tier thresholds
        print("\n7. CURRENT TIER THRESHOLDS")
        print("-" * 40)
        for tier, thresholds in TIER_THRESHOLDS.items():
            print(
                f"   {tier:<12} Reliability >= {thresholds['min_reliability'] * 100:.0f}%, "
                f"Avg Norm >= {thresholds['min_avg_normalized']}"
            )

        # 8. Archive demo
        print("\n8. ARCHIVE FEATURE")
        print("-" * 40)
        print(f"   Current threshold: {8} weeks")
        print("   To archive old weeks: archive_old_weeks(older_than_weeks=8)")
        archived = archive_old_weeks(older_than_weeks=8, session=session)
        print(f"   Archived {archived} weeks (none old enough yet)")

    finally:
        session.close()

    print("\n" + "=" * 60)
    print("EXAMPLE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
