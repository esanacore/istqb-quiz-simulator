# Workstation Setup

This project is a local-first Python desktop app with no external service
dependencies. Setup is mostly about using a recent Python interpreter, cloning
the repository with the Constitution submodule, and running the validation
commands from the repo root.

## Prerequisites

- Python `3.12` or later
- Git
- A UTF-8-capable terminal for the CLI simulator on Windows

No third-party packages are currently required for the desktop app, CLI, unit
tests, or merge scaffold.

## Clone The Repository

```bash
git clone --recurse-submodules git@github.com:esanacore/istqb-quiz-simulator.git
cd istqb-quiz-simulator
git submodule update --init --recursive
```

If you cloned without `--recurse-submodules`, run the final command afterward.

## Optional Virtual Environment

The repo does not currently ship a dependency lockfile, but using an isolated
environment keeps future tooling additions contained:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python --version
```

## First Validation Pass

Run these commands before changing code so the local baseline is known-good:

```powershell
python -m unittest -v
python -m py_compile ISTQBQuizApp.py cli_quiz.py exam_models.py exam_storage.py test_istqb_quiz_app.py merge_scaffold.py ui_layout.py
```

## Run The Desktop App

```powershell
python ISTQBQuizApp.py
```

The app loads `question_bank.json`, builds a randomized 40-question attempt,
and writes attempt history to `exam_history.json` after submission.

## Run The CLI App

The CLI prints ANSI-styled headers and explanations. On Windows PowerShell,
enable UTF-8 first to avoid `charmap` encoding errors:

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONUTF8='1'
python cli_quiz.py
```

If you prefer a persistent shell setting, run `chcp 65001` before launching the
CLI in `cmd.exe`.

## Use The Dataset Merge Scaffold

The merge scaffold is a generic JSON-to-JSON merge tool that writes merged
records, quarantined records, and an audit log:

```powershell
python merge_scaffold.py dataset_merge_config.template.json
```

Outputs are written to `merge_output/` unless the config overrides `output_dir`.

## Constitution Checks

When refreshing governance files or the pinned submodule, run the framework
checks from Git Bash:

```powershell
"C:\Program Files\Git\bin\bash.exe" constitution/scripts/check_compliance.sh --strict .
"C:\Program Files\Git\bin\bash.exe" constitution/scripts/check_version_alignment.sh
```
