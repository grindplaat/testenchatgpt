from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class DataProvider(ABC):
    """Interface for loading fixture, odds, and team history data."""

    @abstractmethod
    def get_fixtures(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_odds(self) -> dict[str, float]:
        raise NotImplementedError

    @abstractmethod
    def get_team_histories(self) -> dict[str, list[dict[str, bool]]]:
        raise NotImplementedError
