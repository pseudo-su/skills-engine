# Linking authored skills

`scripts/link` maintains skill links between this checkout and connected harness discovery directories. Connected destinations are recorded as normalized absolute paths in gitignored checkout-local state. Registry membership identifies intended destinations; ownership of destination contents is always derived from symlink targets.

## Interface

```text
scripts/link init [--no-discover] [--no-sync]

scripts/link dest discover [--add]
scripts/link dest add DIRECTORY [--no-sync]
scripts/link dest remove DIRECTORY
scripts/link dest status

scripts/link sync [--dry-run] [--clear]
scripts/link sync status

scripts/link status
scripts/link --help
```

An empty invocation prints help and exits unsuccessfully. Explicit help prints the same text and exits successfully.

## Initialization

`init` creates checkout-local state, discovers and records existing well-known destinations, and synchronizes every recorded destination.

- `--no-discover` skips well-known destination discovery.
- `--no-sync` skips link synchronization.
- Using both options creates empty state only.

Discovered destinations remain recorded if later synchronization fails, making the failure visible and recoverable through subsequent status and synchronization commands.

## Destinations

### Discovery

`dest discover` checks these well-known discovery directories:

```text
~/.codex/skills
~/.claude/skills
~/.agents/skills
```

Only directories that currently exist are reported. `--add` records and synchronizes newly discovered destinations. Discovery does not prune missing or manually added destinations.

### Addition and removal

`dest add DIRECTORY` records and synchronizes one destination. `--no-sync` records it without inspecting or changing its links. Adding an already recorded destination is idempotent and, without `--no-sync`, synchronizes it.

`dest remove DIRECTORY` clears every link owned by this checkout and then removes the destination from recorded state. If clearing fails, the destination remains recorded so removal can be retried. A missing destination can be removed from state successfully because it has no available links to clear.

Unrelated entries are never removed or overwritten.

### Destination status

`dest status` reports every recorded destination and whether its directory currently exists. Status is informational: missing destinations do not cause a failure exit when inspection itself succeeds.

## Synchronization

`sync` reconciles skill links across every recorded destination. `--dry-run` reports the plan without changing destination contents. `--clear` removes owned links while retaining every destination in recorded state. The options can be combined to preview clearing.

The linker recursively discovers regular files named `SKILL.md` beneath `skills/`. Each manifest's parent directory is a skill source, and that directory's basename is its installed name. Installed names must be unique even when their source directories have different parents.

For each discovered skill, synchronization classifies the corresponding top-level destination entry:

- An owned link already targeting the source is current and remains unchanged.
- An owned link targeting another path beneath this checkout's skill tree is removed and recreated.
- An absent entry is created as an absolute symlink to the source directory.
- An unrelated symlink, file, or directory at the desired name is a conflict.

Owned links whose names no longer correspond to discovered skills are stale and are removed. Applied synchronization removes stale or displaced links before creating desired links. Repeating synchronization against a current destination makes no changes.

Multi-destination operations discover and plan every destination before mutation. Every known conflict is reported, and no destination is modified if any conflict exists. An unexpected runtime failure can still interrupt application after earlier changes have succeeded.

## Ownership and clearing

Only immediate-child symlinks of a destination can be owned. A link is owned when its stored target, normalized lexically without following symlink components, lies strictly beneath this checkout's `skills/` directory. The target does not need to exist.

Clearing removes every owned link, including stale or broken links. It leaves files, directories, nested entries, and symlinks targeting other locations unchanged. A missing destination is a successful no-op and is not created.

## Link status

`sync status` inspects every recorded destination without modifying it. For each destination it reports whether the directory exists and classifies relevant names as:

- `Current`: an owned link targets the current source.
- `Missing`: a discovered skill has no destination entry.
- `Retarget`: an owned link exists but targets a different checkout skill path.
- `Stale`: an owned link has no corresponding discovered skill.
- `Conflict`: an unrelated entry occupies a desired name.

`status` combines destination status with synchronization status. Both status commands are informational and exit successfully after a successful inspection even when they report drift, missing destinations, or conflicts.

## Output and failures

Mutation and dry-run output uses stable labels:

```text
Added destination: PATH
Destination already added: PATH
Removed destination: PATH
Already linked: PATH
Would remove: PATH
Would link: PATH -> SOURCE
Remove: PATH
Link: PATH -> SOURCE
```

Explicit validation and conflict failures are written to standard error with a `link:` prefix and exit status 2. An underlying command can produce another nonzero status under Bash strict mode.

## State and implementation model

Destination state lives in `.state/link-destinations` beneath the checkout. `.state/` is gitignored. Registry updates use a temporary file followed by replacement.

The implementation separates destination state from link state:

1. Parse the command and resolve checkout paths.
2. Load or initialize the destination registry.
3. Discover source skills only for operations that require them.
4. Inventory and classify every selected destination.
5. Preflight all selected destinations before mutation.
6. Update registry state at the command-defined boundary.
7. Remove owned links before creating desired links.
8. Remove registered temporary files when the process exits.

The script requires Bash and uses null-delimited GNU-style `find`, `sort`, and `realpath` behavior. Keep the checkout at a stable path because installed links and the registry contain absolute paths.

## Verification

Changes to the linker must be exercised in an isolated checkout and temporary destinations. Cover initialization, discovery, destination state, synchronization, clearing, status, stale-link pruning, conflict preflight across multiple destinations, and preservation of unrelated entries. Record what has and has not been exercised; execution checks are evidence, not a permanent automated evaluation suite. Static analysis and evaluation design remain open questions in [`TODO.md`](../TODO.md).
