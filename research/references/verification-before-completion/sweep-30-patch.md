## Sweep 30 Additions (Aug 2026)

### TrajectorysentinelL: Deterministic Verification at Completion (arXiv:2608.02464) ★ HIGH <!-- why: LLM judges cost as much as the agent; deterministic recomputation catches 60-96% at 0 FP -->

Framework-bugs paper (2602.21806, 5,669 reports): **76% of agent bugs are Incorrect
Functionality**, dominated by API, configuration, parsing, and serialization failures
— not logic errors. Standard crash-based testing misses all of them.

**Deterministic completion check (zero extra model calls):**
1. Recompute the agent's stated outputs from the tool results it actually received.
   ("The file was written" → read_file the path and confirm non-empty.)
2. Confirm every required tool call category was made — a coverage check.
   ("Plan said search→write→verify": check all three appear in the session tool log.)
3. If claimed result ≠ reconstructed result from tool outputs: FAIL before claiming done.

**Rollback+replay:** when a discrepancy is caught, rollback to the last verified-clean state
and re-run only the failed sub-sequence. Recovery rate: 45% of failures; lifts success 52%→73%
for ~1 extra model call. Do not ask the model to "fix it in place" without rollback.

**API/config/parsing/serialization failures (2602.21806 taxonomy):**
These are the dominant failure classes that crash-based tests miss:
- API sequence errors: tool called in wrong order or with wrong prior state
- Configuration drift: skill/config written but not yet in effect for current session
- Parsing boundary: tool result parsed as one format when it’s actually another
- Serialization: data written correctly but read back as different type/shape

