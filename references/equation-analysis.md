# Equation analysis rules (inherited from PaperMentor)

Analyze **every numbered equation** in the paper. Also include unnumbered inline equations when they are decisive for understanding. Each equation gets one "equation card" HTML block (`.eq-card` in report-template.md).

## Card structure (fixed order)

1. **Title**: meaningful name — number. E.g. `Training objective — Eq. (6)`, `Attention weight — Eq. (2)`. Never a bare title like `Equation (6)`.
2. **The equation**: transcribe the paper's equation **exactly** as LaTeX display math. Preserve variables, subscripts/superscripts, summation/integral limits, conditioning bars, expectation distributions, and constants. If PDF extraction was broken and you reconstructed it, mark it: "source extraction incomplete; reconstructed from context".
3. **Symbol table**: every symbol appearing in this equation (not just first occurrences), with type (scalar/vector/matrix/distribution/function) and dimensions where known.
4. **Term-by-term role decomposition**: split the equation into meaningful terms/factors and explain each term's **functional role**. A good explanation answers:
   - What does this term compare / reward / penalize / normalize / weight / constrain / reconstruct / predict / marginalize / propagate?
   - Why is it included? What behavior changes if it is removed or scaled up?
   - Which claim in the surrounding text does it connect to?

   Example: for $\|\hat{o}_t - o_t\|_2^2$, do not stop at "$\hat{o}_t$ is the predicted observation." Say that the term penalizes the distance between the reconstructed and actual observation, so minimizing it improves reconstruction fidelity at time $t$.
5. **Intuition**: what the equation does, in one or two sentences without math. Where possible, a small numeric example with real numbers (e.g. `[1,2]·[3,4]=11`).
6. **Dependencies**: which earlier equations/definitions/assumptions this comes from, and which later equations use it. Format: `Eq. (3) → this → substituted into Eq. (7)`.

## Theorem/proof cards (theory papers)

When the paper's core content is theorems/lemmas rather than computational equations, replace equation cards with **theorem cards** — same `.eq-card` HTML, adapted sections (fixed order):

1. **Title**: meaningful name — Theorem/Lemma/Proposition number. E.g. `Convergence guarantee — Theorem 2`.
2. **Statement**: exact LaTeX transcription of the statement.
3. **Assumptions table** (replaces the symbol table): each hypothesis → where the proof uses it → what breaks if it is dropped.
4. **Proof skeleton** (replaces term-by-term roles): the proof's moves in order, each transition named (induction, contradiction, union bound, Jensen, ...). Fill in steps the paper waves away and mark them as filled-in.
5. **Intuition**: why it is true in one or two sentences; a small concrete instance, and — when instructive — what goes wrong in a boundary case with an assumption removed.
6. **Dependencies**: which lemmas feed this result, which later results use it.

The prohibitions below apply unchanged (no silent rewrites, no hidden assumptions, examples are not proofs).

## Derivations

When the paper moves from equation A to equation B, list the transitions **without skipping a single step**. Fill in intermediate steps the paper waves away ("it is easy to see"), and mark them as filled-in. Name the assumption used at each transition (independence, Jensen, triangle inequality, ...).

## Prohibitions

- Never replace math with ASCII approximations.
- Never silently rewrite a source equation (if it looks like a typo, note it in a footnote).
- Never list symbol definitions without the term-by-term roles.
- Never treat an example as a proof.
- Never hide assumptions.

## HTML/MathJax caveats

- Display math: `\[ ... \]`; inline: `\( ... \)`.
- HTML special characters: write `<` as `\lt`, `>` as `\gt`; use `&` only inside alignment environments (`aligned`). Violations cause MathJax parse errors → raw text in the PDF.
- Break long equations with `aligned` so they never exceed the page width.
