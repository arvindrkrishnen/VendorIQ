# Package Changelog

## Universal Multi-LLM Single-Report Edition
- Produces only one persistent output: `artifacts/exhaustive_final_report.md`.
- Removed requirements to emit separate progress, evidence, Pugh Matrix, SEC, government contracts, or quality JSON files.
- Added provider adapters for OpenAI, Anthropic Claude, Google Gemini, Perplexity, and offline scaffold mode.
- Added `.env.example` with supported key variables.
- Updated README with provider configuration and VS Code task execution.
- Updated guardrails to enforce single-output compliance and authenticity validation.
- Updated agents and playbooks to preserve section-level multi-agent orchestration.
