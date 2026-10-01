---
name: outline
description: "Construct a factual representation of a subject from bounded evidence at the requested granularity or at increasing levels of granularity until a requested stopping condition is met. Use when asked to outline a subject according to code, tests, documentation, plans, or other specified evidence; do not propose, reconcile, or rewrite the subject."
---

# Outline

## Establish the scope

Determine the subject and permitted evidence from the request. For simple outlining, determine the requested granularity. For progressive outlining, determine the starting granularity and stopping condition.

Inspect the permitted evidence in full within scope. Do not inspect excluded sources or expand into transitive material merely because it is available.

## Represent the subject

Represent the subject as meaningful parts with the concrete facts supported about each part:

```text
- meaningful part of the subject
  - concrete fact
  - concrete fact
```

Choose parts appropriate to the subject and requested granularity rather than mirroring how the evidence is stored. Do not invent intermediate groupings merely to give the outline more levels.

For every outline:

- Include every materially supported concrete statement in its appropriate position.
- Keep distinct statements separate.
- Preserve contradictions directly in the hierarchy.
- Organise and condense the evidence without reconciling conflicts, proposing improvements, inferring unsupported details, or filling apparent gaps.

## Simple outlining

Produce one outline at the granularity requested or implied by the request.

## Progressive outlining

Use progressive outlining when the request includes a stopping condition, such as `outline "Google until all its products and services are identified"`.

1. Produce the current outline.
2. Evaluate the stopping condition against the complete current outline.
3. Identify every part that requires refinement to meet the condition.
4. Outline each selected part as a narrower subject, deriving groupings appropriate to that subject.
5. Ensure each narrower outline preserves or more precisely represents every material fact it will replace.
6. Replace the selected part's existing facts with the narrower outline's parts and facts. Retain the existing facts beneath unexpanded parts.
7. Apply the evidence-faithfulness rules to each intermediate refinement and to the complete consolidated outline.
8. Repeat until the complete consolidated outline satisfies the stopping condition.

Stop when the requested condition is met, not when no further decomposition is possible. Treat claims of completeness as bounded by the permitted evidence. Allow intentionally uneven depth when only some parts require expansion to meet the condition.

## Return the result

Return the completed outline as the operation's outcome. Persist it only when required by the enclosing workflow or explicitly requested.
