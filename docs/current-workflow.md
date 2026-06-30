# Current Hermes Workflow Snapshot

Generated from local runtime state.

## Runtime
- Hermes version: Hermes Agent v0.17.0 (2026.6.19) · upstream 3a55f666
- Config path: `/var/home/rainbow/.hermes/config.yaml`
- Persona file: `/var/home/rainbow/.hermes/SOUL.md`
- Task ledger: `/var/home/rainbow/.hermes/logs/hermes-task-ledger.jsonl`
- Project AGENTS guide: `/var/home/rainbow/.hermes/hermes-agent/AGENTS.md`

## Core operating pattern
- Main model/provider: `gpt-5.4` via `openai-codex`
- Delegation model/provider: `gpt-5.5` via `openai-codex`
- Terminal backend: `local`
- Context compression: enabled at threshold `0.6` with target ratio `0.2`
- Prompt caching TTL: `5m`
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

## Active scheduled automations
- `hourly-hermes-chat-sync`: every 60m | no_agent=False | deliver=local | last_status=ok
- `hermes-mutation-gate-watch`: every 1440m | no_agent=True | deliver=local | last_status=ok
- `hermes-memory-drift-audit`: every 1440m | no_agent=True | deliver=local | last_status=ok
- `skillspector-guard`: every 240m | no_agent=True | deliver=origin | last_status=ok
- `firecrawl-watchdog`: every 10m | no_agent=True | deliver=origin | last_status=ok
- `hermes-platform-watchdog`: every 720m | no_agent=True | deliver=local | last_status=ok

## Important exclusions from repo export
- `~/.hermes/.env`
- `~/.hermes/auth.json`
- session databases/logs containing secrets or third-party content
- raw gateway/session/chat histories
