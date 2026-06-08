# 🧠 ISTQB CTFL Quiz Simulator

A desktop exam simulator for **ISTQB Certified Tester Foundation Level (CTFL v4.0)** practice, built with **Python + Tkinter**.

It is designed to feel closer to a real exam session than a simple flashcard app: timed attempts, randomized 40-question exams, answer shuffling, mark-for-review workflow, attempt history, and detailed post-exam explanations sourced from official sample materials.

## Engineering Constitution

This repository follows the shared Engineering Constitution through the `constitution/` Git submodule.

The constitution provides project-wide standards for:

- AI-assisted development workflow
- testing expectations
- documentation quality
- TODO and changelog maintenance
- security review
- architecture decision records

Project-specific guidance remains in [AGENTS.md](AGENTS.md), [ARCHITECTURE.md](ARCHITECTURE.md), [TESTING.md](TESTING.md), and the SQA artifacts listed below.

For future work:

1. Read [AGENTS.md](AGENTS.md).
2. Read the relevant files in `constitution/`.
3. Update [TODO.md](TODO.md) when roadmap items are discovered or completed.
4. Update [CHANGELOG.md](CHANGELOG.md) for user-facing changes.
5. Record major design decisions in [docs/adr/](docs/adr/).

## ✨ Features

- **Exam-length attempts**: each session builds a randomized `40`-question exam.
- **Large sourced bank**: the app currently uses a larger pool of official-sample-derived questions instead of recycling the same fixed set.
- **Shuffled answer order**: choices are reshuffled per attempt while preserving correctness.
- **Question navigator**: jump directly to any question from the sidebar map.
- **Mark for review**: visually flag questions and revisit them before submission.
- **Persistent history**: store past attempts locally, review newest attempts first, and clear individual or all entries when needed.
- **Results review**: see score, pass/fail status, explanations, and source metadata after each exam.
- **Interactive CLI mode**: run a terminal-first exam flow with navigation commands, history access, ANSI-styled output, and per-question review navigation.
- **Tkinter desktop UI**: lightweight, local, no web stack required.

## 🖼️ What The App Tries To Simulate

This project is intended to reproduce the **pressure and workflow** of an actual certification practice session:

- `60` minute timer
- `40` randomized questions
- progress visibility
- unanswered/marked submission guard
- direct question navigation
- detailed review after completion

It is a **study simulator**, not an official ISTQB exam product.

## 🏗️ Project Structure

```text
practiceISTQB/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── COPILOT_INSTRUCTIONS.md
├── TODO.md
├── CHANGELOG.md
├── constitution/
├── docs/
│   └── adr/
├── ARCHITECTURE.md
├── TESTING.md
├── TEST_PLAN.md
├── SOFTWARE_REQUIREMENTS.md
├── REQUIREMENTS_TRACEABILITY_MATRIX.md
├── CONTRIBUTING.md
├── RELEASE_NOTES_v0.1.0.md
├── PROJECT_EVOLUTION_FRAMEWORK.md
├── SESSION_CHECKLIST.md
├── AI_COLLABORATION_GUIDE.md
├── REFACTOR_PLAYBOOK.md
├── DATASET_INTEGRATION_PLAYBOOK.md
├── MERGE_CHECKLIST.md
├── DATASET_SCHEMA_TEMPLATE.md
├── MERGE_CLI_GUIDE.md
├── COPILOT_REVIEW_STACK.md
├── ISTQBQuizApp.py
├── cli_quiz.py
├── exam_models.py
├── exam_storage.py
├── merge_scaffold.py
├── ui_layout.py
├── dataset_merge_config.template.json
├── question_bank.json
├── exam_history.json        # created at runtime
├── test_istqb_quiz_app.py
├── istqb_ctfl_practice_exam_links.rtf
├── .vscode/
│   └── mcp.json
└── .github/
    ├── agents/
    ├── copilot-instructions.md
    ├── dependabot.yml
    ├── ISSUE_TEMPLATE/
    ├── skills/
    └── workflows/
```

### Core Modules

- [ISTQBQuizApp.py](ISTQBQuizApp.py)
  UI/orchestration layer. Owns Tkinter widgets, rendering, and user interaction.
- [cli_quiz.py](cli_quiz.py)
  Interactive command-line interface built on the same exam and storage layers.
- [exam_models.py](exam_models.py)
  Pure exam-domain logic such as navigation, answers, marks, scoring, restart, and report generation.
- [exam_storage.py](exam_storage.py)
  Question-bank loading, history-entry normalization, history persistence, and randomized exam assembly.
- [ui_layout.py](ui_layout.py)
  Responsive wrap and layout helpers for the Tkinter app.
- [test_istqb_quiz_app.py](test_istqb_quiz_app.py)
  Unit and integration-style tests for storage, domain, CLI helper, responsive-layout, and merge-toolkit behavior.

### SQA Artifacts

- [SOFTWARE_REQUIREMENTS.md](SOFTWARE_REQUIREMENTS.md)
  Testable functional, dataset-toolkit, quality, planned, and out-of-scope requirements.
- [REQUIREMENTS_TRACEABILITY_MATRIX.md](REQUIREMENTS_TRACEABILITY_MATRIX.md)
  Requirements-to-test traceability, manual regression checks, and known coverage gaps.
- [TEST_PLAN.md](TEST_PLAN.md)
  Test levels, techniques, entry/exit criteria, test data rules, and defect-reporting expectations.
- [TESTING.md](TESTING.md)
  Current automated coverage summary and verification commands.

### Project Ops Toolkit

- [PROJECT_EVOLUTION_FRAMEWORK.md](PROJECT_EVOLUTION_FRAMEWORK.md)
  Reusable framework for improving rough or partially complete software projects.
- [SESSION_CHECKLIST.md](SESSION_CHECKLIST.md)
  Practical start-to-finish checklist for structured improvement sessions.
- [AI_COLLABORATION_GUIDE.md](AI_COLLABORATION_GUIDE.md)
  Patterns for working effectively with AI coding assistants.
- [REFACTOR_PLAYBOOK.md](REFACTOR_PLAYBOOK.md)
  Pragmatic refactor sequence for separating UI, domain, and persistence layers.

### Dataset Toolkit

- [DATASET_INTEGRATION_PLAYBOOK.md](DATASET_INTEGRATION_PLAYBOOK.md)
  Reusable method for combining multiple partial datasets into one trustworthy corpus.
- [MERGE_CHECKLIST.md](MERGE_CHECKLIST.md)
  Operational checklist for dataset normalization, conflict handling, and validation.
- [DATASET_SCHEMA_TEMPLATE.md](DATASET_SCHEMA_TEMPLATE.md)
  Canonical schema starter for merged datasets.
- [MERGE_CLI_GUIDE.md](MERGE_CLI_GUIDE.md)
  Usage guide for the generic merge CLI workflow.
- [merge_scaffold.py](merge_scaffold.py)
  Config-driven merge scaffold for ingest, normalize, dedupe, and export workflows.
- [dataset_merge_config.template.json](dataset_merge_config.template.json)
  Example config for running the merge scaffold.
- [RELEASE_NOTES_v0.1.0.md](RELEASE_NOTES_v0.1.0.md)
  Suggested notes for the initial tagged release.

## 🚀 Getting Started

### Requirements

- Python `3.12` or later

Use `python3` in the commands below if your environment does not expose `python`.

### Run The App

```powershell
python ISTQBQuizApp.py
```

### Run The CLI

```powershell
python cli_quiz.py
```

### Run Tests

```powershell
python -m unittest -v
```

### Compile Check

```powershell
python -m py_compile ISTQBQuizApp.py cli_quiz.py exam_models.py exam_storage.py test_istqb_quiz_app.py merge_scaffold.py ui_layout.py
```

## 🧪 Testing Strategy

The current automated tests focus on **logic that should not depend on Tkinter widgets**:

- question-bank validation
- exam-question randomization and answer preservation
- history load/save behavior, newest-first ordering, and normalized history records
- exam navigation and answer state
- mark-for-review behavior
- shared pass-threshold behavior
- timer countdown reduction
- restart/reset logic
- score and report generation
- CLI parsing, rendering, and review helpers
- responsive layout calculations
- merge-toolkit normalization, conflict-resolution, quarantine, and export helpers
- integration-style exam assembly, answering, submission, and history-entry creation

The UI layer is intentionally thinner than before, with state delegated into `ExamSession` so the most important behavior can be tested without GUI automation.

See [TEST_PLAN.md](TEST_PLAN.md) and [REQUIREMENTS_TRACEABILITY_MATRIX.md](REQUIREMENTS_TRACEABILITY_MATRIX.md) for the formal SQA view.

## 🧰 Reusable Frameworks

This repository now includes a small **project-operations toolkit** that can be reused outside this app:

- project review and evolution framework
- refactor playbook
- AI collaboration guide
- dataset integration methodology
- dataset merge schema/checklist/CLI scaffold

That toolkit is intended to make the patterns used in this repo transferable to future software projects and data-integration efforts.

## 🤖 GitHub Automation

The repository includes a GitHub Actions workflow for:

- Python compile checks
- unit test execution on pushes and pull requests

It also includes automated GitHub Actions dependency monitoring via `.github/dependabot.yml`.

It also includes issue templates for:

- bug reports
- feature requests

It also includes a repo-scoped Copilot review stack for desktop UI, docs, testing, and security review:

- workspace MCP configuration in [.vscode/mcp.json](.vscode/mcp.json)
- specialist reviewer agents in [.github/agents](.github/agents)
- reusable review skills in [.github/skills](.github/skills)
- cloud-agent setup in [.github/workflows/copilot-setup-steps.yml](.github/workflows/copilot-setup-steps.yml)

See [COPILOT_REVIEW_STACK.md](COPILOT_REVIEW_STACK.md) for setup and usage.

## 📚 Question Sources

The question bank is built from **adapted questions based on official ISTQB sample-exam materials** referenced in:

- [istqb_ctfl_practice_exam_links.rtf](istqb_ctfl_practice_exam_links.rtf)

Those source references are also preserved in `question_bank.json` and shown in the post-exam review output.

## 🎯 Why This Exists

This tool was created to help bridge the gap between:

- **real-world engineering intuition**
- and the more formal **ISTQB exam mindset**

Practical software experience helps, but the CTFL exam still expects candidates to be precise about terminology, process, and standard testing techniques.

## 🛣️ Suggested Next Steps

- add topic and learning-objective metadata to every question
- introduce weak-area or focused-study mode
- add import tooling for expanding the question bank safely
- split the Tkinter UI further into smaller view components if the interface grows

## ⚠️ Disclaimer

This repository is for **educational practice use only** and should be used alongside the official ISTQB CTFL syllabus and sample exams.
