#!/usr/bin/env python3
import json
import pathlib
import subprocess
from collections import Counter

ROOT = pathlib.Path('/var/home/rainbow/.hermes/skills')
USAGE_PATH = ROOT / '.usage.json'
OUT_JSON = pathlib.Path('/var/home/rainbow/hermes-config/docs/skill-inventory-authoritative.json')
OUT_MD = pathlib.Path('/var/home/rainbow/hermes-config/docs/skill-inventory-authoritative.md')

usage = json.loads(USAGE_PATH.read_text()) if USAGE_PATH.exists() else {}

alias_map = {
    'audiocraft-audio-generation': 'audiocraft',
    'evaluating-llms-harness': 'lm-evaluation-harness',
    'segment-anything-model': 'segment-anything',
    'serving-llms-vllm': 'vllm',
    'last30days': 'last30days-customization',
}

replacement_map = {
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
}

def resolve_replacement(key):
    if key in alias_map:
        return alias_map[key], 'alias'
    if key in replacement_map:
        return replacement_map[key], 'replacement'
    return None, 'unknown_or_historical'

def parse_skill_table(source):
    env = dict(**__import__('os').environ)
    env['COLUMNS'] = '240'
    out = subprocess.check_output(['hermes', 'skills', 'list', '--source', source], text=True, env=env)
    rows = {}
    summary_line = None
    for line in out.splitlines():
        if line.startswith('│') and 'Source' not in line and 'Name' not in line:
            parts = [p.strip() for p in line.strip('│').split('│')]
            if len(parts) >= 5:
                name, category, src, trust, status = parts[:5]
                rows[name] = {'source': src, 'trust': trust, 'status': status, 'category_from_cli': category}
        if 'builtin' in line or 'local' in line:
            summary_line = line
    return rows, summary_line

builtin_rows, builtin_summary = parse_skill_table('builtin')
local_rows, local_summary = parse_skill_table('local')
cli_rows = {**builtin_rows, **local_rows}

records = []
for p in ROOT.rglob('SKILL.md'):
    archived = '.archive' in p.parts
    skill_dir = p.parent
    name = skill_dir.name
    rel = skill_dir.relative_to(ROOT)
    category = rel.parts[0] if len(rel.parts) > 1 else '(root)'
    text = p.read_text(errors='replace')
    desc = ''
    frontmatter_name = None
    for line in text.splitlines()[:30]:
        if line.startswith('name: '):
            frontmatter_name = line.split(':',1)[1].strip().strip('"')
        if line.startswith('description: '):
            desc = line.split(':',1)[1].strip().strip('"')
    usage_key = None
    if name in usage:
        usage_key = name
    else:
        for k,v in alias_map.items():
            if v == name and k in usage:
                usage_key = k
                break
    cli = cli_rows.get(name, {})
    source = cli.get('source', 'archived_or_unresolved' if archived else 'local')
    status = cli.get('status', 'archived' if archived else 'unknown')
    records.append({
        'name': name,
        'frontmatter_name': frontmatter_name,
        'path': str(skill_dir),
        'relative_path': str(rel),
        'category': category,
        'archived': archived,
        'source': source,
        'status': status,
        'usage_key': usage_key,
        'resolved_status': 'active' if not archived else 'archived',
        'description': desc,
        'size_bytes': p.stat().st_size,
        'use_count': usage.get(usage_key, {}).get('use_count') if usage_key else None,
        'patch_count': usage.get(usage_key, {}).get('patch_count') if usage_key else None,
        'last_used_at': usage.get(usage_key, {}).get('last_used_at') if usage_key else None,
    })

active_names = {r['name'] for r in records if not r['archived']}
stale_usage = []
for key, meta in usage.items():
    if key in active_names:
        continue
    mapped, resolved = resolve_replacement(key)
    stale_usage.append({'usage_key': key, 'resolved_status': resolved, 'replacement_skill': mapped, **meta})

summary = {
    'total_records': len(records),
    'active_records': sum(not r['archived'] for r in records),
    'archived_records': sum(r['archived'] for r in records),
    'builtin_records': sum(r['source']=='builtin' and not r['archived'] for r in records),
    'local_records': sum(r['source']=='local' and not r['archived'] for r in records),
    'enabled_records': sum(r['status']=='enabled' and not r['archived'] for r in records),
    'disabled_records': sum(r['status']=='disabled' and not r['archived'] for r in records),
    'stale_usage_count': len(stale_usage),
    'categories': dict(sorted(Counter(r['category'] for r in records if not r['archived']).items())),
    'builtin_cli_summary': builtin_summary,
    'local_cli_summary': local_summary,
}

payload = {'summary': summary, 'records': records, 'stale_usage': stale_usage, 'alias_map': alias_map, 'replacement_map': replacement_map}
OUT_JSON.write_text(json.dumps(payload, indent=2))

lines = []
lines.append('# Authoritative Skill Inventory')
lines.append('')
lines.append('Generated from live local skill files, `hermes skills list --source builtin/local`, and `.usage.json` reconciliation.')
lines.append('')
lines.append('## Summary')
lines.append('')
for k,v in summary.items():
    if k in {'categories','builtin_cli_summary','local_cli_summary'}:
        continue
    lines.append(f'- {k}: {v}')
lines.append(f"- builtin_cli_summary: {summary['builtin_cli_summary']}")
lines.append(f"- local_cli_summary: {summary['local_cli_summary']}")
lines.append('')
lines.append('## Active categories')
lines.append('')
for cat, count in summary['categories'].items():
    lines.append(f'- {cat}: {count}')
lines.append('')
lines.append('## Highest-use active skills (top 20 by use_count)')
lines.append('')
active_sorted = sorted([r for r in records if not r['archived']], key=lambda r: (r['use_count'] or 0), reverse=True)
for r in active_sorted[:20]:
    lines.append(f"- {r['relative_path']} | source={r['source']} | status={r['status']} | use_count={r['use_count'] or 0} | size_bytes={r['size_bytes']}")
lines.append('')
lines.append('## Oversized active skills (>= 20000 bytes)')
lines.append('')
for r in sorted([r for r in records if not r['archived'] and r['size_bytes'] >= 20000], key=lambda r:r['size_bytes'], reverse=True):
    lines.append(f"- {r['relative_path']} | source={r['source']} | status={r['status']} | size_bytes={r['size_bytes']} | use_count={r['use_count'] or 0}")
lines.append('')
lines.append('## Stale usage keys')
lines.append('')
for s in stale_usage[:50]:
    lines.append(f"- {s['usage_key']} | status={s['resolved_status']} | replacement={s['replacement_skill']} | use_count={s.get('use_count',0)}")
OUT_MD.write_text('\n'.join(lines) + '\n')
print(json.dumps(summary, indent=2))
