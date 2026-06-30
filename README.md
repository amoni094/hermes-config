# hermes-config

Configuration, routing workflow, and documentation for a Hermes agent setup.

## Contents

| File/Dir | Description |
|---|---|
| `config.sanitized.yaml` | Full Hermes config with all secrets redacted — shows structure, providers, auxiliary routing |
| `env.template` | Template for `~/.hermes/.env` with all supported keys documented |
| `docs/routing-and-workflow.md` | Capability-based model routing skill — which model to use for what, with quota tables and cron patterns |
| `docs/` | Historical workflow docs, skill inventories, adversarial critiques |
| `scripts/` | Utility scripts for skill inventory and validation |

## Free tier providers configured

All providers below are permanent free tiers (no credit card expiry):

| Provider | RPD | Context | Data training | Strength |
|---|---|---|---|---|
| Groq | 1,000 | 131K | No | Fastest inference (~320 tok/s) |
| Cerebras | 14,400 | **8K free** | No | Highest volume |
| SambaNova | 20/model | 32K–196K | No | Best quality per request |
| Mistral | ~1B tok/mo | 256K–262K | Yes (opt-in) | Huge volume, code specialist |
| Gemini | 1,500 | 1M | Yes (outside EU) | Largest context |
| GitHub Models | 150–1,000 | 128–131K | No | Free GPT-4o + Llama 405B |
| Local Ollama | unlimited | hardware | No | Offline fallback |

## Fallback chain

When Anthropic is unavailable, Hermes cascades automatically:
1. `anthropic/claude-sonnet-4-6` (primary)
2. `gemini/gemini-2.5-flash` (free, 15 RPM)
3. `custom:cerebras/gpt-oss-120b` (free, high RPD, 8K ctx)
4. `custom:local/qwen3:8b` (offline, always available)

## Auxiliary task routing

Internal Hermes ops routed to free tier to reduce paid API usage:

| Task | Provider | Model |
|---|---|---|
| Context compression | Cerebras | gpt-oss-120b |
| Summarization | Cerebras | gpt-oss-120b |
| Title generation | Gemini | gemini-2.5-flash |
| Skills hub | Gemini | gemini-2.5-flash |

## Key routing decisions

See `docs/routing-and-workflow.md` for the full capability matrix. Quick reference:

- **Context >128K** → Gemini 2.5 Flash (1M ctx)
- **Speed-critical** → Groq llama-3.3-70b (~320 tok/s)
- **Max volume** → Cerebras (14,400 RPD, keep prompts <8K)
- **Code tasks** → Mistral Codestral (256K ctx, 1B tok/mo)
- **Best quality free** → SambaNova DeepSeek-V3.2 (20 RPD)
- **Free GPT-4o** → GitHub Models (150–1000 RPD)
- **Agentic tool-use** → Groq compound/compound-mini
- **Free STT** → Groq whisper-large-v3

## Notes

- Groq requires split-tunnel routing when behind ProtonVPN (datacenter IP block).
  A systemd user service (`groq-split-tunnel.service`) handles this automatically.
- SambaNova DeepSeek-V3.2 context is 32K (not 128K) — use V3.1 for longer context.
- Cerebras 8K context cap on free tier is a hard limit.
- Mistral Experiment plan requires data training opt-in — avoid sensitive prompts.
