# External Apps and Services Register

Last updated: 2026-08-26 (main model xAI grok-4.5; Brave primary search; QMD disabled; Hindsight systemd; dashboard :9119)

All external apps, local services, and third-party integrations this Hermes instance depends on.

---

## Local services (self-hosted, running on this machine)

| Service | Port / path | Purpose | Status |
|---------|------------|---------|--------|
| Firecrawl | `http://127.0.0.1:3002` | Web crawl / stealth scrape for research | Active (watchdog every 10m) |
| Graphiti MCP | `http://127.0.0.1:8765/mcp/` | Knowledge graph MCP server | Active |
| FalkorDB | graph backend for Graphiti | Graph DB | Active |
| Hindsight | `http://127.0.0.1:9177` | Vector memory store (API-based; systemd user unit) | Active |
| SearXNG | `http://127.0.0.1:8888` | Local search index (spare; not primary backend) | Active |
| Hermes dashboard | `http://127.0.0.1:9119` | Local WebUI | Active with gateway |

**Note: Ollama is UNINSTALLED (2026-07-12).** Neither Hindsight nor Graphiti use local LLMs.
All inference uses cloud APIs (xAI primary chat; Anthropic vision/Hindsight LLM; OpenAI embeddings; Cerebras/SambaNova/Mistral fallbacks).

---

## Hermes plugins / integrations

| Plugin/Integration | Type | Status | Notes |
|-------------------|------|--------|-------|
| orca-status | Hermes plugin | Active | Only enabled plugin in config.yaml |
| flowstate-qmd | Integration | Present / dormant | QMD MCP **disabled** in config.yaml |
| stealth-browser-mcp | MCP integration | Active (defer_loading) | `~/.hermes/mcp/stealth-browser-mcp/` |

---

## Cloud / external providers

| Provider | Key env var | Status | Notes |
|----------|------------|--------|-------|
| xAI | `XAI_API_KEY` | Active (primary chat) | `grok-4.5` main session model; context_length 200000 |
| Anthropic | `ANTHROPIC_API_KEY` | Active (aux/vision/Hindsight LLM) | `claude-haiku-4-5` vision; Hindsight inference; optional long-context escalation |
| Cerebras | `CEREBRAS_API_KEY` | Active | Fallback #1 `gpt-oss-120b`; free tier 8K ctx cap |
| SambaNova | `SAMBANOVA_API_KEY` | Active | Fallback #2 `DeepSeek-V3.2`; compression fallback hop |
| Mistral | `MISTRAL_API_KEY` | Active | Fallback #3 `mistral-large-latest`; delegation + most auxiliary routes use `mistral-small-latest` |
| OpenAI | `OPENAI_API_KEY` | Key present | Embeddings (Hindsight + Graphiti); custom_provider models gpt-5.4/5.5/5.6-sol for adversarial/override use — not default chat routing |
| Brave Search | `BRAVE_SEARCH_API_KEY` / config `web.brave_api_key` | Active | Primary `web.search_backend=brave` |
| Telegram | `TELEGRAM_BOT_TOKEN` (+ allowed users / home channel) | Active | Primary mobile notification gateway |
| WhatsApp | `WHATSAPP_*` | **Dormant** | Bridge present; intentionally disconnected |

Env keys present (names only; values never exported): ANTHROPIC_API_KEY, BRAVE_SEARCH_API_KEY, BROWSERBASE_*, BROWSER_*, CAMOFOX_URL, CEREBRAS_API_KEY, FIRECRAWL_API_URL, HINDSIGHT_LLM_API_KEY, IMAGE_TOOLS_DEBUG, MISTRAL_API_KEY, MOA_TOOLS_DEBUG, OPENAI_API_KEY, SAMBANOVA_API_KEY, SEARXNG_URL, SERPAPI_API_KEY, TELEGRAM_*, TERMINAL_*, VISION_TOOLS_DEBUG, WEB_TOOLS_DEBUG, WHATSAPP_*, XAI_API_KEY.

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
- Kernel: 7.1.10-200.fc44.x86_64
- Home: /var/home/rainbow
- Toolbox: available for mutable container work
- Python: Hermes venv + system Python

---

## Active local projects

| Project | Path | Purpose |
|---------|------|---------|
| repo1 (LLM Efficiency Gateway) | `/var/home/rainbow/repo1` | FastAPI gateway applying policy redaction, prompt optimization, and cost-tier model routing. See `docs/repo1-eval-harness.md`. |
| hermes-config (this repo) | `/var/home/rainbow/hermes-config` | Sanitized config + ops docs mirror |
| hermes-agent (upstream checkout) | `/var/home/rainbow/.hermes/hermes-agent` | Local agent source tree (not mirrored here) |
