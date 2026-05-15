---
name: requirements-traceability-review
description: Review whether behavior changes are reflected in requirements, test plan, and traceability artifacts for this repository.
---

# Requirements Traceability Review

Use this skill when behavior, tests, workflows, or contributor guidance changes.

## Review procedure

1. Read the implementation diff and identify any changed behavior.
2. Check whether [SOFTWARE_REQUIREMENTS.md](../../../SOFTWARE_REQUIREMENTS.md) needs a requirement update.
3. Check whether [REQUIREMENTS_TRACEABILITY_MATRIX.md](../../../REQUIREMENTS_TRACEABILITY_MATRIX.md) should map new or changed tests.
4. Check whether [TEST_PLAN.md](../../../TEST_PLAN.md) or [TESTING.md](../../../TESTING.md) should change.
5. Return exact file updates that appear missing.

## Repo-specific reminders

- Keep requirements testable.
- Avoid vague “documentation may need updates” output; point to the specific artifact and gap.
