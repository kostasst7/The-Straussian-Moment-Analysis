#!/usr/bin/env python3
"""Clean up PDF extraction artifacts from source text using layout-aware parsing.

Uses pdftotext -layout output which preserves paragraph indentation,
allowing reliable detection of paragraph boundaries and block quotes.

Works with different text layouts by detecting:
- Paragraph starts (indented first lines)
- Block quotes (consistently indented blocks)
- Section dividers (asterisk separators)
- Page headers/footers
- Hyphenated word breaks across lines/pages
"""

import re
import subprocess
from pathlib import Path

ROOT = Path("/Users/kostasstankevicius/The-Straussian-Moment-Analysis")
SOURCES = ROOT / "analyses" / "straussian-moment" / "source-sections"
PDF = ROOT / "2007-thiel.pdf"

MIN_INDENT = 4  # Minimum spaces to count as "indented" (paragraph start or quote)

# Section boundaries (headings as they appear in the layout text)
SECTIONS = [
    {
        "num": 1,
        "title": "Introduction / The Question of Human Nature",
        "filename": "section-1-human-nature.md",
        "start_marker": None,
        "end_marker": "JOHN Locke: THE AMERICAN COMPROMISE",
    },
    {
        "num": 2,
        "title": "John Locke — The American Compromise",
        "filename": "section-2-locke.md",
        "start_marker": "JOHN Locke: THE AMERICAN COMPROMISE",
        "end_marker": "CARL SCHMITT: THE PERSISTENCE OF THE POLITICAL",
    },
    {
        "num": 3,
        "title": "Carl Schmitt — The Persistence of the Political",
        "filename": "section-3-schmitt.md",
        "start_marker": "CARL SCHMITT: THE PERSISTENCE OF THE POLITICAL",
        "end_marker": "LEO STRAUSS: PROCEED WITH CAUTION",
    },
    {
        "num": 4,
        "title": "Leo Strauss — Proceed with Caution",
        "filename": "section-4-strauss.md",
        "start_marker": "LEO STRAUSS: PROCEED WITH CAUTION",
        "end_marker": "RENE GIRARD: THE END OF THE CITY OF MAN",
    },
    {
        "num": 5,
        "title": "René Girard — The End of the City of Man",
        "filename": "section-5-girard.md",
        "start_marker": "RENE GIRARD: THE END OF THE CITY OF MAN",
        "end_marker": "NOTES",
    },
]


def get_layout_text():
    """Extract text from PDF with layout preservation."""
    result = subprocess.run(
        ["pdftotext", "-layout", str(PDF), "-"],
        capture_output=True, text=True,
    )
    return result.stdout


def leading_spaces(line):
    """Count leading spaces."""
    if not line or not line.strip():
        return 0
    return len(line) - len(line.lstrip())


def is_page_artifact(line):
    """Check if a line is a page header, footer, or number."""
    s = line.strip()
    if not s:
        return False
    if re.match(r'^The Straussian Moment\s+\.?\s*\d+$', s):
        return True
    if re.match(r'^\d+\s+Peter Thiel$', s):
        return True
    if re.match(r'^\d{3}$', s):
        return True
    return False


def is_main_section_heading(line):
    """Check if a line is one of the main section headings we already title.

    Only removes the TOP-LEVEL section headings that duplicate the markdown
    header (e.g., "JOHN Locke: THE AMERICAN COMPROMISE"). Internal sub-headings
    like "THE QUESTION OF HUMAN NATURE" are kept as part of the text.
    """
    s = line.strip()
    if not s:
        return False
    # Only match the exact main section headings
    main_headings = [
        "JOHN Locke: THE AMERICAN COMPROMISE",
        "CARL SCHMITT: THE PERSISTENCE OF THE POLITICAL",
        "LEO STRAUSS: PROCEED WITH CAUTION",
        "RENE GIRARD: THE END OF THE CITY OF MAN",
    ]
    for heading in main_headings:
        if heading in s:
            return True
    return False


def is_subheading(line):
    """Check if a line is an internal subheading (centered, ALL-CAPS).

    These are kept in the text but treated as paragraph boundaries.
    """
    s = line.strip()
    if not s or len(s) < 10:
        return False
    if leading_spaces(line) >= 10:
        upper_ratio = sum(1 for c in s if c.isupper()) / max(len(s.replace(' ', '')), 1)
        if upper_ratio > 0.5 and s not in ("NOTES",):
            return True
    return False


def is_divider(line):
    """Check if a line is a section divider (* * *)."""
    s = line.strip()
    if not s:
        return False
    if re.match(r'^[\s*kKOox.×]+$', s) and len(s) <= 20 and '*' in s:
        return True
    return False


def clean_and_split_sections(layout_text):
    """Parse layout text, find section boundaries."""
    all_lines = layout_text.split('\n')

    section_starts = {}
    for i, line in enumerate(all_lines):
        s = line.strip()
        for sec in SECTIONS:
            if sec["start_marker"] and sec["start_marker"] in s:
                section_starts[sec["num"]] = i

    # Section 1 starts at the first body text line
    for i, line in enumerate(all_lines):
        if 'twenty-first century started' in line:
            section_starts[1] = i
            break

    # Find NOTES section
    notes_start = None
    for i, line in enumerate(all_lines):
        if line.strip() == 'NOTES':
            notes_start = i
            break

    section_ranges = {}
    for sec in SECTIONS:
        num = sec["num"]
        start = section_starts.get(num, 0)
        if num < 5:
            end = section_starts.get(num + 1, notes_start or len(all_lines))
        else:
            end = notes_start or len(all_lines)
        section_ranges[num] = (start, end)

    # Capture the poem (before section 1 body)
    poem_lines = []
    for i, line in enumerate(all_lines):
        s = line.strip()
        if not s:
            continue
        if 'The         Straussian Moment' in line or 'Peter Thiel' in s:
            continue
        if 'President, Clarium' in s:
            continue
        if 'Locksley Hall' in s:
            poem_lines.append(line)
            break
        if i < section_starts.get(1, 999) and leading_spaces(line) >= 8:
            poem_lines.append(line)

    return section_ranges, all_lines, poem_lines


def normalize_spaces(text):
    """Collapse multiple spaces into single spaces (layout artifacts)."""
    return re.sub(r'  +', ' ', text)


def extract_clean_lines(all_lines, start, end):
    """Extract content lines for a section, removing artifacts.

    Returns list of (indent, text) tuples for non-blank content lines,
    with 'BLANK' markers where blank lines existed in the original.
    Special types: 'DIVIDER' for section dividers, 'SUBHEADING' for internal headings.
    """
    result = []
    in_drop_cap = True  # At start of section, handle drop-cap region

    for i in range(start, end):
        line = all_lines[i]
        if is_page_artifact(line):
            continue
        if is_main_section_heading(line):
            continue
        if not line.strip():
            if result and result[-1] != 'BLANK':
                result.append('BLANK')
            continue
        if is_divider(line):
            result.append(('DIVIDER', line.strip()))
            in_drop_cap = False
            continue
        if is_subheading(line):
            result.append(('SUBHEADING', line.strip()))
            in_drop_cap = False
            continue

        indent = leading_spaces(line)
        text = normalize_spaces(line.strip())

        # Handle drop-cap region: at the start of a section, the first
        # paragraph may have extra indentation from a large initial letter.
        # All lines in this region (until the first non-indented line) should
        # have their indent set to 0 so they're treated as regular paragraph.
        if in_drop_cap:
            if indent >= MIN_INDENT:
                indent = 0  # Still in drop-cap region
            else:
                in_drop_cap = False  # First non-indented line ends the region

        # Fix drop-cap artifacts: the large initial letter is often lost
        # in extraction, leaving e.g. "he" instead of "The"
        if in_drop_cap and indent == 0 and not result:
            # This is the very first content line. Check for missing drop cap.
            # Common pattern: first word is lowercase but should start uppercase
            if text and text[0].islower():
                # Check if adding "T" makes "The" (most common drop cap)
                if text.startswith('he ') or text.startswith('he\xa0'):
                    text = 'T' + text

        result.append((indent, text))


    # Strip leading/trailing blanks
    while result and result[0] == 'BLANK':
        result.pop(0)
    while result and result[-1] == 'BLANK':
        result.pop()

    return result


def join_with_hyphens(text_a, text_b):
    """Join two text fragments, handling hyphenated word breaks."""
    if not text_a:
        return text_b
    if not text_b:
        return text_a
    # Hyphenated break: text_a ends with letter-hyphen, text_b starts lowercase
    if (text_a[-1] == '-' and len(text_a) >= 2 and text_a[-2].isalpha()
            and not text_a.endswith('--') and text_b[0].islower()):
        return text_a[:-1] + text_b
    return text_a + ' ' + text_b


def process_section(all_lines, start, end):
    """Process section lines into clean markdown text.

    Uses indentation as the primary signal for structure:
    - Lines with >= MIN_INDENT spaces: start of new paragraph or block quote
    - Lines with < MIN_INDENT spaces: continuation of current element
    - Consecutive indented lines (across blank lines): block quote
    - Single indented line followed by unindented: paragraph start
    """
    items = extract_clean_lines(all_lines, start, end)

    # Build elements: list of ('para', text) | ('quote', text) | ('divider', text)
    elements = []
    i = 0

    while i < len(items):
        item = items[i]

        # Skip blank markers
        if item == 'BLANK':
            i += 1
            continue

        # Handle dividers
        if item[0] == 'DIVIDER':
            elements.append(('divider', '\u2042'))
            i += 1
            continue

        # Handle subheadings
        if item[0] == 'SUBHEADING':
            elements.append(('subheading', item[1]))
            i += 1
            continue

        indent, text = item

        if indent >= MIN_INDENT:
            # Indented line. Determine: block quote or paragraph start?
            # Look ahead (past blanks) to see if the NEXT content line
            # is also indented or not.
            is_quote = is_quote_block(items, i)

            if is_quote:
                # Collect all lines of this quote block
                quote_text, i = collect_quote(items, i)
                elements.append(('quote', quote_text))
            else:
                # This is a paragraph start (indented first line).
                # Collect this line + all following unindented continuation lines.
                para_text, i = collect_paragraph(items, i)
                elements.append(('para', para_text))
        else:
            # Unindented line at the start of a section or after a divider/quote.
            # Treat as a paragraph.
            para_text, i = collect_paragraph(items, i)
            elements.append(('para', para_text))

    # Format output
    parts = []
    for etype, etext in elements:
        if etype == 'divider':
            parts.append('\u2042')
        elif etype == 'quote':
            parts.append(f'> {etext}')
        elif etype == 'subheading':
            parts.append(etext)
        else:
            parts.append(etext)

    return '\n\n'.join(parts)


def is_quote_block(items, start_idx):
    """Determine if the indented line at start_idx begins a block quote.

    A block quote has multiple consecutive indented lines (possibly separated
    by blank lines from page breaks). A paragraph start is a single indented
    line followed by unindented continuation.

    Heuristic: look at the next 2-3 non-blank lines after start_idx.
    If at least 2 of them are also indented, it's a quote.
    """
    indented_count = 0
    unindented_count = 0
    checked = 0

    j = start_idx + 1
    while j < len(items) and checked < 4:
        if items[j] == 'BLANK':
            j += 1
            continue
        if isinstance(items[j][0], str):  # DIVIDER, SUBHEADING, etc.
            break
        indent, text = items[j]
        if indent >= MIN_INDENT:
            indented_count += 1
        else:
            unindented_count += 1
        checked += 1
        j += 1

    # If the next non-blank lines are mostly indented, it's a quote
    # If the very next non-blank line is unindented, it's a paragraph start
    if checked == 0:
        return False
    # If first non-blank successor is indented, likely a quote
    j = start_idx + 1
    while j < len(items) and items[j] == 'BLANK':
        j += 1
    if (j < len(items) and items[j] != 'BLANK'
            and not isinstance(items[j][0], str)
            and items[j][0] >= MIN_INDENT):
        return True
    return False


def collect_quote(items, start_idx):
    """Collect a block quote starting at start_idx.

    Gathers consecutive indented lines (allowing blank lines from page breaks
    and occasional unindented continuation after hyphenation).
    Stops when we hit a non-indented line that doesn't continue a hyphen,
    or a divider.
    """
    parts = []
    i = start_idx

    while i < len(items):
        item = items[i]

        if item == 'BLANK':
            # Blank line in a quote: check if the quote continues
            j = i + 1
            while j < len(items) and items[j] == 'BLANK':
                j += 1
            if (j < len(items) and items[j] != 'BLANK'
                    and not isinstance(items[j][0], str)):
                next_indent = items[j][0]
                # If next content line is indented, check whether it's
                # a continuation of THIS quote or the start of a NEW paragraph.
                # Use is_quote_block to check: if the line after j is also
                # indented, the quote continues. If non-indented, j starts
                # a new paragraph (its indentation is paragraph indent, not quote).
                if next_indent >= MIN_INDENT and is_quote_block(items, j):
                    i = j
                    continue
                # If next line is unindented but previous ended with hyphen, continue
                if parts and parts[-1].endswith('-') and not parts[-1].endswith('--'):
                    i = j
                    continue
                # Otherwise, quote is done
                break
            else:
                break

        if isinstance(item[0], str):
            # DIVIDER, SUBHEADING, etc.
            break

        indent, text = item

        if indent >= MIN_INDENT:
            parts.append(text)
            i += 1
        elif parts and parts[-1].endswith('-') and not parts[-1].endswith('--') and text and text[0].islower():
            # Unindented continuation after hyphenation within a quote
            parts.append(text)
            i += 1
        else:
            # Unindented line that's not a hyphen continuation: quote is done
            break

    # Join all parts
    quote_text = join_parts(parts)
    return quote_text, i


def collect_paragraph(items, start_idx):
    """Collect a paragraph starting at start_idx.

    Gathers the starting line and all following unindented continuation lines
    (allowing blank lines from page breaks). Stops at the next indented line
    (which starts a new paragraph or quote) or a divider.
    """
    parts = []
    i = start_idx

    # Add the first line
    if items[i] != 'BLANK' and items[i][0] not in ('DIVIDER', 'SUBHEADING'):
        parts.append(items[i][1])
        i += 1

    while i < len(items):
        item = items[i]

        if item == 'BLANK':
            # Blank line: check what follows
            j = i + 1
            while j < len(items) and items[j] == 'BLANK':
                j += 1
            if j >= len(items):
                break
            next_item = items[j]
            if next_item == 'BLANK':
                break
            if isinstance(next_item[0], str):
                # DIVIDER, SUBHEADING, etc. - end of paragraph
                break
            next_indent = next_item[0]
            if next_indent >= MIN_INDENT:
                # Next content is indented: new paragraph or quote. Stop here.
                break
            else:
                # Next content is unindented: continuation after page break.
                # Skip the blanks and continue collecting.
                i = j
                continue

        if isinstance(item[0], str):
            # DIVIDER, SUBHEADING, etc.
            break

        indent, text = item

        if indent >= MIN_INDENT:
            # New indented line: start of new paragraph or quote. Stop.
            break
        else:
            # Unindented continuation line
            parts.append(text)
            i += 1

    para_text = join_parts(parts)
    return para_text, i


def join_parts(parts):
    """Join text parts, handling hyphenated word breaks."""
    if not parts:
        return ''
    result = parts[0]
    for part in parts[1:]:
        result = join_with_hyphens(result, part)
    return result


def clean_poem(poem_lines):
    """Format the Tennyson poem as markdown block quote."""
    lines = [l.strip() for l in poem_lines if l.strip()]
    return '\n'.join(f'> {l}' for l in lines)


def main():
    print("Extracting text with layout preservation...")
    layout_text = get_layout_text()

    print("Parsing sections...")
    section_ranges, all_lines, poem_lines = clean_and_split_sections(layout_text)

    for sec in SECTIONS:
        num = sec["num"]
        start, end = section_ranges[num]
        print(f"Processing Section {num}: {sec['title']} (lines {start}-{end})...")

        clean_text = process_section(all_lines, start, end)

        # For section 1, prepend the poem
        if num == 1:
            poem_md = clean_poem(poem_lines)
            clean_text = poem_md + '\n\n' + clean_text

        # Build markdown file
        header = f"# Section {num}: {sec['title']}\n\n"
        output = header + clean_text + '\n'

        outpath = SOURCES / sec["filename"]
        outpath.write_text(output)
        print(f"  Written to: {outpath}")

    print("\nDone! Source sections cleaned.")


if __name__ == "__main__":
    main()
