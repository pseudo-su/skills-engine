---
name: recast
description: "Reconstruct a target from a structured outline, using blind recreation, verification, comparison, and incidental diff minimisation. Accept an outline or a description/block that derives one. Use for deliberate from-scratch reconstruction, not ordinary incremental editing."
---

# Recast

## Obtain the outline

Accept a supplied outline, or execute the supplied description/block to derive one. Establish the target, intended outcome, scope, invariants, deliberate changes, and verification. Refine the outline until a writer can execute it without the old implementation or its authoring conversation. This readiness check belongs here.

Keep original material as evidence for the outline and later comparison. Carry forward useful judgement, precise outcomes, and safeguards; exclude structural choices being reconsidered. Account for existing behaviour explicitly as preserved, changed, or intentionally removed. Resolve uncertainty under the active interaction policy.

## Preserve recovery and recreate

Ensure the original state is recoverable before replacing it, using the project's version control or a verified snapshot. Preserve uncommitted user work. Do not require a redundant backup confirmation when recoverability is already established.

Use a fresh writer context with only the approved outline, necessary domain inputs, conventions, and verification commands. Hide the implementation being replaced and the discussion that shaped it. For tests, the production source is necessary input; the old test implementations are excluded. Restrict file access or use a staged view to avoid accidental exposure. Do not delete the only recoverable copy just to create blindness.

If the environment cannot provide a fresh isolated writer, report that limitation before claiming blind recreation. Produce the replacement from scratch. Run appropriate verification, repair failures, and map every outlined requirement to the replacement. Flag unaccounted losses.

## Evaluate and minimise diff

Compare the replacement with both the outline and the original. Assess correctness, omissions, boundary quality, and whether the intended improvement was achieved. Use a fresh reviewer where supported; give it task-local criteria and artifacts without feeding it prior diagnoses.

Minimise incidental diff as part of recast. Restore useful wording, names, fixture values, formatting, and assertion strength when no deliberate change requires their replacement. Do not restore obsolete structure or weaken correctness to reduce the diff. The comparison pass can see originals; the blind writer cannot. Verify again after material changes.

Adopt, revise, or reject based on the evidence. Return the result, requirement accounting, substantive findings, verification performed, and limitations. Under headless, include consequential assumed decisions and how to revisit them. Reconstruction is an experiment, not proof that the replacement is better.
