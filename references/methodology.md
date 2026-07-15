# Nature's 7-step critical paper-reading methodology

Source: Jacques Cornwell, "Seven steps for critically analysing research papers", *Nature* Career Column, 2026-06-09. https://www.nature.com/articles/d41586-026-01209-0

The report is a document that **performs this methodology on the reader's behalf**. Each step becomes a report section; for every step, (a) teach in one paragraph what the reader is supposed to do at this step, then (b) show the result of actually doing it for this paper.

## Phase 1 — The Aerial View (context gathering)

### Step 1. Gain a broad overview
"Resist the urge to dive straight into dense methodology. Instead, scan the abstract and review the figures."
- Dissect the abstract sentence by sentence: label background / method / result / significance.
- Insert the cropped representative figure (method/architecture/pipeline) and read it element by element: what every box/arrow/symbol means, what quantity flows along each arrow in execution order, and transcribe any in-figure math to LaTeX with definitions.
- By the end of this step the reader should grasp the study design, tools, and scope.

### Step 2. Identify the core research question
- Locate the specific hypothesis/question being tested (usually at the end of the introduction).
- Present it as **original quote + translation (if the report language differs) + plain-language unpacking**, and keep referring back to it throughout the report.
- If the paper never states it explicitly, reconstruct it — and say clearly that it is a reconstruction, not a quoted sentence.

### Step 3. Map the knowledge gaps
- Summarize the state of the field from the introduction / related work.
- Which puzzle piece does this paper add: the lineage of existing approaches → each lineage's limitation → where this paper sits.
- Build the map primarily from works the paper actually cites; for the key prior works, apply web verification (verification.md) and summarize each in 1–3 self-contained sentences. A reader who has not read those papers must still be able to follow this one.

## Phase 2 — The Interrogation (detailed evaluation)

### Step 4. Assess the methodology
Evaluate whether the experimental design matches the research question. **Use the audit checklist matching the paper type** identified in SKILL.md Step 1 (mixed papers: combine rows from each applicable variant):

**ML / computational**
- Appropriateness of the tools/models/datasets used
- Number of seeds and repeat runs; variance/confidence intervals reported?
- Negative control = strong contemporary baselines; positive control = systematic ablations
- Raw datasets in public repositories? Training/eval code released?

**Experimental science (wet-lab, physics, psychology, ...)**
- Sample size justified by a statistical power calculation?
- Positive and negative controls present?
- Randomization / blinding where applicable; ethics approval (IRB/IACUC) stated?
- Raw data deposited publicly? Analysis scripts released?

**Theory / mathematics**
- Do the definitions match standard usage (flag silent redefinitions)?
- Are the assumptions of each theorem explicit, and are they reasonable/checkable?
- Proof completeness: which steps are deferred to appendix or "left to the reader"?
- Does the claimed generality match what is actually proven?
- Worked examples given? Do boundary cases / potential counterexamples get addressed?

**Clinical / human subjects**
- Cohort size, selection criteria, and pre-registration
- Endpoints: pre-specified vs post-hoc analyses
- Confounder adjustment; conflicts of interest and funding (feeds Step 7)

This step contains two large subsections:
1. **Method dissection**: explain the method in pipeline order, with the major figure crops.
2. **Equation-by-equation analysis**: every numbered equation in the paper, one card each, per equation-analysis.md. It is normal for this to be the longest section of the report. **Theory papers**: use theorem/proof cards instead (see the variant in equation-analysis.md).

### Step 5. Reach independent conclusions
"Skip the discussion section; examine results and figures directly to form your own interpretation before reading the author interpretations."
- Insert the result figures (original crops) and tables (re-typeset as HTML, cell-verified — see report-template.md) and describe what the data alone shows, **with the authors' interpretation deliberately excluded**.
- For each result, separate "statements this number/plot itself supports" from "things this data alone cannot tell us".
- Give the reader 2–3 questions they should ask themselves when looking at each figure with the discussion covered up, so they can practice the skill.

## Phase 3 — The Verdict (final analysis)

### Step 6. Reconcile conclusions
- Put the Step-5 independent reading side by side with the authors' discussion/conclusion.
- Point out overstated claims, assertions the data does not support, and quietly generalized scope — citing specific sentences and numbers, not vague suspicion.
- Also state where the authors' claims and the independent reading agree (fair assessment).

**Internal-consistency audit (mandatory, not optional):**
- Cross-check **every number in the abstract** against its table/figure source, using the ledger recorded in SKILL.md Step 1. (This is how the sample report caught the paper stating "41.0 BLEU" in §6.1 while Table 2 says 41.8.)
- Recompute simple arithmetic the paper claims: deltas ("+2 BLEU over prior best"), percentages, speedups, parameter counts.
- Check that values repeated across sections agree (hyperparameters in text vs tables, dataset sizes in §Setup vs §Results).
- Report each mismatch with **both locations quoted** (e.g. "§6.1 says X; Table 2 says Y"). If everything matches, say so — a clean audit is also a finding.

### Step 7. Consider alternative explanations
- Confounders: could something else explain the results?
- Limitations the authors acknowledge vs limitations they do not.
- Conflicts of interest and funding sources, if disclosed.

## Closing sections (beyond the 7 steps)

- **Final insight**: reconstruct the paper's core contribution in 3–4 sentences. Then a self-check list of 7 questions (one per step) the reader should be able to answer in their own words.
- **Glossary**: technical terms used in the report, alphabetized (가나다순 for Korean reports).
- **References**: the paper itself + every source used for web verification, with verification status.

Cornwell's time estimate: one to two hours per paper for an experienced reader. In the report's intro, state that this document performs those 1–2 hours of work and shows the process.
