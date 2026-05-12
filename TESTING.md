# Testing

## Current Approach

This repository uses **Python `unittest`** for logic-level automated tests.

Primary test file:

- [test_istqb_quiz_app.py](test_istqb_quiz_app.py)

The current suite focuses on **UI-independent behavior** because that provides the highest confidence-to-effort ratio for this project.

For the formal SQA view, see:

- [SOFTWARE_REQUIREMENTS.md](SOFTWARE_REQUIREMENTS.md)
- [REQUIREMENTS_TRACEABILITY_MATRIX.md](REQUIREMENTS_TRACEABILITY_MATRIX.md)
- [TEST_PLAN.md](TEST_PLAN.md)

## What Is Covered

### Storage Tests

The suite currently verifies:

- valid question-bank loading
- rejection of malformed question-bank files
- rejection of invalid answer definitions
- randomized exam generation
- smaller-bank exam sizing behavior
- preservation of correct answers after option shuffling
- history load behavior when no history file exists
- malformed history rejection
- history primitive normalization
- history save/load round-trip behavior
- normalized history record creation
- newest-first history ordering

### Domain Tests

The suite currently verifies:

- question navigation
- answer persistence
- answer clearing
- mark-for-review behavior
- timer countdown reduction
- restart/reset behavior
- submission and result generation
- score calculation
- empty-session result behavior
- configurable pass-threshold behavior
- session lock behavior after submission

### CLI/Layout Helper Tests

The suite also verifies:

- CLI answer parsing
- CLI progress and map rendering helpers
- CLI per-question review rendering
- responsive layout mode selection
- responsive minimum wrap constraints
- responsive wrap-length calculations

### Merge Toolkit Tests

The suite also verifies:

- source JSON payload validation
- merge config validation
- normalization fallback behavior
- provenance preservation
- dedupe key generation
- authority-based conflict resolution
- equal-authority duplicate handling
- quarantine behavior
- merged/quarantined/audit export helpers

### Integration-Style Tests

The suite includes an end-to-end style check for:

- storage-built exam question assembly
- answering every selected question through `ExamSession`
- submission and score generation
- normalized history-entry creation

## Why UI Logic Is Not Heavily Unit Tested

Tkinter UI testing is possible, but it is more fragile and less valuable than testing:

- domain state transitions
- data validation
- persistence behavior

The current architecture intentionally moves important logic into `exam_models.py` and `exam_storage.py` so those behaviors can be tested directly.

## How To Run Tests

Use `python3` instead of `python` if your local environment does not expose `python`.

```powershell
python -m unittest -v
```

## Compile / Syntax Verification

```powershell
python -m py_compile ISTQBQuizApp.py cli_quiz.py exam_models.py exam_storage.py test_istqb_quiz_app.py merge_scaffold.py ui_layout.py
```

Expected current baseline:

- `40` automated tests
- all tests pass
- compile check passes

## Recommended Future Testing Improvements

### 1. Expand Domain Coverage

Add tests for:

- timeout-related session behavior
- report formatting edge cases
- empty or malformed optional metadata

### 2. Add Storage Edge Cases

Add tests for:

- additional merge scaffold conflict shapes as new rules are added

### 3. Add UI Smoke Coverage

If the project grows further, consider adding lightweight UI smoke tests that validate:

- app startup
- history dialog creation
- result dialog creation
- question navigator rendering

That should still remain secondary to domain/storage tests.

## Testing Philosophy

For this repo, prefer tests that are:

- deterministic
- fast
- isolated from GUI timing
- easy to understand and maintain

The goal is not exhaustive automation of Tkinter widgets. The goal is reliable validation of the rules that make the simulator trustworthy.
