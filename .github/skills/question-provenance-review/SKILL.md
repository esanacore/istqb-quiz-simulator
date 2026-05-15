---
name: question-provenance-review
description: Review question-bank, storage, and merge changes for preserved source provenance, answer integrity, and safe conflict handling.
---

# Question Provenance Review

Use this skill when work touches question content, source metadata, merge tooling, or review reporting.

## Review procedure

1. Check whether any edit weakens source traceability in [question_bank.json](../../../question_bank.json) or downstream review output.
2. Verify that shuffled options still preserve the canonical correct answer.
3. Check merge behavior in [merge_scaffold.py](../../../merge_scaffold.py) for silent conflict handling.
4. Make sure docs do not overstate the officialness of adapted questions.

## Repo-specific reminders

- Prefer source-backed content.
- Prefer quarantine and audit logs over quiet merges for conflicting records.
