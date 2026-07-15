# Report HTML rules

Start `$OUT/report.html` from the skeleton below. `assets/` and `figures/` must sit in the same directory as report.html (copied in SKILL.md Step 0). Use the scripts block, CSS, and MathJax/Paged.js config **as-is**; fill in only the `<!-- CONTENT -->` part.

The template uses locally bundled MathJax (SVG math — no font issues) and Paged.js (page numbers, running headers, TOC page references, fine-grained page-break control). The `window.__PK_DONE` flag at the end of the script chain is what `scripts/render_pdf.mjs` waits for — never remove it.

## Skeleton

```html
<!DOCTYPE html>
<html lang="ko"> <!-- lang="en" for English reports -->
<head>
<meta charset="utf-8">
<title>PaperKraken — {paper title}</title>
<script>
window.PagedConfig = { auto: false };
MathJax = {
  tex: { inlineMath: [['\\(','\\)']], displayMath: [['\\[','\\]']], tags: 'none' },
  svg: { fontCache: 'none' },
  startup: {
    pageReady: () => MathJax.startup.defaultPageReady()
      .then(() => window.PagedPolyfill.preview())
      .then(() => { window.__PK_DONE = true; })
  }
};
</script>
<script src="assets/mathjax/tex-svg.js"></script>
<script src="assets/pagedjs/paged.polyfill.js"></script>
<style>
@font-face { font-family:'Pretendard'; src:url('assets/fonts/PretendardVariable.woff2') format('woff2-variations'); font-weight:100 900; }
@font-face { font-family:'Satoshi'; src:url('assets/fonts/satoshi/Satoshi-400.woff2') format('woff2'); font-weight:400; }
@font-face { font-family:'Satoshi'; src:url('assets/fonts/satoshi/Satoshi-500.woff2') format('woff2'); font-weight:500; }
@font-face { font-family:'Satoshi'; src:url('assets/fonts/satoshi/Satoshi-700.woff2') format('woff2'); font-weight:700; }

:root {
  --ink:#1a1c20; --sub:#5a6070; --line:#e3e6ec; --accent:#0f4c81; --accent-soft:#eef4fa;
  --warn:#9a6700; --warn-soft:#fff8e6; --ok:#1a7f37;
}
* { box-sizing:border-box; }
html { font-size:10.5pt; }
body {
  font-family:'Satoshi','Pretendard',sans-serif; color:var(--ink);
  margin:0; line-height:1.75; word-break:keep-all; overflow-wrap:break-word;
}
@page {
  size:A4; margin:16mm 16mm 18mm 16mm;
  @bottom-center { content: counter(page); font-family:'Satoshi',sans-serif; font-size:8.5pt; color:#5a6070; }
  @top-right { content: string(runhead); font-family:'Satoshi','Pretendard',sans-serif; font-size:8pt; color:#5a6070; letter-spacing:.06em; }
}
@page cover { @bottom-center { content: none; } @top-right { content: none; } }
.cover { page: cover; }
h2 { string-set: runhead content(text); }
.phase h2 { string-set: runhead content(text); }

h1,h2,h3,h4 { line-height:1.35; word-break:keep-all; }
h1 { font-size:1.9rem; margin:0 0 .3rem; }
h2 { font-size:1.35rem; margin:2.2rem 0 .8rem; padding-bottom:.35rem; border-bottom:2px solid var(--ink); break-after:avoid; }
h3 { font-size:1.12rem; margin:1.6rem 0 .6rem; color:var(--accent); break-after:avoid; }
h4 { font-size:1rem; margin:1.2rem 0 .4rem; break-after:avoid; }
p { margin:.55rem 0; }
code { font-family:'NanumGothicCoding','D2Coding',monospace; font-size:.92em; background:#f4f5f7; padding:.08em .35em; border-radius:4px; }

/* Cover */
.cover { display:flex; flex-direction:column; justify-content:center; }
.cover .kicker { color:var(--accent); font-weight:700; letter-spacing:.12em; text-transform:uppercase; font-size:.85rem; }
.cover .meta { color:var(--sub); margin-top:1.2rem; font-size:.95rem; }
.cover .meta div { margin:.2rem 0; }
.cover .toc-box { margin-top:2.5rem; border-top:1px solid var(--line); padding-top:1rem; }

/* Table of contents (works on cover or its own section) */
ul.toc { list-style:none; padding:0; font-size:.95rem; }
ul.toc li { margin:.28rem 0; }
ul.toc li.toc-sub { padding-left:1.2rem; font-size:.9rem; color:var(--sub); }
ul.toc a { color:inherit; text-decoration:none; }
ul.toc a::after { content: target-counter(attr(href), page); float:right; color:var(--sub); }

/* Phase banner & steps */
.phase { break-before:page; background:var(--ink); color:#fff; padding:.9rem 1.2rem; border-radius:10px; margin:0 0 1.4rem; }
.phase .ph-num { font-size:.8rem; letter-spacing:.15em; text-transform:uppercase; opacity:.75; }
.phase h2 { border:none; color:#fff; margin:0; padding:0; }
.step-tag { display:inline-block; background:var(--accent-soft); color:var(--accent); font-weight:700; font-size:.8rem; padding:.15rem .6rem; border-radius:999px; margin-bottom:.2rem; }
.howto { background:var(--accent-soft); border-left:4px solid var(--accent); padding:.7rem 1rem; border-radius:0 8px 8px 0; margin:.8rem 0; font-size:.95rem; break-inside:avoid; }
.howto .howto-label { font-weight:700; color:var(--accent); font-size:.8rem; letter-spacing:.08em; text-transform:uppercase; }

/* Equation cards — the card itself MAY break across pages (prevents huge
   whitespace); only its atomic sub-blocks avoid breaking. */
.eq-card { border:1px solid var(--line); border-radius:12px; padding:1rem 1.2rem; margin:1.1rem 0; }
.eq-card .eq-head { break-inside:avoid; break-after:avoid; }
.eq-card .eq-title { font-weight:700; font-size:1.02rem; margin-bottom:.4rem; }
.eq-card .eq-display { background:#fafbfc; border-radius:8px; padding:.6rem .8rem; margin:.5rem 0; overflow-x:auto; break-inside:avoid; }
.eq-card .eq-sec { font-weight:700; font-size:.82rem; color:var(--sub); letter-spacing:.06em; text-transform:uppercase; margin:.8rem 0 .25rem; break-after:avoid; }
.eq-card table { width:100%; border-collapse:collapse; font-size:.92rem; }
.eq-card td, .eq-card th { border-top:1px solid var(--line); padding:.35rem .5rem; vertical-align:top; text-align:left; }
.eq-card tr { break-inside:avoid; }
.eq-dep { font-size:.9rem; color:var(--sub); background:#f7f8fa; border-radius:8px; padding:.45rem .7rem; break-inside:avoid; }

/* Figures */
figure { margin:1.2rem 0; break-inside:avoid; }
figure img { max-width:100%; border:1px solid var(--line); border-radius:8px; display:block; margin:0 auto; }
figcaption { font-size:.88rem; color:var(--sub); margin-top:.45rem; text-align:center; }
.fig-read { border:1px solid var(--line); border-top:none; border-radius:0 0 10px 10px; padding:.7rem 1rem; margin-top:-.4rem; font-size:.94rem; }
.fig-read dt { font-weight:700; color:var(--accent); margin-top:.5rem; font-size:.86rem; break-after:avoid; }
.fig-read dd { margin:0.1rem 0 0 0; }

/* Verification badges & footnotes */
.badge-v { color:var(--ok); font-weight:700; font-size:.82rem; }
.badge-u { display:inline-block; background:var(--warn-soft); color:var(--warn); font-weight:700; font-size:.78rem; padding:.05rem .5rem; border-radius:999px; }
sup.kref a { color:var(--accent); text-decoration:none; font-weight:700; }

/* Plain tables (also used for re-typeset paper tables) */
table.plain { width:100%; border-collapse:collapse; font-size:.93rem; margin:.8rem 0; }
table.plain th { background:#f4f5f7; }
table.plain th, table.plain td { border:1px solid var(--line); padding:.4rem .6rem; text-align:left; vertical-align:top; }
table.plain tr { break-inside:avoid; }
.table-note { font-size:.85rem; color:var(--sub); margin-top:.2rem; }

/* Prerequisite ladder — number the rungs MANUALLY in the HTML ("1. 개념명").
   CSS counters reset when Paged.js fragments the .ladder across pages, printing
   "0." on continuation pages — do not use counters here. */
.rung { border-left:3px solid var(--accent); padding:.1rem 0 .6rem 1rem; margin:0 0 .6rem .4rem; break-inside:avoid; }
.rung .rung-title { font-weight:700; }
.rung .rung-title .no { color:var(--accent); }
.rung .unlocks { font-size:.88rem; color:var(--sub); }

/* Checklists / quotes */
ul.check { list-style:none; padding-left:.2rem; }
ul.check li::before { content:"☐ "; color:var(--accent); font-weight:700; }
blockquote { border-left:3px solid var(--line); margin:.8rem 0; padding:.2rem 0 .2rem 1rem; color:var(--sub); }

/* Common sticking points (FAQ) */
.stick { border:1px solid var(--line); border-left:4px solid var(--warn); border-radius:0 10px 10px 0; padding:.7rem 1rem; margin:.9rem 0; }
.stick .q { font-weight:700; }
.stick .lbl { font-weight:700; font-size:.78rem; color:var(--warn); text-transform:uppercase; letter-spacing:.06em; margin-top:.5rem; break-after:avoid; }

/* Manual page-break helper — Paged.js ignores inline break styles; use this class */
.pbreak { break-before:page; }

/* Run-it-yourself appendix */
.run-card { border:1px solid var(--line); border-radius:12px; padding:.9rem 1.1rem; margin:1rem 0; }
.run-card .run-title { font-weight:700; margin-bottom:.3rem; break-after:avoid; }
pre.runnable, pre.run-output { font-family:'NanumGothicCoding','D2Coding',monospace; font-size:.86rem; line-height:1.5; border-radius:8px; padding:.6rem .8rem; overflow-x:auto; margin:.4rem 0; break-inside:avoid; }
pre.runnable { background:#f4f5f7; }
pre.run-output { background:var(--accent-soft); border-left:3px solid var(--accent); }
.run-verified { font-size:.8rem; color:var(--ok); font-weight:700; }

mjx-container { break-inside:avoid; }
mjx-container[display="true"] { overflow-x:auto; overflow-y:hidden; max-width:100%; }
</style>
</head>
<body>
<!-- CONTENT -->
</body>
</html>
```

## Content order

1. **Cover** (`.cover`, no page number/header): kicker "PAPERKRAKEN READING REPORT", paper title (original + translated), authors/venue/year, meta (generation date, language, equation count analyzed, figure count), one-line summary — then a **structured table of contents** in `.toc-box` using `ul.toc` with `href="#section-id"` links (page numbers resolve automatically). Every Phase banner and major h2 needs a matching `id`.
2. **How to read this report**: intro to Cornwell's 7-step methodology (1–2 paragraphs + a 3-phase table); note that this document performs the 1–2 hours of expert critical reading and shows the process.
3. **Phase 0 — Background** (state that this is an addition outside the 7 steps):
   - Prerequisite ladder (`.ladder`): from the most primitive concept up to the paper's notation, in dependency order. Each rung: concept name → short explanation → **numeric example with real numbers** → which symbol/equation/claim of the paper it unlocks (`.unlocks`). Do not stop at broad labels like "linear algebra" — decompose into the paper's actual primitives.
   - Related-work map: lineage of approaches → each lineage's limitation → this paper's position. Attach `[K#]` verification footnotes.
4. **Phase 1** (`.phase` banner) — Steps 1, 2, 3. Each step opens with a `.step-tag` (e.g. "STEP 1") and a `.howto` box (what the reader is supposed to do at this step — quoting Cornwell's advice).
5. **Phase 2** — Step 4 (method dissection + all equation cards + methodology-audit checklist table), Step 5 (result figures/tables + independent reading).
6. **Common sticking points (Top 3–5)** — closes Phase 2. For each: the confusion a reader is likely to hit → why the paper's presentation invites that misreading → the resolution. Pick the spots where THIS paper's readers actually stall (a symbol overload, a silently reused variable, an unstated convention), not generic difficulties. Format per `.stick` block:
   ```html
   <div class="stick">
     <div class="q">Q. {the confusion, phrased as the reader would ask it}</div>
     <div class="lbl">왜 헷갈리는가</div><div>{what in the paper invites the misreading}</div>
     <div class="lbl">해소</div><div>{the resolution, referencing the exact equation/figure/section}</div>
   </div>
   ```
   (English reports: labels "Why it trips readers" / "Resolution".)
7. **Phase 3** — Steps 6, 7.
8. **Final insight + 7-question self-check** (`ul.check`).
9. **Appendix — Run it yourself**: 2–4 executable snippets that reproduce the numeric examples from the equation cards / prerequisite ladder, so the reader can verify the math on their own machine. Rules:
   - Eligibility: only self-contained examples reproducible in ≤ 12 lines of numpy — no training loops, no downloads, no GPU. If nothing qualifies, omit the appendix entirely (never force it).
   - Each snippet MUST print something, and the printed result must equal the numeric example already shown in the corresponding card — the snippet is the card's *proof*, not new material.
   - Stochastic examples must fix a seed (`np.random.default_rng(0)`) so output is deterministic.
   - Markup: a `.run-card` per snippet with a `.run-title` naming the card it verifies, then the exact pair
     ```html
     <pre class="runnable"><code>{python, HTML-escaped}</code></pre>
     <pre class="run-output">{exact stdout}</pre>
     ```
     `scripts/verify_snippets.py` executes every `runnable` block and diffs stdout against its `run-output` — the pair format is load-bearing, and escaping matters (`>` → `&gt;`).
   - Add a `.run-verified` line noting the snippets were machine-verified at generation time.
10. **Glossary** (`table.plain`).
11. **References**: paper bibliography entry + `[K#]` web-verified sources (title/authors/year/URL/date checked).

## Figures vs tables from the paper

- **Figures** (diagrams, architecture drawings, plots, attention maps): always the original crop image, per the figure block below. Never redraw.
- **Tables** (results tables, ablation tables): **re-typeset as HTML `table.plain` by default** — crops of tables clip easily and print blurrily. Verify every transcribed cell against the source page, and add a `.table-note` line: "Re-typeset from Table N of the paper; values verified against the original." Include a crop only when re-typesetting is infeasible (huge tables), and then it must pass the same crop QA as figures.

## Figure block format

```html
<figure>
  <img src="figures/figure2.png" alt="...">
  <figcaption>Figure 2 — {semantic caption; do not paste the original caption verbatim, strip broken hyphens/math}</figcaption>
</figure>
<dl class="fig-read">
  <dt>What this figure draws</dt><dd>...</dd>
  <dt>Reading order</dt><dd>Walk the arrows in execution order: the quantity each arrow carries, the transformation each box applies...</dd>
  <dt>In-figure symbols</dt><dd>All math/symbols printed inside the figure, in LaTeX, with definitions. If none, say so explicitly.</dd>
  <dt>What to observe</dt><dd>The design choice/contrast this figure encodes</dd>
  <dt>Connections</dt><dd>Which equations/claims in the body it supports</dd>
</dl>
```

(For Korean reports, translate the `dt` labels: 무엇을 그린 그림인가 / 읽는 순서 / 그림 속 기호 / 주목할 것 / 연결.)

Never write generic advice like "follow the arrows" — every sentence must be specific to this exact figure.

## Page-density rules

The sample-report failure mode to avoid: `break-inside:avoid` on large blocks pushes them wholesale to the next page, leaving half-empty pages and even near-blank orphan pages.

- Equation cards and `.fig-read` blocks are allowed to break across pages (the CSS above already encodes this); only their atomic sub-blocks (equation display, single table row, heading+first-line) stay together.
- Use `break-before:page` ONLY on `.phase` banners and the cover by default. Exception: when QA shows a block stranding a small tail on the next page (e.g. a table's last 1–2 rows alone before a forced phase break), start that block on a fresh page — trading one moderately-shorter page for one near-blank page is always the right trade. **Break properties MUST live in the stylesheet** (the skeleton ships a `.pbreak { break-before:page; }` helper class) — Paged.js builds its fragmentation rules from stylesheets and silently ignores inline `style="break-before:..."` attributes.
- A trailing paragraph tail of 2–3 lines alone on a page: shorten the paragraph (trim ~2 lines of prose) rather than adding breaks.
- A full-page figure is acceptable; a page that is >60% empty is not — if QA finds one, apply the two fixes above or reorder content.
- Avoid CSS counters anywhere content may split across pages (see the ladder note above) — Paged.js resets them on fragment continuation.

## Writing cautions

- Language: natural prose in the chosen language; keep equations/symbols/model names/natural English technical terms in English.
- No ISO timestamps, internal tool names, or generation-process chatter in the report.
- Keep tables narrow enough for the page (≤5 columns recommended).
- Write the whole report as a single HTML file regardless of length (the render script handles it).
- Never remove the `window.__PK_DONE` chain or the two `<script src="assets/...">` tags — the renderer waits on that flag.
