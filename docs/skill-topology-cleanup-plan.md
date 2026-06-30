# Skill Topology Cleanup Plan

Generated: 2026-06-30

## Objective

Reduce routing ambiguity, context bloat, and maintenance overhead in the local Hermes skill set without losing useful capability.

## Guiding principles

1. Fewer umbrella skills, clearer triggers.
2. Smaller `SKILL.md` entrypoints, heavier detail in `references/`.
3. Platform- and integration-specific skills disabled by default unless actively used.
4. Procedures live in skills; stable facts live in memory.
5. Archived or renamed skills must not keep poisoning usage/routing signals.

## Proposed target topology

### A. Development workflow umbrella
Canonical router:
- `workflow-map`

Primary leaves to keep prominent:
- `complexity-gated-planning`
- `isolated-workspace-preflight`
- `test-driven-development`
- `risk-based-review`
- `requesting-code-review`
- `verification-before-completion`
- `subagent-driven-development`

De-emphasize or fold under the router:
- `hermes-workflow-optimization`
- `hermes-operating-pattern`
- `hermes-coding-review-loop`
- `review-driven-followup-fixes`

### B. Hermes runtime / context / memory umbrella
Canonical routers:
- `hermes-context-hygiene`
- `hermes-memory-surface-selection`

Keep as narrow specialist leaves:
- `hermes-context-budgeting`
- `hermes-performance-tuning`
- `hermes-memory-drift-audit`
- `hermes-session-hygiene`
- `agent-runtime-stack-debugging`

De-emphasize or merge guidance from:
- `hermes-workflow-optimization`
- `hermes-operating-pattern`
- `hermes-memory-capture-and-bridge`
- `hermes-observability-and-task-ledger`

### C. GitHub umbrella
Canonical umbrella:
- `github-operations`

Primary specialist to keep:
- `scoped-pr-fix-and-verification`

Candidates to fold into umbrella or keep disabled:
- `split-ci-workflow-change-and-draft-pr`
- `github-issues`
- archived GitHub leaves that are now historical

### D. Research umbrella
Canonical router:
- `research-briefing`

Primary specialists:
- `recent-news-briefing`
- `firecrawl-research`
- `agent-reach-discovery`

Keep disabled/narrow-trigger unless actively used:
- `political-source-monitoring`
- `last30days-customization`
- `stay-in`
- `suggest-music`

### E. Ouroboros umbrella
Canonical router:
- `autonomous-ai-agents`
  or
- `ouroboros/help`

Keep leaf commands only for explicit invocation.
Move examples/checklists out of large leaf SKILL bodies into references.

### F. Fedora Atomic / desktop umbrella
Potential umbrella to create later:
- `fedora-atomic-router`

Likely leaves:
- `atomic-desktop-app-installation`
- `fedora-atomic-dotfiles-adaptation`
- `silverblue-toolbox-wrapper-bootstrap`
- `wayland-session-management`
- `rootless-podman-compose-adaptation`

## Execution phases

### Phase 1: routing cleanup
1. Patch existing umbrellas so they explicitly point to canonical leaves.
2. Remove references to missing skills from metadata and bodies.
3. Add "use this instead of X/Y" notes where overlap is high.

### Phase 2: size reduction
1. Split oversized `SKILL.md` files into:
   - concise trigger-oriented front file
   - references/examples/checklists in `references/`
2. Highest-priority split targets:
   - `research-paper-writing`
   - `hermes-agent`
   - `local-personal-dashboard`
   - `verification-before-completion`
   - `hermes-performance-tuning`
   - `ouroboros/seed`

### Phase 3: inventory truth pass
1. Build one authoritative inventory report with:
   - source type: builtin/local
   - enabled/disabled
   - archived/non-archived
   - file path
   - frontmatter name
   - usage count / patch count / last activity
   - alias mapping for renamed bundled skills
2. Reconcile stale usage entries for removed/archived names.

### Phase 4: disabled-by-default policy
Keep disabled unless explicitly requested or environment-ready:
- Apple/macOS-specific skills on this Linux host
- large creative suites (`comfyui`, `p5js`, `manim-video`, `touchdesigner-mcp`)
- risky/sensitive skills like `godmode`
- low-value dormant integrations like `airtable`, `notion`, `google-workspace`, `teams-meeting-pipeline`

## Concrete changes started in this pass
This pass focuses on low-risk routing/documentation cleanup first:
- patch overlapping workflow/runtime skills to remove stale references and clarify canonical routers
- add this cleanup plan and a decision matrix to the `hermes-config` repo

## Success criteria
- an agent can choose the right umbrella skill with minimal ambiguity
- common workflow tasks load fewer overlapping meta-skills
- oversized skills no longer carry most of their weight in the main `SKILL.md`
- usage/curation reports no longer conflate archived or renamed skills with active ones
