# Copilot Review Stack

## Purpose

This repository includes a repo-scoped Copilot review stack aimed at **Tkinter desktop UI quality**, **desktop usability**, **state-flow correctness**, **documentation sync**, **test coverage planning**, and **requirements/provenance drift**.

It is designed to give the simulator multiple reviewer perspectives without forcing every review into one generic prompt.

## Included Components

### Workspace MCP servers

The workspace MCP configuration lives in [.vscode/mcp.json](.vscode/mcp.json).

| Server | Purpose |
| --- | --- |
| `github` | Pull request and repository context through the GitHub MCP endpoint. |
| `desktop-commander` | Launch the Tkinter app, inspect files, and run targeted local review commands. |
| `desktop-screenshot` | Capture native desktop screenshots for Tkinter UI review on Linux, macOS, or Windows. |

### Custom agents

The custom agents live in [.github/agents](.github/agents).

| Agent | Role |
| --- | --- |
| `automagic` | Default workflow agent for meaningful changes; ensures docs, tests, and traceability review are not skipped. |
| `review-orchestrator` | Routes work to the relevant reviewers and synthesizes findings. |
| `ui-visual-reviewer` | Looks for clipping, spacing, hierarchy, and resize problems. |
| `desktop-accessibility-reviewer` | Looks for keyboard, focus, readability, and usability issues. |
| `tkinter-state-reviewer` | Reviews answer persistence, restart, submit, timer, and navigation state. |
| `requirements-traceability-reviewer` | Checks requirement, test-plan, and traceability alignment. |
| `question-provenance-reviewer` | Protects source metadata and answer integrity. |
| `documentation-sync-reviewer` | Keeps README, architecture, testing, and contributor docs aligned with the codebase. |
| `unit-integration-test-reviewer` | Looks for missing unit and integration regression coverage. |
| `system-e2e-test-reviewer` | Reviews workflow-level system and end-to-end coverage gaps. |
| `cve-analysis-reviewer` | Reviews dependency and supply-chain risk, including CVE-oriented audit opportunities. |

### Skills

The reusable skills live in [.github/skills](.github/skills).

- `ui-polish-review`
- `desktop-accessibility-review`
- `tkinter-architecture-review`
- `documentation-sync-review`
- `unit-integration-test-review`
- `system-e2e-test-review`
- `requirements-traceability-review`
- `question-provenance-review`
- `cve-analysis-review`
- `review-synthesis`

## Why This Stack Fits This Repo

This is a **desktop Tkinter app**, so browser-only review tooling is not enough. The review stack is centered on:

- native desktop screenshots for Tkinter windows
- terminal/process control for launching the local app under a virtual display
- GitHub context for PR-aware review
- repo-specific reviewer instructions tied to `ISTQBQuizApp.py`, `ui_layout.py`, `exam_models.py`, `exam_storage.py`, the SQA artifacts, and contributor-facing documentation

## Local Setup

1. Open the repo in VS Code with GitHub Copilot Chat enabled.
2. Trust the workspace MCP servers from [.vscode/mcp.json](.vscode/mcp.json).
3. Ensure local prerequisites exist:
   - Node.js `18+`
   - Python `3.12+`
   - On Linux, screenshot tools such as `scrot` and `xdotool`
4. Use the `review-orchestrator` agent for broad review requests, or switch directly to a specialist reviewer.

## Recommended Review Workflow

For any meaningful repository change:

1. Start with `automagic` or the `/automagic` prompt.
2. Let it determine the required specialist reviewers.
3. Do not conclude the change is complete until docs, tests, and traceability updates are addressed.

For desktop UI changes:

1. Launch `review-orchestrator`.
2. Ask it to review the changed UI files and run the relevant specialists.
3. If runtime evidence is needed, launch the app with `xvfb-run -a python3 ISTQBQuizApp.py` through `desktop-commander`.
4. Capture screenshots with `desktop-screenshot`.
5. Use `review-synthesis` if several reviewer threads produced overlapping findings.

For broader feature changes:

1. Use `documentation-sync-reviewer` when workflows, architecture, or contributor instructions changed.
2. Use `unit-integration-test-reviewer` for logic and helper coverage gaps.
3. Use `system-e2e-test-reviewer` for user-visible workflow changes.
4. Use `cve-analysis-reviewer` when dependencies, workflows, or third-party tooling changed.

## What Is Automatic vs Not Automatic

The README and other docs do **not** update themselves automatically by magic.

What this repository now does is make review automation the default workflow:

- the `automagic` agent
- the `/automagic` prompt
- stronger repository instructions in `AGENTS.md` and `.github/copilot-instructions.md`
- the PR checklist in `.github/pull_request_template.md`

That combination makes it much harder to skip README, testing, requirements, or specialist review updates during normal repo work.

## Automated Security Signals

The repository also includes [.github/dependabot.yml](.github/dependabot.yml) for weekly GitHub Actions dependency updates. That gives the review stack a real automated supply-chain signal in addition to the CVE review agent and skill.

## Cloud Agent Setup

The Copilot cloud-agent environment is prepared by [.github/workflows/copilot-setup-steps.yml](.github/workflows/copilot-setup-steps.yml).

That workflow installs:

- Python `3.12`
- Node.js `20`
- Linux Tkinter and virtual-display prerequisites
- screenshot prerequisites used by the desktop review workflow
- `pip-audit` for Python dependency CVE analysis when manifests exist

## Safety Notes

- Workspace MCP servers can execute local commands. Only enable them in trusted repositories.
- Avoid hardcoding secrets into `.vscode/mcp.json`.
- The `github` MCP server uses the GitHub Copilot MCP endpoint instead of a repository-specific token in source control.
