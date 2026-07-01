# Hermes Upgrade Pass 3 — 2026-07-01

Third upgrade pass. Focus: security (new upstream adversarial threat patterns),
supply-chain hardening, and a deliberate review of previously-untouched workflow /
token-efficiency / general-config surfaces. All config mutations applied via
`hermes config set`; veto rules edited directly. No secrets committed.

---

## Dependency DAG (execution order)

```
research (read prior passes, live config, veto rules, validate_repo)
   │
   ├─► security: append hard-block rules (reverse-shell, nc/socat, mkfifo, decode-exec)
   ├─► security: append warn rules (html img-src exfil, css concealment)
   ├─► config: hermes config set security.allow_lazy_installs false
   │
   └─►(all above)─► export: mirror veto rules + regenerate config.sanitized.yaml
                        │
                        └─► validate_repo.py  ──► commit ──► push ──► restore delegation.model
```

Security rule authoring and the config change are independent; both must land
before the export/validation/commit stage.

---

## 1. Security Hardening — new upstream threat patterns

### 1a. Veto hard-block rules (+4)

File: `~/.hermes/veto/rules/hermes-hard-blocks.yaml`

| Rule ID | Pattern Blocked | Rationale |
|---|---|---|
| `block-reverse-shell` | `/dev/tcp|/dev/udp` shells; `sh -i` wired to `>&`/`nc`; inline `socket.socket`/`IO::Socket`/`TCPSocket` → shell | Remote interactive host takeover |
| `block-nc-exec-backdoor` | `nc/ncat -e|--exec|-c`, `socat EXEC:|SYSTEM:` | Canonical netcat/socat backdoor |
| `block-mkfifo-backdoor` | `mkfifo` + shell + `nc/ncat/telnet` relay | Named-pipe reverse shell that evades a single-command `nc -e` block |
| `block-obfuscated-decode-exec` | `openssl … -d | sh`, `xxd -r | sh`, python `b64decode`/`codecs.decode | sh` | Non-coreutils decode-then-exec bypasses of `block-base64-exec` |

### 1b. Veto warn rules (+2)

File: `~/.hermes/veto/rules/hermes-warn.yaml`

| Rule ID | Pattern Warned | Rationale |
|---|---|---|
| `warn-html-img-src-exfil` | Written HTML/markdown with `<img src=…?…>`, `url(http…?…)`, `fetch(http…?…)` | Zero-click exfil beacon via auto-loaded remote resource carrying query data |
| `warn-css-visibility-conceal` | `display:none`/`visibility:hidden`/`opacity:0`/`0-1px` sizing near an off-host URL | Hidden injected instructions / concealed exfil that a rendered-page review misses |

Adversarial frame: an attacker with full read access to config/hooks would look
for interpreter-level and encoding-level bypasses of the shell-string blocks. The
pass-3 rules specifically target those bypass classes (socket payloads in three
languages, four decode channels, and a named-pipe relay that splits the backdoor
across multiple tokens). The HTML/CSS warns cover the emerging document-render
exfiltration surface that terminal-only rules never saw.

Total veto rules after pass 3: **24 hard-block, 13 warn**.

---

## 2. Supply-chain / general config

### 2a. `security.allow_lazy_installs` → false

```
hermes config set security.allow_lazy_installs false
```

Previously `true`. Lazy/auto installs let the agent pull arbitrary packages
mid-task without an explicit, reviewable install step — a supply-chain risk
(typosquat / compromised transitive dep executes before any human sees it). On
this immutable Silverblue host, deliberate `uv`/`toolbox` installs are the
correct path anyway, so the convenience cost is negligible against the risk.

---

## 3. Surfaces reviewed and deliberately left unchanged

These were the prior passes' untouched targets. Each was assessed this pass;
none warranted a unilateral flip. Rationale recorded so pass 4 need not re-derive:

| Surface | Current | Verdict | Reason |
|---|---|---|---|
| `approvals.mode` | `manual` (timeout 60, cron `deny`) | keep | It is the correct human-in-the-loop posture. The prior pass being "blocked on reads" was a workflow artifact, not a defect. Flipping to auto would remove the primary consent gate — a security regression, not an improvement. |
| `security.website_blocklist` | disabled, empty | keep | An empty blocklist is inert; enabling it with no domains adds no protection. It should be populated only in response to a concrete threat/policy, not enabled speculatively. |
| `compression.protect_last_n` | 32 | keep | 32 balances recall of recent turns against compression headroom at threshold 0.5 / ratio 0.33. No evidence of premature loss of needed context; lowering risks dropping live working state, raising defeats the compression target. |
| `streaming` | disabled (cli); telegram on | keep | CLI streaming off is a deliberate quieter-output choice; per-platform overrides already correct. |
| `sessions` | auto_prune, 90-day retention, vacuum | keep | Sound hygiene defaults; no secrets in scope, retention reasonable. |
| `logging` | INFO, 50MB, 10 backups | keep | Standard rotating-log posture; INFO is the right signal/noise level. |
| `delegation.max_spawn_depth` | 1 | keep | Same rationale as pass 2 — raising needs a tested orchestration pattern and concurrency co-tuning. |

---

## 4. Repo export

- Mirrored updated veto rules into `veto/rules/` (hard-blocks +4, warn +2).
- Regenerated `config.sanitized.yaml` via `scripts/sanitize_config.py`
  (now reflects `allow_lazy_installs: false`).
- `python3 scripts/validate_repo.py` → **repo validation passed**.

---

## Files changed

| File | Change |
|---|---|
| `~/.hermes/veto/rules/hermes-hard-blocks.yaml` | +4 hard-block rules |
| `~/.hermes/veto/rules/hermes-warn.yaml` | +2 warn rules |
| `~/.hermes/config.yaml` | `security.allow_lazy_installs=false` (via `config set`) |
| `hermes-config/veto/rules/*.yaml` | mirrored |
| `hermes-config/config.sanitized.yaml` | regenerated |
| `hermes-config/docs/upgrade-pass-2026-07-01-pass3.md` | this document |
| `hermes-config/docs/current-workflow.md` | pass-3 refs + settings refreshed |

---

## Completion summary (JSON)

```json
{
  "changes_made": [
    "veto hard-blocks +4: block-reverse-shell, block-nc-exec-backdoor, block-mkfifo-backdoor, block-obfuscated-decode-exec",
    "veto warn +2: warn-html-img-src-exfil, warn-css-visibility-conceal",
    "security.allow_lazy_installs set false (supply-chain hardening)",
    "config.sanitized.yaml regenerated; veto rules mirrored to repo",
    "docs/upgrade-pass-2026-07-01-pass3.md created; current-workflow.md refreshed"
  ],
  "risks_identified": [
    "New backdoor/decode regexes could false-positive on legitimate openssl/xxd/socket usage — mitigated by narrow anchoring (pipe-to-shell or EXEC: required)",
    "HTML/CSS warns are advisory only (action=warn) so do not block genuine exfil, only log it",
    "allow_lazy_installs=false may surface as a failed auto-install mid-task; expected and preferable to silent package pulls"
  ],
  "items_deferred": [
    "Populating website_blocklist domains (needs a concrete policy/threat list)",
    "approvals.mode automation ergonomics (workflow-intent decision, not a security fix)",
    "delegation.max_spawn_depth raise (needs tested orchestration + concurrency co-tuning)"
  ],
  "confidence": "high",
  "recommend_followup": false
}
```
