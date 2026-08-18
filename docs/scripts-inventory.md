# Scripts Inventory

Last updated: 2026-08-18 (20+ new scripts added since 2026-07-03 pass)

All scripts live under `~/.hermes/scripts/` on the local host. Scripts are NOT copied
into this git repo. This doc exists so the purpose of each script is disclosed and
auditable without opening the file.

---

## Cron-backing scripts (run on a schedule)

| Script | Cron job | Schedule | Purpose |
|--------|----------|----------|---------|
| `firecrawl_watchdog.sh` | firecrawl-watchdog | every 10m | Health-check Firecrawl at :3002; alert on failure |
| `browser_orphan_watchdog.sh` | browser-orphan-watchdog | every 30m | Kill orphaned Playwright/Chrome processes |
| `skillspector_guard_enforce.sh` | skillspector-guard | every 240m | Enforce skill-guard checks via skillspector_guard.py |
| `session-prune.sh` | session-auto-prune | every 240m | Prune stale Hermes sessions from session DB |
| `l1-extract.py` | l1-extract-periodic | every 180m | Extract L1 facts from recent session transcripts |
| `l1-promote.py` | l1-promote-periodic | every 220m | Promote extracted L1 facts to Hindsight (script mode) |
| `l1-gmemory-consolidation.py` | g-memory-tier3-nightly | 0 3 * * * | Nightly Graphiti memory consolidation (tier-3) |
| `hermes-mutation-gate-watch.sh` | hermes-mutation-gate-watch | every 1440m | Check mutation-gate state; alert if gate is wrong |
| `hermes-memory-drift-audit.py` | hermes-memory-drift-audit | every 1440m | Audit durable memory for drift vs actual state |
| `hermes-platform-watchdog.sh` | hermes-platform-watchdog | every 720m | Broad platform health check (config, MCP, Graphiti) |
| `obsidian_weekly_review.sh` | obsidian-weekly-review | 0 17 * * 5 | Weekly Obsidian vault review trigger |
| `omni_skill_scan.py` | omni-skill-quality-scan | 0 3 * * 0 | Weekly skill quality scan (scores all 179 skills) |
| `skill_prune_audit.py` | skill-prune-audit | 0 9 1 * * | Monthly skill prune audit |

## Utility scripts (run manually or by agent)

| Script | Purpose |
|--------|---------|
| `skillspector_guard.py` | Full skill inventory guard — detects orphaned, duplicate, mis-categorized skills |
| `skillspector_guard_enforce.sh` | Shell wrapper for skillspector_guard.py with enforce mode |
| `hermes-hud.py` | Local dashboard HUD showing task ledger, memory state, cron status |
| `hermes-mutation-gate.sh` | Manually toggle the mutation gate on/off |
| `hermes-mutation-gate-watch.sh` | Watch mutation gate state (also cron-backed) |
| `firecrawl_stealth_fetch.py` | Stealth-mode Firecrawl page fetch via headless browser |
| `firecrawl_watchdog.sh` | Firecrawl health-check (also cron-backed) |
| `hindsight-ensure.sh` | Ensure Hindsight service is running and healthy at :9177 |
| `hindsight-reembed.py` | Re-embed Hindsight facts with updated embedding model |
| `l1-graphiti-write.py` | Write facts directly to Graphiti (bypasses Hindsight) |
| `l1-context-offload.py` | Offload context to symbolic store for long sessions |
| `memory-query-router.py` | Route memory queries across Hindsight/Graphiti/session_search |
| `memory-staleness.py` | Detect and flag stale durable memory entries |
| `issue-to-agents.py` | Route GitHub issues to isolated Hermes subagent sessions |
| `news_diff_watchdog.py` | Diff-based news watchdog: surface changed signals only |
| `qmd-local.sh` | Launch QMD MCP server (used by mcp_servers.qmd in config.yaml) |
| `mempalace-mcp.sh` | Launch MemPalace MCP server (currently disabled in config.yaml) |
| `stealth-browser-mcp.sh` | Launch Stealth Browser MCP server (from ~/.hermes/mcp/stealth-browser-mcp/) |
| `groq-split-tunnel.sh` | Route Groq API traffic via split tunnel (reference only; Groq not configured) |
| `canvas-offload.py` | Canvas-of-Thought context offload helper |
| `focus_compress.py` | Focused context compression utility |
| `skill-graph-walk.py` | Walk and validate the skill dependency graph |
| `skillopt_score.py` | Score skill quality using SkillOpt rubric |
| `gepa_skill_eval.py` | GEPA-based skill evaluation (genetic-pareto) |
| `validate-skill-ssl.py` | Validate skill SSL (structured skill lifecycle) metadata |
| `skills-commit.sh` | Commit skill changes with correct message format |
| `omni_skill_scan.py` | Scan all skills for quality (also cron-backed) |
| `skill_prune_audit.py` | Audit skills for pruning candidates (also cron-backed) |
| `adversarial_quarantine_review.py` | Review quarantined adversarial findings |
| `stage-improvement.sh` | Stage autonomous improvement proposals to pending-improvements/ dir |
| `obsidian_weekly_review.sh` | Weekly Obsidian vault review (also cron-backed) |
| `session-prune.sh` | Prune stale sessions (also cron-backed) |
| `browser_orphan_watchdog.sh` | Kill orphaned browser processes (also cron-backed) |
| `hermes-platform-watchdog.sh` | Platform health watchdog (also cron-backed) |
| `daily-silverblue-update.sh` | Trigger daily Silverblue rpm-ostree update |
| `daily-silverblue-update-login-trigger.sh` | Login-triggered Silverblue update |
| `reboot-required-notify.sh` | Notify when reboot is required after Silverblue update |

## Sudoers helpers (not executable scripts — sudoers drop-in files)

| File | Purpose |
|------|---------|
| `rainbow-silverblue-updates.sudoers` | Allow passwordless rpm-ostree upgrade for update automation |
| `rainbow-toolbox-dnf-update.sudoers` | Allow passwordless toolbox dnf update |

## Pending improvements staging

| Directory | Purpose |
|-----------|---------|
| `~/.hermes/cache/pending-improvements/` | Staged improvement proposals from autonomous loops; reviewed by curator before applying |

Script: `stage-improvement.sh` — writes YAML-frontmatter proposals to the staging dir.
Usage: `stage-improvement.sh <skill-name> '<description>' <<< 'proposal body'`
