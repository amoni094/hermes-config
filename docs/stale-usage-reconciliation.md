# Stale Usage Metadata Reconciliation

Generated: 2026-06-30

## Purpose

Identify entries in `~/.hermes/skills/.usage.json` that no longer correspond to an active non-archive `SKILL.md` path, so curation/routing work is not biased by stale names.

## Verification method

Compared:
- usage keys from `~/.hermes/skills/.usage.json`
- active non-archive skill directory names discovered from `~/.hermes/skills/**/SKILL.md`

Verified by:
- local Python scan over `.usage.json` and active non-archive `SKILL.md` paths

## Result

- Usage entries with no active non-archive matching skill directory name: 28

These fall into three buckets.

## A. Alias / renamed bundled-skill mismatches

These likely still represent live skills, but the usage key name no longer matches the active skill directory/frontmatter naming convention:

- `audiocraft-audio-generation` -> likely `mlops/models/audiocraft`
- `evaluating-llms-harness` -> likely `mlops/evaluation/lm-evaluation-harness`
- `segment-anything-model` -> likely `mlops/models/segment-anything`
- `serving-llms-vllm` -> likely `mlops/inference/vllm`
- `last30days` -> likely `research/last30days-customization`

Action:
- normalize these to the active skill name/path in the future authoritative inventory report
- migrate historical usage if you want accurate per-skill rankings

## B. Archived / superseded skills still present in usage metadata

These appear to be historical names that are likely archived or replaced by active umbrella/successor skills:

- `github-auth`
- `github-code-review`
- `github-pr-followup-automation`
- `github-pr-workflow`
- `github-repo-management`
- `github:github-pr-followup-automation`
- `signal-oriented-research-briefing`
- `wallust-desktop-theme-integration`
- `waybar-popup-menu-debugging`
- `wayland-session-troubleshooting`

Likely successors:
- GitHub historical leaves -> `github-operations`, `scoped-pr-fix-and-verification`
- `signal-oriented-research-briefing` -> `research-briefing` and `recent-news-briefing`
- `wayland-session-troubleshooting` -> `wayland-session-management`

Action:
- mark as historical in inventory reporting
- avoid using raw usage counts from these names to rank current active skills

## C. Local/legacy names with no current active skill match

These need a human mapping decision or retirement note:

- `cli-anything-hermes`
- `devops/atomic-desktop-app-installation`
- `fedora-atomic-system-maintenance`
- `fedora-atomic-system-updates`
- `hermes-live-research-setup`
- `hermes-security-preflight`
- `hermes-stack-maintenance`
- `linux-vpn-autostart`
- `low-friction-repo-hardening`
- `setup`
- `silverblue-desktop-ricing-adaptation`
- `silverblue-update-automation`
- `software-supply-chain-scanning`

Important note:
Several of these have substantial usage counts, so they are not noise; they are evidence of renamed, absorbed, or removed workflows.

High-signal examples:
- `silverblue-desktop-ricing-adaptation` -> use_count 89
- `wayland-session-troubleshooting` -> use_count 44
- `hermes-security-preflight` -> use_count 29
- `silverblue-update-automation` -> use_count 22
- `signal-oriented-research-briefing` -> use_count 18
- `hermes-stack-maintenance` -> use_count 18

## Recommended next step

When you build the authoritative inventory report, add these fields:
- `usage_key`
- `active_skill_path`
- `resolved_status`: active | alias | archived | unknown
- `replacement_skill`

That will let you:
- preserve historical usage value
- stop stale names from polluting live routing decisions
- identify which old workflows were merged into which new umbrellas

## Bottom line

The stale-usage problem is real, not hypothetical.

You should not use raw `.usage.json` keys as if they directly described the live skill set. A meaningful portion of historical usage belongs to:
- renamed bundled skills
- archived skills
- replaced local workflows
- absorbed umbrella migrations
