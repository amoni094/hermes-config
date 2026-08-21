# Executive Memo Writing — Research Synthesis
**Date:** 2026-08-21 (v1.1 updated 2026-08-21 — SearXNG research pass 2)
**Purpose:** Evidence base for the `exec-memo-writing` Hermes skill.
**Scope:** Academic literature, practitioner frameworks, plain-language policy, GitHub tooling, social signals.

---

## 1. The Problem This Skill Solves

Executives read under time pressure. Research on managerial attention (Mintzberg 1973; Kahneman 2011) consistently shows that senior readers:
- Scan before they read — they decide in 15–30 seconds whether a document deserves deeper attention.
- Anchor on the first strong claim — if it's buried, the memo fails regardless of content quality.
- Mentally penalise jargon, long paragraphs, and passive voice as signals of unclear thinking.
- Process visual hierarchy (headers, white space, bullets) before prose.

A two-page limit is not arbitrary: it matches the natural scan-depth of one printed sheet front-and-back or one scrollless screen. Beyond that, reading becomes effortful; executives either delegate or skim and miss nuance.

---

## 2. Structural Frameworks — Synthesis

### 2a. Barbara Minto — Pyramid Principle (1987, 2nd ed. 1996)
**Core claim:** Begin with the answer (conclusion/recommendation), then support it with grouped, mutually exclusive, collectively exhaustive (MECE) arguments. Arguments should be in parallel logical form.

**Strengths:**
- Forces the writer to know their conclusion before writing — eliminates "thinking on paper."
- MECE grouping reveals gaps in reasoning.
- Widely taught at McKinsey, BCG, and top MBA programs; executives trained in this tradition expect it.

**Known weaknesses (practitioner critique, 2020s):**
- Pyramid can feel cold/mechanical for politically sensitive topics — recommendation-first can close minds before context is established.
- Strictly MECE groupings sometimes destroy narrative flow and feel artificial to non-consulting audiences.
- Doesn't handle uncertainty well — forces a recommendation even when "we don't know yet" is the honest answer.
- Cultural mismatch: East Asian, Southern European, and many public-sector contexts expect context-before-conclusion (inductive structure). Minto is deductive-first.
- Falls short for decision consultants under genuine uncertainty: alternatives generation and alternatives framing is a documented gap (Google Scholar, "Some Assembly Required," "Communicating analytic results").

**Verdict:** Use Minto as the default spine for most internal corporate memos. Modify or invert when: (a) audience is culturally inductive, (b) the topic is politically charged and the recommendation needs to land softly, or (c) uncertainty is genuine and the memo's purpose is to frame options not advocate.

**SCQ variant (Situation-Complication-Question):** A lesser-known Minto extension. Adds an explicit "complication" bridge between situation and recommendation — useful when the trigger is a changed condition (cost spike, new regulation, competitive move) that creates the urgency for action. Structure: Situation (the stable baseline) → Complication (what changed/went wrong) → Question (what should we do?) → Answer (recommendation). More natural narrative arc than pure deductive pyramid; recommended for memos triggered by a discrete event.

### 2b. BLUF — Bottom Line Up Front (US Military origin, widely adopted)
**Core claim:** First sentence = the single most important thing the reader must know or do. Everything after is support.

BLUF is more radical than Minto — it collapses the governing thought into one sentence, not a section. It's the dominant convention in US military, intelligence community, and increasingly in tech (Amazon, Stripe internal culture).

**Practical form:**
```
BLUF: [Action required / decision needed / key finding] — [deadline or stake if applicable].
```

**Strengths over pure Minto:**
- Survives partial reading (executive reads one sentence and delegates correctly).
- Forces writer to name the ask explicitly — no ambiguity about why the memo exists.
- Works in email subject lines and Slack previews (modern delivery channel parity).

**Weakness:**
- Pure BLUF with no context reads as brusque; may alienate readers who expect framing.
- Poor fit for "FYI" informational memos where there is no actionable bottom line.

### 2c. Inverted Pyramid (Journalism tradition; US Federal Plain Language Guidelines)
Like BLUF but applied to every paragraph: most important claim first, supporting detail after. The US Plain Language Act (2010) mandates this structure for federal documents; plainlanguage.gov codifies it in their federal writing guidelines.

Key principles from plainlanguage.gov:
- One idea per sentence. Short sentences (aim ≤25 words).
- Active voice, not passive.
- Concrete nouns and strong verbs — cut nominalizations ("make a decision" → "decide").
- Headers as signposts, not decorations.

### 2d. SitRep / SBAR (Situation-Background-Assessment-Recommendation)
Originated in clinical medicine (IHI), now common in **healthcare ops, risk teams, and safety-critical contexts**. Scope note: literature search confirms SBAR has limited diffusion into general business executive writing — it is primarily a crisis/clinical/risk tool, not a general-purpose memo structure.

Maps naturally to executive memos in those specific contexts:

| SBAR Component | Memo Equivalent |
|---|---|
| Situation | What is happening / the issue |
| Background | Why it matters / context |
| Assessment | What it means / analysis |
| Recommendation | What to do |

SBAR preserves the narrative arc that Minto can strip out. Strong for: incident reports, outage communications, safety/risk escalations, and healthcare-adjacent executive briefings. **Do not use SBAR as the default for standard strategy or operational memos** — executives without clinical or military backgrounds find the rigid 4-section label structure mechanical.

### 2e. Amazon's "6-pager", PR/FAQ, and Narrative Prose tradition
Amazon famously banned PowerPoint in favour of narrative memos read in silence at the start of meetings. Key insight: prose forces reasoning coherence that bullets hide. Fragmented bullet lists can conceal weak logic. Bezos: "Writing a good 4-page memo is harder than writing a 20-slide deck — the act of writing forces you to think clearly." (Quartr/Amazon writing culture, updated Sep 2025)

**Two distinct formats in Amazon's system:**
- **6-pager (operational/strategy memo):** Narrative prose, ~6 pages, covers problem → context → options → recommendation → metrics. Not practical for the 2-page executive brief format this skill targets.
- **PR/FAQ (press release + FAQ):** Forward-looking format for product/innovation decisions. Starts with a hypothetical press release for the finished product, then answers likely customer/stakeholder FAQs. Forces teams to think from the customer's perspective before committing resources. Useful as a variant when the memo's purpose is a **go/no-go on a new product or initiative.**

**Relevant takeaway for short memos:**
- Don't use bullets to avoid writing a sentence. If a point is important, write it as a sentence with a verb.
- Use bullets only for truly enumerable, parallel items (e.g., list of affected systems, list of required approvers).
- A 2-page memo should have mostly prose with strategic use of bullets, not a bullet-point dump.

### 2f. Chip Heath / Made to Stick — Cognitive stickiness
SUCCESs framework (Simple, Unexpected, Concrete, Credible, Emotional, Story) is less about structure and more about why information sticks. Relevant for executive memo:
- **Concrete over abstract**: "Revenue impact: $4.2M in Q3" beats "significant financial exposure."
- **Unexpected**: Lead with the counter-intuitive or surprising finding — it arrests scanning.
- **Credible**: Numbers, named sources, or testable claims. Avoid weasel words.

---

## 3. Writing Style — Research-Backed Principles

### Sentence length and readability
- Flesch-Kincaid research (original 1975; validated repeatedly): sentences >25 words sharply reduce comprehension under time pressure.
- Target: 15–20 words average for executive documents. Use longer sentences sparingly for nuance, shorter ones for emphasis.
- Fog Index target for senior exec memos: 12–14 (college-level, not grad-school).

### Active voice
- Active voice is ~30% faster to read (Charrow & Charrow 1979, legal writing studies; confirmed in technical writing literature).
- Rule: Subject acts. "The board approved X" not "X was approved by the board."
- Exception: use passive when the actor is unknown, irrelevant, or politically awkward to name.

### Nominalizations (zombie nouns)
Helen Sword's research (2012, "Stylish Academic Writing") quantifies how nominalizations ("utilization," "implementation," "consideration") bloat sentences and reduce impact.
- Cut: make a decision → decide; provide assistance → help; in the event that → if.
- Replace process nouns with verbs wherever possible.

**New finding (v1.1):** Nominal style (noun-heavy writing, even when grammatically active) is rated as harder to read AND less interesting by readers — Sword and subsequent cognitive load research confirm that noun-heavy style reduces engagement independent of sentence length. This matters for executive memos where interest and persuasion are goals, not just information transfer. An executive who is bored by the writing will anchor on form over content.

### Paragraph structure
- First sentence of every paragraph = its most important claim (inverted pyramid at paragraph level).
- One topic per paragraph. Max 4–5 sentences.
- No paragraph longer than 6 lines in a 2-page memo.

### Numbers and evidence
- Quantify every claim that can be quantified. "Costs have risen significantly" → "Costs up 18% YoY, $3.2M over budget."
- Cite the source inline briefly: "(Q2 Finance Report)" not a footnote — footnotes break reading flow in short documents.
- Round aggressively for strategic memos: $4.2M not $4,187,423. Precision signals over-engineering.

### Tone calibration
- Match the register to the relationship. A memo to the CEO from a direct report is different from a memo to an external regulator.
- Avoid hedging language that buries the recommendation: "It might perhaps be worth considering..." → "Recommend X."
- Confident ≠ arrogant. "The data supports X" is confident. "Obviously X" is dismissive.

---

## 4. Modern Executive Trends (2024–2026)

### Trend 1: AI-assisted pre-reading / summary layers
Executives increasingly receive AI summaries of long documents before reading them. This means:
- The top 50 words of your memo may be the AI's source for its summary.
- Front-load even more aggressively — if the first paragraph doesn't capture the essence, the AI summary will mislead.
- Use a literal "Summary:" or "BLUF:" label at the top so AI extractors anchor correctly.

### Trend 2: Asynchronous-first communication
Post-pandemic C-suite operates more asynchronously. Memos are read on phones, in transit, at odd hours. Design implications:
- Short paragraphs with line breaks between them (single-column, no dense blocks).
- Key numbers and decisions in bold — allow "bold scan" as a reading mode.
- Avoid tables wider than a phone screen (5–6 columns max, or use a compact callout box instead).

### Trend 3: Radical brevity expectation
2025 practitioner consensus (McKinsey, Deloitte internal guides; LinkedIn exec community): one-page memos are now the aspirational standard. Two pages is the outer acceptable limit. Three pages means the writer hasn't done the thinking.

### Trend 4: Scenario framing for uncertainty
Post-COVID, post-rate-shock era: executives are more comfortable with "3 scenarios" framing than with false precision. A memo that says "Base case: X | Downside: Y | Upside: Z" with a recommendation under each is often more credible than one that presents a single point estimate.

### Trend 5: Decision-forcing design
Best-in-class memos end with a forced choice: "Option A / Option B / Approve as proposed." This prevents "I'll read it later" from becoming "nothing happens." If you want a decision, design for it structurally.

### Trend 6: AI-generated memos — relational gap
A 2026 academic study ("Communicative Effectiveness and Authenticity in Business English Email Writing: Human-written vs AI-generated," 2026) found: AI-generated business communications score *higher* on task completion (clear ask, explicit action) but *lower* on relational markers — rapport, warmth, contextual sensitivity. This is a systematic bias. For executive memos where relationship context matters (board communication, politically charged topics, sensitive personnel situations), AI drafts need explicit prompting to add relational framing. Checklist item added to skill: "Is the tone appropriate for the specific relationship — not just technically correct?"

### Trend 7: Async Monday Memo (remote finance/ops teams, 2024)
Practitioner pattern gaining traction in remote-first organisations: a weekly 1-page "Monday Memo" in Notion/Confluence that replaces the Monday status meeting. Fixed structure: Last week's outcomes → This week's priorities → Blockers / decisions needed. Key design features: async-consumable (no meeting needed), bold-scan readable, decision section explicitly names owner + deadline. Relevant extension of the skill's async-first guidance — supports the argument for memo-over-meeting in distributed teams.

---

## 5. GitHub and Tooling Landscape

Surveyed GitHub for exec-memo templates, writing tools, and AI prompt repos. Key findings:

- **dair-ai/Prompt-Engineering-Guide**: covers LLM writing applications broadly; no dedicated exec memo prompt patterns.
- **GSA/plainlanguage.gov** (archived): canonical plain-language guidelines including inverted pyramid, short sentences, active voice — directly applicable. Content now at digital.gov.
- No dominant open-source exec memo template repo found; the space is fragmented across individual consultants' Notion/PDF templates.
- AI writing tools (Grammarly, Writer.com, Jasper) offer tone/clarity checks but not structural guidance — gap this skill fills.

**Relevant GitHub signals:**
- ASD-STE100 (Simplified Technical English standard) — used in aviation/defense for controlled vocabulary; principles applicable to executive writing: simple words, short sentences, one topic per paragraph.
- McKinsey-style memo templates circulate as Notion/Markdown templates in private repos but no authoritative public version.

---

## 6. Multilingual / Cross-Cultural Considerations

- **English (default):** BLUF-first, Minto pyramid, active voice, short sentences.
- **French/German business:** Expect more formal salutation, more context before conclusion; tone more formal; vous/Sie forms; hedging is culturally appropriate, not weakness.
- **Japanese/Korean/Chinese:** Strong preference for inductive structure (context → analysis → conclusion). Recommendation-first can appear arrogant or disrespectful of the reader's intelligence. Adjust: use Situation → Background → Analysis → Subtle recommendation framing.
- **Spanish/Portuguese (LatAm):** Relationship context matters; opening with acknowledgment of the relationship before business is not filler — it's trust-building. Don't strip it.
- **Arabic:** Right-to-left reading pattern affects visual scanning; deference to seniority in framing; more formal opening required.

**Practical rule:** The skill should prompt the user to specify cultural/language context and apply the appropriate structure variant.

---

## 7. Key Sources

| Source | Type | Relevance |
|---|---|---|
| Minto, B. (1987/1996). *The Pyramid Principle.* | Book | Core structural framework |
| Kahneman, D. (2011). *Thinking Fast and Slow.* | Book | Cognitive load, scanning behaviour |
| Mintzberg, H. (1973). *The Nature of Managerial Work.* | Academic | Executive time/attention research |
| US Plain Language Act (2010) + plainlanguage.gov | Policy | Plain language mandates |
| Flesch, R. (1948). *A new readability yardstick.* | Academic | Readability formula basis |
| Charrow & Charrow (1979). *Making legal language understandable.* | Academic | Active voice speed studies |
| Heath & Heath (2007). *Made to Stick.* | Book | Cognitive stickiness SUCCESs framework |
| Sword, H. (2012). *Stylish Academic Writing.* | Book | Nominalization + nominal style engagement research |
| IHI SBAR Framework | Practitioner | Situation-Background-Assessment-Recommendation (crisis/clinical only) |
| Amazon 6-pager + PR/FAQ culture (Bezos memos; Quartr Sep 2025) | Practitioner | Prose > bullets; narrative coherence; PR/FAQ variant |
| Naumova, I. (2026). *Writing a memo as part of business communication training in a foreign language.* | Academic | Multilingual memo genre analysis |
| GSA/plainlanguage.gov GitHub (archived) | Open source | Inverted pyramid, sentence length guidelines |
| ASD-STE100 (Simplified Technical English) | Standard | Controlled vocabulary, one-topic-per-sentence rules |
| "Some Assembly Required" — SCQ framework analysis | Google Scholar | SCQ variant of Minto for event-triggered memos |
| "Communicating analytic results" — Alternatives framing | Google Scholar | Pyramid weaknesses under uncertainty |
| "Building Logic into Communication Using the Minto Pyramid Principle" | Semantic Scholar | Minto validation in business communication |
| "Communicative Effectiveness and Authenticity in Business English Email Writing: Human-written vs AI-generated" (2026) | Academic | AI memo relational gap — task completion high, warmth low |
| "AI-Enhanced Cybersecurity Executive Reporting" ACM (2026) | Academic | BLUF in technical executive reporting; maturity model |
| "Leading With Effective Communication" (2025) | Book | BLUF technique formalised in leadership communication |
| "Communication Is the Key — Tips for the Judge Advocate, Staff Officer and Leader" (Army Law 2016) | Military Law | BLUF canonical definition and application |
