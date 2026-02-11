from __future__ import annotations


def _recent_sample(history: list[dict], last_n: int = 8) -> list[dict]:
    """Return at most the most recent matches, preserving input order."""
    return history[:last_n]


def _average(values: list[float]) -> float:
    """Return the arithmetic mean, or 0.0 when no values are available."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def _btts_rate(history: list[dict], last_n: int = 8) -> float:
    """Return the BTTS rate over the recent sample, or 0.0 when history is empty."""
    sample = _recent_sample(history, last_n=last_n)
    if not sample:
        return 0.0

    btts_count = sum(
        1
        for match in sample
        if match.get("goals_scored", 0) > 0 and match.get("goals_conceded", 0) > 0
    )
    return btts_count / len(sample)


def extract_btts_features(home_history: list[dict], away_history: list[dict]) -> list[float]:
    """
    Extract a fixed-order BTTS feature vector from both teams' recent histories.

    Feature order:
    1. home_attack_strength: average goals scored by home team in last 8 matches.
    2. home_defensive_weakness: average goals conceded by home team in last 8 matches.
    3. away_attack_strength: average goals scored by away team in last 8 matches.
    4. away_defensive_weakness: average goals conceded by away team in last 8 matches.
    5. combined_btts_trend: average of each team's BTTS rate in last 8 matches,
       where BTTS means both goals_scored > 0 and goals_conceded > 0.

    Missing or empty history safely maps to 0.0 for the affected metric.
    """
    home_sample = _recent_sample(home_history, last_n=8)
    away_sample = _recent_sample(away_history, last_n=8)

    home_attack_strength = _average([m.get("goals_scored", 0) for m in home_sample])
    home_defensive_weakness = _average([m.get("goals_conceded", 0) for m in home_sample])

    away_attack_strength = _average([m.get("goals_scored", 0) for m in away_sample])
    away_defensive_weakness = _average([m.get("goals_conceded", 0) for m in away_sample])

    combined_btts_trend = (_btts_rate(home_history, last_n=8) + _btts_rate(away_history, last_n=8)) / 2

    return [
        home_attack_strength,
        home_defensive_weakness,
        away_attack_strength,
        away_defensive_weakness,
        combined_btts_trend,
    ]
