#!/usr/bin/env python3
"""Check the collection's deliberately simple skill format using stdlib only."""
import json
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
errors = []
names = set()
paths = sorted((root / 'skills').glob('*/SKILL.md'))
for path in paths:
    text = path.read_text()
    parts = text.split('---', 2)
    if len(parts) != 3 or parts[0].strip():
        errors.append(f'{path.relative_to(root)}: missing frontmatter')
        continue
    fields = {}
    for line in parts[1].strip().splitlines():
        key, sep, value = line.partition(':')
        if not sep or key in fields:
            errors.append(f'{path.relative_to(root)}: malformed/duplicate field')
        fields[key] = value.strip()
    name = fields.get('name', '')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or name != path.parent.name:
        errors.append(f'{path.relative_to(root)}: invalid name')
    if name in names:
        errors.append(f'{path.relative_to(root)}: duplicate name')
    names.add(name)
    if set(fields) != {'name', 'description'} or not fields.get('description'):
        errors.append(f'{path.relative_to(root)}: expected name and description')
    if 'TODO' in text or not parts[2].strip():
        errors.append(f'{path.relative_to(root)}: incomplete body')
    if not (path.parent / 'agents' / 'openai.yaml').is_file():
        errors.append(f'{path.relative_to(root)}: missing UI metadata')
for path in root.rglob('*.md'):
    if '.git' in path.parts:
        continue
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if '://' in target or target.startswith('#'):
            continue
        if not (path.parent / target.split('#', 1)[0]).exists():
            errors.append(f'{path.relative_to(root)}: broken reference {target}')
manifest = json.loads((root / 'upstreams.json').read_text())
if manifest.get('schema_version') != 1 or not isinstance(manifest.get('imports'), list):
    errors.append('Invalid upstream manifest')
if not paths:
    errors.append('No skills found')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f'Checked {len(paths)} skills, Markdown references, and upstream manifest')
