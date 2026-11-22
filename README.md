# AI Coding Agents Incidents

A living dataset of real security incidents and failures involving AI coding agents such as Claude Code, Cursor, Codex, and GitHub Copilot.

It is updated as new incidents come out, so it reflects what is known today rather than a fixed snapshot.

## Scope

The core of the dataset is AI coding agents and the tools around them: IDE and CLI agents, cloud coding agents, extensions, config files, MCP servers, and skills.

It also keeps closely related incidents from other kinds of AI agents, because they share the same attack patterns. Every row has an `agent_category` so you can filter:

| `agent_category` | Covers |
|---|---|
| `coding_agent` | AI coding assistants and agents, plus their extensions, config files, MCP servers, and skills |
| `agentic_browser` | Browsers and browser extensions that act for the user (Perplexity Comet, ChatGPT Atlas, Claude in Chrome) |
| `general_assistant` | General AI assistants and their connectors (ChatGPT, claude.ai, Claude Desktop, Manus, OpenClaw) |
| `saas_ai_feature` | AI features built into business or consumer software (Microsoft 365 Copilot, Salesforce Agentforce, Meta's support assistant) |
| `agent_framework` | Libraries and servers for building agents (PraisonAI) |
| `autonomous_agent` | AI models acting on their own in test, research, or pentest setups that reached real systems (OpenAI, Anthropic, Google, and Meta model evaluations) |

For coding agents only, filter on `agent_category == "coding_agent"`.

## Data

- `data/incidents.csv` is the source of truth.
- `data/incidents.json` is generated from the CSV. Do not edit it by hand.

Column meanings and allowed values are listed in [CONTRIBUTING.md](CONTRIBUTING.md#columns).

## Checks

`scripts/validate_incidents.py` checks required fields, allowed values, dates, URLs, duplicates, and that the JSON matches the CSV. It runs in the pre-commit hook and on every pull request through GitHub Actions.

```sh
python3 scripts/validate_incidents.py data/incidents.csv --json data/incidents.json
```

To regenerate the JSON by hand:

```sh
python3 scripts/csv_to_json.py data/incidents.csv data/incidents.json
```

## Pre-commit hook

Enable it once per clone:

```sh
git config core.hooksPath .githooks
```

When you commit a change to the CSV, the hook checks it, regenerates the JSON, and adds the JSON to the commit. It needs `python3` on `PATH` and no extra packages.
