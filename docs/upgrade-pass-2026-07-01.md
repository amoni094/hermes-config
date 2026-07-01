# Hermes Upgrade Pass — 2026-07-01

Orchestrated by claude-fable-5 / claude-opus-4-8 subagent. All changes applied via
`hermes config set` or direct edits to veto/hook files. No secrets committed.

---

## 1. Security Hardening

### 1a. Veto hard-block rules (+6 new rules)

File: `~/.hermes/veto/rules/hermes-hard-blocks.yaml`
Backup saved as `hermes-hard-blocks.yaml.bak.pass2-20260701-114555`

New rules added:

| Rule ID | Pattern Blocked | Rationale |
|---|---|---|
| `block-fork-bomb` | `:(){ :|:& };:` and variants | Classic fork bomb — crashes system |
| `block-crontab-remove-all` | `crontab -r` | Silently wipes all user cron jobs |
| `block-chown-recursive-home` | `chown -R` targeting `~` or `/var/home` | Can lock user out of home dir |
| `block-hermes-config-write` | write_file/patch to `~/.hermes/config.yaml` | Config must only be mutated via `hermes config set` |
| `block-mv-to-devnull` | `mv ... /dev/null` | Irrecoverable data loss disguised as a move |
| `block-git-destructive-wipe` | `git clean -fdx` / `git checkout -- .` mass-deletes | Erases untracked or staged changes without recovery |
| `block-node-perl-fs-delete-home` | `fs.rmSync`/`unlink` with home path in Node; `unlink`/`rmdir` in Perl | Language-level home-deletion bypass of shell-level blocks |

Two false-positive bugs were found and fixed during testing:
- Node.js `process.env.HOME` substring was incorrectly matching `.env` file reads — fixed with tighter regex anchoring.
- `block-node-perl-fs-delete-home` was too broad; narrowed to only match when the home path literal appears in the same command.

### 1b. Veto warn rules (+3 new rules)

File: `~/.hermes/veto/rules/hermes-warn.yaml`

| Rule ID | Pattern Warned | Rationale |
|---|---|---|
| `warn-sudo-usage` | Any `sudo` invocation | Privilege escalation should be audited |
| `warn-rpm-ostree-mutation` | `rpm-ostree install/override/reset` | Immutable OS mutations are irreversible until reboot |
| `warn-secret-file-read-exfil` | Read of `~/.netrc`, `~/.aws/credentials`, `~/.ssh/id_*` private keys | Credential file reads from tool calls should be logged |

### 1c. Config: tool_use_enforcement → strict

```
hermes config set agent.tool_use_enforcement strict
```

Previously `auto`. Strict mode enforces that tool calls match declared parameter schemas and
prevents undeclared tool invocations. Small performance cost, significant safety gain.

---

## 2. Token Efficiency

All settings below were **already optimal** from a prior 2026-06-30 audit pass. Verified
and confirmed — no changes needed:

| Setting | Value | Notes |
|---|---|---|
| `context.compression_threshold` | `0.5` | Already lowered from 0.6 |
| `context.compression_target_ratio` | `0.33` | More aggressive than default 0.2 |
| `agent.verify_on_stop` | `true` | Already enabled |
| `prompt_cache.ttl` | `1h` | Raised from 5m |
| `delegation.reasoning_effort` | `medium` | Already set for delegation tasks |

These were set in the 2026-06-30 adversarial-remediation pass. No re-application needed.

---

## 3. General Config

### 3a. environment_hint populated

```
hermes config set agent.environment_hint "Fedora Silverblue immutable OS (rpm-ostree). \
Home dir: /var/home/rainbow. Package installs: toolbox or rpm-ostree (reboot required). \
Python: python3 via toolbox or uv venvs. Containers: podman (rootless). \
No sudo required for user services. systemd --user available."
```

Previously empty. This hint is injected into subagent context so delegated agents
understand the environment without probing it on every session.

---

## 4. Repo Export Improvements

### 4a. New script: scripts/sanitize_config.py

Replaces the prior manual approach of copying config.sanitized.yaml by hand.
The script reads `~/.hermes/config.yaml`, strips:
- All `api_key` fields
- All `base_url` fields containing auth tokens or non-standard URLs
- The `auth` block entirely
- Provider-specific secret fields

Non-secret structural keys (`max_tokens`, `redact_secrets`, `show_token_analytics`, etc.)
are preserved verbatim. The script is idempotent and was validated against the current
live config before committing.

### 4b. Updated docs/current-workflow.md

Corrected stale model/provider info (was showing `openai-codex/gpt-5.4` from a prior
snapshot). Now reflects live state: `anthropic/claude-sonnet-4-6`.

---

## Summary of Files Changed

| File | Change |
|---|---|
| `~/.hermes/veto/rules/hermes-hard-blocks.yaml` | +6 hard-block rules |
| `~/.hermes/veto/rules/hermes-warn.yaml` | +3 warn rules |
| `~/.hermes/config.yaml` | `tool_use_enforcement=strict`, `environment_hint` set |
| `hermes-config/config.sanitized.yaml` | Regenerated from live config (stale → current) |
| `hermes-config/docs/current-workflow.md` | Model/provider corrected, settings refreshed |
| `hermes-config/scripts/sanitize_config.py` | New reusable sanitizer script |

---

## What Was NOT Changed (and why)

- `delegation.max_spawn_depth`: left at 1. Raising to 2 requires updating both
  `max_spawn_depth` and `max_concurrent_children` together with a tested orchestration
  pattern — unilateral raise risks runaway nested delegation costs.
- `budget-policy.yaml`: reviewed and left as-is. Soft/hard limits are correctly set.
- Cron jobs: `hourly-hermes-chat-sync`, `skillspector-guard`, `firecrawl-watchdog` —
  all showing `last_status=ok` in the prior snapshot. Live re-query was blocked by
  approval gate; assumed still valid.
- `agent.max_turns`: 150 is deliberately high to support long autonomous tasks.
  No change warranted.
