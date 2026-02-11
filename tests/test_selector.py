from app.data_provider.mock_provider import MockDataProvider
from app.picker.selector import build_ranked_picks, split_good_and_extra


def test_ranked_picks_are_sorted_descending_by_value():
    provider = MockDataProvider(data_dir="data")
    picks = build_ranked_picks(
        provider.get_fixtures(), provider.get_odds(), provider.get_team_histories()
    )
    assert picks == sorted(picks, key=lambda p: p.value, reverse=True)


def test_split_good_and_extra_respects_limits_and_non_overlap():
    provider = MockDataProvider(data_dir="data")
    ranked = build_ranked_picks(
        provider.get_fixtures(), provider.get_odds(), provider.get_team_histories()
    )
    good, extra = split_good_and_extra(ranked)

    assert len(good) <= 5
    assert len(extra) <= 10
    assert not ({p.match_id for p in good} & {p.match_id for p in extra})

    for p in good:
        assert p.value >= 0.06
        assert p.model_prob >= 0.55

    for p in extra:
        assert p.value >= 0.03
        assert p.model_prob >= 0.52
