from logic_utils import (
    check_guess,
    parse_guess,
    update_score,
    get_range_for_difficulty,
)


# --- Starter tests: check_guess returns the right outcome label ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- New tests targeting the bugs we fixed ---

def test_check_guess_is_consistent():
    # BUG FIXED: the starter sometimes compared an int guess against a
    # stringified secret, flipping the hint. The outcome must stay correct.
    assert check_guess(60, 50) == "Too High"
    assert check_guess(40, 50) == "Too Low"


def test_score_does_not_swing_on_wrong_guesses():
    # BUG FIXED: "Too High" used to add or subtract 5 based on attempt parity,
    # so the score swung randomly. Wrong guesses should never change the score.
    assert update_score(20, "Too High", attempt_number=2) == 20
    assert update_score(20, "Too High", attempt_number=3) == 20
    assert update_score(20, "Too Low", attempt_number=4) == 20


def test_winning_earlier_scores_higher():
    # Winning on attempt 1 is worth more than winning on attempt 3.
    first_try = update_score(0, "Win", attempt_number=1)
    third_try = update_score(0, "Win", attempt_number=3)
    assert first_try == 100
    assert first_try > third_try
    # Score never drops below the 10-point floor.
    assert update_score(0, "Win", attempt_number=20) == 10


def test_parse_guess_handles_bad_input():
    assert parse_guess("") == (False, None, "Enter a guess.")
    assert parse_guess(None) == (False, None, "Enter a guess.")
    ok, value, err = parse_guess("abc")
    assert ok is False and err == "That is not a number."
    ok, value, err = parse_guess("42")
    assert ok is True and value == 42


def test_hard_range_is_wider_than_easy():
    # BUG FIXED: the starter made "Hard" a narrower range than "Normal".
    easy_low, easy_high = get_range_for_difficulty("Easy")
    hard_low, hard_high = get_range_for_difficulty("Hard")
    assert (hard_high - hard_low) > (easy_high - easy_low)
