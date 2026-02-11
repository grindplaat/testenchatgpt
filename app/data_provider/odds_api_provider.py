from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen

from app.data_provider.base import DataProvider

ODDS_API_BASE = "https://api.the-odds-api.com/v4"
SPORT_KEYS = ["soccer_epl", "soccer_spain_la_liga"]


class OddsApiProvider(DataProvider):
    """Live provider that fetches soccer BTTS odds from The Odds API v4."""

    def __init__(self, api_key: str | None = None, sport_keys: list[str] | None = None) -> None:
        self.api_key = api_key or os.getenv("ODDS_API_KEY")
        if not self.api_key:
            raise ValueError("ODDS_API_KEY is required for provider=oddsapi")
        self.sport_keys = sport_keys or SPORT_KEYS
        self._events: list[dict[str, Any]] | None = None

    def _fetch_sport_events(self, sport_key: str) -> list[dict[str, Any]]:
        query = urlencode(
            {
                "regions": "eu",
                "oddsFormat": "decimal",
                "markets": "btts",
                "apiKey": self.api_key,
            }
        )
        url = f"{ODDS_API_BASE}/sports/{sport_key}/odds?{query}"
        with urlopen(url) as response:  # nosec B310 - expected external HTTP API call
            payload = response.read().decode("utf-8")
        raw_events = json.loads(payload)
        return normalize_odds_api_events(raw_events, sport_key=sport_key)

    def _get_events(self) -> list[dict[str, Any]]:
        if self._events is None:
            events: list[dict[str, Any]] = []
            for sport_key in self.sport_keys:
                events.extend(self._fetch_sport_events(sport_key))
            self._events = events
        return self._events

    def get_fixtures(self) -> list[dict[str, Any]]:
        fixtures: list[dict[str, Any]] = []
        for event in self._get_events():
            fixtures.append(
                {
                    "match_id": event["match_id"],
                    "league": event["league"],
                    "date": event["date"],
                    "home_team": event["home_team"],
                    "away_team": event["away_team"],
                }
            )
        return fixtures

    def get_odds(self) -> dict[str, float]:
        return {event["match_id"]: float(event["btts_yes_odds"]) for event in self._get_events()}

    def get_team_histories(self) -> dict[str, list[dict[str, bool]]]:
        # Live provider currently ranks using market-implied metrics only.
        return {}


def normalize_odds_api_events(raw_events: list[dict[str, Any]], sport_key: str) -> list[dict[str, Any]]:
    """Normalize The Odds API events to local fixture+odds shape."""
    normalized: list[dict[str, Any]] = []
    for event in raw_events:
        yes_price = _extract_btts_yes_price(event)
        if yes_price is None:
            continue

        commence_time = event.get("commence_time")
        date = _date_from_commence_time(commence_time)

        normalized.append(
            {
                "match_id": event.get("id"),
                "league": event.get("sport_title") or sport_key,
                "date": date,
                "home_team": event.get("home_team", "Unknown Home"),
                "away_team": event.get("away_team", "Unknown Away"),
                "btts_yes_odds": yes_price,
            }
        )

    return normalized


def _extract_btts_yes_price(event: dict[str, Any]) -> float | None:
    for bookmaker in event.get("bookmakers", []):
        for market in bookmaker.get("markets", []):
            if market.get("key") != "btts":
                continue
            for outcome in market.get("outcomes", []):
                name = str(outcome.get("name", "")).strip().lower()
                if name in {"yes", "btts_yes", "both teams to score - yes"}:
                    price = outcome.get("price")
                    if price is not None:
                        return float(price)
    return None


def _date_from_commence_time(commence_time: str | None) -> str:
    if not commence_time:
        return "1970-01-01"
    # The Odds API typically returns ISO8601 like: 2026-02-15T14:00:00Z
    return datetime.fromisoformat(commence_time.replace("Z", "+00:00")).date().isoformat()
