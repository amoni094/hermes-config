# hermes-config

Private repository snapshot of the current local Hermes configuration and workflow.
`config.sanitized.yaml` is a sanitized copy of the active Hermes config (all api_key, token, and password fields blanked).

## What's here

- config.yaml — main Hermes config (all audit improvements applied)
- budget-policy.yaml — session budget limits
- SOUL.md — agent persona
- TOOLS.md — toolset config and local service summary
- veto/rules/ — pre-tool security rules
- agent-hooks/ — lifecycle hooks
- plugins/ — active plugin list
- skills-index.md — skills inventory
- cron.snapshot.json — snapshot of all scheduled cron jobs
- audit/ — audit report and change log
- scripts/ — repo maintenance scripts (sanitize, validate, inventory, migrate)

## Documentation (docs/)

- docs/memory-topology.md — full 4-layer memory stack, routing guide, MCP endpoints
- docs/external-apps-register.md — all external/local services, providers, integrations, Python deps
- docs/scripts-inventory.md — all scripts in ~/.hermes/scripts/ with purpose/cron mapping
- docs/current-workflow.md — current runtime snapshot (model, fallback chain, cron jobs, conventions)
- docs/operations-surface-register.md — cron job table, delivery modes, watchdog coverage
- docs/routing-and-workflow.md — provider/model reference and routing rationale
- docs/upgrade-pass-*.md — historical upgrade passes and security hardening decisions
