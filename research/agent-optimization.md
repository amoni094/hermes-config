# Agent Optimization and Efficiency — Research Findings (2024–2026)

Sources: arXiv systematic survey, academic literature sweep July 2026.
Original compiled in: ~/.hermes/skills/research/academic-literature-review/references/

---

## Skill Learning and Self-Improvement

### ExpeL — Experiential Learning Without Fine-Tuning
- **arXiv:** 2308.10144 | AAAI 2024 | Tsinghua LeapLab
- **Code:** github.com/LeapLabTHU/ExpeL
- Agent gathers experience across training tasks, extracts NL insights into a "knowledge pool."
  At inference, recalls insights + past episodes. No fine-tuning. Cross-task learning
  (unlike Reflexion which is per-episode).
- **Metrics:** Outperforms ReAct + Reflexion on HotpotQA, ALFWorld, WebArena.

### SkillOpt — Text-Space Gradient Descent for Agent Skills
- **arXiv:** 2605.23904 | May 2026 | Microsoft Research
- **Code:** aka.ms/skillopt
- Separate optimizer model converts scored rollouts into bounded add/delete/replace edits
  to skill documents. Edit accepted only on held-out validation improvement.
  Textual "learning-rate budget" + rejected-edit buffer. Zero extra inference calls at deployment.
- **Metrics:** +23.5pp (GPT-5.5 direct chat), +24.8pp (Codex agentic loop), +19.1pp (Claude Code).
  Best or tied on all 52 evaluation cells vs. human/one-shot/Trace2Skill/TextGrad/GEPA/EvoSkill.

### MetaSkill-Evolve — Two-Timescale Skill Evolution
- **arXiv:** 2607.05297 | Jul 2026
- Two-timescale: fast task-skill loop + slow meta-skill loop (improves the improvement procedure itself).
  Five API-only pipeline agents.
- **Metrics:** +23.5pp OfficeQA, +16.1pp SealQA.
- **Key insight:** Meta-improvement (improving how you improve) compounds faster than direct skill tuning.

### LatentSkill — Skill to LoRA Compilation
- **arXiv:** 2606.06087 | Jun 2026 | SJTU + Fudan
- Pretrained hypernetwork converts text skills into plug-and-play LoRA adapters. Skill knowledge
  moves from prompt tokens to weight space. Modular loading; composable via parameter arithmetic.
- **Metrics:** ALFWorld +21.4pp seen / +13.4pp unseen; 64.1% fewer prefill tokens (ALFWorld).
- **Note:** Requires fine-tunable model access — not applicable to API-only deployments.

### SkillComposer — Generative Skill Composition (Selection Order)
- **arXiv:** 2606.32025 | Jun 2026
- Formalizes composition as task-conditioned ordered-sequence prediction over skill indices.
  Which skills, how many, and what order are a joint decision — cannot be decoupled.
- **Metrics:** +23.1pp (GPT-5.2-Codex), +18.2pp (Gemini-3-Pro-Preview) over no-skill baseline.

### SkillComposer — Learning to Evolve Skills (Construction)
- **arXiv:** 2606.06079 | Jun 2026
- Decomposes skill construction into three learnable operations: create, improve, merge.
  Trained via rejection sampling. Merge and improve address orthogonal quality dimensions.
- **Metrics:** SkillComposer-4B improves a 27B executor by +4.5 on agent tasks (tau2-Bench, AppWorld).
- **Key insight:** Merge-worthiness (redundancy/overlap) and improve-worthiness (task-fit gap) are
  separate quality signals — not the same dimension.

### CoALA — Cognitive Architectures for Language Agents
- **arXiv:** 2309.02427 | TMLR 2024 | Princeton
- Modular framework: Memory (working/episodic/semantic/procedural) x Action (internal/memory/grounded)
  x Decision (one-shot/planning/execution). Procedural memory = skills. Episodic memory = main lever.

### Self-Evolving AI Agents Survey
- **arXiv:** 2508.07407 | Aug 2025
- **GitHub:** EvoAgentX/Awesome-Self-Evolving-Agents
- Unified framework: System Inputs → Agent System → Environment → Optimisers feedback loop.
  Covers prompt-level, tool-level, memory-level, architecture-level adaptation.

---

## Skill Library Management

### AgentPrune — Communication Redundancy Pruning
- **arXiv:** 2410.02506 | ICLR 2025
- Models agent message flows as a spatial-temporal message-passing graph; one-shot pruning.
  First formal definition of "communication redundancy."
- **Metrics:** 87% cost reduction; 28.1-72.8% token reduction; 3.5-10.8% accuracy boost against
  adversarial attacks.

### ToolScope — Tool Merging + Context-Aware Filtering
- **arXiv:** 2510.20036 | ACL 2026
- ToolScopeMerger: LLM audits semantic overlap, proposes merges, self-corrects via verifier.
  ToolScopeRetriever: ranks and selects top-K tools per query to stay within context window.
- **Metrics:** 8-38% gain in tool selection accuracy across 3 LLMs and 3 benchmarks.
- **Merge threshold:** cosine similarity > 0.92 between skill description embeddings.

### VOYAGER — Foundational Skill Library Architecture
- **arXiv:** 2305.16291 | NeurIPS 2023
- **Web:** voyager.minedojo.org
- Skills stored as executable code. Retrieval: embed descriptions, cosine similarity at query time,
  top-5 retrieved. Skills include self-verification steps returning binary pass/fail.

### SkillRouter — Full-Text Routing at Scale
- **arXiv:** 2603.22455 | Mar 2026
- **Code:** github.com/zhengyanzhao1997/SkillRouter
- Hiding skill body (showing only name+description) causes a 31-44pp drop in routing accuracy
  at 80K-skill scale. Full SKILL.md text is the critical routing signal, not just metadata.
- Architecture: BM25 sparse retrieval over full skill text → 1.2B dense reranker over top-100.
- **Metrics:** 74.0% Hit@1 on ~80K skills. 13x fewer params than prior SOTA; 5.8x faster.
- **Threshold:** Full-text BM25 over skill bodies sufficient at <= 500 skills. Add 1.2B reranker
  when registry grows beyond ~500.
- **Reject option:** if top-1 retrieved skill scores < 0.65 cosine similarity, do not inject any
  skill — let the LLM reason unaided.

### Four-Tier Pruning Decision Matrix
| Tier | Condition | Action |
|------|-----------|--------|
| Archive | Zero invocations 90d AND semantic substitute exists (cos > 0.80) | Disable |
| ACTIVE_DORMANT | Zero invocations BUT no semantic substitute | Preserve with keyword triggers |
| Merge | Two skills with cos_sim > 0.92 on descriptions | LLM-audited merge proposal |
| Delete | Semantic duplicate exists AND outcome-weighted usage is negative | Hard delete |

**Guard:** never disable a skill if no substitute exists with cos_sim > 0.80.

### Agent Skills Survey — Four-Stage Lifecycle
- **arXiv:** 2605.07358 | May 2026
- **GitHub:** JayLZhou/Awesome-Agent-Skills
- Canonical stages: Representation → Acquisition → Retrieval → Evolution.
  Open challenges: quality control, interoperability, safe updating, long-term management.

### Agent Skills Architecture + Security Survey
- **arXiv:** 2602.12430 | AgentSkills'26 Workshop
- 26.1% of community-contributed skills contain vulnerabilities.
  Proposes four-tier gate-based permission model mapping skill provenance to deployment caps.

### SkillsBench — Empirical Quality Findings
- **arXiv:** 2602.12670 | Feb 2026
- **Web:** www.skillsbench.ai
- 87 tasks, 8 domains, 18 model-harness configurations.
- Skills raise average pass rate 33.9% → 50.5% (+16.6pp).
- Focused skills with <= 3 modules outperform larger/exhaustive bundles.
- Smaller models + skills can match larger models without skills.

### SkillRevise — Trace-Conditioned Skill Revision
- **arXiv:** 2606.01139 | May 2026
- Diagnoses skill defects from execution evidence, retrieves repair principles from memory bank,
  applies execution-anchored edits.
- **Metrics:** Raises success rate 36% → 62% on SkillsBench.

### SkillsVote — Evidence-Gated Lifecycle Governance
- **arXiv:** 2605.18401 | May 2026
- Profiles skills for quality, verifiability, and environment requirements.
  Evidence-gated resurrection: only re-enable disabled skill when active set fails AND disabled
  skill matches the failing task (cosine > 0.70).

### Self-Organizing Skill Hierarchies ("Drop the Hierarchy")
- **arXiv:** 2603.28990 | Mar 2026
- 25,000-task experiment across 8 models, 4-256 agents, 8 coordination protocols.
  Agents given only mission + communication protocol spontaneously formed better structures
  than pre-designed hierarchies. Produced 5,006 unique emergent roles from just 8 agents.
- **Implication:** LLM-induced re-clustering (monthly) beats static curator-imposed categories.

### Composite Skill Quality Score
```
Q = 0.35 * task_success_rate
  + 0.25 * (1 - user_correction_rate)
  + 0.20 * routing_precision          # how often retrieved skill was actually used
  + 0.10 * (1 / max(module_count, 1)) # brevity bonus: <= 3 modules is ideal
  + 0.10 * recency_decay              # decays with days since last invocation
```
Skills with Q < 0.3 → surface for curator review.

---

## Harness Design

### TTHE — Test-Time Harness Evolution
- **arXiv:** 2607.08124 | Jul 2026 | HKBU / Imperial
- Test-time harness evolution from unlabeled execution traces; no gold labels.
- **Metrics:** Persistent improvement across SQL / code / tool-use benchmarks.

### Rethinking Harness Evaluation
- **arXiv:** 2607.12227 | Jul 2026 | UW / Allen Institute
- Harness evolution does not consistently beat a matched test-time-search baseline.
  Benchmark overfitting is real.
- **Warning:** Measure harness improvements against TTS baseline, not just no-harness baseline.

### MemoHarness (Notre Dame)
- **arXiv:** 2607.14159 | Jul 2026
- 6-dimensional harness decomposition:
  context / tools / orchestration / memory / decoding / output_handling.
  Dual-layer experience bank. Selective transfer to unseen evaluation suites.

### PreAct — Compile Runs to State Machines
- **arXiv:** 2606.17929 | Jun 2026 | 19PINE-AI
- Compile successful agent runs to state machines; replay without LLM on repeat tasks.
- **Metrics:** 8.5-13x speedup on repeated task types.
- **Application:** Extract deterministic playbooks from successful agentic trajectories.

---

## Observability and Tracing

### AgentOps — DevOps-Mapped Observability Taxonomy
- **arXiv:** 2411.05285 | Nov 2024 | CSIRO
- Systematic mapping study → comprehensive taxonomy.
  What to trace: decision traces, tool call logs, memory state snapshots, planning steps, feedback signals.
  When: per-turn, per-episode, cross-session.
  What to alert on: anomalies, cost overruns, plan deviations, safety violations.

### AgentTrace — Three-Surface Structured Logging
- **arXiv:** 2602.10133 | Feb 2026
- Three trace surfaces:
  (1) Operational (method-level execution)
  (2) Cognitive (LLM interaction introspection)
  (3) Contextual (external system I/O)
- Core schema: L(S:E:C) → R with four properties: consistency, causality, fidelity, interoperability.
  Runtime instrumentation with minimal overhead; OpenTelemetry export; JSONL logs.

---

## Source Reference Table

| Paper | arXiv ID | Venue | Year |
|-------|---------|-------|------|
| ExpeL | 2308.10144 | AAAI 2024 | 2023 |
| CoALA | 2309.02427 | TMLR 2024 | 2023 |
| AgentPrune | 2410.02506 | ICLR 2025 | 2024 |
| Self-Evolving Survey | 2508.07407 | — | 2025 |
| ToolScope | 2510.20036 | ACL 2026 | 2025 |
| SkillOpt | 2605.23904 | — | 2026 |
| SkillRevise | 2606.01139 | — | 2026 |
| LatentSkill | 2606.06087 | — | 2026 |
| SkillComposer (evolution) | 2606.06079 | — | 2026 |
| PreAct | 2606.17929 | — | 2026 |
| SkillComposer (selection) | 2606.32025 | — | 2026 |
| TTHE | 2607.08124 | — | 2026 |
| MemoHarness | 2607.14159 | — | 2026 |
| SkillRouter | 2603.22455 | — | 2026 |
| Drop the Hierarchy | 2603.28990 | — | 2026 |
| Agent Skills Survey | 2605.07358 | — | 2026 |
| SkillsVote | 2605.18401 | — | 2026 |
| SkillsBench | 2602.12670 | — | 2026 |
| MetaSkill-Evolve | 2607.05297 | — | 2026 |
| AgentOps | 2411.05285 | — | 2024 |
| AgentTrace | 2602.10133 | — | 2026 |
