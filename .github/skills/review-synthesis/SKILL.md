---
name: review-synthesis
description: Combine findings from multiple reviewer passes into one prioritized, non-duplicative report when several review roles were used.
---

# Review Synthesis

Use this skill after UI, accessibility, state, traceability, or provenance reviews have all reported findings.

## Review procedure

1. Merge duplicate findings that share the same root cause.
2. Keep only high-signal issues that matter to correctness, usability, or maintainability.
3. Group results by severity.
4. For each result, include affected files, evidence, impact, and the smallest credible fix.
5. If no meaningful issues remain after deduplication, say so clearly.

## Repo-specific reminders

- Do not drown Tkinter UI work in generic style advice.
- Preserve the distinction between UI quality issues and domain-correctness issues.
