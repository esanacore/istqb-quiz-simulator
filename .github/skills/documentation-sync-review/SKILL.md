---
name: documentation-sync-review
description: Review repository documentation for drift when code, workflows, tests, or Copilot customization files change.
---

# Documentation Sync Review

Use this skill when implementation, workflow, or contributor-experience changes might have left docs behind.

## Review procedure

1. Identify what behavior, workflow, or structure changed.
2. Compare that change against [README.md](../../../README.md), [ARCHITECTURE.md](../../../ARCHITECTURE.md), [TESTING.md](../../../TESTING.md), [CONTRIBUTING.md](../../../CONTRIBUTING.md), and [COPILOT_REVIEW_STACK.md](../../../COPILOT_REVIEW_STACK.md).
3. If requirements or verification expectations changed, also check [SOFTWARE_REQUIREMENTS.md](../../../SOFTWARE_REQUIREMENTS.md), [TEST_PLAN.md](../../../TEST_PLAN.md), and [REQUIREMENTS_TRACEABILITY_MATRIX.md](../../../REQUIREMENTS_TRACEABILITY_MATRIX.md).
4. Return exact files and missing edits.

## Repo-specific reminders

- Keep commands aligned with the repo’s current Python invocation guidance.
- Prefer precise documentation deltas over broad “docs stale” comments.
