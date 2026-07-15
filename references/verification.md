# Verification protocol for web-augmented background knowledge

The prerequisite ladder and related-work map contain knowledge from outside the paper. The user's explicit concern: **no false or erroneous content may slip in.** Therefore external knowledge is included only after passing this protocol.

## Verification tiers

Every external item lands in one of three tiers:

| Tier | Condition | Marking |
|---|---|---|
| ✅ Verified | Passed the procedure below | Source footnote |
| ⚠ Unverified | Failed verification but essential for understanding | "⚠ unverified — model knowledge" badge; absence of source stated |
| (Omitted) | Failed verification and not essential | Excluded from the report |

## Procedure

### Cited prior work (related-work map)

1. Get the exact title/authors/year from the paper's reference list (actually read the references section — never guess from in-text citation numbers).
2. Find the work via WebSearch, then **WebFetch its arXiv abstract page or publisher page directly.**
3. The summary written into the report may contain only what the abstract confirms. Do not state details (numbers, method specifics) beyond the abstract unless you actually read the full source.
4. Cross-check title/year/authors against the abstract page. **Never fabricate bibliographic details for a work you could not find.**

### Background concepts (prerequisite ladder)

1. Mathematical definitions (e.g. KL divergence, softmax) may come from model knowledge, but after writing the definition, **self-check it with a small numeric example** (plug in real numbers and verify the arithmetic). A passing check counts as ✅.
2. Empirical/historical claims ("X first proposed Y", "Z is the standard benchmark") require 2+ independent web sources, or the original paper's abstract.
3. Current-state claims (model sizes, SOTA numbers) must be web-confirmed and dated ("as of <check date>"). If unconfirmable, omit.

### Cross-checking rules

- Two sources that cite each other do not count as two independent sources.
- Wikipedia is a first-pass check only; re-confirm against the original paper/official docs when possible.
- Never conclude from search-result snippets alone — WebFetch the actual page.

## Citation marking

- In-text footnotes as `[K1]`, `[K2]`, ... (distinct from the paper's own citations `[1]`, `[2]`).
- References section at the end lists each: title, authors, year, URL, date checked.
- Content taken from the paper itself needs no footnote; footnotes are only for knowledge from outside the paper.

## Parallel research

For many prior works, fan out per-paper research with the Agent tool (general-purpose). Pass this protocol verbatim in each subagent's prompt (read abstracts directly, cross-check bibliography, no fabrication), and re-verify any suspicious returned item yourself with WebFetch.
