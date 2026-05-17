# AI Coding Agents Incidents

A living repository tracking current incidents involving AI coding agents such as Claude Code, Cursor, and Codex.

This repo is updated on an ongoing basis as new incidents surface, so its contents reflect the current state of known issues rather than a fixed historical snapshot.

## Data

- `data/incidents.csv` — the source of truth for incidents.
- `data/incidents.json` — generated JSON export of the same data.

Edit only the CSV. The JSON is regenerated automatically by the pre-commit hook (see below). To regenerate manually:

```sh
python3 scripts/csv_to_json.py data/incidents.csv data/incidents.json
```

## Pre-commit hook

The repo ships a pre-commit hook in `.githooks/pre-commit` that re-runs the CSV → JSON export whenever `data/incidents.csv` is staged, and stages the resulting `data/incidents.json` so the two stay in sync.

Enable it once per clone:

```sh
git config core.hooksPath .githooks
```

Requires `python3` on `PATH`.
