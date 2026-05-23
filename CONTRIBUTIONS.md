# Contributions Guide

Thank you for contributing to the Universal Vendor Analysis skill. This guide explains how to propose changes, improve agents and playbooks, add provider support, strengthen guardrails, and maintain the single-output report contract.

## Contribution Goals

The project welcomes contributions that improve:

- evidence-backed vendor analysis quality;
- multi-agent orchestration;
- provider support for OpenAI, Anthropic Claude, Google Gemini, and Perplexity;
- SEC filing extraction;
- customer and supplier discovery;
- government-contract research;
- products and services cataloging;
- future-actions analysis;
- authenticity evaluation;
- final Markdown report quality;
- token efficiency and runtime reliability.

## Repository Principles

1. **One persistent output**  
   The package must produce only one user-facing artifact: `artifacts/exhaustive_final_report.md`.

2. **Evidence first**  
   Factual claims must have source URLs. Unsupported information must be marked as `Not found in public sources`.

3. **Sub-agent ownership**  
   Each major report section should map to a clear sub-agent or playbook.

4. **Provider portability**  
   Do not hard-code a single LLM provider. New logic should work with OpenAI, Anthropic, Gemini, Perplexity, or offline scaffold mode where practical.

5. **No secrets in source control**  
   Never commit `.env`, API keys, browser session tokens, local credentials, or private customer data.

6. **Clean state matters**  
   Temporary runtime data must be cleaned up before completion. The final report should embed quality, evidence, and Pugh Matrix outputs instead of saving separate artifacts.

## Ways to Contribute

### Improve a sub-agent

Edit `agents.md` to clarify role, task scope, evidence requirements, and passing criteria.

Good sub-agent improvements include:

- clearer task boundaries;
- better evidence hierarchy;
- stronger unsupported-claim handling;
- better report-ready Markdown output format;
- more specific criteria for customers, suppliers, SEC filings, or government contracts.

### Improve a playbook

Edit `playbooks.md` to make execution steps more reliable.

Good playbook improvements include:

- better search patterns;
- improved source priority rules;
- clearer section-level output templates;
- explicit retry paths when sources are missing;
- better guidance for public vs. private vendors.

### Improve guardrails

Edit `guardrails.md` to strengthen validation.

Useful guardrail improvements include:

- authenticity scoring logic;
- source coverage thresholds;
- unsupported claim detection;
- final-report completeness checks;
- single-output validation;
- cleanup checks;
- SEC filing coverage checks;
- government-contract verification checks.

### Add or improve provider adapters

Edit `src/universal_vendor_orchestrator.py` to improve provider compatibility.

Provider work should:

- use environment variables rather than hard-coded keys;
- fail clearly when a key is missing;
- allow model override through CLI arguments;
- preserve the same sub-agent prompt contract across providers;
- return text in a normalized format for the report assembler.

### Improve VS Code tasks

Edit `.vscode/tasks.json` to add useful run configurations.

Task changes should:

- keep arguments explicit;
- avoid storing secrets;
- support provider selection;
- use `artifacts/exhaustive_final_report.md` as the output target.

### Improve the final report assembler

The report assembler should preserve exhaustive content while minimizing unnecessary output files.

Useful improvements include:

- better Markdown structure;
- table rendering for Pugh Matrix output;
- quality JSON validation before insertion;
- evidence appendix grouping by section;
- improved formatting for SEC bullets and future actions.

## Development Setup

Clone the repository and install dependencies:

```bash
git clone <repo-url>
cd <repo-name>
pip install -r requirements.txt
```

Create a local environment file:

```bash
cp .env.example .env
```

Add only the keys you plan to use:

```bash
OPENAI_API_KEY="your-openai-key"
ANTHROPIC_API_KEY="your-anthropic-key"
GEMINI_API_KEY="your-gemini-key"
GOOGLE_API_KEY="your-google-key-if-needed"
PERPLEXITY_API_KEY="your-perplexity-key"
```

Run offline mode for structural checks:

```bash
python src/universal_vendor_orchestrator.py \
  --vendor "Test Vendor" \
  --provider offline
```

Run a model-backed test only when keys are configured:

```bash
python src/universal_vendor_orchestrator.py \
  --vendor "Rubrik, Inc." \
  --ticker RBRK \
  --provider perplexity \
  --model sonar-pro
```

## Pull Request Checklist

Before opening a pull request, verify:

- [ ] The package still produces only `artifacts/exhaustive_final_report.md` as a persistent output.
- [ ] No API keys or secrets are committed.
- [ ] `README.md` is updated if behavior changes.
- [ ] `skills.md` is updated if skill capabilities change.
- [ ] `agents.md` is updated if sub-agent responsibilities change.
- [ ] `playbooks.md` is updated if execution flow changes.
- [ ] `guardrails.md` is updated if validation rules change.
- [ ] Offline scaffold mode still runs.
- [ ] Provider-specific code fails gracefully when keys are missing.
- [ ] Pugh Matrix content is rendered as a Markdown table in the final report.
- [ ] Quality Document JSON is appended as the last section of the final report.
- [ ] Evidence URL requirements are preserved.

## Testing Expectations

At minimum, contributors should run:

```bash
python src/universal_vendor_orchestrator.py --vendor "Test Vendor" --provider offline
```

Then confirm:

```bash
test -f artifacts/exhaustive_final_report.md
find artifacts -type f | wc -l
```

The artifact count should be `1` unless the repository maintainers have explicitly changed the single-output policy.

For provider-backed changes, run at least one configured provider:

```bash
python src/universal_vendor_orchestrator.py \
  --vendor "Rubrik, Inc." \
  --ticker RBRK \
  --provider perplexity \
  --model sonar-pro
```

## Coding Standards

- Keep code readable and modular.
- Use provider adapters rather than duplicating orchestration logic.
- Keep prompt templates clear and versionable.
- Avoid hidden side effects and unexpected file writes.
- Make cleanup idempotent.
- Validate inputs and report actionable errors.
- Prefer explicit CLI arguments over implicit behavior.

## Documentation Standards

Documentation updates should include:

- the reason for the change;
- how to run the updated feature;
- provider-specific configuration, if applicable;
- examples for public and private vendors when relevant;
- guardrail implications.

## Evidence Standards

When improving research prompts or report sections, preserve these source priorities:

1. SEC filings and official annual reports;
2. company investor relations pages;
3. company product, trust, compliance, security, sustainability, and customer pages;
4. government procurement portals, agency notices, FedRAMP listings, and marketplaces;
5. official press releases;
6. reputable analyst, market, and financial references;
7. credible news coverage.

Do not present unsupported vendor claims as fact.

## Issue Template Suggestions

When opening an issue, include:

- affected file or module;
- expected behavior;
- actual behavior;
- provider and model used;
- command run;
- sample vendor tested;
- relevant logs with secrets removed;
- whether the issue affects single-output compliance.

## Contribution Areas Needing Help

High-value contribution areas:

- richer SEC filing extraction;
- better customer/supplier confidence scoring;
- better government-contract detection;
- improved source de-duplication;
- model-specific prompt optimization;
- hallucination and unsupported-claim detection;
- better Pugh Matrix scoring calibration;
- better token-budget controls;
- automated Markdown quality checks.

## Security Policy for Contributors

Do not commit:

- API keys;
- `.env` files;
- customer confidential data;
- private contracts;
- unpublished financial data;
- credentials or browser cookies;
- local cache files containing sensitive outputs.

If you accidentally commit a secret, rotate it immediately and notify maintainers.

## Review Criteria

Maintainers should review contributions for:

- correctness;
- evidence quality;
- provider portability;
- clean-state behavior;
- single-output compliance;
- prompt clarity;
- token efficiency;
- ease of use in VS Code;
- maintainability.

## Release Notes

For meaningful changes, add a short release-note entry describing:

- what changed;
- why it matters;
- migration steps, if any;
- any new environment variables or CLI arguments.

## Contributor Recognition

Contributors may add themselves to a contributors section when the repository owner enables it. Keep recognition concise and tied to meaningful contributions.
