# TOOLS.md - Local Hermes Setup Notes

Last updated: 2026-08-26

## Runtime

- terminal: local backend; Docker is optional on this host.
- Hermes version: v0.20.5 (2026.8.19) · upstream f751a8c5
- Hermes config: ~/.hermes/config.yaml (`_config_version: 39`); secrets: ~/.hermes/.env (never exported)
- Persona: ~/.hermes/SOUL.md
- Dashboard: http://127.0.0.1:9119 (with gateway)

## Memory stack

- **Hermes durable memory**: `~/.hermes/memories/MEMORY.md` + `USER.md`; ~2,200 + ~1,600 char budgets
- **Hindsight**: API-based at :9177 via systemd `hindsight-api.service`; inference=Anthropic API; embeddings=OpenAI `text-embedding-3-small` 1536d. Banks: `hermes-default`, `hermes`. **Ollama NOT used.**
- **Graphiti MCP**: `http://127.0.0.1:8765/mcp/` — FalkorDB backend
- **QMD**: present under integrations; **DISABLED** in config.yaml
- **Session search**: FTS5 over `~/.hermes/state.db` (`messages_fts`) — not sessions.db
- **MemPalace**: present but **DISABLED** in config.yaml
- **Pending improvements staging**: `~/.hermes/cache/pending-improvements/`

See docs/memory-topology.md for the full routing guide.

## Local services

- Firecrawl: `http://127.0.0.1:3002` (self-hosted; watchdog every 10m)
- Brave Search: primary `web.search_backend`
- SearXNG: `http://127.0.0.1:8888` (local spare index; not primary)
- Graphiti MCP: `http://127.0.0.1:8765/mcp/`
- Hindsight: `http://127.0.0.1:9177`
- Hermes dashboard: `http://127.0.0.1:9119`

**Ollama: UNINSTALLED (2026-07-12). Do not reference port 11434.**

## External gateways

- Telegram: active gateway (primary mobile notifications)
- WhatsApp: bridge present but **DORMANT** (do not reconnect without explicit request)

## OS / host

- Fedora 44 Silverblue (immutable rpm-ostree)
- Kernel: 7.1.10-200.fc44.x86_64
- Home: /var/home/rainbow
- Toolbox available for mutable container work

## Skills

- Live index: 135 local + 31 builtin = 160 enabled / 6 disabled (0 hub-installed)
- config.skills.disabled lists additional platform/stale skill names
- Skill guard: skillspector-guard every 240m; weekly omni-skill-quality-scan; monthly skill-prune-audit

## LLM routing summary

| Role | Model | Provider |
|------|-------|----------|
| Main session | grok-4.5 | xai |
| Delegation workers | mistral-small-latest | mistral |
| Vision (auxiliary) | claude-haiku-4-5 | anthropic |
| Compression / title / triage / curator / web_extract | mistral-small-latest | mistral |
| Fallback #1 | gpt-oss-120b | cerebras |
| Fallback #2 | DeepSeek-V3.2 | sambanova |
| Fallback #3 | mistral-large-latest | mistral |
| Embeddings | text-embedding-3-small | openai |
| Adversarial override | gpt-5.6-sol | custom openai |

Full detail: docs/routing-and-workflow.md + config.sanitized.yaml
