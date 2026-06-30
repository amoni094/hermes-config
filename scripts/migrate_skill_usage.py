#!/usr/bin/env python3
import json
import pathlib
from datetime import datetime, timezone

USAGE_PATH = pathlib.Path('/var/home/rainbow/.hermes/skills/.usage.json')
BACKUP_DIR = pathlib.Path('/var/home/rainbow/.hermes/skills')
REPORT_PATH = pathlib.Path('/var/home/rainbow/hermes-config/docs/skill-usage-migration-report.md')

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

def merge_ts(a, b, prefer='max'):
    vals = [x for x in [a,b] if x]
    if not vals:
        return None
    return max(vals) if prefer == 'max' else min(vals)

usage = json.loads(USAGE_PATH.read_text())
backup = BACKUP_DIR / f'.usage.json.bak.{datetime.now().strftime("%Y%m%d-%H%M%S")}'
backup.write_text(json.dumps(usage, indent=2))

migrated = []
skipped = []
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
    migrated.append((old, new, old_entry.get('use_count',0), old_entry.get('patch_count',0)))

USAGE_PATH.write_text(json.dumps(usage, indent=2, sort_keys=True))

lines = []
lines.append('# Skill Usage Migration Report')
lines.append('')
lines.append(f'- Backup: `{backup}`')
lines.append(f'- Migrated entries: {len(migrated)}')
lines.append('')
lines.append('## Migrations')
lines.append('')
for old, new, use_count, patch_count in migrated:
    lines.append(f'- `{old}` -> `{new}` | use_count={use_count} | patch_count={patch_count}')
REPORT_PATH.write_text('\n'.join(lines) + '\n')
print(json.dumps({'backup': str(backup), 'migrated_count': len(migrated)}, indent=2))
