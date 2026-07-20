# SCORED 2026 Reviewer-Critique Resolution Checklist

Last updated: 2026-07-18

This is the persistent checklist for revising the SCORED submission in `updated_scored/`.
Codex's permitted response is **writing and presentation revision only**: no annotation result, consumer
experiment, or regenerated dataset will be invented. The paper may report an author-performed verification
step only after the authors supply its actual sampling frame, procedure, and results. When the available
evidence cannot support a criticism directly, the paper will narrow the corresponding claim and state the
limitation.

## Critique sources covered

This checklist is the merged audit for all four advisor/reviewer-style rounds supplied as of 2026-07-18:

1. the original major-methodological-concerns review used to create Sections A--G;
2. the follow-up review headed **“Major Substantive Concerns”**; and
3. the follow-up review headed **“Methodological validity---the biggest risks”**; and
4. the submission-readiness review headed **“Must fix before submitting,”** together with its Fable rewrite
   proposals.

Every future compiled PDF must be checked against the entire merged checklist, including already-verified
items whose wording could regress during later compression. A concern is not closed merely because it
overlaps an earlier item; any additional requirement introduced by a later review remains open separately.

## Status legend

- `[ ]` Pending
- `[~]` Implemented in source and text-verified; clean PDF compilation still pending
- `[-]` Waiting for an author decision or factual answer
- `[x]` Resolved in source and verified in a clean compiled PDF

## Revision order

1. Correct motivation and evidence boundaries.
2. Repair contribution scope and related-work positioning.
3. Repair methodology reporting and quantitative-claim language.
4. Reframe and explain results, including null and unmet-criterion results.
5. Add explicit RQ answers and complete the presentation/terminology cleanup.
6. Resolve the newly merged substantive and methodological concerns in Section H.
7. Resolve the fourth-round coherence, claim-strength, audit, and readability concerns in Section I.
8. Resolve the PyPI sampling/ecosystem details and artifact inventory in Section G **last**, when the author
   supplies the missing facts or decision.
9. Recover the 11-page budget while keeping all content in this single document.
10. Run final reviewer-style submission QA against all four critique rounds.

---

## A. Motivation, consumers, and security-outcome claims

### [x] A1. Make the Log4Shell scenario explicitly hypothetical and remove XZ Utils

**Criticism:** Section 2.1 reads like an observed zero-critical-versus-Log4Shell result, although the
paper did not run an end-to-end vulnerability experiment. XZ Utils is not a good example because a
normal SBOM would not identify the maliciousness of a legitimate upstream release.

**Writing-only resolution:**

- Remove XZ Utils from the motivating scenario.
- Introduce Log4Shell as a **constructed operational scenario**, not a study result.
- Remove invented outcome language such as one artifact producing zero critical findings and the
  other producing an alert, unless it is explicitly attributed to prior work.
- Attribute the general connection between generator divergence and vulnerability results to the
  cited prior studies.
- State that this paper measures representation, population, and graph differences—not downstream
  vulnerability counts.

**Files:** `sections/02-background.tex`, `sections/01-introduction.tex`, `main.tex`

**Done when:** No sentence can be read as claiming that the 18-package study produced a Log4Shell or
vulnerability-count result.

**Implemented:** The scenario is now labeled constructed, XZ Utils and invented scanner outcomes are
removed, prior vulnerability-report findings are attributed to cited studies, and the abstract,
introduction, and background explicitly bound the present study to generator outputs and field population.

**Verified:** Compiled PDF `SCORED_2026_SBOM (1).pdf`, pp. 1--2, on 2026-07-18.

### [x] A2. Rename the “threat model” as an operational risk model

**Criticism:** The model contains no adversary.

**Writing-only resolution:** Replace “threat model” with “operational risk model” and define the risk
as benign producers and consumers making incompatible assumptions about an underspecified artifact.

**Files:** `sections/02-background.tex`

**Done when:** The section no longer implies an adversarial threat model.

**Implemented:** The subsection now defines a benign-producer/benign-consumer operational risk model and
explicitly excludes adversarial tampering.

**Verified:** Compiled PDF `SCORED_2026_SBOM (1).pdf`, p. 2, on 2026-07-18.

### [x] A3. Mark consumer-side effects as untested risks

**Criticism:** The paper centers consumers but does not inspect a consumer implementation.

**Writing-only resolution:**

- Replace assertions about what consumers *do* or *guess* with statements about what a consumer
  **cannot determine from the SBOM alone**.
- Use “may,” “potential,” and “interpretive risk” for downstream consequences.
- Add a threat-to-validity statement that consumer behavior was not empirically evaluated.
- Describe consumer inspection as future work, not part of the present contribution.

**Files:** `sections/01-introduction.tex`, `sections/04-specification-analysis.tex`,
`sections/05-tool-implementation.tex`, `sections/06-root-causes.tex`,
`sections/07-discussion.tex`, `sections/08-conclusion.tex`, `main.tex`

**Done when:** Every consumer claim is either directly entailed by missing information in the artifact
or explicitly labeled an untested downstream risk.

**Implemented:** Consumer-behavior assertions were rewritten as artifact-level information limits or
potential downstream risks across the abstract, background, specification analysis, tool analysis,
root-cause recommendations, discussion, and conclusion. A dedicated consumer/outcome coverage limitation
now identifies consumer inspection as future work.

**Verified:** Compiled PDF `SCORED_2026_SBOM (1).pdf`, pp. 1--2, 7--10, on 2026-07-18.

---

## B. Contribution scope and traceability

### [x] B1. Remove or tightly scope the “first systematic map” claim

**Criticism:** The firstness claim is unsafe, especially given Wang et al.'s closely related study.

**Writing-only resolution:** Replace firstness language with a bounded description such as
“a specification-centered map of population, conditionality, and interpretation boundaries across
CycloneDX 1.6, SPDX 3.0.1, and CISA guidance.”

**Files:** `sections/01-introduction.tex`, `main.tex`, `sections/08-conclusion.tex`

**Done when:** “first,” “first systematic,” and equivalent priority claims are absent unless narrowly
qualified and defensible.

**Implemented:** The priority claim is removed. The contribution now describes a specification-centered
map of normative force, conditionality, schema/prose boundaries, and producer/consumer semantics. The
stale commented contribution block was removed as well.

**Verified:** Compiled PDF `SCORED_2026_SBOM (2).pdf`, p. 2, on 2026-07-18.

### [x] B2. Make implementation traceability representative rather than exhaustive

**Criticism:** Contribution 2 promises that *each* divergence is traced to a specific permissive clause,
but the paper currently names only broad concept areas.

**Writing-only resolution:**

- Change “trace each observed divergence” to “trace representative divergences.”
- Add specification section numbers and/or existing requirement IDs for the strongest examples:
  provenance, dependency entries, scope/filtering, compositions, formulation, and SPDX profiles or
  relationships.
- Pair those clauses with the already-described tool behavior.
- State that the paper illustrates mechanisms rather than exhaustively mapping every implementation
  decision.

**Files:** `sections/01-introduction.tex`, `sections/04-specification-analysis.tex`,
`sections/05-tool-implementation.tex`, `sections/06-root-causes.tex`

**Done when:** Every retained “traceability” claim has at least one concrete clause/requirement reference
and no exhaustive claim remains.

**Implemented:** The contribution now promises selected rather than exhaustive traceability. Sections 4--6
anchor representative findings to CycloneDX sections and extracted-corpus IDs for dependency coverage,
empty graph entries, supplier, scope, compositions, and formulation; SPDX traceability uses the named Core
Relationship model. The synthesis explicitly states that the causal chains are representative.

**Verified:** Compiled PDF `SCORED_2026_SBOM (2).pdf`, pp. 2 and 7--10, on 2026-07-18.

### [x] B3. Differentiate explicitly from Wang et al.

**Criticism:** Wang et al.'s TOSEM paper studies the adherence gap at large scale, but the current paper
cites it only for tool selection.

**Writing-only resolution:** Add a delta paragraph explaining that Wang et al. measure compliance,
consistency, and accuracy over a large longitudinal SBOM corpus, whereas this paper focuses on a
specification-centered explanation of normative conditionality, schema/prose boundaries, and selected
implementation mechanisms. Do not claim that the present study is larger, more complete, or first.

**Files:** `sections/02-background.tex` or `sections/01-introduction.tex`, `references.bib`

**Done when:** A reviewer can identify the distinct research question and evidence type of the two papers
without inferring the difference themselves.

**Implemented:** The related-work section now contrasts Wang et al.'s two-stage, large-scale empirical
evaluation of compliance, consistency, and accuracy with this paper's specification-centered analysis and
selected source/output mechanisms. It explicitly describes the studies as complementary and disclaims
comparable coverage or statistical generalizability. The cited BibTeX entry's author names were corrected
against the published record.

**Verified:** Compiled PDF `SCORED_2026_SBOM (2).pdf`, pp. 2 and 11, on 2026-07-18.

---

## C. Requirement extraction, LLM scaling, and quantitative claims

### [x] C1. Bound the LLM-scaled corpus claims

**Criticism:** Human–NotebookLM kappa validates the pilot, not the remaining scaled extraction, yet the
full-corpus counts carry substantial argumentative weight.

**Writing-only resolution:**

- State explicitly that no held-out precision/recall estimate is available for the scaled remainder.
- Describe the 2,286 rows as the **extracted corpus**, not exhaustive ground truth.
- Rewrite results as “of the extracted CycloneDX/SPDX/CISA requirements.”
- State that the percentages characterize this corpus and depend on the extraction unit and protocol.
- Avoid treating small percentage differences as substantive.

**Files:** `main.tex`, `sections/01-introduction.tex`, `sections/03-methodology.tex`,
`sections/04-specification-analysis.tex`, `sections/07-discussion.tex`, `sections/08-conclusion.tex`

**Done when:** The paper never implies that pilot kappa is an error rate for the remaining corpus.

**Implemented:** The abstract, contribution statement, methodology, results, threats to validity, and
conclusion now describe a 2,286-row extracted corpus rather than exhaustive ground truth. The held-out audit
is framed as binary primary-unit agreement rather than a precision, recall, or exhaustive-coverage estimate.

**Verified:** The corrected contribution sentence and the remaining bounded-corpus language render in
`SCORED_2026_SBOM (4).pdf`, pp. 1, 3--4, and 10--11, on 2026-07-18.

### [-] C2. Make the corpus auditable without overpromising reproducibility

**Criticism:** NotebookLM is nondeterministic, and the paper currently promises no anonymous artifact.

**Writing-only resolution:**

- If an anonymous supplement/artifact accompanies submission, enumerate exactly what it contains:
  extracted corpus, codebooks, prompts, generated tables, generated SBOMs, and gap-test materials.
- If no artifact accompanies submission, remove “reproducible extraction” language and state that exact
  regeneration is limited by the closed, nondeterministic model.
- Do not claim an artifact exists until its submission mechanism is confirmed.

**Author decision:** An anonymous artifact or supplementary archive is planned. The paper currently marks
its final inventory and anonymous link as **TBA**. Both must be replaced only after the actual submission
package is known; this is tracked as G3 for end-stage resolution.

**Files:** `main.tex`, `sections/03-methodology.tex`, `sections/07-availability.tex`,
`sections/07-discussion.tex`

**Done when:** Availability and reproducibility claims match the files actually supplied to reviewers.

**Implemented so far:** “Reproducible extraction” is removed, the closed model's nondeterminism and limits
on exact regeneration are explicit, and `sections/07-availability.tex` contains the author-requested bold
TBA marker. Final closure awaits the archive inventory and anonymous link.

**Verified provisionally:** The nondeterminism limitation renders on p. 3 and the bold TBA marker on p. 11
of `SCORED_2026_SBOM (3).pdf`; C2 remains open by design.

### [x] C3. Explain what SPDX Stage 1 and Stage 2 kappa do—and do not—show

**Criticism:** SPDX Stage 1 kappa is 0.458. Stage 2 improves agreement, but this does not quantify extraction
coverage or recall.

**Writing-only resolution:**

- State that the table-driven SPDX format caused boundary disagreements during the initial pilot.
- Report the Stage 2 improvement as agreement after protocol refinement.
- Explicitly say this improvement does not estimate held-out extraction coverage.
- Avoid using kappa as proof that the complete SPDX corpus is exhaustive.

**Files:** `sections/03-methodology.tex`, `sections/07-discussion.tex`

**Done when:** The paper distinguishes inter-annotator agreement from extraction precision/recall.

**Implemented:** The methodology attributes the initial SPDX disagreement to table/cell extraction
boundaries, reports the Stage 2 improvement after protocol refinement, renames the table as pilot
requirement-extraction agreement, and states in the table note and threats to validity that kappa does not
estimate held-out precision, recall, or coverage.

**Verified:** Compiled PDF `SCORED_2026_SBOM (3).pdf`, pp. 3--4 and 10, on 2026-07-18.

### [x] C4. Make quantitative precision consistent with the evidence

**Criticism:** The paper calls raw cross-specification counts illustrative but uses their magnitudes as
strong evidence.

**Writing-only resolution:**

- Retain within-specification descriptive counts and percentages only where they support a broad pattern.
- Remove cross-specification magnitude comparisons that assume equivalent extraction units.
- Use wording such as “within our extracted corpus.”
- Explain that specification structure affects the number of extracted units.
- Add a rounding note to tables where displayed subtheme percentages do not sum exactly to theme totals.

**Files:** `sections/03-methodology.tex`, `sections/04-specification-analysis.tex`, generated table inputs if
their captions or notes require editing

**Done when:** The text does not simultaneously call counts non-comparable and use raw count differences as
precise cross-standard evidence.

**Implemented:** Counts are described as rows produced by specification-dependent extraction units;
interpretations are explicitly within-specification and within-corpus. The SPDX and CycloneDX tables use
compact rounding notes, while the included CISA pie chart identifies its 133-row extracted corpus directly
in the caption.

**Verified:** Compiled PDF `SCORED_2026_SBOM (3).pdf`, pp. 3 and 6--7, on 2026-07-18. Both rounding notes
render as compact single lines.

---

## D. Results and evidence–claim alignment

### [x] D1. Reframe the SPDX zero-failure schema-gap result as a null/control finding

**Criticism:** The SPDX table reports no failures and can be read as evidence against the paper.

**Writing-only resolution:**

- State plainly that the selected SPDX tools did not violate the evaluated rules when those rules applied.
- Explain that N/A means the construct was absent and the rule was not exercised; it is not a failure and
  not evidence of correctness for uninstantiated features.
- Remove or narrow the claim that the tested SPDX prose rules are practical “dead letters.”
- Separate two phenomena: violation of an applicable rule versus non-activation of an optional construct.

**Files:** `sections/05-tool-implementation.tex`, `sections/appendix1.tex`, `sections/07-discussion.tex`

**Done when:** The null result is visible, accurately interpreted, and incorporated into the conclusion.

**Implemented:** Section 5 now calls this a null/control finding, states that no selected applicable SPDX
rule was Unmet, and defines N/A as an absent, unexercised construct. The discussion and conclusion preserve
that boundary, and the appendix uses Met/Unmet/N/A rather than PASS/FAIL.

**Verified:** Compiled PDF `SCORED_2026_SBOM (6).pdf`, pp. 9--11 and 13, on 2026-07-18.

### [x] D2. Narrow the role of the 18-package dynamic study

**Criticism:** The study is described broadly but reports no component-overlap, graph-depth, or variance
metrics.

**Writing-only resolution:**

- Describe the dynamic study as a focused validation of selected field-presence and schema-gap criteria.
- Do not present it as a comprehensive divergence benchmark.
- State that it does not quantify inventory overlap, graph depth, or vulnerability-result variation.
- Use it to demonstrate mechanisms and concrete output patterns only.

**Files:** `main.tex`, `sections/01-introduction.tex`, `sections/03-methodology.tex`,
`sections/05-tool-implementation.tex`, `sections/07-discussion.tex`

**Done when:** The stated purpose of the dynamic study matches the results actually reported.

**Implemented:** The abstract, contribution statement, methodology, results introduction, and threats to
validity now describe focused field-presence and schema-gap checks and explicitly exclude inventory-overlap,
graph-depth, reproducibility, consumer-behavior, and vulnerability-result measurements.

**Verified:** Compiled PDF `SCORED_2026_SBOM (6).pdf`, pp. 1, 5, 8, and 11, on 2026-07-18.

### [x] D3. Discuss every unmet CycloneDX criterion

**Criticism:** The text discusses supplier and compositions but not the component-version result or every
other unmet row.

**Writing-only resolution:**

- Add a compact explanation for empty dependency entries, metadata supplier, component versions, and
  compositions.
- Explain the aggregation rule behind each table cell: for example, whether one versionless component is
  sufficient to mark a tool's criterion as unmet.
- Explain the SPDX-versus-CycloneDX component-version contrast without implying universal absence.
- Avoid calling an unmet CISA recommendation a schema violation.

**Files:** `sections/05-tool-implementation.tex`, `sections/appendix1.tex`

**Done when:** Every `FAIL`/unmet row is explained or the table wording is revised so it cannot be
misinterpreted.

**Implemented:** Section 5 explains empty dependency entries, document-level metadata supplier, component
versions, and compositions, including the 18-output counts. The aggregation is explicit: a tool-level cell
is Met only if every applicable output meets the rule, Unmet if any applicable output does not, and N/A only
if no output exercises the construct. The text distinguishes mandatory prose from CISA-derived/advisory
criteria and states that one versionless component makes an output Unmet.

**Verified:** Compiled PDF `SCORED_2026_SBOM (6).pdf`, pp. 8 and 13, on 2026-07-18.

### [x] D4. Rename PASS/FAIL where the test is not conformance

**Criticism:** “FAIL” can imply violation even when a criterion is advisory, CISA-derived, or outside schema
validation.

**Writing-only resolution:** Rename the presentation to “Met / Unmet / N/A,” or clearly define that FAIL
means failure of the study's criterion rather than schema invalidity or specification nonconformance.

**Files:** `sections/appendix1.tex`, `sections/05-tool-implementation.tex`

**Done when:** Table terminology cannot be mistaken for official conformance status.

**Implemented:** Both appendix tables now use Met/Unmet/N/A, define the terms, and state that the CycloneDX
cells are study criteria rather than schema-validity judgments.

**Verified:** Compiled PDF `SCORED_2026_SBOM (6).pdf`, p. 13, on 2026-07-18. Both tables and notes render
cleanly without clipping or overlap.

### [x] D5. Resolve the SPDX Lite Profile contradiction

**Criticism:** Section 4 says the Lite Profile removes ambiguity, while Section 5 says it produced no
measurable change in the evaluated outputs.

**Writing-only resolution:** Change “removes” to “is intended to reduce” or “provides a mechanism to reduce,”
then explain that benefits depend on tools actually declaring and implementing the profile.

**Files:** `sections/04-specification-analysis.tex`, `sections/05-tool-implementation.tex`

**Done when:** The specification capability and observed adoption result are complementary rather than
contradictory.

**Implemented:** Section 4 describes Lite as an intended mechanism whose benefit depends on declaration and
implementation. Section 5 treats the evaluated outputs as an adoption observation, not evidence that Lite
is ineffective.

**Verified:** Compiled PDF `SCORED_2026_SBOM (6).pdf`, pp. 6 and 8, on 2026-07-18.

### [x] D6. State the denominator for the CISA-derived field result

**Criticism:** “5 fields” is uninterpretable without the evaluated total.

**Evidence check:** The implementation originally labeled 11 checks, but the ``component version'' check
reads `CreationInfo.specVersion`, not a package's `packageVersion`. The valid CISA-derived denominator is
therefore **10**: SBOM author, software producer, component name, software identifier, component hash,
license, dependency relationship, tool name, timestamp, and generation context. The version-format check is
a non-CISA control and must be excluded.

**Writing-only resolution:** State “4 of 10 valid CISA-derived checks,” list the four common fields, define
the ten-field operationalization, and explain why the mislabeled document-format check is excluded.

**Files:** `sections/05-tool-implementation.tex`, possibly `sections/03-methodology.tex`

**Done when:** The numerator, denominator, and definition of the evaluated field set are explicit.

**Implemented:** Sections 3 and 5 now report 4/10, list the valid field set and the four common fields, and
explicitly exclude `CreationInfo.specVersion` from both numerator and denominator.

**Verified:** Compiled PDF `SCORED_2026_SBOM (6).pdf`, pp. 5 and 8, on 2026-07-18.

### [x] D7. Acknowledge the SPDX 2.3 versus 3.0.1 interpretive boundary

**Criticism:** Conversion back-checking handles representation loss but does not show that developers of
SPDX 2.3 tools made choices because of SPDX 3.0.1 latitude.

**Writing-only resolution:**

- State that Trivy and Syft's native behavior originates under SPDX 2.3.
- Describe conversion as enabling comparison against a common 3.0.1 representation baseline.
- Explicitly avoid attributing those tools' historical implementation decisions causally to SPDX 3.0.1.
- Limit the result to persistence or visibility of fields under the comparison mapping.

**Files:** `sections/03-methodology.tex`, `sections/05-tool-implementation.tex`,
`sections/07-discussion.tex`

**Done when:** The paper distinguishes comparability from causal traceability.

**Implemented:** The methodology, results, and threats to validity state that Trivy and Syft's behavior
originates under SPDX 2.3, conversion supplies only a common 3.0.1 representation baseline, and the evidence
supports field persistence/visibility rather than causal attribution to 3.0.1.

**Verified:** Compiled PDF `SCORED_2026_SBOM (6).pdf`, pp. 5, 8, and 11, on 2026-07-18.

### [x] D8. Distinguish document-level and component-level supplier consistently

**Criticism:** The current prose blurs `metadata.supplier` with per-component supplier fields.

**Writing-only resolution:** Define both terms once and use the exact level in every finding and table row.
Do not generalize absence at one level to absence at the other.

**Files:** `sections/02-background.tex`, `sections/04-specification-analysis.tex`,
`sections/05-tool-implementation.tex`, `sections/06-root-causes.tex`, `sections/08-conclusion.tex`

**Done when:** Every supplier claim identifies the relevant document or component level.

**Implemented:** Section 2 defines document-level `metadata.supplier` and component-level
`components[].supplier`; Sections 4, 5, 7, 8, the root-cause table, and the appendix use level-specific
terminology. SPDX claims identify package-level `suppliedBy` separately.

**Verified:** Compiled PDF `SCORED_2026_SBOM (6).pdf`, pp. 2 and 8--13, on 2026-07-18.

---

## E. Paper structure, related work, and presentation

### [x] E1. Add explicit answers to RQ1, RQ2, and RQ3

**Criticism:** The methodology lists RQs, but the results never explicitly answer them.

**Writing-only resolution:** Add a short, evidence-bounded answer at the end of the corresponding results
section or in the synthesis:

- **RQ1:** What the specifications constrain and where population/absence semantics remain open.
- **RQ2:** What schemas enforce and how optional/conditional features limit the baseline.
- **RQ3:** Which representative implementation choices occupy those open boundaries.

Repeat only a condensed synthesis in the conclusion.

**Files:** `sections/04-specification-analysis.tex`, `sections/05-tool-implementation.tex`,
`sections/06-root-causes.tex`, `sections/08-conclusion.tex`

**Done when:** The results include explicit, readily identifiable syntheses for RQ1, RQ2, and RQ3.

**Implemented:** Section 4 now gives evidence-bounded answers to RQ1 and RQ2, and Section 5 answers RQ3
while explicitly denying sole-cause and ecosystem-prevalence inferences.

**Verified:** Compiled PDF `SCORED_2026_SBOM.pdf` dated 2026-07-18, pp. 8 and 10. All three answers are
visible, legible, and bounded to the reported evidence.

### [x] E2. Deduplicate and validate the bibliography

**Criticism:** Benedetti/Cofano and O'Donoghue appear twice; Wang also has duplicate entries in the current
bibliography source.

**Writing-only resolution:** Keep one complete entry per work, update all citation keys, and remove the
duplicates. Preserve the final published venue/DOI form where available.

**Files:** `references.bib`, all citing section files

**Done when:** A clean bibliography contains one entry per cited work and no duplicate reference-list items.

**Implemented:** Duplicate O'Donoghue, Benedetti/Cofano, Wang, BOMs Away, and Java-SBOM records were
consolidated. Citations now use one key per work; the retained records use the published DOI form when
available, while the Benedetti et al. record uses the verified CoRR/arXiv metadata because no separate
version-of-record entry was located.

**Verified:** Compiled PDF `SCORED_2026_SBOM.pdf` dated 2026-07-18, p. 12, contains one entry per cited work;
the retained DOI/CoRR metadata renders correctly and no removed duplicate appears.

**Follow-up source audit:** The official ECMA-424 entry existed but was uncited. The introduction now cites
ECMA-424 at the first main-text mention of CycloneDX 1.6, and the BibTeX record points directly to Ecma
International's 1st-edition June 2024 PDF. The next clean Overleaf build must confirm that this reference and
the previously corrected SPDX/sbomqs records are regenerated in the bibliography.

### [x] E3. Verify the SPDX Online Tools citation in a clean build

**Issue already flagged:** The source cites `spdxonlinetools`; the final bibliography must resolve it without
depending on a stale auxiliary file.

**Writing-only resolution:** Verify the exact key in `references.bib`; add or correct the entry if a clean
build reports it undefined.

**Files:** `references.bib`, `sections/03-methodology.tex`

**Done when:** A clean build has no undefined `spdxonlinetools` citation.

**Verified:** The `spdxonlinetools` entry is present in `references.bib`, and compiled PDF
`SCORED_2026_SBOM (6).pdf` resolves the methodology citation as reference [26] on p. 5. No bibliography
addition is required.

### [x] E4. Apply minor language and table corrections

**Required corrections:**

- `lastest` → `latest`
- `tables to to express` → `tables to express`
- `table 1` → `Table~\ref{...}` or capitalized “Table 1”
- Add a rounding note for table totals/subtotals that differ by 0.1 percentage points.
- Remove stale commented five-tool contribution text where it creates maintenance risk.
- Remove visible blue revision coloring from the submission.

**Files:** `main.tex`, `sections/01-introduction.tex`, `sections/03-methodology.tex`,
`sections/04-specification-analysis.tex`, `sections/05-tool-implementation.tex`, relevant table sources

**Done when:** Text search and visual inspection find none of the listed defects.

**Implemented:** Source searches find none of the listed typos or blue revision markup; rounding notes are
present in the affected tables, four-tool terminology is consistent, and stale alternate title/abstract and
inline revision comments were removed. Clean PDF verification is pending.

**PDF check:** The listed text/color defects are absent in `SCORED_2026_SBOM.pdf` dated 2026-07-18, and the
advisor's `\sloppy` plus `\texttt{metadata.supplier}` edits render without clipping. E4 remains open because
the new pagination floats Appendix Table 8 ahead of Section A.2 and ahead of Table 7 on p. 13; restore table
order before marking this item complete.

**Initial ordering fix attempted:** `placeins` is loaded in `main.tex`, and a local `\FloatBarrier` follows
Appendix Table 7. The intent was to prevent Table 8 from overtaking Table 7 or the preceding appendix
subsections without altering either table's content.

**Follow-up PDF check:** `SCORED_2026_SBOM (1).pdf` dated 2026-07-18 shows that the barrier alone is
insufficient in the two-column layout: Table 8 still appears at the top of p. 13 before Sections A.2--A.4 and
Table 7. Table 8 is now additionally anchored at its source position with the `float` package's `[H]` placement.
Keep E4 open until this stronger fix is verified in a clean PDF.

**Final verification:** `SCORED_2026_SBOM (2).pdf` dated 2026-07-18 renders the appendix in the intended
sequence: Sections A.2, A.3, and A.4, followed by Table 7 and then Table 8. Visual inspection finds no clipping,
overlap, or table-order defect. E4 is closed.

### [x] E5. Meet the 11-page limit while preserving the new defenses

**Issue:** Earlier builds exceeded SCORED's 11-page inclusive limit. The CFP also prohibits changing ACM
fonts or margins.

**Writing-only resolution:**

- Keep the complete paper, references, prompts, and schema-gap tables in this one document, per the author's
  decision; do not move content to a separate supplement.
- Keep the central method limitation, null result, representative traceability, Wang delta, and RQ answers in
  the main paper.
- Recover space by deduplicating references, consolidating repeated thesis/takeaway language, tightening
  overlapping tables and prose, and improving page breaks before considering modest spacing changes.
- Preserve enough page buffer for the deferred G1, G2, H7, and G3/C2 wording; repeat the page-budget check
  after those author-supplied details are resolved.

**Files:** Entire active paper; all prompts and appendix tables remain in this document per the author's
decision.

**Done when:** A clean compiled main paper is at most 11 pages and remains legible.

**Progress:** Two conservative prose passes removed 753 source words while preserving the reviewer-facing
method, scope, evidence, and limitation statements. At that stage the supplied PDF was 14 pages; later builds
and the third pass are recorded below.

**Third progress pass:** Starting from the exact sources compiled into the 13-page
`SCORED_2026_SBOM (2).pdf`, a paper-wide pass removed 2,126 additional source words. It standardized subsection
summaries, consolidated repeated motivation/background/method descriptions, removed the redundant
specification-variation table, tightened the auditable source-anchor table, and corrected a stale CycloneDX
theme statement. Active-source word count fell from 10,045 to 7,919 without changing G1, G2, H7, or G3/C2.
No font, margin, or appendix-content reduction was used. E5 remains in progress until a clean PDF confirms an
11-page-or-shorter result and readable float placement.

**Later G2 placeholder expansion:** The provisional 25% agreement description adds 71 source words, bringing
the current active-source count to 7,990---still 2,055 below the sources compiled into the 13-page PDF. Exact
values will replace, rather than add to, the placeholders.

**Author-directed takeaway restoration:** Restoring the four original visual takeaways and adding five
missing subsection takeaways adds 323 source words, bringing the current count to 8,313---still 1,732 below
the 13-page PDF's source. Page-limit status requires recompilation because the nine boxes also add vertical
padding.

**Final G2 values:** Replacing the agreement placeholders with the confirmed compact fractions reduces the
current active-source count to 8,303, which is 1,742 below the 13-page PDF's source.

**Latest PDF verification:** `SCORED_2026_SBOM (3).pdf` reduces the paper from 13 to 12 pages without a font,
margin, clipping, overlap, or readability regression. Page 12 contains only the final CycloneDX appendix
results table and otherwise remains almost entirely blank. The remaining one-page deficit is therefore
primarily a float/appendix-placement problem rather than a need for another broad prose cut. Preserve the
appendix content and target its placement in the final compaction pass.

**Current presentation/compaction pass:** The three proposed conformance levels now begin as separate
paragraphs for scanability. Threats to Validity was consolidated from seven long blocks into five compact
scope-and-control statements. The required NotebookLM, empirical-scope, consumer-outcome, and SPDX-version
boundaries remain explicit, but each is paired directly with the evidence or mitigation that supports the
paper's bounded claims. Recompile to measure the page effect and verify the new paragraph breaks.

**Final verification:** `SCORED_2026_SBOM (5).pdf` is exactly 11 pages including references and appendices.
Page-by-page inspection finds no clipping, overlap, broken float order, margin/font alteration, or illegible
main-text element. All prompts and both schema-gap tables remain in the document; the nine takeaway boxes,
RQ syntheses, method boundaries, evidence chains, compact threats, and separated recommendation levels are
preserved. E5 is closed.

### [~] E6. Run final reviewer-style submission QA

**Verification checklist:**

- Main PDF ≤ 11 pages.
- ACM double-column font and margins remain unmodified; appendix text and tables are legible at 100% zoom.
- No undefined citations, references, or duplicate labels.
- No visible blue text.
- No five-tool claim in compiled content.
- No unsupported firstness, consumer-study, or vulnerability-experiment claim.
- Abstract, contributions, methods, results, threats, and conclusion use consistent scope.
- Table terminology and all denominators are explained.
- Anonymity and availability wording match the actual submission package.
- Review-copy DOI/ISBN/copyright metadata follows the SCORED template rather than displaying unresolved
  placeholder values.
- Every item in this document is either `[x]` or explicitly disclosed as a remaining limitation.

**Files:** Entire `updated_scored/` submission

**Done when:** Clean build and page-by-page visual inspection pass all checks.

**CFP audit:** The manuscript is a strong topical fit for the CFP's SBOM, standards, supply-chain tooling, and
dataset/benchmarking areas. The source uses anonymous double-column `acmart` without geometry, global-font, or
margin overrides, and the paper reports no human-subject involvement. The hard remaining format condition is
the 11-page inclusive limit. The CFP also says reviewers need not read appendices, so the next PDF check must
confirm that the main text still states every essential method boundary and result. The anonymous one-click
supporting-data link remains intentionally deferred under G3/C2.

**Latest QA pass:** `SCORED_2026_SBOM (5).pdf` passes the 11-page, anonymous ACM double-column, visual-render,
figure, table, takeaway-box, appendix-order, citation, reference, label, and bounded-claim checks. No unresolved
cross-reference, missing citation key, duplicate label/bibliography key, author/institution name, five-tool
claim, unsupported firstness claim, or visible rendering defect was found. The later source pass adds ACM
descriptions to both raster figures and explicitly empties DOI/ISBN fields because SCORED supplies no review
values and ACM provides publication identifiers after acceptance/eRights. E6 remains open for the held-out
audit results, author-supplied G1 sampling decision, G3/C2's anonymous artifact inventory/link, and a fresh
page-by-page PDF check.

**Current PDF audit:** `SCORED_2026_SBOM (6).pdf` is exactly 11 pages and passes full-page visual inspection:
no clipping, overlap, broken float order, illegible figure/table, undefined reference, stale dimension label,
or anonymity leak appears. The revised abstract, conclusion, recoding definition, primary-unit method,
conformance levels, and all nine takeaway boxes render correctly. Two visible placeholders remain: the
post-scaling audit results on p. 3 and artifact link/inventory on p. 10. The PDF bibliography still contains
the old authorless SPDX/sbomqs records and old SPDX URL, showing that the revised local `references.bib` was
not included in this Overleaf build. E6 therefore remains open for those two factual placeholders, G1, the
bibliography sync, and one final compile/audit.

**Latest PDF audit:** `SCORED_2026_SBOM (7).pdf` is exactly 11 pages and remains visually clean: no clipping,
overlap, broken float order, illegible table/figure, undefined reference, or anonymity leak was found across
all pages. The revised bibliography is still not fully reflected in the compiled reference list: reference
[1] retains the old SPDX URL and reference [2] still omits Interlynk, although the local `references.bib`
contains both corrections. Recompile the bibliography from scratch on Overleaf after synchronizing the file.
The audit-results placeholder and anonymous-artifact placeholder also remain visible by design.

**Title decision:** The approved title is `Schema-Valid but Semantically Divergent: How SBOM Specifications
Underdetermine Generator Behavior`. It foregrounds the paper's specification-interface thesis, uses
`generator` in the established SBOM sense, covers both inspected implementation decisions and emitted outputs,
and avoids the stronger causal implication of `specification-induced divergence`. Verify its two-line title
and running-header layout in the next PDF.

---

## F. Completed items

### [x] F1. Update methodology figure from five tools to four tools

The included `figures/methodology_pipeline.png` shows Syft, Trivy, cdxgen, and Microsoft SBOM Tool
(four tools total), and `sections/03-methodology.tex` includes that PNG. Stale references in unused patch or
TikZ source files do not affect the compiled figure, but they may be cleaned later for maintainability.

---

## G. Resolve last: author-supplied methodological details

### [-] G1. Complete the PyPI sampling description

**Criticism:** The top-20 selection lacks a date, popularity metric, complete list location, and identities of
the two excluded packages.

**Writing-only resolution:** Add one compact sentence with the selection date, ranking source/metric, the
location of the 18-package list, and the names plus exclusion reasons of the two omitted packages.

**Author input needed later:** Confirm the date, ranking metric/source, and two excluded package names.

**Current hold:** The authors have asked the advisors whether the dynamic sample should remain PyPI-only or
expand to npm/Maven. Do not revise the ecosystem, sampling-frame, package-list, or exclusion wording until
that scope decision is received; the final description must match the study that is actually reported.

**Files:** `sections/03-methodology.tex`, optionally supplementary material

**Done when:** Another researcher can reconstruct the sampling frame from the description.

### [x] G2. Report the thematic-coding agreement result

**Criticism:** The earlier thematic-coding subsection said a secondary coder labeled 25% of requirements but
reported no result. Table 1 does **not** answer this criticism because its kappa values concern
requirement-extraction decisions.

**Resolution after author follow-up:**

- If the thematic result exists, report the coding level (theme or subtheme), specification(s), sample size,
  agreements, disagreements, and resulting percentage. State whether reconciliation followed.
- Do not present one pooled value across incompatible coding tasks unless that pooling was actually used.
- If no result exists, remove the unsupported 25% reliability-test claim and unused formula. Describe the
  codebook-development and reconciliation process honestly, and state the lack of an independent thematic
  reliability estimate as a limitation.
- Keep extraction kappa and thematic-coding reliability clearly separated throughout the paper.

**Confirmed method:** The primary analyst coded an initial 20% sample, completed a collaborative sanity check
on ambiguous codes and category placement, then coded the full corpus with one subtheme per requirement and
formalized the resulting subtheme codebook. A secondary human annotator independently assigned exactly one
subtheme using that finalized codebook. The stratified random sample targeted 25% of each specification and
spanned its sections. Agreement was an exact subtheme match recorded before discussion; all disagreements
were then resolved by consensus. The codebook records subtheme labels and definitions, inclusion/exclusion
criteria, decision rules, and boundary examples. This human--human agreement check is explicitly separated
from Table 1's extraction-agreement results.

**Reported results:** CycloneDX had 392/431 exact matches (91.0%; 39 disagreements), SPDX 91/107 (85.0%; 16
disagreements), and CISA ME-SBOM 28/34 (82.4%; 6 disagreements). The paper reports the compact fractions and
percentages; disagreement counts are directly derivable and retained here for audit. No pooled result is
reported across specifications, and reconciliation is not counted as initial agreement. The threats section
states that this check evaluates subtheme assignment, not granular initial-code agreement or the subsequent
construction of high-level themes.

**Files:** `sections/03-methodology.tex`, `sections/07-discussion.tex`, potentially the methodology figure

**Done when:** The paper either reports a complete, auditable thematic reliability result or makes no claim
that such a quantified test was performed.

**Source resolved:** The methodology now reports the corrected coding sequence and subtheme-level comparison,
stratified sample sizes, exact-match counts, percentages, human--human comparison, and post-score consensus
procedure. All placeholders are removed. G2 remains in progress only until the corrected wording is verified
in the next compiled PDF.

**Prior PDF superseded:** `SCORED_2026_SBOM (3).pdf` rendered the correct samples and values but incorrectly
described the coding level as a high-level theme. The source now says exact subtheme assignment and must be
rechecked in the next PDF before G2 is closed.

**Final verification:** On p. 3 of `SCORED_2026_SBOM (5).pdf`, the codebook chronology, one-subtheme coding
unit, 25% section-stratified samples, exact-match definition, three fractions/percentages, pre-discussion
measurement, and consensus reconciliation all render correctly. Threats to Validity limits the independent
check to reproducible subtheme assignment rather than granular-code or high-level-taxonomy validation. G2 is
closed.

### [-] G3. Finalize the anonymous artifact inventory and link

**Current state:** `sections/07-availability.tex` intentionally contains `\textbf{TBA}` at the author's
request. The precise archive contents are not yet confirmed.

**Author input needed:** Supply the final anonymous link and confirm which materials are actually included:
extracted corpora, codebooks/recoded CSVs, prompts, table/figure scripts and inputs, generated native and
converted SBOMs, and schema-gap rules/results.

**Resolution:** Replace the TBA marker with the anonymous link and enumerate only confirmed files. Verify
that claims about auditability in the methodology and supplementary-material introduction match the archive.

**Files:** `sections/07-availability.tex`, `sections/03-methodology.tex`, `sections/appendix1.tex`

**Done when:** No TBA remains and a reviewer can locate every artifact the paper promises.

---

## H. Merged substantive and methodological concerns from advisor reviews 2 and 3

These items capture every additional obligation introduced by the two 2026-07-18 follow-up reviews. They
must be resolved before page compaction. Where a concern overlaps a verified item, the earlier item remains
closed only for its original scope; the added obligation below remains open.

### Cross-review mapping to already verified work

- The hypothetical Log4Shell/outcome concern maps to A1--A3, verified in prior PDFs; H5 adds a broader SCORED
  security-fit audit without reopening a claim that the present study measured false negatives.
- The low Stage-1 SPDX kappa concern maps to C3, and the non-comparable cross-specification percentages map
  to C4; both are verified, but H2 adds a new count-interpretation and CISA-sanity audit.
- The one-ecosystem/18-package concern maps to D2, and the SPDX 2.3/3.0.1 causal boundary maps to D7; H3 and
  H6 require a new full-paper claim audit and converter-discrepancy disclosure.
- Consumer behavior maps to A3, representative traceability to B2, and Wang differentiation to B3; H1,
  H9, and H14 add stronger evidence-chain, terminology, and novelty requirements.

### [x] H1. Add worked evidence chains and further bound the causal thesis

**Criticism:** Table 6 and the current clause references are too high-level to establish that specification
latitude caused a tool divergence; vendor priorities or defects remain competing explanations.

**Writing-only resolution:**

- Add two or three compact, fully worked examples containing: the exact clause/schema rule and normative
  force; why it permits or fails to prevent multiple behaviors; an inspected source file/function or tool
  option; a short generated-SBOM excerpt or precise output observation; and the bounded downstream risk.
- Include representative schema/prose mismatches in these examples so the mismatch counts are not presented
  without concrete meaning.
- Use causal language only where the chain demonstrates it. Elsewhere say the behavior is *consistent with*,
  *occupies*, or *is not prevented by* specification latitude.
- State explicitly that the study does not rule out bugs, product priorities, or other implementation causes.

**Files:** `main.tex`, `sections/01-introduction.tex`, `sections/04-specification-analysis.tex`,
`sections/05-tool-implementation.tex`, `sections/06-root-causes.tex`, `sections/08-conclusion.tex`

**Done when:** At least two end-to-end chains are visible in the main text and no retained sentence treats
specification latitude as the sole or proven cause of all observed divergence.

**Implemented:** The title and abstract now frame the contribution as mapping specification boundaries to
generator decisions. Section 5 adds two clause-to-code-to-artifact evidence chains: Trivy's opt-in development
dependency coverage and absent completeness declaration, and cdxgen's output-level failure of CycloneDX's
mandatory empty-entry prose rule despite schema validity. The prose names normative force, exact output
observations, and bounded artifact risk, while Table 4 centralizes the otherwise distracting commits and
paths/functions. The introduction, synthesis,
recommendations, discussion, and conclusion explicitly retain defects, product priorities, ecosystem
evidence, and configuration as competing or interacting explanations.

**Verified:** In `SCORED_2026_SBOM (3).pdf`, the bounded title/abstract and novelty framing render on pp. 1--2,
the two complete evidence chains render on pp. 9--10, and the competing-cause limitations remain visible on
pp. 10--12. No clipping, overlap, or causal-language regression was found.

### [x] H2. Reconcile the 2,286-row corpus with its LLM-assisted, protocol-dependent status

**Criticism:** A precise headline number and theme percentages may appear stronger than a nondeterministic,
LLM-scaled extraction with no held-out retrieval validation supports; the 133 CISA rows may look inflated to
readers familiar with the small number of minimum data fields.

**Writing-only resolution:**

- Define 2,286 as the exact size of the *realized extracted-row dataset*, not an estimate of the true number
  of normative requirements in the source documents.
- State which uses are descriptive (within-corpus distributions and audit navigation) and which arguments do
  not depend on row-count magnitude.
- Add a CISA sanity sentence explaining that the 133 rows include bounded directives about creation,
  exchange, lifecycle, framing, and data-field guidance, rather than 133 distinct minimum data fields.
- Audit the abstract, results, and conclusion so percentages provide descriptive context rather than proof of
  specification priorities or cross-specification superiority.

**Files:** `main.tex`, `sections/03-methodology.tex`, `sections/04-specification-analysis.tex`,
`sections/07-discussion.tex`, `sections/08-conclusion.tex`

**Done when:** A reviewer cannot interpret 2,286 or 133 as exhaustive true-requirement counts, and the core
claim remains supported if corpus percentages are treated as descriptive only.

**Implemented:** The abstract, introduction, methodology figure caption, results, threats, and conclusion now
define 2,286 as the exact size of the realized extracted-row dataset rather than an estimate of the true
requirement count. Counts and percentages are restricted to within-corpus description and audit navigation;
the paper states that its clause-level conditionality, schema/prose, and source-trace arguments do not depend
on row-total magnitude. The methodology and CISA results explain that the 133 rows include bounded creation,
exchange, lifecycle, framing, and data-field directives rather than 133 distinct minimum fields.

**Verified:** In `SCORED_2026_SBOM (4).pdf`, the abstract labels the 2,286 rows as a realized,
non-exhaustive dataset on p. 1; the extraction limits and exact row composition render on pp. 3--4; the CISA
sanity explanation renders on pp. 4 and 6; and the within-corpus, non-prevalence, and row-magnitude boundaries
remain explicit on p. 12. No table, figure, or text regression was found.

### [-] H3. Report the held-out post-scaling agreement check

**Criticism:** The reviews ask how many LLM-extracted rows were manually checked after scaling and for false
positive/false negative rates against human material.

**Updated study decision:** A held-out page-based audit will be performed outside the original pilot. For
each specification, pages corresponding to 10% of its total page count are selected randomly from pages not
used in the pilot, then divided into primary units. The primary analyst supplies the independent binary
annotation without first viewing NotebookLM's output; after scoring, a second analyst reviews every
disagreement with the primary analyst.

**Author/factual input needed:** Provide the audited primary-unit count and positive-unit Jaccard overlap for
SPDX. CycloneDX is confirmed at $J=0.923$ across 615 units; CISA ME-SBOM is confirmed at $J=0.919$ across 52
units. The paper need not publish the seed, page identifiers, confusion matrix, precision, recall, kappa, or
raw agreement. Artifact publication and the codebook/corpus inventory remain linked to C2 and G3.

**Files:** `sections/03-methodology.tex`, `sections/07-discussion.tex`, `sections/07-availability.tex`

**Done when:** The paper reports the audited-unit count and Jaccard positive-unit overlap for all three
specifications, explains that the score is set overlap rather than reliability, accuracy, or exhaustive corpus
coverage, and the artifact claim matches what reviewers receive.

**Implemented so far:** The methodology reports the confirmed CycloneDX and CISA unit counts and Jaccard
values, explains why shared negatives are excluded, and documents a post-score second-analyst disagreement
review without converting it into a model-accuracy claim. Threats to Validity gives the same interpretation
boundary. Final closure is tracked together with I4 and awaits the SPDX count and Jaccard value.

### [x] H4. Complete the one-ecosystem and small-sample claim audit

**Criticism:** Even with “not a benchmark” language, broad statements about real-world generators may exceed
18 PyPI packages, one ecosystem, and a small set of selected gap rules.

**Writing-only resolution:**

- Audit the title, abstract, contributions, results, root-cause table, discussion, and conclusion for scope.
- Attribute cross-ecosystem inventory, graph, and vulnerability variation to prior work, not this experiment.
- Describe dynamic results as concrete illustrative patterns in the evaluated Python repositories and tools;
  do not estimate frequency beyond that set.
- Preserve the explicit exclusions of inventory overlap, graph depth, vulnerability outcomes, and consumer
  behavior.

**Files:** `main.tex`, `sections/01-introduction.tex`, `sections/02-background.tex`,
`sections/05-tool-implementation.tex`, `sections/06-root-causes.tex`, `sections/07-discussion.tex`,
`sections/08-conclusion.tex`

**Done when:** Every empirical generalization names or clearly inherits the evaluated tool/ecosystem scope.

**Implemented:** The abstract and contribution statement now distinguish four frozen source snapshots,
CycloneDX checks covering one output per tool for each of 18 selected PyPI package repositories, and three
evaluated SPDX artifacts. The methodology identifies the popularity-based single-ecosystem set as
non-statistical. Results, the interface-boundary table, discussion, and conclusion replace “real-world” and
practice-wide language with exact study scope, preserve all excluded metrics, and state that the observations
are not frequency estimates. Cross-ecosystem inventory and vulnerability variation remains attributed to
prior work.

**Verified:** In `SCORED_2026_SBOM (4).pdf`, the abstract and contributions give the exact four-snapshot,
18-repository-per-CycloneDX-tool, and three-SPDX-artifact scope on pp. 1--2. The non-statistical PyPI boundary
renders on p. 5, individual results retain their evaluated-set scope on pp. 8--10, and the no-frequency and
excluded-measures limitations remain explicit on pp. 11--12.

### [x] H5. Define three distinct notions of completeness and evidence-relative ground truth

**Criticism:** “Complete dependency graph,” “dependency closure,” and “security-grade SBOM” are undefined
without an evidence source such as manifests, lockfiles, resolved environments, images, builds, or runtime.

**Writing-only resolution:** Define and use:

1. **Specification completeness:** required constructs for a declared format/profile are present.
2. **Generator-evidence completeness:** the SBOM faithfully covers the evidence sources the generator claims
   to inspect.
3. **Security-use-case sufficiency:** the artifact contains the evidence required by a stated defensive task.

State that the study does not establish repository-wide or runtime ground truth and that graph depth is not a
stand-alone completeness measure.

**Files:** `sections/02-background.tex`, `sections/03-methodology.tex`,
`sections/04-specification-analysis.tex`, `sections/06-root-causes.tex`, `sections/07-discussion.tex`

**Done when:** Every “complete,” “closure,” and “security-grade” claim either names one of these levels or is
rephrased so its evidence boundary is explicit.

**Implemented:** The background now defines specification completeness, generator-evidence completeness,
and security-use-case sufficiency, and states the evidence boundary for each. Methodology, results,
recommendations, limitations, and conclusion distinguish structural/profile checks, declared producer
evidence, and external ground truth. Ambiguous claims about dependency closure and graph completeness were
rephrased as graph coverage or coverage status, and graph depth is explicitly only a diagnostic.

**Verified:** In `SCORED_2026_SBOM (4).pdf`, all three definitions and their evidence boundaries render
together on p. 3. The codebook-label qualification appears on p. 5, coverage-status terminology is used in
the specification and output results on pp. 7--11, and the recommendations, ground-truth limitation, and
conclusion keep graph depth separate from completeness on pp. 11--12.

### [x] H6. Sharpen SCORED security relevance without inventing an outcome experiment

**Criticism:** The paper can read as standards/quality analysis rather than an ecosystem-defense contribution,
while suggestions to show false-negative CVEs or differing vulnerability counts exceed the study performed.

**Writing-only resolution:**

- Ground the security contribution in defensive interface assurance: whether provenance, dependency,
  filtering, and completeness claims are available for vulnerability response, compliance, and incident
  triage.
- Keep false-negative detection and CVE-count differences attributed to prior studies or labeled constructed
  risks; do not imply this study measured them.
- Explain how machine-readable absence semantics and profile-level checks reduce ambiguity for defensive
  workflows, including provenance attribution during incident response.
- Do not introduce an adversarial-producer claim without evidence; negligent or malicious omission may be
  future work, not an observed result.

**Files:** `main.tex`, `sections/01-introduction.tex`, `sections/02-background.tex`,
`sections/06-root-causes.tex`, `sections/08-conclusion.tex`

**Done when:** The SCORED defense contribution is concrete while all unmeasured security outcomes remain
clearly attributed, hypothetical, or future work.

**Implemented:** The abstract, introduction, background, recommendations, discussion, and conclusion now
frame the contribution as defensive interface assurance for vulnerability response, compliance, and incident
triage. The constructed Log4Shell scenario is labeled as unobserved, empirical vulnerability-result claims
remain attributed to prior work, and the paper expressly excludes consumer implementations, false-negative
rates, and adversarial producers. Absence semantics, profiles, and evidence declarations are tied to the
assessability of defensive workflows without claiming measured security outcomes.

**Verified:** In `SCORED_2026_SBOM (4).pdf`, defensive interface assurance is explicit in the abstract and
introduction on pp. 1--2. The Log4Shell example is labeled constructed and unobserved, and the operational
risk model expressly excludes adversarial producers and measured vulnerability outcomes on p. 2. The
recommendations and conclusion connect the contribution to vulnerability response, compliance, and incident
triage on pp. 11--12 while the threats section preserves the false-negative and consumer-outcome exclusions.

### [x] H7. Separate every SPDX evidence layer and disclose converter discrepancies

**Criticism:** Specification claims about SPDX 3.0.1, native Trivy/Syft 2.3 behavior, converted artifacts,
and Microsoft SBOM Tool's native 3.0.1 output can still blur; reviewers also ask how many conversion
discrepancies were found and excluded.

**Writing-only resolution:** Use explicit labels for all four evidence layers in methodology, results, tables,
and conclusion. Preserve D7's non-causal conversion boundary and report the actual discrepancy count for the
back-checked observations, if recorded.

**Author/factual input needed:** Confirm the number and nature of native-versus-converted discrepancies that
were excluded. If no comprehensive discrepancy log exists, state that the back-check was limited to the
reported field-presence observations and do not imply an exhaustive conversion validation.

**Partner revision verified:** `SCORED_2026_SBOM (5).pdf` states that the scoped comparison covered
the ten CISA-derived fields in native SPDX 2.3 and converted 3.0.1 artifacts, found no presence/absence
discrepancies for those fields, and was not a full-document conversion audit or evidence of lossless mapping.
The methodology and results distinguish Trivy/Syft native 2.3 behavior, converted 3.0.1 comparison artifacts,
Microsoft's native 3.0.1 artifact, and the 3.0.1 specification baseline.

**Final terminology check:** The local methodology now matches the partner's compiled revision by using
`Conversion Fidelity Check` instead of `Back-Checking Protocol`. Appendix Table 6 is interpreted through the
immediately preceding methodology and results text, which identifies Microsoft as native 3.0.1 and Syft/Trivy
as native 2.3 artifacts mapped to the 3.0.1 comparison baseline. H7 is closed.

**Files:** `sections/03-methodology.tex`, `sections/04-specification-analysis.tex`,
`sections/05-tool-implementation.tex`, `sections/07-discussion.tex`, `sections/08-conclusion.tex`

**Done when:** Every SPDX result identifies its evidence version/layer and the converter audit is quantified
or explicitly bounded by the available record.

### [x] H8. Recast the central critique around absence semantics, not optionality alone

**Criticism:** Optional fields are not inherently specification defects; legitimate use cases, disclosure
constraints, ecosystems, and maturity levels require optionality.

**Writing-only resolution:**

- Replace “optional is bad” implications with the stronger interface claim that security-relevant absence
  often lacks a machine-readable reason.
- Use the explicit absence states: not applicable, unknown, unsupported, filtered, intentionally omitted, and
  not required by the declared profile.
- Acknowledge legitimate optionality and argue for use-case profiles plus declared absence semantics.

**Files:** `main.tex`, `sections/01-introduction.tex`, `sections/02-background.tex`,
`sections/04-specification-analysis.tex`, `sections/05-tool-implementation.tex`,
`sections/06-root-causes.tex`, `sections/08-conclusion.tex`

**Done when:** The thesis is fair to multi-use specifications and consistently targets undeclared absence
meaning and missing profile-level contracts.

**Implemented:** The abstract and active sections now acknowledge that optionality legitimately supports
different use cases, ecosystems, disclosure constraints, and maturity levels. The critique is consistently
focused on artifacts that declare neither a use-case profile nor whether missing data is not applicable,
unknown, unsupported, filtered, intentionally omitted, or not required by the declared profile. The proposed
remedy is machine-readable absence states plus task-specific profiles, not universal mandatory population.

**Verified:** In `SCORED_2026_SBOM (4).pdf`, the abstract treats optionality as legitimate on p. 1 and the
operational model lists the explicit absence states on p. 2. The SPDX and CycloneDX takeaways, synthesis
table, discussion, and conclusion consistently target missing profile/absence declarations rather than
optionality itself on pp. 7--12. The proposed remedy remains profiles plus machine-readable absence states.

### [x] H9. Turn recommendations into a concrete, explicitly unevaluated conformance profile

**Criticism:** The root-cause table remains diagnostic; no tool or implementable profile is contributed.

**Writing-only resolution:** Propose a compact three-level check suite, clearly labeled a design proposal
rather than an evaluated artifact:

- Level 1: provenance, component identity/version, timestamp, and tool identity.
- Level 2: evidence-source and filtering declarations, dependency coverage, and completeness status.
- Level 3: vulnerability/VEX context, build/formulation evidence, and task-specific sufficiency claims.

For each level, name machine-checkable fields where the specifications provide them and flag checks requiring
external evidence. Do not claim a prototype or validation that was not performed.

**Files:** `sections/06-root-causes.tex`, `sections/08-conclusion.tex`

**Done when:** Reviewers can see an implementable check hierarchy and its evidence limitations without
mistaking it for a tested contribution.

**Implemented:** Section 6 now presents a cumulative three-level defensive conformance-check suite and
labels it explicitly as a design proposal rather than an implemented or evaluated tool. Level 1 names
CycloneDX and SPDX identity/provenance anchors; Level 2 names dependency, scope, composition, relationship,
and profile anchors while identifying evidence-source, filtering, and absence declarations that need profile
rules or extensions; Level 3 names CycloneDX VEX/formulation and SPDX Security/Build anchors and requires
task-specific assessment. The evidence boundary assigns structural checks to schemas, population and absence
semantics to profile/prose checks, and claim verification to external evidence. The conclusion summarizes the
same hierarchy and states that lower-level passage does not establish higher-level sufficiency or ground
truth.

**Verified:** In `SCORED_2026_SBOM.pdf` compiled at 15:30 on 2026-07-18, the three cumulative levels, named
CycloneDX/SPDX anchors, schema/profile/external-evidence boundaries, and explicit ``not implemented or
evaluated'' qualification render legibly on p. 11. The condensed conclusion restates the unevaluated hierarchy
and lower-level limitation on p. 12 without claiming a prototype or validation.

### [x] H10. Use “consumer-facing ambiguity” consistently

**Criticism:** The paper studies generators and artifacts, not representative consumer implementations, yet
some wording still implies consumers are forced to guess or behave in a particular way.

**Writing-only resolution:** Run a full-text audit and use “consumer-facing ambiguity,” “the artifact does
not determine,” or “a consumer operating only on this artifact cannot infer” unless a consumer claim is
directly cited from prior work. Keep consumer implementation inspection as future work.

**Files:** Entire active paper

**Done when:** No uncited sentence predicts actual consumer behavior from the present study.

**Implemented:** A full-text audit replaced behavioral predictions with consumer-facing ambiguity,
artifact-level implications, or statements about what an artifact does not determine. The constructed
scanner example is explicitly hypothetical, observed consumer implementation and outcome behavior are
excluded, and prior-work findings retain their citations. Consumer implementation inspection remains future
work.

**Verified:** In `SCORED_2026_SBOM (4).pdf`, the scanner example remains explicitly constructed and its
implication is limited to information available in the artifact on p. 2. Results use consumer-facing or
artifact-level language on pp. 7--11, and the discussion/threats sections state that particular consumer
interpretation and vulnerability outcomes were not observed on pp. 11--12. No uncited present-study claim
predicts consumer implementation behavior.

### [x] H11. Make static source inspection independently auditable

**Criticism:** Version numbers and a reading protocol are insufficient for claims about filtering,
relationship translation, and field population if inspected files/functions are unnamed.

**Writing-only resolution:** Add a compact traceability table or worked-example fields naming repository
snapshot/commit, source path, function or option, inspected concept, and corresponding output observation.
Use only source locations that can be verified in the retained local snapshots/artifact.

**Files:** `sections/03-methodology.tex`, `sections/05-tool-implementation.tex`,
`sections/appendix1.tex`, artifact inventory under G3

**Done when:** Each central static-inspection claim has a reproducible source anchor in the paper or promised
artifact.

**Implemented:** Table 4 records all four frozen commits, the format(s) inspected for each tool, and the
repository-relative source paths and functions/options supporting the central Trivy, cdxgen, Syft, and
Microsoft claims, together with the corresponding bounded output observations. The methodology and evidence
chains refer to that table instead of repeating hashes and long paths in the narrative. The anchors were checked
against commits `0c40a8d4b9b9`, `70e7a729b10d`, `e9e34948534a`, and `e47d1d4b1f37`. Final archive inventory
remains reserved under G3.

**Verified before the consolidation:** In `SCORED_2026_SBOM (3).pdf`, the frozen commits and auditable
source/output anchors were legible. The next PDF must verify the revised Table 4 after its new inspected-format
labels and centralized anchors; G3 remains separately open for the final archive inventory.

**Final verification:** In `SCORED_2026_SBOM (5).pdf`, revised Table 4 renders on p. 6 with all four versions,
formats, commits, repository-relative anchors, and bounded observations intact. The table is dense but legible
and no hash/path is redundantly repeated in the surrounding evidence-chain prose. H11 remains closed.

### [x] H12. Calibrate the Microsoft SBOM Tool contrast

**Criticism:** “Makes producer intent explicit” may overstate Microsoft SBOM Tool's strength relative to its
incomplete CISA-derived field population.

**Writing-only resolution:** Identify exactly which document creation metadata, package-level `suppliedBy`,
and typed relationships are stronger in the inspected path, then state which evaluated CISA-derived fields
or Lite Profile obligations remain absent. Present it as a scoped contrast, not a generally superior tool.

**Files:** `sections/04-specification-analysis.tex`, `sections/05-tool-implementation.tex`,
`sections/08-conclusion.tex`

**Done when:** Every favorable Microsoft comparison names the field/relationship and an explicit limitation.

**Implemented:** The paper now limits the contrast to the inspected construction of
`CreationInfo.createdBy`, `createdUsing`, package `suppliedBy`, and typed relationships. It states that absent
supplier input becomes `NOASSERTION`, the evaluated document did not declare Lite Profile conformance, the
4-of-10 universal-field result is aggregate across three SPDX generators, and no overall completeness or
superiority claim follows.

**Verified:** In `SCORED_2026_SBOM (3).pdf`, the scoped Microsoft source anchor and Lite limitation render on
p. 8; the named creation fields, typed relationships, `NOASSERTION`, absent Lite declaration, and no-superiority
boundary render together on p. 10 and are summarized consistently on p. 12.

### [x] H13. Stop treating JSON Schema as a semantic-completeness mechanism

**Criticism:** Schemas are structurally limited by design; the ecosystem gap is the absence of profile-level
conformance and evidence checks beyond schema validation.

**Writing-only resolution:** Audit schema criticism so it distinguishes structural schema obligations,
prose-level conformance, and use-case sufficiency. Do not imply that JSON Schema should validate external
dependency discovery or runtime truth.

**Files:** `main.tex`, `sections/02-background.tex`, `sections/04-specification-analysis.tex`,
`sections/05-tool-implementation.tex`, `sections/06-root-causes.tex`, `sections/08-conclusion.tex`

**Done when:** All recommendations assign structural checks to schemas and semantic/evidence checks to
profiles, producer declarations, or external validation.

**Implemented:** The abstract, background, methodology, results, recommendations, discussion, and conclusion
now limit schema validation to machine-expressible document structure and applicable cross-field constraints.
Prose/profile conformance, declared evidence and filtering coverage, absence meaning, defensive-task
sufficiency, and repository/build/runtime truth are assigned to separate checks, producer declarations, or
external validation. The paper no longer asks JSON Schema to validate dependency discovery or runtime truth.

**Verified:** In `SCORED_2026_SBOM (4).pdf`, the quality-assurance gap explicitly says this is not a JSON
Schema defect on p. 3, and the methodology confines schema comparison to machine-checkable structure on p. 5.
The results keep schema/prose mismatches structural on pp. 7--10, while recommendations and conclusion assign
profiles, producer declarations, and external evidence to semantic and defensive-task assessment on
pp. 11--12.

### [x] H14. Sharpen novelty relative to Yu, O'Donoghue, JBomAudit, and Wang

**Criticism:** “Tools disagree” is established; the paper must show what specification-centered analysis
adds beyond prior output-level measurements.

**Writing-only resolution:** Add one crisp early delta sentence: prior studies measure dependency,
vulnerability, compliance, or accuracy divergence, whereas this paper maps selected divergences to
normative conditionality, schema/prose boundaries, and implementation decision points. State the unique
output of this paper without firstness or superiority language.

**Files:** `sections/01-introduction.tex`, `sections/02-background.tex`

**Done when:** The novelty delta is explicit before the contribution list and remains consistent with B3.

**Implemented:** Immediately before the contribution list, the introduction distinguishes the paper's
clause-to-code-to-artifact mapping from prior estimates of tool disagreement. The Wang comparison now names
the same unique output---selected normative conditionality and schema/prose boundaries connected to concrete
decision points and bounded observations---without firstness, superiority, or comparable-scale claims.

**Verified:** In `SCORED_2026_SBOM (3).pdf`, the clause-to-code-to-artifact novelty delta appears immediately
before the contribution list on p. 2, and the Wang comparison states the same bounded delta without a scale,
firstness, or superiority claim.

### [x] H15. Reduce repetition and overlapping presentation without dropping content

**Criticism:** “Schema validity is not semantic sufficiency” is repeated across the abstract, motivation,
quality gap, takeaway boxes, synthesis, and conclusion; Tables 4--6 overlap.

**Writing-only resolution:** During final in-document compaction, retain one motivation statement, one
evidence-backed synthesis, and one conclusion statement; remove or merge redundant takeaway prose and
consolidate table content where possible. Keep every substantive method/result and retain prompts/tables in
this same document as required by the author.

**Files:** Entire active paper; coordinated with E5

**Done when:** Repetition is materially reduced, no evidence is lost, and the complete document fits the
11-page limit.

**Progress:** A first low-risk prose pass condensed the thematic-codebook description, manual source-reading
protocol, and repeated discussion framing in `sections/03-methodology.tex` and
`sections/07-discussion.tex`. The two files were reduced by 275 source words while preserving the extraction
limits, source-inspection protocol, null result, and evidence boundaries. H15 remains open until the full
in-document compaction and 11-page verification are complete.

**Second progress pass:** A coordinated pass across the abstract, introduction, background, methodology,
implementation synthesis, interface-boundary synthesis, and conclusion removed another 478 source words.
It preserves every corpus denominator, dynamic sample boundary, frozen-snapshot qualification, competing
cause, null result, and proposed-conformance limitation. The cumulative reduction across both passes is 753
source words. H15 remains open because page-limit closure requires a fresh compiled PDF and likely further
table/appendix compaction.

**Third progress pass:** The overlapping specification-variation table was removed because its concepts and
remedies are already represented in the clause trace and interface-boundary table. Prose compaction preserved
corpus denominators, selected schema-gap outcomes, source anchors, competing explanations, and the three-level
proposal. The later author-directed restoration and completion of the visual takeaway convention adds nine
concise boxes while retaining explicit RQ1--RQ2 and RQ3 syntheses. After the G2 expansion and boxes, the current net
reduction across the active paper is 2,495 source words. Final closure depends on the next PDF meeting the page
limit without a layout regression.

**Latest layout result:** `SCORED_2026_SBOM (3).pdf` is 12 pages and is visually clean throughout. The only
substantial unused space is on p. 12, which contains just the final appendix table. Further H15 work should
therefore prioritize appendix float placement and local layout economy, not repeat the completed paper-wide
prose compaction or delete reviewer-facing defenses.

**Final verification:** `SCORED_2026_SBOM (5).pdf` fits the complete paper, references, prompts, and schema-gap
tables into 11 pages. The abstract, motivation, results, takeaways, synthesis, threats, and conclusion retain
distinct roles; the three recommendation levels and five compact validity paragraphs scan cleanly; and no
reviewer-facing evidence or limitation was dropped. H15 is closed.

### [x] H16. Improve methodology-figure legibility

**Criticism:** Figure 1 is dense even at full-page width and may be hard to read in the proceedings PDF.

**Writing-only/presentation resolution:** Simplify labels, increase effective text size, and remove details
already stated in prose while preserving the four-tool configuration and analysis flow. Verify the rendered
figure at 100% zoom and in print-like grayscale.

**Files:** `figures/methodology_pipeline.png` and its source, `sections/03-methodology.tex`

**Done when:** Every label is comfortably legible in the compiled two-column PDF without enlarging the page
footprint.

**Current figure audit / exact author edits:** Preserve the layout and four-tool configuration, but replace
`Reliability: Kappa-validated` with `Pilot agreement: Cohen's kappa`; replace `Total Requirements` with
`Realized extracted rows`; and remove the unquantified `Miles & Huberman inter-coder check` unless G2 supplies
its result. Replace `annotator-derived JSON/XML schemas` and `Annotator Schema` with `official JSON/XML
schemas` and `Official Schema`. Replace the dynamic-analysis claim about controlled tests and isolating
generator choices with `18 selected PyPI repositories; bounded output checks`. Finally, use
`Interface-boundary synthesis`, `Specification clause/boundary`, `Source/output evidence`, and
`Artifact-level risk` instead of causal or consumer-behavior labels. These shorter labels should permit a
larger font without changing the figure footprint.

**Follow-up PDF check:** `SCORED_2026_SBOM.pdf` compiled at 15:30 on 2026-07-18 contains all requested label
corrections and the four-tool configuration, but H16 remains open. In Figure 1 on p. 4, `Pilot agreement:
Cohen's kappa` visibly crosses the extraction-column boundaries, `Realized extracted rows: 2,286` overruns its
box, and the grounded-theory bullet approaches/crosses the taxonomy divider. Wrap these three labels within
their boxes and recompile before closing H16; the remaining panels are accurate and legible.

**Implemented after follow-up:** The regenerated 3253-by-872 PNG wraps the pilot-agreement text into four
lines, shortens the corpus heading to `Realized rows: 2,286`, and wraps the grounded-theory bullet into three
lines. Source and full-resolution image inspection show that all three now remain within their columns, while
the corrected four-tool, official-schema, bounded-output, and interface-boundary labels are preserved.

**Verified:** In `SCORED_2026_SBOM (1).pdf` compiled on 2026-07-18, Figure 1 renders on p. 4 with all labels
inside their panels, the four-tool configuration intact, and no clipping or overlap. Inspection at a realistic
two-column page size and in grayscale confirms that the corrected labels and analysis flow remain legible.

### [x] H17. Report tool versions as frozen study snapshots, not current releases

**Criticism:** Reviewers may check whether Trivy, Syft, cdxgen, and Microsoft SBOM Tool are the latest at
submission time.

**Writing-only resolution:** Verify version metadata and state that these are fixed inspected snapshots with
an inspection date, selected for reproducible analysis rather than claimed as the latest releases. If a
listed version is inaccurate relative to the actual snapshot, correct it; do not silently substitute a newer
version without rerunning its inspection.

**Files:** `sections/03-methodology.tex`, `sections/04-specification-analysis.tex`,
`sections/05-tool-implementation.tex`, artifact inventory under G3

**Done when:** The paper makes no “latest tool version” claim and each version maps to the inspected source
snapshot.

**Implemented:** The methodology identifies the four versions as fixed inspected snapshots that define the
evidence boundary, records that their source anchors were re-verified in July 2026, and states that they are
not current/latest-release claims. Table 4 centralizes the corresponding commits and inspected formats. The
methodology also explains that substituting a later release would require rerunning the source inspection and
output checks. Existing results and limitations scope claims to these frozen snapshots.

**Verified before the consolidation:** `SCORED_2026_SBOM.pdf` compiled at 15:30 on 2026-07-18 showed the
versions, commits, verification date, no-current/latest-release boundary, and rerun requirement. The next PDF
must confirm the same information after commit identifiers were moved from the methodology prose into Table 4.

**Final verification:** `SCORED_2026_SBOM (5).pdf` presents the four fixed versions and July 2026 reinspection
boundary in the methodology on p. 4, with exact commits and inspected formats centralized in Table 4 on p. 6.
No current/latest-release claim remains. H17 remains closed.

### [x] H18. Add a consistent key-takeaway box to every subsection in Sections 4 and 5

**Criticism:** Only some subsections in Sections 4 and 5 ended with a boxed `Key Takeaway`, making the
presentation appear inconsistent or incomplete.

**Writing-only resolution:** Preserve the original visual convention and add a concise, evidence-calibrated
box to every other subsection in Sections 4 and 5. Retain concise RQ1--RQ2 and RQ3 synthesis paragraphs
because they answer the research questions rather than replace subsection takeaways.

**Files:** `sections/04-specification-analysis.tex`, `sections/05-tool-implementation.tex`

**Implemented:** The three original Section 4 boxes and original Section 5 synthesis box were restored. New
boxes now conclude Section 4's Thematic Structure and Common Structural Ambiguities subsections, plus Section
5's CISA Compliance, Security-Relevant Schema Gaps, and Static Inspection subsections. Sections 4 and 5 therefore
contain five and four consistently styled takeaway boxes, respectively. New text preserves the bounded/null
result language and avoids causal, prevalence, or overall-compliance overclaims.

**Done when:** The next compiled PDF shows all nine boxes with consistent styling, no awkward split or
clipping, and acceptable page impact.

**Verified:** In `SCORED_2026_SBOM (3).pdf`, all five Section 4 boxes and all four Section 5 boxes render with
consistent styling across pp. 4--9. None is clipped, overlapped, or awkwardly split, and the separate
explicit RQ-synthesis convention remains intact. H18 is closed.

---

## I. Submission-readiness critique and Fable rewrite audit (review round 4)

The fourth review is implemented in approval-sized batches. Proposed replacement prose from Fable is treated
as an editing aid rather than accepted verbatim: every numerical, causal, and format-level statement must
remain traceable to the paper's actual evidence.

### [x] I1. Repair dangling methodology references in Section 5

**Criticism:** Sections 5.1--5.3 refer to investigation dimensions (1), (2), and (3), but Section 3 does not
define numbered dimensions.

**Approved-scope resolution:** Replace the dangling labels with direct descriptions of the corresponding
analysis: CISA-derived field presence, selected schema/prose criteria, and static source inspection. Do not
add a redundant numbered framework to Section 3.

**Files:** `sections/05-tool-implementation.tex`

**Done when:** No undefined investigation/methodology dimension remains and each subsection states plainly
what evidence it contributes to RQ3.

**Implemented:** Sections 5.1, 5.2, and 5.3 now introduce CISA-derived field presence, selected prose/schema
checks, and static-inspection decision areas directly. Source search finds no undefined dimension reference.

**Verified:** `SCORED_2026_SBOM (6).pdf` contains the three direct subsection descriptions on pp. 6 and 8
and no investigation/methodology-dimension reference.

### [x] I2. Remove the secondary generator/consumer recoding claim

**Criticism:** The abstract, introduction, and appendix advertised a CycloneDX-only secondary recoding as
though it were a general paper contribution.

**Resolution:** The secondary recoding is not required for the reported specification, schema, conditionality,
source, or output findings. We therefore removed it from the abstract, methodology, contribution list,
conclusion, appendix inventory, and methodology figure rather than presenting an asymmetric auxiliary analysis.

**Files:** `sections/03-methodology.tex`, checked against `main.tex`, `sections/01-introduction.tex`, and
`sections/appendix1.tex`

**Done when:** No paper contribution or method claim depends on the CycloneDX-only secondary tags.

**Implemented:** Paper-facing references to the recoding were removed. The main thematic codebook and
human-to-human subtheme agreement remain the reported qualitative method.

**Verification pending:** Recompile and confirm that the revised methodology figure and paper contain no
secondary-recoding claim.

### [x] I3. Reduce repeated hedging while preserving evidence boundaries

**Criticism:** The abstract, contributions, results, threats, and conclusion repeatedly restate the same
scope caveats, causing the paper to sound as though it claims little.

**Proposed resolution:** Let the abstract and conclusion lead with three concrete bounded findings: the
schema-unenforced CycloneDX empty-entry rule and observed violations; absence of document-level supplier and
compositions in the evaluated CycloneDX outputs; and the lack of a uniform cross-field absence vocabulary.
Keep one concise scope sentence in each summary section and centralize detailed limitations in Threats to
Validity. Remove repetitions, not methodological qualifications.

**Guardrails:** Do not copy claims that schema validity requires "almost none" of the fields; do not call all
CISA fields mandatory; do not say either format has no absence mechanism whatsoever; and do not claim that
specification latitude alone caused every output difference.

**Files:** `main.tex`, `sections/01-introduction.tex`, `sections/04-specification-analysis.tex`,
`sections/05-tool-implementation.tex`, `sections/07-discussion.tex`, `sections/08-conclusion.tex`

**Done when:** Each major caveat appears at its most useful location, the abstract/conclusion foreground
evidence, and all claims remain bounded to the mapped clauses, selected criteria, and evaluated artifacts.

**Implemented:** The abstract and conclusion now lead with the empty-entry, metadata-supplier/compositions,
and cross-field absence-vocabulary findings, followed by one empirical-scope boundary. The introduction
states three positive contributions; the Section 4.1 takeaway reports a result; and the related-work
comparison presents the mechanism-tracing contribution positively. Unsupported stronger Fable formulations
were not adopted.

**Verified:** The abstract on p. 1 and conclusion on p. 10 lead with the empty-entry,
supplier/compositions, and absence-vocabulary findings, retain one scope sentence, and render cleanly within
the 11-page PDF.

### [-] I4. Perform and report a held-out post-NotebookLM primary-unit audit

**Criticism:** Human--NotebookLM agreement was measured only on the reconciled pilot, while the scaled
remainder had no independent manual audit.

**Required design before any prose claim:** Keep the original pilot unchanged. For each specification,
randomly select pages corresponding to 10% of its total page count from pages outside the pilot. Divide those
pages into *primary units*: the smallest objective source segments evaluated for extraction (for example, a
sentence, list item, table row or cell, figure caption, or linked class/property definition). Have one analyst
inspect the units without first seeing the NotebookLM output. A unit may yield zero, one, or multiple
separable normative requirements.

**Matching and reporting:** The primary analyst supplies an independent binary annotation before viewing
NotebookLM's output. Compare the positive-unit sets with Jaccard, which ignores shared negatives, and report
the audited-unit count and $J$ for each specification. After recording $J$, a second analyst reviews every
disagreement with the primary analyst to characterize annotation-boundary and extraction errors. The paper
does not need to publish kappa, raw agreement, the random seed, page identifiers, confusion matrix, precision,
or recall.

**Important distinction:** Jaccard measures overlap between the human and NotebookLM positive-unit sets. It
is symmetric and is not a reliability, accuracy, precision, recall, or exhaustive-coverage estimate. The
second-analyst review interprets discrepancies but does not alter the reported pre-reconciliation overlap.

**Author input required:** CycloneDX is complete at 615 units and $J=0.923$; CISA ME-SBOM is complete at 52
units and $J=0.919$. Supply the audited-unit count and Jaccard overlap for SPDX. Until then, the source retains
a visible SPDX placeholder.

**Files after results exist:** `sections/03-methodology.tex`, `sections/07-discussion.tex`, and potentially
the abstract or Table 1 note if space and relevance warrant it

**Done when:** The audit is actually completed and its unit count and Jaccard overlap are reported for all
three specifications without conflating positive-set overlap with reliability, accuracy, or exhaustive corpus
coverage.

**Procedure implemented; SPDX result pending:** The methodology excludes the original pilot, randomly samples
pages corresponding to 10% of each specification's total page count, divides them into primary units, blinds
the primary analyst to NotebookLM output during human labeling, and applies the same binary primary-unit
decision used in the pilot. It reports Jaccard positive-unit overlap for CycloneDX and CISA ME-SBOM, records a
second-analyst review of all disagreements after scoring, and retains a bold TBA marker only for SPDX. Threats
to Validity preserves the non-exhaustive-coverage boundary.

### [x] I5. Clarify the primary unit and the interpretation of extraction kappa

**Criticism:** The extraction procedure does not define the decision unit clearly enough, particularly for
SPDX's table-driven material.

**Proposed resolution:** Add the compact primary-unit definition under I4. Explain that annotators first
decided whether a unit contained normative content and then extracted its separable requirement(s). Preserve
the existing explanation that Stage 1 SPDX disagreements included row/cell/linked-definition boundary
choices; characterize that first score as agreement under the initial protocol, with Stage 2 measuring the
refined boundary rules.

**Files:** `sections/03-methodology.tex`

**Done when:** A reviewer can reconstruct what the annotators saw, what decision they made, and why the Stage
1/Stage 2 scores changed without reading the supplementary prompts.

**Implemented:** The methodology defines the primary unit, binary extraction decision, and multiple-row case.
It explains the SPDX boundary problem and treats Stage 1 kappa as a conservative consistency indicator because
the initial disagreements included unitization. The thematic subsection separately explains why it reports
within-specification agreement rather than one pooled kappa across different codebooks.

**Verified:** The primary-unit definition, binary decision, multiple-row case, Stage 1 unitization caveat,
pilot-only table note, and within-specification thematic-agreement rationale render across pp. 2--4 of
`SCORED_2026_SBOM (6).pdf`.

### [x] I6. Make the proposed conformance suite practically actionable without claiming evaluation

**Criticism:** Section 6 proposes a three-level conformance suite but does not implement or evaluate it.

**Writing-only resolution:** Keep it explicitly a design proposal, then add a compact implementation path:
Level 1 can be encoded as profile-specific schema/presence rules in existing validators (with an example only
if accurately cited); Level 2 needs producer declarations plus evidence/coverage checks; Level 3 combines
security-task profiles with external manifests, builds, containers, or runtime evidence. Do not claim a
prototype, performance, or validation result.

**Files:** `sections/06-root-causes.tex`, possibly `references.bib` if a concrete validator is named

**Done when:** The proposal is concrete enough for practitioners to act on while remaining clearly unevaluated.

**Implemented:** Level 1 maps to profile-specific schema and presence rules; Level 2 combines producer
declarations with evidence, filtering, graph, coverage, and absence checks; and Level 3 compares task-specific
claims with manifests, lockfiles, builds, containers, or runtime evidence. The design-proposal and
future-evaluation boundary remains explicit.

**Verified:** All three implementation paths render as separate, readable paragraphs on p. 9 of
`SCORED_2026_SBOM (6).pdf`; the section still identifies the suite as a proposal rather than a validated tool.

### [x] I7. Resolve targeted readability and local-reference defects

**Criticism:** Dense sentences and specialized phrasing hinder practitioner readability; Section 5.1.1
contains a self-reference to the ten CISA-derived fields used in Section 5.1.1.

**Proposed resolution:** Replace the self-reference with the actual methodology/table anchor, simplify the
densest sentences in the abstract and Section 3, and keep Figure 1 under visual regression review. Preserve
technical terms that carry analytical meaning, but define them once and use plainer verbs around them.

**Files:** `main.tex`, `sections/03-methodology.tex`, `sections/05-tool-implementation.tex`, Figure 1 only if
the next PDF exposes a genuine legibility regression

**Done when:** No circular reference remains, the core method can be followed by a practitioner, and the
figure is legible at the compiled size.

**Implemented:** The CISA subsection points to the methodology's ten-field operationalization rather than to
itself; dense summary and methodology prose was simplified; and stylistic em/en-dash constructions were
removed throughout the active TeX. The literal `--include-dev-deps` flag, comments, and TikZ path syntax were
preserved because they are code rather than prose. Figure 1 was not changed because its previous PDF passed
legibility review.

**Verified:** The Section 5 reference points to the ten-field operationalization in Section 3.4, the revised
abstract and method remain readable, Figure 1 is contained and legible on p. 3, and the full PDF has no visible
em/en-dash prose regression, clipping, or overlap.

### [-] I7b. Make the takeaway boxes self-contained and clarify Section 5.2's security relevance

**Criticism:** The gray boxes should state useful results in plain language, avoid double negatives such as
``No selected applicable SPDX rule was Unmet,'' and Section 5.2 does not clearly explain what its schema/prose
comparison contributes to security.

**Resolution:** Rewrite all nine Section 4 and 5 boxes as self-contained findings or implications. Lead the
Section 5.2 box with the positive SPDX control result and the concrete CycloneDX counts. Rename the subsection
to ``Security-Relevant Schema Gaps'' and explain that dependency-entry coverage supports dependency-aware
security analysis while remaining a structural check rather than a vulnerability-outcome experiment.

**Files:** `sections/04-specification-analysis.tex`, `sections/05-tool-implementation.tex`

**Implemented:** Every box now states a concrete result or actionable interpretation without the original
double negative. Section 5.2 distinguishes the SPDX control result from the CycloneDX finding that 13 cdxgen
and 3 Syft outputs omitted required empty dependency entries not enforced by the schema. It explains the
security relevance as ambiguity between an asserted leaf and unreported graph status, while explicitly
stating that downstream vulnerability decisions were not tested.

**Done when:** The next compiled PDF shows all nine boxes clearly, preserves the 11-page limit, and keeps the
revised Section 5.2 heading and security explanation together without an awkward page break.

### [-] I8. Reserve empirical-scope expansion and PyPI reconstruction for the final factual batch

**Criticism:** The dynamic evidence is limited to 18 unnamed PyPI repositories, one ecosystem, and three SPDX
artifacts.

**Resolution dependency:** This is G1. Await the advisor decision on retaining PyPI or adding npm/Maven, then
report only the study actually performed: selection date, ranking source/metric, complete package list,
excluded packages/reasons, ecosystem boundary, and exact artifact counts. Do not infer causes for the sparse
Trivy/Syft outputs without logs.

**Done when:** G1 is closed and the artifact exposes the package/artifact inventory.

### [-] I9. Replace TBA with a one-click anonymous artifact and audit it for anonymity

**Criticism:** The 2,286-row corpus and clause identifiers are central contributions but cannot be audited
while Artifact Availability says TBA.

**Resolution dependency:** This is G3/C2 and remains explicitly reserved for the end. Upload the confirmed
inventory to an anonymous one-click repository, replace `\textbf{TBA}` with the stable reviewer link, test it
signed out, and inspect archive filenames, metadata, repository history, README text, generated documents,
and URLs for author identities.

**Files:** `sections/07-availability.tex`, archive inventory, `sections/appendix1.tex`

**Done when:** The anonymous link works without authentication, the promised files are present, and neither
the manuscript nor archive deanonymizes the authors.

### [ ] I10. Final four-round submission QA and page-budget regression check

**Resolution:** After I1--I9 and the final factual inputs, compile the exact submission source and inspect all
pages at realistic size. Recheck title/running headers, anonymity, references and DOI/ISBN metadata,
cross-references, clause IDs, table denominators, all nine takeaway boxes, Figure 1, appendix floats, and the
11-page limit. Re-run the full A--I checklist; do not close an item based only on source text.

**Done when:** The submission PDF is internally consistent, anonymous, visually clean, within the CFP limit,
and every closed item is supported by both source and compiled-PDF evidence.
