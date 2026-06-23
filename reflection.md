# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game it looked playable, but the feedback could not be trusted. The hint arrows pointed the wrong way, so a guess that was too high told me to "Go HIGHER", and on top of that the hint seemed to flip every other turn so the same guess gave different advice. The score also moved around in a way I could not predict, sometimes going up and sometimes down for what looked like the same kind of wrong guess. The biggest problem was that "New Game" did not actually start a new game once I had won or lost, the app stayed stuck on the game-over screen.

Two concrete bugs I noticed first:
- The hints lied: "Too High" told me to go higher instead of lower.
- The game never really ended/restarted: after a win or loss, "New Game" left the score and the "game over" state in place.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Secret 50, guess 60 | Hint says "too high, go lower" | Hint said "📈 Go HIGHER!" (wrong direction) | none (silent logic bug) |
| Secret 50, guess 50 on an even-numbered attempt | "Correct! You win" | Compared int 50 against string "50", so it never matched and the hint lied | none (hit the TypeError fallback branch and string-compared) |
| Two "Too High" guesses in a row | Score changes the same way both times | Score went +5 on one attempt and -5 on the next, based only on whether the attempt number was even or odd | none |
| Click "New Game" after winning | Fresh board, score 0, can play again | Stayed on "You already won" screen, old score carried over | none (status and score were never reset) |
| Difficulty "Hard" | Hard should use the widest range | Hard used 1 to 50, which was narrower than Normal's 1 to 100, so "Hard" was actually easier | none |

---

## 2. How did you use AI as a teammate?

I used my AI coding assistant inside VS Code (Claude) to explain the buggy logic and to help me refactor the game logic out of `app.py` into `logic_utils.py`.

- **A correct suggestion:** The AI pointed out that `app.py` was stringifying the secret on every even attempt (`secret = str(st.session_state.secret)`), which forced `check_guess` into its `TypeError` fallback and made it compare a number against text. I verified this by reading the code path and by writing a test that calls `check_guess(60, 50)` and `check_guess(40, 50)` directly, both now return the correct label, so removing the string conversion fixed it.
- **A misleading suggestion:** At one point the AI suggested I could "just sort the score logic by always adding 5 for any guess." That was wrong, because it would let you farm points by guessing forever and never actually reflected getting closer. I rejected it and instead made wrong guesses leave the score unchanged and only award points on a win, which I confirmed with `test_score_does_not_swing_on_wrong_guesses`.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed only when I could see it pass both in a test and in the live game. For the hint bug, I ran `pytest` and watched `test_check_guess_is_consistent` go green, then ran `streamlit run app.py` and confirmed a too-high guess now tells me to go lower. The most useful test was `test_score_does_not_swing_on_wrong_guesses`, because it proved the score no longer depended on whether the attempt number was even or odd, which was the root of the "haywire score" feeling. AI helped me design the tests by suggesting I assert on the same input across different attempt numbers, which is what exposed the parity bug clearly.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the whole `app.py` file from top to bottom every time you click a button or change an input, so it is not like a normal program that runs once and waits. Because of that, anything you want to remember between clicks (the secret number, the score, the attempt count) has to live in `st.session_state`, otherwise it would reset on every rerun. The "game never ends" bug made this click for me: the game state persisted across reruns, so forgetting to reset `status` and `score` in the New Game handler meant the old game-over state survived forever. The fix was to explicitly reset every piece of session state when starting a new game.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is marking the "crime scene" with a `# FIX:` comment and writing a failing test before I touch the logic, so I have proof the bug exists and proof it is gone. The thing I would do differently is to trust AI suggestions less on scoring and game-balance logic and read the diff line by line, since the AI was confident about a change that would have broken the game economy. Overall this project made me treat AI-generated code as a first draft from a fast but careless teammate: useful for speed, but every claim it makes has to be checked against a test or the running app before I believe it.
