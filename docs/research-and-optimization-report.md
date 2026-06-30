# Hermes and AI Agent Optimization Report

Generated: 2026-06-30

## Scope

This report combines:
- local runtime inspection of the current Hermes installation
- Hermes official docs research
- general AI-agent workflow research
- direct review of config, cron jobs, skills inventory, doctor output, and runtime conventions

Primary evidence sources:
- https://hermes-agent.nousresearch.com/docs/guides/tips
- https://hermes-agent.nousresearch.com/docs/guides/automation-blueprints
- https://hermes-agent.nousresearch.com/docs/user-guide/configuration
- https://hermes-agent.nousresearch.com/docs/reference/skills-catalog
- https://addyosmani.com/blog/good-spec/
- https://arxiv.org/html/2603.05344v1

## Current setup snapshot

Strengths already present:
- Strong main model: `gpt-5.4` via `openai-codex`
- Separate delegation model: `gpt-5.5` via `openai-codex`
- Compression enabled with a reasonable threshold and target ratio
- Memory enabled with both memory and user profile stores on
- Local-first terminal backend with persistent shell
- Search/extract stack already tuned toward `searxng + firecrawl`
- Checkpoints enabled
- File mutation verifier enabled
- Secret redaction enabled
- Task ledger present at `~/.hermes/logs/hermes-task-ledger.jsonl`
- High-signal cron/watchdog usage already in place

Relevant local evidence:
- `hermes doctor` reports config version current, memory active, SOUL configured, and no active security advisories
- Firecrawl endpoint responds locally at `http://127.0.0.1:3002/`
- `hermes config check` shows `SEARXNG_URL` and `FIRECRAWL_API_URL` configured

## Highest-value recommendations

### 1. Add a top-level local AGENTS.md for your personal workspace workflow

Why:
- Hermes docs recommend `AGENTS.md` for recurring instructions and project conventions.
- You already have a concise `SOUL.md`, but much of your operating method is still implicit.
- A root `/var/home/rainbow/AGENTS.md` would let every coding/research task inherit your preferred workflow without repeating it.

What to encode there:
- your default repo hygiene rules
- when to delegate vs stay single-agent
- preferred verification commands by project type
- what never belongs in a public/private export
- how to handle Obsidian sync, cron, and task-ledger evidence

Expected benefit:
- less prompt overhead
- fewer corrections
- better consistency across repos and spawned agents

### 2. Reconcile context-length mismatch for local auxiliary/custom providers

Observed:
- Main model context length is `128000`
- custom local provider `qwen3:8b` is configured with `context_length: 64000`
- several auxiliary roles use `custom:local` + `qwen3:8b`

Why it matters:
- official/general agent guidance favors graceful degradation and explicit context engineering
- auxiliary tasks that silently have half the effective context of the main agent can fail or drift under long prompts
- existing task-ledger evidence already shows historical context-size friction around local models

Recommendation:
- either keep auxiliary prompts deliberately short and role-specific
- or raise the local model runtime context if hardware permits and verify the real loaded context

Priority:
- high if you rely heavily on local auxiliary tasks for title generation, triage, curator, and profile description

### 3. Consider switching `approvals.mode` from `manual` to `smart` for day-to-day throughput

Observed:
- config currently uses `approvals.mode: manual`

Why:
- Hermes docs describe `smart` as the recommended middle ground
- your workflow is already verification-heavy and tool-capable
- `manual` is safest but slows repetitive low-risk actions

Recommendation:
- for normal trusted local work, test `approvals.mode: smart`
- keep `manual` if you want maximal friction for destructive commands or for experiments

Expected trade-off:
- better velocity
- slightly more reliance on approval heuristics

### 4. Enable curator backups before enabling wider skill maintenance automation

Observed:
- `curator.enabled: false`
- `curator.backup.enabled: false`
- this profile contains a large number of local/custom skills

Why:
- your skill surface is large and increasingly strategic
- official Hermes guidance favors skills as procedural memory, but unmaintained skills become liabilities
- with many local skills, backup-first maintenance is safer than leaving the set to drift indefinitely

Recommendation:
- first enable curator backups
- then consider enabling curator with conservative intervals
- keep pinning for critical local skills

Suggested posture:
- backup on
- slow review cadence
- archive, never delete, for agent-created material

### 5. Add a compact skills taxonomy pass and reduce overlap in the local skill set

Observed:
- very large mixed skill inventory: builtin + many local skills
- multiple overlapping Hermes-internal meta-skills exist around workflow, review, memory, context, cron, and observability
- many are disabled but still present, increasing inventory entropy

Why:
- large skill catalogs improve power but worsen routing ambiguity
- AI-agent best-practice literature strongly favors clear boundaries, explicit role splits, and modular instructions over sprawling overlap

Recommendation:
- promote a few umbrella skills as canonical entry points
- demote or archive near-duplicates and one-off transitional skills
- add explicit “use this instead of X/Y” notes where overlap is unavoidable

Priority areas for consolidation:
- workflow/meta-skills
- Hermes self-optimization skills
- review/follow-up variations
- Superpowers overlap with Hermes-native workflow skills

### 6. Add explicit verification/runbooks for external bridges flagged by doctor

Observed from `hermes doctor`:
- WhatsApp bridge dependencies have vulnerabilities
- some optional toolchains are missing or partially configured

Recommendation:
- either harden and verify the WhatsApp bridge stack, or intentionally disable and document it as out-of-scope
- keep optional surfaces either “healthy and verified” or “explicitly dormant”; avoid half-maintained edges

Why:
- production agent reliability comes from shrinking ambiguous surfaces
- hostile critique typically attacks stale optional integrations first

### 7. Add a “public export hygiene” skill or AGENTS section

Why:
- this task required exporting config/workflow into a git repo
- the most likely future failure mode is accidental publication of `.env`, `auth.json`, chat history, or gateway metadata

Recommendation:
- codify a reusable export rule set:
  - always sanitize config
  - never export `.env` or `auth.json`
  - redact origin chat IDs and gateway identifiers
  - exclude session DBs and chat logs unless explicitly requested

This would be a good candidate for a reusable local skill.

## Best-practice alignment with external research

### A. Keep specs compact, goal-oriented, and executable

From Addy Osmani’s spec guidance:
- start with a concise goal
- define commands, tests, structure, boundaries, and done-when criteria
- treat specs as living artifacts

Application here:
- your Hermes workflows should keep using compact context packets for delegation
- repo-local AGENTS/spec files should capture commands and boundaries early

### B. Prefer explicit role separation for longer work

From terminal-agent/system-design guidance in the OpenDev paper:
- separate scaffolding from harness behavior
- separate action, critique, compaction, and retrieval concerns
- optimize for progressive degradation and transparency

Application here:
- your current split of main model vs delegation model is good
- next step is sharper specialization of auxiliary roles and skills so local models are only used where they are actually strong

### C. Preserve transparency and inspectability

Research trend:
- strong agent setups expose tool use, approvals, memory writes, and task traces rather than hiding them

Application here:
- your task ledger, cron list, and watchdog stack are already strong
- keep leaning into visible traces over opaque automation

### D. Minimize context bloat at the system level, not just in prompts

Research + Hermes docs both point the same way:
- smaller, sharper persistent instruction files outperform giant generalized prompts
- overlapping skills and sprawling meta-guidance create routing noise

Application here:
- clean skill topology is now a more valuable optimization than adding more skills

## Suggested optimization roadmap

### Phase 1: low-risk immediate wins
1. Create `/var/home/rainbow/AGENTS.md` for personal operating rules
2. Keep using sanitized exports only
3. Decide whether `approvals.mode: smart` fits your trust model
4. Document optional/dormant integrations and fix or disable the WhatsApp bridge path

### Phase 2: skills and context hygiene
1. Identify canonical umbrella skills
2. Patch overlapping local skills with cross-references
3. Archive or retire low-value duplicates
4. Enable curator backups

### Phase 3: model and auxiliary tuning
1. Verify actual runtime context for the local `qwen3:8b` helper path
2. Tighten auxiliary prompts to fit the smaller local context budget
3. Reassess whether some auxiliary roles should use main/provider-backed models instead of local ones

## Bottom line

The current setup is already above average: strong model choices, real verification discipline, task ledger visibility, Firecrawl/SearXNG wired, and useful automation.

The biggest remaining gains are not “add more capability.” They are:
- reduce instruction/skill overlap
- make your operating conventions explicit in a root AGENTS.md
- tighten auxiliary model/context assumptions
- harden export hygiene and optional integrations
