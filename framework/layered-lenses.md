# Layered Lenses: A Deep Reading Framework

A reusable, conversation-driven framework for deep analysis of dense philosophical, political, and theoretical texts. Works through four sequential passes, each applying a different analytical lens section-by-section.

---

## How to Use This Framework

### Starting a New Analysis

1. **Choose your text.** This framework works best with argumentative, thesis-driven texts -- essays, book chapters, political theory, philosophy, intellectual history. It is less suited to purely narrative or descriptive writing.

2. **Identify the text's natural sections.** Before any analysis, break the text into manageable chunks. Use the author's own divisions (chapters, numbered sections, subheadings) when available. If the text lacks explicit divisions, look for shifts in topic, argument, or rhetorical mode. Aim for sections of roughly 3-10 pages each. Create a simple section index:

   ```
   Section 1: [Title or description] — pages X-Y
   Section 2: [Title or description] — pages X-Y
   ...
   ```

3. **Run each pass as a separate conversation session.** Each pass is designed to be worked through in dialogue with an AI assistant (Claude). Start a new conversation for each pass, providing the text and the relevant prompts from this framework. Work through the text section by section within each pass before moving to the next.

4. **Collect outputs as you go.** Each pass produces specific artifacts. Store them in a dedicated directory structure:

   ```
   analysis/
     00-section-index.md
     01-comprehension/
       section-01-summary.md
       section-02-summary.md
       ...
       glossary.md
       open-questions.md
       argument-map.md
     02-architecture/
       structural-annotations.md
       revised-argument-map.md
     03-critical-evaluation/
       balance-sheet.md
       hidden-assumptions.md
       critical-assessment.md
     04-personal-synthesis/
       personal-annotations.md
       one-page-takeaway.md
     bridge-notes/
       bridge-01-to-02.md
       bridge-02-to-03.md
       bridge-03-to-04.md
   ```

5. **Don't skip passes or rush.** The value is cumulative. Comprehension grounds Architecture, Architecture grounds Critical Evaluation, and all three feed Personal Synthesis. Skipping ahead produces shallow results.

### Practical Tips

- You can split a single pass across multiple conversation sessions if the text is long. Just pick up where you left off.
- Keep the text accessible during each session -- quote relevant passages directly in your prompts.
- If a section is short or straightforward, you can combine it with an adjacent section. If a section is exceptionally dense, split it further.
- The prompts below are written as instructions for the AI assistant. Copy them directly into your conversation, substituting section content as needed.

---

## Pass 1: Comprehension Lens

**Core question:** What is actually being said?

**Goal:** Build an accurate, ground-level understanding of the text's content, vocabulary, and argumentative structure before interpreting or evaluating anything.

**How to run this pass:** Work through each section of the text in order. For each section, use the prompts below in sequence. Collect the outputs into the templates at the end.

---

### 1.1 Thinker Backgrounder

**Prompt (give to Claude at the start of each section):**

> I am reading [TEXT TITLE] by [AUTHOR]. I am currently on [SECTION NAME/NUMBER], which discusses [BRIEF TOPIC].
>
> Before I dig into the argument, provide a concise primer on the thinker or intellectual tradition being discussed in this section. Cover: Who were they? What are their key ideas? Why do they matter to the broader argument? What historical or intellectual context should I have in mind? Keep it brief -- just enough to follow the argument without getting lost.
>
> If multiple thinkers appear in this section, cover each one separately.

**What this produces:** A short backgrounder (3-8 sentences per thinker) that the reader can reference while working through the section.

---

### 1.2 Argument Reconstruction

**Prompt:**

> Now I want to reconstruct the argument in [SECTION NAME/NUMBER]. Here is the text of the section:
>
> [PASTE SECTION TEXT]
>
> Help me identify:
> (a) The central claim or thesis of this section -- what is the author asserting?
> (b) The key premises and evidence -- what reasons, examples, or evidence does the author offer in support?
> (c) The connection to the previous section -- how does this section build on, respond to, or pivot from what came before?
>
> If any of these are ambiguous, surface the ambiguity rather than resolving it prematurely. Present the reconstruction in structured form.

**If the reader struggles (follow-up prompt):**

> Let me try some guiding questions:
> - What sentence or passage comes closest to stating the main point?
> - What would someone who disagreed with this section object to first?
> - If you had to summarize this section in a single "because" sentence ("The author argues X because Y"), what would it be?
> - Does this section introduce a new idea, or does it develop/complicate one from earlier?

---

### 1.3 Vocabulary Check

**Prompt:**

> Review this section and surface every term that the author uses in a technical, specialized, or loaded way -- words that carry more weight than their ordinary meaning, or that the author defines (explicitly or implicitly) in a particular way. Include terms from other thinkers that the author adopts or adapts.
>
> Present them as a glossary table with three columns: the term, a plain-language definition, and a note on how the author uses it specifically in this context.

---

### 1.4 Paraphrase Test

**Prompt:**

> Now I want to test my understanding. I will restate the argument of this section in 3-4 sentences in my own words. After I do, compare my paraphrase to the argument reconstruction from step 1.2. Tell me:
> - What did I capture accurately?
> - What did I miss, distort, or oversimplify?
> - Are there any subtle points I flattened?
>
> Be honest -- this is a comprehension check, not a compliment session.

**Note:** The reader should write their paraphrase first, then share it for comparison. If they ask the AI to paraphrase for them, the exercise loses its value.

---

### 1.5 Open Questions

**Prompt:**

> Before we move on, let me capture what is still unclear or confusing about this section. I will list my open questions. For each one, tell me:
> - Is this something the text answers later (if you know)?
> - Is this a genuine ambiguity in the text?
> - Is this a question I should hold for the Critical Evaluation pass?
>
> Also flag anything you think I should be confused about but am not -- blind spots I might have.

---

### Comprehension Lens Output Templates

#### Section Summary Template

```markdown
## Section [NUMBER]: [TITLE]

### Summary (3-5 sentences)
[Write a concise summary of the section's argument, not its topic. What does it claim, not just what does it discuss?]

### Central Claim
[One sentence stating the section's core assertion.]

### Key Premises / Evidence
1. [Premise or piece of evidence]
2. [Premise or piece of evidence]
3. [Premise or piece of evidence]

### Connection to Previous Section
[How does this section relate to what came before? Does it build, pivot, complicate, or contrast?]

### Paraphrase Check
- Accurate: [What the reader captured correctly]
- Gaps: [What was missed or distorted]
```

#### Key Terms Glossary Table

```markdown
## Glossary

| Term | Definition | How the Author Uses It |
|------|-----------|----------------------|
| [term] | [plain-language definition] | [specific usage in this text] |
| [term] | [plain-language definition] | [specific usage in this text] |
| [term] | [plain-language definition] | [specific usage in this text] |
```

#### Open Questions List

```markdown
## Open Questions

### Section [NUMBER]: [TITLE]
1. [Question] -- *[Answered later / Genuine ambiguity / Hold for Critical Evaluation]*
2. [Question] -- *[Answered later / Genuine ambiguity / Hold for Critical Evaluation]*

### Section [NUMBER]: [TITLE]
1. [Question] -- *[Status]*
```

#### End-of-Pass Argument Map Template

```markdown
## Argument Map (After Comprehension Pass)

### Overall Thesis
[The text's overarching argument in 1-2 sentences.]

### Section-by-Section Flow
1. **[Section 1 Title]**: [Core claim] --> leads to...
2. **[Section 2 Title]**: [Core claim] --> leads to...
3. **[Section 3 Title]**: [Core claim] --> leads to...
...

### Key Dependencies
- [Section X] depends on [Section Y] because...
- [Section X] assumes the reader accepted [claim from Section Y]...

### Unresolved Threads
- [Questions or tensions not yet resolved by end of text]
```

---

## Pass 2: Architecture Lens

**Core question:** How is the argument built, and why is it built this way?

**Goal:** Move from understanding what the text says to understanding how it works -- its structure, rhetorical choices, strategic sequencing, and deliberate omissions.

**How to run this pass:** Bring the Comprehension Pass outputs (summaries, argument map, glossary) into the conversation. Work through each section again, but now with the prompts below. You are no longer asking "what does this say?" but "why does it say it this way?"

---

### 2.1 Structural Moves

**Prompt:**

> I have completed a comprehension pass of [TEXT TITLE]. Now I want to analyze the architecture. Here is my argument map from Pass 1:
>
> [PASTE ARGUMENT MAP]
>
> For [SECTION NAME/NUMBER], analyze the structural move: Why does this section come where it does in the text? What does the sequencing accomplish? Would the argument work differently if this section came earlier or later? Is the author building incrementally, circling back, setting up a reversal, or doing something else?

---

### 2.2 Rhetorical Strategy

**Prompt:**

> Now examine the rhetorical strategy in [SECTION NAME/NUMBER]:
> - What examples does the author choose, and why these rather than alternatives? Are the examples doing argumentative work or decorative work?
> - Where does the author use analogy, irony, understatement, or deliberate provocation? What effect does each device produce?
> - Who is the implied audience? Is the author writing for allies, opponents, newcomers, or specialists? Does the audience shift within the text?
> - What tone does the author adopt and does it shift? Where and why?

---

### 2.3 What's Juxtaposed

**Prompt:**

> Identify the deliberate juxtapositions and tensions in [SECTION NAME/NUMBER]. Which ideas, thinkers, or positions does the author place in direct contrast? What emerges from each contrast -- does the author resolve the tension, leave it open, or use it to generate a third position?
>
> Also note any unexpected pairings -- thinkers or ideas brought together that would not normally be associated.

---

### 2.4 What's Absent

**Prompt:**

> Consider what is conspicuously not discussed in [SECTION NAME/NUMBER] and in the text as a whole up to this point:
> - Are there obvious thinkers, positions, or counter-arguments that the author does not engage?
> - Are there historical events, data, or contexts that seem relevant but are left out?
> - Do these omissions appear strategic (serving the argument) or accidental (blind spots)?
>
> Be specific about what you would expect to see and why its absence matters.

---

### 2.5 Author's Own Position

**Prompt:**

> Where in [SECTION NAME/NUMBER] does the author reveal their own commitments, and where do they hide behind description, summary, or other thinkers' views?
> - Identify passages where the author speaks in their own voice versus passages where they ventriloquize through others.
> - Are there moments where the author's real position is legible only between the lines?
> - Does the author use any thinker as a proxy for their own views?

---

### Architecture Lens Output Templates

#### Structural Annotations

```markdown
## Structural Annotations

### Section [NUMBER]: [TITLE]

**Structural Move:** [What this section does in the overall architecture -- e.g., "sets up the central opposition," "provides historical grounding for the theoretical claim in Section 5," "reverses the reader's expectations from Section 2"]

**Rhetorical Strategy:**
- Examples chosen: [list and note why]
- Devices used: [analogy / irony / understatement / provocation -- with specific instances]
- Implied audience: [who is being addressed and how]

**Key Juxtapositions:**
- [Thinker/Idea A] vs. [Thinker/Idea B]: [what emerges from the contrast]

**Notable Absences:**
- [What's missing and whether it appears strategic or accidental]

**Author's Position:**
- Revealed: [where the author speaks directly]
- Hidden: [where the author's view is only implicit]
```

#### Revised Argument Map

```markdown
## Revised Argument Map (After Architecture Pass)

### Overall Thesis
[Refined statement -- may have shifted from Comprehension Pass]

### Structural Logic
[Why the argument is sequenced the way it is -- what the ordering accomplishes]

### Section-by-Section Flow (Revised)
1. **[Section 1 Title]**: [Core claim] -- *Structural role: [role]* -- *Rhetorical mode: [mode]*
2. **[Section 2 Title]**: [Core claim] -- *Structural role: [role]* -- *Rhetorical mode: [mode]*
...

### Key Juxtapositions (Cross-Section)
- [Pair 1]: [What it produces]
- [Pair 2]: [What it produces]

### Strategic Omissions
- [Omission 1]: [Why it matters]

### Author's Commitments (Emerging Picture)
- Stated: [positions the author explicitly endorses]
- Implied: [positions the author seems to hold but does not state directly]
- Unclear: [positions that remain ambiguous]
```

---

## Pass 3: Critical Evaluation Lens

**Core question:** How strong is this argument, really?

**Goal:** Assess the text's strengths and weaknesses with intellectual honesty. Give credit before critique. Identify hidden assumptions and construct the strongest possible counter-arguments.

**How to run this pass:** Bring the outputs from Passes 1 and 2 into the conversation. You now have a solid understanding of what the text says and how it is built. The task is to evaluate whether it succeeds.

---

### 3.1 Strongest Moves

**Prompt:**

> Before any criticism, identify what [SECTION NAME/NUMBER] does well. What is genuinely compelling, original, or illuminating? Where does the author's argument feel strongest?
>
> Be specific -- point to particular passages, moves, or insights. Explain why they work, not just that they do.

---

### 3.2 Weakest Links

**Prompt:**

> Now identify the weakest points in [SECTION NAME/NUMBER]:
> - Are there logical gaps -- places where the conclusion does not follow from the premises?
> - Is evidence cherry-picked -- are counter-examples ignored or dismissed too quickly?
> - Are any positions strawmanned -- presented in weakened form to make them easier to refute?
> - Are there equivocations -- key terms that shift meaning between passages?
> - Are there leaps -- places where the author jumps from a small observation to a sweeping conclusion?
>
> For each weakness, explain how it affects the overall argument. Distinguish between minor imperfections and load-bearing flaws.

---

### 3.3 Hidden Assumptions

**Prompt:**

> Surface the hidden assumptions in [SECTION NAME/NUMBER] and the text as a whole:
> - What does the author take for granted that a reader might reasonably contest?
> - What framing choices shape the reader's perception before the argument even begins? (e.g., which categories are treated as natural, which comparisons are treated as obvious, which starting points are treated as self-evident)
> - Are there assumptions about the reader's values, politics, or intellectual commitments?
>
> For each assumption, note whether it is (a) likely shared by most readers, (b) contestable but defensible, or (c) genuinely problematic.

---

### 3.4 Steelman the Opposition

**Prompt:**

> For each position that the author criticizes or dismisses in [SECTION NAME/NUMBER], construct the strongest possible version of that position. Do not settle for the version the author presents -- build the version that a smart, honest advocate of that position would actually defend.
>
> Then assess: does the author's critique still hold against the steelmanned version, or only against the weaker version presented in the text?

---

### 3.5 Source Audit

**Prompt:**

> Examine how the author uses sources and references in [SECTION NAME/NUMBER]:
> - Are quoted or cited thinkers represented faithfully, or are their views simplified, distorted, or taken out of context to serve the thesis?
> - Does the author engage with the strongest versions of the positions they cite, or do they select convenient passages?
> - Are there important works or thinkers in this domain that are conspicuously absent from the citation record?
>
> If you are familiar with the cited sources, flag specific instances of faithful or unfaithful representation.

---

### Critical Evaluation Lens Output Templates

#### Balance Sheet

```markdown
## Balance Sheet

### Section [NUMBER]: [TITLE]

**Strengths:**
1. [Strength -- with specific reference to passage or move]
2. [Strength]

**Weaknesses:**
1. [Weakness -- with explanation of impact on overall argument]
2. [Weakness]

**Verdict:** [Is this section load-bearing and sound, load-bearing but shaky, or peripheral?]
```

#### Hidden Assumptions List

```markdown
## Hidden Assumptions

| Assumption | Where It Appears | Category |
|-----------|-----------------|----------|
| [assumption] | [section/passage] | [Shared / Contestable / Problematic] |
| [assumption] | [section/passage] | [Shared / Contestable / Problematic] |
```

#### Overall Critical Assessment

```markdown
## Critical Assessment

### What the Text Does Well
[2-3 paragraphs on the text's genuine contributions and strongest arguments.]

### Where the Text Falls Short
[2-3 paragraphs on the most significant weaknesses, distinguishing minor flaws from structural problems.]

### Steelmanned Counter-Arguments
[The 2-3 strongest objections the text does not adequately address.]

### Hidden Assumptions That Matter Most
[The 1-2 assumptions that, if contested, would most significantly undermine the argument.]

### Overall Judgment
[A balanced 1-paragraph assessment: What should a thoughtful reader take from this text, and what should they hold at arm's length?]
```

---

## Pass 4: Personal Synthesis Lens

**Core question:** What does this mean for me?

**Goal:** Move from analysis to integration. Identify what genuinely changes your thinking, what connects to your existing knowledge, where you disagree, and what you want to pursue further.

**How to run this pass:** Bring all prior outputs into the conversation. This pass is the most personal -- the AI assists, but the reader's own responses are the primary material.

---

### 4.1 What Surprised You

**Prompt:**

> Looking back over the entire text and your analysis, identify 3-5 ideas, arguments, or facts that genuinely surprised you -- things you did not know, had not considered, or that challenged an assumption you held.
>
> For each one, explain: Why was this surprising? Was it surprising because it was new information, a new framing, or because it contradicted something you believed?

---

### 4.2 Connections to Existing Knowledge

**Prompt:**

> Map the text's key ideas to other things you know. For each major argument or concept in the text, identify:
> - Other texts, thinkers, or frameworks that address similar questions
> - Real-world events or experiences that illustrate, confirm, or complicate the argument
> - Fields or disciplines where this idea appears in a different form
>
> The goal is to situate this text in your broader intellectual landscape rather than letting it sit in isolation.

---

### 4.3 Disagreements and Tensions

**Prompt:**

> Identify where this text conflicts with your existing beliefs, values, or intellectual commitments:
> - Where do you disagree with the author? Is it a factual disagreement, a values disagreement, or a disagreement about framing?
> - Are any of these disagreements productive -- do they force you to articulate or refine your own position?
> - Are there places where you feel the pull of the author's argument even though you want to resist it? What makes it compelling despite your disagreement?

---

### 4.4 Extractable Ideas

**Prompt:**

> Which concepts, frameworks, or distinctions from this text are useful beyond the text itself? Identify ideas that you could apply to other problems, texts, or domains.
>
> For each one, state:
> - The idea in one sentence
> - Where it came from in the text
> - Where else you might apply it
> - Any modifications needed to make it portable

---

### 4.5 Further Reading

**Prompt:**

> Based on what resonated most in this analysis -- the ideas that surprised you, the questions still open, the connections you want to explore -- suggest 3-5 texts to read next. For each:
> - Title and author
> - Why this text is a good next step (does it deepen, challenge, contextualize, or extend?)
> - What specific question or thread from the current analysis it addresses

---

### Personal Synthesis Lens Output Templates

#### Personal Annotations

```markdown
## Personal Annotations

### Section [NUMBER]: [TITLE]

**What struck me:** [Key reactions, surprises, connections]

**Agreements:** [Where I find the author compelling and why]

**Disagreements:** [Where I push back and why]

**Connections:** [Links to other texts, ideas, experiences]

**Extractable ideas:** [Concepts I want to take with me]
```

#### One-Page Takeaway Document

```markdown
## One-Page Takeaway: [TEXT TITLE]

### The Argument in Brief
[3-5 sentences capturing the text's overall thesis and how it is built.]

### What I Learned
[3-5 bullet points: the most important new ideas or shifts in understanding.]

### What I Question
[2-3 bullet points: the most significant unresolved doubts or disagreements.]

### Ideas to Keep
[2-3 portable concepts or frameworks extracted from the text, stated in my own words.]

### What to Read Next
1. [Title] by [Author] -- [one-sentence reason]
2. [Title] by [Author] -- [one-sentence reason]
3. [Title] by [Author] -- [one-sentence reason]

### One Sentence I Want to Remember
> "[Direct quote from the text that captures something essential.]"
```

---

## Bridge Conversations

Use the following template for the transition conversation between passes. Bridges serve two purposes: consolidating what the previous pass produced and reorienting for the next lens.

---

### Bridge Template: Pass [N] to Pass [N+1]

**Prompt:**

> I have completed Pass [N] ([PASS NAME]) of [TEXT TITLE]. Here are my outputs:
>
> [PASTE RELEVANT OUTPUTS -- summaries, argument map, annotations, etc.]
>
> Before I move to Pass [N+1] ([NEXT PASS NAME]), help me consolidate:
>
> 1. **What we established:** Summarize the key findings from this pass in 5-8 bullet points.
> 2. **What shifted:** Did anything in this pass change or complicate the understanding from the previous pass? Flag any revisions to earlier conclusions.
> 3. **What to carry forward:** Which specific findings, questions, or observations from this pass are most important for the next pass?
> 4. **What to watch for:** Given what we have learned so far, what should I be especially attentive to in the next pass?

---

### Bridge 1-to-2: Comprehension to Architecture

**Additional prompt:**

> Now that I understand what the text says, I want to understand how it is built. Looking at the argument map, which structural choices seem most deliberate or surprising? Where do I expect the Architecture pass to reveal the most?

### Bridge 2-to-3: Architecture to Critical Evaluation

**Additional prompt:**

> Now that I understand both what the text says and how it is constructed, I want to evaluate how well it works. Based on the structural analysis, where do I expect the argument to be strongest? Where do I expect it to be most vulnerable? Which rhetorical moves might be compensating for weak arguments?

### Bridge 3-to-4: Critical Evaluation to Personal Synthesis

**Additional prompt:**

> Now that I have a thorough understanding of the text's content, structure, and strengths and weaknesses, I want to figure out what it means for my own thinking. Looking at the balance sheet and critical assessment, what are the 2-3 ideas most worth wrestling with personally, regardless of whether the overall argument succeeds?

---

## Quick Reference Card

| Pass | Core Question | Steps | Key Outputs |
|------|--------------|-------|-------------|
| **1. Comprehension** | What is actually being said? | Thinker Backgrounder, Argument Reconstruction, Vocabulary Check, Paraphrase Test, Open Questions | Section summaries, Glossary, Open questions list, Argument map |
| **2. Architecture** | How is it built, and why? | Structural Moves, Rhetorical Strategy, What's Juxtaposed, What's Absent, Author's Position | Structural annotations, Revised argument map |
| **3. Critical Evaluation** | How strong is it, really? | Strongest Moves, Weakest Links, Hidden Assumptions, Steelman Opposition, Source Audit | Balance sheet, Hidden assumptions, Critical assessment |
| **4. Personal Synthesis** | What does it mean for me? | Surprises, Connections, Disagreements, Extractable Ideas, Further Reading | Personal annotations, One-page takeaway |

**Between each pass:** Run a Bridge Conversation to consolidate findings and reorient.

**Order matters:** Comprehension --> Architecture --> Critical Evaluation --> Personal Synthesis. Each pass builds on the previous.

**Time estimate:** For a 30-50 page text, expect 1-2 hours per pass. Dense or unfamiliar material may take longer.
