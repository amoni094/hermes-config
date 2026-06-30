#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile
from datetime import datetime, timezone

_HOME = pathlib.Path.home()
USAGE_PATH = _HOME / '.hermes' / 'skills' / '.usage.json'
SKILLS_ROOT = _HOME / '.hermes' / 'skills'
_REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
REPORT_PATH = _REPO_ROOT / 'docs' / 'skill-usage-migration-report.md'

replacement_map = {
    'audiocraft-audio-generation': 'audiocraft',
    'evaluating-llms-harness': 'lm-evaluation-harness',
    'segment-anything-model': 'segment-anything',
    'serving-llms-vllm': 'vllm',
    'last30days': 'last30days-customization',
    'github-auth': 'github-operations',
    'github-code-review': 'github-operations',
    'github-pr-followup-automation': 'github-operations',
    'github:github-pr-followup-automation': 'github-operations',
    'github-pr-workflow': 'github-operations',
    'github-repo-management': 'github-operations',
    'signal-oriented-research-briefing': 'research-briefing',
    'wallust-desktop-theme-integration': 'fedora-atomic-dotfiles-adaptation',
    'waybar-popup-menu-debugging': 'wayland-session-management',
    'wayland-session-troubleshooting': 'wayland-session-management',
    'hermes-security-preflight': 'security-hardening-balance-review',
    'hermes-stack-maintenance': 'hermes-runtime-maintenance',
    'hermes-live-research-setup': 'hermes-web-provider-configuration',
    'silverblue-desktop-ricing-adaptation': 'fedora-atomic-dotfiles-adaptation',
    'silverblue-update-automation': 'atomic-desktop-app-installation',
    'fedora-atomic-system-maintenance': 'hermes-runtime-maintenance',
    'fedora-atomic-system-updates': 'hermes-runtime-maintenance',
    'low-friction-repo-hardening': 'security-hardening-balance-review',
    'software-supply-chain-scanning': 'security-hardening-balance-review',
    'devops/atomic-desktop-app-installation': 'atomic-desktop-app-installation',
    'setup': 'ouroboros-setup-and-health-check',
    'cli-anything-hermes': 'hermes-agent',
}


def atomic_write(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, delete=False) as tmp:
        tmp.write(content)
        temp_path = pathlib.Path(tmp.name)
    temp_path.replace(path)



def merge_ts(a, b, prefer='max'):
    vals = [x for x in [a, b] if x]
    if not vals:
        return None
    return max(vals) if prefer == 'max' else min(vals)



def existing_skill_names() -> set[str]:
    names = set()
    for skill_file in SKILLS_ROOT.rglob('SKILL.md'):
        if '.archive' in skill_file.parts:
            continue
        names.add(skill_file.parent.name)
    return names



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Migrate stale Hermes skill usage keys to their active replacements.')
    parser.add_argument('--apply', action='store_true', help='Actually rewrite ~/.hermes/skills/.usage.json. Default is dry-run.')
    return parser



def main() -> None:
    args = build_parser().parse_args()

    usage = json.loads(USAGE_PATH.read_text())
    valid_targets = existing_skill_names()
    missing_targets = sorted({target for target in replacement_map.values() if target not in valid_targets})
    if missing_targets:
        raise SystemExit('replacement map points to missing active skills: ' + ', '.join(missing_targets))

    migrated = []
    for old, new in replacement_map.items():
        if old not in usage:
            continue
        old_entry = usage[old]
        if new not in usage:
            usage[new] = {
                'archived_at': None,
                'created_at': old_entry.get('created_at'),
                'created_by': old_entry.get('created_by'),
                'last_patched_at': old_entry.get('last_patched_at'),
                'last_used_at': old_entry.get('last_used_at'),
                'last_viewed_at': old_entry.get('last_viewed_at'),
                'patch_count': old_entry.get('patch_count', 0),
                'pinned': old_entry.get('pinned', False),
                'state': 'active',
                'use_count': old_entry.get('use_count', 0),
                'view_count': old_entry.get('view_count', 0),
            }
        else:
            cur = usage[new]
            cur['created_at'] = merge_ts(cur.get('created_at'), old_entry.get('created_at'), prefer='min')
            cur['created_by'] = cur.get('created_by') or old_entry.get('created_by')
            cur['last_patched_at'] = merge_ts(cur.get('last_patched_at'), old_entry.get('last_patched_at'), prefer='max')
            cur['last_used_at'] = merge_ts(cur.get('last_used_at'), old_entry.get('last_used_at'), prefer='max')
            cur['last_viewed_at'] = merge_ts(cur.get('last_viewed_at'), old_entry.get('last_viewed_at'), prefer='max')
            cur['patch_count'] = int(cur.get('patch_count', 0) or 0) + int(old_entry.get('patch_count', 0) or 0)
            cur['use_count'] = int(cur.get('use_count', 0) or 0) + int(old_entry.get('use_count', 0) or 0)
            cur['view_count'] = int(cur.get('view_count', 0) or 0) + int(old_entry.get('view_count', 0) or 0)
            cur['pinned'] = bool(cur.get('pinned', False) or old_entry.get('pinned', False))
            cur['state'] = 'active'
        usage.pop(old)
        migrated.append((old, new, old_entry.get('use_count', 0), old_entry.get('patch_count', 0)))

    lines = []
    lines.append('# Skill Usage Migration Report')
    lines.append('')
    lines.append(f'- Mode: {"apply" if args.apply else "dry-run"}')
    lines.append(f'- Migrated entries: {len(migrated)}')
    lines.append('')
    lines.append('## Migrations')
    lines.append('')
    for old, new, use_count, patch_count in migrated:
        lines.append(f'- `{old}` -> `{new}` | use_count={use_count} | patch_count={patch_count}')
    atomic_write(REPORT_PATH, '\n'.join(lines) + '\n')

    result = {
        'apply': args.apply,
        'migrated_count': len(migrated),
    }

    if args.apply:
        backup = SKILLS_ROOT / f'.usage.json.bak.{datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")}'
        atomic_write(backup, json.dumps(json.loads(USAGE_PATH.read_text()), indent=2) + '\n')
        atomic_write(USAGE_PATH, json.dumps(usage, indent=2, sort_keys=True) + '\n')
        result['backup'] = str(backup)

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
