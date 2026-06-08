# Engineering Constitution Adoption Report

Project: 🧠 ISTQB CTFL Quiz Simulator

Project path: `/home/eric/Repos/istqb-quiz-simulator`

Constitution source: `https://github.com/esanacore/engineering-constitution.git`

## What Happened

The bootstrap script installed the Engineering Constitution in a non-destructive mode.

Existing project files were not overwritten. When a target file already existed, the matching constitution template was copied into `.constitution-bootstrap/templates/` so maintainers can compare and merge manually.

## Current Governance Files

- [x] README.md exists
- [x] AGENTS.md exists
- [x] CLAUDE.md exists
- [x] COPILOT_INSTRUCTIONS.md exists
- [x] TODO.md exists
- [x] CHANGELOG.md exists
- [x] docs/adr exists

## Files Written

- `CLAUDE.md`
- `COPILOT_INSTRUCTIONS.md`
- `TODO.md`
- `CHANGELOG.md`
- `docs/adr/0001-record-architecture-decisions.md`

## Existing Files Preserved

- `AGENTS.md`
- `README.md`

## Integration Follow-Up Applied

After the initial non-destructive bootstrap, existing repository context was folded into the Engineering Constitution structure:

- `AGENTS.md` now includes required constitution reading while preserving the project-specific ISTQB simulator rules.
- `README.md` now explains how the constitution applies to this repository.
- `TODO.md` now consolidates the existing Copilot backlog into constitution categories.
- `CHANGELOG.md` now incorporates the existing v0.1.0 release notes and records the constitution adoption under Unreleased.
- `CLAUDE.md` and `COPILOT_INSTRUCTIONS.md` now point to this project's architecture, testing, traceability, and backlog docs.
- `docs/adr/0001-record-architecture-decisions.md` now documents ADR usage for this repository.

## Detected Project Signals

- GitHub Actions workflows: `.github/workflows`

## Recommended Merge Steps

1. Compare existing files with templates in `.constitution-bootstrap/templates/`.
2. Merge relevant Engineering Constitution sections into existing project files.
3. Customize generated placeholders in TODO.md, CHANGELOG.md, README.md, and ADRs.
4. Commit `.gitmodules`, the `constitution` submodule reference, generated files, and any merged documentation changes.
5. Keep or remove `.constitution-bootstrap/` depending on whether the adoption report is useful to the project.

## Suggested Agent Context

Add or verify these instructions in AGENTS.md:

- Read `constitution/CONSTITUTION.md` before making changes.
- Read `README.md`, `TODO.md`, and `CHANGELOG.md` for project context.
- Update tests, docs, TODO.md, and CHANGELOG.md when relevant.
- Record major design decisions in `docs/adr/`.
