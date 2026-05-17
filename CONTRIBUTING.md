# Contributing

Thanks for helping keep this repo current. It tracks real-world incidents involving AI coding agents (Claude Code, Cursor, Codex, and similar tools).

## What counts as an incident

- A publicly reported failure, outage, or misbehavior of an AI coding agent.
- A security issue (prompt injection, data exfiltration, secret leakage, unsafe tool use, etc.).
- A notable agent-driven mistake with measurable impact (deleted data, leaked credentials, broken production, etc.).
- A vulnerability or weakness disclosed against an agent, its plugins, or its MCP servers.

Rumors, unverifiable anecdotes, and vendor marketing are out of scope.

## How to add an incident

1. Open an issue or a PR with a short, descriptive title (e.g. `2026-05-12 — <agent> deleted production database`).
2. Include the following:
   - **Date** of the incident (YYYY-MM-DD).
   - **Agent / tool** involved and version if known.
   - **Summary** in 2-4 sentences.
   - **Impact** — what broke, who was affected, and how it was discovered.
   - **Source links** — primary sources only (post-mortems, vendor advisories, original posts). Avoid linking to summaries of summaries.
   - **Status** — ongoing, resolved, disputed, etc.
3. Keep entries factual. Save analysis and opinion for a clearly marked notes section.

## Updating an existing incident

- Add new information at the bottom of the entry with a dated update line.
- Don't rewrite history — if a previously reported detail turns out to be wrong, strike it through and explain the correction.

## Style

- Plain Markdown.
- Use ISO dates (YYYY-MM-DD).
- Link to sources inline.
- Anonymize affected individuals unless they have published the incident themselves.

## Reporting a sensitive issue

If you're reporting an active vulnerability in an AI coding agent that has not yet been disclosed, please contact the vendor first and only file here once disclosure is public.
