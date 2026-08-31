---
name: routing-and-workflow
description: Model routing hierarchy for this Hermes instance — anthropic/claude-sonnet-4-6 primary, xAI/grok-4.6 delegation + fallback #1, Mistral + SambaNova free-tier fallbacks. Capability-based decision matrix with context windows and fallback chains.
version: 6.0.0
author: Hermes
---

# Routing Hierarchy (live config 2026-08-31)

## Primary model (Anthropic)

| Role | Model | Provider | When to use |
|------|-------|----------|-------------|
| Main session | claude-sonnet-4-6 | anthropic | Default orchestration (context_length 200000) |
| Delegation workers | grok-4.6 | xai | Subagents / parallel workers (delegation.*); max_concurrent_children=10, max_spawn_depth=1 |
| Auxiliary vision | claude-haiku-4-5 | anthropic | Vision analysis tasks |
| Auxiliary compression | claude-haiku-4-5 | anthropic | Context compression (fallback: sambanova/gemma-4-31B-it; max_concurrency=2; max_tokens=4096) |
| Auxiliary title / triage / curator / web_extract | mistral-small-latest | mistral | High-volume internal ops |

Escalation (manual / skill-driven, not automatic fallback):
- Adversarial review path: `custom:openai` / `gpt-5.6-sol` — explicit override only (prove via agent.log)

---

## Fallback chain (config.yaml fallback_providers)

Fires automatically when the primary provider is unavailable / 429 / timeout:

  1. xai / grok-4.6              (fallback #1; also the delegation model)
  2. mistral / mistral-large-latest   (free-tier volume, long ctx)
  3. sambanova / gemma-4-31B-it       (free, long-context, no data-training policy)

Note: Cerebras was removed from the fallback chain. SambaNova model updated from DeepSeek-V3.2 to gemma-4-31B-it.

---

## Configured providers — capability map

### Anthropic (provider: anthropic)
Key: ANTHROPIC_API_KEY
Primary chat model: claude-sonnet-4-6 (200k context configured)
Auxiliary: claude-haiku-4-5 (vision, compression)
Hindsight LLM inference also uses Anthropic API.
Stale timeout: 900s

### xAI (provider: xai)
Key: XAI_API_KEY
Model: grok-4.6 (200k context)
Role: fallback #1 + delegation model
Used by: delegate_task, fallback_providers[0]

### Mistral (provider: mistral)
Key: MISTRAL_API_KEY
Base URL: https://api.mistral.ai/v1
Fallback model: mistral-large-latest
Auxiliary models: mistral-small-latest (title, triage, curator, web_extract)
Note: mistral-small-latest raises error 422 on `reasoning_effort` parameter — do not pass it.

### SambaNova (provider: sambanova)
Key: SAMBANOVA_API_KEY
Base URL: https://api.sambanova.ai/v1
Fallback model: gemma-4-31B-it
Also: compression fallback (claude-haiku-4-5 → gemma-4-31B-it)
No data-training policy.

### OpenAI (provider: openai)
Key: OPENAI_API_KEY
Used for: Hindsight + Graphiti embeddings (text-embedding-3-small, 1536d) — not for chat
Adversarial review: gpt-5.6-sol via explicit custom:openai override only

---

## Embedding backend

Both Hindsight and Graphiti use OpenAI `text-embedding-3-small` (1536d) via the OpenAI API.
Ollama is UNINSTALLED (2026-07-12). Do not reference port 11434 for embeddings or inference.

---

## Agent runtime settings

| Setting | Value |
|---------|-------|
| tool_use_enforcement | strict |
| verify_on_stop | auto |
| max_turns | 500 |
| gateway_timeout | 1800s |
| session_stall_timeout | 1800s |
| api_max_retries | 5 |
| context_compression threshold | 0.35 (120000 tokens) |
| micro_compact | every 4 turns |
| protect_last_n | 32 |
| idle_compact_after_seconds | 1800 |
| intent_conditioned_offload | true |
| tool_result_cache | session scope, max 200 entries |
| delegation max_concurrent_children | 10 |
| delegation max_spawn_depth | 1 |

---

## Web / search backends

| Function | Backend | Details |
|----------|---------|---------|
| Web search | brave-free | BRAVE_SEARCH_API_KEY; plugin id = brave-free (not bare 'brave') |
| Web extract | firecrawl | Local at http://127.0.0.1:3002; fallback: blocked-page-recovery skill |
| Browser | Playwright/Chromium | ms-playwright cache; stealth-browser-mcp MCP active |

---

## Routing decision heuristics

Use the primary model (claude-sonnet-4-6) for:
- All default in-session work
- Any task requiring tool use, memory, skill loading
- Long-context work (up to 200k tokens)

Use delegation (grok-4.6 workers) for:
- Independent parallel subtasks (research, audits, subagent coding)
- Bounded tasks with clear output contracts
- DO NOT use for tasks requiring user interaction or irreversible side effects

Use fallback chain automatically:
- On 429 / timeout / provider error — fires without user action

Use explicit escalation (not automatic):
- Adversarial review: custom:openai / gpt-5.6-sol only — prove need via agent.log

Do NOT use:
- Cerebras (removed from chain)
- Groq (not configured)
- Google Gemini (not configured)
- Ollama (uninstalled 2026-07-12)
- Any model on a provider not listed in config.yaml

---

## Skill routing

Semantic skill routing via `hermes-semantic-skill-routing` skill. Skills are loaded on demand
per turn when the trigger string matches; the skill file is the canonical procedure, not this doc.

Research pipeline routing: see `research/ROUTING.md` in this repo.

Last updated: 2026-08-31 (primary flipped to anthropic/claude-sonnet-4-6; delegation to xai/grok-4.6;
fallback updated: Cerebras removed, SambaNova model updated to gemma-4-31B-it).
