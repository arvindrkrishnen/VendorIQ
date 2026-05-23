# Package Changelog

## Online-Ready Cross-Platform Edition
- Added online execution support for ChatGPT, Google Gemini AI Studio, and Claude Online.
- Added GitHub-repository execution instructions.
- Created separate `agents/` folder for independently maintainable agents.
- Created separate `playbooks/` folder for independently maintainable playbooks.
- Moved guardrail controls to `guardrails/` folder.
- Added provider-specific online prompts in `prompts/online/`.
- Preserved VS Code / local CLI execution for OpenAI, Anthropic Claude, Google Gemini, Perplexity, and offline scaffold mode.
- Preserved single-output behavior: one final Markdown report.
