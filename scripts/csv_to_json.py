#!/usr/bin/env python3
"""Convert the incidents CSV into a JSON export.

Usage: csv_to_json.py <input.csv> <output.json>
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


def _coerce(key: str, value: str):
    if key == "row_number":
        try:
            return int(value)
        except ValueError:
            return value
    if value == "True":
        return True
    if value == "False":
        return False
    return value


def convert(csv_path: Path, json_path: Path) -> int:
    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = [{k: _coerce(k, v) for k, v in row.items()} for row in reader]
    json_path.write_text(
        json.dumps(rows, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return len(rows)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        sys.stderr.write("usage: csv_to_json.py <input.csv> <output.json>\n")
        return 1
    count = convert(Path(argv[1]), Path(argv[2]))
    sys.stderr.write(f"Wrote {count} incidents to {argv[2]}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
