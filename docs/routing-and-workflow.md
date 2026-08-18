---
name: claude-routing-hierarchy
description: Model routing hierarchy for Hermes — single Anthropic primary model, configured free-tier providers (Cerebras, SambaNova, Mistral) for fallback and auxiliary compression. Capability-based decision matrix with context windows, quotas, and fallback chains.
version: 4.0.0
author: Hermes
---

# Claude Routing Hierarchy

## Primary model (Anthropic)

| Role | Model | When to use |
|------|-------|-------------|
| Main session | claude-sonnet-4-6 | Default orchestration |
| Delegation workers | claude-sonnet-4-6 | Subagents and parallel workers (same model as main) |
| Auxiliary vision | claude-haiku-4-5 (anthropic) | Vision analysis tasks |
| Auxiliary / compression | zai-glm-4.7 (cerebras) | Context compression, web_extract, high-volume internal ops |

There is a single configured Anthropic chat model — `claude-sonnet-4-6` — used for both main
orchestration and delegated subagents. No separate escalation or utility Anthropic tier is
configured. Auxiliary routing: compression and web_extract route to Cerebras `zai-glm-4.7`;
vision routes to `claude-haiku-4-5` (see `auxiliary.*` in config.yaml).

---

## Fallback chain (config.yaml fallback_model)

Fires automatically when Anthropic is unavailable/429/timeout:
  1. anthropic / claude-sonnet-4-6           (primary)
  2. cerebras / gpt-oss-120b                 (free, high RPD, 8K ctx cap on free tier)
  3. sambanova / DeepSeek-V3.2               (free, long-context, no data-training policy)
  4. mistral / mistral-large-latest          (free-tier volume, 262K ctx, data training opt-in)

---

## Configured providers — full capability map

### Cerebras (provider: cerebras)
Key: CEREBRAS_API_KEY
Quota: 14,400 RPD, 30 RPM — highest volume free tier
CRITICAL: free tier caps context at 8K tokens (128K is paid only)
No data training policy
Exactly 3 models available (verified live via `/v1/models`):

| Model | Free ctx | Best for |
|-------|----------|----------|
| gpt-oss-120b | 8K | Fast classification, short summarization |
| gemma-4-31b | 8K | Lightweight reasoning, short tasks |
| zai-glm-4.7 | 8K | Context compression (auxiliary.compression) |

### SambaNova (provider: sambanova)
Key: SAMBANOVA_API_KEY
Quota: 20 RPD per model (low but permanent, no data training)
Strength: best quality per request, no training data concerns, good for privacy-adjacent tasks
Exactly 6 models available (verified live via `/v1/models`):

| Model | Context | Best for |
|-------|---------|----------|
| DeepSeek-V3.2 | 32K | Best reasoning quality (note: 32K not 128K) — used in fallback chain |
| DeepSeek-V3.1 | 131K | Long-context DeepSeek tasks (available, not in fallback chain) |
| gpt-oss-120b | 131K | Heavy reasoning, long context |
| MiniMax-M2.7 | 196K | Longest context on SambaNova |
| Meta-Llama-3.3-70B-Instruct | 131K | General long-context tasks |
| gemma-4-31B-it | 131K | Instruction following |

### Mistral (provider: mistral)
Key: MISTRAL_API_KEY
Quota: ~1B tokens/month (most generous by volume), ~1 RPS, 500K TPM
Warning: data training opt-in required — avoid sensitive prompts
Strength: very long context (up to 262K), specialized models for code/reasoning
72 models total available live (verified via `/v1/models`); the 6 cited below were each
individually confirmed present in that live response:

| Model | Context | Best for |
|-------|---------|----------|
| codestral-latest | 256K | Code generation, completion, review |
| devstral-latest | 262K | Agentic coding tasks, multi-file edits |
| mistral-small-latest | 262K | Fast general tasks |
| mistral-medium-latest | 262K | Stronger general reasoning |
| magistral-small-latest | 262K | Reasoning/thinking tasks |
| ministral-8b-latest | 262K | Tiny fast model, high volume |
| mistral-large-latest | 262K | High token budget — used in fallback chain |

---

## Capability-based routing decision matrix

| Scenario | Model | Provider | Why |
|----------|-------|----------|-----|
| Anthropic primary orchestration | claude-sonnet-4-6 | anthropic | Default, only configured Anthropic chat model |
| Context <8K, max throughput | gpt-oss-120b | cerebras | 14,400 RPD, ~2600 tok/s |
| Context 32K, best one-shot quality | DeepSeek-V3.2 | sambanova | Best reasoning, 20 RPD, first fallback hop |
| Context 32K–196K, privacy-safe | gpt-oss-120b or MiniMax-M2.7 | sambanova | No data training |
| Context 32K–128K, code | codestral-latest | mistral | 256K ctx, purpose-built for code |
| Agentic coding (multi-file) | devstral-latest | mistral | Purpose-built dev agent |
| Reasoning / thinking | magistral-small-latest | mistral | 262K + reasoning |
| High-volume code (>100 calls/day) | ministral-8b-latest | mistral | 1B tok/month budget, cheap per call |
| Compression (auxiliary) | zai-glm-4.7 | cerebras | Fits in 8K, dedicated auxiliary.compression route |

---

## Auxiliary task routing (config.yaml)

Internal Hermes ops — routed off the primary Anthropic model to save cost/latency:

| Task | Provider | Model |
|------|----------|-------|
| compression | cerebras | zai-glm-4.7 (auxiliary.compression, threshold 0.35) |
| web_extract | cerebras | zai-glm-4.7 (auxiliary.web_extract) |
| vision | anthropic | claude-haiku-4-5 (auxiliary.vision) |
| everything else | anthropic | claude-sonnet-4-6 |

There is no separate title-generation or skills-hub auxiliary route configured; those
operations use the primary model unless/until a dedicated auxiliary entry is added to
config.yaml.

---

## Cron job patterns

Hermes does NOT auto-cascade fallback_model for cron jobs — model is fixed at creation.
Only providers actually configured (anthropic, cerebras, sambanova, mistral) are valid here.

Pattern A — high volume, short context (<8K):
  model={"provider": "cerebras", "model": "gpt-oss-120b"}

Pattern B — code-related cron (non-sensitive):
  model={"provider": "mistral", "model": "codestral-latest"}

Pattern C — best quality, once-daily task:
  model={"provider": "sambanova", "model": "DeepSeek-V3.2"}

Pattern D — Anthropic with auto-fallback:
  model={"provider": "anthropic", "model": "claude-sonnet-4-6"}
  (fallback chain: cerebras -> sambanova -> mistral kicks in if Anthropic is down)

---

## Provider quick-reference

| Provider | RPD | Context | Data training | No-credit-card |
|----------|-----|---------|---------------|----------------|
| Cerebras | 14,400 | 8K (free) | No | Yes |
| SambaNova | 20/model | 32K–196K | No | Yes |
| Mistral | ~1B tok/mo | 256K–262K | YES (opt-in req) | Yes |

## OpenAI — wired as explicit-override custom provider (2026-07-06)

Not in the automatic fallback chain. Live in config.yaml as:

```yaml
custom_providers:
- name: openai
  base_url: https://api.openai.com/v1
  key_env: OPENAI_API_KEY
  api_mode: chat_completions
  context_length: 128000
  max_output_tokens: 16384
  models:
    gpt-5.4:
      context_length: 1050000
    gpt-5.5:
      context_length: 1050000
```

Use only via explicit override (`-m gpt-5.4 --provider custom:openai` or a
`delegate_task`/cron `model={"provider": "custom:openai", "model": "gpt-5.4"}` override) —
never assume it's auto-routed. Intended use: cross-provider adversarial review / independent
verifier role, not a routing default (SWE-bench Pro and OSWorld both favor claude-sonnet-5 for
this account's workload — see `docs/routing-proposal-2026-07-06.md` §"Should gpt-5.4/gpt-5.5
replace..." for the full comparison). See the `claude-routing-hierarchy` skill for the CLI
max_tokens gotcha (`cli.py`'s max_tokens resolution ignores a custom provider's
`max_output_tokens` — the gateway path honors it, the plain `hermes chat` CLI path does not;
workaround is a per-call `HERMES_MAX_TOKENS` override, not a global config change).

## Notes

- Cerebras 8K context cap on free tier is a hard limit — do not use for long documents.
- SambaNova DeepSeek-V3.2 has 32K ctx (not 131K like V3.1) — plan prompts accordingly; the
  fallback chain uses V3.2 specifically for its reasoning quality despite the smaller context.
- Mistral 1B token/month budget sounds large but codestral can burn through it quickly on
  large codebases.
- Cerebras resets quota at midnight UTC.
- Ollama is NOT part of chat-completion routing or the fallback chain. It runs locally
  (port 11434) purely to serve embeddings for Hindsight and Graphiti MCP memory layers.
- No Groq, Google Gemini, or GitHub Models provider is configured in this system. Any prior
  documentation referencing those providers described an earlier, unconfigured plan and has
  been removed.
