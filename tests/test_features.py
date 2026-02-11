from app.model.features import extract_btts_features


def test_extract_btts_features_returns_five_values():
    features = extract_btts_features(home_history=[], away_history=[])
    assert len(features) == 5


def test_extract_btts_features_computes_expected_metrics():
    home_history = [
        {"goals_scored": 2, "goals_conceded": 1},
        {"goals_scored": 0, "goals_conceded": 2},
    ]
    away_history = [
        {"goals_scored": 1, "goals_conceded": 1},
        {"goals_scored": 3, "goals_conceded": 0},
    ]

    features = extract_btts_features(home_history=home_history, away_history=away_history)

    assert features == [1.0, 1.5, 2.0, 0.5, 0.5]
