# Multi-Agent Workflows — Research Findings (2024–2026)

Sources: arXiv systematic survey, academic literature sweep July 2026.
Original compiled in skill references under autonomous-ai-agents/ and harness-first-agent-design/

---

## Coordination Topology

### MetaGPT — SOP-Encoded Multi-Agent Collaboration
- **arXiv:** 2308.00352 | ICLR 2024 Oral (No. 1 LLM-based Agent paper)
- Human SOPs encoded into prompt sequences. Specialized role agents (Architect, PM, Engineer, QA)
  collaborate with structured handoffs and artifact validation. MetaGPT X (MGX) launched Feb 2025.

### AgentPrune — One-Shot Communication Graph Pruning
- **arXiv:** 2410.02506 | ICLR 2025
- First paper to formally define "communication redundancy." Models interaction as
  spatial-temporal message-passing graph; one-shot pruning removes redundant edges.
  Integrates into AutoGen, MetaGPT, LangGraph.
- **Metrics:** $5.6 vs. $43.7 for comparable topologies (87% cost reduction);
  28.1-72.8% token reduction; 3.5-10.8% accuracy boost against adversarial attacks.

### DyTopo — Dynamic Topology Routing via Semantic Matching
- **arXiv:** 2602.06039 | Feb 2026
- Manager-guided framework reconstructing sparse directed communication graph per round
  (vs. AgentPrune's one-shot). Each agent outputs lightweight need/key descriptors;
  DyTopo embeds and semantically matches to route private messages only along induced edges.
- **Metrics:** avg. +6.2 over strongest baseline; works across 4 LLM backbones.
- **vs AgentPrune:** DyTopo is per-round (evolving) vs one-shot (fixed); best for multi-round
  reasoning vs batch processing.

### MAS-PromptBench — Prompt Optimization in Multi-Agent Systems
- **arXiv:** 2606.23664 | Jun 2026
- **Code:** github.com/juyangbai/MAS-PromptBench
- Systematic study of system-prompt optimization across diverse MAS setups.
- **Critical finding:** +24.0pp best case, -16.0pp worst case. Outcomes depend heavily on
  task type + communication structure + team size.
- **Warning:** Single-agent prompt optimization does NOT transfer to MAS.

### MACE — Structured Peer-Selection POSG for Agent Coordination
- **arXiv:** 2607.11250 | Jul 2026
- Structured peer-selection using Partially Observable Stochastic Games for capability inference.
  Value of exploration scales with agent diversity.
- **Metrics:** Substantially improves coordination on complex multi-agent tasks.

### Drop the Hierarchy — Emergent Agent Structures
- **arXiv:** 2603.28990 | Mar 2026
- 25,000-task experiment across 8 models, 4-256 agents, 8 coordination protocols.
  Agents spontaneously formed better structures than pre-designed hierarchies.
  Produced 5,006 unique emergent roles from just 8 agents given only mission + communication protocol.
- **Finding:** Monthly LLM-induced taxonomy re-clustering beats static categories.

---

## Safety and Transaction Integrity

### Mnemosyne / ATP — Transaction-Safe Agent Workflows
- **arXiv:** 2607.00269 | Jul 2026
- LLM proposals admitted only if they pass constraint set C. Append-only log. Local repair.
- **Metrics:** < 6% overhead; ~10x fewer repair operations; 0 invalid commits.
- **Application:** Wrap any irreversible LLM agent action (db write, email send, file mutation)
  in a constraint-validation layer before execution.

### PreAct — Compile Runs to State Machines
- **arXiv:** 2606.17929 | Jun 2026 | 19PINE-AI
- Compile successful agent runs to deterministic state machines; replay without LLM on repeat tasks.
- **Metrics:** 8.5-13x speedup on repeated task types.
- **Application:** After any successful complex agentic run, extract the state machine as a
  reusable playbook for identical future tasks.

### Latent Agents — Internalize Multi-Agent Debate
- **arXiv:** 2604.24881 | ACL 2026
- Fine-tune multi-agent debate into single LLM; dynamic reward + length clipping.
- **Metrics:** 93% token reduction vs explicit debate.
- **Note:** Requires fine-tuning — low feasibility for API-only deployments.

---

## Security for Multi-Agent Systems

### CaMeL — Defeating Prompt Injections by Design
- **arXiv:** 2503.18813 | Mar 2025 | Google DeepMind
- Creates a system layer extracting control+data flows from trusted user query.
  Untrusted data (web content, tool results) tagged/tainted — can never affect control flow.
  Capability-based tool permission enforcement: data objects carry permissions of their retrieval context.
- **Metrics:** 77% task success on AgentDojo (injection-heavy) with provable security.
  Baseline agents achieve ~0% on same tasks.

### Progent — Privilege Control via Symbolic Policy + SMT Solver
- **arXiv:** 2504.11703 | Apr 2025 (v3: May 2026) | UC Berkeley, Dawn Song
- LLM auto-generates symbolic security policy (tool names + argument rules) from user task at
  session start. Every tool call deterministically checked. SMT solver classifies updates as
  narrowing (auto-applied) or expansion (requires approval).
  **Monotonic confinement:** action space can only shrink without approval.
  Validated on LangChain + OpenAI Agents SDK.

### Aethelgard — Learned Capability Governance
- **arXiv:** 2604.11839 | Apr 2026 | NeurIPS 2026 Agent Safety Workshop
- **Code:** github.com/sidikbro/aethelgard
- Four layers:
  1. Capability Governor (dynamically scopes which tools agent knows about per session)
  2. RL Learning Policy (PPO on audit logs to learn minimum viable skill set per task type)
  3. Safety Router (hybrid rule-based + fine-tuned classifier intercepts tool calls)
  4. Audit Log (feeds Layer 2 training)
- **Metrics:** Identifies 15x capability overprovisioning in production runtimes.

### MiniScope — Mobile-Style Least-Privilege for Tool Authorization
- **Source:** Semantic Scholar preprint
- Automatically reconstructs permission hierarchies reflecting relationships among tool calls.
  Mobile-style model: grant per-session, not globally. Reduces blast radius from unreliable LLMs.

### Sandboxing Landscape (2026 practitioner study)
- 82% of tested MCP servers vulnerable to path traversal when filesystem not path-scoped.
- Dominant attack vector: prompt injection → exfiltration via tool arguments.
- Isolation substrates: gVisor (~15% overhead), Firecracker (~5ms startup), Kata Containers (~30ms),
  WASM/WASI (minimal, memory isolation).

### FARMA / SENTINEL — Memory Poisoning Attack and Defense
- **arXiv:** 2607.05029 | Jul 2026 | Penn State
- FARMA poisons reasoning traces via self-referential reinforcement (beats consensus defense).
  SENTINEL: 5 structural signals on reasoning provenance. 0% attack success rate vs 100% baseline.

### GhostWriter / AM-Sentry — Tool-Injection Memory Attack
- **arXiv:** 2607.06595 | Jul 2026 | New Mexico State
- Two-phase injection+activation via tool-using agents.
  AM-Sentry: write-policy + retrieve-screen defense stops ~98% injection rate baseline.

---

## Scientific Research Multi-Agent Workflows

### InternAgent — Autonomous Scientific Research (Shanghai AI Lab)
- **arXiv:** 2505.16938 | May 2025
- **Code:** github.com/Alpha-Innovator/InternAgent
- Unified closed-loop multi-agent framework for Autonomous Scientific Research (ASR):
  hypothesis → experiment → verification → iteration. Human expert feedback loop integrated mid-process.
- **Metrics:** Reaction yield 27.6% → 35.4% (12h); Enhancer activity 0.65 → 0.79 (4h);
  2D segmentation 78.8% → 81.0% (30h). Demonstrated across 12 scientific domains.

### AgentBench + AgentRL (Tsinghua THUDM)
- **arXiv:** 2308.03688 | Updated Oct 2025
- Multi-environment benchmark (8 environments). Now integrates AgentRL for end-to-end
  multitask multi-turn RL training — closes the eval-training loop.

---

## Key Role Patterns in Production MAS

### Role Pipeline Pattern (from OpenDev / real deployments)
- Architect: high-level design + constraint specification
- PM / Planner: task decomposition + sequencing
- Engineer / Worker: bounded implementation within constraints
- Reviewer / Critic: adversarial verification, not rubber-stamp
- QA / Verifier: deterministic gates (tests, linter, schema checks)

**Key discipline:** Each role receives only the artifacts it needs, not the full context.
Information minimization reduces cross-role contamination and cuts token cost.

### Sentinel-Tag Coordination Pattern
Agents tag memory entries with a sentinel string (e.g. `msg:cluster:agent-id`).
Other agents filter on that tag to receive cross-agent signals.
Memory service becomes the coordination layer with zero additional protocol infrastructure.
Source: mcp-memory-service v11.3.3 patterns.

---

## Source Reference Table

| Paper | arXiv ID | Venue | Year |
|-------|---------|-------|------|
| MetaGPT | 2308.00352 | ICLR 2024 Oral | 2023 |
| AgentBench | 2308.03688 | — | 2023 |
| CaMeL | 2503.18813 | — | 2025 |
| Progent | 2504.11703 | — | 2025 |
| InternAgent | 2505.16938 | — | 2025 |
| AgentPrune | 2410.02506 | ICLR 2025 | 2024 |
| DyTopo | 2602.06039 | — | 2026 |
| MAS-PromptBench | 2606.23664 | — | 2026 |
| Mnemosyne/ATP | 2607.00269 | — | 2026 |
| Aethelgard | 2604.11839 | — | 2026 |
| Latent Agents | 2604.24881 | ACL 2026 | 2026 |
| PreAct | 2606.17929 | — | 2026 |
| MACE | 2607.11250 | — | 2026 |
| FARMA/SENTINEL | 2607.05029 | — | 2026 |
| GhostWriter/AM-Sentry | 2607.06595 | — | 2026 |
| Drop the Hierarchy | 2603.28990 | — | 2026 |
