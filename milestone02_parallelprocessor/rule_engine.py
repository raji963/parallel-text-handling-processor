import re
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# -------------------------------
# Ensure VADER lexicon is available once
# -------------------------------
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

# Initialize VADER
sia = SentimentIntensityAnalyzer()

# Weighted dictionaries for rule-based scoring
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

# -------------------------------
# Main sentiment analysis function
# -------------------------------
def analyze_sentiment(text):
    words = re.findall(r"\b\w+\b", text.lower())
    score = 0

    for i, word in enumerate(words):
        # Rule-based scoring
        if word in POSITIVE_RULES:
            word_score = POSITIVE_RULES[word]
            # Intensity modifiers
            if i > 0 and words[i-1] in ['very', 'really', 'extremely']:
                word_score *= 1.5
            score += word_score
        elif word in NEGATIVE_RULES:
            word_score = NEGATIVE_RULES[word]
            # Negation handling
            if i > 0 and words[i-1] in ['not', "don't", "didn't", "never"]:
                word_score *= -1
            score += word_score

    # TextBlob sentiment polarity
    blob_score = TextBlob(text).sentiment.polarity

    # VADER sentiment compound score
    vader_score = sia.polarity_scores(text)['compound']

    # Combine all scores
    total_score = score + blob_score + vader_score

    # Determine sentiment label
    if total_score > 0:
        sentiment = "Positive"
    elif total_score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return text, sentiment, total_score