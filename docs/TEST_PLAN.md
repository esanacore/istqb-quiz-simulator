# Docs Test Plan

This document is the `docs/` entry point for repository verification. The
canonical detailed test strategy remains the root-level
[`TEST_PLAN.md`](../TEST_PLAN.md) and [`TESTING.md`](../TESTING.md).

## Primary Automated Checks

```powershell
python -m unittest -v
python -m py_compile ISTQBQuizApp.py cli_quiz.py exam_models.py exam_storage.py test_istqb_quiz_app.py merge_scaffold.py ui_layout.py
```

## Scope Covered

- Quiz-domain rules and scoring
- Question-bank validation and history persistence
- Desktop smoke tests for selected Tkinter flows
- CLI helper and session-flow behavior
- Dataset merge scaffold normalization and duplicate resolution
- Responsive layout helper logic

## Governance Checks

When documentation or Constitution files change, add:

```powershell
"C:\Program Files\Git\bin\bash.exe" constitution/scripts/check_compliance.sh --strict .
"C:\Program Files\Git\bin\bash.exe" constitution/scripts/check_version_alignment.sh
```

## Known Gaps

- There is no dedicated GUI end-to-end harness beyond the existing lightweight
  Tkinter smoke tests.
- The CLI still depends on a UTF-8-capable console on Windows.
- Product requirements and traceability remain in root-level legacy files
  (`SOFTWARE_REQUIREMENTS.md` and `REQUIREMENTS_TRACEABILITY_MATRIX.md`) rather
  than the Constitution's preferred `docs/` paths.
