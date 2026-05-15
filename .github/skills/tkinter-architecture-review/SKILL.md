---
name: tkinter-architecture-review
description: Review desktop implementation changes for separation of UI orchestration from exam-domain and storage logic, especially around state transitions and callbacks.
---

# Tkinter Architecture Review

Use this skill when desktop changes risk mixing widget behavior with domain or persistence logic.

## Review procedure

1. Identify whether behavior belongs in [exam_models.py](../../../exam_models.py) or [exam_storage.py](../../../exam_storage.py) before accepting it in [ISTQBQuizApp.py](../../../ISTQBQuizApp.py).
2. Trace state transitions for answer saving, restart, submit, timeout, and mark-for-review.
3. Flag duplicated logic between the desktop UI and CLI/domain layers.
4. Look for test gaps in [test_istqb_quiz_app.py](../../../test_istqb_quiz_app.py) when behavior changes.

## Repo-specific reminders

- Small, explicit Python is preferred over clever abstraction.
- Domain rules should move into `exam_models.py` first when behavior changes.
