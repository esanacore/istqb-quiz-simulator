"""Interactive command-line quiz runner for ISTQB CTFL practice."""

from __future__ import annotations

import math
import os
import shutil
import textwrap
import time
from json import JSONDecodeError

from exam_models import PASSING_PERCENT, ExamSession
from exam_storage import (
    EXAM_QUESTION_COUNT,
    HISTORY_PATH,
    QUESTION_BANK_PATH,
    build_history_entry,
    build_exam_questions,
    history_entries_newest_first,
    load_history,
    load_questions,
    save_history,
)

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"


def supports_ansi():
    """Return True when the current output stream is likely ANSI-capable."""
    return os.getenv("TERM") is not None or os.name == "nt"


def style(text, *codes):
    """Wrap text in ANSI sequences when available."""
    if not supports_ansi():
        return text
    return "".join(codes) + text + RESET


def format_duration(seconds):
    """Format a remaining-second count as MM:SS."""
    minutes, remainder = divmod(max(0, int(seconds)), 60)
    return f"{minutes:02d}:{remainder:02d}"


def parse_answer_token(command, option_count):
    """Parse an answer command into a zero-based option index."""
    normalized = command.strip().lower()
    if not normalized:
        return None

    if normalized in {"a", "b", "c", "d"}:
        index = ord(normalized) - ord("a")
        return index if index < option_count else None

    if normalized.isdigit():
        index = int(normalized) - 1
        return index if 0 <= index < option_count else None

    return None


def build_progress_bar(answered, total, width=28):
    """Build a fixed-width textual progress bar."""
    if total <= 0:
        return "[" + ("-" * width) + "]"

    filled = math.floor((answered / total) * width)
    filled = max(0, min(width, filled))
    return "[" + ("#" * filled) + ("-" * (width - filled)) + "]"


def build_question_map(session, columns=10):
    """Render a compact question map for the CLI."""
    tokens = []
    for index in range(len(session.questions)):
        label = f"{index + 1:02d}"
        if index == session.current_q:
            token = f"[{label}]"
        elif session.marked_for_review[index]:
            token = f"!{label}!"
        elif session.user_answers[index] is not None:
            token = f" {label}*"
        else:
            token = f" {label}."
        tokens.append(token)

    rows = []
    for start in range(0, len(tokens), columns):
        rows.append(" ".join(tokens[start : start + columns]))
    return "\n".join(rows)


def build_review_text(session, index):
    """Build a focused review block for one submitted question."""
    question = session.questions[index]
    user_pick = session.user_answers[index]
    is_correct = user_pick == question["answer"]
    status = "CORRECT" if is_correct else "WRONG"

    lines = [
        f"Question {index + 1}/{len(session.questions)}: {status}",
        "",
        question["q"],
        "",
        f"Your Answer: {user_pick}",
        f"Correct Answer: {question['answer']}",
        f"Explanation: {question['explanation']}",
    ]
    if question.get("source"):
        lines.append(f"Source: {question['source']}")
    if question.get("topic"):
        lines.append(f"Topic: {question['topic']}")
    if question.get("lo"):
        lines.append(f"Learning Objective: {question['lo']}")
    return "\n".join(lines)


class ISTQBQuizCLI:
    """Terminal interface for the ISTQB practice simulator."""

    def __init__(self):
        self.question_bank = load_questions(QUESTION_BANK_PATH)
        self.history = load_history(HISTORY_PATH)
        self.questions = build_exam_questions(self.question_bank, EXAM_QUESTION_COUNT)
        self.session = ExamSession(self.questions)
        self.exam_submitted = False
        self.last_result = None
        self.last_timer_sync = time.monotonic()

    def reset_timer_anchor(self):
        """Reset the timer sync anchor after a session state change."""
        self.last_timer_sync = time.monotonic()

    def sync_timer(self):
        """Apply elapsed wall-clock time to the current exam session."""
        if self.exam_submitted:
            return

        now = time.monotonic()
        elapsed = int(now - self.last_timer_sync)
        if elapsed > 0:
            self.session.advance_time(elapsed)
            self.last_timer_sync += elapsed

    def clear_screen(self):
        """Clear the terminal for a fresh render."""
        if supports_ansi():
            print("\033[2J\033[H", end="")
        else:
            os.system("cls" if os.name == "nt" else "clear")

    def terminal_width(self):
        """Return the active terminal width with a safe fallback."""
        return shutil.get_terminal_size((100, 40)).columns

    def prompt(self, message):
        """Collect a line of input after syncing the timer once more."""
        self.sync_timer()
        if not self.exam_submitted and self.session.time_left == 0:
            self.submit_exam(timed_out=True)
            return ""
        return input(message).strip()

    def pause(self, message="Press Enter to continue..."):
        """Wait for the user to acknowledge the current screen."""
        input(message)

    def render(self):
        """Render the current quiz state."""
        self.sync_timer()
        if not self.exam_submitted and self.session.time_left == 0:
            self.submit_exam(timed_out=True)
            return

        if self.exam_submitted:
            self.render_completed_state()
            return

        width = self.terminal_width()
        rule = "═" * min(width, 100)
        answered = self.session.answered_count()
        marked = self.session.marked_count()
        remaining = self.session.remaining_count()
        question = self.session.questions[self.session.current_q]

        self.clear_screen()
        print(style("ISTQB CTFL v4.0 CLI Simulator", BOLD, CYAN))
        print(rule)
        print(
            f"Question {self.session.current_q + 1}/{len(self.session.questions)}  "
            f"Time {style(format_duration(self.session.time_left), BOLD, YELLOW)}  "
            f"Target {PASSING_PERCENT:.0f}%"
        )
        print(
            f"{build_progress_bar(answered, len(self.session.questions))}  "
            f"Answered {answered}  Marked {marked}  Remaining {remaining}"
        )
        print()

        wrapped_question = textwrap.fill(
            question["q"],
            width=max(50, min(width - 4, 92)),
        )
        print(style(wrapped_question, BOLD))
        print()

        current_answer = self.session.user_answers[self.session.current_q]
        for index, option in enumerate(question["options"]):
            label = chr(ord("A") + index)
            marker = "●" if option == current_answer else "○"
            prefix = style(f"{marker} {label}.", GREEN if option == current_answer else DIM)
            wrapped_option = textwrap.fill(
                option,
                width=max(42, min(width - 10, 86)),
                subsequent_indent=" " * 6,
            )
            print(f"{prefix} {wrapped_option}")

        if self.session.marked_for_review[self.session.current_q]:
            print()
            print(style("Marked for review", BOLD, MAGENTA))

        print()
        print(style("Question Map", BOLD))
        print(build_question_map(self.session))
        print()
        print(
            "Commands: "
            "A-D/1-4 answer | next | prev | jump <n> | mark | clear | summary | "
            "history | submit | restart | help | quit"
        )

    def render_completed_state(self):
        """Render the post-submit command screen."""
        result_text = "PASS" if self.last_result and self.last_result.passed else "FAIL"
        color = GREEN if self.last_result and self.last_result.passed else RED
        self.clear_screen()
        print(style("ISTQB CTFL v4.0 CLI Simulator", BOLD, CYAN))
        print("═" * min(self.terminal_width(), 100))
        if self.last_result is not None:
            print(
                style(
                    (
                        f"Final Score {self.last_result.score}/{self.last_result.total}  "
                        f"({self.last_result.percent:.2f}%)  {result_text}"
                    ),
                    BOLD,
                    color,
                )
            )
            print()
            print("Use `review` for the full explanation report.")
        print("Commands: review | history | restart | help | quit")

    def show_help(self):
        """Display the CLI command reference."""
        self.clear_screen()
        print(style("CLI Commands", BOLD, CYAN))
        print("A-D or 1-4: answer the current question")
        print("next / prev: move between questions")
        print("jump 12: go directly to question 12")
        print("mark: toggle mark-for-review on the current question")
        print("clear: clear the current answer")
        print("summary: show answered, marked, and unanswered counts")
        print("history: show stored exam history")
        print("clear-history: delete all stored exam history")
        print("submit: finish the exam and score it")
        print("restart: start a fresh randomized exam")
        print("review: inspect explanations after submission")
        print("quit: exit the CLI")
        print()
        self.pause()

    def show_history(self):
        """Display persisted history entries."""
        self.clear_screen()
        print(style("Attempt History", BOLD, CYAN))
        if not self.history:
            print("No stored attempts yet.")
            print()
            self.pause()
            return

        for index, entry in history_entries_newest_first(self.history)[:10]:
            print(
                f"{index + 1:02d}. {entry['timestamp']}  "
                f"{entry['score']}/{entry['total']}  "
                f"{entry['percent']:.2f}%  {entry['result']}"
            )
        print()
        self.pause()

    def clear_history(self):
        """Clear all stored history after confirmation."""
        if not self.history:
            self.clear_screen()
            print("No stored attempts to clear.")
            print()
            self.pause()
            return

        command = self.prompt("Delete all stored history? [y/N]: ").lower()
        if command in {"y", "yes"}:
            self.history.clear()
            save_history(self.history, HISTORY_PATH)

    def show_summary(self):
        """Display attempt status details."""
        unanswered = [
            str(index + 1)
            for index, answer in enumerate(self.session.user_answers)
            if answer is None
        ]
        marked = [
            str(index + 1)
            for index, is_marked in enumerate(self.session.marked_for_review)
            if is_marked
        ]

        self.clear_screen()
        print(style("Attempt Summary", BOLD, CYAN))
        print(
            f"Answered {self.session.answered_count()} / {len(self.session.questions)} | "
            f"Marked {self.session.marked_count()} | "
            f"Remaining {self.session.remaining_count()}"
        )
        print(f"Unanswered: {', '.join(unanswered) if unanswered else 'None'}")
        print(f"Marked: {', '.join(marked) if marked else 'None'}")
        print()
        self.pause()

    def append_history(self):
        """Persist the latest exam attempt."""
        self.history.append(build_history_entry(self.last_result))
        save_history(self.history, HISTORY_PATH)

    def show_review(self):
        """Display a navigable post-exam review."""
        if self.last_result is None:
            self.clear_screen()
            print("No completed exam to review yet.")
            print()
            self.pause()
            return

        review_index = 0
        while True:
            self.clear_screen()
            print(style("Detailed Review", BOLD, CYAN))
            print(build_review_text(self.session, review_index))
            print()
            print("Commands: next | prev | jump <n> | missed | marked | all | close")
            command = input("review> ").strip().lower()
            if command in {"", "next"}:
                review_index = min(len(self.session.questions) - 1, review_index + 1)
            elif command == "prev":
                review_index = max(0, review_index - 1)
            elif command.startswith("jump "):
                _, _, raw_index = command.partition(" ")
                if raw_index.isdigit():
                    review_index = max(0, min(len(self.session.questions) - 1, int(raw_index) - 1))
            elif command == "missed":
                missed_indexes = [
                    index
                    for index, question in enumerate(self.session.questions)
                    if self.session.user_answers[index] != question["answer"]
                ]
                if missed_indexes:
                    review_index = missed_indexes[0]
            elif command == "marked":
                marked_indexes = [
                    index
                    for index, is_marked in enumerate(self.session.marked_for_review)
                    if is_marked
                ]
                if marked_indexes:
                    review_index = marked_indexes[0]
            elif command == "all":
                self.clear_screen()
                print(style("Full Review", BOLD, CYAN))
                print(self.last_result.report)
                print()
                self.pause()
            elif command in {"close", "quit", "q"}:
                return

    def submit_exam(self, timed_out=False):
        """Submit the active exam and show the score summary."""
        if self.exam_submitted:
            return

        self.sync_timer()
        self.exam_submitted = True
        self.last_result = self.session.submit()
        result_text = "PASS" if self.last_result.passed else "FAIL"
        self.append_history()

        self.clear_screen()
        banner_color = GREEN if self.last_result.passed else RED
        heading = "TIME EXPIRED" if timed_out else "EXAM COMPLETE"
        print(style(heading, BOLD, banner_color))
        print(
            style(
                (
                    f"Score {self.last_result.score}/{self.last_result.total}  "
                    f"({self.last_result.percent:.2f}%)  {result_text}"
                ),
                BOLD,
                banner_color,
            )
        )
        print()
        print("Commands: review | history | restart | quit")
        print()
        self.pause()

    def confirm_submit(self):
        """Ask for confirmation before scoring the exam."""
        unanswered = self.session.remaining_count()
        marked = self.session.marked_count()
        command = self.prompt(
            f"Submit exam? unanswered={unanswered}, marked={marked} [y/N]: "
        ).lower()
        if command in {"y", "yes"}:
            self.submit_exam()

    def restart_exam(self):
        """Start a new randomized exam attempt."""
        self.questions = build_exam_questions(self.question_bank, EXAM_QUESTION_COUNT)
        self.session.restart(self.questions)
        self.exam_submitted = False
        self.last_result = None
        self.reset_timer_anchor()

    def handle_active_command(self, command):
        """Process commands while an exam is in progress."""
        answer_index = parse_answer_token(command, len(self.session.questions[self.session.current_q]["options"]))
        if answer_index is not None:
            option = self.session.questions[self.session.current_q]["options"][answer_index]
            self.session.save_answer(option)
            return True

        if command == "next":
            self.session.next_q()
            return True
        if command == "prev":
            self.session.prev_q()
            return True
        if command.startswith("jump "):
            _, _, raw_index = command.partition(" ")
            if raw_index.isdigit():
                self.session.jump_to_question(int(raw_index) - 1)
            return True
        if command == "mark":
            self.session.toggle_mark()
            return True
        if command == "clear":
            self.session.save_answer("")
            return True
        if command == "summary":
            self.show_summary()
            return True
        if command == "history":
            self.show_history()
            return True
        if command == "clear-history":
            self.clear_history()
            return True
        if command == "submit":
            self.confirm_submit()
            return True
        if command == "restart":
            restart = self.prompt("Start a new randomized exam? [y/N]: ").lower()
            if restart in {"y", "yes"}:
                self.restart_exam()
            return True
        if command == "help":
            self.show_help()
            return True
        if command == "quit":
            confirm = self.prompt("Exit without submitting the current exam? [y/N]: ").lower()
            if confirm in {"y", "yes"}:
                raise SystemExit(0)
            return True
        return False

    def handle_post_submit_command(self, command):
        """Process commands after an exam has already been submitted."""
        if command == "review":
            self.show_review()
            return True
        if command == "history":
            self.show_history()
            return True
        if command == "clear-history":
            self.clear_history()
            return True
        if command == "restart":
            self.restart_exam()
            return True
        if command == "help":
            self.show_help()
            return True
        if command == "quit":
            raise SystemExit(0)
        return False

    def run(self):
        """Run the interactive terminal application."""
        while True:
            self.render()
            command = self.prompt("> ").lower()
            if not command:
                continue

            if self.exam_submitted:
                handled = self.handle_post_submit_command(command)
            else:
                handled = self.handle_active_command(command)

            if not handled:
                self.clear_screen()
                print(f"Unknown command: {command}")
                print()
                self.pause()

def main():
    """Run the CLI simulator."""
    try:
        app = ISTQBQuizCLI()
        app.run()
    except (OSError, ValueError, JSONDecodeError) as exc:
        print(f"Unable to load quiz data: {exc}")
        return 1
    except KeyboardInterrupt:
        print()
        print("Exiting.")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
