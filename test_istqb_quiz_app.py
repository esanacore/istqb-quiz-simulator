"""Unit tests for quiz models and storage helpers.

Author: Eric Sanacore
Date: 2026-05-10
"""

import json
import unittest
from datetime import datetime
from pathlib import Path

import cli_quiz
import exam_models
import exam_storage
import merge_scaffold
import ui_layout

TEST_DATA_DIR = Path(__file__).with_name(".testdata")


class ExamStorageTests(unittest.TestCase):
    """Tests for question-bank and history persistence helpers."""

    def setUp(self):
        TEST_DATA_DIR.mkdir(exist_ok=True)

    def tearDown(self):
        if TEST_DATA_DIR.exists():
            for path in TEST_DATA_DIR.iterdir():
                if path.is_file():
                    path.unlink()

    def write_json(self, name, payload):
        """Write a JSON fixture file into the workspace-local test directory."""
        path = TEST_DATA_DIR / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_load_questions_reads_valid_bank(self):
        bank_path = self.write_json(
            "question_bank.json",
            [
                {
                    "q": "Question 1",
                    "options": ["A", "B", "C", "D"],
                    "answer": "B",
                    "explanation": "Because B is correct.",
                }
            ],
        )

        questions = exam_storage.load_questions(bank_path)

        self.assertEqual(1, len(questions))
        self.assertEqual("Question 1", questions[0]["q"])

    def test_load_questions_rejects_answer_not_in_options(self):
        bank_path = self.write_json(
            "question_bank.json",
            [
                {
                    "q": "Broken",
                    "options": ["A", "B", "C", "D"],
                    "answer": "Z",
                    "explanation": "Invalid payload.",
                }
            ],
        )

        with self.assertRaises(ValueError):
            exam_storage.load_questions(bank_path)

    def test_load_questions_rejects_non_list_bank(self):
        bank_path = self.write_json("question_bank.json", {"q": "Not a list"})

        with self.assertRaisesRegex(ValueError, "non-empty list"):
            exam_storage.load_questions(bank_path)

    def test_load_questions_rejects_non_object_record(self):
        bank_path = self.write_json("question_bank.json", ["not an object"])

        with self.assertRaisesRegex(ValueError, "not an object"):
            exam_storage.load_questions(bank_path)

    def test_load_questions_rejects_missing_required_field(self):
        bank_path = self.write_json(
            "question_bank.json",
            [
                {
                    "q": "Missing explanation",
                    "options": ["A", "B", "C", "D"],
                    "answer": "A",
                }
            ],
        )

        with self.assertRaisesRegex(ValueError, "explanation"):
            exam_storage.load_questions(bank_path)

    def test_load_questions_rejects_wrong_option_count(self):
        bank_path = self.write_json(
            "question_bank.json",
            [
                {
                    "q": "Broken",
                    "options": ["A", "B", "C"],
                    "answer": "A",
                    "explanation": "Invalid option count.",
                }
            ],
        )

        with self.assertRaisesRegex(ValueError, "exactly 4"):
            exam_storage.load_questions(bank_path)

    def test_build_exam_questions_returns_shuffled_copies(self):
        question_bank = [
            {
                "q": f"Question {index}",
                "options": ["A", "B", "C", "D"],
                "answer": "C",
                "explanation": "Explanation",
            }
            for index in range(50)
        ]

        exam = exam_storage.build_exam_questions(question_bank)

        self.assertEqual(exam_storage.EXAM_QUESTION_COUNT, len(exam))
        self.assertEqual(50, len(question_bank))
        self.assertTrue(all(question["answer"] in question["options"] for question in exam))
        self.assertTrue(
            all(
                question is not bank_question
                for question in exam
                for bank_question in question_bank
                if question["q"] == bank_question["q"]
            )
        )
        self.assertTrue(
            all(bank_question["options"] == ["A", "B", "C", "D"] for bank_question in question_bank)
        )

    def test_build_exam_questions_uses_smaller_bank_size(self):
        question_bank = [
            {
                "q": f"Question {index}",
                "options": ["A", "B", "C", "D"],
                "answer": "A",
                "explanation": "Explanation",
            }
            for index in range(3)
        ]

        exam = exam_storage.build_exam_questions(question_bank, exam_question_count=40)

        self.assertEqual(3, len(exam))
        self.assertEqual(
            sorted(question["q"] for question in question_bank),
            sorted(question["q"] for question in exam),
        )

    def test_load_history_defaults_to_empty_list_when_file_missing(self):
        history_path = TEST_DATA_DIR / "exam_history.json"

        history = exam_storage.load_history(history_path)

        self.assertEqual([], history)

    def test_save_and_load_history_round_trip(self):
        history_path = TEST_DATA_DIR / "exam_history.json"
        history = [
            {
                "timestamp": "2026-05-10 01:00:00",
                "score": 33,
                "total": 40,
                "percent": 82.5,
                "result": "PASS",
            }
        ]

        exam_storage.save_history(history, history_path)
        loaded = exam_storage.load_history(history_path)

        self.assertEqual(history, loaded)

    def test_load_history_rejects_non_list_history(self):
        history_path = self.write_json("exam_history.json", {"timestamp": "broken"})

        with self.assertRaisesRegex(ValueError, "list"):
            exam_storage.load_history(history_path)

    def test_load_history_normalizes_entries_and_skips_non_dict_values(self):
        history_path = self.write_json(
            "exam_history.json",
            [
                "skip me",
                {
                    "timestamp": 123,
                    "score": "31",
                    "total": "40",
                    "percent": "77.5",
                    "result": "PASS",
                },
            ],
        )

        history = exam_storage.load_history(history_path)

        self.assertEqual(
            [
                {
                    "timestamp": "123",
                    "score": 31,
                    "total": 40,
                    "percent": 77.5,
                    "result": "PASS",
                }
            ],
            history,
        )

    def test_build_history_entry_normalizes_exam_result(self):
        result = exam_models.ExamResult(
            score=27,
            total=40,
            percent=67.555,
            passed=True,
            report="Review",
        )
        timestamp = datetime(2026, 5, 10, 1, 2, 3)

        entry = exam_storage.build_history_entry(result, timestamp=timestamp)

        self.assertEqual(
            {
                "timestamp": "2026-05-10 01:02:03",
                "score": 27,
                "total": 40,
                "percent": 67.56,
                "result": "PASS",
            },
            entry,
        )

    def test_history_entries_newest_first_preserves_original_indexes(self):
        history = [
            {
                "timestamp": "2026-05-10 01:00:00",
                "score": 20,
                "total": 40,
                "percent": 50.0,
                "result": "FAIL",
            },
            {
                "timestamp": "2026-05-11 01:00:00",
                "score": 30,
                "total": 40,
                "percent": 75.0,
                "result": "PASS",
            },
            {
                "timestamp": "2026-05-10 02:00:00",
                "score": 25,
                "total": 40,
                "percent": 62.5,
                "result": "FAIL",
            },
        ]

        indexed_entries = exam_storage.history_entries_newest_first(history)

        self.assertEqual([1, 2, 0], [index for index, _entry in indexed_entries])

    def test_history_entries_newest_first_empty_history(self):
        indexed_entries = exam_storage.history_entries_newest_first([])

        self.assertEqual([], indexed_entries)

    def test_history_entries_newest_first_single_entry(self):
        history = [
            {
                "timestamp": "2026-05-10 01:00:00",
                "score": 30,
                "total": 40,
                "percent": 75.0,
                "result": "PASS",
            }
        ]

        indexed_entries = exam_storage.history_entries_newest_first(history)

        self.assertEqual([(0, history[0])], indexed_entries)

    def test_history_entries_newest_first_tie_broken_by_original_index(self):
        history = [
            {
                "timestamp": "2026-05-10 01:00:00",
                "score": 20,
                "total": 40,
                "percent": 50.0,
                "result": "FAIL",
            },
            {
                "timestamp": "2026-05-10 01:00:00",
                "score": 30,
                "total": 40,
                "percent": 75.0,
                "result": "PASS",
            },
        ]

        indexed_entries = exam_storage.history_entries_newest_first(history)

        self.assertEqual([1, 0], [index for index, _entry in indexed_entries])

    def test_build_history_entry_fail_result(self):
        result = exam_models.ExamResult(
            score=10,
            total=40,
            percent=25.0,
            passed=False,
            report="Review",
        )
        timestamp = datetime(2026, 5, 12, 8, 0, 0)

        entry = exam_storage.build_history_entry(result, timestamp=timestamp)

        self.assertEqual("FAIL", entry["result"])
        self.assertEqual(10, entry["score"])
        self.assertEqual(25.0, entry["percent"])

    def test_load_questions_rejects_empty_list(self):
        bank_path = self.write_json("question_bank.json", [])

        with self.assertRaisesRegex(ValueError, "non-empty list"):
            exam_storage.load_questions(bank_path)

    def test_load_questions_rejects_options_not_a_list(self):
        bank_path = self.write_json(
            "question_bank.json",
            [
                {
                    "q": "Broken",
                    "options": "ABCD",
                    "answer": "A",
                    "explanation": "Options must be a list.",
                }
            ],
        )

        with self.assertRaisesRegex(ValueError, "exactly 4"):
            exam_storage.load_questions(bank_path)

    def test_build_exam_questions_preserves_answer_in_shuffled_options(self):
        question_bank = [
            {
                "q": "Q",
                "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                "answer": "Option 2",
                "explanation": "Explanation",
            }
            for _ in range(10)
        ]

        exam = exam_storage.build_exam_questions(question_bank, exam_question_count=5)

        for question in exam:
            self.assertIn(question["answer"], question["options"])


class ExamSessionTests(unittest.TestCase):
    """Tests for exam navigation, scoring, and restart behavior."""

    def setUp(self):
        self.questions = [
            {
                "q": "Question 1",
                "options": ["A", "B", "C", "D"],
                "answer": "B",
                "explanation": "Explanation 1",
                "source": "Sample 1",
            },
            {
                "q": "Question 2",
                "options": ["A", "B", "C", "D"],
                "answer": "D",
                "explanation": "Explanation 2",
            },
        ]
        self.session = exam_models.ExamSession(self.questions, duration_seconds=120)

    def test_navigation_and_answer_saving(self):
        self.session.save_answer("B")
        self.session.next_q()
        self.session.save_answer("D")

        self.assertEqual(1, self.session.current_q)
        self.assertEqual(["B", "D"], self.session.user_answers)
        self.assertEqual(2, self.session.answered_count())

    def test_navigation_does_not_move_beyond_bounds(self):
        self.session.prev_q()
        self.assertEqual(0, self.session.current_q)

        self.session.next_q()
        self.session.next_q()

        self.assertEqual(1, self.session.current_q)

    def test_clear_answer_updates_counts(self):
        self.session.save_answer("B")
        self.assertEqual(1, self.session.answered_count())
        self.assertEqual(1, self.session.remaining_count())

        self.session.save_answer("")

        self.assertEqual([None, None], self.session.user_answers)
        self.assertEqual(0, self.session.answered_count())
        self.assertEqual(2, self.session.remaining_count())

    def test_toggle_mark_and_jump(self):
        self.session.toggle_mark()
        self.session.jump_to_question(1)
        self.session.toggle_mark()

        self.assertEqual([True, True], self.session.marked_for_review)
        self.assertEqual(2, self.session.marked_count())
        self.assertEqual(1, self.session.current_q)

    def test_restart_resets_state(self):
        self.session.save_answer("B")
        self.session.toggle_mark()
        self.session.time_left = 30

        self.session.restart()

        self.assertEqual(0, self.session.current_q)
        self.assertEqual([None, None], self.session.user_answers)
        self.assertEqual([False, False], self.session.marked_for_review)
        self.assertEqual(120, self.session.time_left)
        self.assertFalse(self.session.submitted)

    def test_advance_time_stops_at_zero_and_ignores_negative_input(self):
        self.session.advance_time(15)
        self.session.advance_time(-20)
        self.session.advance_time(500)

        self.assertEqual(0, self.session.time_left)

    def test_submitted_session_ignores_state_changes_and_timer(self):
        self.session.save_answer("B")
        self.session.submit()

        self.session.advance_time(30)
        self.session.next_q()
        self.session.toggle_mark()
        self.session.save_answer("A")

        self.assertEqual(120, self.session.time_left)
        self.assertEqual(0, self.session.current_q)
        self.assertEqual([False, False], self.session.marked_for_review)
        self.assertEqual(["B", None], self.session.user_answers)

    def test_submit_builds_result_and_locks_session(self):
        self.session.save_answer("B")
        self.session.next_q()
        self.session.save_answer("A")

        result = self.session.submit()
        self.session.jump_to_question(0)
        self.session.save_answer("C")

        self.assertTrue(self.session.submitted)
        self.assertEqual(1, result.score)
        self.assertEqual(2, result.total)
        self.assertEqual(50.0, result.percent)
        self.assertFalse(result.passed)
        self.assertIn("Q1: CORRECT", result.report)
        self.assertIn("Source: Sample 1", result.report)
        self.assertEqual(1, self.session.current_q)
        self.assertEqual(["B", "A"], self.session.user_answers)

    def test_submit_uses_configured_passing_threshold(self):
        session = exam_models.ExamSession(
            self.questions,
            duration_seconds=120,
            passing_percent=50.0,
        )
        session.save_answer("B")
        session.next_q()
        session.save_answer("A")

        result = session.submit()

        self.assertEqual(50.0, result.percent)
        self.assertTrue(result.passed)

    def test_empty_session_result_is_zero_percent_fail(self):
        session = exam_models.ExamSession([], duration_seconds=60)

        result = session.submit()

        self.assertEqual(0, result.score)
        self.assertEqual(0, result.total)
        self.assertEqual(0.0, result.percent)
        self.assertFalse(result.passed)

    def test_jump_to_question_ignores_out_of_range_index(self):
        self.session.jump_to_question(-1)
        self.assertEqual(0, self.session.current_q)

        self.session.jump_to_question(100)
        self.assertEqual(0, self.session.current_q)

    def test_restart_with_replacement_questions(self):
        replacement = [
            {
                "q": "New Question",
                "options": ["W", "X", "Y", "Z"],
                "answer": "W",
                "explanation": "New explanation",
            }
        ]
        self.session.save_answer("B")

        self.session.restart(replacement)

        self.assertEqual(replacement, self.session.questions)
        self.assertEqual([None], self.session.user_answers)
        self.assertEqual([False], self.session.marked_for_review)
        self.assertEqual(0, self.session.current_q)

    def test_advance_time_no_change_on_zero_elapsed(self):
        self.session.advance_time(0)
        self.assertEqual(120, self.session.time_left)

    def test_submit_called_twice_returns_consistent_result(self):
        self.session.save_answer("B")
        self.session.next_q()
        self.session.save_answer("D")

        first_result = self.session.submit()
        second_result = self.session.submit()

        self.assertEqual(first_result.score, second_result.score)
        self.assertEqual(first_result.percent, second_result.percent)
        self.assertEqual(first_result.passed, second_result.passed)

    def test_build_result_includes_topic_and_lo_in_report(self):
        questions = [
            {
                "q": "Q with topic and lo",
                "options": ["A", "B", "C", "D"],
                "answer": "A",
                "explanation": "Explanation",
                "topic": "Static testing",
                "lo": "FL-3.1.1",
            }
        ]
        session = exam_models.ExamSession(questions, duration_seconds=60)
        session.save_answer("A")
        result = session.submit()

        self.assertIn("Topic: Static testing", result.report)
        self.assertIn("Learning Objective: FL-3.1.1", result.report)

    def test_build_result_omits_absent_optional_fields_without_error(self):
        questions = [
            {
                "q": "Q without optional fields",
                "options": ["A", "B", "C", "D"],
                "answer": "A",
                "explanation": "Explanation",
            }
        ]
        session = exam_models.ExamSession(questions, duration_seconds=60)
        session.save_answer("A")
        result = session.submit()

        self.assertNotIn("Source:", result.report)
        self.assertNotIn("Topic:", result.report)
        self.assertNotIn("Learning Objective:", result.report)

    def test_all_wrong_answers_produce_zero_score(self):
        self.session.save_answer("A")
        self.session.next_q()
        self.session.save_answer("A")

        result = self.session.submit()

        self.assertEqual(0, result.score)
        self.assertFalse(result.passed)
        self.assertIn("Q1: WRONG", result.report)
        self.assertIn("Q2: WRONG", result.report)

    def test_answered_and_remaining_counts_across_full_question_set(self):
        self.assertEqual(0, self.session.answered_count())
        self.assertEqual(2, self.session.remaining_count())

        self.session.save_answer("B")
        self.assertEqual(1, self.session.answered_count())
        self.assertEqual(1, self.session.remaining_count())

        self.session.next_q()
        self.session.save_answer("D")
        self.assertEqual(2, self.session.answered_count())
        self.assertEqual(0, self.session.remaining_count())


class CliHelperTests(unittest.TestCase):
    """Tests for the command-line helper functions."""

    def test_parse_answer_token_supports_letters_and_numbers(self):
        self.assertEqual(0, cli_quiz.parse_answer_token("A", 4))
        self.assertEqual(1, cli_quiz.parse_answer_token(" b ", 4))
        self.assertEqual(2, cli_quiz.parse_answer_token("3", 4))
        self.assertIsNone(cli_quiz.parse_answer_token("D", 3))
        self.assertIsNone(cli_quiz.parse_answer_token("9", 4))
        self.assertIsNone(cli_quiz.parse_answer_token("next", 4))

    def test_format_duration_and_progress_bar(self):
        self.assertEqual("02:05", cli_quiz.format_duration(125))
        self.assertEqual("00:00", cli_quiz.format_duration(-10))
        self.assertEqual("[#####-----]", cli_quiz.build_progress_bar(2, 4, width=10))
        self.assertEqual("[----------]", cli_quiz.build_progress_bar(1, 0, width=10))

    def test_build_question_map_marks_current_answered_and_marked(self):
        session = exam_models.ExamSession(
            [
                {
                    "q": "Question 1",
                    "options": ["A", "B", "C", "D"],
                    "answer": "A",
                    "explanation": "Explanation 1",
                },
                {
                    "q": "Question 2",
                    "options": ["A", "B", "C", "D"],
                    "answer": "B",
                    "explanation": "Explanation 2",
                },
                {
                    "q": "Question 3",
                    "options": ["A", "B", "C", "D"],
                    "answer": "C",
                    "explanation": "Explanation 3",
                },
            ]
        )
        session.save_answer("A")
        session.next_q()
        session.toggle_mark()

        question_map = cli_quiz.build_question_map(session, columns=3)

        self.assertIn(" 01*", question_map)
        self.assertIn("[02]", question_map)
        self.assertIn(" 03.", question_map)

    def test_build_review_text_renders_one_question(self):
        session = exam_models.ExamSession(
            [
                {
                    "q": "Question 1",
                    "options": ["A", "B", "C", "D"],
                    "answer": "B",
                    "explanation": "B is correct.",
                    "source": "Sample",
                    "topic": "Testing basics",
                    "lo": "FL-1.1.1",
                }
            ]
        )
        session.save_answer("A")
        session.submit()

        review_text = cli_quiz.build_review_text(session, 0)

        self.assertIn("Question 1/1: WRONG", review_text)
        self.assertIn("Your Answer: A", review_text)
        self.assertIn("Correct Answer: B", review_text)
        self.assertIn("Source: Sample", review_text)
        self.assertIn("Topic: Testing basics", review_text)
        self.assertIn("Learning Objective: FL-1.1.1", review_text)

    def test_parse_answer_token_empty_string_returns_none(self):
        self.assertIsNone(cli_quiz.parse_answer_token("", 4))
        self.assertIsNone(cli_quiz.parse_answer_token("  ", 4))

    def test_parse_answer_token_zero_and_out_of_range_number_return_none(self):
        self.assertIsNone(cli_quiz.parse_answer_token("0", 4))
        self.assertIsNone(cli_quiz.parse_answer_token("5", 4))

    def test_build_progress_bar_fully_answered(self):
        bar = cli_quiz.build_progress_bar(10, 10, width=10)
        self.assertEqual("[##########]", bar)

    def test_build_progress_bar_zero_answered(self):
        bar = cli_quiz.build_progress_bar(0, 10, width=10)
        self.assertEqual("[----------]", bar)

    def test_format_duration_zero_seconds(self):
        self.assertEqual("00:00", cli_quiz.format_duration(0))

    def test_format_duration_one_hour(self):
        self.assertEqual("60:00", cli_quiz.format_duration(3600))

    def test_build_question_map_shows_marked_but_not_current_token(self):
        session = exam_models.ExamSession(
            [
                {
                    "q": "Question 1",
                    "options": ["A", "B", "C", "D"],
                    "answer": "A",
                    "explanation": "Explanation 1",
                },
                {
                    "q": "Question 2",
                    "options": ["A", "B", "C", "D"],
                    "answer": "B",
                    "explanation": "Explanation 2",
                },
            ]
        )
        session.toggle_mark()
        session.next_q()

        question_map = cli_quiz.build_question_map(session, columns=2)

        self.assertIn("!01!", question_map)
        self.assertIn("[02]", question_map)

    def test_build_review_text_correct_answer(self):
        session = exam_models.ExamSession(
            [
                {
                    "q": "Q",
                    "options": ["A", "B", "C", "D"],
                    "answer": "A",
                    "explanation": "A is correct.",
                }
            ]
        )
        session.save_answer("A")
        session.submit()

        review_text = cli_quiz.build_review_text(session, 0)

        self.assertIn("CORRECT", review_text)

    def test_build_review_text_no_optional_fields(self):
        session = exam_models.ExamSession(
            [
                {
                    "q": "Q",
                    "options": ["A", "B", "C", "D"],
                    "answer": "A",
                    "explanation": "A is correct.",
                }
            ]
        )
        session.save_answer("A")
        session.submit()

        review_text = cli_quiz.build_review_text(session, 0)

        self.assertNotIn("Source:", review_text)
        self.assertNotIn("Topic:", review_text)
        self.assertNotIn("Learning Objective:", review_text)


class UiLayoutTests(unittest.TestCase):
    """Tests for responsive layout calculations."""

    def test_determine_layout_mode_switches_at_threshold(self):
        self.assertEqual(ui_layout.COMPACT_LAYOUT, ui_layout.determine_layout_mode(900))
        self.assertEqual(ui_layout.WIDE_LAYOUT, ui_layout.determine_layout_mode(1100))
        self.assertEqual(ui_layout.WIDE_LAYOUT, ui_layout.determine_layout_mode(1280))

    def test_compute_wrap_lengths_expands_in_compact_mode(self):
        compact = ui_layout.compute_wrap_lengths(900, ui_layout.COMPACT_LAYOUT)
        wide = ui_layout.compute_wrap_lengths(1200, ui_layout.WIDE_LAYOUT)

        self.assertGreater(compact["question"], wide["question"] - 100)
        self.assertGreaterEqual(compact["sidebar"], 260)
        self.assertGreater(wide["option"], 380)

    def test_compute_wrap_lengths_enforces_minimum_width(self):
        wraps = ui_layout.compute_wrap_lengths(320, ui_layout.COMPACT_LAYOUT)

        self.assertGreaterEqual(wraps["question"], 440)
        self.assertGreaterEqual(wraps["option"], 380)
        self.assertGreaterEqual(wraps["sidebar"], 260)

    def test_determine_layout_mode_at_exact_threshold_is_wide(self):
        self.assertEqual(ui_layout.WIDE_LAYOUT, ui_layout.determine_layout_mode(1100))

    def test_compute_wrap_lengths_wide_layout_uses_narrow_sidebar(self):
        wraps = ui_layout.compute_wrap_lengths(1200, ui_layout.WIDE_LAYOUT)
        self.assertEqual(180, wraps["sidebar"])

    def test_compute_wrap_lengths_wide_layout_clamps_to_minimum(self):
        wraps = ui_layout.compute_wrap_lengths(320, ui_layout.WIDE_LAYOUT)
        self.assertGreaterEqual(wraps["question"], 440)
        self.assertGreaterEqual(wraps["option"], 380)


class MergeScaffoldTests(unittest.TestCase):
    """Tests for merge scaffold normalization and conflict-resolution behavior."""

    def setUp(self):
        TEST_DATA_DIR.mkdir(exist_ok=True)

    def tearDown(self):
        if TEST_DATA_DIR.exists():
            for path in TEST_DATA_DIR.iterdir():
                if path.is_file():
                    path.unlink()

    def write_json(self, name, payload):
        """Write a JSON fixture file into the workspace-local test directory."""
        path = TEST_DATA_DIR / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_load_merge_config_rejects_missing_sources(self):
        config_path = self.write_json("merge_config.json", {"output_dir": "merge_output"})

        with self.assertRaises(ValueError):
            merge_scaffold.load_merge_config(config_path)

    def test_load_json_records_rejects_non_list_payload(self):
        records_path = self.write_json("records.json", {"id": "1"})

        with self.assertRaisesRegex(ValueError, "JSON list"):
            merge_scaffold.load_json_records(records_path)

    def test_load_merge_config_rejects_non_object_config(self):
        config_path = self.write_json("merge_config.json", [])

        with self.assertRaisesRegex(ValueError, "JSON object"):
            merge_scaffold.load_merge_config(config_path)

    def test_normalize_record_uses_question_text_fallback_and_provenance(self):
        record = merge_scaffold.normalize_record(
            {"id": 7, "q": "  Question text  "},
            source_name="sample_source",
            authority="authoritative",
        )

        self.assertEqual("7", record.record_id)
        self.assertEqual("Question text", record.content)
        self.assertEqual("sample_source", record.payload["source"]["name"])
        self.assertEqual("authoritative", record.payload["quality"]["authority"])

    def test_dedupe_key_normalizes_whitespace_and_case(self):
        record = merge_scaffold.MergeRecord(
            record_id="1",
            content="  This Is A Question  ",
            source_name="source_a",
            source_record_id="1",
            authority="supplementary",
            payload={},
        )

        self.assertEqual("this is a question", merge_scaffold.dedupe_key(record))

    def test_choose_preferred_record_uses_authority_rank(self):
        existing = merge_scaffold.MergeRecord(
            record_id="1",
            content="question",
            source_name="legacy_source",
            source_record_id="L1",
            authority="legacy",
            payload={},
        )
        candidate = merge_scaffold.MergeRecord(
            record_id="2",
            content="question",
            source_name="authoritative_source",
            source_record_id="A1",
            authority="authoritative",
            payload={},
        )

        chosen, rejected, note = merge_scaffold.choose_preferred_record(existing, candidate)

        self.assertIs(candidate, chosen)
        self.assertIs(existing, rejected)
        self.assertIn("higher-authority source", note)
        self.assertIn(note, candidate.transformation_notes)

    def test_choose_preferred_record_keeps_existing_for_equal_authority(self):
        existing = merge_scaffold.MergeRecord(
            record_id="1",
            content="question",
            source_name="source_a",
            source_record_id="A1",
            authority="supplementary",
            payload={},
        )
        candidate = merge_scaffold.MergeRecord(
            record_id="2",
            content="question",
            source_name="source_b",
            source_record_id="B1",
            authority="supplementary",
            payload={},
        )

        chosen, rejected, note = merge_scaffold.choose_preferred_record(existing, candidate)

        self.assertIs(existing, chosen)
        self.assertIs(candidate, rejected)
        self.assertIn("Kept existing", note)

    def test_merge_records_quarantines_empty_dedupe_key(self):
        empty_record = merge_scaffold.MergeRecord(
            record_id="1",
            content="   ",
            source_name="source_a",
            source_record_id="1",
            authority="supplementary",
            payload={},
        )
        valid_record = merge_scaffold.MergeRecord(
            record_id="2",
            content="Valid content",
            source_name="source_b",
            source_record_id="2",
            authority="supplementary",
            payload={},
        )

        merged, quarantined, audit_log = merge_scaffold.merge_records([empty_record, valid_record])

        self.assertEqual(1, len(merged))
        self.assertEqual(1, len(quarantined))
        self.assertIs(empty_record, quarantined[0])
        self.assertIn("Quarantined because dedupe key was empty.", empty_record.transformation_notes)
        self.assertEqual(["Inserted source_b:2"], audit_log)

    def test_run_merge_and_export_helpers(self):
        source_path = self.write_json(
            "source_records.json",
            [{"id": "1", "content": "Question A"}, {"id": "2", "content": "Question A"}],
        )
        config = {
            "sources": [
                {
                    "path": str(source_path),
                    "name": "source_a",
                    "authority": "supplementary",
                }
            ]
        }
        merged, quarantined, audit_log = merge_scaffold.run_merge(config)

        merged_path = TEST_DATA_DIR / "merged_records.json"
        audit_path = TEST_DATA_DIR / "merge_audit.log"
        merge_scaffold.export_records(merged, merged_path)
        merge_scaffold.export_audit_log(audit_log, audit_path)

        exported = json.loads(merged_path.read_text(encoding="utf-8"))
        audit_text = audit_path.read_text(encoding="utf-8")

        self.assertEqual(1, len(merged))
        self.assertEqual(0, len(quarantined))
        self.assertEqual(1, len(exported))
        self.assertIn("transformation_notes", exported[0])
        self.assertIn("Inserted source_a:1", audit_text)

    def test_normalize_source_processes_all_records(self):
        raw_records = [
            {"id": "1", "content": "Question one"},
            {"id": "2", "content": "Question two"},
            {"id": "3", "content": "Question three"},
        ]

        records = merge_scaffold.normalize_source(raw_records, "source_a", "supplementary")

        self.assertEqual(3, len(records))
        self.assertEqual("Question one", records[0].content)
        self.assertEqual("source_a", records[1].source_name)
        self.assertEqual("supplementary", records[2].authority)

    def test_choose_preferred_record_keeps_existing_when_candidate_has_lower_authority(self):
        existing = merge_scaffold.MergeRecord(
            record_id="1",
            content="question",
            source_name="auth_source",
            source_record_id="A1",
            authority="authoritative",
            payload={},
        )
        candidate = merge_scaffold.MergeRecord(
            record_id="2",
            content="question",
            source_name="legacy_source",
            source_record_id="L1",
            authority="legacy",
            payload={},
        )

        chosen, rejected, note = merge_scaffold.choose_preferred_record(existing, candidate)

        self.assertIs(existing, chosen)
        self.assertIs(candidate, rejected)
        self.assertIn("Kept existing", note)

    def test_merge_records_replaces_existing_with_higher_authority_source(self):
        legacy = merge_scaffold.MergeRecord(
            record_id="1",
            content="same question",
            source_name="legacy_source",
            source_record_id="L1",
            authority="legacy",
            payload={},
        )
        authoritative = merge_scaffold.MergeRecord(
            record_id="2",
            content="Same Question",
            source_name="auth_source",
            source_record_id="A1",
            authority="authoritative",
            payload={},
        )

        merged, quarantined, audit_log = merge_scaffold.merge_records([legacy, authoritative])

        self.assertEqual(1, len(merged))
        self.assertEqual(0, len(quarantined))
        self.assertEqual("auth_source", merged[0].source_name)

    def test_merge_records_empty_input_returns_empty_results(self):
        merged, quarantined, audit_log = merge_scaffold.merge_records([])

        self.assertEqual([], merged)
        self.assertEqual([], quarantined)
        self.assertEqual([], audit_log)

    def test_load_merge_config_returns_valid_config(self):
        config_path = self.write_json(
            "merge_config.json",
            {
                "sources": [
                    {"path": "source.json", "name": "src", "authority": "supplementary"}
                ],
                "output_dir": "merge_output",
            },
        )

        config = merge_scaffold.load_merge_config(config_path)

        self.assertIn("sources", config)
        self.assertEqual(1, len(config["sources"]))
        self.assertEqual("merge_output", config.get("output_dir"))


class EndToEndExamFlowTests(unittest.TestCase):
    """Integration-style tests for storage-built exams executed through the domain model."""

    def setUp(self):
        TEST_DATA_DIR.mkdir(exist_ok=True)

    def tearDown(self):
        if TEST_DATA_DIR.exists():
            for path in TEST_DATA_DIR.iterdir():
                if path.is_file():
                    path.unlink()

    def test_build_exam_answer_and_persist_history_flow(self):
        question_bank = [
            {
                "q": "Question 1",
                "options": ["A", "B", "C", "D"],
                "answer": "A",
                "explanation": "A is correct.",
                "source": "Fixture",
            },
            {
                "q": "Question 2",
                "options": ["A", "B", "C", "D"],
                "answer": "C",
                "explanation": "C is correct.",
                "source": "Fixture",
            },
        ]
        questions = exam_storage.build_exam_questions(question_bank, exam_question_count=2)
        session = exam_models.ExamSession(questions, duration_seconds=120)
        for index, question in enumerate(questions):
            session.jump_to_question(index)
            session.save_answer(question["answer"])

        result = session.submit()
        history_entry = exam_storage.build_history_entry(
            result,
            timestamp=datetime(2026, 5, 12, 9, 30, 0),
        )

        self.assertEqual(2, result.score)
        self.assertTrue(result.passed)
        self.assertEqual("PASS", history_entry["result"])
        self.assertEqual("2026-05-12 09:30:00", history_entry["timestamp"])

    def test_all_wrong_answers_produce_fail_entry(self):
        question_bank = [
            {
                "q": "Question 1",
                "options": ["A", "B", "C", "D"],
                "answer": "A",
                "explanation": "A is correct.",
            },
            {
                "q": "Question 2",
                "options": ["A", "B", "C", "D"],
                "answer": "A",
                "explanation": "A is correct.",
            },
        ]
        questions = exam_storage.build_exam_questions(question_bank, exam_question_count=2)
        session = exam_models.ExamSession(questions, duration_seconds=120)
        for index in range(len(questions)):
            session.jump_to_question(index)
            session.save_answer("D")

        result = session.submit()
        history_entry = exam_storage.build_history_entry(result)

        self.assertEqual(0, result.score)
        self.assertFalse(result.passed)
        self.assertEqual("FAIL", history_entry["result"])

    def test_history_save_load_round_trip_with_result(self):
        history_path = TEST_DATA_DIR / "exam_history.json"
        result = exam_models.ExamResult(
            score=30, total=40, percent=75.0, passed=True, report=""
        )
        entry = exam_storage.build_history_entry(result, timestamp=datetime(2026, 5, 12, 10, 0, 0))

        exam_storage.save_history([entry], history_path)
        loaded = exam_storage.load_history(history_path)

        self.assertEqual(1, len(loaded))
        self.assertEqual(30, loaded[0]["score"])
        self.assertEqual("PASS", loaded[0]["result"])
        self.assertEqual("2026-05-12 10:00:00", loaded[0]["timestamp"])


if __name__ == "__main__":
    unittest.main()
