# Contributing to the linker

This guide covers implementation constraints and verification for `scripts/link`. See [linking authored skills](../linking-skills.md) for the user-facing command and behavior reference.

## Responsibilities

The linker maintains two related forms of state:

- Destination state records the discovery directories this checkout should manage.
- Link state is derived from the symlinks currently present in each destination.

Recording a destination does not confer ownership over its contents. The linker owns only immediate-child symlinks whose lexically normalized targets lie strictly beneath this checkout's `skills/` directory. Targets do not need to exist.

## Processing model

The implementation separates its work into phases:

1. Parse the command and resolve checkout paths.
2. Load or initialize destination state.
3. Discover source skills only for operations that require them.
4. Inventory and classify every selected destination.
5. Preflight all selected destinations before mutation.
6. Update destination state at the command-defined boundary.
7. Remove owned links before creating desired links.
8. Remove temporary working files when the process exits.

Keep discovery, planning, and mutation visibly separate. State and helpers should use domain terms such as destinations, skill sources, owned targets, conflicts, removals, and links rather than generic processing names.

## Safety invariants

- Never overwrite an unrelated symlink, file, or directory.
- Report every known conflict across all selected destinations before modifying any destination.
- Preserve unrelated destination entries during synchronization, clearing, and destination removal.
- Remove stale or displaced owned links before creating desired links.
- Do not create a missing destination during clearing, removal, or status.
- Remove a destination from recorded state only after its owned links have been cleared successfully.
- Keep a destination recorded when synchronization fails after it has been discovered or initialized, so the failure remains visible and retryable.
- Treat status as informational: drift and conflicts do not produce failure when inspection itself succeeds.
- Use temporary replacement when updating destination state.

Global preflight protects against known conflicts but cannot make filesystem mutation transactional. An unexpected failure during application can leave earlier operations applied.

## Discovery and naming

Skill discovery recursively finds regular `SKILL.md` files beneath `skills/`. A skill's installed name is the basename of its manifest directory. Reject duplicate installed names even when their source directories differ.

Well-known destination discovery currently checks Codex, Claude, and Agents skill directories. It reports only directories that exist. Do not add automatic pruning without settling how temporarily missing and manually added destinations should behave.

## Verification

Exercise linker changes in an isolated checkout with a controlled home and temporary destinations. Do not use a developer's actual harness directories as mutation targets.

Cover behavior affected by the change, including where relevant:

- Empty and repeated initialization
- Well-known destination discovery
- Destination addition and removal
- Missing and existing destinations
- Dry-run and applied synchronization
- Clearing while retaining destination state
- Destination, synchronization, and combined status
- Idempotent synchronization
- Retargeting and stale-link pruning
- Duplicate installed names
- Invalid destination paths
- Preservation of unrelated entries
- Conflict preflight across multiple destinations with confirmation that no destination changed

Run Bash syntax and Git whitespace checks. Record which behaviors were exercised and which were not in the change handoff; do not treat structural checks as evidence of behavioral correctness. Static analysis and permanent evaluation design remain open questions in [`TODO.md`](../../TODO.md).

## Current evidence and limits

The current command model has been exercised in an isolated checkout for initialization, controlled Codex discovery, destination state, synchronization, clearing, status, retargeting, stale-link pruning, unrelated-link preservation, and cross-destination conflict preflight. The real checkout was used only for read-only status.

Claude and Agents discovery paths have not been separately exercised. Unexpected failures during plan application, concurrent registry writers, and recovery from corrupted destination state have not been evaluated. ShellCheck was unavailable during the current revision.
