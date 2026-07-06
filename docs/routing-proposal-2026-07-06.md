# Routing & Multi-Model Workflow Proposal — 2026-07-06

Status: DRAFT — pending adversarial review round 1
Author: agent (this session), grounded in live-verified state, not the existing docs.

## 0. Why this doc exists

A full provider/model survey (this session) found that `docs/routing-and-workflow.md`,
`README.md`'s routing section, `docs/current-workflow.md`, and the
`claude-routing-hierarchy` / `claude-routing-matrix` skills all describe providers,
models, and config sections that **do not exist in the live `~/.hermes/config.yaml`**.
This doc separates verified ground truth from the existing (partly fictional) docs,
then proposes a corrected routing structure grounded only in what is actually
configured or actually supported by the Hermes codebase.

Every claim below is tagged `[VERIFIED]` (checked against live config/API/source) or
`[PROPOSED]` (a recommended change, not yet applied).

## 1. Verified ground truth

### 1.1 Providers with a working API key (checked via direct `/v1/models` calls)

| Provider | Key present | Models returned | Notes |
|---|---|---|---|
| anthropic | yes | 9 | claude-sonnet-5, claude-fable-5, claude-opus-4-8, claude-opus-4-7, claude-sonnet-4-6, claude-opus-4-6, claude-opus-4-5-20251101, claude-haiku-4-5-20251001, claude-sonnet-4-5-20250929 |
| openai | yes | 100+ | gpt-5.x family (5/5.1/5.2/5.3-chat-latest/5.4/5.5 + codex variants), o1/o1-pro/o3/o3-mini/o4-mini, gpt-4.1 family, gpt-4o family, embeddings/whisper/tts/moderation/image/audio |
| cerebras | yes | 3 | gpt-oss-120b, zai-glm-4.7, gemma-4-31b — 8K context, free tier, Cloudflare requires a normal User-Agent header on direct calls |
| sambanova | yes | 6 | DeepSeek-V3.1 (131K), DeepSeek-V3.2 (32K), Meta-Llama-3.3-70B-Instruct (131K), MiniMax-M2.7 (196K), gemma-4-31B-it (131K), gpt-oss-120b (131K) |
| mistral | yes | 70+ (partial enumeration — not fully counted) | codestral, devstral, magistral, ministral, mistral-large/medium/small families, voxtral, OCR, embed — far larger catalog than any doc lists |
| hindsight | yes (`HINDSIGHT_LLM_API_KEY`) | n/a | memory-subsystem reasoning model, not part of chat routing — separate purpose, do not conflate |

**Freshness note:** Anthropic/OpenAI/Cerebras/SambaNova/Mistral model lists above were
obtained via direct `/v1/models` API calls earlier in this same task (before an
intermediate context compaction), not re-queried in this exact pass. The `.env` key
presence/absence and the `config.yaml` structure (§1.3) *were* re-verified live in
this pass. If material time has passed since the original survey, re-run the
`/v1/models` calls before treating exact model names as current.

### 1.2 Providers with NO key present (confirmed absent from `.env`)

groq, gemini/google, xai, deepseek (standalone), glm, minimax, kimi, dashscope, xiaomi,
huggingface, openrouter, kilocode, opencode-zen, opencode-go, github-models.

**Every one of these appears in the current `routing-and-workflow.md` and/or README as
if configured. None of them are.** This is not a minor staleness issue — it means
current docs actively describe a routing system this instance does not have.

### 1.3 Actual live `config.yaml` routing structure (full file read, 133 lines; `auxiliary` and `custom_providers` keys confirmed absent by direct grep in this pass — 0 matches for either token)

```yaml
model:
  provider: anthropic
  default: claude-sonnet-5
fallback_model:
- provider: cerebras
  model: gpt-oss-120b
  base_url: https://api.cerebras.ai/v1
- provider: sambanova
  model: DeepSeek-V3.2
  base_url: https://api.sambanova.ai/v1
- provider: mistral
  model: mistral-large-latest
  base_url: https://api.mistral.ai/v1
delegation:
  model: claude-sonnet-5
  provider: anthropic
  max_spawn_depth: 1
  max_concurrent_children: 3
```

Confirmed by full-file read: there is **no** `custom_providers:` block, **no**
`auxiliary:` block, and **no** 4th fallback entry for a local/Ollama model anywhere
in the file.

### 1.4 What the Hermes codebase actually supports (source-verified, not doc-verified)

Grepping `hermes-agent` source (not just docs) confirms:
- `auxiliary.compression.model`, `auxiliary.vision.provider`, and similar
  `auxiliary.<task>.<field>` overrides are **real, implemented config keys**
  (`agent/auxiliary_client.py`, `hermes_cli/tips.py` line 329). This is a genuine
  product feature — just never configured on this instance.
- `custom_providers:` entries are real and require an explicit `api_mode` field for
  providers whose default endpoint auto-detects the wrong API shape (documented
  in this repo's own `custom-provider-api-mode-routing.md` skill reference — this
  was previously debugged for `custom:openai` + `gpt-4.1` and hit
  `codec_responses` auto-detection before the explicit `api_mode: chat_completions`
  fix).

**Conclusion: because `config.yaml` has no `auxiliary:` block, context compression
currently runs on the main model (`claude-sonnet-5`), not a cheap auxiliary model.**
This directly contradicts memory/docs claims ("Claude Haiku is the auxiliary model
for compression", "cuts background token cost 85%+") — that behavior is not
happening today; it is only the intended-but-unconfigured behavior of the feature.

## 2. Divergence summary (existing docs vs. verified reality)

| Doc/skill | Claim | Reality | Severity |
|---|---|---|---|
| `routing-and-workflow.md`, README | Main model `claude-sonnet-4-6` | Main model is `claude-sonnet-5` | High — every model reference is one generation stale |
| `routing-and-workflow.md` | Fallback #2 is `sambanova/DeepSeek-V3.1` | Live config uses `DeepSeek-V3.2` | Medium |
| `routing-and-workflow.md`, README | 4th fallback: local `qwen3:8b` via Ollama | No such entry in `fallback_model:` | Medium |
| `routing-and-workflow.md` | Capability routing to Gemini 2.5 Flash, Groq llama-3.3-70b, GitHub Models | None of these providers have a key configured | High — entirely fictional for this instance |
| `routing-and-workflow.md` | Context-compression auxiliary model is Claude Haiku | No `auxiliary:` block exists; compression runs on the main model | High — real cost impact, not just a doc error |
| `claude-routing-matrix` skill | Orchestrator should be "Opus-class", workers "Sonnet-class" | `delegation.model` is `claude-sonnet-5` for both main and delegation — no opus wiring anywhere | Medium — skill describes a policy never implemented in config |
| All docs | OpenAI provider | Never mentioned, despite a working key and 100+ available models | High — a fully paid, functional provider is invisible in every doc |
| All docs | `custom_providers:` block exists | Does not exist in live `config.yaml` (a *skill reference doc* describes fixing one from a past debugging session, but it isn't currently applied) | Medium |

## 3. Research synthesis (routing/cascade literature)

**English sources:**
- FrugalGPT (Chen et al., arXiv:2305.05176, TMLR 2024) — canonical LLM cascade:
  query cheap→expensive sequentially, escalate only when a scoring/reliability
  function rejects the cheaper answer. Reports up to 98% cost reduction at equal
  quality, or +4% accuracy at equal cost vs. always using the strongest model.
- RouteLLM — trains a lightweight router (matrix factorization / BERT) on
  preference data to predict whether a strong model's answer would beat a weak
  model's for a given query; a cost threshold tunes the strong-model call rate.
- "A Unified Approach to Routing and Cascading for LLMs" (arXiv:2410.10347) —
  formalizes "cascade routing" as the union of routing (single-shot classifier
  picks a model) and cascading (sequential escalation); the critical bottleneck in
  both is the quality/confidence estimator, not the size of the model pool.
- "Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey"
  (Moslem et al., arXiv:2603.04445) — taxonomy distinguishing routing/cascading
  across *independently trained* models from Mixture-of-Experts (routing *within*
  one model); this is the correct frame for a multi-provider setup like this one.
- OmniRouter (arXiv:2502.20576) — treats multi-LLM routing as a constrained
  optimization problem with an explicit budget and performance floor, two-stage
  query-to-model assignment.
- Mixture-of-Agents pattern (general literature) — several models propose in
  parallel, one aggregator synthesizes; improves quality over any single model at
  the cost of ~Nx spend/latency. Best applied to high-stakes synthesis, not
  high-volume routine tasks.

**Non-English sources (Japanese, Chinese):**
- 効率的な大規模言語モデル推論のための動的モデルルーティングとカスケード：サーベイ
  (Japanese review/commentary on arXiv:2603.04445) — confirms the same routing/
  cascading taxonomy is recognized independently across language communities; no
  contradicting framework found.
- 大语言模型与混合思维表征的级联实现成本高效的推理 (Chinese commentary on the ICLR'24
  "LLM Cascades with Mixture of Thought Representations for Cost-Efficient
  Reasoning" paper) — cascades cheap→expensive models using answer-consistency /
  chain-of-thought-diversity signals to decide when to escalate, rather than a
  fixed always-escalate or never-escalate rule.
- RouteLLM Chinese-language technical writeups (developer.aliyun.com) and
  LLMRouter (智源社区, UIUC open-source multi-strategy router) corroborate the
  same core finding: the router/estimator quality is the dominant factor in cost
  savings, not which models are in the pool.
- No non-English source contradicted or added a materially different paradigm
  beyond the English-language literature; the survey (2603.04445) is itself the
  most current unifying reference and is discussed consistently across all three
  language communities searched.

**Takeaway for this instance:** none of the literature argues for routing across as
many providers as possible. The consistent finding is that a *good escalation/
routing signal* on a *small, well-understood model set* beats a wide but
loosely-managed provider list. This favors correcting/tightening the existing
5-provider setup over adding more (unconfigured) providers.

## 4. Proposed routing structure [PROPOSED]

### 4.1 Primary chain — unchanged in spirit, corrected in fact

| Role | Model | When | Change from current docs |
|---|---|---|---|
| Main orchestration | `claude-sonnet-5` | Default, all sessions | Fixes stale `claude-sonnet-4-6` references |
| Delegation workers | `claude-sonnet-5` | Subagents (matches live `delegation.model`) | Drops the never-implemented "opus-class orchestrator" policy from `claude-routing-matrix`; that skill should either be implemented in config or marked aspirational, not both |
| High-stakes escalation | `claude-opus-4-8` | Security/architecture review, complex debugging | Confirmed available in Anthropic model list; not currently wired anywhere — recommend using explicitly via model override on delegate_task or a manual `-m` flag, not adding new config plumbing for a single-tier escalation |
| Max reasoning / adversarial red-team | `claude-fable-5` | Formal verification, >100K token synthesis | Unchanged, already correct in existing docs |

### 4.2 Auxiliary task routing — new, actually activates an existing but unused feature

```yaml
auxiliary:
  compression:
    provider: cerebras
    model: zai-glm-4.7
    base_url: https://api.cerebras.ai/v1
```

Rationale: `auxiliary.compression.model` is a real, source-verified config key
(`agent/auxiliary_client.py`). Today compression silently runs on the main model
because this block is absent — meaning every long session pays full Claude-Sonnet
pricing for a mechanical summarization task. Cerebras is already a trusted,
already-keyed, free-tier fallback provider; pointing compression at it delivers
the token-cost reduction the docs have been claiming for a feature that was never
turned on. This is the single highest-value, lowest-risk change in this proposal.

**Model choice within Cerebras — do not default to `gpt-oss-120b` here.** This
repo's own debugging notes (`custom-provider-api-mode-routing.md`) document that
`gpt-oss-120b` returns a reasoning-only response with no `content` key on some
calls, which previously triggered a false "context length exceeded" failure on
this exact compression path. Recommending that same model as the primary
compression target would reintroduce a bug already diagnosed in this repo.
`zai-glm-4.7` (a non-reasoning Cerebras model, also already keyed) is the safer
primary choice. `gpt-oss-120b` should be treated as unsuitable for this role
until the reasoning-only-response issue is fixed upstream or explicitly handled
in `auxiliary_client.py`. **Verify with a live compression cycle before relying
on this in production regardless of model choice** (see §6 test plan).

### 4.3 Fallback chain (outage continuity) — keep current order, fix version only

1. `cerebras/gpt-oss-120b` — fastest, highest quota, matches live config
2. `sambanova/DeepSeek-V3.2` — fix doc to match live config (was incorrectly
   documented as V3.1)
3. `mistral/mistral-large-latest` — largest context ceiling among the three

No 4th "local qwen3:8b" entry — it does not exist in `fallback_model:` and no
Ollama chat model is configured for that purpose (Ollama is embeddings-only here,
per `MEMORY.md`). Remove this claim from all docs rather than add speculative
config for a capability that isn't provisioned.

Per the cascade-routing literature (§3): fallback exists for *continuity during an
outage*, not for *quality optimization* — ordering by available quota/speed (as
today) is correct and should not be changed to a quality-first order.

### 4.4 OpenAI — document as available-but-idle, wire for one specific use case

**Tension to resolve first:** §3's literature takeaway argues against provider
sprawl for routine routing. Adding OpenAI here is not a contradiction of that
takeaway only because it is scoped to a narrow, non-routine use case (below) —
if this scope discipline is not maintained (e.g. someone later wires it into
automatic fallback), the addition becomes exactly the sprawl §3 warns against.

**Not redundant with `claude-fable-5`:** §4.1 already assigns `claude-fable-5` to
"formal verification / adversarial red-team" duty. That is a same-family
(Anthropic) strongest-model escalation — useful for catching *depth* issues
(missed edge cases, insufficient rigor) but not for catching *correlated* failure
modes shared across the whole Claude model family (shared training-data blind
spots, shared systematic biases). The OpenAI addition below targets that second,
distinct failure class — a genuinely different model family reviewing Claude's
own output. Use `claude-fable-5` for "did we think hard enough"; use the OpenAI
cross-check for "are we all wrong in the same way." Both may run in the same
review cycle without duplication.

OpenAI has a working, paid-for key and 100+ models, and is currently invisible in
every doc and every config file. Two options were considered:

- **Rejected:** add OpenAI into the main fallback chain. Anthropic already has an
  internal escalation ladder (sonnet-5 → opus-4-8 → fable-5); adding a 4th
  cross-provider fallback tier increases config surface for a failure mode
  (Anthropic + 3 fallbacks all failing) that has not been observed.
- **[PROPOSED] Accepted:** add a single `custom_providers` entry for OpenAI,
  reusing the already-debugged fix from `custom-provider-api-mode-routing.md`
  (explicit `api_mode: chat_completions` — that fix was validated against
  `gpt-4.1` specifically; the `api_mode` setting is provider-level, not
  model-specific, so it should carry over to other OpenAI chat models, but this
  is an inference, not a re-verified fact — confirm with the smoke test in §6
  before depending on a different model than the one originally debugged), for
  **manual, explicit use in cross-provider adversarial review** — i.e., when
  `adversarial-review` or Ouroboros' evaluate step benefits from a genuinely
  different model family checking Claude's own output. This matches the
  literature's actual argued benefit of heterogeneous ensembles (catching
  correlated failure modes a same-family cascade cannot), and matches this
  repo's own stated trigger conditions for escalation (security, architecture,
  formal verification) rather than being used for routine traffic.

```yaml
custom_providers:
  - name: openai
    base_url: https://api.openai.com/v1
    key_env: OPENAI_API_KEY
    api_mode: chat_completions   # required — auto-detect defaults to codex_responses and breaks non-Responses-API models
```

Usage: invoked explicitly (e.g. `-m gpt-5.1 --provider custom:openai`) during
high-stakes adversarial review rounds, not part of automatic routing. The exact
submodel (gpt-5.1 vs. another gpt-5.x variant) is illustrative, not prescriptive —
pick based on what's current at time of use; re-verify `api_mode` still resolves
correctly if the submodel changes materially (e.g. moving to a model OpenAI
serves only via the Responses API).

### 4.5 Providers to explicitly mark "not provisioned" (not aspirational)

Remove all routing-table entries for groq, gemini/google, xai, github-models, and
openrouter. Replace with one line in the corrected doc: "the following providers
are supported by Hermes but have no API key configured on this instance: groq,
gemini, xai, github-models, openrouter, deepseek, glm, minimax, kimi, dashscope,
huggingface, kilocode, opencode-zen/go. Activating any of them requires adding
the corresponding key to `.env` and, if needed, a `custom_providers` entry." This
removes the misleading "configured" framing without deleting useful context about
what *could* be added later.

## 5. Net change summary

| Area | Action |
|---|---|
| Model version references | Correct `claude-sonnet-4-6` → `claude-sonnet-5` everywhere |
| Fallback model version | Correct `DeepSeek-V3.1` → `DeepSeek-V3.2` |
| Fictional 4th fallback (local qwen3:8b) | Remove |
| Groq / Gemini / GitHub Models / OpenRouter routing tables | Remove; replace with one "not provisioned" note |
| `auxiliary.compression` | Add config block pointing compression to Cerebras (verify first — see §6) |
| OpenAI | Add as `custom_providers` entry for explicit cross-provider adversarial-review use only; not in automatic fallback |
| `claude-routing-matrix` skill (opus orchestrator / sonnet worker policy) | Either implement in `delegation.model` or relabel the skill as an aspirational pattern, not current config — decide and make consistent |
| `claude-routing-hierarchy` skill | Update to reference this proposal once approved |

## 6. Test / verification plan before finalizing

1. Add `auxiliary.compression` block on a scratch copy of config, run a long
   session to force a compression cycle, confirm the compression call actually
   lands on Cerebras (check for the "reasoning-only response" failure mode noted
   in §4.2) — do not ship this change unverified.
2. Add the `custom_providers: openai` entry and run one `-m gpt-5.1 --provider
   custom:openai -z "hi"` smoke test to confirm `api_mode: chat_completions` still
   resolves correctly (matches the already-solved fix, but config drift is
   possible).
3. `hermes config check` after any config.yaml edit.
4. `hermes doctor` (note: known truncation issue in this environment — cross-check
   with direct provider API calls if doctor output looks incomplete).

## 7. Open questions for adversarial review

- Is offloading compression to Cerebras (a weaker/free-tier model) an acceptable
  quality tradeoff for a mechanical summarization task, or does long-context
  compression need main-model-level judgment to avoid losing salient details?
- Should the OpenAI custom_provider entry be scoped to specific tasks
  (adversarial-review only) via a policy note, or is that unenforceable without
  actual code changes, making it a "trust the operator" convention only?
- Does adding `custom_providers: openai` risk being picked up by
  `delegate_task`/cron flows unintentionally if a future config change sets it as
  a default provider? (Mitigation: explicit invocation only, documented as such.)
