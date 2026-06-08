# Copilot Instructions

This repository follows the Engineering Constitution.

## Context Files

Use these files as primary context:

- `constitution/CONSTITUTION.md`
- `constitution/AI_WORKFLOW.md`
- `constitution/TESTING.md`
- `constitution/DOCUMENTATION.md`
- `constitution/SECURITY.md`
- `constitution/ARCHITECTURE.md`
- `README.md`
- `TODO.md`
- `CHANGELOG.md`
- `AGENTS.md`
- `ARCHITECTURE.md`
- `TESTING.md`
- `TEST_PLAN.md`
- `REQUIREMENTS_TRACEABILITY_MATRIX.md`
- `COPILOT_TASK_BACKLOG.md`

## Development Standards

- Prefer existing project conventions.
- Keep changes focused and maintainable.
- Keep domain logic in `exam_models.py` and storage/loading logic in `exam_storage.py` when practical.
- Preserve question provenance and answer correctness.
- Add tests for new behavior.
- Add regression tests for bug fixes.
- Update documentation for changed behavior, setup, architecture, or operations.
- Update TODO.md with discovered follow-up work.
- Update CHANGELOG.md for user-facing changes.
- Update requirements traceability when requirements or tests change.
- Avoid adding unnecessary dependencies.
- Consider security, observability, and release impact.
