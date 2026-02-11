from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.data_provider.base import DataProvider


class MockDataProvider(DataProvider):
    """Loads hardcoded mock data from JSON files."""

    def __init__(self, data_dir: str | Path = "data") -> None:
        self.data_dir = Path(data_dir)

    def _read_json(self, file_name: str) -> Any:
        path = self.data_dir / file_name
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def get_fixtures(self) -> list[dict[str, Any]]:
        return self._read_json("fixtures.json")

    def get_odds(self) -> dict[str, float]:
        odds_items = self._read_json("odds.json")
        return {item["match_id"]: float(item["btts_yes_odds"]) for item in odds_items}

    def get_team_histories(self) -> dict[str, list[dict[str, bool]]]:
        return self._read_json("histories.json")
