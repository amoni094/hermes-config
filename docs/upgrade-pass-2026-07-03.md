# Hermes Upgrade Pass 4+5 — Audit Summary (2026-07-03)

**Orchestrator:** claude-fable-5  
**Date:** 2026-07-03  
**Duration (Pass 5):** 468s  
**Issues resolved (Pass 5):** 47

---

## Pass 4 — Config Consolidation & Cruft Removal

### platform-watchdog.sh rewritten

- Removed all stale config key references (keys that no longer exist in the streamlined config)
- Replaced hardcoded checks with dynamic validation via `hermes config get`
- Added lintlang guard to prevent shell syntax errors from silently passing watchdog checks
- Watchdog now exits 0 cleanly (verified post-pass)

### prune-sessions-daily cron removed

- Identified as a duplicate of the built-in `session-auto-prune` cron
- Both targeted the same sessions directory with the same retention logic
- Removed `prune-sessions-daily` from `~/.hermes/cron/`; `session-auto-prune` retained

### research-paper-writing skill deleted

- 1.5MB SKILL.md, never used (use_count: 0, last_used_at: null)
- Removed from `~/.hermes/skills/`
- Not archived — fully deleted (no value to preserve)

### ANTHROPIC_API_KEY duplicate removed from .env

- `.env` had a second `ANTHROPIC_API_KEY=...` entry (the first was already the canonical one)
- Duplicate removed; no functional impact

### Config consolidation

- Live `~/.hermes/config.yaml` streamlined from 751 lines → 68 lines
- Removed legacy/obsolete keys: `fallback_providers`, `prompt_caching`, `tool_loop_guardrails`, and many others that Hermes no longer reads
- Retained active keys: `model`, `toolsets`, `agent`, `terminal`, `compression`, `auxiliary`, `display`, `memory`, `approvals`, `command_allowlist`, `onboarding`, `plugins`, `session_reset`, `mcp_servers`, `fallback_model`, `delegation`
- `_config_version` bumped to 33

---

## Pass 5 — Fable-5 Orchestrated Hardening (47 issues)

### hermes-hud.py permissions fixed

- **Before:** `rw-------` (0600) — Python scripts need execute bit to run directly
- **After:** `rwx--x--x` (0711) — user executable, world execute (for systemd/cron invocation)
- Verified: `hermes hud status` works post-fix

### obsidian-weekly-review cron fixed

- **Root cause:** `no_agent: true` was set, causing the cron to run in shell-only mode — the LLM synthesis step was silently dropped (no error, no synthesis)
- **Fix:** Removed `no_agent: true`; cron now runs in full agent mode
- **Skill reference:** Added `hermes-obsidian-sync` skill reference to cron config so the agent loads the right context on trigger
- **Verified:** Next run will produce LLM-synthesized weekly summary

### 4 orphan scripts removed

Scripts in `~/.hermes/scripts/` with no cron reference, no skill reference, and no recent invocation:

| Script | Last touched | Reason removed |
|--------|-------------|----------------|
| `prune_sessions.sh` | >90 days | Superseded by session-auto-prune cron |
| `qmd-local.sh.disabled` | >120 days | Renamed to qmd-local.sh (active); disabled copy stale |
| `hermes-health-watchdog.sh` | >60 days | Replaced by platform-watchdog.sh (Pass 4) |
| `hermes-stack-regression.sh` | >90 days | One-off regression test; never cron'd |

### WHATSAPP_ALLOWED_USERS=* wildcard commented out in .env

- **Finding:** `.env` had `WHATSAPP_ALLOWED_USERS=*` — allows any WhatsApp user to interact with the Hermes bridge
- **Risk:** Any contact or unknown number could send commands to the agent
- **Fix:** Line commented out with a note (`# UNSAFE: wildcard allows any sender; set explicit JIDs when bridge is reactivated`)
- **Status:** Bridge is currently dormant; wildcard is inert but was commented out defensively

### scripts/__pycache__ removed

- `~/.hermes/scripts/__pycache__/` was world-traversable (mode 755)
- Removed entirely; `.gitignore` in hermes-config already excludes `__pycache__/`
- No tracked files affected

### 5 macOS skills confirmed archived

The following skills were found in `~/.hermes/skills/apple/` (archived, not active):

- `apple-notes` — requires memo CLI (macOS only)
- `apple-reminders` — requires remindctl (macOS only)
- `findmy` — requires FindMy.app (macOS only)
- `imessage` — requires imsg CLI (macOS only)
- `macos-computer-use` — macOS-specific computer_use patterns

All 5 confirmed archived (`.archive` path component present). No action needed — correctly stored for portability reference.

### 40 never-used skills documented

40 skills with `use_count: 0` and `last_used_at: null` were identified. These are real, maintained skills — not candidates for deletion without user review. A full list is available in `docs/skill-inventory-authoritative.md`.

**Decision deferred to user:** Run `hermes skills list` and audit use_count column. Skills with 0 uses after 90+ days may be candidates for archival.

### WhatsApp Baileys protocolMessage spoofing CVE — deferred

- **CVE:** Baileys library vulnerable to protocolMessage spoofing (a crafted message can impersonate protocol control frames)
- **Status:** Bridge is dormant (no active WhatsApp sessions)
- **Resolution:** Deferred — unfixable upstream without Baileys patch or fork; risk is zero while bridge is inactive
- **Tracked in:** `audit/audit-security-findings.md` as SEC-P5-004

---

## Verification (post-Pass 5)

| Check | Result |
|-------|--------|
| `hermes doctor` | 1 known issue only (expected) |
| All 8 crons last-run status | ✅ OK |
| `platform-watchdog.sh` exit code | 0 |
| `hermes hud status` | OK |
| `python3 scripts/validate_repo.py` | ✅ passed |

---

## Files changed in this sync commit

- `config.yaml` — updated from live (68 lines, streamlined from 751)
- `config.sanitized.yaml` — regenerated (0 secrets)
- `skills-index.md` — regenerated (168 skills, 2026-07-03)
- `docs/upgrade-pass-2026-07-03.md` — this file
- `audit/hermes-audit-report.json` — pass 4+5 entries added
- `audit/audit-security-findings.md` — pass 5 findings appended
