# Orchestrator Agent

Owns execution. Reads skills.md, loads agent registry, selects playbooks, delegates work, validates guardrails, and assembles `exhaustive_final_report.md`. In online chat mode, it performs conceptual sub-agent execution inside the model context. In local mode, it maps section tasks to provider calls.
