# Home

Welcome to the **ISTQB CTFL Quiz Simulator** wiki. Wiki pages are authored
under `wiki/` in this repository and reviewed through normal pull requests.

## What this project does

A desktop exam simulator for ISTQB Certified Tester Foundation Level (CTFL
v4.0) practice, built with Python + Tkinter. It reproduces the pressure and
workflow of a real exam session rather than a flashcard app: a 60-minute
timer, randomized 40-question exams from a large official-sample-derived
bank, shuffled answer order, a question navigator, mark-for-review,
submission guards, persistent attempt history, and detailed post-exam review
with explanations. An interactive CLI mode offers a terminal-first exam flow.
It is a study simulator, not an official ISTQB exam product.

## Getting started

Run the Tkinter app for the desktop UI, or the CLI mode for a terminal-first
flow — lightweight, local, no web stack required. See `docs/SETUP.md`.

## How it works

Each attempt builds a randomized 40-question exam from the question bank,
reshuffling choices while preserving correctness; attempts persist locally
for newest-first history review.

## Where things live

- The simulator source (desktop UI and CLI)
- `docs/` — setup and governance docs
- `constitution/` — Eric's Engineering Constitution submodule (read-only)

## See also

- `docs/HELP.md` — common questions and troubleshooting
- `TODO.md` — the living roadmap
