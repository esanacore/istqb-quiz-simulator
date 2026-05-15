# Software Requirements Specification

## Purpose

This document defines the current software requirements for the ISTQB CTFL v4.0 quiz simulator and its reusable dataset-integration toolkit.

The requirements are intentionally testable. Each requirement has a stable identifier that can be referenced from the requirements traceability matrix.

## Scope

The product scope includes:

- a local Tkinter desktop quiz simulator
- an interactive command-line quiz simulator
- shared exam-state and persistence logic
- an external JSON question bank
- local attempt-history persistence
- a reusable dataset merge scaffold
- repo-level SQA, documentation, and AI-handoff guidance

The product is a study simulator. It is not an official ISTQB exam product.

## Requirement Status Values

- `Implemented`: behavior exists in the current codebase.
- `Partially Covered`: behavior exists but automated coverage is incomplete.
- `Planned`: intended future behavior.
- `Deferred`: intentionally outside the current scope.

## Functional Requirements

| ID | Requirement | Priority | Status |
| --- | --- | --- | --- |
| FR-001 | The system shall load questions from `question_bank.json` instead of hardcoding question content in Python. | Must | Implemented |
| FR-002 | The system shall reject an empty or non-list question bank. | Must | Implemented |
| FR-003 | The system shall reject question records that are not objects. | Must | Implemented |
| FR-004 | The system shall require each question to include `q`, `options`, `answer`, and `explanation`. | Must | Implemented |
| FR-005 | The system shall require exactly four answer options per question. | Must | Implemented |
| FR-006 | The system shall require the correct answer to match one of the answer options. | Must | Implemented |
| FR-007 | The system shall build randomized exam attempts from the question bank. | Must | Implemented |
| FR-008 | The system shall cap exam size at the available question-bank size when the bank is smaller than the requested exam size. | Must | Implemented |
| FR-009 | The system shall shuffle answer option order without changing the canonical correct answer text. | Must | Implemented |
| FR-010 | The system shall manage current-question navigation independent of the UI layer. | Must | Implemented |
| FR-011 | The system shall prevent navigation before the first question or after the last question. | Must | Implemented |
| FR-012 | The system shall persist one selected answer per question during an attempt, including a distinct no-selection state in the desktop UI. | Must | Implemented |
| FR-013 | The system shall allow clearing a selected answer. | Should | Implemented |
| FR-014 | The system shall track answered, unanswered, and marked-for-review counts. | Must | Implemented |
| FR-015 | The system shall allow toggling mark-for-review per question. | Should | Implemented |
| FR-016 | The system shall maintain a countdown timer for an exam attempt. | Must | Implemented |
| FR-017 | The system shall clamp remaining time at zero and ignore negative elapsed-time input. | Must | Implemented |
| FR-018 | The system shall finalize an attempt when submitted. | Must | Implemented |
| FR-019 | The system shall prevent answer, navigation, mark, and timer changes after submission. | Must | Implemented |
| FR-020 | The system shall calculate score, total, percentage, and pass/fail status after submission. | Must | Implemented |
| FR-021 | The system shall use a shared configurable pass threshold. | Must | Implemented |
| FR-022 | The system shall generate a detailed review report with answer, correct answer, explanation, and available metadata. | Must | Implemented |
| FR-023 | The desktop app shall save the active selected answer before timeout or manual submission scoring. | Must | Implemented |
| FR-024 | The desktop app shall provide direct question navigation through a question map. | Should | Implemented |
| FR-025 | The desktop app shall provide a history window. | Should | Implemented |
| FR-026 | The desktop history window shall display newest attempts first. | Should | Implemented |
| FR-027 | The desktop history window shall allow deleting selected history entries. | Should | Implemented |
| FR-028 | The desktop history window shall allow clearing all history after confirmation. | Should | Implemented |
| FR-029 | The CLI shall support answer entry by letter or number. | Must | Implemented |
| FR-030 | The CLI shall support next, previous, jump, mark, clear, summary, history, submit, restart, help, and quit commands. | Should | Implemented |
| FR-031 | The CLI shall display newest history attempts first. | Should | Implemented |
| FR-032 | The CLI shall allow clearing all history after confirmation. | Should | Implemented |
| FR-033 | The CLI shall provide per-question post-submit review navigation. | Should | Implemented |
| FR-034 | The CLI shall report quiz-data loading failures without an unhandled traceback. | Should | Implemented |
| FR-035 | The system shall normalize completed attempts into persisted history entries. | Must | Implemented |
| FR-036 | The system shall load missing history as an empty history list. | Must | Implemented |
| FR-037 | The system shall reject malformed history files that are not lists. | Must | Implemented |
| FR-038 | The system shall normalize history entry primitive values when loading. | Should | Implemented |
| FR-039 | The system shall keep runtime-generated history out of source control. | Should | Implemented |
| FR-040 | The system shall support responsive desktop wrap/layout calculations independent of Tkinter. | Should | Implemented |

## Dataset Toolkit Requirements

| ID | Requirement | Priority | Status |
| --- | --- | --- | --- |
| DT-001 | The merge scaffold shall load source records from JSON list files. | Must | Implemented |
| DT-002 | The merge scaffold shall reject source JSON payloads that are not lists. | Must | Implemented |
| DT-003 | The merge scaffold shall normalize raw records into a canonical merge record shape. | Must | Implemented |
| DT-004 | The merge scaffold shall preserve source name, source record ID, authority, raw payload, and transformation notes. | Must | Implemented |
| DT-005 | The merge scaffold shall generate normalized dedupe keys from record content. | Must | Implemented |
| DT-006 | The merge scaffold shall prefer higher-authority records during duplicate resolution. | Must | Implemented |
| DT-007 | The merge scaffold shall keep existing records when duplicate authority is equal. | Should | Implemented |
| DT-008 | The merge scaffold shall quarantine records with empty dedupe keys. | Must | Implemented |
| DT-009 | The merge scaffold shall export merged and quarantined records to JSON with transformation notes. | Must | Implemented |
| DT-010 | The merge scaffold shall export a human-readable audit log. | Should | Implemented |
| DT-011 | The merge scaffold shall reject non-object or source-less merge configs. | Must | Implemented |

## Quality Requirements

| ID | Requirement | Priority | Status |
| --- | --- | --- | --- |
| QR-001 | Business rules shall live in UI-independent modules where practical. | Must | Implemented |
| QR-002 | The app shall run locally without web infrastructure or third-party runtime dependencies. | Must | Implemented |
| QR-003 | The project shall preserve source traceability for question content. | Must | Implemented |
| QR-004 | Automated tests shall prefer deterministic, fast, UI-independent checks. | Must | Implemented |
| QR-005 | Meaningful code changes shall be verified with unit tests and compile checks. | Must | Implemented |
| QR-006 | Documentation shall be kept aligned with architecture and workflow changes. | Must | Implemented |
| QR-007 | Repository guidance shall instruct future agents to preserve question provenance and answer correctness. | Must | Implemented |
| QR-008 | Runtime-generated state and local IDE files shall be excluded from source control. | Should | Implemented |
| QR-009 | The repository shall provide specialist Copilot reviewer agents for UI, documentation, testing, provenance, and security review workflows. | Should | Implemented |
| QR-010 | The repository shall provide reusable review skills aligned with the project architecture and quality workflow. | Should | Implemented |
| QR-011 | The cloud-agent setup shall provision Python, Node.js, Tkinter, virtual-display, screenshot, and Python audit tooling for review sessions. | Should | Implemented |
| QR-012 | The repository shall provide automated GitHub Actions dependency monitoring through Dependabot. | Should | Implemented |

## Current Planned Requirements

| ID | Requirement | Priority | Status |
| --- | --- | --- | --- |
| PR-001 | The question bank should include topic metadata for every question. | Should | Planned |
| PR-002 | The question bank should include learning-objective metadata for every question. | Should | Planned |
| PR-003 | Review views should support source/topic/result filtering. | Should | Planned |
| PR-004 | The simulator should support weak-area study mode after topic metadata exists. | Could | Planned |
| PR-005 | The simulator should support configurable exam size and duration while preserving current defaults. | Could | Planned |
| PR-006 | The simulator should support history export to JSON or CSV. | Could | Planned |
| PR-007 | The desktop dialogs should be split into smaller view/controller classes if UI complexity continues to grow. | Could | Planned |

## Out Of Scope

| ID | Requirement | Reason |
| --- | --- | --- |
| OS-001 | The system shall not claim to be an official ISTQB exam product. | Legal/product boundary. |
| OS-002 | The system shall not require a hosted backend service. | Current target is local desktop/CLI use. |
| OS-003 | The system shall not silently invent or label unsourced question content as official. | Provenance and correctness risk. |
