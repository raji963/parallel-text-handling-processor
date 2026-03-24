import pandas as pd
import random
import time
from multiprocessing import Pool, cpu_count

# ------------------- SENTIMENT SCORING -------------------
def score_text(text):
    words = text.lower().split()
    score = 0
    pos_count = 0
    neg_count = 0
    i = 0
    while i < len(words):
        word = words[i]
        multiplier = 1
        # Intensifiers
        if word in ["very", "extremely"]:
            multiplier = 2
            i += 1
            if i < len(words):
                word = words[i]
        # Negation
        if i > 0 and words[i-1] == "not":
            multiplier = -1
        if word == "good":
            score += 1 * multiplier
            if multiplier > 0:
                pos_count += multiplier
            else:
                neg_count += -multiplier
        elif word == "bad":
            score -= 1 * multiplier
            if multiplier > 0:
                neg_count += multiplier
            else:
                pos_count += -multiplier
        i += 1
    sentiment = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
    return score, pos_count, neg_count, sentiment

# ------------------- EDGE CASE TESTS -------------------
def test_edge_cases():
    print("\n--- EDGE CASE TESTS ---")
    
    # Empty input
    text = ""
    score, pos, neg, sentiment = score_text(text)
    print("Empty input test:", "Pass" if sentiment == "Neutral" else "Fail")
    
    # Repeated words
    text = "good good bad"
    score, pos, neg, sentiment = score_text(text)
    print("Repeated words test:", "Pass" if pos == 2 and neg == 1 else "Fail")
    
    # Negation
    text = "not good"
    score, pos, neg, sentiment = score_text(text)
    print("Negation test:", "Pass" if neg == 1 else "Fail")
    
    # Intensifier
    text = "very good"
    score, pos, neg, sentiment = score_text(text)
    print("Intensifier test:", "Pass" if pos == 2 else "Fail")

# ------------------- LARGE DATASET GENERATOR -------------------
def generate_dataset(n):
    texts = ["good product", "bad quality", "very good service", "not good", "excellent experience"]
    data = [{"Text": random.choice(texts)} for _ in range(n)]
    df = pd.DataFrame(data)
    return df

# ------------------- PROCESSING FUNCTIONS -------------------
def process_row(row):
    score, pos, neg, sentiment = score_text(row["Text"])
    row["Score"] = score
    row["Positive"] = pos
    row["Negative"] = neg
    row["Sentiment"] = sentiment
    return row

def process_sequential(df):
    data = df.to_dict(orient="records")
    return [process_row(row) for row in data]
    
def process_parallel(df):
    data = df.to_dict(orient="records")   # convert once

    with Pool(cpu_count()) as pool:
        results = pool.map(process_row, data, chunksize=2000)

    return results



# ------------------- LARGE DATASET TEST -------------------
def test_large_datasets():
    sizes = [50000, 100000, 1000000]
    for n in sizes:
        print(f"\n--- Testing dataset: {n} rows ---")
        df = generate_dataset(n)
        
        start = time.time()
        seq_result = process_sequential(df)
        seq_time = time.time() - start
        print(f"Sequential time: {seq_time:.3f}s")
        
        start = time.time()
        par_result = process_parallel(df)
        par_time = time.time() - start
        print(f"Parallel time  : {par_time:.3f}s")
        speedup = seq_time / par_time if par_time > 0 else 0
        print(f"Speedup (seq/par): {speedup:.2f}x")

# ------------------- INVALID FILE TYPE TEST -------------------
def test_invalid_file():
    print("\n--- INVALID FILE TEST ---")
    invalid_files = ["image.png", "document.pdf", "video.mp4"]
    ALLOWED_EXTENSIONS = {'csv', 'txt', 'xlsx'}
    for f in invalid_files:
        valid = f.split(".")[-1].lower() in ALLOWED_EXTENSIONS
        print(f"{f}: {'Pass (rejected)' if not valid else 'Fail'}")

# ------------------- RUN ALL TESTS -------------------
if __name__ == "__main__":
    test_edge_cases()
    test_invalid_file()
    test_large_datasets()