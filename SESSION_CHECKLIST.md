# Session Checklist

## Purpose

Use this checklist at the start and end of a project-improvement session.

It is intended to keep work practical, sequenced, and verifiable.

---

## 1. Intake

- identify the project goal
- identify the current user pain or problem
- inspect top-level files and folders
- read the main entry point
- read the current readme or notes
- identify whether source control metadata exists
- identify whether tests already exist

---

## 2. Baseline

- summarize what the project does today
- identify the files that own the core behavior
- identify the biggest correctness risks
- identify whether the project is prototype-level or maintainable
- run a minimal sanity check if feasible

---

## 3. First Improvements

- fix high-risk behavioral issues first
- stabilize lifecycle/state management
- externalize hardcoded data if needed
- avoid adding scale to unstable behavior

---

## 4. Structural Improvement

- identify logic that should move out of the UI or framework layer
- isolate storage and validation code
- isolate domain logic and state transitions
- keep the public entry point simple

---

## 5. Verification

- run tests
- run syntax/compile checks
- verify startup behavior
- verify changed workflows manually if needed

---

## 6. Documentation

- update or replace the readme if outdated
- add architecture/testing/contribution docs as needed
- add agent or copilot guidance if AI-assisted maintenance is likely
- ensure docs reflect the current structure, not the old one

---

## 7. Hygiene

- add or update `.gitignore`
- keep generated files out of version control
- remove obsolete files when a new canonical replacement exists

---

## 8. Repository Readiness

- add CI workflow if the repo is becoming shareable
- add issue templates if future iteration is expected
- prepare release notes if the current state is a real milestone
- verify repo metadata guidance is ready for manual GitHub setup

---

## 9. AI Handoff Readiness

- update agent instructions
- update Copilot instructions
- add a bounded backlog of safe next tasks
- ensure docs tell future assistants where logic, data, and tests belong

---

## 10. End-Of-Session Closeout

- summarize the current state
- note what was verified
- identify the next highest-value step
- leave the repo cleaner than it started
