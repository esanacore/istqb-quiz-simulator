# Contributing

## Scope

This repository is a local study tool for **ISTQB CTFL v4.0** practice. Contributions should improve one or more of the following:

- correctness
- maintainability
- testability
- sourced question quality
- usability

## Development Priorities

When making changes, prefer this order:

1. correctness
2. testability
3. maintainability
4. UI clarity
5. feature expansion

## Code Standards

- Use **Python** with clear, explicit logic.
- Keep UI concerns in [ISTQBQuizApp.py](ISTQBQuizApp.py).
- Keep CLI presentation concerns in [cli_quiz.py](cli_quiz.py).
- Keep domain logic in [exam_models.py](exam_models.py).
- Keep persistence and exam assembly logic in [exam_storage.py](exam_storage.py).
- Use **Google-style docstrings** for modules, classes, and non-trivial functions.
- Prefer concise, high-signal comments over excessive inline narration.

## Question Content Rules

- Do not hardcode question content in Python files.
- Add or modify question content in [question_bank.json](question_bank.json).
- Preserve source traceability where possible.
- Do not present unsourced content as official ISTQB material.
- Preserve answer correctness when randomization or structure changes are made.

## Testing Expectations

Requirements and tests should stay traceable. When adding or materially changing behavior, update:

- [SOFTWARE_REQUIREMENTS.md](SOFTWARE_REQUIREMENTS.md)
- [REQUIREMENTS_TRACEABILITY_MATRIX.md](REQUIREMENTS_TRACEABILITY_MATRIX.md)
- [TEST_PLAN.md](TEST_PLAN.md) if the verification approach changes

If you change logic in:

- `exam_models.py`
- `exam_storage.py`
- scoring
- history behavior
- CLI command/review behavior
- question assembly
- merge-toolkit behavior

you should update or add unit tests in [test_istqb_quiz_app.py](test_istqb_quiz_app.py).

## Verification Checklist

Before considering work complete, run:

```powershell
python -m unittest -v
python -m py_compile ISTQBQuizApp.py cli_quiz.py exam_models.py exam_storage.py test_istqb_quiz_app.py merge_scaffold.py ui_layout.py
```

## Suggested Contribution Areas

- expand question metadata with topic and learning objective fields
- improve study analytics or weak-area review modes
- add import tooling for source-backed question expansion
- strengthen the reusable merge toolkit for future projects
- further decompose the Tkinter UI into smaller view/controller units
- improve history exploration and filtering

## Pull Request Guidance

If this repo is moved into a normal Git workflow, a good change should include:

- a clear problem statement
- a short implementation summary
- notes on tests run
- screenshots for meaningful UI changes
