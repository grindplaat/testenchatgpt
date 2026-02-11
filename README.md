# BTTS YES Weekend Signal Bot

Simple Python signal bot that estimates BTTS (Both Teams To Score) YES probability and compares it with market odds.

## Features
- Mock JSON-backed data provider
- Live Odds API provider for BTTS market (`markets=btts`) using The Odds API v4
- Mock provider model from last 8 matches per team
- Value scoring using market implied probability
- Output files:
  - `report.md`
  - `picks.json`

## Project structure

```text
app/
  run.py
  data_provider/
  model/
  picker/
data/
  fixtures.json
  odds.json
  histories.json
tests/
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip pytest
```

## Run

### Mock provider (default)

```bash
python -m app.run --weekend
```

Or explicitly:

```bash
python -m app.run --provider mock --weekend
```

### Live Odds API provider

Uses:

`https://api.the-odds-api.com/v4/sports/{sport_key}/odds?regions=eu&oddsFormat=decimal&markets=btts&apiKey=...`

Configured leagues:
- `soccer_epl`
- `soccer_spain_la_liga`

Set API key:

- macOS/Linux (bash/zsh):

```bash
export ODDS_API_KEY="your_api_key_here"
```

- Windows PowerShell:

```powershell
$env:ODDS_API_KEY="your_api_key_here"
```

Then run:

```bash
py -m app.run --weekend --provider oddsapi
```

## Rules
### Mock provider
- `implied_prob = 1 / odds`
- `value = model_prob - implied_prob`
- Good picks:
  - `value >= 0.06`
  - `model_prob >= 0.55`
  - odds in `[1.50, 2.40]`
  - top 5 by value
- Extra picks:
  - `value >= 0.03`
  - `model_prob >= 0.52`
  - odds in `[1.50, 2.40]`
  - next 10 by value

### Odds API provider (current phase)
- Does **not** use histories/model yet
- Computes `implied_prob = 1 / odds`
- Ranks by market-only score and returns:
  - top 5 as Good picks
  - next 10 as Extra picks

## Tests

```bash
pytest -q
```
