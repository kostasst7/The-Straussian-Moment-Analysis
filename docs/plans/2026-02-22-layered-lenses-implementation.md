# Layered Lenses Framework — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a reusable deep reading framework and apply Pass 1 (Comprehension) to Section 1 of "The Straussian Moment."

**Architecture:** Three deliverables — (1) a reusable framework document with conversation prompts and output templates, (2) the analysis directory structure for The Straussian Moment, (3) a completed Pass 1 Comprehension analysis of Section 1. All outputs are markdown documents. The framework document serves as the canonical reference; analysis files are living documents updated during each conversation.

**Source text:** `2007-thiel.pdf` — Peter Thiel, "The Straussian Moment" (2007), ~40 pages, 5 sections.

---

### Task 1: Create the Reusable Framework Document

**Files:**
- Create: `framework/layered-lenses.md`

**Step 1: Create directory**

```bash
mkdir -p framework
```

**Step 2: Write the framework document**

Create `framework/layered-lenses.md` with the following structure:

```markdown
# Layered Lenses: A Deep Reading Framework

## How to Use This Framework
- Instructions for starting a new analysis
- How to identify sections in a text
- How to run each pass as a conversation session

## Pass 1: Comprehension Lens
- Conversation prompts for each step (backgrounder, argument reconstruction, vocabulary, paraphrase test, open questions)
- Output template for section summaries
- Output template for glossary
- Output template for argument map

## Pass 2: Architecture Lens
- Conversation prompts for each step (structural moves, rhetorical strategy, juxtaposition, absences, author's position)
- Output template for structural annotations
- Output template for revised argument map

## Pass 3: Critical Evaluation Lens
- Conversation prompts for each step (strongest moves, weakest links, hidden assumptions, steelman, source audit)
- Output template for balance sheet
- Output template for overall assessment

## Pass 4: Personal Synthesis Lens
- Conversation prompts for each step (surprises, connections, disagreements, extractable ideas, further reading)
- Output template for personal annotations
- Output template for takeaway document

## Bridge Conversations
- Template for transition between passes

## Appendix: Quick Reference Card
- One-page summary of all four passes with core questions
```

Each prompt should be written as a direct instruction Claude can follow in conversation — e.g., "Ask the reader to identify the central claim of this section. If they struggle, offer the following guiding questions: ..."

Each output template should be a fillable markdown structure — e.g.:

```markdown
## Section N: [Title]

### Summary
[3-5 sentences capturing the argument]

### Key Terms
| Term | Definition | How the author uses it |
|------|-----------|----------------------|
| ... | ... | ... |

### Open Questions
- ...
```

**Step 3: Review the document**

Read through `framework/layered-lenses.md` and verify:
- All four passes have complete prompt sets
- All output templates are present and consistent
- The "How to Use" section is clear enough to follow cold

---

### Task 2: Create Analysis Directory Structure

**Files:**
- Create: `analyses/straussian-moment/pass-1-comprehension.md`
- Create: `analyses/straussian-moment/pass-2-architecture.md`
- Create: `analyses/straussian-moment/pass-3-evaluation.md`
- Create: `analyses/straussian-moment/pass-4-synthesis.md`
- Create: `analyses/straussian-moment/takeaways.md`

**Step 1: Create directories**

```bash
mkdir -p analyses/straussian-moment
```

**Step 2: Create skeleton analysis files**

Each file should contain:
- A header identifying the pass and the text
- Section headers for all 5 sections of The Straussian Moment
- Empty output templates from the framework, ready to be filled in

Example for `pass-1-comprehension.md`:

```markdown
# Pass 1: Comprehension — The Straussian Moment

## Section 1: Introduction / The Question of Human Nature
### Summary
### Key Terms
### Open Questions

## Section 2: John Locke — The American Compromise
### Summary
### Key Terms
### Open Questions

[... etc for all 5 sections ...]

## Argument Map
[To be completed after all sections]
```

**Step 3: Verify structure**

```bash
ls -R analyses/straussian-moment/
```

Expected: 5 markdown files, each with section headers matching the text's structure.

---

### Task 3: Extract Text Sections from PDF

**Files:**
- Create: `analyses/straussian-moment/source-sections/section-1-human-nature.md`
- Create: `analyses/straussian-moment/source-sections/section-2-locke.md`
- Create: `analyses/straussian-moment/source-sections/section-3-schmitt.md`
- Create: `analyses/straussian-moment/source-sections/section-4-strauss.md`
- Create: `analyses/straussian-moment/source-sections/section-5-girard.md`

**Step 1: Create directory**

```bash
mkdir -p analyses/straussian-moment/source-sections
```

**Step 2: Extract full text and split by section headers**

Use `pdftotext` to extract the PDF content, then split at each section heading:
- Introduction runs from the start to "JOHN Locke: THE AMERICAN COMPROMISE"
- Each subsequent section runs to the next heading or to the endnotes

```bash
pdftotext 2007-thiel.pdf -
```

Split the output into 5 separate markdown files, one per section. Clean up OCR artifacts (page numbers, broken words across lines) where noticed.

**Step 3: Verify each section file has content**

```bash
wc -l analyses/straussian-moment/source-sections/*.md
```

---

### Task 4: Pass 1 Comprehension — Section 1 (Introduction / The Question of Human Nature)

This is the core analytical work. Follow the framework prompts from `framework/layered-lenses.md`.

**Files:**
- Read: `analyses/straussian-moment/source-sections/section-1-human-nature.md`
- Read: `framework/layered-lenses.md` (Pass 1 prompts)
- Modify: `analyses/straussian-moment/pass-1-comprehension.md` (Section 1 entries)

**Step 1: Thinker Backgrounder**

Section 1 references several thinkers in passing (Voltaire, Augustine, Machiavelli, Adam Smith, Karl Marx, Hegel, Kant, Pierre Manent, Hobbes, Locke). Provide a brief backgrounder on the key intellectual traditions:
- The Enlightenment project and its assumptions about human nature
- The older tradition: Athens (classical philosophy) vs. Jerusalem (Christian theology)
- The early modern crisis: Reformation, Counter-Reformation, Thirty Years' War
- How this context sets up the four thinkers Thiel will examine

Write the backgrounder into the analysis file.

**Step 2: Argument Reconstruction**

Identify and document:
- **Central claim**: What is Thiel's main argument in this section?
- **Key premises**: What evidence and reasoning support it?
- **Connection**: How does this introduction set up the rest of the essay?

Write into the analysis file under Section 1.

**Step 3: Vocabulary Check**

Identify and define technical/loaded terms as used in this section. Expected terms include:
- "homo economicus"
- "Athens and Jerusalem"
- "the modern individual"
- "the state of nature"
- "the Enlightenment project"
- Any others encountered

Write the glossary table into the analysis file.

**Step 4: Conversation — Paraphrase Test**

This step is interactive. Present the summary to the reader and ask them to restate it in their own words. Compare their paraphrase to the reconstructed argument and note any gaps.

For the plan: write a prompt in the analysis file that says:
> **Paraphrase Test**: Try restating the argument of this section in 3-4 sentences of your own. Then compare with the summary above — what did you capture? What did you miss?

**Step 5: Open Questions**

Document questions raised by this section that aren't yet answered. These might include:
- Is Thiel right that 9/11 exposed a fundamental flaw in modern political thought, or is he overstating?
- What exactly does the "older tradition" offer that modernity abandoned?
- How will the four thinkers (Locke, Schmitt, Strauss, Girard) each respond to this problem?

Write into the analysis file.

**Step 6: Review completed Section 1 entry**

Read `analyses/straussian-moment/pass-1-comprehension.md` and verify Section 1 is complete:
- Summary present (3-5 sentences)
- Backgrounder present
- Glossary table filled
- Paraphrase prompt included
- Open questions listed

---

### Task 5: Final Review and Summary

**Step 1: Verify all files exist and have content**

```bash
ls -la framework/
ls -la analyses/straussian-moment/
ls -la analyses/straussian-moment/source-sections/
wc -l framework/layered-lenses.md
wc -l analyses/straussian-moment/pass-1-comprehension.md
```

**Step 2: Read through framework document**

Verify it's self-contained and usable for any text, not just The Straussian Moment.

**Step 3: Read through Pass 1 Section 1 analysis**

Verify it follows the framework's templates and is substantive.

**Step 4: Present summary to user**

Report what was created, what's ready to use, and what the next step is (continuing Pass 1 with Section 2: Locke, in a conversation-driven session).
