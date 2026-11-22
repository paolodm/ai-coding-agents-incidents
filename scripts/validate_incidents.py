#!/usr/bin/env python3
"""Check data/incidents.csv against the dataset rules.

Usage: validate_incidents.py <incidents.csv> [--json <incidents.json>]

With --json, also checks that the JSON export matches the CSV.
Exits non-zero and prints one line per problem if anything is wrong.
"""
from __future__ import annotations

import csv
import datetime as dt
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from csv_to_json import load_rows, render_json  # noqa: E402

COLUMNS = [
    "row_number",
    "date",
    "date_basis",
    "date_notes",
    "incident_name",
    "description",
    "model",
    "harness",
    "agent_category",
    "harm_type",
    "harm_category",
    "severity",
    "affected_party",
    "what_could_have_helped",
    "source_url",
    "original_source_url",
    "publication_decision",
    "validation_confidence",
    "validation_verdict",
    "attack_vector",
    "in_wild_or_research",
    "publication_source_url",
    "additional_evidence_urls",
    "source_url_needs_update",
    "validation_notes",
    "publication_action",
]

OPTIONAL = {
    "date_notes",
    "what_could_have_helped",
    "additional_evidence_urls",
    "validation_notes",
    "publication_action",
}

ALLOWED = {
    "date_basis": {
        "incident_date",
        "incident_date_inferred",
        "disclosure_date",
        "publication_date",
        "approx_publication_date",
        "unverified",
    },
    "agent_category": {
        "coding_agent",
        "agentic_browser",
        "general_assistant",
        "saas_ai_feature",
        "agent_framework",
        "autonomous_agent",
    },
    "harm_category": {
        "code_execution",
        "data_exfiltration",
        "credential_theft",
        "data_loss",
        "unauthorized_change",
        "supply_chain_compromise",
        "unauthorized_access",
        "agent_hijack",
        "service_disruption",
    },
    "severity": {"critical", "high", "medium", "low"},
    "publication_decision": {"keep", "keep_with_caveat", "rewrite_or_verify"},
    "validation_confidence": {"high", "medium_high", "medium", "low"},
    "validation_verdict": {
        "verified",
        "anecdote",
        "research/hardening",
        "partially_verified_disputed_causality",
        "non_security_reliability_incident",
    },
    "in_wild_or_research": {"in the wild", "research"},
    "source_url_needs_update": {"True", "False"},
}

ATTACK_VECTORS = {
    "indirect prompt injection",
    "command/code injection",
    "supply chain",
    "malicious config file",
    "agent misalignment",
    "sandbox escape",
    "auth bypass",
    "missing authentication",
    "insecure default",
    "harness regression",
}

URL_COLUMNS = ["source_url", "original_source_url", "publication_source_url"]
URL_RE = re.compile(r"^https?://\S+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def check_row(row: dict, line: int, today: dt.date) -> list[str]:
    errors = []

    def err(msg: str) -> None:
        errors.append(f"line {line} (row {row.get('row_number', '?')}): {msg}")

    for key, value in row.items():
        if value != value.strip():
            err(f"{key} has leading or trailing whitespace")
        if key not in OPTIONAL and not value.strip():
            err(f"{key} is required")

    if row["row_number"] and not row["row_number"].isdigit():
        err(f"row_number must be a positive integer, got {row['row_number']!r}")

    if row["date"]:
        if not DATE_RE.match(row["date"]):
            err(f"date must be YYYY-MM-DD, got {row['date']!r}")
        else:
            try:
                parsed = dt.date.fromisoformat(row["date"])
            except ValueError:
                err(f"date is not a real calendar date: {row['date']!r}")
            else:
                if parsed > today:
                    err(f"date is in the future: {row['date']}")

    for key, allowed in ALLOWED.items():
        value = row[key]
        if value and value not in allowed:
            err(f"{key} must be one of {sorted(allowed)}, got {value!r}")

    if row["attack_vector"]:
        vectors = [v.strip() for v in row["attack_vector"].split(",")]
        unknown = [v for v in vectors if v not in ATTACK_VECTORS]
        if unknown:
            err(f"attack_vector has unknown values {unknown}; allowed: {sorted(ATTACK_VECTORS)}")
        if len(set(vectors)) != len(vectors):
            err("attack_vector lists the same value twice")

    for key in URL_COLUMNS:
        if row[key] and not URL_RE.match(row[key]):
            err(f"{key} is not an http(s) URL: {row[key]!r}")
    if row["publication_source_url"] and row["publication_source_url"] != row["source_url"]:
        err("publication_source_url must match source_url")

    if row["additional_evidence_urls"]:
        for url in row["additional_evidence_urls"].split(";"):
            if not URL_RE.match(url.strip()):
                err(f"additional_evidence_urls has a non-URL entry: {url.strip()!r}")

    if row["publication_decision"] == "rewrite_or_verify" and not row["publication_action"]:
        err("rows marked rewrite_or_verify need a publication_action saying what to fix")

    return errors


def validate(csv_path: Path, json_path: Path | None) -> list[str]:
    errors = []
    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        if header != COLUMNS:
            missing = [c for c in COLUMNS if c not in header]
            extra = [c for c in header if c not in COLUMNS]
            errors.append(
                f"header does not match expected columns (missing: {missing}, extra: {extra}, "
                "or the order differs)"
            )
            return errors
        rows = list(reader)

    today = dt.date.today()
    seen_numbers: dict[str, int] = {}
    seen_names: dict[str, int] = {}
    for line, row in enumerate(rows, start=2):
        if None in row or any(v is None for v in row.values()):
            errors.append(f"line {line}: wrong number of fields")
            continue
        errors.extend(check_row(row, line, today))
        number = row["row_number"]
        if number in seen_numbers:
            errors.append(f"line {line}: row_number {number} already used on line {seen_numbers[number]}")
        seen_numbers.setdefault(number, line)
        name = row["incident_name"].casefold()
        if name in seen_names:
            errors.append(f"line {line}: incident_name duplicates line {seen_names[name]}")
        seen_names.setdefault(name, line)

    if json_path is not None and not errors:
        expected = render_json(load_rows(csv_path))
        actual = json_path.read_text(encoding="utf-8") if json_path.exists() else ""
        if actual != expected:
            errors.append(
                f"{json_path} is out of date; run: python3 scripts/csv_to_json.py {csv_path} {json_path}"
            )

    return errors


def main(argv: list[str]) -> int:
    args = argv[1:]
    json_path = None
    if "--json" in args:
        i = args.index("--json")
        if i + 1 >= len(args):
            sys.stderr.write("--json needs a path\n")
            return 2
        json_path = Path(args[i + 1])
        del args[i : i + 2]
    if len(args) != 1:
        sys.stderr.write(__doc__)
        return 2

    errors = validate(Path(args[0]), json_path)
    for e in errors:
        print(e, file=sys.stderr)
    if errors:
        print(f"{len(errors)} problem(s) found", file=sys.stderr)
        return 1
    print("incidents.csv looks good", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
