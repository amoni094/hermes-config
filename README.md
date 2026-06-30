# hermes-config

Private repository snapshot of the current local Hermes configuration and workflow.

Contents:
- `config.sanitized.yaml` — sanitized copy of the active Hermes config
- `cron.snapshot.json` — redacted cron/job snapshot
- `docs/current-workflow.md` — runtime/workflow summary
- `docs/skills-inventory.md` — installed skill inventory
- `docs/research-and-optimization-report.md` — optimization research and recommendations
- `docs/adversarial-critique.md` — hostile review / critique of this setup
- `docs/skill-topology-cleanup-plan.md` — proposed umbrella/leaf cleanup plan for the local skill set
- `docs/skill-cleanup-matrix.md` — exact keep/patch/merge/disable/archive decision matrix
- `docs/stale-usage-reconciliation.md` — reconciliation of stale `.usage.json` names vs active skills
- `docs/skill-inventory-authoritative.md` — generated authoritative inventory summary from live files + CLI + usage reconciliation
- `docs/skill-inventory-authoritative.json` — full generated inventory payload
- `docs/skill-replacement-map.md` — proposed replacement mapping for stale/historical usage keys
- `scripts/generate_skill_inventory.py` — reproducible generator for the authoritative inventory reports

Not included:
- `.env`, OAuth tokens, auth stores
- raw session DBs, gateway dumps, or secrets
