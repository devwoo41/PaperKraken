#!/usr/bin/env python3
"""PaperKraken bookmark injector (PyMuPDF).

Adds a PDF outline (viewer sidebar TOC) to a rendered report by locating the
report's h2/h3 headings in the PDF text. Run AFTER render_pdf.mjs:

  uv run --with pymupdf python add_bookmarks.py <report.html> <report.pdf>

- h2 -> level-1 bookmark, h3 -> level-2 bookmark (document order from the HTML).
- The cover page (page 1) is never searched, so cover-TOC lines cannot match.
- Search is forward-only (monotonic page cursor), so repeated strings in
  running headers resolve to their first (correct) page.
- Headings that cannot be located are skipped with a warning — the PDF is
  still valid, just missing that entry. Never fails the pipeline.
"""
import html as htmllib
import re
import sys

import fitz  # PyMuPDF

TAG_RE = re.compile(r"<[^>]+>")
MATH_RE = re.compile(r"\\[\(\[].*?\\[\)\]]")
HEAD_RE = re.compile(r"<(h[23])[^>]*>(.*?)</\1>", re.DOTALL | re.IGNORECASE)


def clean(raw):
    txt = MATH_RE.sub(" ", raw)          # drop inline math (rendered as SVG in the PDF)
    txt = TAG_RE.sub("", txt)
    txt = htmllib.unescape(txt)
    return re.sub(r"\s+", " ", txt).strip()


def headings_from_html(path):
    src = open(path, encoding="utf-8").read()
    # Ignore everything up to the end of the cover section if present.
    out = []
    for m in HEAD_RE.finditer(src):
        level = 1 if m.group(1).lower() == "h2" else 2
        title = clean(m.group(2))
        if title:
            out.append((level, title))
    return out


def find_page(doc, title, start_page):
    """First page >= start_page containing the heading text (shrinking needle)."""
    for needle_len in (28, 16, 10):
        needle = title[:needle_len].strip()
        if not needle:
            continue
        for pno in range(start_page, len(doc)):
            if doc[pno].search_for(needle):
                return pno
    return None


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: add_bookmarks.py <report.html> <report.pdf>")
    html_path, pdf_path = sys.argv[1], sys.argv[2]

    heads = headings_from_html(html_path)
    if not heads:
        sys.exit("no h2/h3 headings found in HTML")

    doc = fitz.open(pdf_path)
    toc, cursor, missed = [], 1, 0  # cursor=1: never search the cover (page index 0)
    for level, title in heads:
        pno = find_page(doc, title, cursor)
        if pno is None:
            print(f"WARN: not found, skipped: {title!r}", file=sys.stderr)
            missed += 1
            continue
        toc.append([level, title, pno + 1])
        cursor = pno  # forward-only; same page may host the next heading too

    # A level-2 entry may not directly follow the document root; normalize.
    for i, entry in enumerate(toc):
        if i == 0 and entry[0] != 1:
            entry[0] = 1

    doc.set_toc(toc)
    doc.saveIncr()
    print(f"OK: {len(toc)} bookmarks added to {pdf_path}"
          + (f" ({missed} headings not located)" if missed else ""))


if __name__ == "__main__":
    main()
