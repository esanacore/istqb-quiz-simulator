---
name: unit-integration-test-review
description: Review code changes for missing unit and integration tests across domain, storage, CLI helper, and merge-tool behavior in this repository.
---

# Unit and Integration Test Review

Use this skill when behavior changes should be covered without relying on a live GUI.

## Review procedure

1. Trace the changed logic into [exam_models.py](../../../exam_models.py), [exam_storage.py](../../../exam_storage.py), [cli_quiz.py](../../../cli_quiz.py), [merge_scaffold.py](../../../merge_scaffold.py), or helpers.
2. Check [test_istqb_quiz_app.py](../../../test_istqb_quiz_app.py) for direct coverage of the changed logic.
3. Prefer recommendations that add small focused `unittest` methods before suggesting larger integration tests.
4. Identify the narrowest missing regression tests that would catch the new failure mode.

## Repo-specific reminders

- Test domain logic directly without requiring a live Tkinter window.
- Integration-style tests are appropriate when storage, result normalization, or end-to-end exam assembly changed.
