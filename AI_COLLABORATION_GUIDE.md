# AI Collaboration Guide

## Purpose

Use this document when working with an AI coding assistant on an existing or growing project.

The goal is to get useful, structured outcomes instead of fragmented edits.

---

## 1. Frame The Request Clearly

A strong request includes:

- what the project is
- what file or area to start with
- what kind of outcome you want
- whether you want review, implementation, refactor, docs, or tests

Examples:

- review this repo and tell me where I left off
- stabilize the current behavior before adding new features
- refactor this into model, storage, and UI modules
- document this repo to a professional standard

---

## 2. Ask For Reality First

Before asking for changes, ask the assistant to:

- inspect the repo
- read the readme
- identify the architecture
- summarize the current state

This avoids low-quality help based on assumptions.

---

## 3. Use A Good Change Order

A strong default order is:

1. inspect
2. summarize
3. fix correctness issues
4. improve structure
5. add tests
6. improve UI
7. improve docs

If the assistant starts with polish before stability, redirect it.

---

## 4. Ask For The Work To Be Carried Through

Useful phrasing:

- implement it, then verify it
- make the change and run tests
- don’t stop at analysis
- continue until the task is actually complete

This reduces partial or advisory-only answers.

---

## 5. Keep The Assistant Focused On Boundaries

Ask the assistant to separate:

- UI
- domain logic
- storage/persistence
- tests
- documentation

This creates maintainable seams instead of monolithic edits.

---

## 6. Ask For Verification Explicitly

Always ask for:

- compile checks
- unit test runs
- summary of what passed or failed

Good prompt pattern:

> Make the change, run the tests, and tell me what still needs attention.

---

## 7. Use The Assistant For Documentation, Not Just Code

AI is particularly useful for:

- readmes
- architecture docs
- contribution guides
- testing docs
- repo-specific agent instructions

But require the docs to match the actual repo structure, not generic templates.

---

## 8. Use AI Carefully With Source Material

When the project depends on trusted datasets, specs, standards, or exams:

- ask the assistant to preserve provenance
- distinguish sourced content from inferred content
- avoid presenting unsourced content as official
- ask for validation rules around imported data

---

## 9. Reusable Prompt Pattern

You can reuse this prompt shape in many projects:

> Review this repository starting with the readme and main entry point.  
> Summarize the current state, identify the highest-risk issues, fix the core structural or behavioral problems first, add tests for the extracted logic, and then improve the documentation so it reflects the actual architecture. Verify changes before finishing.

---

## 10. Collaboration Principles

- ask for inspection before change
- ask for implementation, not just suggestions
- ask for verification
- ask for structure, not just feature work
- ask for docs that match reality
