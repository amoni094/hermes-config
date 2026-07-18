# LLM Routing, Efficiency, and Token Optimization — Research Findings (2024–2026)

Sources: arXiv systematic survey, academic literature sweep July 2026.
Original compiled in: ~/.hermes/skills/research/academic-literature-review/references/token-optimization-papers-2024-2026.md
and ~/.hermes/skills/autonomous-ai-agents/harness-first-agent-design/references/agent-efficiency-jul2026.md

---

## LLM Routing Research

### LLMRouterBench (ACL 2026)
- **arXiv:** 2601.07206 | ACL 2026
- Commercial routers often perform at or below a simple baseline.
  Main gap: model-recall failure (model reliably fails specific query types).
  Large ensembles perform no better than careful curation.
- **Finding:** Route by task type and known model failure modes, not just by model size/cost.

### Dynamic Routing Survey (Trinity College Dublin / Huawei)
- **arXiv:** 2603.04445 | Feb 2026
- 3-dimensional taxonomy: when to route / what to route to / how to route.
  Well-designed routing outperforms the best single model.

### R2-Router — Joint Model + Length-Budget Routing (ICML 2026)
- **arXiv:** 2602.02823 | ICML 2026
- Routers should jointly pick (model, output-length budget), not just model.
  A length-constrained pass on the current-tier model can match a higher-tier model's quality
  at much lower cost.
- **Application:** Before escalating model tier, retry with a tighter length budget on the current model.

---

## Token Optimization: KV-Cache

### SnapKV
- **arXiv:** 2404.14469 | NeurIPS 2024 | UIUC + WestLake University
- 3.6x memory reduction; fine-tuning-free; attention-pattern-based.

### InfiniGen (Seoul National University)
- **arXiv:** 2406.19707 | OSDI 2024 | SNU
- 1.4-2x throughput on 32K+ tokens; 4x GPU memory savings; CPU offload.
- **Code:** github.com/snu-comparch/InfiniGen

### SpeCache (Peking University)
- **arXiv:** 2503.16163 | ICML 2025
- 50% VRAM reduction; low-bit shadow KV for speculative prefetch.

### KeepKV (Chinese Academy of Sciences)
- **arXiv:** 2504.09936 | AAAI 2025
- 2-4x lossless KV compression; Electoral Votes + ZIPM mechanism.

### Expected Attention + KVPress (NVIDIA Paris / Sapienza)
- **arXiv:** 2510.00636 | Oct 2025
- Training-free; closed-form expected attention via Gaussianity of LLM activations.
  Releases KVPress: 20+ compression methods, pip-installable.
- **pip:** `pip install kvpress`

### InfiniteHiP (KAIST + DeepAuto.AI)
- **arXiv:** 2502.08910 | 2026
- 18.95x attention speedup; 3M tokens on single L40s 48GB GPU.

### REFORM (KAIST)
- **arXiv:** 2506.01215 | NeurIPS 2025
- 52% improvement on RULER long-context benchmark; 30% inference time reduction.

---

## Token Optimization: Prompt and Context Compression

### LLMLingua-2 (Microsoft Research)
- **arXiv:** 2403.12968 | ACL 2024 Findings
- 3-6x faster; 1.6-2.9x end-to-end latency at 2-5x compression ratio.
  Task-agnostic; works entirely independently of target LLM; BERT-level encoder runs on CPU.
- **pip:** `pip install llmlingua`

```python
from llmlingua import PromptCompressor
compressor = PromptCompressor(model_name="microsoft/llmlingua-2-xlm-roberta-large-meetingbank")
result = compressor.compress_prompt(context, rate=0.5, force_tokens=["\n", "?"])
compressed = result["compressed_prompt"]
```

### ACC-RAG (Leiden University)
- **arXiv:** 2507.22931 | EMNLP 2025 Findings
- Adaptive compression rate beats any fixed rate on RAG QA benchmarks.
  Hierarchical compressor + adaptive selector.

### Recommended Hybrid RAG Compression Pipeline
1. LLMLingua-2 extractive pass at 3-5x compression on retrieved chunks
2. Complexity gate: if query_complexity > threshold → keep extractive output; else → Haiku abstractive merge
3. Complexity signals: query perplexity, entity count, multi-hop indicator keywords

---

## Token Optimization: Speculative Decoding

### EAGLE-3 (SafeAI Lab / Beihang University)
- **arXiv:** 2503.01840 | NeurIPS 2025
- 3.0-6.5x speedup; 1.38x throughput at batch=64 in SGLang.
- EAGLE lineage: EAGLE-1 (ICML 2024): 2-3x → EAGLE-2 (2024): 3-4.3x → EAGLE-3: 3-6.5x
- **Code:** github.com/SafeAILab/EAGLE

### Heterogeneous-Vocab Speculative Decoding (Weizmann + Intel Labs)
- **arXiv:** 2502.05202 | ICML 2025 Oral (top 1%)
- 2.8x speedup; removes shared-vocab constraint; training-free; off-the-shelf.
  Enables mixing models from different vendor families (e.g. Mistral draft → Llama target).
- **Authors:** Timor, Mamou, Korat, Berchansky, Jain, Pereg, Wasserblat, Harel (Weizmann / Intel)

### OmniDraft (Qualcomm AI Research)
- **arXiv:** 2507.02659 | NeurIPS 2025
- 1.5-2x speedup; single draft model for multiple target families.

### Binary Block Masking (MPI-IS Tubingen, Jonas Geiping)
- **arXiv:** 2409.15097 | NeurIPS Workshop 2024 → ICML 2025
- Up to 9x runtime reduction on sparse FlashAttention masks.
  Drop-in for: packed fine-tuning, Medusa tree attention, sparse long-doc attention.

---

## Token Optimization: Chain-of-Thought Length Reduction

### TALE — Token-Budget-Aware LLM Reasoning (Shanghai Jiao Tong)
- **arXiv:** 2412.18547 | ACL 2025 Findings
- ~40% CoT reduction, ~2% accuracy drop; pure prompt engineering, API-compatible.
- **Calibrated budget targets by task type (set at P80, not median):**
  - Math / formal reasoning: ~800 tokens
  - Code generation: ~600 tokens
  - Factual retrieval: ~200 tokens
  - Creative writing: ~400 tokens
- **Warning:** ThinkPrune (2504.01296) confirms hard budget-forcing without RL causes wrong
  answers when budget < actual task need. Use P80, not median.

**Budget hint pattern (prepend before reasoning task):**
```
[Budget: Use approximately {N} tokens for your reasoning steps.]
```

### Compact Constraint Headers
- **arXiv:** 2604.07192 | 2026
- 71% token reduction for FSM/constrained agent prompts with no constraint satisfaction loss.
  Compress schema headers; rely on structured format, not verbose explanation.

---

## Efficient Inference: Regional Research Highlights

### South Korea
- SNU: InfiniGen (OSDI 2024) — 1.4-2x throughput on 32K+ tokens
- KAIST + DeepAuto.AI: InfiniteHiP — 18.95x attention speedup; 3M tokens on single L40s
- KAIST: REFORM — 52% RULER improvement; 30% inference time reduction
- KAIST-adjacent: Multilingual speculative decoding (arXiv:2406.16758, EMNLP 2024)

### Japan
- NII: LLM-jp-4 32B-A3B (2026) — MoE, only 3B active params at inference (~70% compute reduction); Apache 2.0
- RIKEN + Tokyo Tech: Fugaku-LLM (2024) — data mixing optimization reduces pretraining token budget ~30%

### Germany
- MPI-IS Tubingen: Binary Block Masking — up to 9x runtime reduction on sparse attention

### France / NVIDIA Paris
- Expected Attention + KVPress (arXiv:2510.00636) — closed-form expected attention

### United Kingdom
- Oxford OATML (Yarin Gal): Semantic Entropy — Nature 2024 — AUROC 0.79 for hallucination detection
- Cambridge: EfficientLLM benchmark (arXiv:2505.13840) — spec-decoding + INT8 = highest-leverage combo

### Israel
- Weizmann + Intel Labs: Heterogeneous-vocab SD — removes cross-vendor draft/target constraint

---

## Hallucination Detection

### Semantic Entropy (Oxford OATML, Yarin Gal)
- **Nature 2024**
- AUROC 0.79 for hallucination detection via semantic entropy of output distribution.
  No ground truth required. Works by measuring semantic consistency across multiple samples.

---

## Context Management Research

### AdaCoM — RL Context Management
- **arXiv:** 2605.30785 | 2026
- RL-trained external manager LLM edits frozen agent's context (delete/rewrite/merge).
  Fidelity-reliability tradeoff: strong agent → preserve context; weak agent → compress.

### ReadAgent — Gist Memory
- **arXiv:** 2402.09727 | NeurIPS 2024 | Google DeepMind
- Two-level compression: gist (1-5 sentence summary) + pointer to original.
  Re-reads original on demand. 20x effective context extension.

### RLMs — Recursive Language Models
- **arXiv:** 2512.24601 (v3: May 2026) | MIT CSAIL + Stanford
- Recursively decomposes long prompt into sub-problems, maintains working memory.
  Processes 100x beyond context window without fine-tuning.

---

## Source Reference Table

| Paper | arXiv ID | Venue | Year |
|-------|---------|-------|------|
| LLMRouterBench | 2601.07206 | ACL 2026 | 2026 |
| Dynamic Routing Survey | 2603.04445 | — | 2026 |
| R2-Router | 2602.02823 | ICML 2026 | 2026 |
| SnapKV | 2404.14469 | NeurIPS 2024 | 2024 |
| InfiniGen (SNU) | 2406.19707 | OSDI 2024 | 2024 |
| SpeCache | 2503.16163 | ICML 2025 | 2025 |
| KeepKV | 2504.09936 | AAAI 2025 | 2025 |
| KVPress | 2510.00636 | — | 2025 |
| InfiniteHiP | 2502.08910 | — | 2026 |
| REFORM (KAIST) | 2506.01215 | NeurIPS 2025 | 2025 |
| LLMLingua-2 | 2403.12968 | ACL 2024 | 2024 |
| ACC-RAG | 2507.22931 | EMNLP 2025 | 2025 |
| EAGLE-3 | 2503.01840 | NeurIPS 2025 | 2025 |
| Hetero-vocab SD | 2502.05202 | ICML 2025 Oral | 2025 |
| OmniDraft | 2507.02659 | NeurIPS 2025 | 2025 |
| Binary Block Masking | 2409.15097 | ICML 2025 | 2024 |
| TALE | 2412.18547 | ACL 2025 | 2024 |
| ThinkPrune | 2504.01296 | — | 2025 |
| Compact headers | 2604.07192 | — | 2026 |
| Semantic Entropy | — | Nature 2024 | 2024 |
| AdaCoM | 2605.30785 | — | 2026 |
| ReadAgent | 2402.09727 | NeurIPS 2024 | 2024 |
| RLMs | 2512.24601 | — | 2025 |
| EfficientLLM | 2505.13840 | — | 2025 |
