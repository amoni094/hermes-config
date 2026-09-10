# Signal vs Noise / Information Theory Research Corpus -- Paper Index

Generated: 2026-09-10
Total papers: 42

Papers cited across: information-theory-for-agents, rr-compaction-scorer,
hermes-context-hygiene, hermes-context-budgeting skills.
These underpin the SIGNAL/NOISE/CAUSAL tagging, RR compaction scorer,
rate-distortion framing, and context budget policy in Hermes.

## Paper Listing

| arXiv ID | Title | Referenced In |
|----------|-------|---------------|
| arXiv:2307.03172 | Lost in the Middle: How Language Models Use Long Contexts | IT-for-agents, rr-compaction-scorer |
| arXiv:2507.22931 | (title not recorded) | h-context-budgeting |
| arXiv:2510.00615 | (title not recorded) | rr-compaction-scorer, h-context-budgeting |
| arXiv:2510.07777 | ECS: Effort-Calibrated Summarization for LLM Agents | IT-for-agents, h-context-hygiene |
| arXiv:2601.11585 | ECS: Pragmatic Utility for Agent Context (ECS paper) | IT-for-agents |
| arXiv:2602.09789 | (title not recorded) | rr-compaction-scorer |
| arXiv:2604.11462 | (title not recorded) | IT-for-agents |
| arXiv:2604.14004 | STALE: Semantic Staleness Detection for Agent Memory | IT-for-agents, h-context-hygiene |
| arXiv:2604.15356 | (title not recorded) | IT-for-agents |
| arXiv:2604.17091 | (title not recorded) | h-context-budgeting |
| arXiv:2605.06527 | STALE: System-State Memory Staleness (STALE framework) | IT-for-agents, h-context-hygiene |
| arXiv:2605.26302 | (title not recorded) | h-context-budgeting |
| arXiv:2606.08151 | (title not recorded) | IT-for-agents |
| arXiv:2606.10209 | (title not recorded) | h-context-hygiene |
| arXiv:2606.17016 | (title not recorded) | h-context-budgeting |
| arXiv:2606.18746 | CICL: Continual In-Context Learning for Agents | IT-for-agents, h-context-hygiene |
| arXiv:2606.23525 | SelfCompact: When to Fire/Suppress Compaction | IT-for-agents, h-context-hygiene |
| arXiv:2606.30005 | (title not recorded) | rr-compaction-scorer |
| arXiv:2607.08032 | Rate-Distortion Taxonomy for LLM Context Compaction | IT-for-agents, rr-compaction-scorer, h-context-budgeting |
| arXiv:2607.21503 | (title not recorded) | h-context-budgeting |
| arXiv:2607.25066 | (title not recorded) | rr-compaction-scorer |
| arXiv:2607.28103 | (title not recorded) | IT-for-agents |
| arXiv:2608.00101 | (title not recorded) | h-context-budgeting |
| arXiv:2608.00902 | (title not recorded) | h-context-budgeting |
| arXiv:2608.01056 | (title not recorded) | IT-for-agents, h-context-budgeting |
| arXiv:2608.02113 | (title not recorded) | h-context-budgeting |
| arXiv:2608.07429 | TEPA: Temporally-Extended Persistent Agent Memory | IT-for-agents |
| arXiv:2608.08389 | (title not recorded) | h-context-budgeting |
| arXiv:2608.09412 | (title not recorded) | h-context-budgeting |
| arXiv:2608.11775 | (title not recorded) | h-context-hygiene |
| arXiv:2608.12322 | (title not recorded) | IT-for-agents |
| arXiv:2608.15127 | (title not recorded) | h-context-budgeting |
| arXiv:2608.16370 | Compression Safety: 5x Compression Retrieval Cost Study | IT-for-agents, rr-compaction-scorer, h-context-budgeting |
| arXiv:2608.17433 | (title not recorded) | h-context-budgeting |
| arXiv:2608.19662 | (title not recorded) | h-context-budgeting |
| arXiv:2608.19784 | (title not recorded) | h-context-budgeting |
| arXiv:2608.21265 | (title not recorded) | h-context-budgeting |
| arXiv:2608.22752 | (title not recorded) | h-context-budgeting |
| arXiv:2608.23541 | (title not recorded) | h-context-budgeting |
| arXiv:2609.00237 | (title not recorded) | h-context-budgeting |
| arXiv:2609.01131 | From Source Reconstruction to Predictive State Preservation (Rate-Distortion for Agents) | IT-for-agents, h-context-hygiene |
| arXiv:2609.08033 | (title not recorded) | h-context-hygiene |

## Key Papers (Known Titles)

- arXiv:2307.03172 -- Lost in the Middle (Liu et al.) -- positional attention bias, basis for RR compaction
- arXiv:2601.11585 / arXiv:2510.07777 -- ECS: Effort-Calibrated / Pragmatic Utility scoring
- arXiv:2605.06527 / arXiv:2604.14004 -- STALE: semantic staleness detection for agent memory facts
- arXiv:2606.23525 -- SelfCompact: LLM self-assessment of when to compress
- arXiv:2607.08032 -- Rate-Distortion Taxonomy: KV eviction / prompt pruning / agent memory as one RD problem
- arXiv:2608.07429 -- TEPA: Temporally-Extended Persistent Agent memory, conflict detection
- arXiv:2608.16370 -- Compression Safety: at 5x compression, retrieval calls triple
- arXiv:2609.01131 -- Predictive State Preservation: distortion = lost predictive performance, not lost tokens

## Vervaeke / Relevance Realization Theory

See: research/relevance-realization-corpus.md
Core citation: Vervaeke, Lillicrap & Richards (2012). J. Logic and Computation 22(1):79-99
Applied in: rr-compaction-scorer (retention_score = pp - lambda * cp)
