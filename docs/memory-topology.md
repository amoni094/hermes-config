# Memory Topology

Last updated: 2026-08-26 (QMD disabled; session_search on state.db; Hindsight systemd; dual-track L1 → Graphiti; tier thresholds synced)

Documents the full active memory stack for this Hermes instance. Routing
decisions between layers are governed by the `hermes-memory-surface-selection` skill.

---

## Layer overview

| Layer | Backend | Location | Status | When to use |
|-------|---------|----------|--------|-------------|
| Hermes durable memory | Hermes built-in | `~/.hermes/memories/MEMORY.md` (agent notes), `USER.md` (user profile) | Active | Stable cross-session facts injected into every turn; ~2,200 + ~1,600 char budgets |
| Hindsight | API-based (Anthropic inference + OpenAI embeddings) | Internal DB, port 9177; systemd `hindsight-api.service`; NOT Ollama | Active | Long-term structured knowledge; hindsight_retain / hindsight_recall / hindsight_reflect |
| Graphiti MCP | FalkorDB + Graphiti server | `http://127.0.0.1:8765/mcp/` | Active | Episodic/relational knowledge graph; fact triplets, entity relationships |
| QMD | FlowState-QMD integration | `~/.hermes/integrations/flowstate-qmd/` | **Disabled** in config.yaml | Present on disk; do not route active queries here |
| Session search | SQLite FTS5 | `~/.hermes/state.db` (`messages_fts`) | Always on | In-session and cross-session conversation recall |
| MemPalace | MCP server | `~/.hermes/scripts/mempalace-mcp.sh` | **Disabled** in config.yaml | Not in use; present but not loaded |

---

## Embedding model

**Hindsight** uses OpenAI `text-embedding-3-small` (1536d) via the OpenAI API — NOT Ollama.
Inference for Hindsight's LLM operations uses the Anthropic API.
Ollama is **UNINSTALLED** as of 2026-07-12. Do not reference port 11434.

**Graphiti** also uses OpenAI embeddings via the OpenAI API.
FalkorDB serves as the graph backend.

Hindsight supervisor: `~/.config/systemd/user/hindsight-api.service` binds `127.0.0.1:9177`,
`idle_timeout=0` (no 300s auto-exit). Do not run a second manual daemon alongside the unit.

---

## Hindsight banks

| Bank | Role | Notes |
|------|------|-------|
| `hermes-default` | Primary | Default recall bank for mid-budget sessions |
| `hermes` | Secondary | Alternate bank for older / split traffic |

Unified recall helper: `~/.hermes/scripts/unified-recall.py`.

---

## MCP server endpoints

| Server | URL / command | config.yaml key | Status |
|--------|---------------|-----------------|--------|
| Graphiti | `http://127.0.0.1:8765/mcp/` | `mcp_servers.graphiti` | enabled: true |
| Stealth Browser | local python server under `~/.hermes/mcp/stealth-browser-mcp/` | `mcp_servers.stealth-browser-mcp` | enabled: true (defer_loading) |
| QMD | `~/.hermes/scripts/qmd-local.sh mcp` | `mcp_servers.qmd` | enabled: false |
| MemPalace | `~/.hermes/scripts/mempalace-mcp.sh` | `mcp_servers.mempalace` | enabled: false |
| Scrapfly | remote MCP URL | `mcp_servers.scrapfly` | enabled: false |

---

## Tier thresholds (config.memory.tier_thresholds)

| Key | Value | Notes |
|-----|-------|-------|
| promote_thresholds.stable | 0.45 | Promote to durable/stable track |
| promote_thresholds.volatile | 0.30 | Volatile retention band |
| promote_thresholds.ephemeral | 0.55 | Ephemeral band (higher bar to keep short-lived noise out of promote) |
| min_retention_promote | 0.45 | |
| max_ephemeral_facts | 500 | Soft cap |
| max_volatile_sessions | 20 | Soft cap |
| graphiti_warn_nodes | 40000 | Warn before growth |
| graphiti_halt_nodes | 50000 | Hard stop signal for writers |
| ttl_days_volatile | 30 | purged by memory-ttl-purge |
| ttl_days_stable | 365 | |

Scripts `l1-promote.py`, `memory-ttl-purge.py`, and `l1-graphiti-write.py` load these from
config at runtime (Dual-Track L1 promote). TraceGrant: `l1-tracegrant.py` + lifecycle.db
taint_path/decision_hash integrity checks.

---

## Routing guidance

The `hermes-memory-surface-selection` skill encodes the decision tree. Summary:

- **Prefer durable memory** for preferences, environment facts, conventions — things that
  must survive a session reset and be injected automatically.
- **Prefer Hindsight** for long-form structured knowledge, reference data, synthesis outputs
  you may want to recall by concept.
- **Prefer Graphiti** for entity/relationship graphs, temporal facts, provenance chains
  (who said what, when).
- **Prefer session_search** for recalling what was done or said in a prior conversation —
  history, decisions, outcomes (state.db FTS).
- **Skip QMD and MemPalace** — both disabled.

---

## Staging area

Autonomous improvement proposals (from cron/ralph-loops/subagent runs) are staged to
`~/.hermes/cache/pending-improvements/` via `~/.hermes/scripts/stage-improvement.sh`
rather than auto-applied. Weekly `pending-improvements-review` cron + curator slow pass
review and apply them.
