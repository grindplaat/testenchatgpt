# BTTS YES Weekend Signal Bot

Simple Python signal bot that estimates BTTS (Both Teams To Score) YES probability from mock recent form and compares it with market odds.

## Features
- Mock JSON-backed data provider
- BTTS probability model from last 8 matches per team
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

Weekend-only run:

```bash
python -m app.run --weekend
```

This generates:
- `report.md`
- `picks.json`

## Rules
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

## Tests

```bash
pytest -q
```
