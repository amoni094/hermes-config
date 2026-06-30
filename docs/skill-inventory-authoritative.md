# Authoritative Skill Inventory

Generated from live local skill files, `hermes skills list --source builtin/local`, and `.usage.json` reconciliation.

## Summary

- total_records: 177
- active_records: 167
- archived_records: 10
- builtin_records: 60
- local_records: 107
- enabled_records: 72
- disabled_records: 86
- stale_usage_count: 28
- builtin_cli_summary: 0 hub-installed, 64 builtin, 0 local — 7 enabled, 57 disabled
- local_cli_summary: 0 hub-installed, 0 builtin, 98 local — 65 enabled, 33 disabled

## Active categories

- (root): 4
- apple: 5
- autonomous-ai-agents: 45
- creative: 16
- data-science: 1
- devops: 10
- email: 1
- github: 5
- media: 4
- mlops: 8
- note-taking: 1
- productivity: 10
- red-teaming: 1
- research: 14
- smart-home: 1
- social-media: 1
- software-development: 29
- superpowers: 11

## Highest-use active skills (top 20 by use_count)

- autonomous-ai-agents/hermes-obsidian-sync | source=local | status=enabled | use_count=251 | size_bytes=15516
- software-development/verification-before-completion | source=local | status=enabled | use_count=250 | size_bytes=20668
- autonomous-ai-agents/hermes-agent | source=builtin | status=enabled | use_count=196 | size_bytes=49826
- software-development/workflow-map | source=local | status=enabled | use_count=48 | size_bytes=4198
- software-development/systematic-debugging | source=builtin | status=enabled | use_count=44 | size_bytes=16728
- software-development/local-personal-dashboard | source=local | status=enabled | use_count=43 | size_bytes=34962
- software-development/complexity-gated-planning | source=local | status=enabled | use_count=42 | size_bytes=2948
- research/recent-news-briefing | source=local | status=enabled | use_count=39 | size_bytes=9764
- software-development/subagent-driven-development | source=local | status=enabled | use_count=29 | size_bytes=6675
- software-development/requesting-code-review | source=builtin | status=enabled | use_count=27 | size_bytes=13253
- autonomous-ai-agents/ouroboros-plugin-development | source=local | status=enabled | use_count=25 | size_bytes=20798
- github/github-operations | source=local | status=enabled | use_count=24 | size_bytes=10857
- autonomous-ai-agents/hermes-performance-tuning | source=local | status=enabled | use_count=21 | size_bytes=20242
- github/scoped-pr-fix-and-verification | source=local | status=enabled | use_count=19 | size_bytes=7907
- autonomous-ai-agents/hermes-memory-surface-selection | source=local | status=enabled | use_count=19 | size_bytes=11960
- research/research-briefing | source=local | status=enabled | use_count=18 | size_bytes=10288
- devops/fedora-atomic-dotfiles-adaptation | source=local | status=enabled | use_count=18 | size_bytes=8850
- devops/atomic-desktop-app-installation | source=local | status=enabled | use_count=17 | size_bytes=8937
- superpowers/writing-skills | source=local | status=enabled | use_count=15 | size_bytes=5054
- software-development/isolated-workspace-preflight | source=local | status=enabled | use_count=15 | size_bytes=4460

## Oversized active skills (>= 20000 bytes)

- research/research-paper-writing | source=builtin | status=disabled | size_bytes=104468 | use_count=0
- autonomous-ai-agents/hermes-agent | source=builtin | status=enabled | size_bytes=49826 | use_count=196
- software-development/local-personal-dashboard | source=local | status=enabled | size_bytes=34962 | use_count=43
- autonomous-ai-agents/claude-code | source=builtin | status=disabled | size_bytes=34288 | use_count=0
- creative/humanizer | source=builtin | status=disabled | size_bytes=30025 | use_count=0
- autonomous-ai-agents/ouroboros/seed | source=local | status=enabled | size_bytes=29897 | use_count=1
- creative/p5js | source=builtin | status=disabled | size_bytes=27494 | use_count=0
- creative/comfyui | source=builtin | status=disabled | size_bytes=24287 | use_count=0
- autonomous-ai-agents/ouroboros-plugin-development | source=local | status=enabled | size_bytes=20798 | use_count=25
- software-development/verification-before-completion | source=local | status=enabled | size_bytes=20668 | use_count=250
- autonomous-ai-agents/hermes-performance-tuning | source=local | status=enabled | size_bytes=20242 | use_count=21
- research/llm-wiki | source=builtin | status=disabled | size_bytes=20129 | use_count=0
- red-teaming/godmode | source=local | status=disabled | size_bytes=20044 | use_count=0

## Stale usage keys

- audiocraft-audio-generation | status=alias | replacement=audiocraft | use_count=0
- cli-anything-hermes | status=unknown_or_historical | replacement=None | use_count=2
- devops/atomic-desktop-app-installation | status=unknown_or_historical | replacement=None | use_count=1
- evaluating-llms-harness | status=alias | replacement=lm-evaluation-harness | use_count=0
- fedora-atomic-system-maintenance | status=replacement | replacement=hermes-runtime-maintenance | use_count=4
- fedora-atomic-system-updates | status=replacement | replacement=hermes-runtime-maintenance | use_count=11
- github-auth | status=replacement | replacement=github-operations | use_count=1
- github-code-review | status=replacement | replacement=github-operations | use_count=12
- github-pr-followup-automation | status=replacement | replacement=github-operations | use_count=4
- github-pr-workflow | status=replacement | replacement=github-operations | use_count=8
- github-repo-management | status=replacement | replacement=github-operations | use_count=9
- github:github-pr-followup-automation | status=replacement | replacement=github-operations | use_count=1
- hermes-live-research-setup | status=replacement | replacement=hermes-web-provider-configuration | use_count=9
- hermes-security-preflight | status=replacement | replacement=security-hardening-balance-review | use_count=29
- hermes-stack-maintenance | status=replacement | replacement=hermes-runtime-maintenance | use_count=18
- last30days | status=alias | replacement=last30days-customization | use_count=17
- linux-vpn-autostart | status=unknown_or_historical | replacement=None | use_count=5
- low-friction-repo-hardening | status=replacement | replacement=security-hardening-balance-review | use_count=4
- segment-anything-model | status=alias | replacement=segment-anything | use_count=0
- serving-llms-vllm | status=alias | replacement=vllm | use_count=0
- setup | status=unknown_or_historical | replacement=None | use_count=1
- signal-oriented-research-briefing | status=replacement | replacement=research-briefing | use_count=18
- silverblue-desktop-ricing-adaptation | status=replacement | replacement=fedora-atomic-dotfiles-adaptation | use_count=89
- silverblue-update-automation | status=replacement | replacement=atomic-desktop-app-installation | use_count=22
- software-supply-chain-scanning | status=replacement | replacement=security-hardening-balance-review | use_count=5
- wallust-desktop-theme-integration | status=replacement | replacement=fedora-atomic-dotfiles-adaptation | use_count=7
- waybar-popup-menu-debugging | status=replacement | replacement=wayland-session-management | use_count=8
- wayland-session-troubleshooting | status=replacement | replacement=wayland-session-management | use_count=44
