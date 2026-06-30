# Hermes Audit Config Changes — 2026-06-30

Applied from holistic audit (auditor: claude-opus-4-8).

## config.yaml patches

| Setting | Old | New | Rationale |
|---------|-----|-----|-----------|
| agent.api_max_retries | 1 | 3 | Survive transient 429/5xx in long/delegated sessions |
| mcp_discovery_timeout | 0.5 | 3 | qmd has connect_timeout:45; 0.5s intermittently drops knowledge base |
| compression.target_ratio | 0.2 | 0.33 | 0.2 over-compresses multi-agent context; 0.33 preserves synthesis fidelity |
| compression.protect_last_n | 20 | 32 | Single fan-out wave can exceed 20 messages |
| prompt_caching.cache_ttl | 5m | 1h | 5m evicts cache between delegation waves in 30m sessions |
| auxiliary.compression.max_tokens | 2048 | 4096 | Avoid truncated summaries on large 128k sessions |
| tool_loop_guardrails.hard_stop_enabled | false | true | Warn-only does not stop runaway loops |

## veto/security patches (by security subagent)

- hermes-hard-blocks.yaml: +5 new hard-block rules (find -delete, truncate -s0, python os.remove, chmod -R $HOME, dd zeros to file)
- veto-pre-tool.py: patched to fail CLOSED on parse error / exception (was failing open)
- track-budget.py: audit note added — destructive_calls is post-hoc only, not pre-blocked

## new skills created

- autonomous-ai-agents/hermes-context-packet — canonical compact JSON spawn packet schema
- autonomous-ai-agents/hermes-swarm-consensus — deterministic verdict reducer + arbiter escalation

## skills patched

- autonomous-ai-agents/hermes-role-pipelines — added Context Packet Discipline, Handoff Checkpointing, Conflict Resolution sections
