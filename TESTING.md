# Testing

## Current Approach

This repository uses **Python `unittest`** for logic-level automated tests.

Primary test file:

- [test_istqb_quiz_app.py](C:/Projects/practiceISTQB/test_istqb_quiz_app.py:1)

The current suite focuses on **UI-independent behavior** because that provides the highest confidence-to-effort ratio for this project.

## What Is Covered

### Storage Tests

The suite currently verifies:

- valid question-bank loading
- rejection of invalid answer definitions
- randomized exam generation
- preservation of correct answers after option shuffling
- history load behavior when no history file exists
- history save/load round-trip behavior

### Domain Tests

The suite currently verifies:

- question navigation
- answer persistence
- mark-for-review behavior
- restart/reset behavior
- submission and result generation
- score calculation
- session lock behavior after submission

## Why UI Logic Is Not Heavily Unit Tested

Tkinter UI testing is possible, but it is more fragile and less valuable than testing:

- domain state transitions
- data validation
- persistence behavior

The current architecture intentionally moves important logic into `exam_models.py` and `exam_storage.py` so those behaviors can be tested directly.

## How To Run Tests

```powershell
python -m unittest -v
```

## Compile / Syntax Verification

```powershell
python -m py_compile ISTQBQuizApp.py exam_models.py exam_storage.py test_istqb_quiz_app.py
```

## Recommended Future Testing Improvements

### 1. Expand Domain Coverage

Add tests for:

- timeout-related session behavior
- report formatting edge cases
- empty or malformed optional metadata

### 2. Add Storage Edge Cases

Add tests for:

- malformed history files
- missing required question fields
- wrong option counts
- non-dictionary entries in source files

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
