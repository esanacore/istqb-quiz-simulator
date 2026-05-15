## Summary

- problem:
- change:

## Review Gate Checklist

- [ ] I ran the repository change gate workflow (`automagic` agent or `/automagic` prompt).
- [ ] I updated `README.md` if the change affects project structure, workflows, automation, or contributor experience.
- [ ] I updated `TESTING.md`, `TEST_PLAN.md`, and `REQUIREMENTS_TRACEABILITY_MATRIX.md` if tests or verification changed.
- [ ] I updated `SOFTWARE_REQUIREMENTS.md` if behavior or quality requirements changed.
- [ ] I ran the relevant specialist reviewers for this scope.

## Specialist Reviewers Used

- [ ] documentation-sync-reviewer
- [ ] unit-integration-test-reviewer
- [ ] requirements-traceability-reviewer
- [ ] ui-visual-reviewer
- [ ] desktop-accessibility-reviewer
- [ ] tkinter-state-reviewer
- [ ] system-e2e-test-reviewer
- [ ] cve-analysis-reviewer
- [ ] question-provenance-reviewer

## Verification

- [ ] `python3 -m unittest -v`
- [ ] `python3 -m py_compile ISTQBQuizApp.py cli_quiz.py exam_models.py exam_storage.py test_istqb_quiz_app.py merge_scaffold.py ui_layout.py`
- [ ] additional verification, if applicable:

## UI Evidence

- [ ] screenshots attached or not needed
