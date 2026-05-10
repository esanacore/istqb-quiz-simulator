# Refactor Playbook

## Purpose

This playbook describes a practical way to refactor a working-but-messy project without losing momentum.

---

## 1. Identify The Current Responsibilities

Before moving code, identify:

- UI or framework code
- domain logic
- persistence code
- validation code
- reporting or formatting code

If everything is mixed together, that is the problem to solve.

---

## 2. Move Logic By Responsibility, Not By Size

Do not split files randomly just because they are large.

Split by ownership:

- model/state module
- storage/validation module
- UI/controller module

This creates seams that are meaningful.

---

## 3. Preserve External Behavior

A good refactor should keep the user-visible behavior stable unless you are also intentionally fixing bugs.

During refactor:

- keep entry points working
- keep commands the same when possible
- keep data formats stable unless you have a migration plan

---

## 4. Extract The Most Testable Logic First

Good first extraction targets:

- scoring rules
- navigation/state transitions
- validation rules
- report generation
- file-backed normalization

These are the parts that benefit most immediately from unit testing.

---

## 5. Add Tests Around The New Boundaries

Once logic moves into cleaner modules:

- test the domain model directly
- test storage helpers directly
- avoid over-relying on UI tests for logic validation

The refactor is more valuable if it increases test coverage.

---

## 6. Clean Up Naming And Docstrings

After the refactor works:

- improve module names
- improve function names
- add Google-style docstrings
- reduce duplicated logic

Refactoring without naming cleanup leaves a half-finished result.

---

## 7. Verify At Each Stage

After each structural step:

- run tests
- run compile checks
- verify imports still work
- verify the app still starts

This prevents large refactors from becoming hard to debug.

---

## 8. End State

A good refactor should leave the project with:

- clearer ownership
- less duplication
- thinner UI layer
- stronger tests
- docs that match the new structure
