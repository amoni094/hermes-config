# Current Hermes Workflow Snapshot

Generated from local runtime state. Last refreshed: 2026-08-18 (version, model, memory topology,
compression threshold, verify_on_stop, cron jobs, skills count — full drift pass).

## Runtime
- Hermes version: Hermes Agent v0.20.3 (2026.8.16.2)
- Config path: `/var/home/rainbow/.hermes/config.yaml`
- Persona file: `/var/home/rainbow/.hermes/SOUL.md`
- Task ledger: `/var/home/rainbow/.hermes/logs/hermes-task-ledger.jsonl`
- Project AGENTS guide: `/var/home/rainbow/.hermes/hermes-agent/AGENTS.md`
- Host: Fedora 44 Silverblue (immutable rpm-ostree), kernel 7.1.8-200.fc44.x86_64, home `/var/home/rainbow`

## Core operating pattern
- Main model/provider: `claude-sonnet-4-6` via `anthropic`
- Fallback chain: `cerebras/gpt-oss-120b` → `sambanova/DeepSeek-V3.2` → `mistral/mistral-large-latest`
- Delegation model/provider: `claude-sonnet-4-6` via `anthropic` (same as main; no separate tier)
- Auxiliary compression model/provider: `cerebras/zai-glm-4.7` (auxiliary.compression)
- Auxiliary web_extract model/provider: `cerebras/zai-glm-4.7`
- Auxiliary vision model/provider: `anthropic/claude-haiku-4-5`
- Terminal backend: `local` (persistent shell enabled)
- Context compression: enabled at threshold `0.35` (tokens: 80,000), micro_compact every 3 turns
- `agent.tool_use_enforcement`: `permissive`; `agent.verify_on_stop`: `auto`
- `agent.max_turns`: 500; `agent.gateway_timeout`: 1800s
- Memory enabled: `True` / user profile enabled: `True`
- Web search/extract: `searxng` (local :8888) + `firecrawl` (local :3002)
- Browser engine: Playwright/Chromium (ms-playwright cache)
- Prompt caching TTL: 1h

## Memory stack
- Hermes durable memory (MEMORY.md + USER.md): ~2,200 + ~1,600 char budgets
- Hindsight: API-based (Anthropic API inference, OpenAI `text-embedding-3-small` 1536d) — NOT Ollama; internal DB self-contained at port 9177
- Graphiti MCP: `http://127.0.0.1:8765/mcp/`, group_id=`hermes`, FalkorDB backend (port 6379)
- Hindsight banks: `hermes-default` (~8,210 facts), `hermes` (~283 facts)
- QMD: flowstate-qmd integration (personal Obsidian wiki corpus)
- Session search: always-on SQLite session DB
- MemPalace: **DISABLED** in config.yaml (script present, not loaded)

See `docs/memory-topology.md` for full routing guide.

## Workflow conventions observed
- Concise global persona focused on direct, resourceful, verifiable work.
- Local-first terminal workflow with persistent shell enabled.
- Heavy use of skills (179 local, 6 disabled), delegation, session search, memory, cron, and watchdog scripts.
- Pre-tool governance via `veto-pre-tool.py` evaluating rules in `~/.hermes/veto/rules/`.
- Background and delegation runs leave inspectable traces in the Hermes task ledger.
- Improvement proposals from autonomous runs staged to `~/.hermes/cache/pending-improvements/` (not auto-applied).

## Repo export exclusions

This git repo is a sanitized snapshot. The following are intentionally excluded:
- `~/.hermes/.env` — API keys and secrets
- `~/.hermes/auth.json` — authentication state
- raw gateway/session/chat histories
- Session DBs, raw logs, process state, unredacted chat IDs

## Active scheduled automations (15 jobs, all deliver=local)

| Job | Schedule | Mode | Purpose |
|-----|----------|------|---------|
| `hermes-chat-sync-4h` | every 240m | agent | Obsidian vault sync (hermes-obsidian-sync skill) |
| `hermes-mutation-gate-watch` | every 1440m | script | Mutation gate state check |
| `hermes-memory-drift-audit` | every 1440m | script | Durable memory drift audit |
| `skillspector-guard` | every 240m | script | Skill guard enforcement |
| `firecrawl-watchdog` | every 10m | script | Firecrawl health check (:3002) |
| `hermes-platform-watchdog` | every 720m | script | Broad platform health (config, MCP, Graphiti) |
| `session-auto-prune` | every 240m | script | Prune stale sessions from session DB |
| `obsidian-weekly-review` | 0 17 * * 5 | agent+script | Weekly Obsidian vault review |
| `browser-orphan-watchdog` | every 30m | script | Kill orphaned Playwright/Chrome processes |
| `l1-extract-periodic` | every 180m | script | Extract L1 facts from sessions |
| `l1-hindsight-promote` | every 240m | agent | Promote L1 facts to Hindsight |
| `l1-promote-periodic` | every 220m | script | L1 promote pipeline (script mode) |
| `omni-skill-quality-scan` | 0 3 * * 0 | script | Weekly skill quality scan (omni_skill_scan.py) |
| `skill-prune-audit` | 0 9 1 * * | script | Monthly skill prune audit |
| `g-memory-tier3-nightly` | 0 3 * * * | script | Nightly Graphiti memory consolidation |
