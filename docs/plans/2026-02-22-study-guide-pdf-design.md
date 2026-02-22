# Study Guide PDF Design

**Date**: 2026-02-22
**Status**: Approved

## Overview

Generate a single interleaved study guide PDF for "The Straussian Moment" that combines comprehension analysis materials with the source text in reading order.

## Structure (repeated for each of 5 sections)

1. **Before You Read** — Backgrounder (thinker primers, intellectual context, what to watch for)
2. **The Text** — Thiel's actual essay text for this section
3. **After You Read** — Summary, Key Terms glossary, Paraphrase Test prompt, Open Questions

Page breaks between sections.

## Implementation Steps

1. Generate Pass 1 comprehension analyses for Sections 2-5 (parallel subagents)
2. Assemble one master markdown file in reading order
3. Convert to PDF using pandoc
4. Output: `straussian-moment-study-guide.pdf` in project root

## Dependencies

- Section 1 comprehension: already complete
- Sections 2-5 comprehension: need to be generated
- Source text sections: already extracted in `analyses/straussian-moment/source-sections/`
- PDF conversion: pandoc (install if needed)
