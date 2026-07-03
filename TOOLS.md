# TOOLS.md - Local Hermes Setup Notes

## Runtime

- terminal: local backend; Docker is optional on this host.
- Python: 3.14.6 (system python3); uv/uvx available at ~/.hermes/bin/
- Hermes config: ~/.hermes/config.yaml; secrets: ~/.hermes/.env
- Persona: ~/.hermes/SOUL.md

## Memory stack (4 layers)

- Hermes durable memory: ~/.hermes/memories/MEMORY.md (agent notes) + USER.md (user profile)
- Hindsight: local_embedded backend via Ollama at http://localhost:11434; data at ~/.hindsight/
- Graphiti MCP: http://127.0.0.1:8765/mcp/ — group_id=hermes, reasoning group=hermes-reasoning
- QMD: flowstate-qmd integration; accessed via mcp_qmd_* tools
- Session search: always-on sqlite session DB
- MemPalace: present but DISABLED in config.yaml

See docs/memory-topology.md for the full routing guide.

## Local services

- Ollama: http://localhost:11434; models: qwen3:8b, llama3.2:3b
- Firecrawl: http://127.0.0.1:3002 (self-hosted)
- SearXNG: configured URL (web search backend)
- Graphiti: http://127.0.0.1:8765/mcp/ (Neo4j knowledge graph MCP)
- World Monitor: started via worldmonitor-start.sh (news signals)

## External gateways

- Telegram: active gateway (primary mobile notifications)
- WhatsApp: bridge present but DORMANT (npm vulns; do not reconnect without explicit request)

## OS / host

- Fedora 44 Silverblue (immutable rpm-ostree)
- Kernel 7.0.14-201.fc44.x86_64
- Home: /var/home/rainbow
- Toolbox available for mutable container work
