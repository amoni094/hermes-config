# Scripts Inventory

Last updated: 2026-08-30 (added research sweep, news watchdog, skill-wiki, browser-act-guard, working-memory, constraint-binding-lint, diff-impact, tool-auth-gate, critique-bank)

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
| `session-prune.sh` | session-auto-prune | every 240m | Prune stale Hermes sessions from state.db |
| `l1-extract.py` | l1-extract-periodic | every 180m | Extract L1 facts from recent session transcripts |
| `l1-promote.py` | l1-promote-periodic | every 220m | Dual-Track L1 promote (Hindsight path; staggered vs extract) |
| `l1-graphiti-reconcile.py` | l1-graphiti-periodic | every 240m | Reconcile/write L1 facts into Graphiti |
| `l1-gmemory-consolidation.py` | g-memory-tier3-nightly | 0 3 * * * | Nightly Graphiti memory consolidation (tier-3) |
| `memory-ttl-purge.py` | memory-ttl-purge | 0 3 * * * | Expire ephemeral/volatile tiers per config thresholds |
| `hermes-mutation-gate-watch.sh` | hermes-mutation-gate-watch | every 1440m | Check mutation-gate state; alert if gate is wrong |
| `hermes-memory-drift-audit.py` | hermes-memory-drift-audit | every 1440m | Audit durable memory for drift vs actual state |
| `hermes-platform-watchdog.sh` | hermes-platform-watchdog | every 720m | Broad platform health check (config, MCP, Graphiti) |
| `obsidian_weekly_review.sh` | obsidian-weekly-review | 0 17 * * 5 | Weekly Obsidian vault review trigger |
| `omni_skill_scan.py` | omni-skill-quality-scan | 0 3 * * 0 | Weekly skill quality scan |
| `skill_prune_audit.py` | skill-prune-audit | 0 9 1 * * | Monthly skill prune audit |

Agent-mode cron jobs without a dedicated script: `hermes-chat-sync-4h`, `l1-hindsight-promote`, `pending-improvements-review`, `hermes-research-apply`.
| `news_diff_watchdog.py` | news-diff-watchdog | every 90m | Diff-based news signal watcher (HF Papers, Papers With Code, AI blogs) |
| `hermes-research-sweep.py` | hermes-research-weekly | 0 6 * * 2 | Sweep arXiv + multilingual sources across 7 AI agent research categories |
| `skill-wiki.py` | skill-wiki-weekly | 0 6 * * 0 | Generate weekly skill wiki index |

## Utility scripts (run manually or by agent)

| Script | Purpose |
|--------|---------|
| `skillspector_guard.py` | Full skill inventory guard — orphans, duplicates, mis-categorization |
| `skillspector_guard_enforce.sh` | Shell wrapper for skillspector_guard.py with enforce mode |
| `hermes-hud.py` | Local dashboard HUD (task ledger, memory, cron) |
| `hermes-mutation-gate.sh` | Manually toggle the mutation gate on/off |
| `hermes-mutation-gate-watch.sh` | Watch mutation gate state (also cron-backed) |
| `firecrawl_stealth_fetch.py` | Stealth-mode Firecrawl page fetch via headless browser |
| `firecrawl_watchdog.sh` | Firecrawl health-check (also cron-backed) |
| `hindsight-ensure.sh` | Ensure Hindsight service is running/healthy at :9177 |
| `hindsight-reembed.py` | Re-embed Hindsight facts with updated embedding model |
| `l1-graphiti-write.py` | Write facts directly to Graphiti |
| `l1-graphiti-reconcile.py` | Reconcile Graphiti vs L1 promote outputs (also cron-backed) |
| `l1-context-offload.py` | Offload context to symbolic store for long sessions |
| `l1-tracegrant.py` | TraceGrant lifecycle integrity (taint_path + decision_hash) |
| `memory-query-router.py` | Route memory queries across Hindsight/Graphiti/session_search |
| `memory-staleness.py` | Detect and flag stale durable memory entries |
| `memory-provenance.py` | Provenance tracking for memory facts |
| `memory-ttl-purge.py` | TTL purge for tiered memory (also cron-backed) |
| `unified-recall.py` | Unified multi-bank Hindsight recall helper |
| `retry-budget-guard.py` | Enforce config.memory.retry_budgets across writers |
| `issue-to-agents.py` | Route GitHub issues to isolated Hermes subagent sessions |
| `news_diff_watchdog.py` | Diff-based news watchdog: surface changed signals only |
| `am-sentry.py` | Agent/memory sentry checks |
| `qmd-local.sh` | Launch QMD MCP server (mcp_servers.qmd currently **disabled**) |
| `mempalace-mcp.sh` | Launch MemPalace MCP server (currently **disabled**) |
| `stealth-browser-mcp.sh` | Launch Stealth Browser MCP server |
| `skill-router-index.py` | Build/refresh semantic skill routing index |
| `skill-yield-tracker.py` | Track skill yield / usage outcomes |
| `skill-graph-walk.py` | Walk and validate the skill dependency graph |
| `skillopt_score.py` | Score skill quality using SkillOpt rubric |
| `gepa_skill_eval.py` | GEPA-based skill evaluation (genetic-pareto) |
| `validate-skill-ssl.py` | Validate skill SSL (structured skill lifecycle) metadata |
| `skills-commit.sh` | Commit skill changes with correct message format |
| `omni_skill_scan.py` | Scan all skills for quality (also cron-backed) |
| `skill_prune_audit.py` | Audit skills for pruning candidates (also cron-backed) |
| `adversarial_quarantine_review.py` | Review quarantined adversarial findings |
| `trace2skill.py` | Compile trajectories into skill drafts |
| `canvas-offload.py` | Canvas-of-Thought context offload helper |
| `focus_compress.py` | Focused context compression utility |
| `stage-improvement.sh` | Stage autonomous improvement proposals to pending-improvements/ |
| `obsidian_weekly_review.sh` | Weekly Obsidian vault review (also cron-backed) |
| `session-prune.sh` | Prune stale sessions (also cron-backed) |
| `browser_orphan_watchdog.sh` | Kill orphaned browser processes (also cron-backed) |
| `hermes-platform-watchdog.sh` | Platform health watchdog (also cron-backed) |
| `daily-silverblue-update.sh` | Daily Silverblue rpm-ostree / flatpak / toolbox / managed-repo sweep |
| `daily-silverblue-update-login-trigger.sh` | Login-triggered Silverblue update |
| `reboot-required-notify.sh` | Notify when a post-update reboot is required after Silverblue update |
| `groq-split-tunnel.sh` | Route Groq API traffic via split tunnel (reference only; Groq not configured) |
| `browser_act_guard.py` | Browser action guard — validates browser actions against veto rules before execution |
| `test_browser_act_guard.py` | Unit tests for browser_act_guard.py |
| `working-memory.py` | Working memory manager: skill_selection_from_wm + constraint_binding |
| `constraint-binding-lint.py` | Lint skill/config files for missing constraint binding declarations |
| `diff-impact.py` | Compute blast-radius impact diff for proposed code/skill changes |
| `tool-auth-gate.py` | Gate tool invocations against auth/approval requirements |
| `critique-bank.py` | Manage critique bank for adversarial review findings |
| `skill-state.py` | Inspect/set skill state (enabled/disabled/quarantined) |

## Sudoers helpers (not executable scripts — sudoers drop-in files)

| File | Purpose |
|------|---------|
| `rainbow-silverblue-updates.sudoers` | Allow passwordless rpm-ostree upgrade for update automation |
| `rainbow-toolbox-dnf-update.sudoers` | Allow passwordless toolbox dnf update |

## Pending improvements staging

| Directory | Purpose |
|-----------|---------|
| `~/.hermes/cache/pending-improvements/` | Staged autonomous improvement proposals awaiting curator review |
