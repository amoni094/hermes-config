---
name: claude-routing-hierarchy
description: Model routing hierarchy for Hermes — xAI grok-4.5 primary, free-tier providers (Cerebras, SambaNova, Mistral) for fallback and auxiliary. Capability-based decision matrix with context windows, quotas, and fallback chains.
version: 5.0.0
author: Hermes
---

# Routing Hierarchy (live config 2026-08-26)

## Primary model (xAI)

| Role | Model | When to use |
|------|-------|-------------|
| Main session | grok-4.5 (xai) | Default orchestration (context_length 200000) |
| Delegation workers | mistral-small-latest (mistral) | Subagents / parallel workers (delegation.*); max_concurrent_children=10, max_spawn_depth=1 |
| Auxiliary vision | claude-haiku-4-5 (anthropic) | Vision analysis tasks |
| Auxiliary compression / title / triage / curator / web_extract | mistral-small-latest (mistral) | High-volume internal ops; compression has sambanova→mistral-large fallback_chain |

Escalation (manual / skill-driven, not automatic fallback):
- grok-4.6 — harder reasoning when grok-4.5 is insufficient
- Anthropic long-context / sonnet-class — when xAI path fails quality or needs long secure context
- custom:openai `gpt-5.6-sol` — adversarial review path (prove via agent.log)

---

## Fallback chain (config.yaml fallback_providers)

Fires automatically when the primary provider is unavailable/429/timeout:
  1. xai / grok-4.5                     (primary)
  2. cerebras / gpt-oss-120b            (free, high RPD, 8K ctx cap on free tier)
  3. sambanova / DeepSeek-V3.2          (free, long-context, no data-training policy)
  4. mistral / mistral-large-latest     (free-tier volume, long ctx, data training opt-in)

---

## Configured providers — capability map

### xAI (provider: xai)
Key: XAI_API_KEY
Primary chat model: grok-4.5 (200k context configured)

### Cerebras (provider: cerebras)
Key: CEREBRAS_API_KEY
Quota: high free RPD — free tier caps context at 8K tokens
Models (discovered): gpt-oss-120b, gemma-4-31b
Role: first automatic fallback hop

### SambaNova (provider: sambanova)
Key: SAMBANOVA_API_KEY
Quota: low per-model free RPD; no data training
Models (discovered): DeepSeek-V3.1/V3.2, gpt-oss-120b, MiniMax-M2.7/M3, Meta-Llama-3.3-70B-Instruct, gemma-4-31B-it
Role: second fallback hop; compression auxiliary fallback

### Mistral (provider: mistral)
Key: MISTRAL_API_KEY
Quota: high monthly token volume; data training opt-in — avoid sensitive prompts
Role: third fallback hop (mistral-large-latest); delegation + most auxiliary routes (mistral-small-latest)
Many models discovered (codestral, devstral, magistral, ministral family, OCR/voxtral, etc.)

### Anthropic (provider: anthropic)
Key: ANTHROPIC_API_KEY
Role: auxiliary vision (claude-haiku-4-5); Hindsight LLM inference; optional escalation
providers.anthropic.stale_timeout_seconds: 900

### OpenAI (custom_provider openai)
Key: OPENAI_API_KEY
Role: embeddings for Hindsight + Graphiti; override models gpt-5.4 / gpt-5.5 / gpt-5.6-sol (not default chat)

---

## Capability-based routing decision matrix

| Scenario | Model | Provider | Why |
|----------|-------|----------|-----|
| Default orchestration | grok-4.5 | xai | Configured primary |
| Subagent / leaf worker | mistral-small-latest | mistral | delegation.* |
| Context <8K, max throughput fallback | gpt-oss-120b | cerebras | First fallback hop |
| Privacy-safe / quality fallback hop | DeepSeek-V3.2 | sambanova | Second fallback hop |
| Volume fallback / large free budget | mistral-large-latest | mistral | Third fallback hop |
| Code generation | codestral-latest / devstral-latest | mistral | Purpose-built (manual select) |
| Compression / titles / triage | mistral-small-latest | mistral | auxiliary.* |
| Vision | claude-haiku-4-5 | anthropic | auxiliary.vision |
| Adversarial review | gpt-5.6-sol | custom:openai | Skill/convention; prove via agent.log |
| Embeddings | text-embedding-3-small | openai | Hindsight + Graphiti only |

---

## Web / browser routing

| Surface | Backend | Notes |
|---------|---------|-------|
| web_search | brave | Primary; SearXNG :8888 remains local spare |
| web_extract | firecrawl | Local :3002 |
| browser | Playwright Chromium | ms-playwright cache path in config |
| computer_use | cua-driver | wayland: true |

---

## Safety / loop posture (config)

- approvals.mode: off (destructive_slash_confirm false)
- tool_loop_guardrails: warnings + hard_stop; tool_result_cache session-scoped
- agent.verify_on_stop: auto; tool_use_enforcement: permissive
- No autonomous loops with irreversible side effects outside repo (user convention)

---

## Related docs

- `docs/current-workflow.md` — runtime snapshot
- `docs/memory-topology.md` — memory surfaces
- `docs/external-apps-register.md` — providers and local services
- Live skill: `claude-routing-hierarchy` (may lag this snapshot; prefer this file + config.sanitized.yaml when they disagree)
