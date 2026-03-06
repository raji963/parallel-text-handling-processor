import re

# Weighted dictionaries
POSITIVE_RULES = {
    "excellent": 3,
    "amazing": 2,
    "good": 1,
    "happy": 2,
    "love": 2,
    "great": 2
}

NEGATIVE_RULES = {
    "terrible": -3,
    "bad": -1,
    "worst": -2,
    "error": -2,
    "poor": -2,
    "hate": -3
}


def analyze_sentiment(text):
    words = re.findall(r"\b\w+\b", text.lower())
    score = 0

    for word in words:
        if word in POSITIVE_RULES:
            score += POSITIVE_RULES[word]
        elif word in NEGATIVE_RULES:
            score += NEGATIVE_RULES[word]

    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return text, sentiment, score