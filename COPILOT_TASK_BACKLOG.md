# Copilot Task Backlog

## Purpose

This backlog is meant to give GitHub Copilot or other coding assistants **bounded, safe, high-value tasks** for improving the repository without losing structure or correctness.

Use these tasks one at a time.

---

## Priority 1: Safe High-Value Improvements

### 1. Add lightweight UI smoke checks

Goal:

- add guarded smoke tests or a documented manual script for desktop startup, history dialog, result dialog, and navigator rendering

Why:

- the requirements traceability matrix currently marks several Tkinter behaviors as manual or partial

Constraints:

- keep UI tests optional or robust in headless environments

### 2. Add topic metadata to the question bank

Goal:

- add a `topic` field to all questions in `question_bank.json`
- current baseline: `0/96` questions have topic metadata

Why:

- improves future filtering
- supports weak-area study modes
- improves analytics potential

Constraints:

- do not alter answer correctness
- preserve existing source metadata

### 3. Add learning objective metadata to the question bank

Goal:

- add an `lo` or `learning_objective` field for each question
- current baseline: `0/96` questions have learning-objective metadata

Why:

- improves review quality
- supports targeted practice modes

Constraints:

- keep schema consistent across records

### 4. Add source/topic-aware review filtering

Goal:

- let users filter reviewed questions by source now, and by topic once metadata exists

Why:

- improves post-exam study workflow
- builds on the CLI per-question review pattern without requiring a new exam mode

Constraints:

- keep filtering presentation-layer only until topic metadata is complete
- do not change scoring or history schema for this task

---

## Priority 2: Targeted Product Improvements

### 5. Add weak-area study mode

Goal:

- create an alternate exam mode that favors missed topics

Why:

- improves learning efficiency

Recommended design:

- complete topic metadata first
- track topic-level misses in history or a separate stats file
- bias question selection, but do not remove randomness entirely

### 6. Add exam settings dialog

Goal:

- let the user choose exam size and duration

Why:

- supports shorter study sessions

Constraints:

- preserve current defaults of `40` questions and `60` minutes

### 7. Improve result-window formatting

Goal:

- make the report easier to scan visually

Ideas:

- stronger section separators
- per-question status headers
- optional summary by topic

### 8. Add export of exam history to JSON or CSV

Goal:

- let users export attempt history

Why:

- useful for tracking progress over time

---

## Priority 3: Structural / Maintenance Improvements

### 9. Split Tkinter dialogs into dedicated classes

Goal:

- extract history window and results window into smaller UI classes

Why:

- reduces `ISTQBQuizApp.py` density

Constraints:

- do not move domain logic back into the UI layer

### 10. Add dedicated validation helpers to `exam_storage.py`

Goal:

- separate validation from loading logic

Why:

- improves readability and reuse

### 11. Add typed aliases or light typing improvements

Goal:

- improve readability of history and question record shapes

Why:

- makes future maintenance easier

Constraints:

- keep typing pragmatic, not overengineered

### 12. Add a reusable data-import pipeline for question-bank expansion

Goal:

- create a structured importer for bringing in new source-backed questions

Why:

- reduces manual JSON editing risk

### 13. Add repository automation for merge-toolkit smoke validation

Goal:

- extend GitHub Actions to compile and smoke-check merge toolkit behavior

Why:

- keeps toolkit changes safer over time

---

## Task Execution Rules For Copilot

When using this backlog with Copilot:

- do one task at a time
- keep changes bounded
- update tests if logic changes
- update docs if behavior or structure changes
- preserve question provenance
- do not invent official-source claims

---

## Recommended Next Three Tasks

If starting immediately, use this order:

1. add lightweight UI smoke checks
2. add topic metadata to the question bank
3. add learning objective metadata to the question bank

---

## Completed / Baseline Tasks

These are already represented in the current codebase and tests:

- merge-scaffold unit tests for config loading, dedupe keys, authority-based conflict resolution, quarantine behavior, and export helpers
- shared pass-threshold behavior in `exam_models.py`
- shared history-entry normalization in `exam_storage.py`
- CLI per-question review rendering and navigation
- newest-first history display while preserving delete behavior
- confirmed clear-history actions in the desktop history window and CLI
- explicit non-object question-bank record validation test
- 41-test automated suite across storage, domain, CLI helpers, layout helpers, merge toolkit, and integration-style exam flow
- SQA requirements, test plan, and requirements traceability matrix documents
