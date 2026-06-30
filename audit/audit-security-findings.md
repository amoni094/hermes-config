# Hermes Veto Security Audit — Findings

Date: 2026-06-30
Scope: ~/.hermes/veto/rules/ and ~/.hermes/agent-hooks/ (veto-pre-tool.py, track-budget.py)

## 1. Hard-block coverage extended (hermes-hard-blocks.yaml)

Added five new critical hard-block rules for destructive commands previously
uncovered:

| Rule ID                       | Covers                                                        |
|-------------------------------|--------------------------------------------------------------|
| `block-find-delete`           | `find ... -delete`                                           |
| `block-truncate-zero`         | `truncate -s0`, `truncate --size=0`                         |
| `block-python-fs-delete-home` | `python[3] -c` with os.remove/unlink/rmdir/removedirs or shutil.rmtree targeting `$HOME`, `~/.hermes`, `/var/home/rainbow`, or `os.environ['HOME']` |
| `block-chmod-recursive-home`  | `chmod -R` / `--recursive` on `$HOME`, `~`, `~/.hermes`     |
| `block-dd-zero-to-file`       | `dd if=/dev/zero` or `if=/dev/null` writing to a file (`of=` not a device). Device targets already covered by pre-existing `block-disk-format`. |

## 2. veto-pre-tool.py — fail-closed posture

FINDING: The hook previously FAILED OPEN on payload parse error — a malformed or
empty stdin payload caused it to emit `{}` (allow). Rule loading/evaluation
errors were also unguarded.

REMEDIATION (applied): Added `_fail_closed()` helper. The hook now blocks when:
  - stdin payload cannot be parsed as JSON,
  - payload is not a JSON object,
  - rule loading or evaluation raises any exception.
Note: non-zero exit was already treated as block by the protocol, so an
uncaught crash was already safe; the gap was the explicit `{}` on parse error.
SKIP_TOOLS read-only tools still pass through (intended; no governance needed).

## 3. track-budget.py — destructive_calls is post-hoc only

FINDING: `track-budget.py` is a POST_tool_call hook. It increments
`destructive_calls` AFTER the tool has already executed and only blocks the
*next* action once a hard limit is breached. There is NO pre-tool gate tied to
`destructive_calls`; the call that crosses the limit still runs.

STATUS: Documented (not auto-fixed, as converting it to a pre-tool enforcer is
a behavioral change beyond audit scope). An AUDIT NOTE comment was added to the
top of track-budget.py.

RECOMMENDATION: To enforce destructive_calls pre-execution, mirror the counter
check into a pre_tool_call hook that blocks when projected count (current + 1)
would meet/exceed the limit. Pre-execution blocking of individual destructive
*commands* is already handled by veto-pre-tool.py pattern hard-blocks.

## Remaining gaps / notes
- Pattern-based blocks can be evaded by obfuscation (env-var indirection,
  base64-piped commands, alternate binaries). veto-pre-tool.py matches
  case-insensitively, which helps, but determined evasion is possible.
- `block-python-fs-delete-home` only covers inline `-c`; script files invoking
  the same calls are not inspected.
- track-budget.py `DESTRUCTIVE_PATTERNS` substring list (e.g. "rm ") may both
  over- and under-count vs. the veto regex rules; the two systems are not
  reconciled.

## Backups
All edited files backed up as `<file>.bak.audit-20260630-201705`.
