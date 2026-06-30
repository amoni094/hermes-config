#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import py_compile
import subprocess
from typing import Iterable

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / 'config.sanitized.yaml'
CRON_PATH = REPO_ROOT / 'cron.snapshot.json'
GITIGNORE_PATH = REPO_ROOT / '.gitignore'
README_PATH = REPO_ROOT / 'README.md'
CURRENT_WORKFLOW_PATH = REPO_ROOT / 'docs/current-workflow.md'

REQUIRED_GITIGNORE_ENTRIES = {
    '.env',
    'auth.json',
    'state.db',
    'state.db-*',
    'logs/',
    'sessions/',
    'processes.json',
    'channel_directory.json',
    'gateway_state.json',
    '__pycache__/',
    '*.py[cod]',
}

FORBIDDEN_CONFIG_KEY_PATTERNS = (
    'api_key',
    'access_token',
    'refresh_token',
    'bot_token',
    'bearer_token',
    'client_secret',
    'secret_key',
    'password',
    'authorization',
    'cookie',
)

SAFE_CONFIG_KEY_EXACT_ALLOWLIST = {
    'telegram_allowed_users',
    'discord_allowed_users',
    'slack_allowed_users',
    'mattermost_allowed_users',
    'matrix_allowed_users',
    'whatsapp_allowed_users',
    'telegram_home_channel',
    'telegram_home_channel_name',
    'whatsapp_enabled',
    'access_token_env',
}

REDACTED_MARKERS = {'<redacted>', 'redacted', ''}


def fail(message: str) -> None:
    raise SystemExit(message)


def atomic_read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding='utf-8')


def iter_python_files() -> Iterable[pathlib.Path]:
    for path in sorted((REPO_ROOT / 'scripts').glob('*.py')):
        if path.name.startswith('.'):
            continue
        yield path


def validate_python_compiles() -> None:
    for path in iter_python_files():
        py_compile.compile(str(path), doraise=True)


def validate_gitignore() -> None:
    lines = {
        line.strip()
        for line in atomic_read_text(GITIGNORE_PATH).splitlines()
        if line.strip() and not line.lstrip().startswith('#')
    }
    missing = sorted(REQUIRED_GITIGNORE_ENTRIES - lines)
    if missing:
        fail(f'.gitignore missing required exclusions: {", ".join(missing)}')



def walk_mapping(node, path='root'):
    if isinstance(node, dict):
        for key, value in node.items():
            current = f'{path}.{key}'
            yield current, key, value
            yield from walk_mapping(value, current)
    elif isinstance(node, list):
        for idx, value in enumerate(node):
            yield from walk_mapping(value, f'{path}[{idx}]')



def key_looks_sensitive(key: str) -> bool:
    normalized = key.lower()
    if normalized in SAFE_CONFIG_KEY_EXACT_ALLOWLIST:
        return False
    return any(pattern in normalized for pattern in FORBIDDEN_CONFIG_KEY_PATTERNS)



def validate_sanitized_config() -> None:
    config = yaml.safe_load(atomic_read_text(CONFIG_PATH))
    if not isinstance(config, dict):
        fail('config.sanitized.yaml did not parse into a mapping')

    offenders: list[str] = []
    for dotted_path, key, value in walk_mapping(config):
        if key_looks_sensitive(str(key)) and value not in (None, '', [], {}):
            offenders.append(dotted_path)
    if offenders:
        fail('config.sanitized.yaml still contains non-empty sensitive-looking keys: ' + ', '.join(offenders))



def validate_cron_snapshot() -> None:
    payload = json.loads(atomic_read_text(CRON_PATH))
    jobs = payload.get('jobs', [])
    if not isinstance(jobs, list):
        fail('cron.snapshot.json missing jobs list')

    for job in jobs:
        origin = job.get('origin')
        if origin is None:
            continue
        if not isinstance(origin, dict):
            fail(f"job {job.get('name', '<unknown>')} origin is not an object or null")
        for field in ('chat_id', 'chat_name', 'thread_id'):
            value = origin.get(field)
            if value is None:
                continue
            text = str(value).strip().lower()
            if text not in REDACTED_MARKERS:
                fail(
                    f"job {job.get('name', '<unknown>')} has unredacted origin field {field}={value!r}"
                )



def validate_documentation_markers() -> None:
    readme = atomic_read_text(README_PATH)
    if 'sanitized copy of the active Hermes config' not in readme:
        fail('README.md no longer states that the config export is sanitized')

    workflow = atomic_read_text(CURRENT_WORKFLOW_PATH)
    expected_phrases = [
        '~/.hermes/.env',
        '~/.hermes/auth.json',
        'raw gateway/session/chat histories',
    ]
    missing = [phrase for phrase in expected_phrases if phrase not in workflow]
    if missing:
        fail('docs/current-workflow.md missing export-exclusion markers: ' + ', '.join(missing))



def validate_no_tracked_pycache() -> None:
    tracked_pycache = []
    for path in REPO_ROOT.rglob('*'):
        if '.git' in path.parts:
            continue
        if '__pycache__' not in path.parts and path.suffix not in {'.pyc', '.pyo'}:
            continue
        rel = str(path.relative_to(REPO_ROOT))
        proc = subprocess.run(
            ['git', 'ls-files', '--error-unmatch', rel],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0:
            tracked_pycache.append(rel)
    if tracked_pycache:
        fail('Remove tracked Python cache artifacts from the repo tree: ' + ', '.join(sorted(tracked_pycache)))



def main() -> None:
    validate_python_compiles()
    validate_gitignore()
    validate_sanitized_config()
    validate_cron_snapshot()
    validate_documentation_markers()
    validate_no_tracked_pycache()
    print('repo validation passed')


if __name__ == '__main__':
    main()
