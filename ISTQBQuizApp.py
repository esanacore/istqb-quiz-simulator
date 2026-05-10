"""Tkinter UI for the ISTQB CTFL quiz simulator.

Author: Eric Sanacore
Date: 2026-05-10

This module owns presentation, user interaction, and orchestration. Pure exam
state lives in ``exam_models.py`` and file-backed question/history operations
live in ``exam_storage.py``.
"""

from json import JSONDecodeError
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from exam_models import ExamSession
from exam_storage import (
    EXAM_QUESTION_COUNT,
    HISTORY_PATH,
    QUESTION_BANK_PATH,
    build_exam_questions,
    load_history,
    load_questions,
    save_history,
)

BG_COLOR = "#f4efe6"
PANEL_COLOR = "#fffaf2"
ACCENT_COLOR = "#1f5f5b"
ACCENT_SOFT = "#d7ebe6"
TEXT_COLOR = "#1f2933"
MUTED_TEXT = "#52606d"
WARNING_COLOR = "#a16207"
SUCCESS_COLOR = "#2f855a"
REVIEW_BG = "#fff1bf"
NAV_CURRENT = "#1f5f5b"
NAV_ANSWERED = "#d7ebe6"
NAV_MARKED = "#f6d365"
NAV_EMPTY = "#e5e7eb"


class ISTQBQuizApp:
    """Desktop quiz simulator for ISTQB Foundation Level practice.

    The class coordinates three concerns:

    1. Loading persistent data such as the question bank and exam history.
    2. Managing UI widgets and user interactions.
    3. Delegating exam state transitions to ``ExamSession``.

    Args:
        root: Root Tkinter window for the application.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("ISTQB CTFL v4.0 Simulator")
        self.root.geometry("920x720")
        self.root.minsize(860, 680)
        self.root.configure(bg=BG_COLOR)

        self.question_bank = self.load_questions()
        self.history = self.load_history()
        self.questions = self.build_exam_questions()
        self.session = ExamSession(self.questions)

        self.history_window = None
        self.history_tree = None
        self.navigator_buttons = []
        self.timer_running = True
        self.timer_job = None
        self.exam_submitted = False

        self.setup_ui()
        self.update_timer()
        self.load_question()

    def load_questions(self):
        """Load and validate the external question bank."""
        return load_questions(QUESTION_BANK_PATH)

    def load_history(self):
        """Load persisted attempt history from disk."""
        return load_history(HISTORY_PATH)

    def save_history(self):
        """Persist the current in-memory attempt history."""
        save_history(self.history, HISTORY_PATH)

    def build_exam_questions(self):
        """Create a randomized, shuffled exam attempt from the source bank."""
        return build_exam_questions(self.question_bank, EXAM_QUESTION_COUNT)

    def setup_ui(self):
        """Create and style the main application interface."""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "History.Treeview",
            background=PANEL_COLOR,
            fieldbackground=PANEL_COLOR,
            foreground=TEXT_COLOR,
            rowheight=28,
        )
        self.style.configure(
            "History.Treeview.Heading",
            background=ACCENT_SOFT,
            foreground=TEXT_COLOR,
            font=("Segoe UI", 10, "bold"),
        )
        self.style.map(
            "History.Treeview",
            background=[("selected", ACCENT_COLOR)],
            foreground=[("selected", "white")],
        )

        self.header = tk.Frame(self.root, bg=BG_COLOR)
        self.header.pack(fill="x", padx=22, pady=(18, 10))

        self.title_label = tk.Label(
            self.header,
            text="ISTQB CTFL v4.0 Simulator",
            font=("Georgia", 21, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = tk.Label(
            self.header,
            text="Randomized exam practice from official ISTQB sample materials",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=MUTED_TEXT,
        )
        self.subtitle_label.pack(anchor="w", pady=(3, 10))

        self.status_card = tk.Frame(
            self.header,
            bg=PANEL_COLOR,
            highlightbackground=ACCENT_SOFT,
            highlightthickness=1,
        )
        self.status_card.pack(fill="x")
        self.status_left = tk.Frame(self.status_card, bg=PANEL_COLOR)
        self.status_left.pack(side="left", padx=16, pady=12)
        self.status_right = tk.Frame(self.status_card, bg=PANEL_COLOR)
        self.status_right.pack(side="right", padx=16, pady=12)

        self.timer_label = tk.Label(
            self.status_right,
            text="",
            font=("Segoe UI", 12, "bold"),
            fg=WARNING_COLOR,
            bg=PANEL_COLOR,
        )
        self.timer_label.pack(anchor="e")

        self.session_label = tk.Label(
            self.status_left,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
        )
        self.session_label.pack(anchor="w")
        self.refresh_history_summary()

        self.bank_label = tk.Label(
            self.status_left,
            text=f"Bank: {len(self.question_bank)} Questions | Exam: {len(self.questions)} Randomized",
            font=("Segoe UI", 10),
            bg=PANEL_COLOR,
            fg=MUTED_TEXT,
        )
        self.bank_label.pack(anchor="w", pady=(4, 0))

        self.progress_label = tk.Label(
            self.status_right,
            text="",
            font=("Segoe UI", 10),
            bg=PANEL_COLOR,
            fg=MUTED_TEXT,
        )
        self.progress_label.pack(anchor="e", pady=(6, 0))

        self.content = tk.Frame(self.root, bg=BG_COLOR)
        self.content.pack(fill="both", expand=True, padx=22, pady=(4, 12))

        self.main_column = tk.Frame(self.content, bg=BG_COLOR)
        self.main_column.pack(side="left", fill="both", expand=True, padx=(0, 14))

        self.sidebar = tk.Frame(
            self.content,
            bg=PANEL_COLOR,
            highlightbackground=ACCENT_SOFT,
            highlightthickness=1,
            width=220,
        )
        self.sidebar.pack(side="right", fill="y")
        self.sidebar.pack_propagate(False)

        self.question_card = tk.Frame(
            self.main_column,
            bg=PANEL_COLOR,
            highlightbackground=ACCENT_SOFT,
            highlightthickness=1,
        )
        self.question_card.pack(fill="both", expand=True)

        self.q_num_label = tk.Label(
            self.question_card,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL_COLOR,
            fg=ACCENT_COLOR,
        )
        self.q_num_label.pack(anchor="w", padx=24, pady=(18, 6))

        self.q_label = tk.Label(
            self.question_card,
            text="",
            font=("Georgia", 16, "bold"),
            wraplength=760,
            justify="left",
            height=4,
            anchor="w",
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
        )
        self.q_label.pack(fill="x", padx=24, pady=(0, 18))

        self.var = tk.StringVar()
        self.option_buttons = []
        self.options_frame = tk.Frame(self.question_card, bg=PANEL_COLOR)
        self.options_frame.pack(fill="both", expand=True, padx=18, pady=(0, 12))
        for _ in range(4):
            button = tk.Radiobutton(
                self.options_frame,
                text="",
                variable=self.var,
                value="",
                font=("Segoe UI", 11),
                pady=12,
                padx=12,
                anchor="w",
                justify="left",
                wraplength=720,
                bg=PANEL_COLOR,
                fg=TEXT_COLOR,
                selectcolor=ACCENT_SOFT,
                activebackground=PANEL_COLOR,
                activeforeground=TEXT_COLOR,
                highlightthickness=0,
                relief="flat",
                bd=0,
            )
            button.pack(fill="x", anchor="w", padx=10, pady=4)
            self.option_buttons.append(button)

        self.setup_navigator()

        self.footer = tk.Frame(self.root, bg=BG_COLOR)
        self.footer.pack(fill="x", padx=22, pady=(0, 22))
        self.footer_bar = tk.Frame(
            self.footer,
            bg=PANEL_COLOR,
            highlightbackground=ACCENT_SOFT,
            highlightthickness=1,
        )
        self.footer_bar.pack(fill="x")

        self.back_btn = self._build_action_button(
            self.footer_bar,
            "<< Back",
            self.prev_q,
            bg=ACCENT_SOFT,
            fg=TEXT_COLOR,
        )
        self.back_btn.pack(side="left", padx=(14, 5), pady=12)

        self.mark_btn = self._build_action_button(
            self.footer_bar,
            "Mark for Review",
            self.toggle_mark,
            bg="#efe3b1",
            fg=TEXT_COLOR,
            width=16,
        )
        self.mark_btn.pack(side="left", padx=5, pady=12)

        self.next_btn = self._build_action_button(
            self.footer_bar,
            "Next >>",
            self.next_q,
            bg=ACCENT_SOFT,
            fg=TEXT_COLOR,
        )
        self.next_btn.pack(side="left", padx=5, pady=12)

        self.history_btn = self._build_action_button(
            self.footer_bar,
            "History",
            self.show_history_window,
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
            width=12,
        )
        self.history_btn.pack(side="right", padx=8, pady=12)

        self.submit_btn = self._build_action_button(
            self.footer_bar,
            "SUBMIT EXAM",
            self.confirm_submit,
            bg=ACCENT_COLOR,
            fg="white",
            activebackground="#184d49",
            activeforeground="white",
            width=15,
        )
        self.submit_btn.pack(side="right", padx=(8, 18), pady=12)

    def _build_action_button(
        self,
        parent,
        text,
        command,
        bg,
        fg,
        width=10,
        activebackground=None,
        activeforeground=None,
    ):
        """Create a consistently styled action button."""
        return tk.Button(
            parent,
            text=text,
            width=width,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=activebackground or bg,
            activeforeground=activeforeground or fg,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )

    def setup_navigator(self):
        """Build the question map used for direct question navigation."""
        title = tk.Label(
            self.sidebar,
            text="Question Map",
            font=("Georgia", 15, "bold"),
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
        )
        title.pack(anchor="w", padx=14, pady=(14, 6))

        subtitle = tk.Label(
            self.sidebar,
            text="Jump to any question and track answered or marked items.",
            font=("Segoe UI", 9),
            bg=PANEL_COLOR,
            fg=MUTED_TEXT,
            justify="left",
            wraplength=180,
        )
        subtitle.pack(anchor="w", padx=14, pady=(0, 10))

        self.legend_frame = tk.Frame(self.sidebar, bg=PANEL_COLOR)
        self.legend_frame.pack(fill="x", padx=14, pady=(0, 10))
        self.add_legend_item("Current", NAV_CURRENT)
        self.add_legend_item("Answered", NAV_ANSWERED)
        self.add_legend_item("Marked", NAV_MARKED)
        self.add_legend_item("Unanswered", NAV_EMPTY)

        self.navigator_frame = tk.Frame(self.sidebar, bg=PANEL_COLOR)
        self.navigator_frame.pack(fill="both", expand=True, padx=12, pady=(4, 10))

        columns = 5
        self.navigator_buttons = []
        for index in range(len(self.questions)):
            button = tk.Button(
                self.navigator_frame,
                text=str(index + 1),
                width=3,
                command=lambda idx=index: self.jump_to_question(idx),
                relief="flat",
                font=("Segoe UI", 9, "bold"),
                cursor="hand2",
            )
            row = index // columns
            column = index % columns
            button.grid(row=row, column=column, padx=4, pady=4, sticky="nsew")
            self.navigator_buttons.append(button)

        for column in range(columns):
            self.navigator_frame.grid_columnconfigure(column, weight=1)

        self.navigator_summary = tk.Label(
            self.sidebar,
            text="",
            font=("Segoe UI", 10),
            bg=PANEL_COLOR,
            fg=MUTED_TEXT,
            justify="left",
        )
        self.navigator_summary.pack(anchor="w", padx=14, pady=(0, 14))

    def add_legend_item(self, label_text, bg_color):
        """Add a labeled color swatch to the navigator legend."""
        row = tk.Frame(self.legend_frame, bg=PANEL_COLOR)
        row.pack(anchor="w", pady=2)
        swatch = tk.Label(row, text="  ", bg=bg_color, width=2, relief="flat")
        swatch.pack(side="left")
        label = tk.Label(
            row,
            text=label_text,
            font=("Segoe UI", 9),
            bg=PANEL_COLOR,
            fg=MUTED_TEXT,
        )
        label.pack(side="left", padx=8)

    def refresh_history_summary(self):
        """Update the high-level attempt/pass summary in the header."""
        passes = sum(1 for entry in self.history if entry["result"] == "PASS")
        self.session_label.config(text=f"History: {len(self.history)} Attempts ({passes} Pass)")

    def refresh_exam_progress(self):
        """Refresh progress metrics for the current exam attempt."""
        answered = self.session.answered_count()
        marked = self.session.marked_count()
        remaining = self.session.remaining_count()
        self.progress_label.config(
            text=f"Answered: {answered} | Marked: {marked} | Remaining: {remaining}"
        )
        self.navigator_summary.config(
            text=f"Answered: {answered}/{len(self.questions)}\nMarked for review: {marked}\nUnanswered: {remaining}"
        )

    def refresh_navigator(self):
        """Recolor question-map buttons to reflect current exam state."""
        for index, button in enumerate(self.navigator_buttons):
            if index == self.session.current_q:
                bg = NAV_CURRENT
                fg = "white"
            elif self.session.marked_for_review[index]:
                bg = NAV_MARKED
                fg = TEXT_COLOR
            elif self.session.user_answers[index] is not None:
                bg = NAV_ANSWERED
                fg = TEXT_COLOR
            else:
                bg = NAV_EMPTY
                fg = TEXT_COLOR

            button.config(bg=bg, fg=fg, activebackground=bg, activeforeground=fg)

        self.refresh_exam_progress()

    def jump_to_question(self, index):
        """Persist the current answer and navigate directly to a question."""
        if self.exam_submitted:
            return
        self.save_answer()
        self.session.jump_to_question(index)
        self.load_question()

    def add_history_entry(self, score, total, percent, result_text):
        """Append a completed attempt to persistent history."""
        self.history.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "score": score,
                "total": total,
                "percent": round(percent, 2),
                "result": result_text,
            }
        )
        self.save_history()
        self.refresh_history_summary()
        self.refresh_history_tree()

    def delete_history_entry(self):
        """Delete one or more selected history records from the table."""
        if self.history_tree is None:
            return

        selected_items = self.history_tree.selection()
        if not selected_items:
            messagebox.showinfo(
                "Delete History",
                "Select at least one history entry to remove.",
            )
            return

        if not messagebox.askyesno(
            "Delete History",
            "Remove the selected history entries?",
        ):
            return

        indexes = sorted((int(item) for item in selected_items), reverse=True)
        for index in indexes:
            if 0 <= index < len(self.history):
                del self.history[index]

        self.save_history()
        self.refresh_history_summary()
        self.refresh_history_tree()

    def refresh_history_tree(self):
        """Reload the history table with the current in-memory records."""
        if self.history_tree is None:
            return

        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        for index, entry in enumerate(self.history):
            self.history_tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    entry["timestamp"],
                    f"{entry['score']}/{entry['total']}",
                    f"{entry['percent']:.2f}%",
                    entry["result"],
                ),
            )

    def close_history_window(self):
        """Close the history popup and clear widget references."""
        if self.history_window is not None:
            self.history_window.destroy()
            self.history_window = None
            self.history_tree = None

    def show_history_window(self):
        """Open the history popup or focus it if already open."""
        if self.history_window is not None and self.history_window.winfo_exists():
            self.history_window.lift()
            return

        self.history_window = tk.Toplevel(self.root)
        self.history_window.title("Exam History")
        self.history_window.geometry("760x380")
        self.history_window.configure(bg=BG_COLOR)
        self.history_window.protocol("WM_DELETE_WINDOW", self.close_history_window)

        title = tk.Label(
            self.history_window,
            text="Attempt History",
            font=("Georgia", 18, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        )
        title.pack(anchor="w", padx=16, pady=(14, 8))

        columns = ("timestamp", "score", "percent", "result")
        self.history_tree = ttk.Treeview(
            self.history_window,
            columns=columns,
            show="headings",
            height=12,
            style="History.Treeview",
        )
        self.history_tree.heading("timestamp", text="Attempt Time")
        self.history_tree.heading("score", text="Score")
        self.history_tree.heading("percent", text="Percent")
        self.history_tree.heading("result", text="Result")
        self.history_tree.column("timestamp", width=220, anchor="w")
        self.history_tree.column("score", width=100, anchor="center")
        self.history_tree.column("percent", width=100, anchor="center")
        self.history_tree.column("result", width=100, anchor="center")
        self.history_tree.pack(fill="both", expand=True, padx=15, pady=15)

        button_frame = tk.Frame(self.history_window, bg=BG_COLOR)
        button_frame.pack(fill="x", padx=15, pady=(0, 15))
        self._build_action_button(
            button_frame,
            "Delete Selected",
            self.delete_history_entry,
            bg="#f3d9d9",
            fg=TEXT_COLOR,
            width=14,
            activebackground="#e8c2c2",
        ).pack(side="left")
        self._build_action_button(
            button_frame,
            "Close",
            self.close_history_window,
            bg=ACCENT_SOFT,
            fg=TEXT_COLOR,
            width=10,
            activebackground="#c3e0d9",
        ).pack(side="right")

        self.refresh_history_tree()

    def load_question(self):
        """Render the current question and apply its visual state."""
        question = self.questions[self.session.current_q]
        self.q_num_label.config(
            text=f"Question {self.session.current_q + 1} of {len(self.questions)}"
        )
        self.q_label.config(text=question["q"])

        for index, option in enumerate(question["options"]):
            self.option_buttons[index].config(text=option, value=option)

        current_answer = self.session.user_answers[self.session.current_q]
        self.var.set(current_answer if current_answer else "")

        if self.session.marked_for_review[self.session.current_q]:
            card_bg = REVIEW_BG
            mark_text = "Unmark"
            mark_bg = "#f2c94c"
        else:
            card_bg = PANEL_COLOR
            mark_text = "Mark for Review"
            mark_bg = "#efe3b1"

        self.question_card.config(bg=card_bg)
        self.options_frame.config(bg=card_bg)
        self.q_num_label.config(bg=card_bg)
        self.q_label.config(bg=card_bg)
        for button in self.option_buttons:
            button.config(bg=card_bg, activebackground=card_bg)
        self.mark_btn.config(text=mark_text, bg=mark_bg)

        self.refresh_navigator()

    def next_q(self):
        """Advance to the next question after saving the current answer."""
        if self.exam_submitted:
            return
        self.save_answer()
        self.session.next_q()
        self.load_question()

    def prev_q(self):
        """Go back to the previous question after saving the current answer."""
        if self.exam_submitted:
            return
        self.save_answer()
        self.session.prev_q()
        self.load_question()

    def save_answer(self):
        """Write the current radio-button selection into the session."""
        self.session.save_answer(self.var.get())

    def toggle_mark(self):
        """Toggle the mark-for-review flag on the current question."""
        if self.exam_submitted:
            return
        self.session.toggle_mark()
        self.load_question()

    def update_timer(self):
        """Update the countdown timer and trigger timeout submission."""
        self.timer_job = None
        if not self.timer_running or self.exam_submitted:
            return

        minutes, seconds = divmod(self.session.time_left, 60)
        self.timer_label.config(text=f"Time Remaining: {minutes:02d}:{seconds:02d}")

        if self.session.time_left == 0:
            self.timer_running = False
            self.show_results(timed_out=True)
            return

        self.session.time_left -= 1
        self.timer_job = self.root.after(1000, self.update_timer)

    def confirm_submit(self):
        """Ask the user for confirmation before final submission."""
        if self.exam_submitted:
            return
        self.save_answer()
        unanswered = self.session.user_answers.count(None)
        marked = self.session.marked_for_review.count(True)
        message = (
            "Are you sure you want to submit?\n\n"
            f"Unanswered: {unanswered}\n"
            f"Marked for Review: {marked}"
        )
        if messagebox.askyesno("Confirm Submission", message):
            self.show_results()

    def cancel_timer(self):
        """Cancel any pending Tkinter timer callback."""
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def set_exam_controls_state(self, state):
        """Enable or disable exam interaction controls."""
        for widget in (
            self.back_btn,
            self.next_btn,
            self.mark_btn,
            self.submit_btn,
            self.history_btn,
        ):
            widget.config(state=state)
        for button in self.option_buttons:
            button.config(state=state)
        for button in self.navigator_buttons:
            button.config(state=state)

    def show_results(self, timed_out=False):
        """Finalize the session and show the scored review report.

        Args:
            timed_out: True when the result window is being shown because the
                countdown reached zero.
        """
        if self.exam_submitted:
            return

        self.exam_submitted = True
        self.timer_running = False
        self.cancel_timer()
        if timed_out:
            self.timer_label.config(text="Time Remaining: 00:00")
        self.set_exam_controls_state(tk.DISABLED)

        result = self.session.submit()
        result_text = "PASS" if result.passed else "FAIL"
        self.add_history_entry(result.score, result.total, result.percent, result_text)

        result_window = tk.Toplevel(self.root)
        result_window.title("Results & Explanation")
        result_window.geometry("700x560")
        result_window.configure(bg=BG_COLOR)

        summary_text = (
            f"FINAL SCORE: {result.score}/{result.total} "
            f"({result.percent:.2f}%) - {result_text}"
        )
        if timed_out:
            summary_text = f"TIME EXPIRED\n{summary_text}"

        summary = tk.Label(
            result_window,
            text=summary_text,
            font=("Georgia", 16, "bold"),
            bg=BG_COLOR,
            fg=SUCCESS_COLOR if result.passed else WARNING_COLOR,
        )
        summary.pack(pady=(16, 12))

        text_area = scrolledtext.ScrolledText(
            result_window,
            wrap=tk.WORD,
            width=78,
            height=22,
            font=("Consolas", 10),
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
            relief="flat",
            bd=1,
        )
        text_area.insert(tk.INSERT, result.report)
        text_area.config(state=tk.DISABLED)
        text_area.pack(padx=20, pady=10, fill="both", expand=True)

        button_frame = tk.Frame(result_window, bg=BG_COLOR)
        button_frame.pack(fill="x", padx=20, pady=(0, 16))
        self._build_action_button(
            button_frame,
            "Restart Test",
            lambda: self.restart_test(result_window),
            bg=ACCENT_COLOR,
            fg="white",
            width=12,
            activebackground="#184d49",
            activeforeground="white",
        ).pack(side="left")
        self._build_action_button(
            button_frame,
            "Close Simulator",
            self.root.destroy,
            bg=ACCENT_SOFT,
            fg=TEXT_COLOR,
            width=14,
            activebackground="#c3e0d9",
        ).pack(side="right")

    def restart_test(self, result_window):
        """Close the result window and begin a fresh randomized attempt."""
        result_window.destroy()
        self.cancel_timer()
        self.questions = self.build_exam_questions()
        self.session.restart(self.questions)
        self.timer_running = True
        self.exam_submitted = False
        self.var.set("")
        self.bank_label.config(
            text=f"Bank: {len(self.question_bank)} Questions | Exam: {len(self.questions)} Randomized"
        )
        self.set_exam_controls_state(tk.NORMAL)
        self.update_timer()
        self.load_question()


def main():
    """Run the desktop application."""
    root = tk.Tk()
    try:
        ISTQBQuizApp(root)
    except (OSError, ValueError, JSONDecodeError) as exc:
        messagebox.showerror(
            "Question Bank Error",
            f"Unable to load application data.\n\n{exc}",
        )
        root.destroy()
    else:
        root.mainloop()


if __name__ == "__main__":
    main()
