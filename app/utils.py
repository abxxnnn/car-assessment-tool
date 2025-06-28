def score_to_rating(score: float) -> str:
    if score >= 950:
        return "Excellent"
    elif score >= 800:
        return "Very Good"
    elif score >= 650:
        return "Good"
    elif score >= 500:
        return "Average"
    else:
        return "Avoid"