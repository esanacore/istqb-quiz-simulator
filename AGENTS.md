# AGENTS.md

## Purpose

This repository contains a local desktop quiz simulator for **ISTQB CTFL v4.0** exam practice.

Agents working in this repo should optimize for:

- correctness of testing concepts
- maintainability of Python code
- preserving the sourced-question workflow
- keeping UI behavior stable while improving structure

## Architecture

- `ISTQBQuizApp.py`
  Tkinter UI and orchestration only.
- `exam_models.py`
  Pure exam-state logic. Prefer adding business rules here instead of embedding them in the UI.
- `exam_storage.py`
  Question loading, validation, randomized exam assembly, and history persistence.
- `question_bank.json`
  Externalized question pool. Do not hardcode new question content into Python.
- `test_istqb_quiz_app.py`
  Unit tests for non-UI logic.

## Working Rules

- Prefer changes that keep domain logic out of Tkinter callbacks.
- Add or update unit tests when changing behavior in `exam_models.py` or `exam_storage.py`.
- Treat question provenance as important. New questions should be source-backed and traceable.
- Preserve answer correctness when shuffling options.
- Avoid introducing dependencies unless there is a strong justification.
- Keep the app runnable with a simple `python ISTQBQuizApp.py`.

## Documentation Rules

- Use Markdown for repository docs.
- Use Google-style Python docstrings for modules, classes, and non-trivial functions.
- Keep comments high signal. Do not add line-by-line narration comments.

## Verification

Before finishing meaningful code changes, run:

```powershell
python -m unittest -v
python -m py_compile ISTQBQuizApp.py exam_models.py exam_storage.py test_istqb_quiz_app.py
```

## Preferred Improvement Priorities

1. Correctness
2. Testability
3. Maintainability
4. UI polish
5. New features
