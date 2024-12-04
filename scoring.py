def get_score(score):
    level = 0
    """Return a category based on the quiz score."""
    if score < 6:
        level = 2
    elif score < 12:
        level = 3
    else:
        level= 4
    return level
