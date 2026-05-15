---
name: automagic
description: Run the repository change workflow so docs, tests, requirements, and reviewer checks are not skipped.
agent: automagic
tools:
  - search/codebase
  - github/*
  - desktop-commander/*
  - desktop-screenshot/*
argument-hint: "[feature, files, or change summary]"
---

Run the repository change gate for this work:

${input:changeSummary:Describe the feature, fix, or files being changed}

Required behavior:

1. Determine which specialist reviewers must run.
2. Always include documentation, unit/integration test, and requirements/traceability review.
3. Include UI, system/e2e, CVE, or provenance review when the scope requires it.
4. Identify required documentation and test updates before implementation is considered complete.
5. Return a concise gate checklist with:
   - reviewers used
   - required file updates
   - verification needed
   - any remaining manual follow-up

Use these references while reviewing:

- [Copilot Review Stack](../../COPILOT_REVIEW_STACK.md)
- [Contributing](../../CONTRIBUTING.md)
- [Testing](../../TESTING.md)
- [Test Plan](../../TEST_PLAN.md)
- [Requirements Traceability Matrix](../../REQUIREMENTS_TRACEABILITY_MATRIX.md)
