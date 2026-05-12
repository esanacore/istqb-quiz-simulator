# Requirements Traceability Matrix

## Purpose

This matrix maps software requirements to automated checks, manual checks, or known coverage gaps.

Automated test IDs are `unittest` method names from `test_istqb_quiz_app.py`.

## Coverage Legend

- `Automated`: covered by unit or integration-style automated tests.
- `Manual`: covered by documented/manual workflow only.
- `Partial`: some automated coverage exists, but UI or workflow behavior still needs manual confirmation.
- `Gap`: requirement is planned or not yet covered.

## Functional Requirements Traceability

| Requirement | Coverage | Verification |
| --- | --- | --- |
| FR-001 | Automated | `test_load_questions_reads_valid_bank` |
| FR-002 | Automated | `test_load_questions_rejects_non_list_bank` |
| FR-003 | Automated | `test_load_questions_rejects_non_object_record` |
| FR-004 | Automated | `test_load_questions_rejects_missing_required_field` |
| FR-005 | Automated | `test_load_questions_rejects_wrong_option_count` |
| FR-006 | Automated | `test_load_questions_rejects_answer_not_in_options` |
| FR-007 | Automated | `test_build_exam_questions_returns_shuffled_copies`, `test_build_exam_answer_and_persist_history_flow` |
| FR-008 | Automated | `test_build_exam_questions_uses_smaller_bank_size` |
| FR-009 | Automated | `test_build_exam_questions_returns_shuffled_copies` |
| FR-010 | Automated | `test_navigation_and_answer_saving`, `test_toggle_mark_and_jump` |
| FR-011 | Automated | `test_navigation_does_not_move_beyond_bounds` |
| FR-012 | Automated | `test_navigation_and_answer_saving` |
| FR-013 | Automated | `test_clear_answer_updates_counts` |
| FR-014 | Automated | `test_clear_answer_updates_counts`, `test_toggle_mark_and_jump` |
| FR-015 | Automated | `test_toggle_mark_and_jump` |
| FR-016 | Automated | `test_advance_time_stops_at_zero_and_ignores_negative_input` |
| FR-017 | Automated | `test_advance_time_stops_at_zero_and_ignores_negative_input` |
| FR-018 | Automated | `test_submit_builds_result_and_locks_session` |
| FR-019 | Automated | `test_submitted_session_ignores_state_changes_and_timer` |
| FR-020 | Automated | `test_submit_builds_result_and_locks_session`, `test_empty_session_result_is_zero_percent_fail` |
| FR-021 | Automated | `test_submit_uses_configured_passing_threshold` |
| FR-022 | Automated | `test_submit_builds_result_and_locks_session`, `test_build_review_text_renders_one_question` |
| FR-023 | Partial | Desktop behavior implemented in `show_results`; needs UI smoke/manual timeout confirmation. |
| FR-024 | Partial | Domain jump covered by `test_toggle_mark_and_jump`; Tkinter map rendering remains manual. |
| FR-025 | Manual | Desktop history window should be smoke-tested manually until UI automation exists. |
| FR-026 | Automated | `test_history_entries_newest_first_preserves_original_indexes` |
| FR-027 | Manual | Delete behavior depends on Tkinter selection; original-index helper is automated. |
| FR-028 | Manual | Confirmation/UI behavior requires manual or future UI smoke coverage. |
| FR-029 | Automated | `test_parse_answer_token_supports_letters_and_numbers` |
| FR-030 | Partial | Helper parsing and domain effects covered; full interactive loop remains manual. |
| FR-031 | Automated | `test_history_entries_newest_first_preserves_original_indexes` |
| FR-032 | Manual | CLI command path should be exercised manually; persistence helper is covered. |
| FR-033 | Automated | `test_build_review_text_renders_one_question` |
| FR-034 | Manual | CLI startup error path should be smoke-tested manually with malformed data. |
| FR-035 | Automated | `test_build_history_entry_normalizes_exam_result`, `test_build_exam_answer_and_persist_history_flow` |
| FR-036 | Automated | `test_load_history_defaults_to_empty_list_when_file_missing` |
| FR-037 | Automated | `test_load_history_rejects_non_list_history` |
| FR-038 | Automated | `test_load_history_normalizes_entries_and_skips_non_dict_values` |
| FR-039 | Manual | `.gitignore` review and `git status` inspection. |
| FR-040 | Automated | `test_compute_wrap_lengths_expands_in_compact_mode`, `test_compute_wrap_lengths_enforces_minimum_width`, `test_determine_layout_mode_switches_at_threshold` |

## Dataset Toolkit Traceability

| Requirement | Coverage | Verification |
| --- | --- | --- |
| DT-001 | Automated | `test_run_merge_and_export_helpers` |
| DT-002 | Automated | `test_load_json_records_rejects_non_list_payload` |
| DT-003 | Automated | `test_normalize_record_uses_question_text_fallback_and_provenance` |
| DT-004 | Automated | `test_normalize_record_uses_question_text_fallback_and_provenance`, `test_run_merge_and_export_helpers` |
| DT-005 | Automated | `test_dedupe_key_normalizes_whitespace_and_case` |
| DT-006 | Automated | `test_choose_preferred_record_uses_authority_rank` |
| DT-007 | Automated | `test_choose_preferred_record_keeps_existing_for_equal_authority` |
| DT-008 | Automated | `test_merge_records_quarantines_empty_dedupe_key` |
| DT-009 | Automated | `test_run_merge_and_export_helpers` |
| DT-010 | Automated | `test_run_merge_and_export_helpers` |
| DT-011 | Automated | `test_load_merge_config_rejects_missing_sources`, `test_load_merge_config_rejects_non_object_config` |

## Quality Requirements Traceability

| Requirement | Coverage | Verification |
| --- | --- | --- |
| QR-001 | Automated/Review | Domain/storage/helper tests exercise UI-independent logic. |
| QR-002 | Manual | Run `python ISTQBQuizApp.py` and `python cli_quiz.py`; no third-party dependencies are declared. |
| QR-003 | Review | `question_bank.json` contains `source`; provenance rules are documented in `AGENTS.md` and `CONTRIBUTING.md`. |
| QR-004 | Automated | `python -m unittest -v` covers 41 fast tests. |
| QR-005 | Automated | `python -m unittest -v` and `python -m py_compile ...`. |
| QR-006 | Review | README, architecture, testing, requirements, and backlog docs updated with behavior changes. |
| QR-007 | Review | `AGENTS.md`, `.github/copilot-instructions.md`, and backlog guidance. |
| QR-008 | Review | `.gitignore` excludes `exam_history.json`, `.testdata/`, `__pycache__/`, and `.idea/`. |

## Planned Requirement Gaps

| Requirement | Coverage | Notes |
| --- | --- | --- |
| PR-001 | Gap | Current baseline: `0/96` questions have topic metadata. |
| PR-002 | Gap | Current baseline: `0/96` questions have learning-objective metadata. |
| PR-003 | Gap | Source/topic/result review filtering is not implemented. |
| PR-004 | Gap | Weak-area study mode depends on topic metadata and/or richer history stats. |
| PR-005 | Gap | Exam settings dialog is not implemented. |
| PR-006 | Gap | History export is not implemented. |
| PR-007 | Gap | Dialog extraction is a maintainability task, not current behavior. |

## Manual Regression Checklist

Run these checks before a release or after UI changes:

1. Start the desktop app with `python ISTQBQuizApp.py`.
2. Answer a question, navigate next/back, and confirm the answer persists.
3. Mark and unmark a question in the desktop UI.
4. Open history, verify newest-first ordering, delete one entry, and clear all entries with confirmation.
5. Submit an exam and inspect the result window.
6. Start the CLI with `python cli_quiz.py`.
7. Use CLI answer, navigation, mark, summary, history, review, restart, and clear-history commands.
8. Temporarily point to malformed test data in a controlled environment and verify startup errors are clear.
