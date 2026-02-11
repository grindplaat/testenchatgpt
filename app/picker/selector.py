from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from app.model.btts_probability import match_btts_probability


@dataclass
class Pick:
    match_id: str
    date: str
    league: str
    home_team: str
    away_team: str
    odds: float
    implied_prob: float
    model_prob: float
    value: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_ranked_picks(
    fixtures: list[dict[str, Any]],
    odds_by_match_id: dict[str, float],
    team_histories: dict[str, list[dict[str, bool]]],
) -> list[Pick]:
    picks: list[Pick] = []

    for fixture in fixtures:
        match_id = fixture["match_id"]
        if match_id not in odds_by_match_id:
            continue

        odds = float(odds_by_match_id[match_id])
        if not (1.50 <= odds <= 2.40):
            continue

        home = fixture["home_team"]
        away = fixture["away_team"]

        home_history = team_histories.get(home, [])
        away_history = team_histories.get(away, [])
        model_prob = match_btts_probability(home_history, away_history, last_n=8)
        implied_prob = 1 / odds
        value = model_prob - implied_prob

        picks.append(
            Pick(
                match_id=match_id,
                date=fixture["date"],
                league=fixture["league"],
                home_team=home,
                away_team=away,
                odds=round(odds, 2),
                implied_prob=round(implied_prob, 4),
                model_prob=round(model_prob, 4),
                value=round(value, 4),
            )
        )

    return sorted(picks, key=lambda p: p.value, reverse=True)


def split_good_and_extra(ranked_picks: list[Pick]) -> tuple[list[Pick], list[Pick]]:
    good_candidates = [
        p
        for p in ranked_picks
        if p.value >= 0.06 and p.model_prob >= 0.55 and 1.50 <= p.odds <= 2.40
    ]
    good_picks = good_candidates[:5]

    used_ids = {p.match_id for p in good_picks}
    extra_candidates = [
        p
        for p in ranked_picks
        if p.match_id not in used_ids
        and p.value >= 0.03
        and p.model_prob >= 0.52
        and 1.50 <= p.odds <= 2.40
    ]
    extra_picks = extra_candidates[:10]

    return good_picks, extra_picks
