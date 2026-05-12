# Release Notes: v0.1.0

## Initial Public Baseline

This release establishes the first complete baseline for the project as both:

- an **ISTQB CTFL v4.0 desktop quiz simulator**
- a **reusable project-improvement and dataset-integration toolkit**

## Simulator Highlights

- randomized `40`-question exam attempts
- sourced practice-question bank built from official sample materials
- shuffled answer choices per attempt
- question navigator with direct jumping and state visibility
- mark-for-review workflow
- persistent attempt history with newest-first display, selective deletion, and clear-all controls
- post-exam scoring, explanations, and source metadata review
- terminal-first CLI exam flow with per-question review navigation

## Codebase Improvements

- UI/domain/storage responsibilities split into separate modules
- Google-style docstrings added across Python modules
- 41 automated tests for domain, storage, CLI helper, merge-toolkit, layout, and integration-style exam flow logic
- `.gitignore` added for local/runtime artifacts

## Documentation Additions

- `README.md`
- `ARCHITECTURE.md`
- `TESTING.md`
- `TEST_PLAN.md`
- `SOFTWARE_REQUIREMENTS.md`
- `REQUIREMENTS_TRACEABILITY_MATRIX.md`
- `CONTRIBUTING.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`

## Toolkit Additions

- `PROJECT_EVOLUTION_FRAMEWORK.md`
- `SESSION_CHECKLIST.md`
- `AI_COLLABORATION_GUIDE.md`
- `REFACTOR_PLAYBOOK.md`
- `DATASET_INTEGRATION_PLAYBOOK.md`
- `MERGE_CHECKLIST.md`
- `DATASET_SCHEMA_TEMPLATE.md`
- `MERGE_CLI_GUIDE.md`
- `merge_scaffold.py`
- `dataset_merge_config.template.json`
