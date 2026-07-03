# Scripts Inventory

Last updated: 2026-07-03

All scripts live under `~/.hermes/scripts/` on the local host. This file
documents what each script does and which ones are referenced by cron jobs.
Scripts are NOT copied into this git repo (they may contain paths, env refs,
or internal logic not safe for sanitized snapshot). This doc exists so the
purpose of each script is disclosed and auditable without opening the file.

---

## Cron-backing scripts (run on a schedule)

| Script | Cron job | Schedule | Purpose |
|--------|----------|----------|---------|
| `firecrawl_watchdog.sh` | firecrawl-watchdog | every 10m | Health-check Firecrawl at :3002; alert on failure |
| `skillspector_guard_enforce.sh` | skillspector-guard | every 240m | Enforce skill-guard checks via skillspector_guard.py |
| `session-prune.sh` | session-auto-prune | every 240m | Prune stale Hermes sessions from session DB |
| `hermes-mutation-gate-watch.sh` | hermes-mutation-gate-watch | every 1440m | Check mutation-gate state; alert if gate is wrong |
| `hermes-memory-drift-audit.py` | hermes-memory-drift-audit | every 1440m | Audit durable memory for drift vs actual state |
| `hermes-platform-watchdog.sh` | hermes-platform-watchdog | every 720m | Broad platform health check (config, MCP, Ollama, Graphiti) |
| `obsidian_weekly_review.sh` | obsidian-weekly-review | 0 17 * * 5 | Weekly Obsidian vault review trigger |

## Utility scripts (run manually or by agent)

| Script | Purpose |
|--------|---------|
| `skillspector_guard.py` | Full skill inventory guard — detects orphaned, duplicate, mis-categorized skills |
| `hermes-hud.py` | Local dashboard HUD showing task ledger, memory state, cron status |
| `firecrawl_stealth_fetch.py` | Stealth-mode Firecrawl page fetch via headless browser |
| `hermes-mutation-gate.sh` | Manually toggle the mutation gate on/off |
| `hermes-evolve-skill.sh` / `hermes-evolution-promote.sh` / `hermes-evolution-review.sh` | Hermes skill evolution loop helpers |
| `issue-to-agents.py` | Route GitHub issues to isolated Hermes subagent sessions |
| `news_feed_ingest.py` | Ingest news feeds into QMD/Obsidian for research pipeline |
| `news_diff_watchdog.py` | Diff-based news watchdog: surface changed signals only |
| `render_social_page.py` | Render social signal aggregate page for local dashboard |
| `social_signals.py` | Pull and score social signals (Reddit, HN) |
| `worldmonitor_news_signal.py` | World Monitor news signal extractor |
| `worldmonitor_reseed_reddit.py` | Reseed World Monitor Reddit sources |
| `worldmonitor-start.sh` | Start World Monitor service |
| `groq-split-tunnel.sh` | Route Groq API traffic via split tunnel (Groq blocks datacenter IPs) |
| `qmd-local.sh` | Launch QMD MCP server (used by mcp_servers.qmd in config.yaml) |
| `mempalace-mcp.sh` | Launch MemPalace MCP server (currently disabled in config.yaml) |
| `stealth-browser-mcp.sh` | Launch stealth-browser MCP server |
| `skills-commit.sh` | Commit current skills snapshot to hermes-config git |
| `reboot-required-notify.sh` | Notify when a reboot is required (rpm-ostree pending) |
| `daily-silverblue-update.sh` / `daily-silverblue-update-login-trigger.sh` | Fedora Silverblue layered package auto-update |

## Sudoers / access files

| File | Purpose |
|------|---------|
| `rainbow-silverblue-updates.sudoers` | Allow rainbow user to run Silverblue update commands without password |
| `rainbow-toolbox-dnf-update.sudoers` | Allow rainbow user to run toolbox dnf commands without password |

These are excluded from git per `.gitignore` (they are host-specific and may
reference exact binary paths).

---

## Repo audit scripts (committed to this git, in scripts/)

These scripts are safe to commit — they contain no secrets and operate on
the snapshot repo itself:

| Script | Purpose |
|--------|---------|
| `generate_skill_inventory.py` | Generate skills-index.md from local skills directory |
| `migrate_skill_usage.py` | Migrate skill usage references after a rename/move |
| `sanitize_config.py` | Redact secrets from config.yaml → config.sanitized.yaml |
| `validate_repo.py` | Validate sanitized config, cron snapshot, .gitignore, README integrity |
