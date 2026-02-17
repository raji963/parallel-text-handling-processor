# rule_engine.py

POSITIVE_WORDS = ["good", "great", "excellent", "love", "happy"]
NEGATIVE_WORDS = ["bad", "poor", "terrible", "hate", "problem"]
KEYWORDS = ["error", "fail", "issue"]


def score_text(chunk):
    """
    Simple positive/negative word count scoring
    """
    words = chunk.lower().split()

    positive_count = 0
    negative_count = 0

    for word in words:
        if word in POSITIVE_WORDS:
            positive_count += 1
        if word in NEGATIVE_WORDS:
            negative_count += 1

    return positive_count - negative_count


def detect_patterns(chunk):
    """
    Detect keyword patterns like error or issue
    """
    found_keywords = []
    words = chunk.lower().split()

    for keyword in KEYWORDS:
        if keyword in words:
            found_keywords.append(keyword)

    return found_keywords
