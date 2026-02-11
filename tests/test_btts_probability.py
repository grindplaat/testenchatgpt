from app.model.btts_probability import match_btts_probability, team_btts_tendency


def test_team_btts_tendency_balanced_sample():
    history = [
        {"scored": True, "conceded": True},
        {"scored": True, "conceded": False},
        {"scored": False, "conceded": True},
        {"scored": True, "conceded": True},
    ]
    tendency = team_btts_tendency(history, last_n=4)
    assert 0.70 < tendency < 0.90


def test_match_btts_probability_average_of_two_teams():
    high = [{"scored": True, "conceded": True}] * 8
    low = [{"scored": False, "conceded": False}] * 8
    prob = match_btts_probability(high, low, last_n=8)
    assert prob == 0.5
