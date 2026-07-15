# Troubleshooting

This project is small enough that most failures fall into one of four buckets:
question-bank data issues, history-file issues, terminal-encoding issues, or
running commands from the wrong working directory.

## CLI Fails With A `charmap` Encoding Error

- **Symptoms**: Launching `python cli_quiz.py` prints the title banner and then
  fails with a `charmap` codec error on Windows.
- **Cause**: The CLI writes ANSI/box-drawing output to a console that is not in
  UTF-8 mode.
- **Fix**:
  1. In PowerShell, set UTF-8 for the current session:
     `$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'`
  2. Re-run `python cli_quiz.py`.
  3. If you are using `cmd.exe`, run `chcp 65001` first.

## App Fails To Start Because Quiz Data Cannot Be Loaded

- **Symptoms**: The desktop app shows a question-bank error dialog, or the CLI
  reports invalid quiz data on startup.
- **Cause**: `question_bank.json` is missing, malformed, or contains records
  that do not match the expected schema (`q`, `options`, `answer`,
  `explanation`, exactly four options, and an answer present in the options).
- **Fix**:
  1. Confirm the command is being run from the repository root.
  2. Open `question_bank.json` and check for malformed JSON.
  3. Run `python -m unittest -v`; the storage tests will usually pinpoint the
     failing shape assumption.

## History File Is Corrupt Or Contains Unexpected Data

- **Symptoms**: Startup fails while loading `exam_history.json`, or history
  entries render strangely after manual edits.
- **Cause**: `exam_history.json` must be a JSON list of attempt dictionaries.
- **Fix**:
  1. Back up the file if you need the current contents.
  2. Replace it with `[]` or remove it entirely; the app recreates history on
     the next completed attempt.
  3. Re-run the app and submit one test attempt to confirm persistence works.

## Merge Scaffold Rejects The Config

- **Symptoms**: `python merge_scaffold.py ...` exits with a config or JSON-list
  validation error.
- **Cause**: The scaffold expects a top-level JSON object with a non-empty
  `sources` list, and each source file must contain a JSON list.
- **Fix**:
  1. Start from `dataset_merge_config.template.json`.
  2. Verify every configured `path` exists.
  3. Make sure each source file contains a JSON list rather than an object.

## Environment Reset

If your local state becomes noisy or confusing:

1. Delete `__pycache__/` directories if they exist.
2. Remove or reset `exam_history.json` if persisted attempts are interfering
   with manual checks.
3. Re-run `git submodule update --init --recursive`.
4. Re-run `python -m unittest -v` and the `py_compile` command from
   `docs/COMMAND_REFERENCE.md`.
