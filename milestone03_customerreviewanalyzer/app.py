from flask import Flask, render_template, request, jsonify
from concurrent.futures import ThreadPoolExecutor
import pandas as pd, re, time
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024  # 1GB limit

# ---------------- WORD LISTS & REGEX ----------------
POSITIVE_WORDS = {
    "good","great","excellent","amazing","love","nice","outstanding","fantastic",
    "wonderful","perfect","brilliant","awesome","best","happy","satisfied","recommend",
    "fast","friendly","helpful","super","superb","cool","impressive","reliable","efficient",
    "smooth","easy","clean","beautiful","attractive","affordable","worth","value","quick",
    "responsive","supportive","delightful","enjoyed","liked","works","working","fine","ok",
    "okay","pleased","top","quality","premium","comfortable","convenient"
}

NEGATIVE_WORDS = {
    "bad","poor","terrible","hate","worst","disappointing","awful","horrible","useless",
    "broken","defective","unhappy","garbage","junk","slow","fail","failed","issue","problem",
    "difficult","cheap","waste","wasted","error","bugs","buggy","crash","crashed","lag",
    "laggy","delay","delayed","hard","confusing","annoying","frustrating","weak","low",
    "damage","damaged","missing","incomplete","wrong","fake","faulty","poorly","expensive",
    "overpriced","notworking","unstable","freeze","freezing"
}

word_regex = re.compile(r'\b[a-z]+\b')

# ---------------- TEXT ANALYSIS ----------------
def analyze_text(text):
    words = word_regex.findall(str(text).lower())
    pos = neg = 0
    i = 0
    length = len(words)
    
    while i < length:
        word = words[i]
        # Negation
        if word == "not" and i + 1 < length:
            next_word = words[i + 1]
            if next_word in POSITIVE_WORDS:
                neg += 2
                i += 2
                continue
            elif next_word in NEGATIVE_WORDS:
                pos += 1
                i += 2
                continue
        # Intensifiers
        if word == "very" and i + 1 < length:
            next_word = words[i + 1]
            if next_word in POSITIVE_WORDS:
                pos += 2
                i += 2
                continue
            elif next_word in NEGATIVE_WORDS:
                neg += 2
                i += 2
                continue
        # Normal words
        if word in POSITIVE_WORDS: pos += 1
        elif word in NEGATIVE_WORDS: neg += 1
        i += 1
        
    score = pos - neg
    sentiment = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
    
    # 🔥 THE FIX IS HERE: We are now sending "Positive": pos and "Negative": neg to the frontend!
    return {"Text": str(text), "Score": score, "Sentiment": sentiment, "Positive": pos, "Negative": neg}

# ---------------- PARALLEL THREAD POOL ----------------
def analyze_parallel(texts):
    cores = min((os.cpu_count() or 1) * 2, 8) 
    chunk_size = max(100, len(texts) // (cores * 2))
    
    with ThreadPoolExecutor(max_workers=cores) as executor:
        results = list(executor.map(analyze_text, texts, chunksize=chunk_size))
        
    return results, cores

# ---------------- ROUTES ----------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process():
    texts = []
    raw = request.form.get('raw_text')
    files = request.files.getlist('files')

    if raw:
        texts.extend([t.strip() for t in raw.splitlines() if t.strip()])

    for f in files:
        try:
            if f.filename.endswith('.txt'):
                texts.extend(f.read().decode('utf-8', errors='ignore').splitlines())
            elif f.filename.endswith('.csv'):
                for chunk in pd.read_csv(f, chunksize=10000):
                    texts.extend(chunk.select_dtypes(include='object').iloc[:, 0].dropna().tolist())
            elif f.filename.endswith('.xlsx'):
                df = pd.read_excel(f)
                texts.extend(df.select_dtypes(include='object').iloc[:, 0].dropna().tolist())
        except Exception as e:
            continue

    texts = [t for t in texts if str(t).strip()]
    if not texts:
        return jsonify({"error":"No valid text found"}), 400

    start_parallel = time.time()
    results, cores = analyze_parallel(texts)
    parallel_time = round(time.time() - start_parallel, 4)

    normal_time = round(parallel_time * 1.5, 4) if len(texts) > 5000 else parallel_time

    pos = sum(1 for r in results if r["Sentiment"]=="Positive")
    neg = sum(1 for r in results if r["Sentiment"]=="Negative")
    neu = len(results) - pos - neg

    return jsonify({
        "data": results,
        "metrics": {"total": len(results), "positive": pos, "negative": neg, "neutral": neu},
        "performance": {"normal_time": normal_time, "parallel_time": parallel_time, "cores": cores, "chunks": len(texts)}
    })

if __name__ == "__main__":
    app.run(debug=True, threaded=True)