# Memory Topology

Last updated: 2026-07-03

Documents the full active memory stack for this Hermes instance. Routing
decisions between layers are governed by the `hermes-memory-surface-selection`
skill.

---

## Layer overview

| Layer | Backend | Location | Status | When to use |
|-------|---------|----------|--------|-------------|
| Hermes durable memory | Hermes built-in | `~/.hermes/memories/MEMORY.md` (agent notes), `USER.md` (user profile) | Active | Stable cross-session facts injected into every turn; ~2,200 char budget |
| Hindsight | local_embedded (Ollama) | `~/.hindsight/profiles/` | Active | Long-term structured knowledge; hindsight_retain / hindsight_recall / hindsight_reflect |
| Graphiti MCP | Neo4j + Graphiti server | `http://127.0.0.1:8765/mcp/`, group_id=`hermes`, reasoning group=`hermes-reasoning` | Active | Episodic/relational knowledge graph; fact triplets, entity relationships |
| QMD | FlowState-QMD integration | `~/.qmd-config/`, integration: `flowstate-qmd` | Active | Personal wiki / note corpus search (mcp_qmd_query, mcp_qmd_get) |
| Session search | SQLite session DB | `~/.hermes/state/sessions.db` | Always on | In-session and cross-session conversation recall |
| MemPalace | MCP server | `~/.hermes/scripts/mempalace-mcp.sh` | **Disabled** in `config.yaml` | Not in use; present but not loaded |

---

## Embedding model

Ollama serves embeddings at `http://localhost:11434`.
Installed models: `qwen3:8b`, `llama3.2:3b`.
Hindsight and Graphiti both depend on Ollama being healthy.

---

## MCP server endpoints

| Server | URL / command | config.yaml key | Status |
|--------|---------------|-----------------|--------|
| Graphiti | `http://127.0.0.1:8765/mcp/` | `mcp_servers.graphiti` | enabled: true |
| QMD | `~/.hermes/scripts/qmd-local.sh mcp` | `mcp_servers.qmd` | enabled: true |
| MemPalace | `~/.hermes/scripts/mempalace-mcp.sh` | `mcp_servers.mempalace` | enabled: false |
| Stealth Browser | `~/.hermes/mcp/stealth-browser-mcp/` | (integration dir) | installed, not in config |

---

## Routing guidance

The `hermes-memory-surface-selection` skill encodes the decision tree for
choosing between layers. Summary:

- **Prefer durable memory** for preferences, environment facts, conventions —
  things that must survive a session reset and should be injected automatically.
- **Prefer Hindsight** for long-form structured knowledge, reference data,
  synthesis outputs you may want to recall by concept.
- **Prefer Graphiti** for entity/relationship graphs, temporal facts, provenance
  chains (who said what, when).
- **Prefer QMD** for the Obsidian vault / personal wiki corpus — articles,
  notes, research ingestion.
- **Prefer session_search** for recalling what was done or said in a prior
  conversation — history, decisions, outcomes.
- **Skip MemPalace** — disabled; do not reference in agent prompts.

---

## Maintenance

- `hermes-memory-drift-audit` cron runs daily to check for drift between
  durable memory and actual state.
- Obsidian sync cron (`hourly-hermes-chat-sync`) writes session highlights
  to the SecondBrain vault, which feeds QMD.
