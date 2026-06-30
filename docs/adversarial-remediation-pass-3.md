# Adversarial Remediation Pass 3

Generated: 2026-06-30

## Scope

This pass repeated the hostile review of the `hermes-config` repository itself, with extra emphasis on:
- repository-local guardrails
- safer maintenance scripts
- validation that catches export hygiene regressions before commit

It also incorporated fresh external research on two themes:
- repo/instruction optimization for agent efficiency
- CI/repository hardening patterns for security-sensitive automation

## Research signals used

### Repository-level optimization
From the 2026 AGENTS.md efficiency study (`arXiv:2601.20404v2`):
- root-level `AGENTS.md` files measurably reduced median runtime and token usage for coding agents
- persistent repo guidance is more reliable than re-explaining workflow rules ad hoc
- the best value comes from compact, actionable instructions rather than sprawling prose

### Tool and automation design
From Anthropic's tooling guidance (`https://www.anthropic.com/engineering/writing-tools-for-agents`):
- agent-facing tools/scripts should expose clear contracts, return meaningful errors, and avoid ambiguous side effects
- smaller, sharper tool surfaces beat clever but opaque machinery
- evaluation loops should use realistic tasks and fresh verification, not only intuition

### Workflow hardening
From current GitHub Actions hardening guidance (Orca Security overview: `https://orca.security/resources/blog/github-actions-hardening/`):
- CI/repo automation should follow least surprise, least privilege, and defense in depth
- mutable, under-validated automation becomes a supply-chain risk even in otherwise small repos
- secret scanning and redaction checks are only useful if they are explicit and verifiable, not assumed

## Fresh findings

### 1. Repo had no local validation gate
The export relied mostly on operator care plus scattered docs.

Impact:
- easy to regress redaction or export hygiene silently
- no single command verified the repo's core safety properties

### 2. Migration script was too easy to run destructively
`scripts/migrate_skill_usage.py` previously rewrote the live `~/.hermes/skills/.usage.json` immediately on invocation.

Impact:
- unnecessary blast radius for a script that should be reversible and deliberate
- awkward to inspect planned changes without touching live state

### 3. Inventory generator lacked failure boundaries
`scripts/generate_skill_inventory.py` used direct `check_output()` without timeout or explicit error shaping and wrote outputs non-atomically.

Impact:
- hangs or partial writes could leave the repo in a misleading state
- CLI parsing failures would be harder to diagnose quickly

### 4. Repo hygiene did not ignore Python cache artifacts
The repo ignored secret-bearing runtime files, but not generated Python cache noise.

Impact:
- easy to pollute status/diffs during verification runs
- avoidable review noise in a repo that should stay low-entropy

## Changes implemented

### Repo guardrails
Added:
- `AGENTS.md`
- `scripts/validate_repo.py`

What they enforce:
- required secret/state exclusions remain in `.gitignore`
- `config.sanitized.yaml` does not contain non-empty sensitive-looking key fields
- `cron.snapshot.json` origin identifiers remain redacted/null
- key docs still state the sanitized-export posture
- Python scripts compile cleanly
- tracked Python cache artifacts are rejected

### Script hardening
Updated:
- `scripts/generate_skill_inventory.py`
- `scripts/migrate_skill_usage.py`

Hardening applied:
- atomic writes for generated outputs
- explicit subprocess timeout and clearer failure messages in the inventory generator
- dry-run default for usage migration; `--apply` now required for live rewrite
- target-skill existence validation before usage migration
- clearer reporting of migration mode and outcome

### Repo hygiene
Updated:
- `.gitignore`
- `README.md`

Changes:
- ignore `__pycache__/` and `*.py[cod]`
- document the new validation script and safer migration semantics

### Regenerated outputs
Refreshed:
- `docs/skill-inventory-authoritative.md`
- `docs/skill-inventory-authoritative.json`
- `docs/skill-usage-migration-report.md`

## Why these changes were chosen

These fixes met the bar for this pass because they are:
- high-confidence and locally verifiable
- directly responsive to real repo-level failure modes
- low-risk to the user's live Hermes workflow unless explicitly invoked with `--apply`

I intentionally did not force broader behavioral changes like approval-mode flips or optional integration retirement in this pass, because those still require workflow-intent decisions rather than repo-guardrail corrections.

## Verification evidence

Verified by:
- `python3 -m compileall scripts`
- `python3 scripts/validate_repo.py`
- `python3 scripts/generate_skill_inventory.py`
- `python3 scripts/migrate_skill_usage.py`
- `git diff -- scripts/validate_repo.py scripts/generate_skill_inventory.py scripts/migrate_skill_usage.py .gitignore README.md AGENTS.md docs/adversarial-remediation-pass-3.md docs/skill-inventory-authoritative.md docs/skill-inventory-authoritative.json docs/skill-usage-migration-report.md`

## Bottom line

This pass moved the repo from "careful but mostly manual" toward "self-checking and safer by default".

The biggest improvement is not a new feature; it is that future export/maintenance passes now have:
- a repo-local instruction file
- a one-command validation gate
- safer script defaults for live-state mutation
