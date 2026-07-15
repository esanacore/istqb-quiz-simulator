# Agent Handoff

## Current State

- The desktop Tkinter simulator (`ISTQBQuizApp.py`) and terminal simulator
  (`cli_quiz.py`) both run locally from the repository root.
- Shared quiz-domain behavior lives in `exam_models.py` and `exam_storage.py`.
- Automated validation currently consists of `python -m unittest -v` plus the
  explicit `py_compile` command documented in [`COMMAND_REFERENCE.md`](COMMAND_REFERENCE.md).
- The repository now carries repo-specific setup, architecture, command, and
  troubleshooting docs under `docs/`.

## Important Working Files

- `question_bank.json`: canonical quiz-question source
- `exam_history.json`: runtime-generated attempt history file
- `test_istqb_quiz_app.py`: automated test suite
- `merge_scaffold.py` and `dataset_merge_config.template.json`: reusable
  dataset-merge tooling

## Operational Caveats

- The CLI requires a UTF-8 console on Windows; otherwise `python cli_quiz.py`
  can fail with a `charmap` encoding error.
- There is no dependency lockfile yet. The app currently relies on the Python
  standard library only.
- The repository uses root-level testing and requirements docs
  (`TEST_PLAN.md`, `TESTING.md`, `SOFTWARE_REQUIREMENTS.md`,
  `REQUIREMENTS_TRACEABILITY_MATRIX.md`) alongside the `docs/` governance layer.

## Next Recommended Checks

1. Run `python -m unittest -v`.
2. Run the `py_compile` command from [`COMMAND_REFERENCE.md`](COMMAND_REFERENCE.md).
3. If governance files changed, run the Constitution compliance and version
   alignment checks from Git Bash.
