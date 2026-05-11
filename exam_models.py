"""Pure exam-domain models for the ISTQB quiz simulator.

Author: Eric Sanacore
Date: 2026-05-10
"""

from dataclasses import dataclass


@dataclass
class ExamResult:
    """Represents the outcome of a completed exam attempt.

    Attributes:
        score: Number of correctly answered questions.
        total: Total number of questions in the attempt.
        percent: Percentage score for the attempt.
        passed: Whether the result met the configured passing threshold.
        report: Human-readable review report shown in the results window.
    """

    score: int
    total: int
    percent: float
    passed: bool
    report: str


class ExamSession:
    """State machine for one exam attempt.

    This class intentionally has no Tkinter dependencies. It is responsible for
    navigation, answer persistence, mark-for-review behavior, restart behavior,
    countdown state, and score/report generation.

    Args:
        questions: Exam questions selected for the current attempt.
        duration_seconds: Total countdown time allocated to the attempt.
    """

    def __init__(self, questions, duration_seconds=60 * 60):
        self.questions = questions
        self.duration_seconds = duration_seconds
        self.restart()

    def restart(self, questions=None):
        """Reset the attempt to a pristine state.

        Args:
            questions: Optional replacement question set for the next attempt.
        """
        if questions is not None:
            self.questions = questions
        self.current_q = 0
        self.user_answers = [None] * len(self.questions)
        self.marked_for_review = [False] * len(self.questions)
        self.time_left = self.duration_seconds
        self.submitted = False

    def advance_time(self, elapsed_seconds):
        """Decrease the remaining exam time by a whole-second amount.

        Args:
            elapsed_seconds: Number of elapsed seconds to subtract.
        """
        if self.submitted:
            return self.time_left

        elapsed_seconds = max(0, int(elapsed_seconds))
        self.time_left = max(0, self.time_left - elapsed_seconds)
        return self.time_left

    def save_answer(self, value):
        """Persist the current answer choice for the active question.

        Args:
            value: Selected answer text or an empty value to clear the answer.
        """
        if self.submitted:
            return
        self.user_answers[self.current_q] = value if value else None

    def next_q(self):
        """Advance to the next question when possible."""
        if self.submitted:
            return
        if self.current_q < len(self.questions) - 1:
            self.current_q += 1

    def prev_q(self):
        """Move back to the previous question when possible."""
        if self.submitted:
            return
        if self.current_q > 0:
            self.current_q -= 1

    def jump_to_question(self, index):
        """Jump directly to a question by index.

        Args:
            index: Zero-based question index.
        """
        if self.submitted:
            return
        if 0 <= index < len(self.questions):
            self.current_q = index

    def toggle_mark(self):
        """Toggle the mark-for-review flag on the active question."""
        if self.submitted:
            return
        self.marked_for_review[self.current_q] = not self.marked_for_review[self.current_q]

    def answered_count(self):
        """Return the number of answered questions."""
        return sum(1 for answer in self.user_answers if answer is not None)

    def marked_count(self):
        """Return the number of questions marked for review."""
        return sum(1 for mark in self.marked_for_review if mark)

    def remaining_count(self):
        """Return the number of unanswered questions."""
        return len(self.questions) - self.answered_count()

    def build_result(self):
        """Create a score summary and detailed review report."""
        score = 0
        report = "--- EXAM REVIEW ---\n\n"

        for index, question in enumerate(self.questions):
            user_pick = self.user_answers[index]
            is_correct = user_pick == question["answer"]
            if is_correct:
                score += 1

            status = "CORRECT" if is_correct else "WRONG"
            report += f"Q{index + 1}: {status}\n"
            report += f"Your Answer: {user_pick}\n"
            report += f"Correct Answer: {question['answer']}\n"
            report += f"Explanation: {question['explanation']}\n"
            if question.get("source"):
                report += f"Source: {question['source']}\n"
            if question.get("topic"):
                report += f"Topic: {question['topic']}\n"
            if question.get("lo"):
                report += f"Learning Objective: {question['lo']}\n"
            report += "-" * 30 + "\n"

        total = len(self.questions)
        percent = (score / total) * 100 if total else 0.0
        passed = percent >= 65
        return ExamResult(score=score, total=total, percent=percent, passed=passed, report=report)

    def submit(self):
        """Finalize the attempt and return its result."""
        if self.submitted:
            return self.build_result()
        self.submitted = True
        return self.build_result()
