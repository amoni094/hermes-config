# External Apps and Services Register

Last updated: 2026-07-03

All external apps, local services, and third-party integrations that this
Hermes instance depends on or interacts with.

---

## Local services (self-hosted, running on this machine)

| Service | Port / path | Purpose | Status |
|---------|------------|---------|--------|
| Ollama | `http://localhost:11434` | LLM inference + embeddings. Models: `qwen3:8b`, `llama3.2:3b` | Active |
| Firecrawl | `http://127.0.0.1:3002` | Web crawl / stealth scrape for research | Active (watchdog every 10m) |
| Graphiti MCP | `http://127.0.0.1:8765/mcp/` | Knowledge graph MCP server (Neo4j backend) | Active |
| SearXNG | configured URL | Privacy-first web search backend | Active |
| World Monitor | started via `worldmonitor-start.sh` | News signal aggregator | Active (manual start) |

## Hermes plugins / integrations

| Plugin/Integration | Type | Status | Notes |
|-------------------|------|--------|-------|
| orca-status | Hermes plugin | Active | Only enabled plugin in config.yaml |
| flowstate-qmd | Integration | Active | Powers QMD MCP server; personal wiki corpus |
| stealth-browser-mcp | MCP integration | Installed | `~/.hermes/mcp/stealth-browser-mcp/`; not in config |
| hermes-agent-self-evolution | Integration dir | Present | Self-evolution harness |
| hermes-agent-acp-skill | Integration dir | Present | ACP routing to Codex CLI |
| opencode-hermes-multiagent | Integration dir | Present | Opencode multi-agent integration |
| honcho-self-hosted | Integration dir | Present | Honcho context manager |
| lintlang | Integration dir | Present | Shell lint used by watchdog scripts |
| zouroboros-swarm-executors | Integration dir | Present | Ouroboros swarm execution layer |
| flowstate-qmd.disabled | Integration dir | Disabled | Older QMD variant; superseded |
| MemPalace MCP | `mempalace-mcp.sh` | **Disabled** | Disabled in config.yaml; script present |

## Cloud / external providers

| Provider | Key env var | Quota / tier | Status | Notes |
|----------|------------|--------------|--------|-------|
| Anthropic | `ANTHROPIC_API_KEY` | Paid | Active (primary) | claude-sonnet-4-6 main session; claude-opus-4-8 delegation; claude-haiku-4-5 auxiliary |
| Cerebras | `CEREBRAS_API_KEY` | Free (14,400 RPD) | Active | Fallback #1; free tier 8K ctx cap |
| SambaNova | `SAMBANOVA_API_KEY` | Free (20 RPD/model) | Active | Fallback #2; no data training |
| Mistral | `MISTRAL_API_KEY` | Free (~1B tok/month) | Active | Fallback #3; data training opt-in |
| Google Gemini | `GOOGLE_API_KEY` | Free (1,500 RPD) | Key present, **not in fallback chain** | Prompts used for training outside EU/UK/EEA |
| Groq | `GROQ_API_KEY` | Free (1,000 RPD) | Key commented out in .env | Blocked from datacenter IPs; split-tunnel required |
| Telegram | `TELEGRAM_BOT_TOKEN` | — | Active | Primary gateway for mobile notifications |
| OpenAI Codex | — | — | Logged in | Used by `opencode-hermes-multiagent` / ACP skill |
| WhatsApp | npm bridge | — | **Dormant / disconnected** | `hermes doctor` reports 1 critical + 2 high npm vulns; do not reconnect without explicit request |
| Agent Reach | `~/.agent-reach/` | — | Installed | News/research sidecar; `agent-reach-discovery` skill |
| Firecrawl API | local only | — | Self-hosted | No cloud API key; all traffic to local :3002 |

## Local development tools

| Tool | Path / command | Purpose |
|------|---------------|---------|
| Python 3.14.6 | system python3 | Primary scripting runtime |
| uv / uvx | `~/.hermes/bin/uv`, `uvx` | Fast Python package management |
| tirith | `~/.hermes/bin/tirith` | Policy/veto evaluation |
| git | system | Version control |
| Toolbox (Fedora) | `toolbox` | Mutable container for layered tools |

## Research output pipeline (added 2026-07-03)

New Python library stack for PowerPoint + Excel + chart generation.
Lives at `~/research-output/` (not part of Hermes config; documented here
for dependency disclosure).

| Library | Version | Purpose |
|---------|---------|---------|
| python-pptx-ng | 0.7.0 | PowerPoint generation (actively maintained fork of python-pptx) |
| openpyxl | 3.1.5 | Excel read/modify (template-based workflows) |
| xlsxwriter | 3.2.9 | Excel write-only (superior native charts) |
| matplotlib | 3.11.0 | Chart rendering → PNG (150 DPI) |
| seaborn | 0.13.2 | Statistical chart styling |
| compress_pptx | 1.3.1 | PPTX file size optimization |
| markitdown | 0.1.6 | PPTX/Office → Markdown conversion (verification) |

Project entry point: `~/research-output/scripts/run_pipeline.py --demo`

---

## Integration posture decisions (as of 2026-07-03)

- **WhatsApp bridge**: intentionally dormant; npm vulns present; do not reconnect without explicit user request
- **MemPalace**: present but disabled; no active use case
- **Gemini key**: present but not in active fallback chain (training data risk outside EU)
- **Groq key**: present but commented out (.env); split-tunnel needed; not active fallback
- **Stealth browser MCP**: installed but not wired into config.yaml mcp_servers; manual use only
