from __future__ import annotations

import math


def team_btts_tendency(history: list[dict[str, bool]], last_n: int = 8) -> float:
    """
    Estimate a team's tendency for BTTS-style games from recent matches.

    Uses the geometric mean of:
    - rate of matches in which the team scored
    - rate of matches in which the team conceded
    """
    if not history:
        return 0.5

    sample = history[:last_n]
    total = len(sample)
    scored_rate = sum(1 for m in sample if m.get("scored", False)) / total
    conceded_rate = sum(1 for m in sample if m.get("conceded", False)) / total
    return math.sqrt(scored_rate * conceded_rate)


def match_btts_probability(
    home_history: list[dict[str, bool]],
    away_history: list[dict[str, bool]],
    last_n: int = 8,
) -> float:
    """Average both teams' BTTS tendencies as a match-level model probability."""
    home_tendency = team_btts_tendency(home_history, last_n=last_n)
    away_tendency = team_btts_tendency(away_history, last_n=last_n)
    return (home_tendency + away_tendency) / 2
