# Adversarial Critique of hermes-config

Generated: 2026-06-30

This is a hostile review of the exported `hermes-config` repository and the underlying Hermes operating setup. The goal is to identify where an attacker, a careless operator, or future-you under time pressure would get burned.

## Executive summary

The setup is strong in capability and operational maturity, but it has four main attack surfaces:

1. configuration/secret export mistakes
2. skill sprawl and routing ambiguity
3. optional integration drift
4. local auxiliary-model mismatch and hidden complexity

The private repo created for this task is reasonably sanitized, but the underlying environment still contains enough adjacent sensitive material that a sloppy future export could leak more than intended.

## Findings

### 1. High: nearby secret-bearing files make “copy the config repo” a recurring footgun

Observed locally:
- `~/.hermes/.env` exists
- `~/.hermes/auth.json` exists by convention and is excluded here
- gateway/session/state/log stores exist under the same tree as the safe config files

Why this is dangerous:
- your safe files and unsafe files live close together
- future “backup ~/.hermes” or “git init in ~/.hermes” actions could accidentally publish credentials, OAuth tokens, bot tokens, or private chat metadata

What mitigates it now:
- this export excluded `.env`, auth stores, state DBs, and raw logs
- secret redaction is enabled in Hermes

What still worries me:
- safety currently depends more on operator discipline than on hard separation

Recommendation:
- maintain a dedicated export repo/workdir, never initialize git inside `~/.hermes`
- add explicit `.gitignore` rules for `.env`, `auth.json`, `state.db*`, `logs/`, `sessions/`, `channel_directory.json`, `gateway_state.json`, and `processes.json`
- codify export rules in AGENTS.md or a local skill

### 2. Medium-High: skill sprawl increases wrong-skill selection risk

Observed:
- large local skill inventory with many meta/workflow/Hermes-internal skills
- multiple families overlap in review, workflow, observability, memory, cron, and self-optimization
- curator is disabled, so drift pressure accumulates

Why this is dangerous:
- the more overlapping skills you have, the easier it is for an agent to load a merely-relevant skill instead of the best one
- duplicated guidance creates instruction collisions
- stale local skills silently override better current practice

Adversarial angle:
- this is not a classic attacker exploit; it is a reliability exploit
- the system can be nudged into suboptimal behavior by ambiguous routing and old instructions

Recommendation:
- define canonical entry skills
- archive or merge duplicates
- patch overlapping skills so they explicitly route to the umbrella skill

### 3. Medium: auxiliary local-model path may be underprovisioned relative to the main workflow

Observed:
- main context length: 128k
- local custom provider context for `qwen3:8b`: 64k
- local model is used for several helper/auxiliary roles

Why this is dangerous:
- failures in helper roles are easy to miss because they do not always fail loudly
- titles, triage, curator passes, and other helper actions can degrade silently when context is bigger than expected
- mixed-context systems produce inconsistent behavior that looks “flaky” instead of obviously broken

Recommendation:
- either verify and raise local helper context, or constrain helper prompts more aggressively
- keep helper responsibilities narrow and short-context by design

### 4. Medium: manual approvals are safe, but they can hide process debt

Observed:
- `approvals.mode: manual`

Critique:
- manual approvals reduce accidental damage, which is good
- but they can also conceal that too many routine tasks still require constant human supervision
- if the workflow becomes tedious, humans start approving reflexively, which defeats the point

Recommendation:
- either keep manual and accept the friction consciously
- or move to `smart` and verify that your guardrails still match your risk tolerance

### 5. Medium: optional bridge/tool surfaces are not uniformly healthy

Observed from doctor:
- WhatsApp bridge dependencies have vulnerabilities
- some optional surfaces are missing system dependencies or credentials

Adversarial angle:
- stale optional integrations are ideal hiding places for future breakage
- they create noisy alerts, false confidence, and maintenance debt

Recommendation:
- classify each optional integration as one of:
  - active and maintained
  - intentionally disabled
  - experimental and isolated
- do not leave them in a vague middle state

### 6. Medium: cron/watchdog estate is useful but creates background-complexity debt

Observed:
- several active cron/watchdog jobs
- some jobs still reference `deliver: origin` even though CLI-local cron delivery semantics differ
- strong automation footprint across sync, watchdog, memory audit, and guard scripts

Why this matters:
- background automation improves resilience, but every extra job creates hidden state and debugging branches
- cron complexity can make failures look like random environmental weirdness

Recommendation:
- keep a single human-readable operations note listing each job’s purpose, owner, and expected output
- periodically prune jobs whose value no longer exceeds their cognitive overhead

### 7. Low-Medium: the repo export is private, but privacy is not a substitute for hygiene

Critique:
- “private repo” is good, not sufficient
- private repos still leak through screenshots, collaborator mistakes, local machine compromise, token misuse, or accidental public forks

Recommendation:
- treat this repo as sensitive operational metadata
- keep the content sanitized even though the remote is private

## What this repo did well

Positive notes from the hostile review:
- config was exported in sanitized form, not raw secret form
- cron snapshot was redacted
- workflow and skills were documented instead of dumping the entire Hermes home
- the export avoided raw session stores and logs
- the setup itself already uses secret redaction, checkpoints, memory, and a task ledger

## Strongest next defenses

1. Add a root personal `AGENTS.md`
2. Create an export-hygiene checklist/skill
3. Enable backup-first skill maintenance
4. Rationalize overlapping skills
5. Verify local auxiliary context and helper-model fit
6. Either fix or intentionally retire stale optional integrations

## Bottom line

The main security risk is not that Hermes is weak. It is that the environment is powerful, stateful, and dense. The more powerful and persistent an agent setup becomes, the more the real failures shift from “can it do the task” to:
- did we separate safe/exportable state from sensitive state
- did we keep instructions coherent
- did we keep background automation understandable
- did we remove half-maintained edges

This setup is good enough to deserve stricter operational hygiene than a casual toy agent install.