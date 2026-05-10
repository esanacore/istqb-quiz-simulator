# Architecture

## Overview

The application is intentionally split into **three layers**:

1. **UI / orchestration**
2. **Domain model**
3. **Persistence / exam assembly**

This keeps Tkinter concerns separate from logic that should be easy to test and maintain.

## Layers

### 1. UI Layer

File: [ISTQBQuizApp.py](C:/Projects/practiceISTQB/ISTQBQuizApp.py:1)

Responsibilities:

- create and style Tkinter widgets
- render current exam state
- manage user actions such as navigation and submission
- update visual state such as question highlighting and question map colors
- show results and history windows

The UI should not own core scoring or navigation rules beyond delegating to the domain layer.

### 2. Domain Layer

File: [exam_models.py](C:/Projects/practiceISTQB/exam_models.py:1)

Responsibilities:

- represent one exam attempt
- persist in-memory answer state
- manage navigation between questions
- manage mark-for-review state
- reset attempts
- build result summaries and review reports

Primary types:

- `ExamSession`
- `ExamResult`

This layer is pure Python and intentionally has no Tkinter dependency.

### 3. Storage Layer

File: [exam_storage.py](C:/Projects/practiceISTQB/exam_storage.py:1)

Responsibilities:

- load and validate `question_bank.json`
- load and save `exam_history.json`
- assemble randomized exam attempts from the larger bank
- shuffle answer order while preserving correctness

This layer is where file-backed behavior and question-pool rules should live.

### 4. Dataset Toolkit Layer

Files:

- [merge_scaffold.py](C:/Projects/practiceISTQB/merge_scaffold.py:1)
- [DATASET_INTEGRATION_PLAYBOOK.md](C:/Projects/practiceISTQB/DATASET_INTEGRATION_PLAYBOOK.md:1)
- [MERGE_CHECKLIST.md](C:/Projects/practiceISTQB/MERGE_CHECKLIST.md:1)
- [DATASET_SCHEMA_TEMPLATE.md](C:/Projects/practiceISTQB/DATASET_SCHEMA_TEMPLATE.md:1)

Responsibilities:

- define how multiple partial datasets should be normalized and merged
- preserve provenance across combined records
- provide a reusable merge scaffold for future projects
- make dataset integration repeatable instead of ad hoc

## Data Files

### Question Bank

File: [question_bank.json](C:/Projects/practiceISTQB/question_bank.json:1)

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

1. UI starts and loads question bank plus persisted history.
2. Storage layer builds a randomized `40`-question exam from the larger bank.
3. Domain session is initialized with the selected exam questions.
4. UI renders the active question and navigator state.
5. User answers, jumps, marks, and submits.
6. Domain layer computes the score and review report.
7. UI writes the attempt to history and displays results.

## Design Notes

- The current architecture favors **clarity over abstraction depth**.
- Tkinter remains in one main UI file to avoid over-fragmentation.
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
