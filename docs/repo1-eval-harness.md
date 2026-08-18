# repo1 — LLM Efficiency Gateway: Eval Harness, Regression Suite, and Drift Detection

Last updated: 2026-08-18

## What is repo1

`/var/home/rainbow/repo1` is a local LLM efficiency gateway — a FastAPI service that
applies policy redaction, prompt optimization, and cost-tier model routing before
forwarding requests to upstream providers. It is a personal/research project, not a
shared or deployed service.

Structure:
- `apps/api/` — FastAPI gateway (uvicorn, `/v1/chat/completions`, `/providers/health`, `/ui`)
- `packages/policy/` — `PolicyEngine`: pattern-based PII redaction, token budget enforcement
- `packages/optimizer/` — `optimize_messages()`: dedup, trim, context window management
- `packages/router/` — `ModelRouter`: cost-tier routing (local → cheap → standard → premium)
- `packages/telemetry/` — `estimate_tokens()`, Prometheus metrics
- `packages/evals/` — eval harness (see below)

---

## Eval harness design (2026-08-18)

### Motivation

The project had 2 smoke eval stubs and no regression suite. To make the eval system
useful as a CI gate the following were needed:

1. Code-based evaluators — deterministic checks that don't require an LLM judge
2. A regression baseline — golden cases whose scores must not drop between runs
3. A drift detector — statistical alarm for when aggregated pass_rate or avg_score
   drifts below historical norms

### Research synthesis applied

**EWMA one-step-ahead anomaly detection** (prediction-error residual approach):
- Standard EWMA anomaly detection computes z-score against the post-update EWMA.
  This is wrong: after 20 identical observations (e.g. pass_rate = 1.0), the
  estimated variance collapses to 0. A sudden drop produces z = 0/0 → no flag.
- Fix: compute z against the PRE-UPDATE EWMA (prediction error / one-step-ahead
  residual), THEN update the EWMA and variance. This correctly produces z = -100
  for a drop from 1.0 to 0.0 after a constant series.

**Minimum prior variance floor**:
- Even with the pre-update approach, variance can be 0 on the very first drop.
- A `min_variance` floor (default 1e-4) ensures std is never 0, so any first-drop
  produces a finite z-score.

**Warmup period (min_obs)**:
- Drift is only flagged from the `min_obs`-th call onward (default 3). Prevents
  false alarms during the EWMA warm-up.

**NaN/inf guard**:
- Non-finite metric values (NaN, inf) would permanently corrupt the EWMA.
- Guard: flag as drift, skip the update, preserve state for subsequent calls.

**Empty suite semantics**:
- `avg_score` on an empty suite returns `1.0` (vacuously passing), not `0.0`.
  A 0.0 would misfire on callers checking `score < 0.5`.

### Key files

| File | Purpose |
|------|---------|
| `packages/evals/src/llm_gateway_evals/core.py` | Full eval harness: EvalCase, EvalResult, SuiteResult, evaluators, run_eval_suite(), smoke_cases(), regression_cases(), RegressionBaseline, DriftDetector |
| `packages/evals/src/llm_gateway_evals/__init__.py` | Public exports |
| `tests/test_evals.py` | 61 pytest cases across evaluator unit tests, regression suite, drift detector, and end-to-end pipeline guard |
| `tests/test_gateway_api.py` | Existing API tests; `test_provider_health_endpoint` patched to not require live network |

### Evaluators (code-based, no LLM judge)

| Evaluator | What it checks |
|-----------|---------------|
| `_no_crash_check` | Pipeline completes without exception |
| `_policy_check` | `policy.allowed` matches `case.expect_policy_pass` |
| `_redaction_check` | `[redacted]` sentinel appears in messages when expected |
| `_routing_tier_check` | Routed model tier matches `case.expect_tier` (when set) |
| `_optimization_note_check` | Expected optimizer note appears when set |

### Smoke cases (6)

Normal chat, empty messages, PII redaction (password/secret), token budget block,
optimizer dedup (duplicate system prompts), restricted sensitivity routing.

### Regression cases (10)

Golden cases that define pass/fail at the component level:
- `reg_empty_messages_no_crash` — empty input, no exception
- `reg_redact_api_key` — api_key pattern redacted
- `reg_redact_ssn` — SSN pattern partially redacted
- `reg_redact_token_key` — token= key redacted
- `reg_token_limit_blocks_policy` — policy blocks at 200K tokens
- `reg_dedup_system_messages` — optimizer notes duplicate removal
- `reg_restricted_sensitivity_routes_local` — restricted → local tier
- `reg_normal_small_prompt_routes_cheap` — normal + small → cheap tier
- `reg_policy_allows_benign` — benign message passes policy
- `reg_password_redacted_present` — password redacted, request still allowed

### DriftDetector API

```python
from llm_gateway_evals import DriftDetector, run_eval_suite, smoke_cases, regression_cases

det = DriftDetector(alpha=0.3, sigma_threshold=2.0, min_obs=3, min_variance=1e-4)
cases = smoke_cases() + regression_cases()

for each_run:
    result = run_eval_suite(cases)
    drifted = det.update({
        "pass_rate": result.pass_rate,
        "avg_score":  result.avg_score,
    })
    if any(drifted.values()):
        alert("eval drift detected", det.state_snapshot())
```

### Adversarial passes (3)

Three adversarial passes were run after initial implementation. Findings and fixes:

Pass 1:
- Vacuous redaction check had wrong guard order (policy is None checked before
  expect_redaction) — fixed: guard expect_redaction first.
- Empty `__init__.py` prevented `from llm_gateway_evals import run_eval_suite` — fixed.
- `test_provider_health_endpoint` required live Ollama — monkeypatched `main._provider_health`.

Pass 2:
- `avg_score` on empty suite returned `0.0` — changed to `1.0` (vacuous pass).
- Missing warmup non-flag test — added `test_no_flag_during_warmup`.
- End-to-end drift guard only checked `pass_rate`, not `avg_score` — added.
- Docstring for `min_obs` was slightly inaccurate — corrected.

Pass 3:
- NaN/inf metric values would permanently corrupt EWMA state — added guard:
  flag as drift, skip update, preserve state.

### Test result baseline

As of 2026-08-18: 57 tests from the pre-existing suite + 61 from the new eval suite
= fully passing, 0 failures. (The provider health test failure on Ollama is resolved.)

---

## Running the tests

```
cd /var/home/rainbow/repo1
python3 -m pytest -q
```

Expected: all passing, ~0.5s. The suite exercises real pipeline components
(PolicyEngine, optimize_messages, ModelRouter) with no mocking — deterministic because
those components are stateless and rule-based.
