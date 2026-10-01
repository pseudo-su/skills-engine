# Working in Skills Engine

Maintain working methods from evidence, not a generic catalogue of potential skills. Read the relevant skill and real execution artifacts before changing a method. Keep changes concise and distinguish process improvements from structural refactoring.

Canonical authored skills live in skills/. Global harness entries should be symlinks to this checkout. Project-specific conventions belong in their project repository. Imported skills retain provenance and licenses; consult upstreams.json before modifying upstream/.

Composition semantics live in skills/core/composition/SKILL.md. Consult that skill before changing or applying composition, and preserve its information-flow and scoping contracts. Composition is instruction notation; do not build an interpreter, dependency engine, or overlay mechanism without a concrete need.

Exercise link installation, stale-link pruning, and removal in a temporary directory when changing scripts/link. Process revisions need evidence from fresh use; record what has and has not been evaluated. Static analysis and evaluation approaches are undecided; consult TODO.md before introducing infrastructure.

Use normal git review and recovery. Never stage unrelated user work or overwrite an occupied installation path. Do not choose a repository-wide license on the owner's behalf.
