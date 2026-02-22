#!/usr/bin/env python3
"""Build an HTML study guide with embedded original PDF pages.

Instead of extracting and reformatting the source text (which introduces
artifacts), this embeds the original PDF pages directly using the browser's
native PDF viewer. Backgrounders go before, summaries go after.

Usage: python build-html.py
Output: output/study-guide.html + output/sections/section-N.pdf
"""

import subprocess
import re
from pathlib import Path

import markdown
import pikepdf

ROOT = Path("/Users/kostasstankevicius/The-Straussian-Moment-Analysis")
ANALYSES = ROOT / "analyses" / "straussian-moment"
PDF = ROOT / "2007-thiel.pdf"
OUTPUT = ROOT / "output"
SECTIONS_DIR = OUTPUT / "sections"

# Section markers (same as clean-source-text.py)
SECTIONS = [
    {
        "num": 1,
        "title": "Introduction / The Question of Human Nature",
        "start_marker": None,
        "end_marker": "JOHN Locke: THE AMERICAN COMPROMISE",
        "analysis": ANALYSES / "pass-1-comprehension.md",
        "analysis_type": "main",
    },
    {
        "num": 2,
        "title": "John Locke: The American Compromise",
        "start_marker": "JOHN Locke: THE AMERICAN COMPROMISE",
        "end_marker": "CARL SCHMITT: THE PERSISTENCE OF THE POLITICAL",
        "analysis": ANALYSES / "section-2-comprehension.md",
        "analysis_type": "standalone",
    },
    {
        "num": 3,
        "title": "Carl Schmitt: The Persistence of the Political",
        "start_marker": "CARL SCHMITT: THE PERSISTENCE OF THE POLITICAL",
        "end_marker": "LEO STRAUSS: PROCEED WITH CAUTION",
        "analysis": ANALYSES / "section-3-comprehension.md",
        "analysis_type": "standalone",
    },
    {
        "num": 4,
        "title": "Leo Strauss: Proceed with Caution",
        "start_marker": "LEO STRAUSS: PROCEED WITH CAUTION",
        "end_marker": "RENE GIRARD: THE END OF THE CITY OF MAN",
        "analysis": ANALYSES / "section-4-comprehension.md",
        "analysis_type": "standalone",
    },
    {
        "num": 5,
        "title": "Rene Girard: The End of the City of Man",
        "start_marker": "RENE GIRARD: THE END OF THE CITY OF MAN",
        "end_marker": "NOTES",
        "analysis": ANALYSES / "section-5-comprehension.md",
        "analysis_type": "standalone",
    },
]


# ---------------------------------------------------------------------------
# Step 1: Determine page ranges per section
# ---------------------------------------------------------------------------

def get_page_text(page_num):
    """Extract text from a single PDF page using pdftotext."""
    result = subprocess.run(
        ["pdftotext", "-f", str(page_num), "-l", str(page_num), str(PDF), "-"],
        capture_output=True, text=True,
    )
    return result.stdout


def get_total_pages():
    """Get total page count using pikepdf."""
    with pikepdf.open(PDF) as pdf:
        return len(pdf.pages)


def find_section_pages():
    """Find the start page for each section marker."""
    total = get_total_pages()
    marker_pages = {}

    for page_num in range(1, total + 1):
        text = get_page_text(page_num)

        # Section 1: find the first page with body text
        if "twenty-first century started" in text and 1 not in marker_pages:
            marker_pages[1] = page_num

        # Other sections: find their heading markers
        for sec in SECTIONS:
            if sec["start_marker"] and sec["start_marker"] in text:
                if sec["num"] not in marker_pages:
                    marker_pages[sec["num"]] = page_num

        # Find NOTES page (end of essay)
        if re.search(r'^NOTES\s*$', text, re.MULTILINE):
            if "NOTES" not in marker_pages:
                marker_pages["NOTES"] = page_num

    return marker_pages, total


def compute_page_ranges(marker_pages, total_pages):
    """Compute (start_page, end_page) for each section.

    Boundary pages (where the next section's heading appears) are included in
    both the current and next section, since they often contain trailing text
    from the current section above the heading.
    Section 1 includes the title/poem page(s) before the body text starts.
    Section 5 includes the page where NOTES starts (essay ends on that page).
    """
    # Section 1 starts at page 1 (includes title/poem pages)
    starts = {1: 1}
    for sec in SECTIONS[1:]:
        starts[sec["num"]] = marker_pages[sec["num"]]

    notes_page = marker_pages.get("NOTES", total_pages)

    ranges = {}
    section_nums = [s["num"] for s in SECTIONS]
    for i, num in enumerate(section_nums):
        start = starts[num]
        if i + 1 < len(section_nums):
            # Include the boundary page (may have trailing text from this section)
            end = starts[section_nums[i + 1]]
        else:
            # Last section ends at the NOTES page (which has the final paragraph)
            end = notes_page
        ranges[num] = (start, end)

    return ranges


# ---------------------------------------------------------------------------
# Step 2: Split PDF into per-section files
# ---------------------------------------------------------------------------

def split_pdf(page_ranges):
    """Extract page ranges into separate PDF files using pikepdf."""
    SECTIONS_DIR.mkdir(parents=True, exist_ok=True)

    with pikepdf.open(PDF) as source:
        for sec in SECTIONS:
            num = sec["num"]
            start, end = page_ranges[num]
            out_path = SECTIONS_DIR / f"section-{num}.pdf"

            dst = pikepdf.Pdf.new()
            # pikepdf uses 0-based indexing
            for page_idx in range(start - 1, end):
                dst.pages.append(source.pages[page_idx])
            dst.save(out_path)

            print(f"  Section {num}: pages {start}-{end} -> {out_path.name}")


# ---------------------------------------------------------------------------
# Step 3: Extract backgrounder/summary from analysis files
# ---------------------------------------------------------------------------

def extract_section1_parts(filepath):
    """Extract backgrounder and after-reading from the main comprehension file."""
    text = filepath.read_text()

    # Find Section 1 content (between "## Section 1:" and "## Section 2:")
    start = text.find("## Section 1:")
    end = text.find("## Section 2:")
    if start == -1 or end == -1:
        return "", ""
    section_text = text[start:end].strip()

    bg_start = section_text.find("### Backgrounder")
    summary_start = section_text.find("### Summary")
    if bg_start == -1 or summary_start == -1:
        return section_text, ""

    backgrounder = section_text[bg_start:summary_start].strip()
    after_reading = section_text[summary_start:].strip()
    return backgrounder, after_reading


def extract_standalone_parts(filepath):
    """Extract backgrounder and after-reading from a standalone analysis file."""
    text = filepath.read_text()

    bg_start = text.find("## Backgrounder")
    if bg_start == -1:
        bg_start = text.find("### Backgrounder")

    summary_start = text.find("## Summary")
    if summary_start == -1:
        summary_start = text.find("### Summary")

    if bg_start == -1 or summary_start == -1:
        return text, ""

    backgrounder = text[bg_start:summary_start].strip()
    after_reading = text[summary_start:].strip()
    return backgrounder, after_reading


# ---------------------------------------------------------------------------
# Step 4: Generate HTML
# ---------------------------------------------------------------------------

def md_to_html(md_text):
    """Convert markdown text to HTML."""
    return markdown.markdown(md_text, extensions=["tables", "fenced_code"])


def estimate_pdf_height(num_pages):
    """Estimate a good embed height based on page count.

    Each PDF page is roughly letter-size. We want enough height to show
    one page at a time comfortably while allowing scrolling.
    """
    return 900


def build_html(page_ranges):
    """Generate the study guide HTML file."""
    sections_html = []

    for sec in SECTIONS:
        num = sec["num"]
        title = sec["title"]
        start, end = page_ranges[num]
        num_pages = end - start + 1

        # Extract analysis content
        if sec["analysis_type"] == "main":
            backgrounder_md, after_md = extract_section1_parts(sec["analysis"])
        else:
            backgrounder_md, after_md = extract_standalone_parts(sec["analysis"])

        backgrounder_html = md_to_html(backgrounder_md)
        after_html = md_to_html(after_md)

        pdf_height = estimate_pdf_height(num_pages)

        section = f"""
    <section id="section-{num}">
      <h1>Section {num}: {title}</h1>

      <div class="before-reading">
        <h2>Before You Read</h2>
        {backgrounder_html}
      </div>

      <div class="original-text">
        <h2>The Text</h2>
        <p class="pdf-info">Pages {start}&ndash;{end} of the original document ({num_pages} page{'s' if num_pages != 1 else ''})</p>
        <embed src="sections/section-{num}.pdf#toolbar=0&view=FitH" type="application/pdf"
               width="100%" height="{pdf_height}px">
      </div>

      <div class="after-reading">
        <h2>After You Read</h2>
        {after_html}
      </div>
    </section>"""
        sections_html.append(section)

    # Build navigation
    nav_links = []
    for sec in SECTIONS:
        nav_links.append(
            f'<a href="#section-{sec["num"]}">{sec["num"]}. {sec["title"]}</a>'
        )
    nav_html = "\n        ".join(nav_links)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>The Straussian Moment &mdash; Study Guide</title>
  <style>
    * {{
      box-sizing: border-box;
    }}

    body {{
      font-family: Georgia, 'Times New Roman', serif;
      font-size: 16px;
      line-height: 1.7;
      color: #1a1a1a;
      background: #fafaf8;
      margin: 0;
      padding: 0;
    }}

    header {{
      background: #2c2c2c;
      color: #f0ede6;
      padding: 2.5rem 2rem;
      text-align: center;
    }}

    header h1 {{
      font-size: 2rem;
      margin: 0 0 0.3rem 0;
      font-weight: normal;
      letter-spacing: 0.02em;
    }}

    header .subtitle {{
      font-size: 1rem;
      color: #b8b4a8;
      font-style: italic;
    }}

    nav {{
      background: #3a3a3a;
      padding: 1rem 2rem;
      text-align: center;
      position: sticky;
      top: 0;
      z-index: 100;
      border-bottom: 1px solid #555;
    }}

    nav a {{
      color: #d4d0c8;
      text-decoration: none;
      margin: 0 0.8rem;
      font-size: 0.85rem;
      padding: 0.3rem 0;
      border-bottom: 2px solid transparent;
      transition: border-color 0.2s, color 0.2s;
    }}

    nav a:hover {{
      color: #fff;
      border-bottom-color: #c9a96e;
    }}

    .intro {{
      max-width: 48rem;
      margin: 2rem auto;
      padding: 0 2rem;
    }}

    .intro h2 {{
      font-size: 1.3rem;
      color: #333;
      margin-bottom: 0.5rem;
    }}

    .intro p, .intro li {{
      font-size: 0.95rem;
      color: #444;
    }}

    section {{
      max-width: 56rem;
      margin: 0 auto 3rem auto;
      padding: 0 2rem;
    }}

    section h1 {{
      font-size: 1.8rem;
      color: #2c2c2c;
      border-bottom: 2px solid #c9a96e;
      padding-bottom: 0.4rem;
      margin-top: 3rem;
    }}

    section h2 {{
      font-size: 1.3rem;
      color: #444;
      margin-top: 2rem;
      margin-bottom: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-weight: normal;
    }}

    .before-reading, .after-reading {{
      background: #fff;
      border: 1px solid #e0ddd4;
      border-radius: 4px;
      padding: 1.5rem 2rem;
      margin: 1rem 0;
    }}

    .before-reading h3, .after-reading h3 {{
      font-size: 1.1rem;
      color: #555;
      margin-top: 1.5rem;
      margin-bottom: 0.5rem;
    }}

    .before-reading h4, .after-reading h4 {{
      font-size: 1rem;
      color: #666;
      margin-top: 1.2rem;
      margin-bottom: 0.4rem;
      font-style: italic;
    }}

    .before-reading p, .after-reading p {{
      margin-bottom: 0.8rem;
      text-align: justify;
    }}

    .before-reading ul, .after-reading ul,
    .before-reading ol, .after-reading ol {{
      margin-bottom: 0.8rem;
      padding-left: 1.5rem;
    }}

    .before-reading li, .after-reading li {{
      margin-bottom: 0.4rem;
    }}

    blockquote {{
      margin: 1em 0;
      padding: 0.5em 1.2em;
      border-left: 3px solid #c9a96e;
      background: #f9f8f4;
      font-style: italic;
      color: #555;
    }}

    .original-text {{
      margin: 1.5rem 0;
    }}

    .pdf-info {{
      font-size: 0.85rem;
      color: #888;
      margin-bottom: 0.5rem;
      font-style: italic;
    }}

    embed {{
      border: 1px solid #ccc;
      border-radius: 4px;
      background: #fff;
    }}

    table {{
      border-collapse: collapse;
      width: 100%;
      margin: 1em 0;
      font-size: 0.9rem;
    }}

    th, td {{
      border: 1px solid #ddd;
      padding: 0.6rem 0.8rem;
      text-align: left;
      vertical-align: top;
    }}

    th {{
      background: #f5f3ee;
      font-weight: bold;
      color: #444;
    }}

    hr {{
      border: none;
      border-top: 1px solid #ddd;
      margin: 2rem 0;
    }}

    strong {{
      color: #222;
    }}

    code {{
      font-family: 'Menlo', 'Courier New', monospace;
      font-size: 0.88em;
      background: #f4f3ef;
      padding: 1px 5px;
      border-radius: 3px;
    }}

    footer {{
      text-align: center;
      padding: 2rem;
      color: #999;
      font-size: 0.85rem;
      border-top: 1px solid #e0ddd4;
      margin-top: 3rem;
    }}
  </style>
</head>
<body>
  <header>
    <h1>The Straussian Moment</h1>
    <div class="subtitle">Peter Thiel (2007) &mdash; Study Guide</div>
  </header>

  <nav>
    {nav_html}
  </nav>

  <div class="intro">
    <h2>How to Use This Guide</h2>
    <p>For each section of the essay, this guide provides three parts in reading order:</p>
    <ol>
      <li><strong>Before You Read</strong> &mdash; Background on the thinkers and concepts you'll encounter. Read this first to orient yourself.</li>
      <li><strong>The Text</strong> &mdash; Thiel's actual essay, displayed as the original typeset pages. Read it carefully, noting what's clear and what's confusing.</li>
      <li><strong>After You Read</strong> &mdash; A summary, glossary of key terms, a paraphrase test, and open questions. Use these to check and deepen your understanding.</li>
    </ol>
    <p>Take your time with each section before moving to the next.</p>
  </div>

  {"".join(sections_html)}

  <footer>
    Layered Lenses Deep Reading Framework &mdash; Pass 1: Comprehension
  </footer>
</body>
</html>"""

    output_path = OUTPUT / "study-guide.html"
    output_path.write_text(html)
    return output_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Finding section page boundaries...")
    marker_pages, total_pages = find_section_pages()
    print(f"  PDF has {total_pages} pages")
    for key, page in sorted(marker_pages.items(), key=lambda x: x[1]):
        print(f"  {key}: page {page}")

    print("\nComputing page ranges...")
    page_ranges = compute_page_ranges(marker_pages, total_pages)
    for sec in SECTIONS:
        num = sec["num"]
        start, end = page_ranges[num]
        print(f"  Section {num}: pages {start}-{end}")

    print("\nSplitting PDF into per-section files...")
    split_pdf(page_ranges)

    print("\nGenerating HTML study guide...")
    output_path = build_html(page_ranges)
    print(f"\nDone! Open in browser: {output_path}")


if __name__ == "__main__":
    main()
