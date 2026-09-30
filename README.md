# Skills Engine

A personal skills library for improving agentic working methods through real use.

Work through a real problem, capture the useful method, use it in a fresh session, extract evidence, revise, and repeat. A committed revision is a hypothesis about better execution; reuse supplies the evidence.

## First version

| Skill | Contribution |
|---|---|
| [outline](skills/outline/SKILL.md) | Structured understanding |
| [grill](skills/grill/SKILL.md) | Adaptive questioning and challenge |
| [recast](skills/recast/SKILL.md) | Blind reconstruction from an outline, verification, and incidental diff minimisation |
| [extract](skills/extract/SKILL.md) | Durable capture of useful session outcomes |
| [headless](skills/headless/SKILL.md) | Scoped autonomous decisions with a final assumptions record |
| [cautiously](skills/cautiously/SKILL.md) | Scoped, more frequent alignment checks |
| [composition](skills/composition/SKILL.md) | Scope, pipes, and context boundaries |
| [improve-skill](skills/improve-skill/SKILL.md) | Evidence-based improvement, including itself |
| [recast-unit-tests](skills/recast-unit-tests/SKILL.md) | First concrete composed application |

These are initial drafts derived from an exercised test-recreation process and subsequent design discussion. Their effectiveness needs evidence from real use. Static analysis and evaluation approaches remain open questions in [TODO.md](TODO.md).

## Composition

```text
headless
    recast "unit tests for src/example"
        independently
            outline "existing unit test coverage"
            outline "implementation behaviour and expected cases"
        |> reconcile "gaps, mismatches, and boundaries in both directions"
        |> grill "finalise the outline and course of action"
    |> extract
```

This is agent-interpreted notation, not a programming language or slash-command interpreter. Skill mention syntax and discovery depend on the harness. Load composition and the referenced skills explicitly if your harness does not discover them. Quoting a composition for discussion does not request execution.

Indentation scopes policy. `|>` passes results. `separately` returns distinct child outputs with shared context allowed; `independently` adds an information firewall. Neither implies parallel scheduling. True isolation requires fresh contexts and controlled inputs; an instruction alone cannot erase information already seen.

## Local setup

```sh
git clone https://github.com/pseudo-su/skills-engine.git
cd skills-engine
python3 scripts/link.py --destination ~/.agents/skills --dry-run
python3 scripts/link.py --destination ~/.agents/skills
```

The explicit destination keeps harness integration configurable. Use `~/.claude/skills` instead for a Claude Code installation that discovers that directory. Each link points directly to a skill in this checkout. Existing unrelated entries are never overwritten. Keep the checkout at a stable path; moving it breaks links. Project/team skills can be linked into a project's discovery directory instead and maintained through its review process.

Unlink using the same checkout and destination:

```sh
python3 scripts/link.py --destination ~/.agents/skills --remove
```

Only links owned by this checkout are removed. These scripts do not configure the harness or install anything until invoked.

## Ownership and evolution

Authored skills live in `skills/`. Public imports will live in `upstream/`, with their source, pinned revision, license, and adaptations tracked in [upstreams.json](upstreams.json). None are imported yet. See [upstream maintenance](docs/upstream-maintenance.md).

Prefer cohesive skills; extract shared methods when experience shows a useful independent boundary. Keep project-specific knowledge in project repositories where it belongs. Improve canonical sources, not copied installation directories. Do not introduce an overlay system until an actual adaptation requires it.

See [principles](docs/principles.md) and [working conventions](AGENTS.md).
