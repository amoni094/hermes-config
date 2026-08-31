### Framework Bugs v4: Root Cause Distribution (arXiv:2602.21806, updated Aug 2026) ★ HIGH <!-- why: sign-off QA checklist was missing the dominant actual bug categories from empirical study of 2,823 agent episodes across 3 frameworks -->

Largest empirical study of agent framework bugs to date (updated Aug 2026). **76% of bugs = Incorrect Functionality** (not crashes). Root cause distribution:

| Root Cause | Share | Sign-off check |
|---|---|---|
| API misuse / contract violation | 31% | Did every tool call use the documented argument schema? Check one call per unique tool used. |
| Config / environment mismatch | 22% | Does the agent's assumed config match the actual runtime config? Spot-check one key assumption. |
| Parsing / serialization error | 18% | Are all structured outputs (JSON, YAML, schemas) validated at the boundary, not assumed well-formed? |
| Execution trace divergence | 14% | Does the agent’s internal plan match the actual sequence of tool calls made? |
| Reasoning / logic error | 9% | Standard sign-off catches this; no new check needed. |
| Other | 6% | — |

**Add to sign-off table — framework-bug row (required for any agentic run using 2+ distinct tools or 2+ sequential tool calls of any type):**

| Check | Status | Evidence |
|---|---|---|
| API contract | PASS / FAIL | List one tool call + args verified against schema |
| Config match | PASS / FAIL | State assumed config value + verification command |
| Serialization boundary | PASS / FAIL | State where structured output was validated |
| Trace fidelity | PASS / FAIL | Planned steps vs. actual tool call sequence |

For simple single-tool tasks: mark all four N/A with a one-line justification.

Reference: arXiv:2602.21806, "A Study of Agent Framework Bugs", v4 Aug 2026.

## Sweep 29 Additions (Aug 2026)

### Governed Pass: Don't Self-Certify (github:Framework-Drift/governed-pass) ★ HIGH
1. Hash-lock the task contract at start — agent cannot change scope mid-run.
2. Agreement ≠ independence: reviewers sharing a spec find the same bugs.
3. Closed disposition vocabulary — decisions must be named (pass/repair/escalate), not free-form.
4. Heterogeneous adversarial review — use different model families (~$6.25 cross-model review, positive ROI).
5. Never self-certify: the agent that performed the task cannot be the final reviewer.

### AgentJudgeBench: Score Traces not just Outcomes (arXiv:2608.26623) ★ MED
