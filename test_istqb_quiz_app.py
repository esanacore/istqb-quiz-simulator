"""Unit tests for quiz models and storage helpers.

Author: Eric Sanacore
Date: 2026-05-10
"""

import json
import unittest
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


class CliHelperTests(unittest.TestCase):
    """Tests for the command-line helper functions."""

    def test_parse_answer_token_supports_letters_and_numbers(self):
        self.assertEqual(0, cli_quiz.parse_answer_token("A", 4))
        self.assertEqual(2, cli_quiz.parse_answer_token("3", 4))
        self.assertIsNone(cli_quiz.parse_answer_token("9", 4))
        self.assertIsNone(cli_quiz.parse_answer_token("next", 4))

    def test_format_duration_and_progress_bar(self):
        self.assertEqual("02:05", cli_quiz.format_duration(125))
        self.assertEqual("[#####-----]", cli_quiz.build_progress_bar(2, 4, width=10))

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


class UiLayoutTests(unittest.TestCase):
    """Tests for responsive layout calculations."""

    def test_determine_layout_mode_switches_at_threshold(self):
        self.assertEqual(ui_layout.COMPACT_LAYOUT, ui_layout.determine_layout_mode(900))
        self.assertEqual(ui_layout.WIDE_LAYOUT, ui_layout.determine_layout_mode(1280))

    def test_compute_wrap_lengths_expands_in_compact_mode(self):
        compact = ui_layout.compute_wrap_lengths(900, ui_layout.COMPACT_LAYOUT)
        wide = ui_layout.compute_wrap_lengths(1200, ui_layout.WIDE_LAYOUT)

        self.assertGreater(compact["question"], wide["question"] - 100)
        self.assertGreaterEqual(compact["sidebar"], 260)
        self.assertGreater(wide["option"], 380)


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


if __name__ == "__main__":
    unittest.main()
