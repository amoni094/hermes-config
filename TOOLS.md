# TOOLS.md - Local Hermes Setup Notes

Last updated: 2026-08-18

## Runtime

- terminal: local backend; Docker is optional on this host.
- Python: 3.11.15 (Hermes venv); system also has 3.14.6; uv/uvx available at ~/.hermes/bin/
- Hermes version: v0.20.3 (2026.8.16.2)
- Hermes config: ~/.hermes/config.yaml; secrets: ~/.hermes/.env
- Persona: ~/.hermes/SOUL.md

## Memory stack (5 layers + staging)

- **Hermes durable memory**: `~/.hermes/memories/MEMORY.md` (agent notes) + `USER.md` (user profile); ~2,200 + ~1,600 char budgets
- **Hindsight**: API-based at port 9177; inference=Anthropic API, embeddings=OpenAI `text-embedding-3-small` 1536d; internal DB self-contained. Banks: `hermes-default` (~8,210 facts), `hermes` (~283 facts). **Ollama NOT used.**
- **Graphiti MCP**: `http://127.0.0.1:8765/mcp/` — group_id=`hermes`; FalkorDB backend at :6379 (replaces Neo4j)
- **QMD**: flowstate-qmd integration; accessed via mcp_qmd_* tools; personal Obsidian wiki corpus
- **Session search**: always-on SQLite session DB at `~/.hermes/state/sessions.db`
- **MemPalace**: present but **DISABLED** in config.yaml
- **Pending improvements staging**: `~/.hermes/cache/pending-improvements/` — autonomous loop proposals staged here for curator review

See docs/memory-topology.md for the full routing guide.

## Local services

- Firecrawl: `http://127.0.0.1:3002` (self-hosted; watchdog every 10m)
- SearXNG: `http://localhost:8888` (web search backend)
- Graphiti MCP: `http://127.0.0.1:8765/mcp/` (knowledge graph)
- FalkorDB: `localhost:6379` (Graphiti graph backend; replaces Neo4j)
- Hindsight: `http://localhost:9177` (vector memory)

**Ollama: UNINSTALLED (2026-07-12). Do not reference port 11434.**

## External gateways

- Telegram: active gateway (primary mobile notifications)
- WhatsApp: bridge present but **DORMANT** (npm vulns; do not reconnect without explicit request)

## OS / host

- Fedora 44 Silverblue (immutable rpm-ostree)
- Kernel: 7.1.8-200.fc44.x86_64
- Home: /var/home/rainbow
- Toolbox available for mutable container work

## Skills

- 179 local skills across 6 domain families; 6 disabled; 0 hub-installed
- Skill guard enforced by skillspector-guard cron (every 240m)
- Skill quality scanned weekly by omni-skill-quality-scan (0 3 * * 0)

## LLM routing summary

| Role | Model | Provider |
|------|-------|----------|
| Main session | claude-sonnet-4-6 | anthropic |
| Delegation workers | claude-sonnet-4-6 | anthropic |
| Vision (auxiliary) | claude-haiku-4-5 | anthropic |
| Compression (auxiliary) | zai-glm-4.7 | cerebras |
| Web extract (auxiliary) | zai-glm-4.7 | cerebras |
| Fallback #1 | gpt-oss-120b | cerebras |
| Fallback #2 | DeepSeek-V3.2 | sambanova |
| Fallback #3 | mistral-large-latest | mistral |
