# hermes-config

## Snapshot freshness
- As of: **2026-08-26**
- Hermes: **v0.20.5 (2026.8.19)** · upstream `f751a8c5`
- Config version: **39**
- Primary model: **xai / grok-4.5**
- Web: **brave** search + **firecrawl** extract
- Memory provider: **hindsight** (QMD + MemPalace disabled)
- Cron jobs mirrored: **18** (see `cron.snapshot.json`)


Private repository snapshot of the active local Hermes configuration and workflow.
`config.sanitized.yaml` is a sanitized copy of the active Hermes config (all api_key, token, and
password fields blanked).

## What's here

### Files

| Path | Purpose |
|------|---------|
| `config.sanitized.yaml` | Sanitized live config (credentials blanked) — v39 |
| `budget-policy.yaml` | Session token/cost budget limits |
| `SOUL.md` | Agent persona (~50 words, intentionally minimal) |
| `TOOLS.md` | Toolset config and local service summary |
| `veto/rules/` | Pre-tool security governance (hard blocks + warnings) |
| `agent-hooks/` | Lifecycle hooks |
| `plugins/` | Active plugin list |
| `skills-index.md` | Skills inventory snapshot (regenerate after large skill churn) |
| `cron.snapshot.json` | Scheduled cron job snapshot |
| `audit/` | Audit reports and change log |
| `scripts/` | Repo maintenance scripts (sanitize, validate, inventory, migrate) |

### Architecture Overview

Self-hosted Hermes agent (Nous Research) on Fedora 44 Silverblue. Primary chat is
**xAI grok-4.5**; Anthropic/OpenAI/Cerebras/SambaNova/Mistral fill auxiliary, embedding,
and fallback roles. Full write-up: [`docs/how-i-work.md`](docs/how-i-work.md).

#### Model routing

| Role | Model | When |
|------|-------|------|
| Main session | `grok-4.5` (xai) | Default orchestration (200k context) |
| Delegation workers | `mistral-small-latest` (mistral) | Subagents; max_concurrent_children=10, max_spawn_depth=1 |
| Auxiliary / compression / title / triage / curator / web_extract | `mistral-small-latest` (mistral) | High-volume internal ops |
| Auxiliary vision | `claude-haiku-4-5` (anthropic) | Vision |
| Automatic fallback | cerebras `gpt-oss-120b` → sambanova `DeepSeek-V3.2` → mistral `mistral-large-latest` | Primary unavailable |

Context compression threshold **0.35**; micro_compact every 3 turns. Escalation to grok-4.6 /
Anthropic long-context / openai `gpt-5.6-sol` is manual/skill-driven, not automatic fallback.

#### Memory stack

| Layer | Backend | Scope |
|-------|---------|-------|
| 1. Hermes durable | `MEMORY.md` / `USER.md` | Injected every session (~2.2k + ~1.6k) |
| 2. Hindsight | API (Anthropic LLM + OpenAI embeddings) :9177 | Long-term structured knowledge |
| 3. Graphiti MCP | FalkorDB + Graphiti :8765 | Episodic relational graph |
| 4. Session search | FTS5 on `~/.hermes/state.db` | Conversation history |

QMD and MemPalace are installed on disk but **disabled** in config. Ollama is uninstalled.

#### Skills

Live index: **160 enabled** (135 local + 31 builtin), **6 disabled**, 0 hub.
`skillspector-guard` every 4h; weekly quality scan; monthly prune audit.

#### Orchestration

- **Parallel subagents** via `delegate_task` — up to 10 concurrent; leaf-only (`max_spawn_depth: 1`)
- **18 scheduled cron jobs** — Obsidian sync, L1 extract/promote/graphiti, TTL purge, session hygiene, Firecrawl/platform/browser watchdogs, skill guard/scan/prune, pending-improvements review, memory drift + mutation gate
- **Ouroboros** — quality escalation path for formal evaluate/iterate loops when enabled
- **Pre-tool veto** — hard-blocks dangerous patterns before tool calls land

#### Improvements over out-of-the-box Hermes

1. Multi-layer memory (durable + Hindsight + Graphiti + session FTS)
2. Pre-tool veto governance with rule-based hard blocks
3. Large custom skill library with guard + quality cron
4. Multi-provider fallback + capability routing (xAI primary)
5. 18 scheduled background jobs (sync, L1 pipeline, watchdogs, curator)
6. Local Firecrawl + Brave search; SearXNG retained as spare
7. Minimal persona; behavioral rules in AGENTS.md + veto + skills
8. Config versioning with structured upgrade passes
9. Automated skill quality enforcement via skillspector-guard
10. Hermes-to-Cowork port repo for Desktop Tasks equivalents


## Documentation (docs/)

- `docs/how-i-work.md` — **comprehensive architecture reference**: memory layers, task handling, orchestration, skills, workflows, improvements over OOTB Hermes
- `docs/memory-topology.md` — full 4-layer memory stack, routing guide, MCP endpoints
- `docs/external-apps-register.md` — all external/local services, providers, integrations, Python deps
- `docs/scripts-inventory.md` — all scripts in ~/.hermes/scripts/ with purpose/cron mapping
- `docs/current-workflow.md` — current runtime snapshot (model, fallback chain, cron jobs, conventions)
- `docs/operations-surface-register.md` — cron job table, delivery modes, watchdog coverage
- `docs/routing-and-workflow.md` — provider/model reference and routing rationale
- `docs/upgrade-pass-*.md` — historical upgrade passes and security hardening decisions
- `docs/repo1-eval-harness.md` — LLM Efficiency Gateway (repo1): eval harness design, regression suite, EWMA drift detection, and adversarial pass findings (2026-08-18)

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
- Live index: 160 enabled (135 local + 31 builtin), 6 disabled, 0 hub
- Additional names listed under `skills.disabled` in config for platform/stale skills
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
- `skills.disabled` in config.yaml covers platform-incompatible, dependency-missing, and stale skills
  (macOS-only, unused tool surfaces, etc.)
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

Routing between layers is governed by the `hermes-memory-surface-selection` skill.
Authoritative detail: `docs/memory-topology.md`.

### Layer overview

| Layer | Backend | Scope | When to use |
|-------|---------|-------|-------------|
| **Hermes durable** | Built-in (`MEMORY.md` / `USER.md`) | Session-injected | Preferences, environment facts, stable conventions; 2,200 + 1,600 char budgets |
| **Hindsight** | API (Anthropic LLM + OpenAI embeddings) :9177 | Long-term structured knowledge | Semantic recall; hindsight_retain/recall/reflect |
| **Graphiti MCP** | FalkorDB + Graphiti :8765 | Episodic/relational graph | Entity relationships, temporal facts, provenance |
| **Session search** | SQLite FTS5 (`~/.hermes/state.db`) | Conversation history | Prior decisions/outcomes; always-on |
| **QMD** | FlowState-QMD (disabled) | — | Present on disk; disabled in config |
| **MemPalace** | MCP (disabled) | — | Disabled; skip |

### Routing rules (summary)
- **Durable memory** — must inject every turn; keep compact.
- **Hindsight** — long-form structured knowledge, concept recall.
- **Graphiti** — entity/relationship/temporal/provenance.
- **Session search** — what was said/done in past chats (state.db FTS).
- **QMD / MemPalace** — disabled; skip.

### Embedding backend
OpenAI `text-embedding-3-small` for Hindsight and Graphiti. Ollama uninstalled (2026-07-12).
Hindsight supervised by systemd `hindsight-api.service` (`idle_timeout=0`).


## LLM Routing

Authoritative detail: `docs/routing-and-workflow.md` + `config.sanitized.yaml`.

### Primary roles

| Role | Model | Provider |
|------|-------|----------|
| Main orchestration | grok-4.5 | xai |
| Delegation workers | mistral-small-latest | mistral |
| Auxiliary compression / title / triage / curator / web_extract | mistral-small-latest | mistral |
| Auxiliary vision | claude-haiku-4-5 | anthropic |

Manual escalation (not automatic fallback): grok-4.6, Anthropic long-context, openai `gpt-5.6-sol` (adversarial).

### Fallback chain
Fires automatically when the primary provider is unavailable:
1. `cerebras / gpt-oss-120b` — fast free tier, 8K context cap
2. `sambanova / DeepSeek-V3.2` — quality hop, no data-training policy
3. `mistral / mistral-large-latest` — high token budget

### Capability-based heuristics
- Context <8K, max throughput → Cerebras gpt-oss-120b
- Privacy-sensitive quality hop → SambaNova DeepSeek-V3.2
- Code-heavy free-tier → Mistral codestral/devstral (manual select)
- Compression / high-volume internal ops → Mistral small (configured auxiliary)

### Context compression
Enabled at threshold **0.35**. Auxiliary model: `mistral/mistral-small-latest` with
sambanova → mistral-large fallback_chain. micro_compact every 3 turns; protect_last_n=32.


## Workflow Patterns

### Single-agent (default)
Most tasks are handled in a single session with the primary model. The agent uses persistent
shell state, skill loading, and memory retrieval to complete multi-step work without spawning
subagents.

### Delegate_task (parallel subagents)
Used when work is independent across multiple subtasks or would flood the main context window
with intermediate data. Each subagent gets an isolated terminal session and context packet.
Config: `mistral-small-latest` (mistral) as delegation model, `max_concurrent_children: 10`,
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
- Config is versioned (`_config_version: 37`). Upgrade passes are logged in `docs/upgrade-pass-*.md`.
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
