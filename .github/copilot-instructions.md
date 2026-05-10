# GitHub Copilot Instructions

## Repository Context

This project is a **Python/Tkinter desktop quiz simulator** for **ISTQB CTFL v4.0** practice.

Copilot should assume:

- the UI layer lives in `ISTQBQuizApp.py`
- domain logic lives in `exam_models.py`
- persistence and question-bank logic live in `exam_storage.py`
- generic dataset merge tooling lives in `merge_scaffold.py`
- tests use Python `unittest`
- question content belongs in `question_bank.json`, not embedded in Python

## Coding Guidance

- Prefer **small, explicit Python code** over clever abstractions.
- Keep UI concerns separate from scoring, navigation, and persistence logic.
- When adding business rules, implement them in `exam_models.py` first.
- When adding file-backed behavior, implement it in `exam_storage.py`.
- When adding dataset-integration behavior, implement it in `merge_scaffold.py` or a clearly related merge helper module.
- Preserve compatibility with local execution via:

```powershell
python ISTQBQuizApp.py
```

Preferred sequence for meaningful improvements:

1. inspect current files and docs
2. fix correctness issues
3. improve structure
4. add or update tests
5. update documentation
6. polish UI or developer experience

## Testing Guidance

When generating tests:

- use `unittest`
- test domain logic directly without requiring a live Tkinter window
- cover navigation, restart, scoring, and data validation paths
- cover merge normalization and conflict-resolution behavior when editing dataset tooling

## Documentation Guidance

- Use Google-style docstrings for Python code.
- Use Markdown for repository documentation.
- Keep comments concise and useful.
- Keep architecture, testing, and contribution docs aligned with the current code layout.

## Content Guidance

- Do not invent “official” ISTQB questions and present them as sourced unless provenance is known.
- Prefer source-tagged or traceable question content.
- Preserve correct-answer integrity when modifying question structures or randomization logic.
- Do not silently merge conflicting datasets without quarantine or audit behavior.
