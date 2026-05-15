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
- desktop radio-button helper conversion for explicit no-selection state

### CLI/Layout Helper Tests

The suite also verifies:

- CLI answer parsing
- CLI progress and map rendering helpers
- CLI per-question review rendering
- CLI submit and restart command flow
- CLI startup error handling for malformed quiz data
- responsive layout mode selection
- responsive minimum wrap constraints
- responsive wrap-length calculations

### Desktop Smoke Tests

The suite also verifies lightweight desktop workflows with a hidden Tk root:

- jump-to-question answer persistence
- history window creation and newest-first ordering
- result submission disabling exam controls and recording history
- restart flow resetting the radio-button state and re-enabling controls

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

## Dependency / Supply-Chain Verification

For the current repository, the main automated supply-chain signals are:

- weekly GitHub Actions updates through [.github/dependabot.yml](.github/dependabot.yml)
- CVE-oriented review guidance in [COPILOT_REVIEW_STACK.md](COPILOT_REVIEW_STACK.md)

If Python dependency manifests are added or changed, run:

```powershell
pip-audit --desc
```

The Copilot cloud-agent setup also provisions `pip-audit` in `.github/workflows/copilot-setup-steps.yml` so security review sessions can use the same command.

Expected current baseline:

- `84` automated tests
- all tests pass
- compile check passes

## Copilot Review Automation

Automated tests remain the primary correctness signal, but the repository now also includes a repo-scoped Copilot review stack for:

- documentation sync
- unit and integration coverage review
- system/e2e workflow review
- CVE and supply-chain review
- UI, accessibility, and Tkinter state-flow review

See [COPILOT_REVIEW_STACK.md](COPILOT_REVIEW_STACK.md) for the reviewer roles and workflow.

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

- timeout-driven result flow
- history deletion and clear-history confirmation dialogs
- question navigator rendering under more layout states
- larger desktop resize and wrap stress cases

That should still remain secondary to domain/storage tests.

## Testing Philosophy

For this repo, prefer tests that are:

- deterministic
- fast
- isolated from GUI timing
- easy to understand and maintain

The goal is not exhaustive automation of Tkinter widgets. The goal is reliable validation of the rules that make the simulator trustworthy.
