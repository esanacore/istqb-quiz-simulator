"""Responsive layout helpers for the quiz interfaces."""

WIDE_LAYOUT = "wide"
COMPACT_LAYOUT = "compact"
COMPACT_LAYOUT_THRESHOLD = 1100


def determine_layout_mode(window_width):
    """Choose the main-window layout mode for a given width."""
    if window_width < COMPACT_LAYOUT_THRESHOLD:
        return COMPACT_LAYOUT
    return WIDE_LAYOUT


def compute_wrap_lengths(window_width, layout_mode):
    """Return wrap lengths for question, option, and sidebar text."""
    width = max(720, int(window_width))
    if layout_mode == WIDE_LAYOUT:
        question_wrap = max(440, width - 360)
        option_wrap = max(380, width - 420)
        sidebar_wrap = 180
    else:
        question_wrap = max(440, width - 120)
        option_wrap = max(380, width - 160)
        sidebar_wrap = max(260, width - 80)

    return {
        "question": question_wrap,
        "option": option_wrap,
        "sidebar": sidebar_wrap,
    }
