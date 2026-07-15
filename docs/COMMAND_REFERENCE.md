# Command Reference

Run every command from the repository root.

## Core App Commands

- `python ISTQBQuizApp.py`
  Starts the Tkinter desktop simulator.
- `python cli_quiz.py`
  Starts the terminal-first simulator. On Windows, prefer a UTF-8 console:
  `$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'`.

## Test And Validation Commands

- `python -m unittest -v`
  Runs the full automated test suite in `test_istqb_quiz_app.py`.
- `python -m py_compile ISTQBQuizApp.py cli_quiz.py exam_models.py exam_storage.py test_istqb_quiz_app.py merge_scaffold.py ui_layout.py`
  Verifies that the main Python modules compile cleanly.

## Dataset Toolkit

- `python merge_scaffold.py dataset_merge_config.template.json`
  Runs the generic JSON merge workflow and writes outputs under `merge_output/`
  unless the config overrides the destination.

## Constitution Checks

- `"C:\Program Files\Git\bin\bash.exe" constitution/scripts/check_compliance.sh --strict .`
  Verifies that the repository carries the expected Constitution files.
- `"C:\Program Files\Git\bin\bash.exe" constitution/scripts/check_version_alignment.sh`
  Verifies that local governance files do not mention stale Constitution
  versions after a submodule update.

## Git And Submodule Maintenance

- `git submodule update --init --recursive`
  Initializes or refreshes the pinned Constitution checkout.
- `git submodule update --remote constitution`
  Moves the submodule to the latest remote-tracked commit; review and validate
  before committing.
