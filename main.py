"""The Funniest Sick-Day Excuse — make.fun entry (program/v1).

Writes a single-line sick-day excuse (1-200 characters, UTF-8) to
``$MAKEFUN_OUTPUT_DIR/entry.txt``.

The line was written against the published judge brief, most important
first: (1) a reason a boss might half believe (a back gone out) that a
coworker would laugh at; (2) a fresh idea, not a fever, a dog or a dead
grandmother; (3) the twist lands at the end ("tiny landlord collecting
rent"); (4) it reads like a real person typing a message; (5) no wasted
words. One line, well under 200 characters.

Run (as the grader does)::

    python3 -P -s main.py

Deterministic: the same excuse is written on every run.
"""

import os
import sys

MAX_CHARS = 200
MIN_CHARS = 1

EXCUSE = (
    "Sorry, can't come in today \u2014 my back went out this morning and "
    "my cat has taken it as a sign to sit on my chest like a tiny "
    "landlord collecting rent."
)


def resolve_output_dir():
    """Return the output directory.

    The grader sets MAKEFUN_OUTPUT_DIR; fall back to a local ./output
    directory so the program is runnable by hand.
    """
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output")


def validate(text):
    """Enforce the competition gate: 1-200 chars, one line, not blank."""
    if not isinstance(text, str):
        raise ValueError("excuse must be a string")
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("excuse must not contain control characters")
    if "\t" in text:
        raise ValueError("excuse must not contain tabs")
    stripped = text.strip()
    if not stripped:
        raise ValueError("excuse must not be only whitespace")
    if len(text) != len(stripped):
        raise ValueError("excuse must not have leading/trailing whitespace")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            "excuse must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    text.encode("utf-8")  # must be valid UTF-8 text
    return text


def main():
    excuse = validate(EXCUSE)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(excuse + "\n")
    # Dev-run log only; the grader keeps stdout/stderr to itself.
    print("wrote %s (%d characters)" % (path, len(excuse)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
