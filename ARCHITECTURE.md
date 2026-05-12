# Architecture

## Overview

The application is intentionally split into **three layers**:

1. **Presentation / orchestration**
2. **Domain model**
3. **Persistence / exam assembly**

This keeps Tkinter concerns separate from logic that should be easy to test and maintain.

The repository also maintains SQA artifacts:

- [SOFTWARE_REQUIREMENTS.md](SOFTWARE_REQUIREMENTS.md)
- [REQUIREMENTS_TRACEABILITY_MATRIX.md](REQUIREMENTS_TRACEABILITY_MATRIX.md)
- [TEST_PLAN.md](TEST_PLAN.md)
- [TESTING.md](TESTING.md)

Those documents define testable requirements, map requirements to automated/manual checks, and record known verification gaps.

## Layers

### 1. Presentation Layer

Files:

- [ISTQBQuizApp.py](ISTQBQuizApp.py)
- [cli_quiz.py](cli_quiz.py)
- [ui_layout.py](ui_layout.py)

Responsibilities:

- create and style Tkinter widgets
- provide an interactive command-line exam flow
- render current exam state in desktop and terminal surfaces
- manage user actions such as navigation and submission
- update visual state such as question highlighting, wrap behavior, and question map colors
- show results and history views

The presentation layer should not own core scoring or navigation rules beyond delegating to the domain layer.

### 2. Domain Layer

File: [exam_models.py](exam_models.py)

Responsibilities:

- represent one exam attempt
- persist in-memory answer state
- manage navigation between questions
- manage mark-for-review state
- reset attempts
- build result summaries and review reports
- own the pass/fail threshold used by both presentation surfaces

Primary types:

- `ExamSession`
- `ExamResult`

This layer is pure Python and intentionally has no Tkinter dependency.

### 3. Storage Layer

File: [exam_storage.py](exam_storage.py)

Responsibilities:

- load and validate `question_bank.json`
- load and save `exam_history.json`
- normalize completed attempts into history records
- assemble randomized exam attempts from the larger bank
- shuffle answer order while preserving correctness

This layer is where file-backed behavior and question-pool rules should live.

### 4. Dataset Toolkit Layer

Files:

- [merge_scaffold.py](merge_scaffold.py)
- [DATASET_INTEGRATION_PLAYBOOK.md](DATASET_INTEGRATION_PLAYBOOK.md)
- [MERGE_CHECKLIST.md](MERGE_CHECKLIST.md)
- [DATASET_SCHEMA_TEMPLATE.md](DATASET_SCHEMA_TEMPLATE.md)
- [MERGE_CLI_GUIDE.md](MERGE_CLI_GUIDE.md)
- [dataset_merge_config.template.json](dataset_merge_config.template.json)

Responsibilities:

- define how multiple partial datasets should be normalized and merged
- preserve provenance across combined records
- provide a reusable merge scaffold for future projects
- document the config-driven merge CLI workflow
- make dataset integration repeatable instead of ad hoc

## Data Files

### Question Bank

File: [question_bank.json](question_bank.json)

Contains:

- question text
- 4 answer options
- correct answer text
- explanation
- source metadata
- optional topic / learning objective metadata

### Exam History

File: `exam_history.json`

Created at runtime.

Contains:

- timestamp
- score
- total questions
- percent
- pass/fail result

## Runtime Flow

1. Desktop UI or CLI starts and loads question bank plus persisted history.
2. Storage layer builds a randomized `40`-question exam from the larger bank.
3. Domain session is initialized with the selected exam questions.
4. UI renders the active question and navigator state.
5. User answers, jumps, marks, and submits.
6. Domain layer computes the score and review report.
7. UI asks storage to normalize the history record, persists the attempt, and displays results.

## Design Notes

- The current architecture favors **clarity over abstraction depth**.
- Tkinter remains in one main UI file to avoid over-fragmentation.
- Shared exam behavior is intended to stay in `exam_models.py` so the GUI and CLI do not drift.
- The domain model is the primary seam for future test growth.
- If the UI grows significantly, the next split should be:
  - main window controller
  - history dialog
  - result dialog
  - navigator panel

## Extension Guidance

When adding new behavior:

- add domain rules to `exam_models.py`
- add file-backed logic to `exam_storage.py`
- keep `ISTQBQuizApp.py` focused on rendering and event handling

When adding study features such as topic targeting or weak-area review:

- first define the data shape in `question_bank.json`
- then extend storage assembly behavior
- then wire the new mode into the UI
