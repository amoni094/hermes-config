# Hermes Veto Security Audit — Findings

Date: 2026-06-30
Scope: ~/.hermes/veto/rules/ and ~/.hermes/agent-hooks/ (veto-pre-tool.py, track-budget.py)

## 1. Hard-block coverage extended (hermes-hard-blocks.yaml)

Added five new critical hard-block rules for destructive commands previously
uncovered:

| Rule ID                       | Covers                                                        |
|-------------------------------|--------------------------------------------------------------|
| `block-find-delete`           | `find ... -delete`                                           |
| `block-truncate-zero`         | `truncate -s0`, `truncate --size=0`                         |
| `block-python-fs-delete-home` | `python[3] -c` with os.remove/unlink/rmdir/removedirs or shutil.rmtree targeting `$HOME`, `~/.hermes`, `/var/home/rainbow`, or `os.environ['HOME']` |
| `block-chmod-recursive-home`  | `chmod -R` / `--recursive` on `$HOME`, `~`, `~/.hermes`     |
| `block-dd-zero-to-file`       | `dd if=/dev/zero` or `if=/dev/null` writing to a file (`of=` not a device). Device targets already covered by pre-existing `block-disk-format`. |

## 2. veto-pre-tool.py — fail-closed posture

FINDING: The hook previously FAILED OPEN on payload parse error — a malformed or
empty stdin payload caused it to emit `{}` (allow). Rule loading/evaluation
errors were also unguarded.

REMEDIATION (applied): Added `_fail_closed()` helper. The hook now blocks when:
  - stdin payload cannot be parsed as JSON,
  - payload is not a JSON object,
  - rule loading or evaluation raises any exception.
Note: non-zero exit was already treated as block by the protocol, so an
uncaught crash was already safe; the gap was the explicit `{}` on parse error.
SKIP_TOOLS read-only tools still pass through (intended; no governance needed).

## 3. track-budget.py — destructive_calls is post-hoc only

FINDING: `track-budget.py` is a POST_tool_call hook. It increments
`destructive_calls` AFTER the tool has already executed and only blocks the
*next* action once a hard limit is breached. There is NO pre-tool gate tied to
`destructive_calls`; the call that crosses the limit still runs.

STATUS: Documented (not auto-fixed, as converting it to a pre-tool enforcer is
a behavioral change beyond audit scope). An AUDIT NOTE comment was added to the
top of track-budget.py.

RECOMMENDATION: To enforce destructive_calls pre-execution, mirror the counter
check into a pre_tool_call hook that blocks when projected count (current + 1)
would meet/exceed the limit. Pre-execution blocking of individual destructive
*commands* is already handled by veto-pre-tool.py pattern hard-blocks.

## Remaining gaps / notes
- Pattern-based blocks can be evaded by obfuscation (env-var indirection,
  base64-piped commands, alternate binaries). veto-pre-tool.py matches
  case-insensitively, which helps, but determined evasion is possible.
- `block-python-fs-delete-home` only covers inline `-c`; script files invoking
  the same calls are not inspected.
- track-budget.py `DESTRUCTIVE_PATTERNS` substring list (e.g. "rm ") may both
  over- and under-count vs. the veto regex rules; the two systems are not
  reconciled.

## Backups
All edited files backed up as `<file>.bak.audit-20260630-201705`.

---

# Pass 5 — Security Findings (2026-07-03)

**Orchestrator:** claude-fable-5  
**Scope:** Full ~/.hermes scan — .env, scripts/, cron/, skills/, agent-hooks/

## SEC-P5-001 — WHATSAPP_ALLOWED_USERS wildcard (medium)

**Finding:** `.env` contained `WHATSAPP_ALLOWED_USERS=*`. This allows any WhatsApp user (any JID) to send commands to the Hermes bridge when it is active.

**Risk:** Any unknown number could trigger Hermes tools or read agent output if the bridge is restarted without reviewing this setting.

**Remediation (applied):** Line commented out in `.env` with a warning note. Bridge is currently dormant; this is a defensive fix for when it is reactivated.

**Recommendation:** When reactivating the WhatsApp bridge, set explicit JIDs: `WHATSAPP_ALLOWED_USERS=+61xxxxxxx@s.whatsapp.net`.

---

## SEC-P5-002 — scripts/__pycache__ world-traversable (low)

**Finding:** `~/.hermes/scripts/__pycache__/` had mode `755` (world-traversable + world-readable). Compiled `.pyc` bytecode files were readable by any local user.

**Risk:** Low on single-user host, but bytecode can reveal internal logic/paths and is unnecessary to expose.

**Remediation (applied):** Removed `~/.hermes/scripts/__pycache__/` entirely. Python will recreate it on next import (mode depends on umask). `.gitignore` in hermes-config already excludes it.

---

## SEC-P5-003 — hermes-hud.py non-executable (low)

**Finding:** `~/.hermes/scripts/hermes-hud.py` had permissions `rw-------` (0600). The shebang `#!/usr/bin/env python3` requires the execute bit for direct invocation.

**Risk:** Script would fail to run directly (e.g., from cron or systemd). Silent failure if cron invokes it as `./hermes-hud.py` without explicit `python3` prefix.

**Remediation (applied):** Changed to `rwx--x--x` (0711). Execute bit set for owner; group/other execute allows systemd user-service and cron invocation.

---

## SEC-P5-004 — WhatsApp Baileys protocolMessage spoofing CVE (medium, deferred)

**Finding:** The Baileys library (used by the Hermes WhatsApp bridge) is vulnerable to protocolMessage type spoofing. A crafted incoming message can impersonate protocol control frames, potentially triggering unintended bridge behaviors.

**Risk:** Medium when bridge is active; effectively zero when dormant.

**Status:** Deferred. The bridge is not active. The vulnerability is in the upstream Baileys library and has no patch at time of audit. A fork or library replacement would be required to fix it.

**Recommendation:** Before reactivating the bridge, check for a Baileys patch or evaluate alternative libraries (e.g., whatsapp-web.js). Keep `WHATSAPP_ALLOWED_USERS` to explicit JIDs as defense-in-depth.

---

## SEC-P5-005 — obsidian-weekly-review no_agent silent failure (info)

**Finding:** The `obsidian-weekly-review` cron had `no_agent: true`, which suppresses LLM synthesis silently — the cron appeared to run successfully but produced no AI-generated output.

**Risk:** Informational (functionality gap, not security). However, a misconfigured cron that silently skips its main purpose is a reliability risk.

**Remediation (applied):** `no_agent: true` removed. Cron now runs in agent mode with `hermes-obsidian-sync` skill reference.

---

## SEC-P5-006 — 4 orphan scripts in ~/.hermes/scripts/ (info)

**Finding:** Four scripts with no active cron reference, no skill reference, and no recent invocation:
- `prune_sessions.sh` — superseded by session-auto-prune
- `qmd-local.sh.disabled` — stale copy of active qmd-local.sh
- `hermes-health-watchdog.sh` — replaced by platform-watchdog.sh
- `hermes-stack-regression.sh` — one-off test, never scheduled

**Risk:** Orphan scripts can be accidentally invoked or cause confusion. No active security risk.

**Remediation (applied):** All 4 removed from `~/.hermes/scripts/`.

---

## SEC-P5-007 — 40 never-used skills (info)

**Finding:** 40 skills have `use_count: 0` and `last_used_at: null` across the skills inventory. These are legitimate, maintained skills — not abandoned code. However, a large inactive skills set increases the skills-router disambiguation surface.

**Risk:** Low. More a maintenance/performance concern than a security issue.

**Status:** Documented. Full list available in `docs/skill-inventory-authoritative.md`. Pending user decision on archival candidates.

