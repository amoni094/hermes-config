# linux-vpn-autostart Historical Note

Generated: 2026-06-30

## Status

This key remains intentionally unresolved in the migrated skill-usage data:
- `linux-vpn-autostart`

## Why it was not auto-mapped

Evidence confirms it was a real historical skill/workflow name used in prior sessions, but there is no active non-archive skill file in the current local skill library with that exact name, and there is no sufficiently confident successor mapping to merge automatically without risking false history.

Candidate successors considered but rejected as automatic replacements:
- `devops/wayland-session-management`
  - too broad; session/window/display recovery is not the same thing as VPN autostart
- `autonomous-ai-agents/hermes-runtime-maintenance`
  - also too broad; runtime maintenance is not a VPN/autostart workflow

## Current policy

- Keep `linux-vpn-autostart` out of the automatic replacement map.
- Treat it as a historical-only usage key.
- Preserve it in reports so the history is not lost.
- Do not merge its counts into another active skill unless a future session recovers a real replacement skill or recreates the workflow explicitly.

## Practical effect

After the migration pass:
- stale usage keys were reduced to 1
- the sole remaining key is `linux-vpn-autostart`
- this is expected and intentional, not an unfinished migration error

## Recommendation

If this workflow becomes relevant again, prefer one of two paths:
1. recreate a dedicated VPN/autostart skill with a clear scope, then migrate this historical key into it
2. keep it permanently historical if the workflow is no longer part of the active skill library
