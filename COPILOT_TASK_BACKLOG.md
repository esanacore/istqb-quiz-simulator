# Copilot Task Backlog

## Purpose

This backlog is meant to give GitHub Copilot or other coding assistants **bounded, safe, high-value tasks** for improving the repository without losing structure or correctness.

Use these tasks one at a time.

---

## Priority 1: Safe High-Value Improvements

### 1. Add topic metadata to the question bank

Goal:

- add a `topic` field to all questions in `question_bank.json`

Why:

- improves future filtering
- supports weak-area study modes
- improves analytics potential

Constraints:

- do not alter answer correctness
- preserve existing source metadata

### 2. Add learning objective metadata to the question bank

Goal:

- add an `lo` or `learning_objective` field for each question

Why:

- improves review quality
- supports targeted practice modes

Constraints:

- keep schema consistent across records

### 3. Add merge-scaffold unit tests

Goal:

- create tests for `merge_scaffold.py`

Why:

- the merge toolkit is currently documented and runnable, but not yet unit tested

Suggested coverage:

- config loading
- duplicate key generation
- authority-based conflict resolution
- quarantine behavior for empty keys

### 4. Add history sorting in the history window

Goal:

- show most recent attempts first

Why:

- better usability

Constraints:

- do not break delete behavior

### 5. Add a “Clear History” action with confirmation

Goal:

- allow clearing all stored attempts in one action

Why:

- useful for resets and fresh study cycles

Constraints:

- require confirmation
- update UI immediately after deletion

---

## Priority 2: Targeted Product Improvements

### 6. Add weak-area study mode

Goal:

- create an alternate exam mode that favors missed topics

Why:

- improves learning efficiency

Recommended design:

- track topic-level misses in history or a separate stats file
- bias question selection, but do not remove randomness entirely

### 7. Add exam settings dialog

Goal:

- let the user choose exam size and duration

Why:

- supports shorter study sessions

Constraints:

- preserve current defaults of `40` questions and `60` minutes

### 8. Add question search/filter tools for review mode

Goal:

- let users filter reviewed questions by source, topic, or result

Why:

- improves post-exam study workflow

### 9. Improve result-window formatting

Goal:

- make the report easier to scan visually

Ideas:

- stronger section separators
- per-question status headers
- optional summary by topic

### 10. Add export of exam history to JSON or CSV

Goal:

- let users export attempt history

Why:

- useful for tracking progress over time

---

## Priority 3: Structural / Maintenance Improvements

### 11. Split Tkinter dialogs into dedicated classes

Goal:

- extract history window and results window into smaller UI classes

Why:

- reduces `ISTQBQuizApp.py` density

Constraints:

- do not move domain logic back into the UI layer

### 12. Add dedicated validation helpers to `exam_storage.py`

Goal:

- separate validation from loading logic

Why:

- improves readability and reuse

### 13. Add typed aliases or light typing improvements

Goal:

- improve readability of history and question record shapes

Why:

- makes future maintenance easier

Constraints:

- keep typing pragmatic, not overengineered

### 14. Add a reusable data-import pipeline for question-bank expansion

Goal:

- create a structured importer for bringing in new source-backed questions

Why:

- reduces manual JSON editing risk

### 15. Add repository automation for merge-toolkit smoke validation

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

1. add merge-scaffold unit tests
2. add topic metadata to the question bank
3. add history sorting in the history window
