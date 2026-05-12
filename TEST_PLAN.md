# Test Plan

## Purpose

This plan defines the verification approach for the quiz simulator and dataset merge toolkit.

The project follows an ISTQB-aligned mindset: requirements should be identifiable, tests should be traceable, and known coverage gaps should be explicit.

## Test Levels

### Unit Tests

Unit tests cover deterministic logic that can run without a GUI:

- question-bank validation
- exam assembly
- exam session state transitions
- scoring and report generation
- history normalization and ordering
- CLI parsing/rendering helpers
- responsive layout calculations
- merge scaffold normalization, dedupe, conflict handling, and export helpers

### Integration-Style Tests

Integration-style tests combine storage-built exam questions with domain execution and history-entry creation.

Current integration-style coverage:

- `EndToEndExamFlowTests.test_build_exam_answer_and_persist_history_flow`

### Manual UI Regression

Tkinter windows and full CLI interactive loops are primarily manual for now because the highest-risk logic is isolated in UI-independent modules.

Manual checks are listed in `REQUIREMENTS_TRACEABILITY_MATRIX.md`.

## Test Design Techniques

The current suite uses:

- equivalence partitioning for valid and invalid question/history payloads
- boundary value checks for navigation bounds, timer floor, compact/wide layout thresholds, and empty sessions
- decision-table style checks for pass/fail threshold and merge authority choices
- state transition checks for restart, submit lock, mark toggling, and answer clearing
- integration workflow coverage for exam assembly, answering, submission, and history persistence

## Entry Criteria

Run the automated suite when:

- `exam_models.py` changes
- `exam_storage.py` changes
- `cli_quiz.py` command or helper behavior changes
- `ui_layout.py` changes
- `merge_scaffold.py` changes
- question-bank schema expectations change
- documentation claims new behavior or coverage

## Exit Criteria

Before considering meaningful changes complete:

```powershell
python -m unittest -v
python -m py_compile ISTQBQuizApp.py cli_quiz.py exam_models.py exam_storage.py test_istqb_quiz_app.py merge_scaffold.py ui_layout.py
```

Use `python3` instead of `python` if the local environment does not expose `python`.

Expected current baseline:

- 41 automated tests pass
- compile check exits successfully

## Test Data

Automated tests create temporary JSON fixtures in `.testdata/`.

Rules:

- test data must be deterministic
- test data must not mutate `question_bank.json`
- runtime history belongs in `exam_history.json` and is ignored by git
- source-backed question content should remain traceable

## Defect Reporting Expectations

When a test fails or a defect is found, record:

- affected requirement ID if known
- exact command or workflow
- observed result
- expected result
- suspected layer: UI, CLI, domain, storage, layout, merge toolkit, or docs
- whether the issue affects answer correctness or source provenance

## Coverage Gaps

Known gaps:

- no automated Tkinter smoke tests
- no automated full interactive CLI loop tests
- no topic or learning-objective metadata coverage until metadata exists
- no weak-area study tests because that feature is not implemented
- no export tests for history because history export is not implemented

These gaps are tracked in `REQUIREMENTS_TRACEABILITY_MATRIX.md` and `COPILOT_TASK_BACKLOG.md`.
