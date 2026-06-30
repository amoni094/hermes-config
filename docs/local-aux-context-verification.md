# Local Auxiliary Context Verification

Generated: 2026-06-30

## Purpose

Verify whether the configured local auxiliary-model context lengths in Hermes match the actual Ollama runtime metadata.

## Why this matters

The earlier adversarial pass flagged a mismatch risk between the main 128k context and the local helper path used for auxiliary roles such as:
- `title_generation`
- `triage_specifier`
- `profile_describer`
- `curator`

A bad configured context length can make helper failures look random instead of obviously configuration-related.

## Live verification

Verified with direct runtime inspection against the local Ollama API:

```bash
python3 - <<'PY'
import json, urllib.request
for model in ['llama3.2:3b','qwen3:8b']:
    req=urllib.request.Request('http://localhost:11434/api/show', data=json.dumps({'name':model}).encode(), headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        obj=json.load(r)
    mi=obj.get('model_info', {})
    vals={k:v for k,v in mi.items() if 'context_length' in k or k=='general.context_length'}
    print(model, vals)
PY
```

Observed runtime values:
- `llama3.2:3b` -> `131072`
- `qwen3:8b` -> `40960`

## Previous config state

The Hermes config had:
- `qwen3:8b.context_length: 64000`
- `llama3.2:3b.context_length: 64000`

Interpretation:
- `qwen3:8b` was overstated by 23040 tokens relative to the live runtime.
- `llama3.2:3b` was conservative, not overstated.

## Remediation applied

I updated the live Hermes config and the repo snapshot so that:
- `qwen3:8b.context_length: 40960`

I left `llama3.2:3b` unchanged at `64000` because that value is lower than the verified runtime capacity and is therefore conservative rather than dangerous.

## Operational conclusion

The highest-confidence optimization here is not to make the local helper path larger on paper; it is to make the configured value truthful.

This reduces the chance that Hermes will assume a larger prompt budget for `qwen3:8b` than Ollama is actually serving.

## Follow-up recommendation

If helper workloads start failing from prompt pressure again, prefer this order:
1. keep helper prompts narrower
2. move the heaviest helper role to `provider: main` or another backed provider
3. only then revisit local-runtime model/context changes
