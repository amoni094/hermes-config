# Current Hermes Workflow Snapshot

Generated from local runtime state. Last refreshed: 2026-09-10 (Hermes v0.21.1 / upstream 990473a7; kernel 7.1.13; skills count updated 173 local/29 builtin/196 enabled; compression threshold 0.5; 11 new cron jobs added: concept-lattice-nightly, cs-primers-quarterly, cs-research-interpret, cs-research-weekly, desktop-sync-nightly, firewall-port-audit, hermes-math-interpret, hermes-math-sweep, hypermem-promote, se-gos-weekly, state-wal-checkpoint; total now 33).

## Runtime
- Hermes version: Hermes Agent v0.21.1 (2026.9.7) · upstream 990473a7
- Config path: `/var/home/rainbow/.hermes/config.yaml`
- Persona file: `/var/home/rainbow/.hermes/SOUL.md`
- Task ledger: `/var/home/rainbow/.hermes/logs/hermes-task-ledger.jsonl`
- Project AGENTS guide: `/var/home/rainbow/.hermes/hermes-agent/AGENTS.md`
- Host: Fedora 44 Silverblue (immutable rpm-ostree), kernel 7.1.13-200.fc44.x86_64, home `/var/home/rainbow`

## Core operating pattern
- Main model/provider: `claude-sonnet-4-6` via `anthropic` (context_length 200000)
- Fallback chain (`fallback_providers`): `xai/grok-4.6` → `mistral/mistral-large-latest` → `sambanova/gemma-4-31B-it`
- Delegation model/provider: `grok-4.6` via `xai` (max_concurrent_children=10, max_spawn_depth=1; toolset profiles)
- Auxiliary compression: `anthropic/claude-haiku-4-5` (fallback: sambanova/gemma-4-31B-it; max_concurrency=2; max_tokens=4096)
- Auxiliary title/triage/curator/web_extract: `mistral/mistral-small-latest`
- Auxiliary vision: `anthropic/claude-haiku-4-5`
- Terminal backend: `local`
- Context compression: enabled at threshold `0.5` (120000 tokens); micro_compact every 4 turns; protect_last_n=32; idle_compact_after_seconds=1800; intent_conditioned_offload=true
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
- 173 local + 29 builtin = 196 enabled / 6 disabled skills; heavy skill-driven routing.
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

## Active scheduled automations (33 jobs, all deliver=local)

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
| `concept-lattice-nightly` | 0 4 * * * | script | Nightly concept lattice index over skills/memory |
| `state-wal-checkpoint` | 20 3 * * * | script | Nightly WAL checkpoint for state.db |
| `hermes-math-sweep` | 0 1 * * 2 | script | Tuesday: sweep arXiv math categories |
| `hermes-math-interpret` | 30 6 * * 2 | script | Tuesday: interpret math sweep output into skill findings |
| `cs-research-weekly` | 0 2 * * 4 | script | Thursday: sweep CS/systems research |
| `cs-research-interpret` | 30 6 * * 4 | script | Thursday: interpret CS sweep output |
| `cs-primers-quarterly` | 0 3 1 */3 * | script | Quarterly: generate CS domain primers |
| `hypermem-promote` | every 220m | script | Hypermem tier promote (staggered with l1-promote) |
| `desktop-sync-nightly` | 0 10 * * * | script | Daily desktop→ThinkPad backup sync to F:\Hermes |
| `firewall-port-audit` | 10 4 * * 1 | script | Weekly Monday firewall/port audit |
| `se-gos-weekly` | 0 5 * * 0 | script | Weekly: bridge SE-GoS findings into Graphiti |
