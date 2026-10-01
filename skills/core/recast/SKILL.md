---
name: recast
description: "Reconstruct a target from a structured outline, using blind recreation, verification, comparison, and incidental diff minimisation. Accept an outline or a description/block that derives one. Use for deliberate from-scratch reconstruction, not ordinary incremental editing."
---

# Recast

## 1. Prepare an executable outline

Accept a supplied outline, or execute the supplied description/block to derive one. Establish the target, intended outcome, scope, invariants, deliberate changes, and verification. Refine the outline until a writer can execute it without the old implementation or its authoring conversation. This readiness check belongs here.

Use the original material as evidence for the outline. Carry forward useful judgement, precise outcomes, and safeguards; exclude structural choices being reconsidered. Account for existing behaviour explicitly as preserved, changed, or intentionally removed. Resolve uncertainty under the active interaction policy.

## 2. Preserve the original

Keep the original for later comparison. Ensure its exact state is recoverable through the project's version control or a verified snapshot before replacing it. Preserve uncommitted user work. Do not require redundant backup confirmation when recoverability is already established.

## 3. Remove the target and isolate the writer

Confirm that a fresh writer context and the required source restrictions are available. If they are not, report the limitation before removing the target or claiming blind recreation.

After verifying recoverability, completely remove the target from its working location before starting the fresh writer. Do not delete the only recoverable copy just to create blindness.

Use a fresh writer context with only the approved outline, necessary domain inputs, conventions, and verification commands. Hide the recoverable original and the discussion that shaped it. For tests, the production source is necessary input; the old test implementations are excluded. Restrict file access or use a staged view to prevent access through version control, snapshots, or other paths.

If the outline must cross the context boundary through a temporary artifact, treat that artifact as part of the workflow rather than permanent documentation and remove it only after its result is accepted.

## 4. Recreate and verify the target

Require the blind writer to recreate the absent target from scratch. Adopt its complete output as the replacement baseline; do not use it merely as guidance for incrementally editing the original. Run appropriate verification and repair failures while the original remains hidden. Restore access to the original only after the replacement baseline has been created and verified. Apply all subsequent changes to the replacement.

## 5. Account for the outline

First compare the replacement with the outline and account for every requirement. Use a concrete mapping such as:

```text
| Outlined requirement | Replacement evidence | Status | Notes |
|---|---|---|---|
| condition and outcome | resulting location | present, changed, omitted, or missing | rationale |
```

Every omission or deliberate change needs a reason; every unexplained missing requirement must be resolved or reported. Account in the other direction as well: identify replacement elements not justified by an outlined requirement and retain them only with a reason. Run verification against the resulting state and require the success criteria established in the outline.

## 6. Compare with the original

Compare the replacement with the original to minimise incidental diff. Restore useful wording, names, fixture values, formatting, and assertion strength when no deliberate change requires their replacement. Do not restore obsolete structure or weaken correctness to reduce the diff. Verify again after material changes.

## 7. Review and decide

Finally review correctness separately from incidental diff. Assess omissions, boundary quality, and whether the intended improvement was achieved. Use a fresh reviewer where supported; give it the final candidate, task-local criteria, and necessary artifacts without feeding it prior diagnoses or conclusions. Address substantive findings, ignore mere style preferences, and verify after material changes.

Adopt, revise, or reject based on the evidence. Return the result, requirement accounting, substantive findings, verification performed, and limitations. Under `headlessly`, include consequential assumed decisions and how to revisit them. Reconstruction is an experiment, not proof that the replacement is better.
