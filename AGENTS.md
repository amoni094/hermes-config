# AGENTS.md for hermes-config

Purpose:
- keep this repo as a sanitized, private snapshot of Hermes configuration and workflow state
- make validation and export hygiene explicit for future agent passes

Rules:
1. Never add live secrets or state from `~/.hermes`.
   - forbidden: `.env`, `auth.json`, session DBs, raw logs, gateway state, process state, unredacted chat IDs
2. Treat every config or cron snapshot refresh as a security-sensitive export.
   - prefer sanitized/redacted copies only
   - read back changed files before commit
3. Keep repo automation low-friction and inspectable.
   - prefer stdlib Python scripts
   - fail fast with clear errors
   - default destructive migrations to dry-run unless explicit apply is requested
4. Verification before completion is mandatory.
   - run `python3 scripts/validate_repo.py`
   - run `python3 -m compileall scripts`
   - if inventory generation logic changed, rerun `python3 scripts/generate_skill_inventory.py`
5. Keep documentation aligned with live repo posture.
   - README should continue to say the export is sanitized
   - docs/current-workflow.md should continue to list major exclusions

Notes:
- This repo intentionally documents operational surfaces and findings, but should not become a dump of raw runtime state.
- Prefer additive guardrails over broad, noisy scanners that would create false confidence without local verification.
