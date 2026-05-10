"""Persistence and exam-assembly helpers for the quiz simulator.

Author: Eric Sanacore
Date: 2026-05-10
"""

import json
import random
from copy import deepcopy
from pathlib import Path


QUESTION_BANK_PATH = Path(__file__).with_name("question_bank.json")
HISTORY_PATH = Path(__file__).with_name("exam_history.json")
EXAM_QUESTION_COUNT = 40


def load_questions(question_bank_path=QUESTION_BANK_PATH):
    """Load and validate the quiz question bank from JSON.

    Args:
        question_bank_path: Path to the question bank JSON file.

    Returns:
        A list of validated question dictionaries.

    Raises:
        ValueError: If the file content is structurally invalid.
    """
    with Path(question_bank_path).open("r", encoding="utf-8") as handle:
        questions = json.load(handle)

    if not isinstance(questions, list) or not questions:
        raise ValueError("Question bank must contain a non-empty list of questions.")

    for index, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            raise ValueError(f"Question {index} is not an object.")

        required_keys = {"q", "options", "answer", "explanation"}
        missing_keys = required_keys.difference(question)
        if missing_keys:
            missing = ", ".join(sorted(missing_keys))
            raise ValueError(f"Question {index} is missing required fields: {missing}.")

        options = question["options"]
        if not isinstance(options, list) or len(options) != 4:
            raise ValueError(f"Question {index} must contain exactly 4 answer options.")

        if question["answer"] not in options:
            raise ValueError(f"Question {index} answer must match one of its options.")

    return questions


def load_history(history_path=HISTORY_PATH):
    """Load persisted attempt history from disk.

    Args:
        history_path: Path to the history JSON file.

    Returns:
        A normalized list of history records.

    Raises:
        ValueError: If the file does not contain a list.
    """
    history_path = Path(history_path)
    if not history_path.exists():
        return []

    with history_path.open("r", encoding="utf-8") as handle:
        history = json.load(handle)

    if not isinstance(history, list):
        raise ValueError("Exam history must contain a list of attempts.")

    normalized_history = []
    for entry in history:
        if not isinstance(entry, dict):
            continue
        normalized_history.append(
            {
                "timestamp": str(entry.get("timestamp", "")),
                "score": int(entry.get("score", 0)),
                "total": int(entry.get("total", 0)),
                "percent": float(entry.get("percent", 0.0)),
                "result": str(entry.get("result", "")),
            }
        )

    return normalized_history


def save_history(history, history_path=HISTORY_PATH):
    """Persist attempt history to disk.

    Args:
        history: List of attempt-history dictionaries.
        history_path: Path to the history JSON file.
    """
    with Path(history_path).open("w", encoding="utf-8") as handle:
        json.dump(history, handle, indent=2)


def build_exam_questions(question_bank, exam_question_count=EXAM_QUESTION_COUNT):
    """Create a randomized exam subset with shuffled answer order.

    Args:
        question_bank: Source pool of validated questions.
        exam_question_count: Desired number of questions for one attempt.

    Returns:
        A new list of copied question dictionaries ready for one exam attempt.
    """
    exam_size = min(exam_question_count, len(question_bank))
    selected_questions = random.sample(question_bank, exam_size)
    exam_questions = []

    for question in selected_questions:
        shuffled_question = deepcopy(question)
        random.shuffle(shuffled_question["options"])
        exam_questions.append(shuffled_question)

    return exam_questions
