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
- CLI startup and command-loop flows through mocked input
- responsive layout calculations
- merge scaffold normalization, dedupe, conflict handling, and export helpers

### Desktop Smoke Tests

Lightweight desktop smoke tests exercise selected Tkinter workflows with a hidden root window:

- jump-to-question answer persistence
- result submission and control disabling
- history window creation and ordering
- restart reset behavior

### Integration-Style Tests

Integration-style tests combine storage-built exam questions with domain execution and history-entry creation.

Current integration-style coverage:

- `EndToEndExamFlowTests.test_build_exam_answer_and_persist_history_flow`

### Manual UI Regression

Tkinter windows and full CLI interactive loops are primarily manual for now because the highest-risk logic is isolated in UI-independent modules.

Manual checks are listed in `REQUIREMENTS_TRACEABILITY_MATRIX.md`.

### Copilot Review Automation

The repository also uses a repo-scoped Copilot review stack to add specialist reviewer perspectives for:

- documentation drift
- unit and integration coverage gaps
- system/e2e workflow gaps
- CVE and supply-chain risk
- desktop UI, accessibility, and Tkinter state-flow checks

These reviewer passes complement, but do not replace, the automated `unittest` suite and manual UI regression checks.

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
- third-party tooling, GitHub Actions workflows, or dependency manifests change

## Exit Criteria

Before considering meaningful changes complete:

```powershell
python -m unittest -v
python -m py_compile ISTQBQuizApp.py cli_quiz.py exam_models.py exam_storage.py test_istqb_quiz_app.py merge_scaffold.py ui_layout.py
```

If Python dependency manifests are introduced or changed, also run:

```powershell
pip-audit --desc
```

Use `python3` instead of `python` if the local environment does not expose `python`.

Expected current baseline:

- 84 automated tests pass
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

- no automated timeout-triggered Tkinter result smoke test
- no exhaustive automated CLI command-loop coverage for every command path
- no topic or learning-objective metadata coverage until metadata exists
- no weak-area study tests because that feature is not implemented
- no export tests for history because history export is not implemented

Current mitigations for those gaps include:

- manual regression steps in the traceability matrix
- screenshot- and desktop-command-assisted review through the Copilot review stack
- specialist reviewer agents for docs, tests, workflow gaps, and CVE analysis

These gaps are tracked in `REQUIREMENTS_TRACEABILITY_MATRIX.md` and `COPILOT_TASK_BACKLOG.md`.
