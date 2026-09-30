#!/usr/bin/env python3
"""Link authored skills to an explicit harness discovery directory."""
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--remove', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    destination = args.destination.expanduser().resolve()
    sources = sorted(p.parent.resolve() for p in (root / 'skills').glob('*/SKILL.md'))
    if not sources:
        parser.error('No authored skills found')
    operations = []
    conflicts = []
    for source in sources:
        link = destination / source.name
        present = link.exists() or link.is_symlink()
        owned = link.is_symlink() and link.resolve() == source
        if args.remove:
            if owned:
                operations.append(('remove', link, source))
        elif owned:
            print(f'Already linked: {link}')
        elif present:
            conflicts.append(str(link))
        else:
            operations.append(('link', link, source))
    # Preflight every entry before any mutation.
    if conflicts:
        parser.error('Refusing to overwrite occupied paths: ' + ', '.join(conflicts))
    if not args.dry_run and not args.remove and operations:
        destination.mkdir(parents=True, exist_ok=True)
    for action, link, source in operations:
        print(f'{"Would " if args.dry_run else ""}{action}: {link} -> {source}')
        if args.dry_run:
            continue
        if action == 'remove':
            link.unlink()
        else:
            link.symlink_to(source, target_is_directory=True)


if __name__ == '__main__':
    main()
