# Operations Surface Register

Generated: 2026-06-30

This note exists to reduce background-complexity debt. It records the live cron/watchdog estate and the current posture of optional integrations that showed up in the latest adversarial pass.

## Cron and watchdog jobs

Verified with:
- `hermes cron list --all`
- repo snapshot `cron.snapshot.json`

| Job | Schedule | Deliver | Mode | Purpose | Current status |
|---|---|---:|---|---|---|
| `hourly-hermes-chat-sync` | every 60m | `local` | agent | sync recent Hermes activity into the Obsidian vault | active / last run ok |
| `hermes-mutation-gate-watch` | every 1440m | `local` | script | check mutation-gate state | active / last run ok |
| `hermes-memory-drift-audit` | every 1440m | `local` | script | audit durable memory drift | active / last run ok |
| `skillspector-guard` | every 240m | `origin` | script | enforce skill guard checks | active / last run ok |
| `firecrawl-watchdog` | every 10m | `origin` | script | keep Firecrawl healthy | active / last run ok |
| `hermes-platform-watchdog` | every 720m | `local` | script | broad Hermes platform health check | active / last run ok |

## Delivery semantics note

Important CLI-specific reminder:
- `deliver: local` means the job output is stored locally; it does not message this terminal session.
- `deliver: origin` is meaningful for jobs created from gateway-connected chats, but should not be assumed to notify this CLI session.

This matters because an adversarial review should treat silent-or-misread delivery assumptions as operational risk.

## Optional integration posture

Verified with:
- `hermes doctor`
- `hermes config check`

### Healthy / intentionally in use
- Telegram gateway variables are present.
- Firecrawl local endpoint is configured.
- SearXNG URL is configured.
- OpenAI Codex auth is logged in.

### Present but needs explicit ownership
- WhatsApp bridge is enabled in env/config surface and `hermes doctor` reports:
  - `1 critical`
  - `2 high`
  - `2 moderate`
  npm vulnerabilities in the bridge dependencies

## Required posture decisions

### 1. WhatsApp bridge
Current state is intentionally disconnected/dormant.

User decision captured for this pass:
- keep WhatsApp disconnected
- do not remediate or reconnect it as part of this optimization wave

Operational rule:
- treat the bridge as intentionally out of scope until the user explicitly asks to re-enable it
- keep documentation honest that `hermes doctor` may still report dependency vulnerabilities while the bridge remains dormant

This removes the ambiguity without changing the runtime bridge state.

### 2. Cron estate
Current cron count is still small enough to reason about, but large enough to justify a standing register like this one.

Recommended maintenance rule:
- every new job should have an obvious owner, purpose, delivery mode, and expected success signal
- prune jobs whose value no longer exceeds their debugging cost

## Implemented this pass
- Added this register to the repo.
- Expanded the root `/var/home/rainbow/AGENTS.md` with cron/watchdog and export-hygiene rules so the policy also exists outside this repo snapshot.
