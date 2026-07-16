# Intercoder Check Instructions

## Purpose

This artifact supports an independent second-coder check. The first completed pass is archived as a pilot calibration round under `archive/pilot_second_coder_round_1/`; its agreement and kappa should not be cited as formal intercoder reliability. The completed formal second-coder reliability files are included in `data/core31_second_coder_formal_results.csv` and `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md`; blank templates remain for future reruns if the codebook changes.

## Task Priority

Primary task:

- Independent full coding of the strongest evidence output for the 31-record study-level coded set.

Optional task:

- Sampled review of corpus layer, legacy A-profile, evidence object, and external-evidence profile.

The primary task matches the current manuscript synthesis, which uses natural-language workflow, capability, and evidence-output fields rather than the historical A/E axis as its main prose structure.

## Independence Requirement

The second coder must complete coding independently. For a future rerun of the 31-record primary task, give the coder:

- `evidence_output_codebook.md`;
- `SUBMISSION_UPDATE_SECOND_CODER_RERUN_NOTES.md`;
- `data/core31_second_coder_formal_blind_template.csv`;
- the public papers and public project/artifact pages listed in the blind file.

Do not give the second coder `data/core31_second_coder_adjudication_template.csv` before independent coding is complete. That file contains original labels and is only for later comparison, disagreement discussion, and adjudication. The second coder should not inspect original A/E labels, original evidence labels, original evidence objects, adjudication fields, or any answer key before recording their own decisions.

Agreement rates and Cohen's kappa require real second-coder decisions. They must not be invented, estimated, or reported from blank templates.

## Primary CSV Fields

Fill `data/core31_second_coder_formal_blind_template.csv` during a future formal primary-task rerun. The template is intentionally blank; completed formal results are stored separately.

- `core_id`: stable Core-study identifier.
- `record_id`: candidate record identifier from the artifact.
- `system_alias`: short system or benchmark name.
- `title`: record title.
- `publication_status`: publication/material status only. Boundary role is recorded separately.
- `boundary_role`: `standard_core_entry` or `governance_boundary_case`.
- `materials_to_review`: non-sensitive instruction describing which public materials to inspect.
- `coder2_strongest_evidence_output`: second coder's strongest-evidence-output decision. Use `candidate judgment`, `controlled task completion`, `runtime safety signal`, `reproducible validation`, `externally traceable material`, `claim-level audit material`, or `governance boundary case`.
- `coder2_decision_reason`: short justification grounded in the paper or public material.
- `coder2_uncertainty_note`: optional uncertainty note, including missing material or ambiguous evidence boundary.

## Optional Sampled Review

If reviewer time allows, the author may also ask for a sampled review of corpus layer and historical A/E-style fields using `data/intercoder_sample_blind.csv` and `data/intercoder_check_template.csv`. This optional task should remain separate from the 31-Core strongest-evidence-output task.

The sample may include:

- 10--12 study-level coded records;
- 8--10 study-level coded / extended-synthesis boundary records;
- 5--8 extended synthesis studies.

The optional task can inspect corpus layer, legacy A-profile, evidence object, and external-evidence profile. It should not be used to claim full-corpus agreement.

## Submission-Update Independent Review

The 2026-07-15 sensitivity search has a separate 41-row blind template: `data/submission_update_20260715_second_coder_blind_template.csv`. Use it to independently decide the analytical layer before coding lifecycle coverage, primary system shape, cross-stage capabilities, strongest evidence output, external traceability, and claim boundary. Do not inspect `data/submission_update_20260715_full_coding_audit.csv` before completing the pass because that file contains the author decisions.

The tightened-boundary rerun uses `data/submission_update_20260715_second_coder_rerun_blind_template.csv` together with `SUBMISSION_UPDATE_SECOND_CODER_RERUN_NOTES.md`. The original blank update template and previous pass are retained for provenance. The adopted independent rerun decisions are in `data/submission_update_20260715_second_coder_results.csv`, and their pre-adjudication agreement is reported in `reports/SUBMISSION_UPDATE_SECOND_CODER_PRE_ADJUDICATION_REPORT.md`. The existing 31-record agreement results do not apply to these update-search records. The assistant-prepared working draft preserves both inputs; the author-confirmed resolution is stored separately in `data/submission_update_20260715_adjudicated.csv`. This finalization records author acceptance of an evidence-based resolution and is not described as two-human consensus or third-coder adjudication.

## Post-Coding Comparison

Only after independent coding is complete:

1. Copy `coder2_strongest_evidence_output`, `coder2_decision_reason`, and `coder2_uncertainty_note` into `data/core31_second_coder_adjudication_template.csv` or an equivalent adjudication sheet.
2. Compare coder2 decisions with `original_strongest_evidence_output`; legacy E-level fields are retained only for historical traceability or fallback.
3. Mark disagreements in the disagreement fields.
4. Discuss disagreements with reference to `evidence_output_codebook.md`, `SUBMISSION_UPDATE_SECOND_CODER_RERUN_NOTES.md`, `codebook.md`, and the public materials.
5. Record final adjudicated decisions only after author review; an assistant-prepared working draft is a proposal, not human consensus.
6. Preserve the original coder2 decision, reason, uncertainty note, disagreement note, and adjudicated result.

## Agreement Calculation

After the future formal second-coder decisions are complete, the author may report:

- raw agreement for strongest evidence output;
- Cohen's kappa for strongest evidence output.

Optional sampled review of corpus layer, legacy A-profile, evidence object, and external-evidence profile remains separate. Multi-label fields should use row-level exact agreement, mean row Jaccard, micro F1, and per-label summaries rather than a single-label kappa. Blank or incomplete coder2 fields mean coding is incomplete; in that state the artifact must warn rather than report formal agreement or kappa. Pilot agreement/kappa values are calibration notes only.

## Security Boundary

Do not include undisclosed PoCs, exploit payloads, private target details, sensitive crash inputs, private vendor communication, or vulnerability reproduction steps in any intercoder file. If a decision depends on sensitive material, record a non-sensitive reason and mark the source as restricted.

