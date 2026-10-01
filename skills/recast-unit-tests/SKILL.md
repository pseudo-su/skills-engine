---
name: recast-unit-tests
description: "Rebuild unit tests from independent outlines of the existing tests and implementation, correcting coverage and boundary problems through blind reconstruction. Use when recreating tests or bringing a stale suite back into alignment with the source."
---

# Recast Unit Tests

Load composition, outline, grill, recast, and extract from this collection. Honour an enclosing interaction policy; otherwise use normal interaction.

Resolve the target source files, existing test files, and test command before starting. When given tests, identify the source units they directly exercise. When given source, locate its tests. For a directory, enumerate the relevant source and test files. Include directly tested units only; do not absorb transitive dependencies that have their own unit-test boundary. If no existing tests are found, use an empty test-derived outline. If the target scope or test command cannot be established from available evidence, resolve it under the active interaction policy before outlining.

```text
recast "unit tests for the requested target"
    independently
        blindly
            outline "the requested target according to its existing tests; inspect no production implementation"
        |> gate
        blindly
            outline "the requested target according to its production implementation; inspect no existing tests"
        |> gate
    |> "reconcile the outlines into a complete reconstruction outline"
    |> grill "finalise the reconstruction outline and course of action"
|> extract
```

## Reconcile the outlines

Begin only after both independent outlines have passed their gates. Perform these passes in order. Keep their findings distinguishable until producing the reconstruction outline.

### Compare coverage

Match cases by condition and expected outcome, not wording. Classify every case as:

- **Aligned:** supported by both outlines.
- **Test-only:** present in the existing tests but absent from the implementation-derived outline. Investigate whether it is stale, misplaced, an undocumented requirement, or evidence of a source regression.
- **Implementation-only:** present in the implementation-derived outline but absent from the existing tests. Treat it as a potential coverage gap, not an automatic requirement.

List materially different input variations separately. When uncertain whether two cases are equivalent, keep them distinct until the uncertainty is resolved. Treat suspicious implementation behaviour as a decision rather than blessing it as required behaviour.

### Evaluate structural fit

Evaluate the placement of every existing case against the current source structure. Keep this separate from coverage gaps. Determine whether:

- Tests still combine source units that have split or duplicate setup for units that have merged.
- Each case is in the correct test file for the unit it exercises.
- A collaborator previously treated as an internal detail is now a separate unit boundary, or the reverse.

Record the intended file and unit for every misplaced case. Do not report an implementation-only case as a placement problem merely because no test currently exists.

### Evaluate semantic fit

Evaluate every existing test, including misplaced tests, at its intended unit boundary. Determine whether:

- Mocks stop at the unit's true external collaborators rather than reaching through them.
- Assertions cover the unit's observable outputs and side effects without asserting collaborator internals.
- Setup belongs to the unit under test rather than arranging hidden state inside a collaborator.
- Existing assertion strength and useful exact outcomes are preserved.

Record the correct mock, setup, and assertion boundary for every violation.

### Produce the reconstruction outline

Before synthesis, make the coverage, structural, and semantic findings reviewable and resolve consequential uncertainty under the active interaction policy. Then combine the three passes into the complete intended suite. Account for every existing and implementation-derived case. Do not discard useful coverage merely because its current placement or implementation is wrong.

Describe the complete intended suite rather than a diff. Include:

- Test files to create, replace, or remove.
- The responsibility of each resulting file.
- Shared fixtures and helpers.
- Every test's exact name and unit under test.
- Every scenario's condition and expected outcome.
- Arrange, act, and assert requirements.
- Required mock and collaborator boundaries.
- Deliberate removals and their reasons.
- The verification command.

For unit tests, successful recast verification requires a green relevant test suite. Treat every planned scenario as an outlined requirement: map it to a resulting test or give an explicit reason for its omission.
