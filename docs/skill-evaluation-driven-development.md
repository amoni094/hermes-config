---
name: evaluation-driven-development
description: >
  Use when turning every AI agent change into a measured experiment with before/after comparison. EDD is the offline validation gate between developing a change and merging it — it answers "does it work?" and "did it regress?".
version: 1.1.0
triggers:
  - "evaluate my agent change"
  - "did I introduce a regression"
  - "run evals before merging"
  - "evaluation-driven development"
  - "measure agent performance before and after"
  - "test my prompt change"
  - "evaluate my skill"
  - "run skill evals"
  - "test this skill before shipping"
  - "benchmark my skill"
related_skills:
  - autonomous-agent-loop-design
  - verification-before-completion
  - adversarial-review
  - gepa-omni-optimization
---

# Evaluation-Driven Development (EDD)

Pattern from Alejandro Aboy (Workpath, Jun 2026): every AI agent change is a hypothesis.
Before merging, answer two questions:
1. **What is the performance of the new feature?**
2. **Did my change introduce any regressions?**

Only when both look good do you accept the pull request.

> "The fact that they're not complaining doesn't mean there's no issue going on."
> — Alejandro Aboy

## The Silent Failure Problem

AI agent regressions are invisible without explicit evaluation:
- Change a prompt, refactor a tool → an old feature quietly stops working
- Example: cleaning noisy instructions out of a system prompt made one agent start
  fabricating IDs it previously got right. No error. No complaint. Just wrong.

Without EDD, you only discover regressions when users hit them.

## Core Loop

```
branch → develop change → generate traces → run evaluators
→ compare experiment vs baseline → accept PR (or iterate)
```

Every feature starts as a **hypothesis on a branch**. Every feature ends in a **PR
backed by an experiment** with clear traces and metrics.

## Two Modes

### Mode 1 — Quick Manual Check (small changes)
- Fire ~30 fresh traces from your changed agent
- Read traces back manually (or with a targeted judge)
- No persistent dataset, no formal experiment — ephemeral, takes minutes
- Best for: small prompt tweaks, single-behavior fixes, targeted regressions

### Mode 2 — Automated Experiment (significant changes)
- Turn traces into a **dataset** (named, versioned set of test cases)
- Run an **experiment** where LLM judges score every item automatically
- Compare Experiment A (before) vs Experiment B (after) numerically
- This is the ONLY way to catch subtle regressions reliably
- Best for: new features, refactors, model upgrades, major prompt changes

The Aggression setting controls adversariality of simulated traces:
- Happy path → normal trace generation
- Adversarial → corner cases designed to break the agent

## Implementation Components

### 1. Evaluation harness
A headless Claude Code run that:
- Loads the agent under test
- Generates simulated traces using the Aggression setting
- Feeds traces to evaluators
- Reports results as a named experiment

You can run this as a Claude Code skill invoked before merge.

### 2. Evaluators
Three types, in order of cost and reliability:
- **Code-based**: deterministic checks — exact string match, schema validation, regex, output length bounds
- **Heuristic**: statistical signals — token count, latency, retry count
- **LLM-judge**: semantic quality — correctness, relevance, tone, factual accuracy

Use code-based + heuristic first. Add LLM-judge only where deterministic checks can't cover.

**Validate your LLM judge**: before trusting it, align it with human judgments on 20-50 examples.
If the judge disagrees with humans on >20% of cases, don't trust it at all.
Real failure mode: "Our LLM judge passed everything. It was wrong."

### 3. Observability platform
Tools: Opik (open-source), Langfuse, Braintrust.
These store traces, manage datasets and evaluators, run experiments, and enable comparison.
Opik has a free managed tier (25k spans/month).

## Minimal EDD Without Observability Tools

If you don't have Opik/Langfuse yet, minimal EDD is still possible:

```
1. Write 5-10 test prompts that cover your feature + existing behaviors you care about
2. Run your agent BEFORE the change, save outputs to baseline.json
3. Make your change
4. Run the same test prompts AFTER, save to experiment.json
5. Compare with a simple diff or LLM judge: did anything regress?
```

This is "EDD-lite" — not as rigorous, but 10x better than shipping without any comparison.

## The Hypothesis-First Pattern

Every change starts as a stated hypothesis:
- "Adding the user's OKR history to context will increase alignment_score by >5%"
- "Removing the verbose error handling will reduce token usage without hurting accuracy"
- "Switching from gpt-4o to claude-sonnet-4-6 will maintain quality while cutting cost by 40%"

The hypothesis determines:
- What traces to generate (what inputs test the hypothesis)
- What evaluators to run (what metrics measure the hypothesis)
- What regression suite to run (what existing behaviors must not change)

Without a stated hypothesis, evaluation results are ambiguous — you can't tell if a
change is good without knowing what you were trying to achieve.

## Regression Suite Discipline

Maintain a growing regression suite: when a bug is fixed, add the test case to the suite.
Rules:
- Every fixed agent bug becomes a test case
- Every user-reported failure becomes a test case
- Run the full regression suite on every significant change
- Never shrink the suite without justification

This is Evaluation-Driven Development's version of test-driven development.

## Integration with Hermes

EDD in Hermes can be run as:
- A `/edd` skill that wraps the evaluation harness
- Pre-merge gate in the `/night` pipeline (before PR reviewer)
- Manual check after any significant skill or prompt change
- Cron job that runs the regression suite nightly

EDD is not just for agents — apply it to any Hermes skill that runs on real tasks:
if you change a skill's instructions, run it on a set of representative tasks and
compare the outputs before and after merging the skill change.

## Quality Flywheel: Loop Until Target Met

Pattern from google/skills Agent Platform Eval Flywheel skill (2026): run stages in order
on the first pass, then loop stages 2-5 until quality targets are reached. Do NOT exit
after a single evaluation pass — one pass only establishes a baseline.

The five stages (run in order, then loop 2→5):

1. **Define** — state the hypothesis + quality targets before touching any code or prompt.
   What score on which metric constitutes "done"? Write it down. Without this, you have no
   exit condition for the loop.
2. **Build dataset** — collect representative test cases (real traces, synthetic generation,
   or adversarial corner cases). Minimum 10 items; 50+ for statistically meaningful regression detection.
   For skill-level EDD, minimum 5 evals covering: happy path, edge case, adversarial input, and regression case.
3. **Evaluate** — run evaluators (code-based → heuristic → LLM-judge in that order).
   Record all scores. This is your baseline on pass 1; a checkpoint on passes 2+.
4. **Analyze failures** — cluster failures, identify root causes. Do NOT jump straight to
   fixing. Failure analysis determines WHETHER to change code, prompt, or dataset.
5. **Improve** — make exactly one targeted change per loop iteration. Multi-change loops
   produce unattributable score changes.

**Loop exit condition:** STOP when all of these hold in the same pass:
- Primary metric ≥ target (as defined in stage 1)
- No regression in secondary metrics vs. baseline (stage 3, pass 1)
- Failure analysis on the latest pass shows no HIGH-severity root causes remaining

**Shortcuts that waste time** (from google/skills):

| Shortcut | Why it fails |
|---|---|
| Tune the metric threshold down so it passes | Hides real failures — fix the agent, not the bar |
| Add more training examples before fixing root causes | Training data can't fix broken logic |
| Run evaluation only on happy-path inputs | Corner-case failures dominate production issues |
| Fix multiple things in one iteration | Score changes become unattributable |
| Declare success after one passing run | Statistical noise — need 2+ consecutive clean passes |

**Consecutive-pass discipline:** a single clean pass is not sufficient. Require 2 consecutive passes
with no HIGH-severity failures before declaring the loop complete. This catches evaluation noise
and prevents premature exit on a lucky batch.

## EDD + GEPA omni: Automatic Optimization

When EDD finds a skill or prompt scoring below threshold, GEPA omni can drive
the improvement loop automatically instead of manual iteration:

1. EDD defines the evaluation harness (test cases + score function)
2. GEPA omni runs the optimization: parallel GEPA / AutoResearch / Meta-Harness
   each exploring with 1/3 of budget, best candidate handed to fresh engine
3. The optimized artifact is sent back through EDD for regression check
4. If score > threshold and no regressions, accept the change

This turns EDD from "measure and manually fix" into "measure and automatically fix."
The EDD harness IS the GEPA evaluator. No duplicate work.

Key: your EDD test cases must be deterministic (temperature=0 for LLM judges) and
representative (cover the distribution of real inputs, not just happy paths). A
GEPA optimizer chasing a noisy evaluator will produce garbage.

See the `gepa-omni-optimization` skill for the full API and Hermes-specific patterns.

## Skill-Level EDD: Evaluating Hermes Skills (from Anthropic skill-creator, Aug 2026)

When the artifact under evaluation is a Hermes skill (not an agent loop or prompt), use
this specific pattern adapted from Anthropic's skill-creator workflow:

### Parallel with-skill vs baseline subagent launch
**Critical discipline:** spawn both runs in the SAME turn. Do NOT do with-skill first,
then come back for baselines — fire everything simultaneously so results arrive together.

For each test case:
- **With-skill run:** subagent loads the skill and executes the test prompt; saves outputs to
  `<workspace>/iteration-N/eval-<name>/with_skill/outputs/`
- **Baseline run** (choose one):
  - New skill: no skill loaded, same prompt
  - Improving existing skill: snapshot old version first (`cp -r skill/ skill-snapshot/`),
    point baseline at snapshot, save to `old_skill/outputs/`

### evals.json schema
Save test cases to `evals/evals.json` before running. Schema:
```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "eval_name": "descriptive-name-not-just-eval-0",
      "prompt": "User's exact task prompt",
      "expected_output": "Description of expected result",
      "files": [],
      "assertions": []
    }
  ]
}
```
Write the `assertions` array WHILE the subagent runs — draft them during the wait, not after.
Each assertion: `{ "type": "contains|regex|llm_judge|schema", "value": "...", "weight": 1.0 }`
- `contains`: output must contain the literal string in `value`
- `regex`: output must match the regex pattern in `value`
- `llm_judge`: pass `value` as the judging criterion to an LLM (returns 0.0–1.0 score)
- `schema`: output must parse as valid JSON matching the JSON Schema object in `value`

### While runs are in progress: draft assertions
Do NOT idle-wait for subagents. Use the time to:
1. Draft assertions for each test case (add to eval_metadata.json)
2. Identify edge cases not covered by existing test prompts
3. Note which output qualities are verifiable (deterministic) vs require LLM-judge

### eval_metadata.json per eval directory
```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Reviewing results: show before analyze
After runs complete, show the user outputs BEFORE making your own quality judgment.
Do NOT analyze and declare a winner without giving the user a chance to see examples.
Create a benchmark.json pairing with-skill vs baseline outputs, then surface it.

Pattern for benchmark.json:
```json
[
  {
    "eval_id": 1,
    "eval_name": "descriptive-name",
    "with_skill_output": "...",
    "baseline_output": "...",
    "assertion_results": [{"assertion": "...", "passed": true, "score": 1.0}],
    "overall_score": 0.85
  }
]
```

### Workspace layout
```
<skill-name>-workspace/     ← all paths below are relative to this root
  iteration-1/
    descriptive-eval-name/
      with_skill/outputs/
      old_skill/outputs/      (or without_skill/outputs/)
      eval_metadata.json
  iteration-2/
    ...
  evals/
    evals.json              ← test cases, relative path: <workspace>/evals/evals.json
```
Don't create all directories upfront — create them as each subagent produces output.

### Skill description optimization (final step)
After the skill body is stable and user is satisfied, optimize the description for
triggering accuracy. The description is the primary triggering mechanism — undertriggering
(skill not used when it should be) is the dominant failure mode.

Technique: generate candidate descriptions with varied phrasing, run each against
your test prompts, measure how often the skill triggers correctly, pick the highest-scoring
variant. Keep the "Use when" trigger clause pushy — err toward over-triggering rather than
under-triggering for skills that have meaningful workflow value.

### Progressive disclosure discipline
- Keep SKILL.md under ~500 lines; beyond that, split detail into `references/` files
  with clear pointers from SKILL.md on when to read each
- Metadata (name + description) is always in context (~100 words)
- SKILL.md body loads when triggered
- References load only when explicitly needed (unlimited size, no context overhead)
- For multi-domain skills, organize by variant: `references/aws.md`, `references/gcp.md` etc.

### Webapp testing eval pattern (Playwright)
For skills whose output is a web UI or dashboard, add a Playwright-backed eval layer
on top of the standard LLM-judge layer:
- Implement a `scripts/with_server.py` harness that: starts the target server on a
  free port, waits for readiness (health-check GET), runs the eval script, then tears
  down the server. Pattern: `python scripts/with_server.py --server "python app.py" --port 3000 -- python eval.py`
- Eval script: navigate → screenshot → DOM check → assert on rendered state
- This gives a deterministic verification layer that LLM judges can't provide
- Decision tree: static HTML → read and selector-assert directly; dynamic SPA → server + Playwright

## Pitfalls

- **Baseline not fired simultaneously** (skill-level EDD) — spawning with-skill and baseline
  subagents sequentially instead of in the same turn doubles elapsed time and introduces
  scheduling variance. Fire both in a single `delegate_task(tasks=[...])` call.

- **All workspace directories created upfront** — resist the urge to mkdir the full workspace
  layout before any subagent runs. Create directories as each subagent produces output.
  Pre-creating dirs hides whether runs actually succeeded.

- **Analyzing before showing** — after runs complete, the instinct is to immediately declare
  a winner. Don't. Show raw with-skill vs baseline outputs to the user first via benchmark.json;
  let them see examples before you render judgment.

- **Metric bar lowered to declare success** — if scores are below target, fix the agent/skill,
  not the threshold. A lowered bar hides real failures.

- **Single-pass success declaration** — one clean evaluation pass is noise. Require 2 consecutive
  passes with no HIGH-severity failures before declaring the loop complete.

- **LLM judge not validated** — before trusting an LLM judge, align it with 20-50 human judgments.
  If disagreement > 20%, the judge is unreliable. Don't use it as the primary quality gate.

- **with_server.py as black-box assumption** — there is no pre-installed with_server.py; you must
  implement the server harness yourself when running webapp eval patterns. See pattern description
  in the Webapp testing section.
