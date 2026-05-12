# AGENTS.md

## Purpose

This repository contains a local desktop quiz simulator for **ISTQB CTFL v4.0** exam practice.

Agents working in this repo should optimize for:

- correctness of testing concepts
- maintainability of Python code
- preserving the sourced-question workflow
- keeping UI behavior stable while improving structure

This repository also contains a reusable **project-improvement and dataset-integration toolkit**. Agents may improve that toolkit, but should avoid letting toolkit work destabilize the simulator itself.

## Architecture

- `ISTQBQuizApp.py`
  Tkinter UI and orchestration only.
- `exam_models.py`
  Pure exam-state logic. Prefer adding business rules here instead of embedding them in the UI.
- `exam_storage.py`
  Question loading, validation, randomized exam assembly, history-entry normalization, and history persistence.
- `cli_quiz.py`
  Terminal UI built on the same exam-state and storage layers as the desktop app.
- `ui_layout.py`
  Pure responsive-layout helper logic for the Tkinter app.
- `merge_scaffold.py`
  Generic merge CLI scaffold for combining multiple source datasets into one normalized output.
- `question_bank.json`
  Externalized question pool. Do not hardcode new question content into Python.
- `test_istqb_quiz_app.py`
  Unit tests for non-UI logic.

Supporting docs worth keeping aligned:

- `README.md`
- `ARCHITECTURE.md`
- `TESTING.md`
- `TEST_PLAN.md`
- `SOFTWARE_REQUIREMENTS.md`
- `REQUIREMENTS_TRACEABILITY_MATRIX.md`
- `CONTRIBUTING.md`
- `COPILOT_TASK_BACKLOG.md`
- `PROJECT_EVOLUTION_FRAMEWORK.md`
- `DATASET_INTEGRATION_PLAYBOOK.md`
- `MERGE_CLI_GUIDE.md`

## Working Rules

- Inspect the current repo state before changing structure or docs.
- Prefer changes that keep domain logic out of Tkinter callbacks.
- Add or update unit tests when changing behavior in `exam_models.py` or `exam_storage.py`.
- Update the requirements traceability matrix when adding, removing, or materially changing requirements or tests.
- Keep requirements testable and assign stable requirement IDs for new behavior.
- If changing merge behavior, keep `merge_scaffold.py`, `MERGE_CLI_GUIDE.md`, and the dataset toolkit docs consistent.
- Treat question provenance as important. New questions should be source-backed and traceable.
- Preserve answer correctness when shuffling options.
- Avoid introducing dependencies unless there is a strong justification.
- Keep the app runnable with a simple `python ISTQBQuizApp.py`.

Preferred change order:

1. correctness
2. structure/testability
3. tests
4. docs
5. UI polish
6. feature expansion

## Documentation Rules

- Use Markdown for repository docs.
- Use Google-style Python docstrings for modules, classes, and non-trivial functions.
- Keep comments high signal. Do not add line-by-line narration comments.
- When architecture or workflow changes, update the related markdown docs in the same change.

## Verification

Before finishing meaningful code changes, run:

```powershell
python -m unittest -v
python -m py_compile ISTQBQuizApp.py cli_quiz.py exam_models.py exam_storage.py test_istqb_quiz_app.py merge_scaffold.py ui_layout.py
```

## Preferred Improvement Priorities

1. Correctness
2. Testability
3. Maintainability
4. Documentation accuracy
5. UI polish
6. New features
