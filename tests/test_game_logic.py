from logic_utils import check_guess

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
