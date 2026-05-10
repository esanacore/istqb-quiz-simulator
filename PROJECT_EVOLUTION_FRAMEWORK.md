# Project Evolution Framework

## Purpose

This document captures a reusable framework for taking a rough or partially complete software project and improving it systematically over a working session.

It is based on a practical progression that moved a small prototype into a more maintainable, testable, documented, and product-like repository.

Use this as a **generic execution pattern** for future projects.

---

## 1. Start With Reality, Not Assumptions

Before making changes:

- inspect the repository contents
- read the main entry point
- read the existing README or equivalent project notes
- identify the actual current architecture
- verify whether source control metadata exists
- run a minimal sanity check if possible

Goal:

- understand where the project actually is
- identify what is working
- identify what is fragile
- determine the right next step instead of guessing

---

## 2. Reconstruct The Current State

Distill the project into a small set of truths:

- what the project does today
- what files matter most
- what features already exist
- what is prototype-level versus production-like
- what obvious bugs, gaps, or architectural issues exist

This should produce a practical “where you left off” view.

---

## 3. Stabilize Core Behavior Before Expanding Features

Before adding more content, UI, or complexity:

- fix lifecycle bugs
- fix state-management issues
- eliminate double-trigger or timing problems
- lock down submission/finalization behavior
- make failure and edge-case behavior explicit

Principle:

Do not scale broken behavior.

---

## 4. Separate Data From Logic Early

If content or configuration is hardcoded:

- move it into external files such as JSON, CSV, YAML, or TOML
- validate those files at load time
- fail clearly when external data is malformed

Benefits:

- easier content expansion
- cleaner code
- better maintainability
- easier sourcing and auditing

---

## 5. Prefer Source-Backed Content Over Invented Content

When a project depends on domain knowledge, reference material, or external correctness:

- use authoritative sources
- preserve provenance
- distinguish adapted content from original content
- avoid passing off invented material as sourced material

If copyright applies:

- adapt and summarize when needed
- avoid verbatim duplication

---

## 6. Scale The Product In A Realistic Order

A useful sequence for expanding a project is:

1. stabilize core behavior
2. externalize data
3. expand content or coverage
4. randomize or vary usage patterns if applicable
5. improve state visibility and user workflow
6. improve persistence and history
7. improve visual design
8. improve testability
9. improve documentation

This order usually produces better outcomes than leading with polish or feature count.

---

## 7. Add Variation Without Losing Correctness

When building repeated-use tools, add variety safely:

- randomize selected items from a larger pool
- shuffle presentation order when correctness can be preserved
- ensure all derived state still references the same canonical answer
- validate that randomization does not corrupt the data model

Variation should improve usefulness without reducing trust.

---

## 8. Add Persistent User-Oriented Features Thoughtfully

Good persistence candidates include:

- history
- preferences
- progress
- saved state

When adding them:

- use explicit file-backed storage
- keep the schema simple
- support deletion or reset
- reflect persisted state in the UI

Principle:

Persistence should be inspectable and reversible.

---

## 9. Improve UI Only After Workflow Is Solid

Once the functional behavior is stable:

- improve visual hierarchy
- improve spacing and readability
- add progress indicators
- add direct navigation for multi-step experiences
- make state visible at a glance
- style auxiliary windows and dialogs consistently

UI improvements should make the product easier to use, not just nicer to look at.

---

## 10. Extract Domain Logic Out Of The UI

A common turning point is moving from:

- one large UI file

to:

- UI layer
- domain/state layer
- storage/persistence layer

Benefits:

- clearer responsibilities
- easier unit testing
- easier maintenance
- less brittle feature changes

Rule of thumb:

If a rule can be tested without a window, it probably should not live in the UI layer.

---

## 11. Add Tests At The Boundaries That Matter Most

Start with tests that protect trust-critical behavior:

- data validation
- state transitions
- scoring or calculations
- persistence
- restart/reset behavior
- report generation

Prefer:

- fast tests
- deterministic tests
- non-UI tests

Do not force UI automation first if the core logic can be isolated more cheaply.

---

## 12. Modularize When The Structure Is Clear

Do not split files randomly.

Split after responsibilities are visible. A practical pattern is:

- `ui` module for rendering and user interaction
- `models` module for domain state and rules
- `storage` module for file and persistence logic
- `tests` module for automated validation

Modularization should reduce duplication and clarify ownership.

---

## 13. Raise Documentation Quality As The Code Matures

Once the structure stabilizes:

- replace ad hoc notes with a real `README.md`
- add architecture documentation
- add testing documentation
- add contribution guidance
- add agent/copilot instructions if AI-assisted work is expected

Documentation should reflect:

- what the project is
- how it is organized
- how to run it
- how to test it
- how to extend it safely

---

## 14. Standardize Comments And Docstrings

When the project reaches a maintainable baseline:

- add module docstrings
- add class docstrings
- add function docstrings for non-trivial behavior
- use a consistent format such as Google style
- keep comments high-signal

Avoid:

- narrating obvious code
- commenting every line
- using comments to compensate for unclear structure

---

## 15. Add Repository Hygiene

Before closing out a session:

- add `.gitignore`
- ignore caches and generated files
- ignore local test scratch data
- ignore runtime-generated state when appropriate

This keeps the repository cleaner and easier to manage over time.

---

## 16. Verify At Each Meaningful Stage

After important changes:

- run syntax/compile checks
- run tests
- validate file layout
- confirm that refactors did not break startup behavior

Verification should happen continuously, not only at the end.

---

## 17. Use This As A Repeatable Session Pattern

For future projects, a strong default session sequence is:

1. inspect repo
2. read current docs and entry point
3. summarize current state
4. fix high-risk functional issues
5. externalize data/config
6. expand source-backed content or capability
7. improve UX/workflow
8. add persistence/history if useful
9. extract domain logic from UI or framework code
10. add unit tests
11. modularize
12. improve docs
13. add repo hygiene
14. rerun verification

---

## 18. Guiding Principles

- **Work from current truth, not idealized assumptions.**
- **Stabilize before scaling.**
- **Separate content, logic, and UI.**
- **Prefer source-backed correctness.**
- **Extract testable logic early.**
- **Polish after workflow works.**
- **Document once structure is real.**
- **Leave the repo cleaner than you found it.**

---

## 19. How To Use This Document

For a future project, you can use this file in three ways:

### As a kickoff checklist

Use sections 1 through 4 before changing code.

### As an execution order

Use sections 5 through 16 as the recommended progression for evolving the project.

### As an AI or collaborator brief

Give this file to a coding assistant or collaborator and ask them to:

- follow the sequence pragmatically
- avoid skipping stability and testability
- document structural changes as they go

---

## 20. Optional Future Companion Docs

If you want to turn this into a fuller reusable methodology, add:

- `SESSION_CHECKLIST.md`
- `REFACTOR_PLAYBOOK.md`
- `AI_COLLABORATION_GUIDE.md`
- `REPO_BOOTSTRAP_TEMPLATE.md`

That would turn this from a framework document into a reusable project-operations toolkit.
