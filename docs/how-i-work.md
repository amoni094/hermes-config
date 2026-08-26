# How This Agent Works — Architecture Reference

Generated: 2026-07-05; last refreshed 2026-08-26 for live routing/memory/cron drift.
Source of truth for system design, memory handling, task execution, orchestration, skills,
and improvements over out-of-the-box Hermes. Prefer `docs/current-workflow.md` +
`config.sanitized.yaml` for exact live values when this narrative lags.

---

## Overview

This is a self-hosted Hermes (NousResearch) agentic assistant on Fedora 44 Silverblue,
with multi-provider routing (xAI grok-4.5 primary). The agent runs as a persistent local
daemon with a persistent shell, multi-layer memory, a skills library, scheduled background
automation, and a pre-tool security governance layer.

The core loop is: receive task → consult memory + skills → plan → execute tools → verify →
update memory + skills → respond. Most tasks are handled in a single session. Complex,
parallel, or context-flooding tasks are delegated to subagents.

---

## Memory System

Memory is layered. Each layer has a different scope, cost, and retrieval mechanism.
The routing skill (`hermes-memory-surface-selection`) governs which layer to use.

### Layer 1 — Hermes durable memory (MEMORY.md / USER.md)
- **Backend:** Built-in Hermes memory store
- **Scope:** Injected into every session automatically (always-on)
- **Budget:** ~2,200 chars (MEMORY.md) + ~1,600 chars (USER.md)
- **Content:** Session-persistent facts — user preferences, environment constants,
  tool quirks, stable conventions, provider chain, project paths
- **When to write:** Cross-session facts that must survive a session reset and be
  injected automatically. Keep compact: only add if it prevents the user repeating
  themselves. Remove stale entries when adding new ones.
- **When NOT to write:** Task progress, PR numbers, completed-work logs, or facts
  that will be stale in 7 days. Those belong in session_search.

### Layer 2 — Hindsight (API-based)
- **Backend:** Hindsight API on :9177 (systemd `hindsight-api.service`); Anthropic LLM inference;
  OpenAI `text-embedding-3-small` embeddings. Ollama is not used.
- **Scope:** Long-term structured knowledge, queryable by concept
- **Retrieval:** `hindsight_recall(query)` for semantic search; `hindsight_reflect(query)`
  for synthesis across stored facts; `hindsight_retain(content)` to write
- **Content:** Reference data, research synthesis outputs, facts that need semantic
  retrieval across sessions — too large or too volatile for the char-limited durable memory
- **Banks:** `hermes-default` (primary), `hermes` (secondary); helper `unified-recall.py`

### Layer 3 — Graphiti MCP (FalkorDB knowledge graph)
- **Backend:** Graphiti server at localhost:8765, FalkorDB database
- **Scope:** Episodic and relational knowledge — entity relationships, temporal facts,
  provenance chains, decision history
- **Retrieval:** `mcp__graphiti_search_memory_facts(query)` for fact search;
  `mcp__graphiti_search_nodes(query)` for entity search; `mcp__graphiti_add_memory()` to write
- **Group IDs:** `hermes` (general agent knowledge), `hermes-reasoning` (reasoning traces)
- **When to use:** When the relationship between entities matters (who decided what, when,
  under what circumstances); when temporal ordering of facts is relevant
- **Dependency:** Requires Graphiti server + FalkorDB to be running. If the MCP endpoint is
  unreachable, fall back to Hindsight or durable memory.

### Layer 4 — QMD / FlowState-QMD (DISABLED)
- **Backend:** FlowState QMD MCP server script present (`~/.hermes/scripts/qmd-local.sh`)
- **Status:** **disabled** in config.yaml — do not route live queries here
- **Note:** Obsidian sync still runs via `hermes-chat-sync-4h` / weekly review without QMD MCP

### Layer 5 — Session search (always-on)
- **Backend:** SQLite FTS5 over `~/.hermes/state.db` (`messages_fts`)
- **Scope:** Full conversation history across all sessions
- **Retrieval:** `session_search(query)` — FTS5 keyword and boolean search
- **Rule:** Always reach for this before asking the user to repeat themselves.
  If a user references something from a past session, search first.

### Disabled: MemPalace
- Present on disk (`~/.hermes/scripts/mempalace-mcp.sh`) but disabled in config.yaml.
  Do not reference it. If re-enabled in future, update this doc.

### Embedding backend
- OpenAI `text-embedding-3-small` (1536d) for Hindsight and Graphiti via OPENAI_API_KEY.
- Hindsight LLM inference uses the Anthropic API.
- Ollama is **UNINSTALLED** (2026-07-12). Do not reference port 11434.
- Hindsight is supervised by systemd user unit `hindsight-api.service` on :9177.


---

## Task Handling

### Single-agent (default for most tasks)
1. Session starts; durable memory (MEMORY.md + USER.md) is injected automatically.
2. AGENTS.md (workspace rules) is loaded from the working directory.
3. Agent reads the task, checks available_skills in the system prompt.
4. If a matching skill is found, loads it with `skill_view()` before proceeding.
5. Executes tools (terminal, read_file, web_search, etc.) using the persistent shell.
6. Shell state (env vars, working directory, activated venvs) persists across tool calls
   within the same session — no need to re-source environments.
7. After completing a complex task (5+ tool calls), offers to save approach as a skill.
8. Updates durable memory if a new stable fact was learned.

### Context compression
- Triggered automatically when context approaches threshold (0.35).
- Compression model: `mistral/mistral-small-latest` (auxiliary.compression; fallback sambanova/DeepSeek-V3.2 → mistral/mistral-large-latest).
- Compressed context is a summarized handoff; tool results and intermediate data are
  elided. The primary model context is preserved at the summary level.
- Resume display is set to compact (3 exchanges shown on resume).

### Verification discipline
- `verify_on_stop: auto` — stop-path verification is automatic when appropriate.
  High-stakes work still loads the `verification-before-completion` skill explicitly.
- `tool_use_enforcement: permissive` — the agent does not require explicit approval for
  every tool call. The pre-tool veto layer (not the agent config) handles blocking.

---

## Orchestration

### Delegate_task (parallel subagents)
- Used when: (a) subtasks are independent and can run in parallel, (b) a subtask
  would flood the main context window with intermediate data, (c) a subtask requires
  reasoning-heavy isolated work (code review, research synthesis, debugging).
- **Config:** `delegation.model: mistral-small-latest` (provider mistral), `max_concurrent_children: 10`,
  `max_spawn_depth: 1` (leaf subagents only; no recursive delegation); hierarchy_aware + toolset profiles.
- **Context packet discipline:** Subagents have no memory of the parent conversation.
  All required context (file paths, error messages, constraints, goal, done criteria,
  proof commands) must be passed in the `context` field of the task spec.
- **Language discipline:** If the user is writing in a non-English language, note this
  in the subagent context so it responds in the correct language.
- **Result verification:** Subagent self-reports are not trusted without verification.
  For operations with external side-effects (HTTP POST, file writes, git push), require
  a verifiable handle (URL, commit SHA, HTTP status) and verify independently.

### Multi-agent pipelines (fan-out / fan-in)
- Fan-out: parallel workers receive scoped subtasks (researcher, coder, tester, reviewer).
- Fan-in: results are merged by the primary agent or a synthesis step.
- Role catalog: researcher, coder, tester, reviewer, integrator, documenter.
- The `hermes-role-pipelines` skill documents the standard role templates.

### Cron / background automation
18 scheduled jobs run on a defined cadence. All deliver locally (no gateway delivery).
Authoritative table: `docs/operations-surface-register.md` + `cron.snapshot.json`.

| Job | Schedule | Mode | Purpose |
|-----|----------|------|---------|
| `hermes-chat-sync-4h` | every 240m | agent | Sync session highlights into Obsidian vault |
| `skillspector-guard` | every 240m | no-agent script | Enforce skill quality rules; flag violations |
| `session-auto-prune` | every 240m | no-agent script | Prune stale sessions from state.db |
| `firecrawl-watchdog` | every 10m | no-agent script | Health-check Firecrawl at :3002 |
| `browser-orphan-watchdog` | every 30m | no-agent script | Kill orphaned Playwright/Chrome processes |
| `hermes-platform-watchdog` | every 720m | no-agent script | Broad platform health (config, MCP, Graphiti) |
| `hermes-mutation-gate-watch` | every 1440m | no-agent script | Check mutation-gate integrity |
| `hermes-memory-drift-audit` | every 1440m | no-agent script | Detect drift between durable memory and actual state |
| `l1-extract-periodic` | every 180m | no-agent script | Extract L1 facts from sessions |
| `l1-promote-periodic` | every 220m | no-agent script | Dual-track L1 promote |
| `l1-hindsight-promote` | every 240m | agent | Promote L1 facts to Hindsight |
| `l1-graphiti-periodic` | every 240m | no-agent script | Graphiti reconcile |
| `g-memory-tier3-nightly` | 0 3 * * * | no-agent script | Nightly Graphiti consolidation |
| `memory-ttl-purge` | 0 3 * * * | no-agent script | Expire ephemeral/volatile tiers |
| `omni-skill-quality-scan` | 0 3 * * 0 | no-agent script | Weekly skill quality scan |
| `skill-prune-audit` | 0 9 1 * * | no-agent script | Monthly skill prune audit |
| `pending-improvements-review` | 0 10 * * 0 | agent | Weekly curator review of staged improvements |
| `obsidian-weekly-review` | Fridays 17:00 | agent + script | Weekly vault synthesis |

**CLI note:** On this CLI session, `deliver=local` means output is stored in the cron
log; it does NOT message this terminal. Use `hermes cron list` to inspect results.

### Ouroboros (quality escalation)
Ouroboros is a quality escalation path, not a default workflow. Use when:
- Requirements are underspecified or multiple interpretations are plausible
- Failure cost is high (security decisions, architecture, formal verification)
- Iterative convergence is preferred over single-pass
- A formal acceptance-criteria gate is needed before declaring done

Ouroboros workflow stages: `interview` → `seed` (spec) → `run` (execute) →
`evaluate` (gate pass/fail) → `ralph` (iterative fix loop until gate passes).
The `auto` command compresses the full loop to a single invocation.

Orca (meta-layer) is used for improving agent designs themselves — role templates,
prompt engineering, decomposition logic — not for production task execution.

---

## Skills Framework

Skills are YAML-frontmatter + markdown files (`SKILL.md`) stored under `~/.hermes/skills/`.
Each skill contains: trigger conditions, numbered steps with exact commands, pitfalls, and
verification steps. They encode the user's preferred approach for recurring tasks and carry
specialist knowledge (API endpoints, tool-specific commands, non-obvious pitfalls).

### Skill loading
- The available_skills list is injected into the system prompt (names + one-line descriptions).
- The agent matches the task to skill triggers and loads the full skill via `skill_view()`.
- **Loading discipline:** Err on the side of loading. A skill with context you don't need
  is better than missing critical steps. Load skills even for tasks you think you know —
  they encode this environment's specific conventions.

### Skill lifecycle
1. **Author** — `skill_manage(action='create')` with YAML frontmatter + body
2. **Load** — `skill_view(name)` triggers full content load into context
3. **Patch** — `skill_manage(action='patch')` for targeted updates; never defer
   patching a stale step; update immediately when a gap is found during use
4. **Disable** — listed under `skills.disabled` in config.yaml; stays on disk,
   not surfaced in available_skills list
5. **Delete** — `skill_manage(action='delete', absorbed_into=...)` for dead skills;
   `absorbed_into` is required (consolidation target or empty string for pruning)
6. **Guard** — `skillspector-guard` cron runs every 4 hours; flags orphaned,
   mis-categorized, or quality-violating skills without manual intervention

### Current inventory (as of 2026-07-05)
- 142 total: 0 hub + 24 builtin + 118 local
- 101 enabled, 41 disabled
- 24 domain families

### Key skill families
| Family | Representative skills |
|--------|-----------------------|
| `autonomous-ai-agents/` | hermes-config-repo-audit, hermes-cowork-port-sync, hermes-memory-surface-selection, graphiti-mcp-setup, autonomous-agent-loop-design |
| `software-development/` | systematic-debugging, test-driven-development, hermes-coding-review-loop, complexity-gated-planning, claude-code-skill-authoring |
| `devops/` | atomic-desktop-app-installation, fedora-atomic-dotfiles-adaptation, rootless-podman-compose-adaptation, linux-wifi-stability |
| `github/` | github-operations, github-issues, scoped-pr-fix-and-verification, github-issue-agent |
| `superpowers/` | using-superpowers, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, using-git-worktrees |
| `research/` | arxiv, firecrawl-research, academic-literature-review, stay-in, suggest-music |
| `note-taking/` | obsidian, obsidian-research-ingestion |
| `computer-use/` | computer-use |

---

## Pre-Tool Security Governance (Veto Layer)

All tool calls are evaluated by `veto-pre-tool.py` before execution. Two rule files govern this:

### Hard blocks (`veto/rules/hermes-hard-blocks.yaml`)
Unconditionally blocked patterns (critical severity):
- Recursive force-deletes (`rm -rf /`, `rm -rf ~`, etc.)
- Disk formatting commands
- Process kill signals to system processes
- Network backdoor patterns (reverse shells, bind shells, socat/nc/mkfifo abuse,
  Python/Perl one-liner shells, base64 decode-then-exec chains)
- HTML/CSS side-channel exfiltration patterns

### Warnings (`veto/rules/hermes-warn.yaml`)
Flagged for attention without blocking:
- Sensitive file access (`.env`, `auth.json`, credential files)
- Elevated privilege commands (`sudo`, `su`, `chmod 777`)
- Potentially destructive writes to system paths

### Destructive commands
- `approvals.destructive_commands: false` — no auto-approval.
- `command_allowlist` permits only specific known-safe ops: service restart, `hermes update`.
- All other destructive commands require explicit user confirmation.

---

## Improvements Over Out-of-the-Box Hermes

This configuration makes several significant improvements beyond a default Hermes install:

### 1. 4-layer memory stack (OOTB: 1 layer)
Default Hermes has only the built-in durable memory (MEMORY.md/USER.md). This config adds:
- **Hindsight** (API-based Anthropic + OpenAI embeddings) — semantic long-term knowledge
- **Graphiti MCP** (FalkorDB) — episodic relational graph with temporal facts
- **session_search** — FTS5 over full conversation history on state.db (always-on)
- QMD present but disabled; MemPalace disabled
The `hermes-memory-surface-selection` skill governs routing between active surfaces.

### 2. Pre-tool veto governance (OOTB: approval prompts only)
Default Hermes can prompt before destructive commands. This config adds a rule-based
pre-tool evaluation layer that hard-blocks dangerous patterns (network backdoors,
disk wipes, exfiltration) without needing to recognize them in the moment.

### 3. Skills library (160 enabled live — OOTB: ~20–31 builtin)
135 local custom skills covering: multi-agent orchestration, Fedora Atomic devops,
research workflows, Obsidian integration, security review patterns, model routing
hierarchies, config repo auditing, and cowork port translation.
Skills are continuously maintained: patched on use, guarded by automated cron enforcement.

### 4. Multi-provider fallback chain (OOTB: single provider)
xAI grok-4.5 primary with automatic fallback to Cerebras → SambaNova → Mistral on 429/timeout.
Delegation + most auxiliary routes use Mistral small. Capability-based heuristics still apply for free-tier hops
by context size, speed, and privacy requirements.

### 5. 8 scheduled background jobs (OOTB: none)
Autonomous cron automation handles Obsidian sync, session hygiene, skill guard enforcement,
Firecrawl health, platform health, memory drift detection, mutation gate integrity, and
weekly vault review — all without user intervention.

### 6. Local-first search (OOTB: external search)
SearXNG self-hosted instance + Firecrawl self-hosted scraper replace external search APIs.
No search queries leave the local network infrastructure.

### 7. Persona / soul optimization (OOTB: default verbose persona)
SOUL.md is intentionally minimal (~50 words). Behavioral rules live in AGENTS.md
(workspace-scoped, loaded at session start) and veto rules (enforced at tool-call time).
Skills carry procedural knowledge. This separation reduces per-session token injection
compared to a monolithic constitution.

### 8. Config versioning and upgrade passes (OOTB: no versioning)
Config is versioned (`_config_version: 33`). Structured upgrade passes (5 documented passes)
are orchestrated by a dedicated reasoning model, logged in `docs/upgrade-pass-*.md`, and
verified before the next pass begins. This prevents opaque technical debt accumulation.

### 9. Skill quality enforcement (OOTB: no quality layer)
`skillspector-guard` cron runs every 4 hours to detect orphaned, duplicate, or
mis-categorized skills and flag violations. Skill deletions require `absorbed_into` field
to distinguish consolidation from pruning. Large never-used skills are pruned outright.

### 10. Hermes-to-Cowork port repo (OOTB: not applicable)
A parallel git repo (`hermes-to-cowork-port`) translates all configurations into Claude
Cowork (Claude Desktop Tasks mode) equivalents, kept in sync after each audit. This enables
the same workflows to run in Cowork when the local Hermes daemon is unavailable.

---

## See Also

- `docs/memory-topology.md` — full memory stack with MCP endpoints and routing decision tree
- `docs/routing-and-workflow.md` — provider/model reference and routing rationale
- `docs/current-workflow.md` — current runtime snapshot (model, fallback chain, cron jobs)
- `docs/operations-surface-register.md` — cron job table, delivery modes, watchdog coverage
- `docs/external-apps-register.md` — all services, providers, integrations, Python deps
- `docs/scripts-inventory.md` — all ~/.hermes/scripts/ with purpose and cron mappings
- `veto/rules/hermes-hard-blocks.yaml` — hard-blocked tool-call patterns
- `cron.snapshot.json` — machine-readable cron state snapshot
