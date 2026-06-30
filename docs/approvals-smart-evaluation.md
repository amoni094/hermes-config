# approvals.mode smart evaluation

Generated: 2026-06-30

## Purpose

Evaluate `approvals.mode: smart` in a controlled, non-permanent way without changing the user's standing approval posture.

## Live check performed

I verified that the config can be toggled to `smart` and cleanly restored to `manual`.

Command used:

```bash
set -e
orig=$(python3 - <<'PY'
import yaml, pathlib
obj=yaml.safe_load(pathlib.Path('/var/home/rainbow/.hermes/config.yaml').read_text())
print(obj.get('approvals',{}).get('mode',''))
PY
)
printf 'original=%s\n' "$orig"
hermes config set approvals.mode smart >/dev/null
mid=$(python3 - <<'PY'
import yaml, pathlib
obj=yaml.safe_load(pathlib.Path('/var/home/rainbow/.hermes/config.yaml').read_text())
print(obj.get('approvals',{}).get('mode',''))
PY
)
printf 'after_set=%s\n' "$mid"
hermes config set approvals.mode "$orig" >/dev/null
final=$(python3 - <<'PY'
import yaml, pathlib
obj=yaml.safe_load(pathlib.Path('/var/home/rainbow/.hermes/config.yaml').read_text())
print(obj.get('approvals',{}).get('mode',''))
PY
)
printf 'restored=%s\n' "$final"
```

Observed result:
- `original=manual`
- `after_set=smart`
- `restored=manual`

## Conclusion

`smart` is mechanically available and the setting round-trips cleanly.

## Recommendation

Keep the standing mode at `manual` for now unless you explicitly want higher day-to-day throughput with more heuristic approval behavior.

Reasoning:
- the current optimization pass already improved correctness and operational hygiene without needing a trust-policy change
- `manual` remains the more conservative default for a powerful local agent environment
- if you later want to trial `smart`, it should be a deliberate workflow decision rather than an adversarial-cleanup side effect

## Current state after evaluation

The live config was restored to:
- `approvals.mode: manual`
