# Local CLI Prompt Template for Interactive HTML Output

Use this command pattern after updating the local orchestrator to support HTML output:

```bash
python src/universal_vendor_orchestrator.py \
  --vendor "<VENDOR>" \
  --ticker <TICKER> \
  --website <WEBSITE> \
  --provider perplexity \
  --model sonar-pro \
  --depth exhaustive \
  --output artifacts/exhaustive_final_report.html
```

Expected final output:

```text
artifacts/exhaustive_final_report.html
```

The final artifact must be a self-contained interactive HTML report, not Markdown.
