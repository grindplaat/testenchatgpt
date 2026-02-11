from app.run import build_parser


def test_parser_help_includes_provider_flag():
    parser = build_parser()
    help_text = parser.format_help()

    assert "--provider" in help_text
    assert "mock" in help_text
    assert "oddsapi" in help_text


def test_provider_default_is_mock():
    parser = build_parser()
    args = parser.parse_args([])

    assert args.provider == "mock"
