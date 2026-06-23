# Game Glitch Investigator: The Impossible Guesser

## The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

This repo is my **fixed** version: the logic has been refactored into
`logic_utils.py`, the broken hints and scoring are repaired, and the game is
covered by automated tests.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`
3. Run the tests: `pytest`

## Bugs Found and Fixed

1. **Hints lied (wrong direction).** "Too High" told you to go HIGHER. Fixed the
   hint text in `app.py` so directions are correct.
2. **Secret flipped type every other turn.** `app.py` stringified the secret on
   even attempts, forcing a broken string comparison in `check_guess`. Removed it.
3. **Score went haywire.** "Too High" added or subtracted points based on attempt
   parity. Scoring is now deterministic: points only on a win, earlier wins worth more.
4. **"New Game" never reset the game.** `status` and `score` were never cleared, so
   after one win/loss the game stayed over forever. New Game now fully resets state.
5. **"Hard" was easier than "Normal."** Hard used a narrower number range. Fixed the
   difficulty ranges so Hard is genuinely the widest.

## Document Your Experience

- **Purpose:** A Streamlit number-guessing game. The player guesses a secret number
  within an attempt limit, gets higher/lower hints, and earns a score for winning.
- **Bugs found:** Backwards/flipping hints, randomly swinging score, a "New Game"
  button that did not restart, and difficulty ranges that were backwards. See above.
- **Fixes applied:** Refactored `get_range_for_difficulty`, `parse_guess`,
  `check_guess`, and `update_score` into `logic_utils.py` as pure functions, repaired
  each bug, and added pytest coverage for every fix.

## Demo Walkthrough

A sample game on **Normal** difficulty (range 1 to 50), secret number 30:

1. User enters a guess of 40, game returns "Too high. Go LOWER!"
2. User enters a guess of 20, game returns "Too low. Go HIGHER!"
3. User enters a guess of 30, game returns "Correct!" and balloons appear.
4. Score updates only on the win, and earlier wins are worth more points.
5. "Attempts left" counts down correctly with each guess.
6. Clicking "New Game" fully resets the board: new secret, score back to 0,
   and the game is playable again instead of staying stuck on "game over".

## Test Results

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
collected 8 items

tests/test_game_logic.py ........                                        [100%]

============================== 8 passed in 0.01s ===============================
```

## Stretch Features

- [ ] (Optional) Enhanced UI changes can go here.
