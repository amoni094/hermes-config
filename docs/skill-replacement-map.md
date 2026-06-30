# Skill Replacement Map

Generated: 2026-06-30

This is the proposed replacement map for stale or historical usage keys that no longer map cleanly to an active non-archive skill directory name.

## Alias / renamed bundled skills

| Historical key | Replacement skill |
|---|---|
| audiocraft-audio-generation | mlops/models/audiocraft |
| evaluating-llms-harness | mlops/evaluation/lm-evaluation-harness |
| segment-anything-model | mlops/models/segment-anything |
| serving-llms-vllm | mlops/inference/vllm |
| last30days | research/last30days-customization |

## Archived / superseded historical skills

| Historical key | Proposed replacement |
|---|---|
| github-auth | github/github-operations |
| github-code-review | github/github-operations |
| github-pr-followup-automation | github/github-operations |
| github:github-pr-followup-automation | github/github-operations |
| github-pr-workflow | github/github-operations |
| github-repo-management | github/github-operations |
| signal-oriented-research-briefing | research/research-briefing |
| wallust-desktop-theme-integration | devops/fedora-atomic-dotfiles-adaptation |
| waybar-popup-menu-debugging | devops/wayland-session-management |
| wayland-session-troubleshooting | devops/wayland-session-management |

## Local legacy workflows needing policy mapping

| Historical key | Proposed replacement | Confidence |
|---|---|---|
| hermes-security-preflight | software-development/security-hardening-balance-review | medium |
| hermes-stack-maintenance | autonomous-ai-agents/hermes-runtime-maintenance | medium |
| hermes-live-research-setup | autonomous-ai-agents/hermes-web-provider-configuration | low-medium |
| silverblue-desktop-ricing-adaptation | devops/fedora-atomic-dotfiles-adaptation | high |
| silverblue-update-automation | devops/atomic-desktop-app-installation | low |
| fedora-atomic-system-maintenance | autonomous-ai-agents/hermes-runtime-maintenance | low-medium |
| fedora-atomic-system-updates | autonomous-ai-agents/hermes-runtime-maintenance | low-medium |
| linux-vpn-autostart | devops/wayland-session-management | low |
| low-friction-repo-hardening | software-development/security-hardening-balance-review | medium |
| software-supply-chain-scanning | software-development/security-hardening-balance-review | medium |
| setup | autonomous-ai-agents/ouroboros-setup-and-health-check | low |
| cli-anything-hermes | autonomous-ai-agents/hermes-agent | low |
| devops/atomic-desktop-app-installation | devops/atomic-desktop-app-installation | path-format mismatch |

## Migration policy

Use this order when reconciling usage metadata:
1. exact active skill name
2. alias map for renamed bundled skills
3. explicit replacement map for archived/superseded skills
4. mark unresolved items as historical-only if no confident replacement exists

## Recommendation

Do not mutate `.usage.json` blindly in the first pass.
Instead:
- keep the raw historical file intact
- make the generator emit `replacement_skill` / `resolved_status`
- only later, if desired, build a one-shot migration script that writes a normalized derived usage report or updates the raw file with a backup
