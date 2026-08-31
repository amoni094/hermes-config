# Sweep Implementation Pitfalls

Collected across sweeps 23–24. Apply to any session that implements sweep findings into scripts.

---

## Verification Script Naming Mismatches

When writing a post-implementation verifier, symbol names in the check often differ from what
was actually written (e.g. `PREFERENCE_VOLATILE_TTL_DAYS` int vs actual `VOLATILE_PREFERENCE_TTL`
timedelta; `nl_policy_gap` function vs actual `NL_POLICY_BYPASS` constant).

**Fix:** Before writing the verifier, run:

    grep -n 'def \|^[A-Z_]* =' <script.py> | head -40

Use actual symbol names from grep output — never from intent or session memory.

---

## Inline Heredoc Verification Scripts

`python3 - << 'EOF'` with lambda helpers fails silently on arity mismatch — no line number,
just `TypeError`. Use named temp files instead:

    python3 /tmp/hermes-verify-<sweep-name>.py   # then delete after

Write the file with `terminal()`, run it, check exit_code, then remove it. Gives full
traceback on failure.

---

## Skill_view Pruning After Context Compression

After any context compaction boundary, skill_view calls for large skills (>50KB) will return
`[SKILL_PRUNED]`. Always reload immediately before the first write in a new context window.
The compaction summary preserves the task list but not skill content.

**Pattern:**
1. Read compaction summary for pending task list
2. Reload pruned skills: `skill_view(name='...')`
3. Verify current script state with grep/read_file before patching
4. Then implement

---

## Memory Replace: Char Budget

`memory(action='replace', ...)` fails when the replacement content + existing memory total
exceeds the char budget (~2200 chars). Pattern: do a batch replace+remove in a single
`operations=[...]` call to free space and add new content atomically. Do not add first
and expect a second pass to trim.

---

## l1-graphiti-write.py Arg Parsing

This script uses ad-hoc `sys.argv` parsing, NOT `argparse`. Adding new flags requires
matching the existing manual parsing loop (scan `args[i]` for `--flag`, set a bool).
Do not introduce `argparse` in a patch — it would break the existing arg contract.

---

## Sweep 24 Specific Notes

- Only ~10 papers exceeded cutoff 2608.23552 (unusually sparse; most 2608.23xxx were non-CS)
- High-value findings came from adjacent IDs (security papers below cutoff, HN threads)
- Reference file written to: `agent-memory-consolidation/references/sweep-24-findings.md`
- All 5 modified scripts pass `py_compile`; 32-point ad-hoc verifier ran clean after naming fix

## First-pass count is not a backlog (Sweep 26)

- A subagent "185 relevant papers" from HTML title-filter is **not** 185 unimplemented findings. Sweep 23 deleg_d802e67e task-0: 347 candidates → 185 noisy titles (wildfire, fashion KG, ICS) → 36 assessed / 16 HIGH. Implement only the downselected HIGH set after abs-page verification.
- Do not treat compaction summaries, crash dumps, or IDs above the live `arxiv.org/list/*/recent` max as papers. Verify every ID at `https://arxiv.org/abs/{id}` before any skill or runtime change. Tombstoned crash-dump IDs (HASTE 2608.20888, RethinkSkill 2608.20777, 2608.23567+) stay untrusted.
- Zero papers above cutoff is a complete result — do not invent titles to fill a quota.
- If parallel research leaves finish in ~1–2s with no finding file, that is not evidence of empty literature. Parent continues the walk (arxiv list/recent, HN newest, GitHub trending). Do not re-dispatch the same leaf route in the same session.
- Benchmark-only SKIP can be wrong when the *method* is harness-usable without the benchmark (CatchBench PRE/LIVE/POST → verification-before-completion, Sweep 27).
- After any promote-gate script change, re-read `config.yaml` `memory.tier_thresholds.promote_thresholds` against code `VC_PROMOTE_THRESH` — config/code drift was real after Sweep 24.
- Bare "Explicitly not built" bullet lists fail user follow-ups. Every defer needs benefit-for-this-stack + partial coverage + cost/risk + revisit trigger (`arxiv-sweep-findings` Maintenance Notes §8; example matrix in `references/sweep-27.md`). High-benefit/high-cost is a valid park; low-fit-for-stack is a permanent SKIP.
- Partial absorption is not full paper implementation: Dual-Track ≠ full MemSIF topical/event; `enabled_toolsets` ≠ ToolGraph reranker; warn/halt ≠ Graphiti hard eviction. Name the residual explicitly so the next sweep does not re-litigate or double-build.

## Sweep 28

### web.search_backend must match plugin id
After web provider plugins, the registry name is `brave-free`, not `brave`.
Config `search_backend: brave` raises provider NotFoundError even when BRAVE_SEARCH_API_KEY is valid.
Smoke: resolve registry providers before claiming web is live.

### PyYAML full dump strips comments
Prefer surgical line edits or ruamel when touching config.yaml mid-sweep.
If full dump is used, diff key-set against a state-snapshot (not file size alone).

### Constraint objects vs prose
Do not store the same must-constraint as both binding-typed YAML and free-text current_state
(AgentPrune / SkillZip). Lint handoffs with constraint-binding-lint.py.

### Working memory is not Hindsight
WM (`cache/working-memory/`) is session task state. Do not promote WM progress lines into durable
memory without the normal Dual-Track / promote gates.

## Sweep 30

### Crossref without domain filter = medical/physics noise flood
Adding Crossref as a source without a computer-science field filter inflated raw paper count
from ~80 to 420 per sweep, with majority being biomedical and physics papers.
Filter required: add `field_of_study=computer-science` parameter to every Crossref query.
Alternatively: tighten query to include `AND (agent OR LLM OR "language model")`.
Smoke test after adding a new source: raw count without cs filter should be <150 per sweep.

### Multi-source sweeps can surface below-cutoff papers
When new sources (HF Papers, PWC, Crossref, OpenAlex multilingual) are added, they may surface
papers with arXiv IDs below the current cutoff. This is not a regression — the cutoff only
applies to arXiv listing walks, not cross-source retrieval. Record the cutoff as unchanged,
not as the lowest new ID found. The sweep-30 entry in the sweep index correctly shows the
new cutoff as equal to the old one.

