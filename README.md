# 🧠 ISTQB CTFL Quiz Simulator

A desktop exam simulator for **ISTQB Certified Tester Foundation Level (CTFL v4.0)** practice, built with **Python + Tkinter**.

It is designed to feel closer to a real exam session than a simple flashcard app: timed attempts, randomized 40-question exams, answer shuffling, mark-for-review workflow, attempt history, and detailed post-exam explanations sourced from official sample materials.

## ✨ Features

- **Exam-length attempts**: each session builds a randomized `40`-question exam.
- **Large sourced bank**: the app currently uses a larger pool of official-sample-derived questions instead of recycling the same fixed set.
- **Shuffled answer order**: choices are reshuffled per attempt while preserving correctness.
- **Question navigator**: jump directly to any question from the sidebar map.
- **Mark for review**: visually flag questions and revisit them before submission.
- **Persistent history**: store past attempts locally and remove individual history entries when needed.
- **Results review**: see score, pass/fail status, explanations, and source metadata after each exam.
- **Interactive CLI mode**: run a terminal-first exam flow with navigation commands, history access, and ANSI-styled output.
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
├── ARCHITECTURE.md
├── TESTING.md
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
└── .github/
    ├── copilot-instructions.md
    ├── ISSUE_TEMPLATE/
    └── workflows/
```

### Core Modules

- [ISTQBQuizApp.py](C:/Projects/practiceISTQB/ISTQBQuizApp.py:1)
  UI/orchestration layer. Owns Tkinter widgets, rendering, and user interaction.
- [cli_quiz.py](C:/Projects/practiceISTQB/cli_quiz.py:1)
  Interactive command-line interface built on the same exam and storage layers.
- [exam_models.py](C:/Projects/practiceISTQB/exam_models.py:1)
  Pure exam-domain logic such as navigation, answers, marks, scoring, restart, and report generation.
- [exam_storage.py](C:/Projects/practiceISTQB/exam_storage.py:1)
  Question-bank loading, history persistence, and randomized exam assembly.
- [ui_layout.py](C:/Projects/practiceISTQB/ui_layout.py:1)
  Responsive wrap and layout helpers for the Tkinter app.
- [test_istqb_quiz_app.py](C:/Projects/practiceISTQB/test_istqb_quiz_app.py:1)
  Unit tests for the storage, domain, CLI helper, and responsive-layout layers.

### Project Ops Toolkit

- [PROJECT_EVOLUTION_FRAMEWORK.md](C:/Projects/practiceISTQB/PROJECT_EVOLUTION_FRAMEWORK.md:1)
  Reusable framework for improving rough or partially complete software projects.
- [SESSION_CHECKLIST.md](C:/Projects/practiceISTQB/SESSION_CHECKLIST.md:1)
  Practical start-to-finish checklist for structured improvement sessions.
- [AI_COLLABORATION_GUIDE.md](C:/Projects/practiceISTQB/AI_COLLABORATION_GUIDE.md:1)
  Patterns for working effectively with AI coding assistants.
- [REFACTOR_PLAYBOOK.md](C:/Projects/practiceISTQB/REFACTOR_PLAYBOOK.md:1)
  Pragmatic refactor sequence for separating UI, domain, and persistence layers.

### Dataset Toolkit

- [DATASET_INTEGRATION_PLAYBOOK.md](C:/Projects/practiceISTQB/DATASET_INTEGRATION_PLAYBOOK.md:1)
  Reusable method for combining multiple partial datasets into one trustworthy corpus.
- [MERGE_CHECKLIST.md](C:/Projects/practiceISTQB/MERGE_CHECKLIST.md:1)
  Operational checklist for dataset normalization, conflict handling, and validation.
- [DATASET_SCHEMA_TEMPLATE.md](C:/Projects/practiceISTQB/DATASET_SCHEMA_TEMPLATE.md:1)
  Canonical schema starter for merged datasets.
- [MERGE_CLI_GUIDE.md](C:/Projects/practiceISTQB/MERGE_CLI_GUIDE.md:1)
  Usage guide for the generic merge CLI workflow.
- [merge_scaffold.py](C:/Projects/practiceISTQB/merge_scaffold.py:1)
  Config-driven merge scaffold for ingest, normalize, dedupe, and export workflows.
- [dataset_merge_config.template.json](C:/Projects/practiceISTQB/dataset_merge_config.template.json:1)
  Example config for running the merge scaffold.
- [RELEASE_NOTES_v0.1.0.md](C:/Projects/practiceISTQB/RELEASE_NOTES_v0.1.0.md:1)
  Suggested notes for the initial tagged release.

## 🚀 Getting Started

### Requirements

- Python `3.14` or later

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
- history load/save behavior
- exam navigation and answer state
- mark-for-review behavior
- timer countdown reduction
- restart/reset logic
- score and report generation
- CLI parsing and rendering helpers
- responsive layout calculations

The UI layer is intentionally thinner than before, with state delegated into `ExamSession` so the most important behavior can be tested without GUI automation.

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

It also includes issue templates for:

- bug reports
- feature requests

## 📚 Question Sources

The question bank is built from **adapted questions based on official ISTQB sample-exam materials** referenced in:

- [istqb_ctfl_practice_exam_links.rtf](C:/Projects/practiceISTQB/istqb_ctfl_practice_exam_links.rtf:1)

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
