---
name: desktop-accessibility-review
description: Review the Tkinter desktop experience for keyboard reachability, focus flow, readable text density, and usability issues when UI or navigation changes are made.
---

# Desktop Accessibility Review

Use this skill for desktop interaction changes, especially around question answering, navigation, dialogs, and history review.

## Review procedure

1. Inspect the relevant code paths in [ISTQBQuizApp.py](../../../ISTQBQuizApp.py).
2. Check whether controls can be understood and used without relying only on color or pointer precision.
3. Verify that labels, confirmations, and progress state remain easy to scan.
4. If screenshots are available, look for low-contrast or overly dense layouts.
5. Focus on realistic desktop usability issues rather than abstract standards compliance.

## Repo-specific reminders

- Keep recommendations dependency-light.
- Prefer changes that improve clarity for exam-taking under time pressure.
