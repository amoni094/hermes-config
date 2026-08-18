# Operations Surface Register

Generated: 2026-08-18 (refreshed from 2026-07-03; 7 new jobs added, job names corrected)

This note records the live cron/watchdog estate and the current posture of optional integrations.

## Cron and watchdog jobs

Verified with `hermes cron list --all` on 2026-08-18. All 15 jobs active, all last-run: ok.

| Job | Schedule | Deliver | Mode | Purpose |
|-----|----------|---------|------|---------|
| `hermes-chat-sync-4h` | every 240m | `local` | agent | Sync recent Hermes activity into Obsidian vault |
| `hermes-mutation-gate-watch` | every 1440m | `local` | script | Check mutation-gate state; alert if wrong |
| `hermes-memory-drift-audit` | every 1440m | `local` | script | Audit durable memory drift vs actual state |
| `skillspector-guard` | every 240m | `local` | script | Enforce skill-guard checks |
| `firecrawl-watchdog` | every 10m | `local` | script | Firecrawl health check at :3002 |
| `hermes-platform-watchdog` | every 720m | `local` | script | Broad platform health (config, MCP, Graphiti) |
| `session-auto-prune` | every 240m | `local` | script | Prune stale Hermes sessions from session DB |
| `obsidian-weekly-review` | 0 17 * * 5 | `local` | agent+script | Weekly Obsidian vault review |
| `browser-orphan-watchdog` | every 30m | `local` | script | Kill orphaned Playwright/Chrome processes |
| `l1-extract-periodic` | every 180m | `local` | script | Extract L1 facts from session transcripts |
| `l1-hindsight-promote` | every 240m | `local` | agent | Promote extracted L1 facts to Hindsight |
| `l1-promote-periodic` | every 220m | `local` | script | L1 promote pipeline (script mode, separate interval to avoid race) |
| `omni-skill-quality-scan` | 0 3 * * 0 | `local` | script | Weekly skill quality scan across all 179 skills |
| `skill-prune-audit` | 0 9 1 * * | `local` | script | Monthly skill prune audit |
| `g-memory-tier3-nightly` | 0 3 * * * | `local` | script | Nightly Graphiti memory consolidation |

## Delivery semantics note

- `deliver: local` means job output is stored locally in `~/.hermes/cron/output/`; it does not message the CLI terminal.
- `deliver: origin` is meaningful only for jobs created from gateway-connected chats (Telegram etc.).
- All current jobs use `deliver: local`.

## Optional integration posture

### Healthy / intentionally in use
- Telegram gateway: active (primary mobile notifications)
- Firecrawl: active local endpoint at :3002 (watchdog every 10m)
- SearXNG: active at local port :8888
- Graphiti MCP: active at :8765, FalkorDB backend at :6379
- Hindsight: active at :9177, API-based (Anthropic + OpenAI embeddings) — Ollama NOT used

### Present but dormant
- WhatsApp bridge: variables present; intentionally disconnected/dormant (npm vulns)
- MemPalace MCP: script present, disabled in config.yaml

### Removed
- Ollama: uninstalled 2026-07-12. Neither Hindsight nor Graphiti use local Ollama anymore.
