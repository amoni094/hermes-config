# Skill Cleanup Decision Matrix

Generated: 2026-06-30

Legend:
- keep = remain as-is or near-as-is
- patch = update routing/description/body/references
- merge = absorb into umbrella or sibling
- disable = keep installed but not active by default
- archive = retire after reference check

| Skill | Current role | Decision | Priority | Reason |
|---|---|---:|---:|---|
| workflow-map | dev workflow router | keep | P0 | Best existing canonical router for development workflow selection |
| complexity-gated-planning | planning leaf | keep | P0 | Clear narrow leaf with strong trigger |
| isolated-workspace-preflight | isolation leaf | keep | P0 | Distinct and useful |
| test-driven-development | implementation discipline | keep | P0 | Core leaf |
| risk-based-review | review-depth selector | keep | P0 | Core leaf |
| requesting-code-review | review pipeline | keep | P0 | Core leaf |
| verification-before-completion | final proof gate | patch | P0 | High-value but oversized; should stay canonical with more references |
| subagent-driven-development | delegation leaf | keep | P0 | Clear specialization |
| hermes-workflow-optimization | Hermes meta workflow | patch | P1 | Useful but overlaps router/operating-pattern; remove stale refs and narrow trigger |
| hermes-operating-pattern | broad Hermes umbrella | patch | P1 | Keep as umbrella/map only; trim stale sibling references |
| hermes-context-budgeting | context cap/compression tuning | patch | P1 | Useful but should explicitly route back to context-hygiene for general session hygiene |
| hermes-context-hygiene | session hygiene router | keep | P1 | Strong trigger and clear boundary |
| hermes-memory-surface-selection | memory/retrieval router | keep | P1 | Strong router; high-value for memory discipline |
| hermes-performance-tuning | runtime performance tuning | patch | P1 | valuable but likely oversized and overlapping with workflow optimization |
| hermes-memory-drift-audit | memory audit specialist | keep | P1 | narrow and useful |
| hermes-session-hygiene | dormant runtime hygiene leaf | patch | P2 | likely useful, but needs explicit trigger and relation to context-hygiene |
| agent-runtime-stack-debugging | runtime debugging leaf | keep | P2 | zero-use but valuable specialist |
| github-operations | GitHub umbrella | keep | P0 | best umbrella already present |
| scoped-pr-fix-and-verification | PR repair specialist | keep | P0 | strong narrow use case |
| split-ci-workflow-change-and-draft-pr | CI/PR specialist | merge | P2 | likely fold into GitHub umbrella unless unique trigger remains |
| github-issues | issue specialist | disable | P3 | situational, low centrality |
| research-briefing | research umbrella | keep | P0 | best umbrella |
| recent-news-briefing | news output specialist | keep | P1 | narrow counterpart to research umbrella |
| firecrawl-research | retrieval-layer specialist | keep | P1 | distinct backend/retrieval value |
| agent-reach-discovery | discovery specialist | keep | P2 | useful but niche |
| political-source-monitoring | specialized research leaf | disable | P2 | narrow trigger only |
| last30days-customization | specialized research leaf | disable | P3 | niche / low-use |
| autonomous-ai-agents | autonomous umbrella | keep | P1 | likely best top router for family |
| ouroboros/help | ouroboros router | keep | P1 | useful within ouroboros family |
| ouroboros/seed | large command leaf | patch | P1 | oversized and likely reference-heavy |
| ouroboros/run | command leaf | keep | P2 | explicit invocation skill |
| ouroboros/qa | command leaf | keep | P2 | explicit invocation skill |
| ouroboros/auto | command leaf | keep | P2 | explicit invocation skill |
| local-personal-dashboard | project workflow | patch | P1 | heavily patched, likely needs case notes moved to references |
| research-paper-writing | oversized specialist | patch | P1 | 100KB+ skill body is too large |
| hermes-agent | Hermes authoritative umbrella | patch | P1 | keep authoritative, but continue splitting examples into references |
| claude-code | external delegate skill | disable | P2 | zero-use on this host/workflow |
| codex | external delegate skill | disable | P2 | zero-use in skill layer |
| opencode | external delegate skill | disable | P2 | zero-use in skill layer |
| godmode | red-team/risky specialist | disable | P1 | sensitive, large, explicit-intent only |
| comfyui | large creative suite | disable | P2 | specialized, zero-use |
| p5js | creative suite | disable | P2 | specialized, zero-use |
| humanizer | creative specialist | patch | P3 | oversized if kept, otherwise disable |
| apple-notes | platform-specific | disable | P1 | wrong host platform |
| apple-reminders | platform-specific | disable | P1 | wrong host platform |
| findmy | platform-specific | disable | P1 | wrong host platform |
| imessage | platform-specific | disable | P1 | wrong host platform |
| macos-computer-use | platform-specific | disable | P1 | wrong host platform |
| atomic-desktop-app-installation | Fedora Atomic specialist | keep | P2 | host-relevant |
| fedora-atomic-dotfiles-adaptation | Fedora Atomic specialist | keep | P2 | host-relevant |
| silverblue-toolbox-wrapper-bootstrap | Fedora Atomic specialist | keep | P2 | host-relevant |
| wayland-session-management | desktop recovery specialist | keep | P2 | host-relevant |
| rootless-podman-compose-adaptation | container specialist | disable | P3 | situational |

## Archive/reconcile candidates

These are not direct edit targets in this pass, but should be checked for lingering references or stale usage metadata:
- archived GitHub leaves superseded by `github-operations`
- archived research leaves superseded by `research-briefing` / `recent-news-briefing`
- archived Wayland troubleshooting leaves superseded by `wayland-session-management`
- stale usage-only names such as:
  - `silverblue-desktop-ricing-adaptation`
  - `silverblue-update-automation`
  - `hermes-security-preflight`
  - `hermes-stack-maintenance`
  - `signal-oriented-research-briefing`

## Immediate live patch targets selected for this run
- `hermes-workflow-optimization`
- `hermes-operating-pattern`
- `hermes-context-budgeting`

## Pass 2 — Security integration (2026-06-30)

### Newly installed — security/ category
| Skill | Source | Status |
|---|---|---|
| security/codeql | Trail of Bits | active |
| security/semgrep | Trail of Bits | active |
| security/sarif-parsing | Trail of Bits | active |
| security/fp-check | Trail of Bits | active |
| security/agentic-actions-auditor | Trail of Bits | active |
| security/owasp-security | community | active |
| security/secret-hygiene | user-created | active |

### Archived in this pass
| Skill | Reason |
|---|---|
| xurl | CLI not installed on this host |
| yuanbao | CLI not installed on this host |
| petdex | mascot utility, no practical use |
| godmode | 403-line jailbreak, sensitive, no workflow use |
| superpowers-bootstrap | thin pointer to using-superpowers, redundant |
| porting-superpowers-to-hermes | one-time migration task, already done |
| apple/* (5 skills) | wrong host platform (Linux/Fedora Atomic) |
| codebase-inspection | superseded by semgrep + codeql |
| writing-plans | superseded by complexity-gated-planning |
| thunderbird-local-email-workflow | situational, low-use |

### Patches applied
- `requesting-code-review`: added security skill routing (semgrep, codeql, owasp-security, fp-check, secret-hygiene); tiered escalation in Step 2
- `workflow-map`: security routing extension added
- All broken `related_skills` references resolved across 16 skill files
- Descriptions trimmed: agentic-actions-auditor, fp-check, owasp-security

### New skill added
- `autonomous-ai-agents/autonomous-agent-loop-design`: patterns from Karpathy autoresearch (nanochat) — numeric objectives, cheap surrogates, reference-driven context, eval-as-infrastructure

These were chosen because they are high-overlap, low-risk documentation/routing edits with clear stale references to missing sibling skills.
