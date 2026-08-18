# External Apps and Services Register

Last updated: 2026-08-18 (Ollama removed; FalkorDB replaces Neo4j; model names corrected to sonnet-4-6;
Hindsight API-based; new integrations documented; repo1 LLM gateway project added)

All external apps, local services, and third-party integrations this Hermes instance depends on.

---

## Local services (self-hosted, running on this machine)

| Service | Port / path | Purpose | Status |
|---------|------------|---------|--------|
| Firecrawl | `http://127.0.0.1:3002` | Web crawl / stealth scrape for research | Active (watchdog every 10m) |
| Graphiti MCP | `http://127.0.0.1:8765/mcp/` | Knowledge graph MCP server | Active |
| FalkorDB | `localhost:6379` | Graph DB backend for Graphiti (replaces Neo4j) | Active |
| Hindsight | `http://localhost:9177` | Vector memory store (API-based, self-contained internal DB) | Active |
| SearXNG | `http://localhost:8888` | Privacy-first web search backend | Active |

**Note: Ollama is UNINSTALLED (2026-07-12).** Neither Hindsight nor Graphiti use local LLMs.
All inference uses cloud APIs (Anthropic, OpenAI embeddings).

---

## Hermes plugins / integrations

| Plugin/Integration | Type | Status | Notes |
|-------------------|------|--------|-------|
| orca-status | Hermes plugin | Active | Only enabled plugin in config.yaml |
| flowstate-qmd | Integration | Active | Powers QMD MCP server; personal Obsidian wiki corpus |
| stealth-browser-mcp | MCP integration | Installed | `~/.hermes/mcp/stealth-browser-mcp/`; browser automation via CDP |

---

## Cloud / external providers

| Provider | Key env var | Quota / tier | Status | Notes |
|----------|------------|--------------|--------|-------|
| Anthropic | `ANTHROPIC_API_KEY` | Paid | Active (primary) | `claude-sonnet-4-6` for main session and delegation; `claude-haiku-4-5` for auxiliary vision. No separate escalation/utility Anthropic tier configured |
| Cerebras | `CEREBRAS_API_KEY` | Free (14,400 RPD) | Active | Fallback #1; also auxiliary.compression and web_extract (zai-glm-4.7); free tier 8K ctx cap |
| SambaNova | `SAMBANOVA_API_KEY` | Free (20 RPD/model) | Active | Fallback #2 (DeepSeek-V3.2); no data training |
| Mistral | `MISTRAL_API_KEY` | Free (~1B tok/month) | Active | Fallback #3 (mistral-large-latest); data training opt-in |
| OpenAI | `OPENAI_API_KEY` | Paid | Key present | Used for: Hindsight embeddings (text-embedding-3-small 1536d) + Graphiti embeddings. NOT in routing config for chat completions |
| Telegram | `TELEGRAM_BOT_TOKEN` | — | Active | Primary mobile notification gateway |
| WhatsApp | `WHATSAPP_*` | — | **Dormant** | Bridge present; intentionally disconnected (npm vulns) |

---

## Python library dependencies (non-standard)

| Library | Purpose | Installed via |
|---------|---------|---------------|
| `python-pptx` | PowerPoint generation | pip |
| `openpyxl` | Excel workbook read/write | pip |
| `xlsxwriter` | Excel workbook generation | pip |
| `matplotlib` | Chart generation for dashboards | pip |
| `seaborn` | Statistical chart generation | pip |
| `markitdown` | Convert docs/PDFs to markdown | pip |
| `python-docx` | Word document read/write | pip |
| `playwright` | Browser automation (Chromium) | pip + `playwright install chromium` |
| `PyYAML` | YAML parsing in scripts | pip |
| `falkordb` | FalkorDB Python client | pip |
| `graphiti-core` | Graphiti knowledge graph client | pip |

---

## OS / host

- Fedora 44 Silverblue (immutable rpm-ostree)
- Kernel: 7.1.8-200.fc44.x86_64
- Home: /var/home/rainbow
- Toolbox: available for mutable container work
- Python: 3.11.15 (Hermes venv); system also has 3.14.6

---

## Active local projects

| Project | Path | Purpose |
|---------|------|---------|
| repo1 (LLM Efficiency Gateway) | `/var/home/rainbow/repo1` | FastAPI gateway applying policy redaction, prompt optimization, and cost-tier model routing. Monorepo with packages: evals, policy, optimizer, router, telemetry. See `docs/repo1-eval-harness.md`. |
