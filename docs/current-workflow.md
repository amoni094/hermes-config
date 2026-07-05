# Current Hermes Workflow Snapshot

Generated from local runtime state. Last refreshed: 2026-07-05 (architecture doc + scripts inventory update + delegation model / compression threshold drift fixes).

## Runtime
- Hermes version: Hermes Agent v0.18.0 (2026.7.1) · upstream dec4485d · local 7e8f50a1 (+1 carried commit)
- Config path: `/var/home/rainbow/.hermes/config.yaml`
- Persona file: `/var/home/rainbow/.hermes/SOUL.md`
- Task ledger: `/var/home/rainbow/.hermes/logs/hermes-task-ledger.jsonl`
- Project AGENTS guide: `/var/home/rainbow/.hermes/hermes-agent/AGENTS.md`
- Host: Fedora 44 Silverblue (immutable rpm-ostree), kernel 7.0.14-201.fc44.x86_64, home `/var/home/rainbow`

## Core operating pattern
- Main model/provider: `claude-sonnet-4-6` via `anthropic`
- Fallback chain: `cerebras/gpt-oss-120b` → `sambanova/DeepSeek-V3.1` → `mistral/mistral-large-latest`
- Delegation model/provider: `claude-sonnet-4-6` via `anthropic`
- Terminal backend: `local` (persistent shell enabled)
- Context compression: enabled at threshold `0.4`
- `agent.tool_use_enforcement`: `permissive`; `agent.verify_on_stop`: `false`
- Memory enabled: `True` / user profile enabled: `True`
- Web search/extract: `searxng` + `firecrawl`
- Browser engine: `auto`
- TTS provider: `edge`

## Memory stack
- Hermes durable memory (MEMORY.md + USER.md): ~2,200 char budget
- Hindsight (local_embedded/Ollama): ~/.hindsight/
- Graphiti MCP: http://127.0.0.1:8765/mcp/, group_id=hermes
- QMD: flowstate-qmd integration
- Session search: always-on
- MemPalace: present, DISABLED

See `docs/memory-topology.md` for full routing guide.

## Workflow conventions observed
- Concise global persona focused on direct, resourceful, verifiable work.
- Local-first terminal workflow with persistent shell enabled.
- Heavy use of skills, delegation, session search, memory, cron, and watchdog scripts.
- Pre-tool governance via `veto-pre-tool.py` evaluating rules in `~/.hermes/veto/rules/`.
- Background and delegation runs leave inspectable traces in the Hermes task ledger.

## Active scheduled automations (8 jobs, all last-run: ok as of 2026-07-03)
- `hourly-hermes-chat-sync`: every 240m | agent | deliver=local | Obsidian vault sync
- `skillspector-guard`: every 240m | no_agent | deliver=local | skill guard enforcement
- `session-auto-prune`: every 240m | no_agent | deliver=local | prune stale sessions
- `firecrawl-watchdog`: every 10m | no_agent | deliver=local | Firecrawl health check
- `hermes-platform-watchdog`: every 720m | no_agent | deliver=local | broad platform health
- `hermes-mutation-gate-watch`: every 1440m | no_agent | deliver=local | mutation gate check
- `hermes-memory-drift-audit`: every 1440m | no_agent | deliver=local | memory drift audit
- `obsidian-weekly-review`: 0 17 * * 5 | agent + script | deliver=local | weekly vault review

## Recent upgrade passes
- See `docs/upgrade-pass-2026-07-03.md` for the latest pass (Pass 4+5): config consolidation
  751 → 68 lines, platform-watchdog rewrite, prune-sessions-daily removed (duplicate),
  research-paper-writing skill pruned, ANTHROPIC_API_KEY duplicate removed, 47 hardening
  issues resolved by Fable-5 orchestrator.
- See `docs/upgrade-pass-2026-07-01-pass3.md` for pass 3: +4 hard-block and +2 warn veto rules
  (reverse/bind shells, nc/socat/mkfifo backdoors, decode-then-exec bypasses,
  HTML img-src exfil, CSS concealment).
- See `docs/upgrade-pass-2026-07-01.md` for prior security-hardening,
  token-efficiency, and config-hygiene changes, plus sanitizer script.

## Important exclusions from repo export
- `~/.hermes/.env`
- `~/.hermes/auth.json`
- session databases/logs containing secrets or third-party content
- raw gateway/session/chat histories

