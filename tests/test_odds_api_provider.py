import json
from pathlib import Path

from app.data_provider.odds_api_provider import normalize_odds_api_events


def test_normalize_odds_api_events_extracts_btts_yes_and_date():
    sample_path = Path("tests/samples/odds_api_soccer_epl_sample.json")
    raw_events = json.loads(sample_path.read_text(encoding="utf-8"))

    normalized = normalize_odds_api_events(raw_events, sport_key="soccer_epl")

    assert len(normalized) == 2
    assert normalized[0]["match_id"] == "event_1"
    assert normalized[0]["home_team"] == "Arsenal"
    assert normalized[0]["away_team"] == "Chelsea"
    assert normalized[0]["btts_yes_odds"] == 1.8
    assert normalized[0]["date"] == "2026-02-14"

    assert normalized[1]["match_id"] == "event_2"
    assert normalized[1]["btts_yes_odds"] == 1.65
    assert normalized[1]["date"] == "2026-02-15"
