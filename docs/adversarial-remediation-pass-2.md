# Adversarial Remediation Pass 2

Generated: 2026-06-30

## Scope

This pass repeated the adversarial review with fresh optimization research and then implemented only the changes that were both:
- high-confidence improvements
- safe to apply without guessing about the user's external workflow intent

## Research signals used

From current Hermes docs and live inspection:
- keep prompt-support files compact and explicit
- verify live provider/runtime state instead of trusting stale config values
- use Hermes-native config/doctor/cron commands as the primary source of truth
- treat background automation and optional integrations as first-class operational surfaces, not hidden implementation details

Relevant references consulted during this pass:
- Hermes docs: context compression and caching
- Hermes docs: providers and auxiliary-model behavior
- Hermes docs/user stories: cost/overhead and skill-routing pressure

## Fresh findings

### 1. Real qwen helper-context mismatch

Verified live via the local Ollama API:
- configured `qwen3:8b` context in Hermes: `64000`
- actual runtime `qwen3:8b` context: `40960`

This was a genuine correctness issue, not just a preference.

### 2. Curator backup posture still unsafe-by-omission

Verified live:
- `curator.enabled: false`
- `curator.backup.enabled: false` before this pass

That meant a future move toward curator-driven maintenance would start from a weaker rollback posture than necessary.

### 3. Operational policy existed mostly in scattered notes

A root `~/AGENTS.md` already existed, which is good, but it was still missing the high-signal rules that matter most for Hermes self-maintenance:
- export hygiene
- verification defaults
- cron/watchdog semantics
- compact delegation packet expectations

### 4. Optional-integration ambiguity remains

`hermes doctor` still reports WhatsApp bridge dependency vulnerabilities.

This remains a live risk surface, but it was not safe to silently disable because that could break a real user workflow. I documented it instead of forcing a behavioral change.

## Changes implemented

### Live workspace policy hardening
Updated:
- `/var/home/rainbow/AGENTS.md`

Added:
- Hermes-native verification defaults
- explicit export-hygiene rules
- cron/watchdog policy and CLI delivery semantics
- sharper delegation-packet guidance

### Live Hermes config improvements
Updated live config:
- set `curator.backup.enabled: true`
- corrected `custom_providers.local.models.qwen3:8b.context_length` from `64000` to `40960`

Why these were chosen:
- both are high-confidence, low-ambiguity fixes
- neither changes approval posture or disables user-facing integrations
- both directly address adversarial findings with verifiable evidence

### Repo additions
Added:
- `docs/local-aux-context-verification.md`
- `docs/operations-surface-register.md`
- this file

Refreshed:
- `config.sanitized.yaml`
- `README.md`

## Changes intentionally not forced

### `approvals.mode`
I did not flip `manual` -> `smart` automatically.

Reason:
- that is a workflow-trust tradeoff, not a correctness bug
- it changes how destructive-command approvals behave

### WhatsApp bridge state
I did not disable or remediate the WhatsApp bridge automatically.

Reason:
- `hermes doctor` proves dependency risk, but not whether the user currently depends on the bridge
- changing it would be an externally visible behavior change

Follow-up decision after this pass:
- the user wants WhatsApp kept disconnected/intentionally dormant
- future optimization work should document that posture, not reconnect the bridge unless explicitly requested

## Verification evidence

Verified by:
- `hermes config check`
- `hermes doctor`
- `hermes cron list --all`
- direct Ollama runtime inspection against `http://localhost:11434/api/show`
- readback of:
  - `/var/home/rainbow/AGENTS.md`
  - `/var/home/rainbow/hermes-config/config.sanitized.yaml`
  - `/var/home/rainbow/hermes-config/docs/local-aux-context-verification.md`
  - `/var/home/rainbow/hermes-config/docs/operations-surface-register.md`

## Bottom line

This pass converted two important adversarial findings from “documented risk” into actual remediations:
- the helper-context mismatch is now truthful in config
- curator now has backup posture enabled before any future broader maintenance automation

The main unresolved adversarial item is still the WhatsApp bridge dependency surface, which now has clearer documentation but still needs an explicit keep-or-retire decision.
