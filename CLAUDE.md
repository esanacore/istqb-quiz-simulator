# CLAUDE.md

This repository follows Eric's Engineering Constitution.

## Required Reading

Before making changes, read:

- `constitution/CONSTITUTION.md`
- `constitution/AI_WORKFLOW.md`
- `constitution/TESTING.md`
- `constitution/DOCUMENTATION.md`
- `constitution/SECURITY.md`
- `README.md`
- `TODO.md`
- `CHANGELOG.md`

## Completion Checklist

Before completing work:

- Confirm the requested change is implemented.
- Add or update relevant tests.
- Update documentation when needed.
- Update TODO.md with discovered or completed work.
- Update CHANGELOG.md for user-facing changes.
- Keep the demo page current — when a change alters user-facing behavior and the repository has a `demo.html`, update it in the same change; a demo still showing the old behavior is an incomplete change (`constitution/DOCUMENTATION.md`, "Demo Page").
- Consult and extend the session log — before planning, read the newest rows of `docs/sessions/README.md` and search `docs/sessions/` for earlier sessions on the same topic (`bash constitution/scripts/find_sessions.sh <keyword>`), reading the ones that match; before completing non-trivial work, add this session's summary there (request, context, decisions, discoveries, outcome — a summary, never a transcript, and never a secret) and list it in the index (`constitution/AI_WORKFLOW.md`, "Session Summaries").
- Consider security impact.
- Identify useful follow-up work.
- Summarize changes and verification.
