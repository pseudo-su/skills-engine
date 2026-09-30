---
name: outline
description: "Construct a structured understanding of a target or target description for comparison, planning, or reconstruction. Use when asked to outline code, tests, skills, processes, or expected behaviour; do not rewrite the target."
---

# Outline

Resolve the subject and purpose from the supplied target or description. Inspect the authoritative material in full within scope. Follow context restrictions imposed by the caller; do not expand into excluded evidence or transitive dependencies merely because they are available.

Represent the understanding in a form suitable for its consumer. Group by meaningful units. Record conditions and outcomes, responsibilities, boundaries, constraints, and relevant failure or edge cases. Distinguish observed behaviour, inferred expectations, and unresolved questions. Include evidence locations where useful.

For existing tests, enumerate what each test actually arranges, exercises, and asserts, including assertion strength and collaborator boundaries. For implementation, derive expected cases from every relevant function and branch without assuming the code is correct; flag suspicious behaviour for a decision rather than blessing it as a requirement.

For an outline intended for recast, include the complete intended state: units or files, interfaces, shared setup, conditions, actions, expected outcomes, verification, and deliberate removals. Preserve valuable requirements and rationale, without reproducing implementation details the reconstruction is meant to reconsider.

Keep the outline self-contained. Do not silently change the target or present proposals as existing facts. Ask about material uncertainty according to the active interaction policy. Return the outline and its unresolved questions; persist it only when needed by the workflow or requested.
