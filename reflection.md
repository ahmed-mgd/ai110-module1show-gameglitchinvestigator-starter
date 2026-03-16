# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

  1) The hint suggested to go higher when the number was lower, and vice versa.
  2) Winning after resetting the game with previous attempts yields inconsistent scores.
  3) Can't start a "New Game" after a previous win
  4) The range to guess between (e.g. 1 to 100) in the settings menu does not match the "Guess a number..." alert. The alert always says to guess between 1 and 100
  5) The hard setting gives a smaller (easier) range than the normal setting, which may or may not be a bug.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude Code to analyze the code and suggest solutions and Github Copilot for making smaller iterations and suggestions.

One correct suggestion provided by Claude Code was regarding the "New Game" reset bug. It pointed out that the status does not change back to playing and the history isn't reset. I verified this by playing back through the game and noting that the "You already won" alert disappears and the history is correctly reset.

```
● Found the bug. When "New Game" is clicked, the code resets attempts and secret but never resets
  st.session_state.status back to "playing". So the status stays "won", and the check at line 140 immediately shows
  the "You already won" message and calls st.stop().

● Update(app.py)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 Edit file
 app.py
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
 134  if new_game:
 135      st.session_state.attempts = 0
 136      st.session_state.secret = random.randint(1, 100)
 137 +    st.session_state.status = "playing"
 138 +    st.session_state.history = []
 139      st.success("New game started.")
 140      st.rerun()
 141
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
```

One incomplete suggestion provided by the AI dealt with the score not being correctly updated throughout gameplay. It initally suggested that the reason was due to the incorrect rewarding of points on even guesses, but upon iteration it spotted the actual cause:

```
What was already fixed:

Bug 3: update_score was rewarding +5 points on even-numbered wrong guesses. That's been corrected.
What's still broken (not addressed yet):

Score is never reset on New Game. The if new_game: block resets attempts, secret, status, and history — but not score. So it carries over across games.

Score has no visible display during gameplay. It only appears in the collapsed debug expander and in the final win/loss message. Players have no feedback that the score is changing mid-game.
```
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed by writing a pytest case that targeted the specific broken behavior, running the full test suite to confirm it passed, and then playing through the game a couple of times with different values to make sure it works. For example, `test_guess_too_high` checks that guessing 60 when the secret is 50 returns the outcome `"Too High"` and a hint containing `"LOWER"`. Similarly, `test_new_game_resets_status_to_playing` confirmed the New Game bug was gone by asserting that calling `reset_game_state` on a "won" state always sets status back to `"playing"`. The AI helped streamline designing these tests significantly. I could give it simple direction about what behavior I wanted covered and it handled the more technical details like setting up the `SimpleNamespace` mock state object and writing the assertions correctly.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

Streamlit reruns the entire Python script from top to bottom every time the user interacts with anything. Without session state, any variable assigned at the top of the script would be reassigned fresh on every rerun, which is why the secret number kept changing: `random.randint(low, high)` ran again each time. The fix was wrapping the secret generation in `if "secret" not in st.session_state:`, so a new random number is only picked once at the start of a game and then saved across reruns.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to carry forward is writing a test immediately after identifying a bug so I have a clear way to confirm when the fix actually works. Next time I work with AI on a coding task, I would be more incremental: apply one small change at a time, run the tests, and verify before moving to the next issue, rather than letting changes pile up in a disorganized way. This project made me realize that AI-generated code always needs a human to guide and validate it.