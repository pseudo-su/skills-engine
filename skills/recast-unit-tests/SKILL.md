---
name: recast-unit-tests
description: "Rebuild unit tests from independently derived coverage and implementation outlines, reconciled and grilled before blind reconstruction. Use when asked to recreate tests or fix stale test boundaries; loads composition and the referenced primitive skills."
---

# Recast Unit Tests

Load composition, outline, grill, recast, and extract from this collection. Honour an enclosing interaction policy; otherwise use normal interaction. Resolve source/test targets and the test runner before starting. Limit scope to directly exercised source units; do not absorb separately tested transitive dependencies.

```text
recast "unit tests for the requested target"
    independently
        outline "existing unit test coverage from target tests only"
        outline "expected cases from target implementation only"
    |> "reconcile coverage, behaviour, and unit boundaries in both directions"
    |> grill "finalise the complete outline and course of action"
|> extract
```

For reconciliation, match condition and expected outcome semantically. Identify stale/misplaced cases, missing expected cases, suspicious source behaviour, and cases already aligned. Assess both file placement and mock/assertion/setup boundaries. Produce a complete intended suite, including file changes, shared fixtures, exact scenarios, arrange/act/assert details, verification command, and deliberate removals.

Supply the implementation-outlining agent only scoped source paths and task instructions, never existing tests or the existing-coverage inventory. Recast's writer receives the final outline and production source, without the old test implementations. Preserve useful exact outcomes and assertion requirements in the outline; recover incidental wording and formatting during recast's comparison pass.

Extraction should consider a concise PR description explaining substantive test issues fixed and new files, plus evidenced skill learnings or genuine remaining work. Do not manufacture artifacts for phases with nothing worth retaining.
