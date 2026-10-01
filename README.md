# Skills Engine

A personal skills library for improving agentic working methods through real use.

Work through a real problem, capture the useful method, use it in a fresh session, extract evidence, revise, and repeat. A committed revision is a hypothesis about better execution; reuse supplies the evidence.

## First version

| Skill | Contribution |
|---|---|
| [outline](skills/core/outline/SKILL.md) | Structured understanding |
| [grill](skills/core/grill/SKILL.md) | Adaptive questioning and challenge |
| [recast](skills/core/recast/SKILL.md) | Blind reconstruction from an outline, verification, and incidental diff minimisation |
| [extract](skills/core/extract/SKILL.md) | Durable capture of useful session outcomes |
| [composition](skills/core/composition/SKILL.md) | Interpretation and execution semantics for composed skills |
| [improve-skill](skills/improve-skill/SKILL.md) | Evidence-based improvement, including itself |
| [recast-unit-tests](skills/recast-unit-tests/SKILL.md) | First concrete composed application |

These are initial drafts derived from an exercised test-recreation process and subsequent design discussion. Their effectiveness needs evidence from real use. Static analysis and evaluation approaches remain open questions in [TODO.md](TODO.md).

Shared building blocks live in `skills/core/`. More specialised skills remain directly under `skills/` until concrete feature or domain groupings justify deeper structure.

## Composition

```text
headlessly
    recast "unit tests for src/example"
        independently
            blindly
                outline "existing unit test coverage"
            |> gate
            blindly
                outline "implementation behaviour and expected cases"
            |> gate
        |> "reconcile gaps, mismatches, and boundaries in both directions"
        |> grill "finalise the outline and course of action"
    |> extract
```

This is agent-interpreted notation, not a programming language or slash-command interpreter. Skill mention syntax and discovery depend on the harness. Load composition and the referenced skills explicitly if your harness does not discover them. Quoting a composition for discussion does not request execution.

A composed skill loads composition and the skills it names, then is invoked like any other skill. Composition provides their shared interpretation contract; it is not a separate execution command.

Indentation scopes policy. `|>` passes results. `gate` reports the preceding result for comprehension and correctness before passing its accepted or corrected form onward. `blindly` prevents descendants from inheriting parent task state. `openly` permits sibling state sharing, `collaboratively` requires useful coordination, and `independently` isolates siblings; each returns distinct labelled child outputs. None implies parallel scheduling. True isolation requires fresh contexts and controlled inputs; an instruction alone cannot erase information already seen.

## Local setup

```sh
git clone https://github.com/pseudo-su/skills-engine.git
cd skills-engine
scripts/link connect ~/.agents/skills
```

Use `~/.codex/skills` for Codex or `~/.claude/skills` for Claude Code. Connecting records the destination in gitignored checkout-local state and synchronizes its skill links. Each link points directly to a skill in this checkout. Existing unrelated entries are never overwritten. Keep the checkout at a stable path; moving it breaks links. Project/team skills can be connected to a project's discovery directory instead and maintained through its review process.

Synchronize or inspect every connected destination:

```sh
scripts/link sync
scripts/link status
```

Disconnecting clears links owned by this checkout and forgets the destination. Pass `--no-sync` to `connect` or `disconnect` to change only the recorded connection state.

```sh
scripts/link disconnect ~/.agents/skills
```

Synchronization also prunes owned links to skills removed from the checkout. The script does not configure the harness or install anything until invoked.

See [linking authored skills](docs/linking-skills.md) for the complete interface, ownership rules, and synchronization behavior.

## Ownership and evolution

Authored skills live in `skills/`. Public imports will live in `upstream/`, with their source, pinned revision, license, and adaptations tracked in [upstreams.json](upstreams.json). None are imported yet. See [upstream maintenance](docs/upstream-maintenance.md).

Prefer cohesive skills; extract shared methods when experience shows a useful independent boundary. Keep project-specific knowledge in project repositories where it belongs. Improve canonical sources, not copied installation directories. Do not introduce an overlay system until an actual adaptation requires it.

See [principles](docs/principles.md) and [working conventions](AGENTS.md).
