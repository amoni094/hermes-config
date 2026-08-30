# Current Hermes Workflow Snapshot

Generated from local runtime state. Last refreshed: 2026-08-30 (v0.20.6 upgrade; primary
model flipped to anthropic/claude-sonnet-4-6; delegation to xai/grok-4.6; compression to
anthropic/claude-haiku-4-5; enforcement strict; 22 cron jobs including new research pipeline).

## Runtime
- Hermes version: Hermes Agent v0.20.6 (2026.8.27) · upstream 52e5e7c0
- Config path: `/var/home/rainbow/.hermes/config.yaml`
- Persona file: `/var/home/rainbow/.hermes/SOUL.md`
- Task ledger: `/var/home/rainbow/.hermes/logs/hermes-task-ledger.jsonl`
- Project AGENTS guide: `/var/home/rainbow/.hermes/hermes-agent/AGENTS.md`
- Host: Fedora 44 Silverblue (immutable rpm-ostree), kernel 7.1.10-200.fc44.x86_64, home `/var/home/rainbow`

## Core operating pattern
- Main model/provider: `claude-sonnet-4-6` via `anthropic` (context_length 200000)
- Fallback chain (`fallback_providers`): `xai/grok-4.6` → `mistral/mistral-large-latest` → `sambanova/gemma-4-31B-it`
- Delegation model/provider: `grok-4.6` via `xai` (max_concurrent_children=10, max_spawn_depth=1; toolset profiles)
- Auxiliary compression: `anthropic/claude-haiku-4-5` (fallback: sambanova/gemma-4-31B-it; max_concurrency=2; max_tokens=4096)
- Auxiliary title/triage/curator/web_extract: `mistral/mistral-small-latest`
- Auxiliary vision: `anthropic/claude-haiku-4-5`
- Terminal backend: `local`
- Context compression: enabled at threshold `0.35` (120000 tokens); micro_compact every 4 turns; protect_last_n=32; idle_compact_after_seconds=1800; intent_conditioned_offload=true
- `agent.tool_use_enforcement`: `strict`; `agent.verify_on_stop`: `auto`
- `agent.max_turns`: 500; `agent.gateway_timeout`: 1800s; `agent.session_stall_timeout`: 1800s
- Memory enabled via provider `hindsight`; char budgets MEMORY 2200 / USER 1600
- Web search/extract: `brave-free` (search) + `firecrawl` (extract, local :3002)
- Browser engine: Playwright/Chromium (ms-playwright cache)
- Prompt caching TTL: 1h
- Tool-loop guardrails: warnings + hard_stop on; session tool_result_cache (max 200) excluding mutating tools
- `agent.api_max_retries`: 5

## Memory stack
- Hermes durable memory (MEMORY.md + USER.md): ~2,200 + ~1,600 char budgets
- Hindsight: API-based (Anthropic API inference, OpenAI `text-embedding-3-small` 1536d) — NOT Ollama; daemon on :9177 supervised by systemd user unit `hindsight-api.service` (idle_timeout=0)
- Graphiti MCP: `http://127.0.0.1:8765/mcp/`, FalkorDB backend; L1 dual-track promote → Graphiti via l1-graphiti-write / reconcile
- Hindsight banks: `hermes-default` (primary), `hermes` (secondary)
- QMD / MemPalace: **DISABLED** in config.yaml (scripts present, not loaded)
- Session search: always-on FTS over `~/.hermes/state.db` (`messages_fts`) — NOT sessions.db
- Memory tier thresholds: promote stable 0.45 / volatile 0.30 / ephemeral 0.55; max_ephemeral_facts=500; max_volatile_sessions=20; graphiti_warn/halt 40k/50k
- L1 pipeline cadence: extract 180m → promote 220m → hindsight 240m → graphiti 240m; nightly ttl-purge + g-memory consolidation at 03:00

See `docs/memory-topology.md` for full routing guide.

## Workflow conventions
- Concise global persona focused on direct, resourceful, verifiable work.
- Local-first terminal workflow; cloud-only inference (Ollama uninstalled 2026-07-12).
- 141 local + 30 builtin = 165 enabled / 6 disabled skills; heavy skill-driven routing.
- Pre-tool governance via veto rules under `~/.hermes/veto/rules/` (mirrored under `veto/` in this repo).
- Background and delegation runs leave inspectable traces in the Hermes task ledger.
- Improvement proposals staged to `~/.hermes/cache/pending-improvements/` (weekly review cron; not auto-applied).
- Escalation discipline: daily driver claude-sonnet-4-6; escalate to grok-4.6 (delegation) / adversarial review (gpt-5.6-sol via openai custom provider) only when justified — see `claude-routing-hierarchy` skill and `docs/routing-and-workflow.md`.

## Repo export exclusions

This git repo is a sanitized snapshot. The following are intentionally excluded:
- `~/.hermes/.env` — API keys and secrets
- `~/.hermes/auth.json` — authentication state
- raw gateway/session/chat histories
- Session DBs, raw logs, process state, unredacted chat IDs

## Active scheduled automations (22 jobs, all deliver=local)

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
| `pending-improvements-review` | 0 10 * * 0 | agent | Weekly review of staged pending improvements; receives hermes-research-apply output as context |
| `skill-wiki-weekly` | 0 6 * * 0 | script | Weekly skill wiki index generation |
| `news-diff-watchdog` | every 90m | script | Diff-based news signal watcher (HF Papers, PWC, AI blogs) |
| `hermes-research-weekly` | 0 6 * * 2 | script | Tuesday 06:00 AEST: sweep arXiv + multilingual sources across 7 AI agent research categories |
| `hermes-research-apply` | 0 7 * * 2 | agent | Tuesday 07:00 AEST: apply research sweep findings as skill patches |
