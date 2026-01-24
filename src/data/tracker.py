"""Data collection and tracking logic."""

from datetime import datetime

from .models import Alliance, Player, WarResult
from .storage import get_session


def add_player(name: str, power: int = 0, level: int = 1, alliance_id: int | None = None) -> Player:
    """Add a new player to the database."""
    with get_session() as session:
        player = Player(name=name, power=power, level=level, alliance_id=alliance_id)
        session.add(player)
        session.commit()
        session.refresh(player)
        return player


def update_player_stats(player_id: int, power: int | None = None, level: int | None = None):
    """Update a player's stats."""
    with get_session() as session:
        player = session.get(Player, player_id)
        if player:
            if power is not None:
                player.power = power
            if level is not None:
                player.level = level
            session.commit()


def add_alliance(name: str, tag: str | None = None) -> Alliance:
    """Add a new alliance to the database."""
    with get_session() as session:
        alliance = Alliance(name=name, tag=tag)
        session.add(alliance)
        session.commit()
        session.refresh(alliance)
        return alliance


def record_war_result(
    alliance_id: int,
    opponent_name: str,
    our_score: float,
    opponent_score: float,
    war_date: datetime | None = None,
) -> WarResult:
    """Record a war result."""
    if war_date is None:
        war_date = datetime.now()

    if our_score > opponent_score:
        result = "win"
    elif our_score < opponent_score:
        result = "loss"
    else:
        result = "draw"

    with get_session() as session:
        war_result = WarResult(
            war_date=war_date,
            alliance_id=alliance_id,
            opponent_name=opponent_name,
            our_score=our_score,
            opponent_score=opponent_score,
            result=result,
        )
        session.add(war_result)
        session.commit()
        session.refresh(war_result)
        return war_result


def get_war_stats(alliance_id: int) -> dict:
    """Get war statistics for an alliance."""
    with get_session() as session:
        wars = session.query(WarResult).filter(WarResult.alliance_id == alliance_id).all()

        total = len(wars)
        wins = sum(1 for w in wars if w.result == "win")
        losses = sum(1 for w in wars if w.result == "loss")
        draws = sum(1 for w in wars if w.result == "draw")

        return {
            "total": total,
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "win_rate": wins / total if total > 0 else 0,
        }
