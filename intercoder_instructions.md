# Intercoder Check Instructions

## Purpose

This artifact prepares materials for an independent second-coder check. It does not contain completed second-coder decisions, agreement rates, Cohen's kappa, weighted kappa, or resolved disagreements.

## Task Priority

Primary task:

- Independent full coding of the strongest evidence output for all 31 Core studies.

Optional task:

- Sampled review of corpus layer, legacy A-profile, evidence object, and external-evidence profile.

The primary task matches the current manuscript synthesis, which uses natural-language workflow, capability, and evidence-output fields rather than the historical A/E axis as its main prose structure.

## Independence Requirement

The second coder must complete coding independently. For the 31-Core primary task, give the coder:

- `evidence_output_codebook.md`;
- `data/core31_second_coder_blind.csv`;
- the public papers and public project/artifact pages listed in the blind file.

Do not give the second coder `data/core31_second_coder_adjudication_template.csv` before independent coding is complete. That file contains original labels and is only for later comparison, disagreement discussion, and adjudication. The second coder should not inspect original A/E labels, original evidence labels, original evidence objects, adjudication fields, or any answer key before recording their own decisions.

Agreement rates and Cohen's kappa require real second-coder decisions. They must not be invented, estimated, or reported from blank templates.

## Primary CSV Fields

Fill `data/core31_second_coder_blind.csv` during the primary task.

- `core_id`: stable Core-study identifier.
- `record_id`: candidate record identifier from the artifact.
- `system_alias`: short system or benchmark name.
- `title`: record title.
- `publication_status`: public-material status known to the artifact.
- `materials_to_review`: non-sensitive instruction describing which public materials to inspect.
- `coder2_strongest_evidence_output`: second coder's strongest-evidence-output decision. Use `candidate judgment`, `controlled task completion`, `runtime safety signal`, `reproducible validation`, `externally traceable material`, `claim-level audit material`, or `governance boundary case`.
- `coder2_decision_reason`: short justification grounded in the paper or public material.
- `coder2_uncertainty_note`: optional uncertainty note, including missing material or ambiguous evidence boundary.

## Optional Sampled Review

If reviewer time allows, the author may also ask for a sampled review of corpus layer and historical A/E-style fields using `data/intercoder_sample_blind.csv` and `data/intercoder_check_template.csv`. This optional task should remain separate from the 31-Core strongest-evidence-output task.

The sample may include:

- 10--12 Core studies;
- 8--10 Core / Supporting boundary records;
- 5--8 Supporting studies.

The optional task can inspect corpus layer, legacy A-profile, evidence object, and external-evidence profile. It should not be used to claim full-corpus agreement.

## Adjudication Workflow

After independent coding is complete:

1. Copy coder2 decisions into `data/core31_second_coder_adjudication_template.csv` or an equivalent adjudication sheet.
2. Compare coder2 decisions with the original labels.
3. Mark disagreements in the disagreement fields.
4. Discuss disagreements with reference to `evidence_output_codebook.md`, `codebook.md`, and the public materials.
5. Record final adjudicated decisions only after review.
6. Preserve the original coder2 decision, reason, uncertainty note, disagreement note, and adjudicated result.

## Agreement Calculation

After real second-coder decisions exist, the author may calculate:

- raw agreement for strongest evidence output;
- Cohen's kappa for strongest evidence output, if the category set is appropriate and all rows are coded;
- optional raw agreement for sampled corpus layer, legacy A-profile, evidence object, and external-evidence profile.

Blank coder2 fields mean coding is incomplete. In that state the artifact may warn that second-coder results are pending, but it must not report agreement or kappa.

## Security Boundary

Do not include undisclosed PoCs, exploit payloads, private target details, sensitive crash inputs, private vendor communication, or vulnerability reproduction steps in any intercoder file. If a decision depends on sensitive material, record a non-sensitive reason and mark the source as restricted.
