---
name: system-e2e-test-review
description: Review desktop and CLI workflow changes for missing system or end-to-end coverage, smoke checks, and documented manual verification gaps.
---

# System and E2E Test Review

Use this skill when a change affects whole user workflows rather than isolated functions.

## Review procedure

1. Identify the user-visible workflow that changed.
2. Check whether the current automated suite already covers that workflow indirectly.
3. If not, determine whether the repo should add a stronger integration test, a manual smoke path, or a documented verification note.
4. For desktop UI changes, use screenshot-based or smoke-flow thinking before recommending new GUI harnesses.
5. For CLI changes, expect the workflow to remain runnable locally and describable in docs.

## Repo-specific reminders

- Tkinter system coverage is currently lighter than unit/integration coverage; say that clearly when relevant.
- Keep `TEST_PLAN.md` and `REQUIREMENTS_TRACEABILITY_MATRIX.md` honest about what is automated versus manual.
