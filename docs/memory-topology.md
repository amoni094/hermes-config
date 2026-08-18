# Memory Topology

Last updated: 2026-08-18 (Ollama removed; Hindsight API-based; FalkorDB backend; Stealth Browser in MCP)

Documents the full active memory stack for this Hermes instance. Routing
decisions between layers are governed by the `hermes-memory-surface-selection` skill.

---

## Layer overview

| Layer | Backend | Location | Status | When to use |
|-------|---------|----------|--------|-------------|
| Hermes durable memory | Hermes built-in | `~/.hermes/memories/MEMORY.md` (agent notes), `USER.md` (user profile) | Active | Stable cross-session facts injected into every turn; ~2,200 + ~1,600 char budgets |
| Hindsight | API-based (Anthropic inference + OpenAI embeddings) | Internal DB, port 9177; NOT Ollama | Active | Long-term structured knowledge; hindsight_retain / hindsight_recall / hindsight_reflect |
| Graphiti MCP | FalkorDB (port 6379) + Graphiti server | `http://127.0.0.1:8765/mcp/`, group_id=`hermes` | Active | Episodic/relational knowledge graph; fact triplets, entity relationships |
| QMD | FlowState-QMD integration | `~/.hermes/integrations/flowstate-qmd/` | Active | Personal Obsidian wiki / note corpus search (mcp_qmd_query, mcp_qmd_get) |
| Session search | SQLite session DB | `~/.hermes/state/sessions.db` | Always on | In-session and cross-session conversation recall |
| MemPalace | MCP server | `~/.hermes/scripts/mempalace-mcp.sh` | **Disabled** in config.yaml | Not in use; present but not loaded |

---

## Embedding model

**Hindsight** uses OpenAI `text-embedding-3-small` (1536d) via the OpenAI API — NOT Ollama.
Inference for Hindsight's LLM operations uses the Anthropic API (claude-haiku-4-5).
Ollama is **UNINSTALLED** as of 2026-07-12. Do not reference port 11434.

**Graphiti** also uses OpenAI `text-embedding-3-small` via `OPENAI_API_URL=https://api.openai.com/v1`.
FalkorDB serves as the graph backend at port 6379.

---

## Hindsight banks

| Bank | Facts | Notes |
|------|-------|-------|
| `hermes-default` | ~8,210 | Primary bank |
| `hermes` | ~283 | Secondary bank |

---

## MCP server endpoints

| Server | URL / command | config.yaml key | Status |
|--------|---------------|-----------------|--------|
| Graphiti | `http://127.0.0.1:8765/mcp/` | `mcp_servers.graphiti` | enabled: true |
| Stealth Browser | `~/.hermes/mcp/stealth-browser-mcp/` | `mcp_servers.stealth-browser-mcp` | installed (in mcp/ dir) |
| QMD | `~/.hermes/scripts/qmd-local.sh mcp` | `mcp_servers.qmd` | enabled: true |
| MemPalace | `~/.hermes/scripts/mempalace-mcp.sh` | `mcp_servers.mempalace` | enabled: false |

---

## Routing guidance

The `hermes-memory-surface-selection` skill encodes the decision tree for choosing between
layers. Summary:

- **Prefer durable memory** for preferences, environment facts, conventions — things that
  must survive a session reset and be injected automatically.
- **Prefer Hindsight** for long-form structured knowledge, reference data, synthesis outputs
  you may want to recall by concept.
- **Prefer Graphiti** for entity/relationship graphs, temporal facts, provenance chains
  (who said what, when).
- **Prefer QMD** for the Obsidian vault / personal wiki corpus — articles, notes, research
  ingestion.
- **Prefer session_search** for recalling what was done or said in a prior conversation —
  history, decisions, outcomes.
- **Skip MemPalace** — disabled.

---

## Staging area

Autonomous improvement proposals (from cron/ralph-loops/subagent runs) are staged to
`~/.hermes/cache/pending-improvements/` via `~/.hermes/scripts/stage-improvement.sh`
rather than auto-applied. The curator slow pass reviews and applies them.
