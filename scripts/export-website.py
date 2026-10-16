#!/usr/bin/env python3
"""Publish explicitly selected canonical sources into website/; --check detects drift."""
from __future__ import annotations

import argparse
import json
import posixpath
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'(?P<open>!?\[[^\]\n]*\]\()(?P<target><[^>\n]*>|[^)\n]*)(?P<close>\))')
ATTRIBUTE = re.compile(r'''(?P<open>\b(?:href|src)=["'])(?P<target>[^"']*)(?P<close>["'])''')


def public_markdown(root: Path, manifest: dict, source: str, content: str) -> str:
    """Keep canonical links usable when a project document is exported to the site."""
    site_root = manifest['site_root']
    exported = {item['source']: item['destination'] for item in manifest['exports']}

    def replace(match: re.Match) -> str:
        target = match['target'].strip()
        if not target or target.startswith(('#', '/', '{')):
            return match[0]
        angle = target.startswith('<') and target.endswith('>')
        raw = target[1:-1] if angle else target
        url = urlsplit(raw)
        if url.scheme or url.netloc:
            return match[0]
        path = posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(url.path)))
        if path == '..' or path.startswith('../'):
            raise ValueError(f'{source}: link leaves repository: {target}')
        destination = exported.get(path, path)
        if destination.startswith(site_root + '/'):
            address = '/' + destination[len(site_root) + 1:]
            if address.endswith('/README.md'):
                address = address[:-len('README.md')]
            elif address.endswith('.md'):
                address = address[:-3]
            address = quote(address, safe='/')
        else:
            local = root / path
            if not local.exists():
                raise ValueError(f'{source}: canonical link target missing: {target}')
            address = manifest['repository_url'] + '/' + quote(path, safe='/')
            if local.is_dir():
                address = address.replace('/blob/main/', '/tree/main/')
        address = urlunsplit(('', '', address, url.query, url.fragment))
        if angle:
            address = '<' + address + '>'
        return match['open'] + address + match['close']

    # Code examples are source instructions, not Markdown links to rewrite.
    parts = re.split(r'(^```[^\n]*\n.*?^```\s*$)', content, flags=re.M | re.S)
    for i in range(0, len(parts), 2):
        parts[i] = ATTRIBUTE.sub(replace, LINK.sub(replace, parts[i]))
    content = ''.join(parts)
    notice = f'<!-- Generated from {source}; edit that canonical source and run python3 scripts/export-website.py. -->\n\n'
    if content.startswith('---\n'):
        end = content.find('\n---\n', 4)
        if end != -1:
            return content[:end + 5] + '\n' + notice + content[end + 5:].lstrip('\n')
    return notice + content


def export(root: Path, check: bool = False) -> list[str]:
    manifest = json.loads((root / 'scripts/website-content.json').read_text())
    changed = []
    for item in manifest['exports']:
        source = root / item['source']
        destination = root / item['destination']
        if not destination.resolve().is_relative_to((root / manifest['site_root']).resolve()):
            raise ValueError(f'Export destination leaves website: {item["destination"]}')
        content = source.read_bytes()
        if item['format'] == 'markdown':
            content = public_markdown(root, manifest, item['source'], content.decode()).encode()
        if destination.exists() and destination.read_bytes() == content:
            continue
        changed.append(item['destination'])
        if not check:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Report stale exports without writing')
    parser.add_argument('--root', type=Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        changed = export(args.root.resolve(), args.check)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'{exc}\n')
    if changed:
        print(('Stale exports: ' if args.check else 'Exported: ') + ', '.join(changed))
    else:
        print('Website exports are current.')
    return int(args.check and bool(changed))


if __name__ == '__main__':
    raise SystemExit(main())
