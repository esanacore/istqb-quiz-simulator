# Operations

This repository is a local-only desktop/CLI study tool. It does not expose a
network service or require production infrastructure, but it still benefits
from a minimal operations posture for local support and release hygiene.

## Runtime Expectations

- Run commands from the repository root so relative paths to
  `question_bank.json` and `exam_history.json` resolve correctly.
- Keep the question bank in UTF-8 JSON.
- Treat `exam_history.json` as local runtime state rather than a source asset.

## Local Validation Path

Before publishing changes:

```powershell
python -m unittest -v
python -m py_compile ISTQBQuizApp.py cli_quiz.py exam_models.py exam_storage.py test_istqb_quiz_app.py merge_scaffold.py ui_layout.py
```

For governance changes, also run:

```powershell
"C:\Program Files\Git\bin\bash.exe" constitution/scripts/check_compliance.sh --strict .
"C:\Program Files\Git\bin\bash.exe" constitution/scripts/check_version_alignment.sh
```

## Failure Recovery

- If quiz history is corrupted, back it up and replace `exam_history.json` with
  `[]` or delete it so the app can recreate it.
- If the CLI fails to render on Windows, set
  `$env:PYTHONIOENCODING='utf-8'` and `$env:PYTHONUTF8='1'`.
- If the Constitution submodule is missing, run
  `git submodule update --init --recursive`.

## Release Notes

- Update `README.md`, `CHANGELOG.md`, and any affected governance docs together.
- Because the app is local-only, operational regressions are usually packaging,
  data-shape, or console-encoding problems rather than deployment failures.
