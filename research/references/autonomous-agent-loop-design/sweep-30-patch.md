### Prime Agent: Harness Separation + Continual Harness (arXiv:2608.23552) ★ HIGH <!-- why: validates harness-first-agent-design with empirical trajectory data; adds persistent-REPL and recursive-subagent patterns absent from this skill -->

Prime Agent separates the **execution harness** from **strategy** into distinct runtime layers that do not share code paths. Key findings applicable to Hermes autonomous loops:

**Four harness responsibilities (never mix with strategy code):**
1. **Execution** — shell/tool dispatch, timeout, retry with exponential backoff
2. **Recovery** — detect stuck/failed states; rollback to last checkpoint; re-enter loop at safe point
3. **Verification** — compare pre/post state hashes; check required tool calls were made; confirm outputs non-empty
4. **Resource accounting** — token budget tracking per iteration; cost accumulation; hard stop at budget

**Continual Harness pattern:** maintain a persistent REPL across trajectory boundaries so the agent does not lose working state between sessions. This is distinct from memory — it is an active execution environment that survives checkpointing.

**Recursive subagent comms:** subagents communicate directly with their parent (not only via shared memory). The parent harness receives typed JSON from subagents and validates schema before consuming — prevents cascade failures from silent type errors.

**Hermes implementation:**
- `delegate_task` is already the recursive-subagent dispatch mechanism — ensure every subagent output_schema is specified and validated before acting on results
- Persistent REPL ≈ background terminal session with `background=True`; keep session_id across calls
- Recovery entry point: when a loop iteration fails, rollback to last verified checkpoint (last confirmed tool output) and re-enter, not restart
- Resource accounting: track cumulative API calls per loop; add hard-stop guard at N iterations or M tokens

Reference: arXiv:2608.23552, "Prime Agent: Persistent Harness for Recursive Multi-Agent Execution", Aug 2026.

## Sweep 29 Additions (Aug 2026)

### SKILL.state for Long-Horizon Loops (arXiv:2608.26263) ★ HIGH

For loops exceeding ~10 steps, switch from append-only conversation history to SKILL.state:
- At each step: model receives only (1) immutable skill spec, (2) current structured state,
  (3) latest observation (ring-buffered to last 3)
- Intermediate reasoning is discarded after commit — prevents prompt bloat
- Token savings accumulate linearly; accuracy improves on long-horizon tasks

Usage: `python3 ~/.hermes/scripts/skill-state.py init --session $SID --skill SKILL_NAME`
Then at each loop step: `skill-state.py step --session $SID --skill SKILL_NAME --observation "..."`
See config: `memory.skill_state.activate_threshold_steps: 10`
