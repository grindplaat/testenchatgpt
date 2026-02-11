from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from app.data_provider.mock_provider import MockDataProvider
from app.data_provider.odds_api_provider import OddsApiProvider
from app.picker.selector import (
    build_ranked_market_only_picks,
    build_ranked_picks,
    split_good_and_extra,
    split_top_good_and_extra,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BTTS YES weekend signal bot")
    parser.add_argument("--weekend", action="store_true", help="Use weekend fixtures only")
    parser.add_argument(
        "--provider",
        choices=["mock", "oddsapi"],
        default="mock",
        help="Data provider to use",
    )
    return parser


def _is_weekend(date_text: str) -> bool:
    dt = datetime.strptime(date_text, "%Y-%m-%d")
    return dt.weekday() >= 5


def _render_md_table(picks: list[dict], section_title: str) -> str:
    lines = [
        f"## {section_title}",
        "",
        "| # | Match | League | Date | Odds | Model | Implied | Value |",
        "|---:|---|---|---|---:|---:|---:|---:|",
    ]
    for idx, p in enumerate(picks, start=1):
        lines.append(
            f"| {idx} | {p['home_team']} vs {p['away_team']} | {p['league']} | {p['date']} | {p['odds']:.2f} | {p['model_prob']:.4f} | {p['implied_prob']:.4f} | {p['value']:.4f} |"
        )
    if not picks:
        lines.append("| - | No picks | - | - | - | - | - | - |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.provider == "oddsapi":
        provider = OddsApiProvider()
    else:
        provider = MockDataProvider(data_dir="data")

    fixtures = provider.get_fixtures()
    if args.weekend:
        fixtures = [f for f in fixtures if _is_weekend(f["date"])]

    odds = provider.get_odds()

    if args.provider == "oddsapi":
        ranked_picks = build_ranked_market_only_picks(
            fixtures=fixtures,
            odds_by_match_id=odds,
        )
        good_picks, extra_picks = split_top_good_and_extra(ranked_picks)
    else:
        ranked_picks = build_ranked_picks(
            fixtures=fixtures,
            odds_by_match_id=odds,
            team_histories=provider.get_team_histories(),
        )
        good_picks, extra_picks = split_good_and_extra(ranked_picks)

    good_dicts = [p.to_dict() for p in good_picks]
    extra_dicts = [p.to_dict() for p in extra_picks]

    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "scope": "weekend" if args.weekend else "all",
        "provider": args.provider,
        "good_picks": good_dicts,
        "extra_picks": extra_dicts,
    }

    Path("picks.json").write_text(json.dumps(output, indent=2), encoding="utf-8")

    report = [
        "# BTTS YES Weekend Signal Bot Report",
        "",
        f"Generated at: {output['generated_at']}",
        f"Scope: {output['scope']}",
        f"Provider: {output['provider']}",
        "",
        _render_md_table(good_dicts, "Top 5 Good Picks"),
        _render_md_table(extra_dicts, "Next 10 Extra Picks"),
    ]
    Path("report.md").write_text("\n".join(report), encoding="utf-8")

    print("Generated report.md and picks.json")


if __name__ == "__main__":
    main()
