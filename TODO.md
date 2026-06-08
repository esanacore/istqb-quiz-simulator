# TODO

This file is the living roadmap for the ISTQB CTFL Quiz Simulator.

It consolidates the existing Copilot backlog into the Engineering Constitution TODO structure. Keep entries specific, actionable, and current.

## Features

- [ ] Add topic metadata to every question in `question_bank.json`.
- [ ] Add learning-objective metadata to every question in `question_bank.json`.
- [ ] Add source-aware and topic-aware filtering in result review.
- [ ] Add weak-area study mode based on missed topics.
- [ ] Add an exam settings dialog for exam size and duration while preserving defaults of 40 questions and 60 minutes.
- [x] Add export of exam history to JSON or CSV.

## Technical Debt

- [ ] Keep question-bank expansion source-backed and provenance-preserving.
- [ ] Extend automation so merge-toolkit behavior is smoke-checked in CI.

## Refactoring

- [ ] Split Tkinter history and result dialogs into dedicated UI classes.
- [ ] Add dedicated validation helpers in `exam_storage.py`.
- [ ] Add pragmatic typed aliases for history and question record shapes.
- [ ] Add a reusable data-import pipeline for safe question-bank expansion.

## Testing

- [ ] Add lightweight UI smoke checks for desktop startup, history dialog, result dialog, and navigator rendering.
- [ ] Keep UI smoke checks optional or robust in headless environments.
- [ ] Continue updating `REQUIREMENTS_TRACEABILITY_MATRIX.md` as test coverage changes.

## Documentation

- [ ] Keep `COPILOT_TASK_BACKLOG.md` aligned with this TODO file or retire it after migration.
- [ ] Keep `TESTING.md`, `TEST_PLAN.md`, and `REQUIREMENTS_TRACEABILITY_MATRIX.md` aligned with verification changes.
- [ ] Document any new question metadata schema fields before changing `question_bank.json`.

## Nice-to-Have

- [ ] Improve result-window formatting with stronger section separators and summary information.
- [ ] Add optional topic summary in post-exam review after topic metadata exists.
