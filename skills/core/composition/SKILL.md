---
name: composition
description: "Interpret and perform indentation-based compositions of skills, including scoped user-interaction and context-sharing policies, pipes, and gates. Use when given composition notation or when loaded by a composed skill; do not treat quoted examples as execution requests."
---

# Composition

Interpret this notation as instructions for an agent, not executable code. Load the referenced skills from their canonical locations before applying them. Resolve names against this collection and the active project; identify ambiguous or missing skills instead of inventing their contracts. Plain-language steps are allowed and need not be separate skills.

A composed skill must load composition and the skills it names. Invoke the composed skill normally; composition supplies the shared interpretation and execution contract rather than a separate runtime step.

## Core primitives

- **Indentation:** give an operation or policy a child block and establish its scope. Evaluate the block and supply its result to the containing operation, subject to that operation's contract. A scoped execution policy governs its descendants according to its policy type.
- **`|>`:** pass the preceding result into the next operation. At a given indentation level it connects adjacent expressions. A block returns its final expression unless its primitive specifies otherwise. Supplying an expression as a child block or piping its result into the containing operation are equivalent when that operation accepts the same input in either position.
- **Raw strings:** interpret a string in expression position as instructions to perform. Interpret a string following a named operation as an argument to that operation. Raw-string instructions are not implied named primitives.
- **`gate`:** receive the preceding result, present it for user comprehension and correctness review, and wait for acceptance or corrections before dependent work continues. Return the accepted or corrected result without changing its output shape. A gate reviews the produced artifact; it does not perform the adaptive investigation of `grill`.

## Scoped execution policies

A policy governs how work in its indented block is performed. Policies governing different concerns or context relationships are orthogonal and can be nested. Leaving a policy's block restores its enclosing or default behaviour.

### User interaction policies

Normal interaction applies when no interaction policy is present. An interaction policy governs every operation and decision point in its block, including gates and grills. An inner interaction policy overrides its enclosing interaction policy within that subtree.

- **`headlessly`:** resolve ordinary clarification and confirmation points using the best-supported decision and continue. At a gate, review and correct the result autonomously. An inner grill still challenges the subject, but resolves its questions internally without simulating user approval. Prefer reversible choices when evidence is weak and preserve settled preferences and constraints. Keep a concise record of consequential assumed decisions, rationale, uncertainty, affected work, and how to revisit them; report it when the scope completes. Do not invent facts, credentials, consent, or authorisation, and stop for genuine blockers.
- **`cautiously`:** surface meaningful proposed choices earlier and add gates where earlier confirmation can prevent consequential misalignment, especially for competing interpretations, scope changes, removals, changed expectations, and adoption of reconstructed results. Always honour explicit and policy-added gates and wait for acceptance or corrections. Make checkpoints concrete and reviewable, group related decisions, and avoid redundant gates around an explicit gate. Continue independent read-only or reversible preparation while waiting, but do not advance dependent work.

### Context sharing policies

- **`blindly`:** perform the block in a fresh context without inherited parent task state. Supply only the block's incoming input, explicit instructions and arguments, referenced skill definitions, and necessary project, verification, system, and safety instructions. Permit explicitly supplied evidence even when its type would otherwise be excluded. Exclude all other enclosing conversation, evidence, implementations, and parent artifacts. Restrict access to unassigned sources through files, version control, snapshots, and alternate paths. Return the block's normal result. If a fresh controlled context or source restriction cannot be provided, disclose the limitation and do not claim blind execution.
- **`independently`:** return a labelled collection of distinct child results while isolating siblings from one another. Children may inherit the same permitted parent state, but must not see one another's evidence, working state, outputs, or conclusions until all children finish. Use fresh child contexts and restrict shared artifacts where supported. If sibling isolation cannot be achieved, disclose the limitation and do not claim independent results.
- **`openly`:** perform each child as a distinct task and return all child results, labelled by task. Children may share context, evidence, working state, outputs, and conclusions, and may communicate before completion. Sharing is permitted, not required. No execution order or parallelism is implied.
- **`collaboratively`:** return the same collection while requiring children to coordinate where it can improve their assigned work. Share relevant evidence and intermediate state, exchange questions and feedback, and allow children to adapt their work in response while retaining distinct task ownership and labelled results. No execution order or parallelism is implied.

For `openly`, `collaboratively`, and `independently`, each child receives the block's incoming input plus its explicit arguments, not the previous child's output. After the block, the parent can inspect and combine every result. Under `independently`, do not let children read sibling artifacts. A gate inside an independent child exposes only that child's result, and its review must not provide sibling evidence or conclusions to that child or any unfinished sibling.

## Skill application

Treat descriptions as task-specific inputs, not permission to discard a skill's constraints. Reading a skill to inspect or discuss it does not initiate its procedure. Interpret an execution request in light of the user's stated intent.

Scoped execution policies configure their blocks rather than acting as ordinary pipeline stages. `openly`, `collaboratively`, and `independently` additionally return the labelled collection of child results. `recast` accepts a supplied outline or a block/description that produces one. Its block's result is the reconstruction brief. `extract` receives the preceding outcome and uses the session as evidence; it does not merely serialise the preceding value.

Keep composition short. Preserve each constituent skill's contract rather than copying its entire procedure into the composition. If a detail has no named primitive, express it in plain language. Naming, branching, retries, and scheduling syntax are not defined in this version.

## Example

```text
cautiously
    recast "unit tests for the requested target"
        independently
            blindly
                outline "existing test coverage; inspect only the target tests"
            |> gate
            blindly
                outline "expected cases; inspect only the target implementation"
            |> gate
        |> "reconcile coverage, behaviour, and boundaries in both directions"
        |> grill "finalise the outline and course of action"
    |> extract
```

Before execution, resolve the target, source paths, test paths, and verification command. The blind tasks receive their respective paths without inheriting the parent transcript, and independence prevents them from sharing their evidence or conclusions. The plain-language reconciliation step produces a proposed complete outline.
