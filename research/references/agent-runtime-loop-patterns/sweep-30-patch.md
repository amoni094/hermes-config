### TrajectorysentinelL: Lightweight Failure Detection Without LLM Judges (arXiv:2608.02464, Aug 2026) ★ HIGH

On 2,823 agent episodes across 3 frameworks and 4 models: a **one-class echo-state-network
+ CUSUM alarm** detects 71% of failures at 5% false-alarm budget (AUROC 0.872). The detector
triggers at 200 microseconds per step — three orders of magnitude below a judge call.
Detection advantage is monotone with post-onset horizon: +0.09 at ≤3 steps, +0.40 at ≥9.

**More powerful: deterministic verification layer** (zero retraining, transfers unchanged):
- Recompute the agent's stated totals from the tool results it actually received
- Confirm every required tool call was made (coverage check)
- Head-to-head: catches 60% of failures at 0 of 63 false positives (vs monitor: 54% at 17% FP)
- Combined with coverage check: 96% catch rate
- Transfers unchanged to llama3.1:8b (110/110 at 0/10 FP); 0 false positives on 1,825 healthy episodes

**Rollback + replay recovery:**
- Flagged runs rolled back and re-run live: recovers 45% of failures vs 16% resampling control (p=0.0005)
- Lifts task success from 52% → 73% for ~1 extra model call per run
- Code + traces: github.com/sunnydubey1111/agent-trajectory-sentinel

**Hermes pattern:**
1. **Deterministic verification** (add to `verification-before-completion` workflow): after any multi-tool run, recompute claimed outputs from tool results received. If claimed sum ≠ sum of tool outputs: flag.
2. **Coverage check**: confirm every required tool call category was made (e.g. if plan says "search then write", verify both happened).
3. **Rollback+replay**: when LivePlan watchdog fires AND deterministic verification catches a failure, don't just steer — rollback to last verified state and re-run the failed sub-sequence (one extra model call; 45% recovery rate).
4. **No LLM for monitoring**: the SQL watchdog (section 5) IS the cheap monitor. Add a coverage-check column to the session table.

---

## 5b. Circuit Breaker Ladder: Steer → Constrain → Stop

Pattern distilled from: munder-difflin (chaitanyagiri/munder-difflin, MIT, ~1.7k stars).
Complements the LivePlan SQL watchdog (section 5) with an explicit 3-rung escalation
that applies when an agent is looping, storming errors, or blowing its budget.

### The Three Rungs

**Rung 1 — Steer:** inject a corrective prompt into the agent's next turn.
- Trigger: same tool failed 3 times OR result_hash unchanged for 2 consecutive turns.
- Action: append to next tool result: "You've tried X N times without progress. What
  alternative approach should you take? List it before continuing."
- Cost: zero additional model calls; steers rather than interrupts.

