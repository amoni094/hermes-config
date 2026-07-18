# Research Index

This directory contains research findings compiled from academic literature surveys
conducted between 2024 and 2026. All papers are cited with arXiv IDs or DOIs where
available, and have been verified against source abstracts.

All content is in English. Where original research was published in other languages
(Chinese, Japanese, Korean, Russian, French, German), findings have been translated
and summarized in English. Non-English source venues are noted in the entries.

## Files

| File | Topics |
|------|--------|
| [agent-memory-systems.md](agent-memory-systems.md) | Memory architectures, RAG, forgetting mechanisms, contradiction detection, memory security |
| [agent-optimization.md](agent-optimization.md) | Skill learning, self-improvement, skill library management, harness design, observability |
| [multi-agent-workflows.md](multi-agent-workflows.md) | Coordination topology, safety, security, multi-agent system design patterns |
| [neurosymbolic-ai.md](neurosymbolic-ai.md) | NeSy paradigms, theorem proving, robot planning, constrained generation, local implementation |
| [llm-routing-and-efficiency.md](llm-routing-and-efficiency.md) | LLM routing, KV-cache optimization, prompt compression, speculative decoding, CoT reduction |

## Key Themes Across Findings

### Memory and State Management
The dominant research direction is moving from simple vector similarity retrieval to
structured memory management: write-time normalization gates, temporal knowledge graphs
with bi-temporal validity, hierarchical memory tiers (short/mid/long-term), and
biologically-inspired forgetting mechanisms (decay, interference, consolidation).

### Agent Efficiency via Skills
Skills consistently improve task performance (+16-24pp depending on domain) but only when:
- focused (3 or fewer modules)
- routed using full skill body text (not just metadata)
- maintained through a lifecycle (create/improve/merge, not just add)

Pre-compiling successful agentic runs into deterministic state machines (PreAct) is a
highly practical optimization: 8.5-13x speedup on repeat tasks.

### Neurosymbolic Integration
The highest-value NeSy pattern for production agents is the symbolic feedback loop:
LLM generates candidate → formal verifier provides binary pass/fail → loop.
This pattern is cheap (no fine-tuning), API-compatible, and yields substantial accuracy
gains (Forethought: ~30%; BioProAgent: 95.6% vs 21.0% baseline with 6x token reduction).

### Multi-Agent Safety
Two key safety architectures emerged in 2026:
1. Transaction-safe workflows (Mnemosyne/ATP): LLM proposals admitted only if they pass
   a constraint set; append-only log; <6% overhead; 0 invalid commits.
2. Prompt injection isolation (CaMeL): tag untrusted data from tool results so it can
   never influence control flow; 77% task success on injection-heavy benchmarks.

### LLM Routing
Routing by task type and known model failure modes beats routing by size/cost tier.
The R2-Router (ICML 2026) insight is actionable immediately: before escalating model tier,
retry with a tighter length budget on the current model.

## Research Coverage Dates
- English academic: 2024–July 2026
- Non-English venues: 2023–July 2026 (multilingual sweep)
- Last updated: July 2026
