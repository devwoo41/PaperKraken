---
name: paperkraken
description: Reads a research paper PDF using Nature's "Seven steps for critically analysing research papers" methodology (Jacques Cornwell, 2026) and produces a tutorial-grade comprehension report as a clean PDF, in Korean or English (user's choice). Includes a prerequisite-knowledge ladder, a web-verified related-work map, term-by-term analysis of EVERY numbered equation, cropped original figures with element-by-element readings, and a critical evaluation (methodology audit, independent conclusions, alternative explanations). Use when the user provides a paper PDF or arXiv link and asks to read/analyze it or make a report — e.g. "이 논문 읽어줘", "논문 분석 리포트 만들어줘", "PaperKraken으로 읽어줘", "analyze this paper". Do not use for interactive tutoring (that is PaperMentor) or shallow summaries.
---

# PaperKraken

Take one paper PDF as input and produce one **complete, tutorial-grade comprehension report PDF**.
The goal is not a summary: a reader should be able to fully understand the paper and evaluate it critically from this report alone.

Core principles:
- The methodology follows `references/methodology.md` (Nature's 3-phase / 7-step framework).
- Report structure and HTML rules follow `references/report-template.md`.
- Equation analysis follows `references/equation-analysis.md` — analyze **every numbered equation**, one by one.
- Web-augmented background knowledge MUST pass the verification protocol in `references/verification.md`. Unverified external claims are either dropped or explicitly badged as unverified.
- The output PDF must have no parsing errors, no broken glyphs (tofu), no broken math, no clipped pages — and this is confirmed by a **mandatory visual QA step** before reporting completion.

## Inputs

1. **Paper PDF path** (required). If given an arXiv URL, download the PDF first (`https://arxiv.org/pdf/<id>`).
2. **Language**: `ko` or `en`. If the user did not specify, ask with AskUserQuestion — Korean vs English only (ask nothing else: depth is always tutorial-grade, equations always all, figures always included).

Language rule: write the report prose in the chosen language, but keep equations, symbols, model names, and natural English technical terms (loss, gradient, attention, objective, ...) in English.

## Workflow

### Step 0 — Session setup

```bash
# Output directory: next to the paper PDF
OUT="<paper-dir>/paperkraken-<paper-slug>"
mkdir -p "$OUT/figures"
cp -r <skill-dir>/assets "$OUT/assets"
# Renderer dependency (one-time; tiny driver package, no browser download)
npm ls -g playwright-core >/dev/null 2>&1 || npm install -g playwright-core
```

`<skill-dir>` is the directory containing this SKILL.md — when installed as a plugin this resolves as `${CLAUDE_PLUGIN_ROOT}` (≈ `~/.claude/plugins/cache/paperkraken/...`); when symlinked into `~/.claude/skills/` it is that directory. The assets bundle Pretendard/Satoshi fonts, a local MathJax (SVG math), and a local Paged.js (page numbers, running headers, TOC page references) so rendering never depends on a CDN.

### Step 1 — Read the paper in full

Read the entire PDF with the Read tool (use the `pages` parameter in chunks for papers over 10 pages). While reading, record:

- **Paper type**: ML/computational, experimental science (wet-lab, physics, psychology...), theory/mathematics, or clinical/human-subjects. This selects the Step-4 audit checklist variant (methodology.md) and equation cards vs theorem/proof cards (equation-analysis.md). Mixed papers combine variants.
- Section structure and the core research question/hypothesis (usually at the end of the introduction)
- A list of **all numbered equations** (number, location, one-line role) — miss none. For theory papers, the list of all theorems/lemmas instead.
- **Abstract-number ledger**: every quantitative claim in the abstract (and headline claims in the intro/conclusion) with where its source table/figure should be — Step 6's internal-consistency audit checks each one.
- All figures/tables and what each one is meant to prove
- Key cited prior work (candidates for the related-work map)
- Claimed contributions, limitations, and whether data/code are released
- Candidate **sticking points**: places where you yourself had to re-read — overloaded symbols, silently reused variables, unstated conventions. These feed the report's "common sticking points" section.

### Step 2 — Extract figures

```bash
# Detect candidates (caption-based)
uv run --with pymupdf python <skill-dir>/scripts/extract_figures.py list <paper.pdf>
# Auto-extract
uv run --with pymupdf python <skill-dir>/scripts/extract_figures.py auto <paper.pdf> -o "$OUT/figures"
```

Open every extracted PNG with the Read tool and **verify it visually against these pass/fail criteria** — a crop FAILS if any of the following holds, and must be re-cropped before use:

- Characters or plot elements cut off at ANY edge (e.g. a caption reading "~~T~~able 2:" or "~~E~~nglish-to-German" means the left edge clipped — this exact defect shipped in an early sample report; check edges character by character)
- Stray content bleeding in from adjacent sections/columns (section headings, body-text lines, a neighboring figure's edge)
- The figure's own axis labels, legends, or sub-titles missing
- Resolution visibly blurry at print size

Re-crop manually when needed:

```bash
uv run --with pymupdf python <skill-dir>/scripts/extract_figures.py crop <paper.pdf> --page N --rect x0,y0,x1,y1 -o "$OUT/figures" --name figure3
# Full-page render with a coordinate grid overlay, for picking crop rects
uv run --with pymupdf python <skill-dir>/scripts/extract_figures.py page <paper.pdf> --page N -o "$OUT/figures" --grid
```

Always secure the representative figure (method/architecture/pipeline). For results, select 2–4 plots that Step 5 (independent conclusions) will use. Every figure in the report must be an original crop — never redraw or substitute a generated diagram.

**Tables are different**: re-typeset paper tables as HTML by default instead of cropping them (crops of tables clip and blur easily) — see the "Figures vs tables" rule in `references/report-template.md`. Verify every transcribed cell against the source.

### Step 3 — Web-verified background research

Follow `references/verification.md`:
- Research the prerequisite concepts the paper assumes and its key cited prior work via WebSearch/WebFetch (prefer arXiv abstract pages).
- Only include cross-verified content, each item with a source footnote.
- For papers with many citations, fan out per-paper research with the Agent tool in parallel.

### Step 4 — Write the report HTML

Write `$OUT/report.html` exactly per `references/report-template.md`. Key points:

- The Nature 3-phase / 7-step structure is the report's skeleton (the report also teaches the methodology itself to the reader up front).
- Phase 0 (prerequisite ladder + related-work map) comes before Phase 1 so background is filled first.
- Inside Step 4, an "equation-by-equation analysis" subsection: one card per numbered equation, following `references/equation-analysis.md` (theorem/proof cards for theory papers).
- A "common sticking points" section (Top 3–5 anticipated confusions with resolutions) closes Phase 2 — sourced from the sticking points recorded in Step 1.
- A "Run it yourself" appendix: 2–4 numpy snippets that reproduce the equation cards' numeric examples (eligibility rules in `references/report-template.md`). After writing the HTML, verify them — every snippet must PASS before rendering:

```bash
uv run --with numpy python <skill-dir>/scripts/verify_snippets.py "$OUT/report.html"
```

If a snippet fails, the card's numeric example itself may be wrong — fix whichever is incorrect (never tweak the printed output to match a buggy snippet).
- Math must be LaTeX (`\( \)`, `\[ \]`) — never ASCII approximations. Transcribe source equations exactly; if PDF extraction was broken, mark the equation as reconstructed.
- Insert figure images via relative `figures/` paths, with the element-by-element reading directly beneath each.

### Step 5 — Render the PDF

```bash
node <skill-dir>/scripts/render_pdf.mjs "$OUT/report.html" "$OUT/<paper-slug>-report.pdf"
# Then inject the PDF outline (viewer-sidebar bookmarks from the report's h2/h3):
uv run --with pymupdf python <skill-dir>/scripts/add_bookmarks.py "$OUT/report.html" "$OUT/<paper-slug>-report.pdf"
```

The render script launches Playwright Chromium, waits for the template's `window.__PK_DONE` flag (MathJax typeset + Paged.js pagination complete), then prints. If it warns that the flag was never set, treat the output as broken and debug (usually a MathJax parse error or a removed script tag).

The bookmark script prints how many entries it added and warns about any heading it could not locate — a couple of missed h3s is tolerable; zero or near-zero entries means something is wrong (run it again after checking the HTML heading tags).

### Step 6 — Visual QA (never skip)

```bash
pdftoppm -png -r 80 -f 1 -l 3 "$OUT/<slug>-report.pdf" "$OUT/qa"
# Also render: one math-heavy page, EVERY page containing a figure/table crop,
# and the final page.
```

Open the rendered PNGs with Read and check:
- [ ] No broken Korean/Latin glyphs (□ tofu)
- [ ] Equations rendered as SVG (raw `\frac{...}` text visible = MathJax failure)
- [ ] Every figure crop passes the Step-2 crop criteria **as printed** (no clipped edge characters, no stray content)
- [ ] Page numbers present on content pages, absent on the cover; running header shows the current Phase
- [ ] TOC page numbers are non-zero and plausible
- [ ] No page is more than ~60% empty and no near-blank orphan pages (a heading or a two-line tail alone on a page = fail)
- [ ] No heading orphaned at the bottom of a page with its body on the next
- [ ] No table overflows the page width
- [ ] Bookmark script reported a plausible entry count (roughly one per h2/h3)
- [ ] `verify_snippets.py` passed on the final HTML (re-run if the appendix was edited after the first check)

On any failure: fix the HTML → re-render → re-check. Do not report completion before QA passes.

### Step 7 — Deliver

The final message must include: the PDF path, total page count, a composition summary (number of equations analyzed, figures included, web-verified background items), and the paper's core idea in 3–4 sentences.

## Failure handling

- **Chromium not found**: suggest `npx playwright install chromium`, then retry.
- **`playwright-core` missing / npm broken**: `npm install -g playwright-core`. As a last resort, `bash <skill-dir>/scripts/render_pdf.sh` is a legacy one-shot CLI fallback — but it cannot wait for Paged.js, so when using it, remove the `paged.polyfill.js` script tag and the `window.PagedConfig`/`PagedPolyfill` lines from the HTML first (the report then renders correctly, just without page numbers/TOC numbers).
- **Paged.js misbehaves** (hangs, mangled layout): same degradation path — strip the Paged.js script tag + config lines and re-render with `render_pdf.mjs`; everything except page numbers/running headers/TOC numbers still works.
- **PyMuPDF extraction fails (e.g. scanned PDF)**: render full pages with `pdftoppm`, read them visually, and obtain figures via page mode + manual crop.
- **Math not rendered / renderer times out**: raise `PK_TIMEOUT` (ms, default 120000) for very long reports; check for MathJax parse errors (`<`/`>`/`&` in TeX — see equation-analysis.md).
- **Background item fails verification**: drop it by default; if truly essential, include it with an explicit "⚠ unverified — model knowledge" badge.
