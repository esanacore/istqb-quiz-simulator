"""Unit tests for quiz models and storage helpers.

Author: Eric Sanacore
Date: 2026-05-10
"""

import json
import unittest
from pathlib import Path

import exam_models
import exam_storage

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


if __name__ == "__main__":
    unittest.main()
