# Authoritative Skill Inventory

Generated from live local skill files, `hermes skills list --source builtin/local`, and `.usage.json` reconciliation.

## Summary

- total_records: 164
- active_records: 142
- archived_records: 22
- builtin_records: 24
- local_records: 118
- enabled_records: 101
- disabled_records: 41
- stale_usage_count: 29
- builtin_cli_summary: 0 hub-installed, 24 builtin, 0 local — 14 enabled, 10 disabled
- local_cli_summary: 0 hub-installed, 0 builtin, 118 local — 87 enabled, 31 disabled

## Active categories

- (root): 3
- autonomous-ai-agents: 54
- creative: 1
- devops: 10
- github: 5
- media: 1
- mlops: 1
- note-taking: 2
- productivity: 9
- research: 9
- security: 3
- software-development: 36
- superpowers: 8

## Highest-use active skills (top 20 by use_count)

- autonomous-ai-agents/hermes-obsidian-sync | source=local | status=enabled | use_count=363 | size_bytes=25492
- software-development/verification-before-completion | source=local | status=enabled | use_count=260 | size_bytes=24213
- autonomous-ai-agents/hermes-agent | source=builtin | status=enabled | use_count=221 | size_bytes=51955
- devops/fedora-atomic-dotfiles-adaptation | source=local | status=enabled | use_count=115 | size_bytes=9253
- github/github-operations | source=local | status=enabled | use_count=68 | size_bytes=13322
- devops/wayland-session-management | source=local | status=enabled | use_count=59 | size_bytes=5158
- autonomous-ai-agents/hermes-memory-surface-selection | source=local | status=enabled | use_count=54 | size_bytes=23836
- software-development/workflow-map | source=local | status=enabled | use_count=52 | size_bytes=5437
- software-development/claude-routing-hierarchy | source=local | status=enabled | use_count=48 | size_bytes=13844
- software-development/complexity-gated-planning | source=local | status=enabled | use_count=47 | size_bytes=7766
- software-development/adversarial-review | source=local | status=enabled | use_count=47 | size_bytes=17284
- software-development/systematic-debugging | source=builtin | status=enabled | use_count=46 | size_bytes=17098
- software-development/local-personal-dashboard | source=local | status=enabled | use_count=45 | size_bytes=35300
- devops/atomic-desktop-app-installation | source=local | status=enabled | use_count=44 | size_bytes=10646
- software-development/subagent-driven-development | source=local | status=enabled | use_count=40 | size_bytes=12022
- software-development/security-hardening-balance-review | source=local | status=enabled | use_count=40 | size_bytes=5445
- autonomous-ai-agents/hermes-context-hygiene | source=local | status=enabled | use_count=33 | size_bytes=15771
- software-development/requesting-code-review | source=builtin | status=enabled | use_count=31 | size_bytes=14756
- autonomous-ai-agents/agent-memory-consolidation | source=local | status=enabled | use_count=29 | size_bytes=35103
- autonomous-ai-agents/hermes-session-hygiene | source=local | status=enabled | use_count=27 | size_bytes=13847

## Oversized active skills (>= 20000 bytes)

- autonomous-ai-agents/hermes-agent | source=builtin | status=enabled | size_bytes=51955 | use_count=221
- software-development/local-personal-dashboard | source=local | status=enabled | size_bytes=35300 | use_count=45
- autonomous-ai-agents/agent-memory-consolidation | source=local | status=enabled | size_bytes=35103 | use_count=29
- autonomous-ai-agents/claude-code | source=builtin | status=enabled | size_bytes=34636 | use_count=7
- software-development/document-layout-design | source=local | status=enabled | size_bytes=31885 | use_count=20
- creative/humanizer | source=builtin | status=disabled | size_bytes=30025 | use_count=1
- autonomous-ai-agents/ouroboros/seed | source=local | status=disabled | size_bytes=29897 | use_count=1
- autonomous-ai-agents/hermes-obsidian-sync | source=local | status=enabled | size_bytes=25492 | use_count=363
- software-development/verification-before-completion | source=local | status=enabled | size_bytes=24213 | use_count=260
- productivity/rich-pdf-generation | source=local | status=disabled | size_bytes=24211 | use_count=2
- autonomous-ai-agents/hermes-memory-surface-selection | source=local | status=enabled | size_bytes=23836 | use_count=54
- autonomous-ai-agents/harness-first-agent-design | source=local | status=enabled | size_bytes=22841 | use_count=6
- autonomous-ai-agents/ouroboros-plugin-development | source=local | status=enabled | size_bytes=21140 | use_count=25

## Stale usage keys

- apple-notes | status=unknown_or_historical | replacement=None | use_count=0
- apple-reminders | status=unknown_or_historical | replacement=None | use_count=0
- codebase-inspection | status=unknown_or_historical | replacement=None | use_count=9
- config-audit-and-hardening | status=unknown_or_historical | replacement=None | use_count=2
- findmy | status=unknown_or_historical | replacement=None | use_count=0
- free-llm-provider-integration | status=unknown_or_historical | replacement=None | use_count=12
- hermes-budget-governance | status=unknown_or_historical | replacement=None | use_count=2
- hermes-mcp-integration | status=unknown_or_historical | replacement=None | use_count=26
- hermes-memory-drift-audit | status=unknown_or_historical | replacement=None | use_count=18
- hermes-performance-tuning | status=unknown_or_historical | replacement=None | use_count=48
- hermes-runtime-maintenance | status=unknown_or_historical | replacement=None | use_count=63
- hermes-to-gui-agent-port | status=unknown_or_historical | replacement=None | use_count=7
- home-router-firewall-review | status=unknown_or_historical | replacement=None | use_count=2
- imessage | status=unknown_or_historical | replacement=None | use_count=0
- last30days-customization | status=unknown_or_historical | replacement=None | use_count=28
- linux-vpn-autostart | status=unknown_or_historical | replacement=None | use_count=5
- macos-computer-use | status=unknown_or_historical | replacement=None | use_count=0
- medical-research-analysis | status=unknown_or_historical | replacement=None | use_count=2
- portable-scripts-and-exports | status=unknown_or_historical | replacement=None | use_count=1
- porting-superpowers-to-hermes | status=unknown_or_historical | replacement=None | use_count=2
- recent-news-briefing | status=unknown_or_historical | replacement=None | use_count=54
- research-briefing | status=unknown_or_historical | replacement=None | use_count=37
- security-hardening-code-review | status=unknown_or_historical | replacement=None | use_count=6
- silverblue-system-update | status=unknown_or_historical | replacement=None | use_count=4
- skills-library-hygiene | status=unknown_or_historical | replacement=None | use_count=2
- superpowers-bootstrap | status=unknown_or_historical | replacement=None | use_count=1
- thunderbird-local-email-workflow | status=unknown_or_historical | replacement=None | use_count=1
- xurl | status=unknown_or_historical | replacement=None | use_count=0
- yuanbao | status=unknown_or_historical | replacement=None | use_count=0
