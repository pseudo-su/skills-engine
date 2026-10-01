# Linking authored skills

`scripts/link` maintains skill links between this checkout and connected harness discovery directories. Connected destinations are recorded in the gitignored `.state/link-destinations` file. The registry belongs to this checkout and stores normalized absolute paths.

## Interface

```text
scripts/link connect DIRECTORY [--no-sync]
scripts/link disconnect DIRECTORY [--no-sync]
scripts/link sync [DIRECTORY ...] [--dry-run]
scripts/link clear [DIRECTORY ...] [--dry-run]
scripts/link status [DIRECTORY ...]
```

`connect` records one destination and synchronizes it by default. Preflight conflicts prevent both synchronization and registration. `--no-sync` records the destination without inspecting or changing its links.

`disconnect` clears owned links and then forgets one connected destination. If clearing fails, the destination remains connected. `--no-sync` forgets it without inspecting or changing its links.

`sync`, `clear`, and `status` accept zero or more connected destinations. With no destination arguments, they operate on every connected destination. An explicitly supplied destination must already be connected.

`sync --dry-run` and `clear --dry-run` report planned changes without modifying destinations. Dry runs never change connection state.

## Synchronization behavior

The linker recursively discovers regular files named `SKILL.md` beneath `skills/`. Each manifest's parent directory is a skill source, and that directory's basename is its installed name. Installed names must be unique even when their source directories have different parents.

For each discovered skill, synchronization classifies the corresponding top-level destination entry:

- An owned link already targeting the source is current and remains unchanged.
- An owned link targeting another path beneath this checkout's skill tree is removed and recreated.
- An absent entry is created as an absolute symlink to the source directory.
- An unrelated symlink, file, or directory at the desired name is a conflict.

Owned links whose names no longer correspond to discovered skills are stale and are removed. Every conflict is reported before the destination or registry is changed. Applied synchronization removes stale or displaced links before creating links. Repeated synchronization against a current destination makes no changes.

## Clearing and ownership

Only immediate-child symlinks of a destination can be owned. A link is owned when its stored target, normalized lexically without following symlink components, lies strictly beneath this checkout's `skills/` directory. The target does not need to exist.

`clear` removes every owned link, including stale or broken links. It leaves files, directories, nested entries, and symlinks targeting other locations unchanged. A missing destination is a successful no-op and is not created. Clearing does not alter connection state.

## Status

`status` is read-only. For each selected destination it reports whether the directory is present and classifies relevant names as:

- `Current`: an owned link targets the current source.
- `Missing`: a discovered skill has no destination entry.
- `Retarget`: an owned link exists but targets a different checkout skill path.
- `Stale`: an owned link has no corresponding discovered skill.
- `Conflict`: an unrelated entry occupies a desired name.

## Output and failure behavior

Mutation and dry-run output uses stable labels:

```text
Connected: PATH
Already connected: PATH
Disconnected: PATH
Already linked: PATH
Would remove: PATH
Would link: PATH -> SOURCE
Remove: PATH
Link: PATH -> SOURCE
```

Explicit validation and conflict failures are written to standard error with a `link:` prefix and exit status 2. An underlying command can produce another nonzero status under Bash strict mode.

## Implementation model

The implementation separates connection state from link state:

1. Parse the command and resolve checkout paths.
2. Load the connected-destination registry.
3. Discover source skills only for operations that require them.
4. Inventory and classify each selected destination.
5. Preflight the complete destination plan before mutation.
6. Update registry state at the command-defined boundary.
7. Remove owned links before creating desired links.
8. Remove registered temporary files when the process exits.

The registry identifies destinations the checkout is expected to manage. It does not confer ownership over their contents; ownership is derived from each symlink target. Registry updates use a temporary file followed by replacement, and unrelated destination entries are never overwritten.

The script requires Bash and uses null-delimited GNU-style `find`, `sort`, and `realpath` behavior. Keep the checkout at a stable path because installed links and the registry contain absolute paths.

## Verification evidence

The command lifecycle has been exercised in an isolated checkout for:

- Connecting without synchronization
- Status of a missing destination
- Bare synchronization across connected destinations
- Status of current links
- Dry-run clearing
- Disconnecting with clearing
- Preservation of unrelated links
- Connecting with synchronization
- Disconnecting without clearing
- Conflict preflight without registration or partial installation

Earlier linker behavior was also exercised for recursive discovery, stale-link migration and pruning, lexical ownership, duplicate protection, and invalid destinations. These checks are execution evidence, not a permanent automated evaluation suite. Static analysis and evaluation design remain open questions in [`TODO.md`](../TODO.md).
