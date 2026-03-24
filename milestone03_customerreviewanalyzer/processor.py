import re
from multiprocessing import Pool, cpu_count

# =========================
# WORD LISTS
# =========================
POSITIVE_WORDS = {
    "good","great","excellent","amazing","love","nice","outstanding",
    "fantastic","wonderful","perfect","brilliant","awesome","best",
    "happy","satisfied","recommend","fast","friendly","helpful","super","superb","cool","impressive","reliable","efficient",
    "smooth","easy","clean","beautiful","attractive","affordable",
    "worth","value","quick","responsive","supportive","delightful",
    "enjoyed","liked","works","working","fine","ok","okay",
    "pleased","top","quality","premium","comfortable","convenient"
}

NEGATIVE_WORDS = {
    "bad","poor","terrible","hate","worst","disappointing","awful",
    "horrible","useless","broken","defective","unhappy","garbage",
    "junk","slow","fail","failed","issue","problem","difficult","cheap","waste","wasted","error","bugs","buggy","crash",
    "crashed","lag","laggy","delay","delayed","hard","confusing",
    "annoying","frustrating","weak","low","damage","damaged",
    "missing","incomplete","wrong","fake","faulty","poorly",
    "expensive","overpriced","notworking","unstable","freeze","freezing"
}

# =========================
# SPLIT TEXT INTO SENTENCES
# =========================
def split_text(text):
    text = re.sub(r'(?<![.!?])\s+(?=[A-Z])', '. ', text)
    sentences = re.split(r'[.!?]+|\n', text)
    return [s.strip() for s in sentences if s.strip()]

# =========================
# SPLIT INTO CHUNKS (NEW 🔥)
# =========================
def split_into_chunks(data, chunk_size=10000):
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

# =========================
# SINGLE TEXT ANALYSIS
# =========================
def analyze_single_text(text):
    words = re.findall(r'\b\w+\b', text.lower())
    pos = 0
    neg = 0
    i = 0

    while i < len(words):
        word = words[i]

        # NEGATION
        if word == "not" and i + 1 < len(words):
            next_word = words[i+1]
            if next_word in POSITIVE_WORDS:
                neg += 2
                i += 2
                continue
            elif next_word in NEGATIVE_WORDS:
                pos += 1
                i += 2
                continue

        # INTENSIFIERS
        if word == "very" and i + 1 < len(words):
            next_word = words[i+1]
            if next_word in POSITIVE_WORDS:
                pos += 2
                i += 2
                continue
            elif next_word in NEGATIVE_WORDS:
                neg += 2
                i += 2
                continue

        # NORMAL WORD (handles repeated words automatically)
        if word in POSITIVE_WORDS:
            pos += 1
        elif word in NEGATIVE_WORDS:
            neg += 1

        i += 1

    score = pos - neg
    sentiment = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"

    return (text, score, sentiment)

# =========================
# MAIN FUNCTION (UPDATED 🔥)
# =========================
def analyze_texts(texts):
    cores = cpu_count()

    # 🔹 Create chunks
    chunks = split_into_chunks(texts, chunk_size=10000)
    total_chunks = len(chunks)

    # 🔹 Parallel processing
    chunk_size = max(50, len(texts)//(cores*2))
    with Pool(cores) as pool:
        results = pool.map(analyze_single_text, texts, chunksize=chunk_size)

    return results, total_chunks, cores