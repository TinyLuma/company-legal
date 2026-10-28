#!/usr/bin/env python3
"""Check repository structure; --release adds conservative publication checks."""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--release', action='store_true', help='Require published status, dates and no known placeholders')
parser.add_argument('--app', help='Limit document checks to one registered App ID')
args = parser.parse_args()
errors = []
def fail(message):
    errors.append(message)
def valid_date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        return False
    try:
        datetime.date.fromisoformat(value)
        return True
    except ValueError:
        return False

try:
    manifest = json.loads((ROOT / 'apps.json').read_text(encoding='utf-8'))
except (OSError, ValueError) as exc:
    sys.exit(f'ERROR: Cannot read apps.json: {exc}')
if not isinstance(manifest, dict) or manifest.get('schema_version') != 1 or not isinstance(manifest.get('apps'), list):
    sys.exit('ERROR: Expected schema_version=1 and an apps array')
apps = manifest['apps']
ids = []
selected = 0
# Common markers from the supplied drafts; this is not a complete legal review.
placeholder = re.compile(r'【[^】\n]+】|\[(?:To be completed|Legal entity name|Legal entity and mailing address|Mailing address|Privacy email|Support email)\]|YOUR_GITHUB_OWNER|OWNER/REPO', re.I)
for app in apps:
    if not isinstance(app, dict):
        fail('Each apps entry must be an object')
        continue
    app_id = app.get('id', '')
    if not isinstance(app_id, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', app_id):
        fail(f'Invalid App ID: {app_id!r}')
        continue
    if app_id in ids:
        fail(f'Duplicate App ID: {app_id}')
    ids.append(app_id)
    if args.app and app_id != args.app:
        continue
    selected += 1
    if not app.get('name'):
        fail(f'{app_id}: Missing name')
    if app.get('status') not in ('draft', 'published'):
        fail(f'{app_id}: status must be draft or published')
    for key in ('effective_date', 'updated_at'):
        value = app.get(key)
        if value is not None and not valid_date(value):
            fail(f'{app_id}: Invalid {key}, use YYYY-MM-DD or null')
        if args.release and not valid_date(value):
            fail(f'{app_id}: Release requires confirmed {key}')
    if args.release and app.get('status') != 'published':
        fail(f'{app_id}: Release requires status=published')
    if not (ROOT / 'apps' / app_id / 'README.md').is_file():
        fail(f'{app_id}: Missing App README.md')
    docs = app.get('documents')
    if not isinstance(docs, dict) or not docs:
        fail(f'{app_id}: Missing documents mapping')
        continue
    registered = set()
    for kind, languages in docs.items():
        if not isinstance(kind, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', kind):
            fail(f'{app_id}: Invalid document kind {kind!r}')
            continue
        if not isinstance(languages, dict) or not languages:
            fail(f'{app_id}/{kind}: Missing language mapping')
            continue
        for lang, rel in languages.items():
            if not isinstance(lang, str) or not re.fullmatch(r'[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*', lang):
                fail(f'{app_id}/{kind}: Invalid language {lang!r}')
                continue
            expected = f'apps/{app_id}/{kind}/{lang}.md'
            if rel != expected:
                fail(f'{app_id}: Expected path {expected!r}, got {rel!r}')
                continue
            registered.add(rel)
            path = (ROOT / rel).resolve()
            if not path.is_relative_to(ROOT) or not path.is_file():
                fail(f'Missing or unsafe file: {rel}')
                continue
            text = path.read_text(encoding='utf-8')
            if not text.strip():
                fail(f'Empty file: {rel}')
            if args.release:
                match = placeholder.search(text)
                if match:
                    fail(f'{rel}: Unfilled placeholder {match.group(0)}')
                # Current policies use Chinese / English effective-date labels.
                if kind in ('privacy', 'terms') and lang in ('zh-CN', 'en'):
                    label = '生效日期' if lang == 'zh-CN' else 'Effective date'
                    if not re.search(re.escape(label) + r'[：:]\*\*\s*' + re.escape(str(app.get('effective_date'))), text):
                        fail(f'{rel}: Effective date must match manifest (YYYY-MM-DD)')
    for path in (ROOT / 'apps' / app_id).rglob('*.md'):
        rel = path.relative_to(ROOT).as_posix()
        if path.name != 'README.md' and rel not in registered:
            fail(f'Unregistered document: {rel}')
if not selected:
    fail(f'No matching App: {args.app or "(empty manifest)"}')
if not args.app:
    for path in (ROOT / 'apps').iterdir():
        if path.is_dir() and path.name not in ids:
            fail(f'Unregistered App directory: {path.name}')
if errors:
    print('\n'.join('ERROR: ' + e for e in errors))
    sys.exit(1)
print(f'OK: {selected} App(s); ' + ('release checks passed' if args.release else 'structure checks passed (not a release approval)'))
