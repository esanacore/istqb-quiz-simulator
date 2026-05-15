---
name: ui-polish-review
description: Review Tkinter UI changes for spacing, clipping, readability, action hierarchy, and resize behavior when work touches the desktop app or layout helpers.
---

# UI Polish Review

Use this skill when a change touches [ISTQBQuizApp.py](../../../ISTQBQuizApp.py), [ui_layout.py](../../../ui_layout.py), or any UI screenshot/documentation.

## Review procedure

1. Read the changed desktop UI files first.
2. Check whether long question text, wrapped options, sidebars, and footer controls still fit cleanly.
3. Look for visual hierarchy issues around navigation, submit, mark-for-review, and history actions.
4. If MCP desktop tools are available, launch the app and capture screenshots for narrow and wide window states.
5. Return only findings that would noticeably affect user confidence or readability.

## Repo-specific reminders

- The UI layer should orchestrate, not own business rules.
- Responsive layout behavior is part of the expected desktop experience.
- Suggest screenshots in reviews when a UI change would be hard to assess from code alone.
