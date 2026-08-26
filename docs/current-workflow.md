# Current Hermes Workflow Snapshot

Generated from local runtime state. Last refreshed: 2026-08-26 (full drift pass after Hermes
v0.20.5 update + config v39 migration; main model now xAI grok-4.5).

## Runtime
- Hermes version: Hermes Agent v0.20.5 (2026.8.19) · upstream f751a8c5
- Config path: `/var/home/rainbow/.hermes/config.yaml` (`_config_version: 39`)
- Persona file: `/var/home/rainbow/.hermes/SOUL.md`
- Task ledger: `/var/home/rainbow/.hermes/logs/hermes-task-ledger.jsonl`
- Project AGENTS guide: `/var/home/rainbow/.hermes/hermes-agent/AGENTS.md`
- Host: Fedora 44 Silverblue (immutable rpm-ostree), kernel 7.1.10-200.fc44.x86_64, home `/var/home/rainbow`

## Core operating pattern
- Main model/provider: `grok-4.5` via `xai` (context_length 200000)
- Fallback chain (`fallback_providers`): `cerebras/gpt-oss-120b` → `sambanova/DeepSeek-V3.2` → `mistral/mistral-large-latest`
- Delegation model/provider: `mistral-small-latest` via `mistral` (leaf workers; max_concurrent_children=10, max_spawn_depth=1, hierarchy_aware + toolset profiles)
- Auxiliary compression: `mistral/mistral-small-latest` (fallback_chain: sambanova/DeepSeek-V3.2 → mistral/mistral-large-latest; reasoning_effort=medium; max_concurrency=2)
- Auxiliary title/triage/curator/web_extract: `mistral/mistral-small-latest`
- Auxiliary vision: `anthropic/claude-haiku-4-5`
- Custom providers (override-only, not auto-routed): openai (gpt-5.4/5.5/5.6-sol), cerebras, sambanova, mistral — keyed via `*_API_KEY` env vars
- Terminal backend: `local`
- Context compression: enabled at threshold `0.35`; micro_compact every 3 turns; protect_last_n=32; idle_compact_after_seconds=1800
- `agent.tool_use_enforcement`: `permissive`; `agent.verify_on_stop`: `auto`
- `agent.max_turns`: 500; `agent.gateway_timeout`: 1800s; `agent.session_stall_timeout`: 1800s
- Memory enabled via provider `hindsight`; char budgets MEMORY 2200 / USER 1600
- Web search/extract: `brave` (search) + `firecrawl` (extract, local :3002). SearXNG still runs locally at :8888 as a spare/local index
- Browser engine: Playwright/Chromium (ms-playwright cache); computer_use.wayland=true
- Prompt caching TTL: 1h
- Tool-loop guardrails: warnings + hard_stop on; session tool_result_cache (max 200) excluding mutating tools
- Approvals mode: `off` (destructive_slash_confirm false); command_allowlist includes hermes update / stop-restart service

## Memory stack
- Hermes durable memory (MEMORY.md + USER.md): ~2,200 + ~1,600 char budgets
- Hindsight: API-based (Anthropic API inference, OpenAI `text-embedding-3-small` 1536d) — NOT Ollama; daemon on :9177 supervised by systemd user unit `hindsight-api.service` (idle_timeout=0)
- Graphiti MCP: `http://127.0.0.1:8765/mcp/`, FalkorDB backend; L1 dual-track promote → Graphiti via l1-graphiti-write / reconcile
- Hindsight banks: `hermes-default` (primary), `hermes` (secondary)
- QMD / MemPalace: **DISABLED** in config.yaml (scripts present, not loaded)
- Session search: always-on FTS over `~/.hermes/state.db` (`messages_fts`) — NOT sessions.db
- Memory tier thresholds (config): promote stable 0.45 / volatile 0.30 / ephemeral 0.55; max_ephemeral_facts=500; max_volatile_sessions=20; graphiti_warn/halt 40k/50k
- L1 pipeline cadence: extract 180m → promote 220m → hindsight 240m → graphiti 240m; nightly ttl-purge + g-memory consolidation at 03:00

See `docs/memory-topology.md` for full routing guide.

## Workflow conventions observed
- Concise global persona focused on direct, resourceful, verifiable work.
- Local-first terminal workflow; cloud-only inference (Ollama uninstalled 2026-07-12).
- Heavy use of skills (135 local + 31 builtin = 160 enabled / 6 disabled in live index; config.skills.disabled lists platform/stale names), delegation, session_search, memory, cron, watchdogs.
- Pre-tool governance via veto rules under `~/.hermes/veto/rules/` (mirrored under `veto/` in this repo).
- Background and delegation runs leave inspectable traces in the Hermes task ledger.
- Improvement proposals staged to `~/.hermes/cache/pending-improvements/` (weekly review cron; not auto-applied).
- Escalation discipline: daily driver grok-4.5; escalate to grok-4.6 / anthropic long-context / gpt-5.6-sol (adversarial) only when justified — see `claude-routing-hierarchy` skill and `docs/routing-and-workflow.md`.

## Repo export exclusions

This git repo is a sanitized snapshot. The following are intentionally excluded:
- `~/.hermes/.env` — API keys and secrets
- `~/.hermes/auth.json` — authentication state
- raw gateway/session/chat histories
- Session DBs, raw logs, process state, unredacted chat IDs

## Active scheduled automations (18 jobs, all deliver=local)

| Job | Schedule | Mode | Purpose |
|-----|----------|------|---------|
| `hermes-chat-sync-4h` | every 240m | agent | Obsidian vault sync (hermes-obsidian-sync skill) |
| `hermes-mutation-gate-watch` | every 1440m | script | Mutation gate state check |
| `hermes-memory-drift-audit` | every 1440m | script | Durable memory drift audit |
| `skillspector-guard` | every 240m | script | Skill guard enforcement |
| `firecrawl-watchdog` | every 10m | script | Firecrawl health check (:3002) |
| `hermes-platform-watchdog` | every 720m | script | Broad platform health (config, MCP, Graphiti) |
| `session-auto-prune` | every 240m | script | Prune stale sessions from state.db |
| `obsidian-weekly-review` | 0 17 * * 5 | agent+script | Weekly Obsidian vault review |
| `browser-orphan-watchdog` | every 30m | script | Kill orphaned Playwright/Chrome processes |
| `l1-extract-periodic` | every 180m | script | Extract L1 facts from sessions |
| `l1-hindsight-promote` | every 240m | agent | Promote L1 facts to Hindsight |
| `l1-promote-periodic` | every 220m | script | L1 promote pipeline (staggered vs extract) |
| `l1-graphiti-periodic` | every 240m | script | Graphiti reconcile / write path |
| `omni-skill-quality-scan` | 0 3 * * 0 | script | Weekly skill quality scan |
| `skill-prune-audit` | 0 9 1 * * | script | Monthly skill prune audit |
| `g-memory-tier3-nightly` | 0 3 * * * | script | Nightly Graphiti memory consolidation |
| `memory-ttl-purge` | 0 3 * * * | script | Expire ephemeral/volatile memory tiers |
| `pending-improvements-review` | 0 10 * * 0 | agent | Weekly curator review of staged improvements |
