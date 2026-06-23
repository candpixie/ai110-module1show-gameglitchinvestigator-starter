"""Core game logic, refactored out of app.py so it can be unit-tested.

These functions are pure: no Streamlit, no session state, no UI strings beyond
the outcome label. The UI layer (app.py) decides how to render each outcome.
"""


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Hard":
        return 1, 100
    # Normal is the default.
    return 1, 50


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        # Accept "42" and "42.0" but coerce to a whole number.
        value = int(float(raw)) if "." in raw else int(raw)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome label.

    Returns one of: "Win", "Too High", "Too Low"

    # FIX: The starter compared ints against a stringified secret on every
    # other turn (TypeError branch), which made the hints lie. Logic now
    # works on plain ints only, so the comparison is always meaningful.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update the running score based on the outcome.

    # FIX: The starter awarded/penalised "Too High" guesses based on whether
    # the attempt number was even or odd, so the score swung randomly. Scoring
    # is now deterministic: you earn points only by winning, and earlier wins
    # are worth more. Wrong guesses never change the score.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)

    # "Too High" / "Too Low" / anything else: no change.
    return current_score
