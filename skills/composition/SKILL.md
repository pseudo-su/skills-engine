---
name: composition
description: "Interpret indentation-based compositions of skills, including scoped interaction policies, pipes, and separate or independent branches. Use when asked to compose methods or execute this notation; do not treat quoted examples as execution requests."
---

# Composition

Interpret this notation as instructions for an agent, not executable code. Load the referenced skills from their canonical locations before applying them. Resolve names against this collection and the active project; identify ambiguous or missing skills instead of inventing their contracts. Plain-language steps are allowed and need not be separate skills.

## Core primitives

- **Indentation:** give an operation a child block and establish its scope. Evaluate the block and supply its result to the containing operation, subject to that operation's contract. A wrapper governs all descendants and their decision points. The innermost explicit interaction policy overrides its enclosing policy within that subtree; restore the outer policy on leaving it.
- **`|>`:** pass the preceding result into the next operation. At a given indentation level it connects adjacent expressions. A block returns its final expression unless its primitive specifies otherwise. Supplying an expression as a child block or piping its result into the containing operation are equivalent when that operation accepts the same input in either position.
- **Raw strings:** interpret a string in expression position as instructions to perform. Interpret a string following a named operation as an argument to that operation. Raw-string instructions are not implied named primitives.
- **`separately`:** perform each child as a distinct task and return all child results, labelled by task. Shared context and collaboration are allowed. No execution order or parallelism is implied.
- **`independently`:** return the same collection, with isolation. Give each child only its assigned inputs and necessary shared instructions. Do not share siblings' evidence, working, outputs, or conclusions until all children finish. Restrict source access as well as message history. Use fresh contexts with task-specific inputs where supported. If isolation cannot be achieved, disclose the limitation; do not claim an independent result from a context that has already seen the excluded material.

For either branching primitive, each child receives the block's incoming input plus its explicit arguments, not the previous child's output. After the block, the parent can inspect and combine every result. Shared files are a possible information leak: do not let children read sibling artifacts.

## Skill application

Treat descriptions as task-specific inputs, not permission to discard a skill's constraints. Reading a skill to inspect or discuss it does not initiate its procedure. Interpret an execution request in light of the user's stated intent.

`headless` and `cautiously` wrap execution; they are not stages. An inner `grill` still probes choices under headless, but resolves them autonomously. `recast` accepts a supplied outline or a block/description that produces one. Its block's result is the reconstruction brief. `extract` receives the preceding outcome and uses the session as evidence; it does not merely serialise the preceding value.

Keep composition short. Preserve each constituent skill's contract rather than copying its entire procedure into the composition. If a detail has no named primitive, express it in plain language. Naming, branching, retries, and scheduling syntax are not defined in this version.

## Example

```text
cautiously
    recast "unit tests for the requested target"
        independently
            outline "existing test coverage; inspect only the target tests"
            outline "expected cases; inspect only the target implementation"
        |> "reconcile coverage, behaviour, and boundaries in both directions"
        |> grill "finalise the outline and course of action"
    |> extract
```

Before execution, resolve the target, source paths, test paths, and verification command. The independent tasks receive their respective paths, not a shared transcript containing the existing tests. The plain-language reconciliation step produces a proposed complete outline.
