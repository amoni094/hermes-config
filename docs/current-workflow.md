# Current Hermes Workflow Snapshot

Generated from local runtime state. Last refreshed: 2026-07-01 (upgrade pass 2).

## Runtime
- Hermes version: Hermes Agent v0.17.0 (2026.6.19) · upstream 3a55f666
- Config path: `/var/home/rainbow/.hermes/config.yaml`
- Persona file: `/var/home/rainbow/.hermes/SOUL.md`
- Task ledger: `/var/home/rainbow/.hermes/logs/hermes-task-ledger.jsonl`
- Project AGENTS guide: `/var/home/rainbow/.hermes/hermes-agent/AGENTS.md`
- Host: Fedora Silverblue (immutable rpm-ostree), kernel 7.0.x, home `/var/home/rainbow`

## Core operating pattern
- Main model/provider: `claude-sonnet-4-6` via `anthropic`
- Fallback providers: `gemini/gemini-2.5-flash`, `custom:cerebras/gpt-oss-120b`, `custom:local/qwen3:8b`
- Delegation model/provider: `claude-opus-4-8` via `anthropic` (reasoning_effort `medium`)
- Terminal backend: `local` (persistent shell enabled)
- Context compression: enabled at threshold `0.5` with target ratio `0.33`
- Prompt caching TTL: `1h`
- `agent.tool_use_enforcement`: `strict`; `agent.verify_on_stop`: `true`
- Memory enabled: `True` / user profile enabled: `True`
- Web search/extract: `searxng` + `firecrawl`
- Browser engine: `auto`
- STT provider: `local`; TTS provider: `edge`

## Workflow conventions observed
- Concise global persona focused on direct, resourceful, verifiable work.
- Local-first terminal workflow with persistent shell enabled.
- Heavy use of skills, delegation, session search, memory, cron, and watchdog scripts.
- Verification-oriented setup with checkpoints enabled and file mutation verifier enabled.
- Background and delegation runs leave inspectable traces in the Hermes task ledger.
- Pre-tool governance via `veto-pre-tool.py` (fail-closed) evaluating local Veto-format
  rules in `~/.hermes/veto/rules/`; post-tool budget accounting via `track-budget.py`.

## Active scheduled automations
- `hourly-hermes-chat-sync`: every 60m | no_agent=False | deliver=local | last_status=ok
- `hermes-mutation-gate-watch`: every 1440m | no_agent=True | deliver=local | last_status=ok
- `hermes-memory-drift-audit`: every 1440m | no_agent=True | deliver=local | last_status=ok
- `skillspector-guard`: every 240m | no_agent=True | deliver=origin | last_status=ok
- `firecrawl-watchdog`: every 10m | no_agent=True | deliver=origin | last_status=ok
- `hermes-platform-watchdog`: every 720m | no_agent=True | deliver=local | last_status=ok

## Recent upgrade passes
- See `docs/upgrade-pass-2026-07-01.md` for the latest security-hardening,
  token-efficiency, and config-hygiene changes, plus a reusable sanitizer script
  (`scripts/sanitize_config.py`) for regenerating this repo's config export.

## Important exclusions from repo export
- `~/.hermes/.env`
- `~/.hermes/auth.json`
- session databases/logs containing secrets or third-party content
- raw gateway/session/chat histories
