# Changelog

All notable user-facing changes to this project should be documented in this file.

This project follows semantic versioning.

## Unreleased

### Added

- Added Engineering Constitution integration through the `constitution/` submodule.
- Added repository-level `TODO.md`, `CHANGELOG.md`, `CLAUDE.md`, `COPILOT_INSTRUCTIONS.md`, and `docs/adr/`.

### Changed

- Consolidated existing backlog guidance into the Engineering Constitution TODO format.

### Fixed

### Removed

### Security

## 0.1.0 - Initial Public Baseline

### Added

- Added ISTQB CTFL v4.0 desktop quiz simulator baseline.
- Added randomized 40-question exam attempts.
- Added sourced practice-question bank built from official sample materials.
- Added shuffled answer choices per attempt while preserving correctness.
- Added question navigator with direct jumping and state visibility.
- Added mark-for-review workflow.
- Added persistent attempt history with newest-first display, selective deletion, and clear-all controls.
- Added post-exam scoring, explanations, and source metadata review.
- Added terminal-first CLI exam flow with per-question review navigation.
- Added project documentation: `README.md`, `ARCHITECTURE.md`, `TESTING.md`, `TEST_PLAN.md`, `SOFTWARE_REQUIREMENTS.md`, `REQUIREMENTS_TRACEABILITY_MATRIX.md`, `CONTRIBUTING.md`, `AGENTS.md`, and `.github/copilot-instructions.md`.
- Added reusable project-improvement and dataset-integration toolkit documentation.
- Added merge scaffold and dataset merge configuration template.

### Changed

- Split UI, domain, and storage responsibilities into separate modules.
- Added Google-style docstrings across Python modules.

### Fixed

### Removed

### Security
