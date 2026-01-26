"""Tests for data module."""


from src.data.models import Alliance, Player, WarResult


def test_player_model():
    """Test Player model creation."""
    player = Player(name="TestPlayer", power=1000, level=10)
    assert player.name == "TestPlayer"
    assert player.power == 1000
    assert player.level == 10


def test_alliance_model():
    """Test Alliance model creation."""
    alliance = Alliance(name="Test Alliance", tag="TST")
    assert alliance.name == "Test Alliance"
    assert alliance.tag == "TST"


def test_war_result_model():
    """Test WarResult model creation."""
    from datetime import datetime

    war = WarResult(
        war_date=datetime.now(),
        alliance_id=1,
        opponent_name="Enemy",
        our_score=100.0,
        opponent_score=50.0,
        result="win",
    )
    assert war.result == "win"
    assert war.our_score == 100.0
