from types import SimpleNamespace
from logic_utils import check_guess, update_score, reset_game_state

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High" and hint
    # must tell the player to go LOWER (not HIGHER — the original bug swapped these).
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected hint to say LOWER, got: {message}"

def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low" and hint
    # must tell the player to go HIGHER (not LOWER — the original bug swapped these).
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected hint to say HIGHER, got: {message}"

def test_score_win_first_attempt():
    # Winning on attempt 1: points = 100 - 10*(1-1) = 100.
    result = update_score(0, "Win", 1)
    assert result == 100

def test_score_win_second_attempt():
    # Winning on attempt 2: points = 100 - 10*(2-1) = 90.
    result = update_score(0, "Win", 2)
    assert result == 90

def test_score_win_accumulates():
    # Score accumulates on top of an existing score.
    result = update_score(50, "Win", 1)
    assert result == 150

def test_score_win_late_attempt_floors_at_10():
    # After 10+ attempts the minimum points awarded is 10, not negative.
    result = update_score(0, "Win", 10)
    assert result == 10

def test_new_game_resets_attempts():
    # After a new game, attempts must be 0 regardless of prior play.
    state = SimpleNamespace(attempts=5, secret=42, status="won", history=[1, 2, 3])
    reset_game_state(state)
    assert state.attempts == 0

def test_new_game_resets_status_to_playing():
    # The original bug left status as "won", blocking the player from guessing.
    # After reset, status must be "playing".
    state = SimpleNamespace(attempts=5, secret=42, status="won", history=[1, 2, 3])
    reset_game_state(state)
    assert state.status == "playing"

def test_new_game_clears_history():
    # History from the previous game must not carry over.
    state = SimpleNamespace(attempts=5, secret=42, status="won", history=[10, 20, 30])
    reset_game_state(state)
    assert state.history == []

def test_new_game_secret_in_range():
    # The new secret must fall within the requested low/high range.
    state = SimpleNamespace(attempts=0, secret=0, status="playing", history=[])
    reset_game_state(state, low=1, high=100)
    assert 1 <= state.secret <= 100
