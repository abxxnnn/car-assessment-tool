def score_to_rating(score_out_of_10: float) -> str:
    if score_out_of_10 >= 8.6:
        return "🌟 Excellent (Almost like new)"
    elif score_out_of_10 >= 7.3:
        return "✅ Very Good"
    elif score_out_of_10 >= 5.9:
        return "🟡 Good (Minor repairs needed)"
    elif score_out_of_10 >= 4.5:
        return "⚠️ Average (Significant repairs needed)"
    else:
        return "❌ Avoid unless very cheap"
