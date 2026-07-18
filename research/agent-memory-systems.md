# Agent Memory Systems — Research Findings (2024–2026)

Sources: arXiv systematic survey (July 2026), verified abstracts.
Original compiled in: ~/.hermes/skills/autonomous-ai-agents/agent-memory-consolidation/references/

---

## Memory System Architectures

### Mem0 — Production-Ready Long-Term Memory
- **arXiv:** 2504.19413 | Apr 2025 | cs.CL/cs.AI
- Write-time normalization gate: LLM decides insert/update/delete/merge before storage.
  Dual-mode: flat vector + optional graph-based relational memory.
- **Metrics:** 26% relative improvement on LOCOMO benchmark vs OpenAI full-context;
  91% lower p95 latency; >90% token cost reduction.
- **Key insight:** Pre-write normalization gate eliminates noisy duplicates at source.

### AgeMem — Agentic Memory with RL-Trained Unified Policy
- **arXiv:** 2601.01885 (v2: Apr 2026) | Jan 2026 | cs.CL
- **Authors:** Yu, Yao, Xie et al. (Alibaba DAMO)
- Memory ops (store/retrieve/update/summarize/discard) as tool-based actions trained via
  3-stage progressive RL + step-wise GRPO for sparse discontinuous rewards.
- **Metrics:** Outperforms strong baselines on 5 long-horizon benchmarks.
- **Code:** https://github.com/y1y5/AgeMem

### MemoryOS — OS-Inspired 3-Tier Memory Hierarchy
- **arXiv:** 2506.06326 | Jun 2025 | EMNLP 2025
- Short-term (context buffer) → mid-term (session history) → long-term (persistent personal).
  Composite eviction score: `score = alpha * recency + beta * frequency + gamma * importance`.
  Consolidation gate before long-term promotion.
- **Key insight:** Frequency dimension is missing from most agent memory implementations.

### MemOS — Memory OS with MemCube Abstraction
- **arXiv:** 2507.03724 (v4: Dec 2025) | Jul 2025 | cs.CL
- **Authors:** Li et al. (39-author consortium; MemTensor)
- MemCube = (content, metadata{provenance, versioning, type}, access_log).
  Types: plaintext / activation-based / parameter-level. MemCubes can be migrated,
  composed, fused (episodic → parametric via fine-tuning). Unifies RAG + KV-cache +
  model weights under one API.

### Zep / Graphiti — Temporal Knowledge Graph for Agent Memory
- **arXiv:** 2501.13956 | Jan 2025 | cs.CL/cs.AI/cs.IR
- Bi-temporal KG with valid_at/invalid_at edges. Contradiction resolution via LLM
  verification + edge invalidation (sets invalid_at, preserves history).
  Enables "belief at time T" queries.
- **Metrics:** DMR: 94.8% vs 93.4% (MemGPT). LongMemEval: 18.5% accuracy gain +
  90% latency reduction.

### TrustMem — Trustworthy Memory Consolidation (Jun 2026)
- **arXiv:** 2606.25161 | Jun 2026
- **Authors:** Yang, Paul, Srinivasan, Kulkarni, Chappidi
- Memory updates can omit info, corrupt existing memory, or hallucinate unsupported content.
  Adds Memory Transition Verifier scoring each update on: coverage / preservation / faithfulness.
  Builds preference pairs among candidates and runs preference-guided RL.
- **Metrics:** SOTA on MemoryAgentBench (ICLR 2026), HaluMem, Mem-alpha validation.
  +12.14 F1 on HaluMem. Reduces omission/corruption/hallucination by 40.1%/79.1%/50.0%.
- **Key insight:** Binary NLI contradiction check is insufficient — omission and unfaithful
  paraphrase also corrupt memory state.

### Human-Inspired Memory Architecture (May 2026)
- **arXiv:** 2605.08538 | May 2026
- Six-mechanism biologically-grounded architecture:
  1. Sleep-phase consolidation (batch dedup + integration, run offline/idle)
  2. Interference-based forgetting (new similar memories degrade old ones)
  3. Engram maturation (memories strengthen with reinforced recall)
  4. Reconsolidation upon retrieval (retrieving makes memory editable again)
  5. Entity knowledge graphs
  6. Hybrid multi-cue retrieval (multiple signals, not just top-K vector similarity)
- **Key insight:** Reconsolidation-on-retrieval — facts are static until retrieved, then
  become editable. A cheap approximation: when a fact is retrieved and used, run a staleness
  check on that specific fact since it was surfaced.

### SCM — Sleep-Consolidated Memory (Apr 2026)
- **arXiv:** 2604.20943 | Apr 2026
- Multi-stage sleep cycle: consolidation → dreaming → intentional forgetting.
  "Perfect recall + robust noise pruning" on benchmark.
- **Signal:** Two independent groups (this + arXiv:2605.08538) converging on sleep-phase
  batch consolidation in the same quarter — strong architectural signal.

---

## Episodic Memory Theory

### Position: Episodic Memory is the Missing Piece
- **arXiv:** 2502.06975 | Feb 2025 | cs.CL
- 5 cognitive properties currently missing from agents:
  1. Cue-dependent retrieval
  2. Spatiotemporal indexing
  3. Single-shot learning
  4. Autonoetic consciousness
  5. Constructive reconstruction
- **Gap:** Pure semantic-similarity retrieval misses all five. Spatiotemporal keys
  (session timestamp + task context) + cue-based lookup (partial key fragments) unexplored.

### H-MEM — Hierarchical Memory with Index Routing
- **arXiv:** 2507.22925 | Jul 2025 | cs.CL
- Multi-level abstraction tree. Each vector carries positional index pointer to related
  sub-memories in next layer. Index-based routing = O(log N) vs O(N) k-NN.
- **Metrics:** Outperforms 5 baselines on LoCoMo long-term dialogue dataset.
- **Insight:** Abstract summary nodes double as compression. Implementable via HNSW +
  periodic LLM summarization passes.

---

## RAG and Context Optimization

### MemoRAG — Global Memory + Draft-Answer Clue Generation
- **arXiv:** 2409.05591 (v3: Apr 2025) | Sep 2024 | TheWebConf 2025
- **Authors:** Qian, Liu, Zhang et al. (RUC / BAAI)
- Dual-system: (1) light long-range model creates global memory (KV compression), generates
  draft answers as retrieval clues; (2) expensive model uses clues + retrieved chunks for
  final answer. Memory trained with RLGF (RL from Generation Quality Feedback).
- **Gap:** Direct user query → embedding lookup. Draft-answer-as-clue (HyDE variant)
  improves recall on vague queries.

### ReadAgent — Gist Memory with Two-Level Compression
- **arXiv:** 2402.09727 | NeurIPS 2024 | Google DeepMind
- LLM segments context into coherent episodes; compresses each to short gist (1-5 sentences)
  + pointer to original; re-reads original on demand.
- **Metrics:** 20x effective context extension. +20% on QuALITY.

### RAPTOR — Recursive Abstractive Tree Retrieval
- **arXiv:** 2401.18059 | ICLR 2024 | Stanford NLP + MIT CSAIL
- **Authors:** Sarthi, Abdullah, Tuli, Khanna, Goldie, Manning
- Builds summary tree: leaf = raw chunk, parent = LLM summary of clustered children
  (Gaussian mixture in embedding space). Retrieval traverses tree at any level.
- **Metrics:** +10.9% QASPER, +3.9% QuALITY (RAPTOR + GPT-4). SOTA multi-step QA.

### RLMs — Recursive Language Models
- **arXiv:** 2512.24601 (v3: May 2026) | Dec 2025 | cs.AI/cs.CL
- **Authors:** Zhang, Kraska, Khattab (MIT CSAIL + Stanford)
- Inference-time paradigm: treats long prompt as external environment, decomposes into
  snippets, recursively calls itself over sub-problems, maintains working memory of results.
- **Metrics:** Processes 100x beyond context window. +26% vs compaction, +130% vs CodeAct,
  +13% vs Claude Code on long-retrieval tasks.
- **Code:** https://github.com/alexzhang13/rlm

### LongRAG — Long-Context Retrieval Units
- **arXiv:** 2406.15319 | Jun 2024 | CMU LTI
- **Authors:** Jiang et al. (Carnegie Mellon Language Technologies Institute)
- Replace 100-token chunks with 4K-token documents. Fewer retrieval units (2-8 vs 50-100).
  Long-context LLM handles full unit in one pass.
- **Metrics:** NQ: 62.7% answer recall with only 4 units (vs 100 short units for equivalent
  DPR recall). Reduces retrieval precision requirements.

---

## Forgetting Mechanisms

### Forgetting Mechanism Taxonomy (from memory system surveys)
- **Source:** Multiple surveys including arXiv 2507.05633, 2507.22931
- **Types:**
  1. Decay-based: time-weighted score reduction, Ebbinghaus curve approximation
  2. Interference-based: proactive (new overwrites old) / retroactive (old interferes with new)
  3. Capacity-limited eviction: FIFO, LRU, LFU, importance-weighted
  4. Selective rehearsal: periodic replay of at-risk memories (hippocampal SWS replay analog)
  5. Abstraction-driven compression: replace episodic set with semantic summary as memories age
- **Metrics:** Importance-weighted eviction outperforms FIFO/LRU by 15-30% on recall benchmarks.
- **Key gap:** Time-decay weighting (importance × e^(-lambda * age)) + frequency tracking.

### MemoryOS Composite Eviction Score
```
score = alpha * recency + beta * frequency + gamma * importance
```
- Short-term: FIFO eviction
- Mid-term: LFU with importance override
- Long-term: importance-only threshold + consolidation gate

---

## Contradiction Detection and Consistency

### Post-Retrieval NLI Consistency Filtering
- **Source:** RAG Survey (arXiv 2506.00054, Jun 2025) + Zep paper
- **Approaches:**
  1. NLI post-filtering: score chunks for entailment/contradiction with query+context
     before injection; ~8-12% hallucination reduction
  2. Contrastive decoding: generate with/without retrieval, take difference
  3. Self-consistency voting: multiple retrieval calls, majority-vote; +5-15% on multi-hop QA
  4. Attribution-aware generation: model cites source chunk per claim

### Zep Temporal Conflict Resolution
- When new fact conflicts with existing edge: LLM verification → set `invalid_at=now`
  on old edge → insert new edge with `valid_at=now`.
  Preserves both edges for historical queries.

---

## Memory Security (July 2026)

### FARMA / SENTINEL (Penn State) — Memory Poisoning and Defense
- **arXiv:** 2607.05029 | Jul 2026
- **FARMA:** Poisons reasoning traces via self-referential reinforcement (beats consensus defense).
- **SENTINEL:** 5 structural signals on reasoning provenance. 0% ASR vs 100% baseline.
- **Application:** Verify that retrieved memories have provenance metadata before trusting.

### GhostWriter / AM-Sentry (NM State) — Tool-Injection Memory Attack
- **arXiv:** 2607.06595 | Jul 2026
- Two-phase injection+activation via tool-using agents.
  AM-Sentry defense: write-policy + retrieve-screen. ~98% injection rate baseline; AM-Sentry stops it.
- **Application:** Memory write-policy enforcement — validate what gets written, not just what's read.

---

## Production Patterns (mcp-memory-service, Jul 2026)

Source: doobidoo/mcp-memory-service v11.3.3 (Codeberg, 2026-07-01)

### NLI-based contradiction detection
Before writing a new memory, run NLI against existing memories in same entity/topic domain.
Practical approximation: surface new + existing fact to LLM with binary question: "Does new
fact contradict existing? Y/N + reason." If Y: prepare REPLACE, not ADD.

### Session-end consolidation gate
Commit: "fix(hooks): gate session-end consolidation on substantive content" (2026-06-22).
Default = skip consolidation if session was idle chatter, simple Q&A, or one-turn answers.
Hard gate: only consolidate if session had 5+ non-trivial tool calls, user correction,
workflow surprise, or new environmental knowledge discovered.

### Multi-agent shared memory via sentinel tags
Agents tag memories with a sentinel string (e.g. `msg:cluster:agent-id`). Other agents
filter on that tag to receive cross-agent signals. Memory service becomes coordination layer.

### Memory quality scoring (per-entry)
Score each entry on: relevance, freshness, specificity. Low-scoring memories decay on each
retrieval miss, pruned at threshold. Current implementations gate new entries but don't prune stale ones.

### Typed knowledge graph edges
Edge types: causes, fixes, contradicts, depends_on, supersedes. More precise than vector proximity.
A "fixes" edge between "bug X" and "workaround Y" survives semantic drift in embedding space.

---

## July 2026 High-Impact Papers

### AutoMem (Stanford)
- **arXiv:** 2607.01224 | Jul 2026
- Two-loop: outer loop rewrites memory scaffold (prompts/schemas/vocab);
  inner loop trains memory specialist from its own good decisions.
- **Metrics:** 2-4x improvement on Crafter/MiniHack/NetHack. 32B open model approaches
  Opus-class quality on memory-intensive tasks.

### Shared Selective Persistent Memory
- **arXiv:** 2607.09493 | Jul 2026
- 4-category selective persistence: task specs / data schemas / tool configs / output constraints.
  Zero-token data refresh; RBAC sharing between agents.
- **Metrics:** 96% vs 79% task completion; 97x token reduction; 14x time reduction.

### AdaCoM (context management via RL)
- **arXiv:** 2605.30785 | May 2026
- RL-trained external manager LLM edits frozen agent's context (delete/rewrite/merge).
  Fidelity-reliability tradeoff: strong agent → preserve, weak agent → compress.
- **Metrics:** Beats fixed-context baselines on web search.

---

## Implementation Priority Matrix

| Gap | Effort | ROI |
|-----|--------|-----|
| Time-decay on retrieval scores: `score * exp(-0.1 * days_since_access)` | Low | High |
| HyDE query expansion: generate draft answer → use as embedding query | Low | High |
| Access frequency counter on knowledge graph edges | Low | High |
| Post-retrieval pairwise NLI filter | Medium | High |
| Write-time normalization gate (Mem0 style: insert/update/delete/merge) | Medium | High |
| Gist + pointer 2-level compression (ReadAgent pattern) | Medium | Medium |
| Mid-term memory tier (session-scoped) | High | Medium |
| Hierarchical index routing (H-MEM, HNSW + abstract summary nodes) | High | Medium |
| RAPTOR tree over corpus (offline periodic job) | High | Medium |
| Sleep-phase batch consolidation (idle-time dedup pass) | Medium | High |
