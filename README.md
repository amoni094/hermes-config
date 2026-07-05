# hermes-config

Private repository snapshot of the active local Hermes configuration and workflow.
`config.sanitized.yaml` is a sanitized copy of the active Hermes config (all api_key, token, and
password fields blanked).

## What's here

- `config.yaml` — main Hermes config (all audit improvements applied, currently v33)
- `budget-policy.yaml` — session budget limits
- `SOUL.md` — agent persona
- `TOOLS.md` — toolset config and local service summary
- `veto/rules/` — pre-tool security governance rules
- `agent-hooks/` — lifecycle hooks
- `plugins/` — active plugin list
- `skills-index.md` — skills inventory
- `cron.snapshot.json` — snapshot of all scheduled cron jobs
- `audit/` — audit report and change log
- `scripts/` — repo maintenance scripts (sanitize, validate, inventory, migrate)

## Documentation (docs/)

- `docs/how-i-work.md` — **comprehensive architecture reference**: memory layers, task handling, orchestration, skills, workflows, improvements over OOTB Hermes
- `docs/memory-topology.md` — full 4-layer memory stack, routing guide, MCP endpoints
- `docs/external-apps-register.md` — all external/local services, providers, integrations, Python deps
- `docs/scripts-inventory.md` — all scripts in ~/.hermes/scripts/ with purpose/cron mapping
- `docs/current-workflow.md` — current runtime snapshot (model, fallback chain, cron jobs, conventions)
- `docs/operations-surface-register.md` — cron job table, delivery modes, watchdog coverage
- `docs/routing-and-workflow.md` — provider/model reference and routing rationale
- `docs/upgrade-pass-*.md` — historical upgrade passes and security hardening decisions

---

## Soul / Persona Configuration

The agent's personality is set in `SOUL.md`. It is intentionally minimal:

> Be concise, resourceful, and grounded. Prefer direct answers, minimal filler, and
> concrete actions. Optimize for local context, small prompts, and verifiable results.
> Ask only when necessary.

**Design rationale:** A short, declarative persona injects fewer tokens per session than a
long constitution. Behavioral rules belong in `AGENTS.md` (workspace-scoped rules loaded
at session start), veto rules (hard blocks and warnings enforced at tool-call time), and
skills (procedural knowledge loaded on demand). The soul file is purely voice and posture —
not operational rules, not routing logic.

**Optimization applied:** Persona kept at ~50 words. No redundant directives that duplicate
AGENTS.md content. Imperative phrasing avoided (declarative facts, not commands to self).

---

## Skills Management

Skills are reusable procedural knowledge files (`SKILL.md`) organized into domain families.
They contain trigger conditions, numbered steps with exact commands, pitfalls, and
verification steps. The agent loads a skill on demand when a matching task is recognized.

### Current inventory
- ~142 skills across 24 domains
- ~101 enabled, ~41 disabled (platform-incompatible, dependency-missing, or stale)
- Skill usage is tracked per-entry: `use_count`, `last_used_at`, `created_at`, `state`

### Lifecycle
1. **Author** — skills created via `skill_manage(action='create')`, stored under `~/.hermes/skills/`
2. **Load** — triggered by pattern match in the agent's task prefix or explicit `skill_view()` call
3. **Patch** — updated in-place via `skill_manage(action='patch')` when steps are found stale
4. **Disable** — platform-incompatible or low-value skills are listed under `skills.disabled` in
   `config.yaml`; they remain on disk but are not surfaced in the skills index
5. **Delete** — permanent removal only for provably dead skills (`use_count: 0`, `last_used_at: null`,
   no current-use case); deletion records an `absorbed_into` target or empty string to signal
   consolidation vs pruning
6. **Guard** — `skillspector-guard` cron runs every 4 hours to enforce quality rules on the
   enabled skills surface and flag violations without human intervention

### Optimization applied
- 41 skills disabled in `config.yaml` covering macOS-only skills (no toolset dependency),
  platform tools with no installed dependency (e.g. toolsets disabled in config), and stale
  skills with zero use count and no active workflow
- Skill families with overlap are flagged for consolidation rather than silent duplication
- Large never-used skills (e.g. 1.5 MB `research-paper-writing`, `use_count: 0`) deleted outright
- Skills are kept current: stale steps patched immediately when discovered during use

### Key skill families
| Family | Description |
|--------|-------------|
| `autonomous-ai-agents/` | Multi-agent orchestration, delegation, memory surface selection, MCP integration, config repo audit |
| `software-development/` | TDD, debugging, code review, context budgeting, routing hierarchy, skill authoring |
| `devops/` | Fedora Atomic ops, Podman, Wi-Fi stability, Wayland, thermal throttling |
| `github/` | Issue triage, PR lifecycle, scoped fixes, CI workflow |
| `research/` | arXiv, Firecrawl, music/film rec, agent discovery |
| `superpowers/` | Core agentic workflow patterns (brainstorming, plans, git worktrees, reviews) |
| `note-taking/` | Obsidian vault read/write/search and research ingestion |
| `computer-use/` | Desktop automation, background UI driving |

---

## Memory System — Topology and Routing

The agent runs a 4-layer memory stack. Each layer has a distinct scope, retrieval mechanism,
and cost profile. Routing between layers is governed by the `hermes-memory-surface-selection`
skill. See `docs/memory-topology.md` for the full routing decision tree and MCP endpoints.

### Layer overview

| Layer | Backend | Scope | When to use |
|-------|---------|-------|-------------|
| **Hermes durable** | Built-in (`MEMORY.md` / `USER.md`) | Session-injected, always-on | Cross-session preferences, environment facts, stable conventions; 2,200 char budget |
| **Hindsight** | local_embedded via Ollama | Long-term structured knowledge | Reference data, synthesis outputs, semantic recall; `hindsight_retain` / `hindsight_recall` |
| **Graphiti MCP** | Neo4j + Graphiti server at `localhost:8765` | Episodic/relational knowledge graph | Entity relationships, temporal facts, provenance chains; group_id=`hermes` |
| **QMD** | FlowState-QMD → Obsidian vault | Personal wiki corpus search | Articles, notes, research ingestion; `mcp_qmd_query` / `mcp_qmd_get` |
| **Session search** | SQLite (`~/.hermes/state/sessions.db`) | Conversation history | Prior decisions, task outcomes, what was said/done in past sessions; always-on |
| **MemPalace** | MCP server (disabled) | — | Disabled; not loaded; do not reference |

### Routing rules (summary)
- **Durable memory** — preferences, environment constants, tool quirks that must survive a
  session reset and be injected automatically. Keep compact (~2,200 char).
- **Hindsight** — store detailed structured knowledge, long reference outputs, and facts that
  need semantic retrieval by concept. Backed by Ollama embeddings (local, private).
- **Graphiti** — entity-entity relationships, time-stamped facts, provenance (who decided
  what and when). Episodic memory with graph traversal.
- **QMD** — search the Obsidian vault and personal wiki corpus. Fed by the hourly Obsidian
  sync cron (`hourly-hermes-chat-sync`).
- **Session search** — always reach for this before asking the user to repeat something. FTS5
  over the full conversation history.
- **MemPalace** — disabled; skip.

### Embedding backend
Ollama serves embeddings at `http://localhost:11434`. Installed models: `qwen3:8b`,
`llama3.2:3b`. Both Hindsight and Graphiti depend on Ollama being healthy.

---

## LLM Routing

Provider-agnostic routing with an Anthropic primary chain, capability-based escalation,
and a multi-provider fallback. Full routing table in `docs/routing-and-workflow.md`.

### Primary chain (Anthropic)

| Role | Model | When |
|------|-------|------|
| Main orchestration | claude-sonnet-4-6 | Default for all sessions |
| Delegation workers | claude-sonnet-4-6 | Subagents and parallel workers (same model as main) |
| Auxiliary / utility | claude-haiku-4-5 | Context compression (high-volume internal operations) |
| Escalation | claude-fable-5 | Formal verification, adversarial red-team, >100K token synthesis, max reasoning; escalate only when correctness > cost |

**Escalation discipline:** Do not escalate to Fable-5 for routine edits, simple debug, or
summarization. Escalate only when the task genuinely requires maximum reasoning or very large
document synthesis.

### Fallback chain
Fires automatically on Anthropic 429 / timeout / unavailability:
1. `cerebras / gpt-oss-120b` — fast, high-volume free tier, 8K context cap
2. `sambanova / DeepSeek-V3.1` — long-context, no data-training policy
3. `mistral / mistral-large-latest` — high token budget, 262K context

### Capability-based routing (free-tier providers)
Multiple free-tier providers are configured for cron jobs, leaf subagents, and auxiliary tasks.
Key routing heuristics:
- Context >128K → Gemini 2.5 Flash (1M context window)
- Context 32K–128K, code → Codestral (256K, purpose-built for code)
- Context <8K, max throughput → Cerebras gpt-oss-120b (14,400 RPD, ~2,600 tok/s)
- Speed-critical / real-time → Groq llama-3.3-70b (lowest latency, ~320 tok/s)
- Privacy-sensitive → SambaNova or GitHub Models (no data-training policies)
- Offline / no network → local Qwen3:8b via Ollama (always available)

### Context compression
Enabled at threshold 0.4. Claude Haiku is the auxiliary model for compression operations.
This reduces token spend on long sessions without changing the primary model's context.

---

## Workflow Patterns

### Single-agent (default)
Most tasks are handled in a single session with the primary model. The agent uses persistent
shell state, skill loading, and memory retrieval to complete multi-step work without spawning
subagents.

### Delegate_task (parallel subagents)
Used when work is independent across multiple subtasks or would flood the main context window
with intermediate data. Each subagent gets an isolated terminal session and context packet.
Config: `claude-sonnet-4-6` as delegation model, `max_concurrent_children: 3`,
`max_spawn_depth: 1`.

**When to delegate:**
- Reasoning-heavy subtasks (code review, research synthesis, debugging)
- Parallel independent workstreams (research A and B simultaneously)
- Tasks that would flood context with intermediate data

**Context packet discipline:** Subagents receive all required context via the task `context`
field — they have no memory of the parent conversation.

### Cron / background automation
8 scheduled jobs cover ongoing maintenance without user intervention:

| Job | Schedule | Purpose |
|-----|----------|---------|
| `hourly-hermes-chat-sync` | Every 240m | Obsidian vault sync (session highlights) |
| `skillspector-guard` | Every 240m | Skills quality enforcement |
| `session-auto-prune` | Every 240m | Prune stale sessions |
| `firecrawl-watchdog` | Every 10m | Firecrawl health check |
| `hermes-platform-watchdog` | Every 720m | Broad platform health |
| `hermes-mutation-gate-watch` | Every 1440m | Mutation gate integrity check |
| `hermes-memory-drift-audit` | Every 1440m | Memory drift detection |
| `obsidian-weekly-review` | Fridays 17:00 | Weekly vault synthesis (LLM agent + script) |

All jobs run locally (`deliver=local`); output is inspectable via `hermes cron list`.

### Multi-agent pipelines (role-based)
For complex bounded tasks, the agent uses a fan-out / fan-in pattern:
- **Fan-out:** parallel workers each receive a scoped subtask (research, implementation,
  testing, review)
- **Fan-in:** results are merged by a synthesis step or the primary agent
- Role catalog: researcher, coder, tester, reviewer, integrator, documenter

### Ouroboros (quality escalation)
Ouroboros is used as a quality escalator for vague, underspecified, or high-stakes work —
not for every task. Trigger conditions:
- Requirements are unclear or multiple interpretations are plausible
- Failure cost is high (security, arch decisions, formal verification)
- Iterative convergence is preferred over a single-pass attempt
- A formal acceptance-criteria gate is needed

Ouroboros workflow: `interview` → `seed` (spec) → `run` (execute) → `evaluate` (gate) →
`ralph` (iterative fix loop). The `auto` command compresses this to a single invocation.

Orca (meta-layer) is used for swarm improvement: agent role design, prompt refinement,
worker template evolution, decomposition logic, and routing heuristic changes — not for
production task execution.

### Adaptive routing by task complexity
| Complexity | Routing |
|------------|---------|
| Simple execution (single tool, known answer) | Single-turn, no delegation |
| Research / discovery | `web_search` + `web_extract` + session_search; delegate if multi-domain |
| Specification needed | Ouroboros interview → seed |
| Implementation | Primary agent or delegate to worker subagent |
| Verification / fixup | Ouroboros evaluate or ralph loop |
| Long-running background | Cron job or tracked background process |

---

## Self-Optimization and Maintenance Patterns

The system is designed to improve itself over time without requiring explicit user direction.

### Continuous skill improvement
- Every time a skill is used and a gap, error, or outdated step is found, the skill is
  patched immediately (`skill_manage(action='patch')`), not deferred
- After difficult or iterative tasks (5+ tool calls, non-trivial error recovery), the
  approach is saved as a new skill or merged into an existing one
- `skillspector-guard` enforces skill quality rules every 4 hours and flags violations

### Memory hygiene
- Durable memory (`MEMORY.md` / `USER.md`) is kept compact and signal-dense; stale or
  redundant entries are removed when new facts are added
- `hermes-memory-drift-audit` cron detects drift between durable memory and actual system
  state daily
- Hindsight and Graphiti are append-based; no pruning needed on normal cadence

### Cron and watchdog hygiene
- Duplicate cron jobs are identified and removed (e.g. `prune-sessions-daily` removed when
  found to duplicate the built-in `session-auto-prune`)
- Orphan scripts (no cron reference, no skill reference, no recent invocation) are removed
  during upgrade passes
- Watchdog scripts are validated against the live config before each run to avoid false
  passes from stale hardcoded keys

### Config evolution
- Config is versioned (`_config_version: 33`). Upgrade passes are logged in `docs/upgrade-pass-*.md`.
- Conservative disable-only approach for capabilities: features are disabled (reversible)
  before being deleted
- `hermes config check` is run after every config change; `hermes doctor` on a maintenance
  cadence

### Upgrade passes
The system has undergone structured upgrade passes orchestrated by a dedicated reasoning model.
Each pass addresses a bounded set of issues, produces a logged audit summary, and is verified
before the next pass begins. This prevents accumulated technical debt from becoming opaque.

---

## Security Posture

Security governance is layered across config, veto rules, and operational hygiene.

### Pre-tool veto layer
All tool calls pass through a governance evaluation before execution. Two rule files:
- `veto/rules/hermes-hard-blocks.yaml` — critical-severity patterns that are unconditionally
  blocked: recursive force-deletes, disk formatting, process kill signals to system processes,
  network backdoor patterns (reverse shells, bind shells, socat/nc/mkfifo misuse), decode-then-exec
  chains, and exfiltration via HTML/CSS side channels
- `veto/rules/hermes-warn.yaml` — warn-severity patterns that flag for attention without
  blocking: sensitive file access, elevated privilege commands, and potentially destructive writes

### Destructive command approvals
`approvals.destructive_commands: false` — the agent does not auto-approve destructive commands.
An explicit command allowlist (`command_allowlist`) permits only specific known-safe system
operations (e.g. service restarts and Hermes self-updates).

### Secret hygiene
- All API keys, tokens, and passwords are stored in `.env` (excluded from this repo)
- `config.sanitized.yaml` in this repo has all credential fields blanked
- Sanitizer script (`scripts/sanitize.sh`) runs before every repo export
- WhatsApp bridge: dormant. Previously had a wildcard sender allowlist; this has been
  commented out. When the bridge is reactivated, explicit JID allowlisting is required before
  enabling

### Messaging consent
The agent will not enter or send messages to any external chat, contact, or platform without
explicit per-session user consent. This is enforced by the `messaging-consent-boundaries`
skill and the AGENTS.md operating rules.

### Network exposure
- All MCP servers are local-only (`localhost:8765` for Graphiti, local script for QMD)
- SearXNG (web search) and Firecrawl (web extract) run as local self-hosted services;
  no search queries are sent to third-party search infrastructure
- Telegram/Discord gateway runs as a local user service; webhook is inbound-only

### Data training policy
Provider selection accounts for data training risk. Providers with confirmed no-training
policies are preferred for privacy-sensitive prompts. Mistral is explicitly noted as a
training-opt-in provider; sensitive prompts are not routed there.

### Repo export hygiene
Never exported from this repo:
- `.env` (API keys, tokens, passwords)
- `auth.json` (gateway credentials)
- `state.db*` (session state)
- `sessions/`, `logs/`, `gateway_state.json`, `channel_directory.json`, `processes.json`
- Raw session histories or chat logs containing third-party content

---

## Important exclusions from repo export

- `~/.hermes/.env`
- `~/.hermes/auth.json`
- Session databases / logs containing secrets or third-party content
- Raw gateway / session / chat histories
