# Contributing

Thanks for helping keep this dataset current. It tracks real incidents involving AI coding agents (Claude Code, Cursor, Codex, and similar tools), plus closely related AI agent incidents. See [Scope](README.md#scope).

## What counts as an incident

- A publicly reported failure, outage, or misbehavior of an AI agent.
- A security issue (prompt injection, data exfiltration, secret leakage, unsafe tool use, and so on).
- A notable agent-driven mistake with real impact (deleted data, leaked credentials, broken production).
- A vulnerability disclosed against an agent, its plugins, or its MCP servers.

Rumors, unverifiable anecdotes, and vendor marketing are out of scope.

## Adding an incident

1. Enable the pre-commit hook once: `git config core.hooksPath .githooks`.
2. Add a row to `data/incidents.csv` with the next unused `row_number`.
3. Fill every required column (see [Columns](#columns)) using only the allowed values.
4. Use primary sources: researcher write-ups, vendor advisories, GitHub advisories, NVD, post-mortems, or the original post. Avoid summaries of summaries.
5. Commit the CSV. The hook checks it and regenerates `data/incidents.json`.
6. Open a pull request with a short title, for example `Add 2026-05-12 Cursor production database deletion`.

Anonymize affected people unless they published the incident themselves.

## Correcting an incident

- Do not silently rewrite history. Add a dated note to the end of `validation_notes`, separated by ` | `, for example: `[correction 2026-11-21] Date changed from 2025-08-01 to 2025-08-05 per the Check Point post.`
- When you replace a source, put the new link in `source_url` and `publication_source_url`. Leave the first link in `original_source_url`.
- If a row needs work you cannot finish, set `publication_decision` to `rewrite_or_verify` and describe what is needed in `publication_action`. Clear `publication_action` when it is done.

## Columns

| Column | Required | Meaning and allowed values |
|---|---|---|
| `row_number` | yes | Unique integer. Gaps are fine. |
| `date` | yes | `YYYY-MM-DD`. `date_basis` says what the date means. |
| `date_basis` | yes | `incident_date`, `incident_date_inferred`, `disclosure_date`, `publication_date`, `approx_publication_date`, or `unverified` (date not yet checked against a source). |
| `date_notes` | no | How the date was chosen. |
| `incident_name` | yes | Short, unique title. |
| `description` | yes | A few factual sentences. |
| `model` | yes | Model involved, or "unspecified". |
| `harness` | yes | Product and mode, for example "Cursor (Agent Mode)". |
| `agent_category` | yes | `coding_agent`, `agentic_browser`, `general_assistant`, `saas_ai_feature`, `agent_framework`. See [Scope](README.md#scope). |
| `harm_type` | yes | Free-text detail of the harm. |
| `harm_category` | yes | The main harm: `code_execution`, `data_exfiltration`, `credential_theft`, `data_loss`, `unauthorized_change` (agent changed files or systems it was told not to), `supply_chain_compromise`, `unauthorized_access`, `agent_hijack` (agent made to act for an attacker), `service_disruption` (outages, quality regressions). |
| `severity` | yes | `critical`, `high`, `medium`, `low`. |
| `affected_party` | yes | Who was affected. |
| `what_could_have_helped` | no | Controls that would have prevented or limited the harm. |
| `source_url` | yes | Best primary source. |
| `original_source_url` | yes | First source recorded for the row. Same as `source_url` unless it was replaced. |
| `publication_decision` | yes | `keep`, `keep_with_caveat`, `rewrite_or_verify`. |
| `validation_confidence` | yes | `high`, `medium_high`, `medium`, `low`. |
| `validation_verdict` | yes | `verified`, `anecdote`, `research/hardening`, `partially_verified_disputed_causality`, `non_security_reliability_incident`. |
| `attack_vector` | yes | One or more, comma-separated: `indirect prompt injection`, `command/code injection`, `supply chain`, `malicious config file`, `agent misalignment`, `sandbox escape`, `auth bypass`, `missing authentication`, `insecure default`, `harness regression`. |
| `in_wild_or_research` | yes | `in the wild` or `research`. |
| `publication_source_url` | yes | Must match `source_url`. Kept so existing users of the data do not break. |
| `additional_evidence_urls` | no | Extra sources, separated by `; `. |
| `source_url_needs_update` | yes | `True` if `source_url` is broken or weak, otherwise `False`. |
| `validation_notes` | no | Verification notes and dated corrections. |
| `publication_action` | no | Open follow-up for the row. Blank when nothing is pending. |

## Reporting a sensitive issue

If you are reporting an active vulnerability in an AI agent that has not been disclosed yet, contact the vendor first and only file it here once disclosure is public.
