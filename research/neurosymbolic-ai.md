# Neurosymbolic AI — Research Findings (2024–2026)

Sources: English academic (arXiv, ACM, IEEE, NeurIPS, ICLR, IJCAI, AAAI, KR, EMNLP),
non-English venues (Chinese CCF/CNCC, Japanese IPSJ, Korean RISS, Russian RAS/SPIIRAS,
French TALN/CORIA, German arXiv institutions), GitHub ecosystem, PyPI.
Full survey: ~/Documents/neurosymbolic-ai-research-2026.md
Local implementation: ~/Documents/neurosymbolic/nesy.py (6 classes, all verified)

---

## What Is Neurosymbolic AI?

Neurosymbolic AI (NeSy AI) combines:
- Neural networks: perception, unstructured data, generalization — but black-box, hallucination-prone
- Symbolic AI: logic, interpretability, constraint satisfaction — but brittle at scale

Goal: systems that can BOTH perceive and reason, with interpretable, verifiable outputs.

### Core Architecture Taxonomy

| Type | Description | Example |
|------|-------------|---------|
| Sequential | Neural produces symbolic; symbolic reasons | Scene graph → logic query |
| Cooperative | Neural and symbolic iterate, improving each other | AlphaGeometry LM + deducer |
| Compiled | Symbolic knowledge embedded as differentiable constraints | Logic Tensor Networks (LTN) |
| Concurrent | Parallel neural+symbolic with joint loss | DeepProbLog |

---

## Five Main Paradigms

### A. Neural-Symbolic Integration
LLMs augmented with formal solvers, constraint reasoners, or knowledge graphs.
Examples: Logic-LM, SatLM (NL → FOL → solver feedback), NeSyGPT (Answer Set Programming).

### B. Logic Tensor Networks (LTN)
First-order predicate logic grounded as differentiable real-valued tensors.
Fuzzy logic operators make logical computation differentiable. Logic = loss function.
- **GitHub:** https://github.com/logictensornetworks/logictensornetworks
- **pip:** `pip install ltn` (TensorFlow 2), `pip install LTNtorch` (PyTorch)

### C. Neuro-Symbolic Concept Learner (NS-CL)
Learns visual concepts, words, and semantic parsing jointly without explicit supervision.
(ICLR 2019, MIT-IBM). Neural perception + symbolic reasoning programs.
- 2024 extension: arXiv:2403.00323 (softened, gradient-friendly symbol grounding)

### D. Differentiable Programming
Symbolic logic (temporal, LTL, ASP, Datalog) embedded into differentiable objectives.
Key tool: Scallop (Datalog-based, ACM PLDI 2023) — https://github.com/scallop-lang/scallop

### E. Probabilistic Logic Networks
Neural predicates inside logic programs. Neural outputs as probability distributions in
Prolog programs. KU Leuven. DeepProbLog — https://github.com/ML-KULeuven/deepproblog

---

## Key Papers 2023-2026

### Theorem Proving and Formal Mathematics

#### AlphaGeometry (Google DeepMind, Nature 2024)
- Neural LM proposes auxiliary constructions; symbolic Horn-clause deduction engine proves.
  Trained on 100M synthetically generated geometry theorems.
- **Metrics:** 25/30 IMO geometry problems (2000-2022) vs 10/30 prior best. 54% solve rate overall.

#### AlphaGeometry2 (Google DeepMind)
- **arXiv:** 2502.03544 | 2025
- Extends to handle object movements, linear equations of angles/ratios/distances.
  Gemini architecture for LM; novel knowledge-sharing between search trees; 10x more synthetic data.
- **Metrics:** 84% solve rate on IMO 2000-2024 (+30pp vs AG1). Silver medal equivalent at IMO 2024.
- **GitHub:** https://github.com/google-deepmind/alphageometry2

#### Forethought — NeSy Code Verification
- **arXiv:** 2607.04096 | Jul 2026
- ~30% accuracy gain, 3 orders of magnitude less compute than frontier models.
  PAL-style: LLM generates proof steps, symbolic verifier checks each step.

#### Aria Code Agent Verification
- **arXiv:** 2607.06341 | Jul 2026 (Claude Code)
- Verified 4,257/4,257 Iris formal lemmas via harness → soundness gate pattern.
  Key pattern: LLM generates candidate → formal verifier provides binary pass/fail → loop.

#### seL4 Proof Generation (NJU / ETH, OSDI 2026)
- **arXiv:** 2603.19715 | OSDI 2026
- LLM generates seL4 (formally verified microkernel) theorems. 77.6% success on seL4 theorems.

### Robot Planning and Embodied AI

#### VisualPredicator (MIT / Cambridge / Cornell)
- **arXiv:** 2410.23156 | ICLR 2025 Spotlight
- Neuro-Symbolic Predicates implemented by neural networks with symbolic semantics.
  Online algorithm invents predicates from raw visual observations, builds abstract world models.
- **Metrics:** Better sample complexity than hierarchical RL; stronger OOD generalization than VLM planning.

#### SPARK — Training-Free Robot Behavior Trees
- **arXiv:** 2606.30613 | 2026
- Single Gemini call composes a typed behavior tree of control primitives.
  Second call uses alternative text prompts; SAM3 evaluates detection confidence; recovery loop retries.
- **Metrics:** 43.7% on LIBERO-PRO vs 18.2% CaP-Agent0 baseline (>2x). 68% avg across 3 robot families.

#### BioProAgent — FSM-Constrained Planning
- **arXiv:** 2603.00876 | ACL 2026 Oral | PKU
- Finite state machine constrains agent planning loop. Design → verify → rectify cycle.
- **Metrics:** 95.6% task success vs 21.0% baseline; 6x token reduction.

### Knowledge Graph Reasoning

#### Neural-Symbolic KG Reasoning Survey
- **ACM TKDD 2024** | DOI:10.1145/3686806
- Hybrid methods consistently outperform pure neural or pure symbolic on FB15K-237, WN18RR.

#### SciAtlas — Scientific Knowledge Graph
- **arXiv:** 2605.22878 | 2026 | Zhejiang University
- 43M papers, 26 disciplines, 157M entities, 3B triplets.
  NeSy retrieval: tri-path collaborative recall + graph reranking for scientific discovery.

### LLM Verification and Critique

#### LLM-as-a-Verifier (Stanford / UCB)
- **arXiv:** 2607.05391 | Jul 2026
- Structured LLM-based verification pipeline. SWE-Bench SOTA: 78.2%.
  Multi-criterion scoring with decomposed verification prompts.

#### SCOPE — Subgoal Critique for Code
- **arXiv:** 2607.05810 | Jul 2026 | Vanderbilt
- Subgoal-based critique decomposes code task into verifiable sub-goals before full solution.
- **Metrics:** 39.4% LiveCodeBench vs 36.6% Reflexion.

#### LLM-as-a-Verifier Criterion Prompt Pattern
```
Given the following criterion: [CRITERION]
Evaluate the solution on a scale of 0-1.
Criterion: Does the solution [SPECIFIC VERIFIABLE PROPERTY]?
Score: 0 = completely fails, 0.5 = partially, 1 = fully satisfies
Explanation: [brief justification]
```
Aggregate scores across N criteria. Scope to specific, falsifiable properties.

### Constrained Generation

#### CDC — Constrained Diffusion for Code (UVA)
- **arXiv:** 2605.16829 | 2026
- Training-free constrained generation for code. Compatible with any code LLM.

#### NeSyCR — Cross-Domain Code Synthesis (CVPR 2026, SKK University)
- **arXiv:** 2603.18495 | CVPR 2026
- Counterfactual check pattern: generate candidate, ask "what would need to change for this
  to be wrong?" as a validity cross-check.
- **Metrics:** +31.14% task success on cross-domain code synthesis.

#### Compact Constraint Headers (Tang)
- **arXiv:** 2604.07192 | 2026
- Compact schema/constraint representation for FSM-constrained agents.
- **Metrics:** 71% token reduction with no loss in constraint satisfaction rate.

### Clinical and Domain Applications

#### AlphaNeSy-CTM — Clinical Trial Matching
- **arXiv:** 2606.20895 | 2026
- NeSy approach to clinical trial eligibility: symbolic eligibility criteria + neural matching.
- **Metrics:** +30% improvement on clinical trial matching benchmarks.

#### CRISTAL — Bayesian Few-Shot Classification
- **arXiv:** 2606.29799 | 2026
- Bayes-optimal performance at 5 examples. Frontier LLMs plateau at 40 examples.

---

## Production-Ready NeSy Frameworks

| Framework | GitHub | Stars | Last Commit | pip install | Notes |
|-----------|--------|-------|-------------|-------------|-------|
| Outlines | dottxt-ai/outlines | 14,500 | Jul 2026 (daily) | `pip install outlines` | Grammar-constrained LLM generation; used in vLLM/Ollama |
| SymbolicAI | ExtensityAI/symbolicai | 1,700 | Jun 2026 | `pip install symbolicai` | NeSy LLM orchestration + Lean4 formal verification |
| SynaLinks | SynaLinks/synalinks | 446 | Jul 2026 (daily) | `pip install synalinks` | Keras-inspired NeSy LM; graph RAG, in-context RL, Text2SQL |
| PyReason | lab-v2/pyreason | 344 | May 2026 | `pip install pyreason` | Graph temporal logic; NumPy/Numba parallel inference |
| z3-solver | Z3Prover/z3 | — | Active | `pip install z3-solver` | SMT solver; fully working on Python 3.14 |

### Research Frameworks

| Framework | Notes |
|-----------|-------|
| DeepProbLog | `pip install deepproblog` — needs SWI-Prolog < 9.0 for approx inference |
| LTNtorch | `pip install LTNtorch` — PyTorch version of Logic Tensor Networks |
| Scallop | Build from source (Rust nightly); Differentiable Datalog; PLDI 2023 |
| mOWL | `pip install mowl-borg` — ML with OWL ontologies |

### LLM + Symbolic Integration Patterns (ranked by practicality)

1. **Grammar-constrained decoding** (Outlines): symbolic grammar masks logits at inference time. Most production-ready.
2. **PAL / Program-Aided LMs**: LLM writes Python → Python interpreter executes → answer. No extra library needed.
3. **Text2SQL / Text2Cypher**: LLM generates structured query → DB executes. Most-deployed NeSy in enterprise.
4. **Symbolic feedback loop**: LLM generates code → pytest/mypy/Z3 runs → result fed back. Standard agentic coding pattern.
5. **LLM → Z3 constraints**: LLM generates SMT constraints; Z3 verifies/finds solution. Good for spec verification.
6. **RAG as symbolic memory**: vector DB + knowledge graph = symbolic retrieval layer for LLM reasoning.

---

## Local Implementation (nesy.py)

File: `~/Documents/neurosymbolic/nesy.py`
All 6 classes verified with Python 3.14.6.

| Class | Basis | Key Methods |
|-------|-------|-------------|
| `SymbolicVerifier` | Z3 SMT solver | `make_int/bool`, `check_integer_constraints`, `verify_postcondition` |
| `GraphReasoner` | networkx forward-chaining | `load_from_llm_output`, `risk_report` |
| `ConstrainedOutput` | Pydantic + PAL | `validate(data, Schema)`, `execute_pal(code)` |
| `CodingVerifier` | Forethought+Progent+SkillOpt | `run_pal`, `verify_spec`, `audit_dependencies`, `score_code_change` |
| `LLMVerifier` | LLM-as-a-Verifier 2607.05391 | `build_criterion_prompt`, `aggregate_scores`, `scope_critique_prompt`, `memharness_decompose` |
| `FSMAgent` | BioProAgent 2603.00876 | `design_verify_rectify()`, `read_verify_write()`, `compact_schema_prompt` |

---

## Non-English Research Findings

| Language | Status | Key Finding |
|----------|--------|-------------|
| Chinese | Found | Robust Abductive Learning (Li Yufeng, Nanjing University); KG+LLM bidirectional roadmap (Wu Xindong) |
| Japanese | Found | IPSJ 2024: Toulmin + KG debate partner; MUSUBIX Z3 for software requirements (Qiita) |
| Korean | Gap | No independent native-language NeSy research found — confirmed genuine gap |
| Russian | Partial | RAS/SPIIRAS 2023: ontology-oriented NeSy for collaborative decision support (RSF grant) |
| French | Found | CORIA-TALN 2026: causal NeSy agent; Prevyo MR4AP (defense-funded) |
| German | Found | UDE ClassicLogic benchmark; TIB/Leibniz OAKG HITL (4hr → 24min literature review) |

---

## Research Gaps (from arXiv:2501.05435 systematic review, 1,428 papers)

- Explainability: 28% of papers address — largest single gap
- Meta-cognition: 5% — almost no work
- Symbol grounding does not imply compositional generalization (iLTN finding: arXiv:2604.26521)
- LLM hallucination in symbolic pipelines
- Counterfactual reasoning
- Korean NeSy research: confirmed gap — no native-language work found

---

## Source Reference Table

| Paper | arXiv / DOI | Venue | Year |
|-------|-------------|-------|------|
| NeSy AI Survey | 2501.05435 | — | 2025 |
| NeSy for LLM Reasoning (IJCAI survey) | 2508.13678 | IJCAI 2025 | 2025 |
| AlphaGeometry | — | Nature 2024 | 2024 |
| AlphaGeometry2 | 2502.03544 | — | 2025 |
| VisualPredicator | 2410.23156 | ICLR 2025 Spotlight | 2024 |
| CaMeL | 2503.18813 | — | 2025 |
| Progent | 2504.11703 | — | 2025 |
| BioProAgent | 2603.00876 | ACL 2026 Oral | 2026 |
| Compact headers | 2604.07192 | — | 2026 |
| NeSyCR | 2603.18495 | CVPR 2026 | 2026 |
| SPARK | 2606.30613 | — | 2026 |
| iLTN | 2604.26521 | — | 2026 |
| CRISTAL | 2606.29799 | — | 2026 |
| alphaNeSy-CTM | 2606.20895 | — | 2026 |
| DeepLog (KU Leuven) | 2605.10279 | IJCAI | 2026 |
| seL4 proof gen | 2603.19715 | OSDI 2026 | 2026 |
| Forethought | 2607.04096 | — | 2026 |
| LLM-as-a-Verifier | 2607.05391 | — | 2026 |
| Aria code agent | 2607.06341 | — | 2026 |
| SCOPE | 2607.05810 | — | 2026 |
| CDC | 2605.16829 | — | 2026 |
| Scallop | DOI:10.1145/3591280 | ACM PLDI 2023 | 2023 |
| KG Reasoning Survey | DOI:10.1145/3686806 | ACM TKDD 2024 | 2024 |
