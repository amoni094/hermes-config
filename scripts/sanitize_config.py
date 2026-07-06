#!/usr/bin/env python3
"""sanitize_config.py — produce config.sanitized.yaml from the live Hermes config.

Reads the live config (default ~/.hermes/config.yaml) and writes a sanitized
copy into this repo with every secret-looking value blanked. The blanking key
set mirrors validate_repo.py's FORBIDDEN_CONFIG_KEY_PATTERNS so a freshly
generated export always passes validation.

Sanitization rules:
  - Any mapping key whose lowercased name contains a forbidden pattern
    (api_key, access_token, refresh_token, bot_token, bearer_token,
    client_secret, secret_key, password, authorization, cookie, secret,
    token, passwd) has its value replaced with '' — unless the exact key is
    on the allowlist (e.g. access_token_env, which names an env var, not a
    secret).
  - base_url values that embed userinfo/auth (https://user:pass@host) are
    blanked; plain provider base_urls are preserved (they are not secret).
  - Chat/thread identifiers in gateway/platform blocks are left to the cron
    snapshot tooling; this script only touches the config document.

Usage:
  python3 scripts/sanitize_config.py            # uses ~/.hermes/config.yaml
  python3 scripts/sanitize_config.py --source /path/to/config.yaml
"""
from __future__ import annotations

import argparse
import pathlib
import re

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = pathlib.Path.home() / ".hermes" / "config.yaml"
OUT_PATH = REPO_ROOT / "config.sanitized.yaml"

FORBIDDEN_KEY_PATTERNS = (
    "api_key", "access_token", "refresh_token", "bot_token", "bearer_token",
    "client_secret", "secret_key", "password", "authorization", "cookie",
    "secret", "token", "passwd",
)

# Exact keys that merely NAME a secret source / toggle redaction and are safe to keep.
ALLOWLIST = {
    "access_token_env",  # names an env var, not a secret
    "redact_secrets",    # boolean policy flag
    "redact_pii",        # boolean policy flag
    "max_tokens",        # numeric model param, not a secret
    "max_output_tokens", # numeric model param, not a secret (contains "token" substring)
    "show_token_analytics",  # boolean display flag
    "session_ttl_seconds",   # numeric TTL, not a secret
}

# Mapping keys whose VALUE is a nested config block (not a scalar secret) and
# should be recursed into rather than blanked wholesale.
STRUCTURAL_KEYS = {
    "secrets",  # top-level bitwarden config container (recurse; leaf secrets still blanked)
}

AUTH_IN_URL = re.compile(r"^[a-z]+://[^/@\s]+:[^/@\s]+@")


def key_is_sensitive(key: str) -> bool:
    norm = key.lower()
    if norm in ALLOWLIST:
        return False
    return any(pat in norm for pat in FORBIDDEN_KEY_PATTERNS)


def sanitize(node):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if isinstance(k, str) and k.lower() in STRUCTURAL_KEYS:
                out[k] = sanitize(v)
            elif isinstance(k, str) and key_is_sensitive(k):
                out[k] = ""
            elif isinstance(k, str) and k.lower() in ("base_url", "callback_url", "public_url", "server_url") \
                    and isinstance(v, str) and AUTH_IN_URL.match(v):
                out[k] = ""
            else:
                out[k] = sanitize(v)
        return out
    if isinstance(node, list):
        return [sanitize(v) for v in node]
    return node


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=pathlib.Path, default=DEFAULT_SOURCE)
    ap.add_argument("--out", type=pathlib.Path, default=OUT_PATH)
    args = ap.parse_args()

    if not args.source.exists():
        raise SystemExit(f"source config not found: {args.source}")

    raw = yaml.safe_load(args.source.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise SystemExit("source config did not parse into a mapping")

    cleaned = sanitize(raw)
    args.out.write_text(
        yaml.safe_dump(cleaned, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )
    print(f"wrote sanitized config -> {args.out}")


if __name__ == "__main__":
    main()
