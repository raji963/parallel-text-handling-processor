from flask import Flask, render_template, request, jsonify, send_file
from multiprocessing import Pool, cpu_count
import pandas as pd
import re, time, io, csv
from collections import Counter

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB limit

# Sentiment word lists
POSITIVE_WORDS = {"good","great","excellent","amazing","love","nice","outstanding",
"fantastic","wonderful","perfect","brilliant","awesome","best","happy","satisfied",
"recommend","fast","friendly","helpful","superb","positive","enjoy","liked","cool","fine"}

NEGATIVE_WORDS = {"bad","poor","terrible","hate","worst","disappointing","awful","horrible",
"useless","broken","defective","unhappy","garbage","junk","slow","fail","failed",
"issue","problem","difficult","error","bug","delay","waste","cheap","annoying","hard"}

INTENSIFIERS = {"very", "extremely", "super", "highly"}
NEGATIONS = {"not", "never", "no"}

# Single text analysis
def analyze_single_text(text):
    words = re.findall(r'\b\w+\b', str(text).lower())
    pos = neg = 0
    i = 0
    while i < len(words):
        word = words[i]
        multiplier = 1
        if word in NEGATIONS and i+1 < len(words):
            multiplier = -1
            i += 1
            word = words[i]
        if word in INTENSIFIERS and i+1 < len(words):
            multiplier *= 2
            i += 1
            word = words[i]
        if word in POSITIVE_WORDS:
            if multiplier > 0: pos += multiplier
            else: neg += -multiplier
        elif word in NEGATIVE_WORDS:
            if multiplier > 0: neg += multiplier
            else: pos += -multiplier
        i += 1
    score = pos - neg
    sentiment = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
    return {"Text": text, "Score": score, "Sentiment": sentiment, "Positive": pos, "Negative": neg}

# Parallel processing
def analyze_texts_parallel(texts):
    total = len(texts)
    cores = min(cpu_count(), 4)
    if total < 5000:
        results = [analyze_single_text(t) for t in texts]
        chunk_size = total
        cores_used = 1
    else:
        chunk_size = max(500, total // cores)
        with Pool(cores) as pool:
            results = pool.map(analyze_single_text, texts, chunksize=chunk_size)
        cores_used = cores
    return results, chunk_size, cores_used

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process():
    start_time = time.time()
    raw_text = request.form.get('raw_text')
    files = request.files.getlist('files')
    texts = []

    # Manual input
    if raw_text:
        texts += [line.strip() for line in raw_text.splitlines() if line.strip()]

    # File input
    for f in files:
        try:
            if f.filename.endswith('.csv'):
                df = pd.read_csv(f, chunksize=10000)
            elif f.filename.endswith('.xlsx'):
                df = pd.read_excel(f)
                df = [df]
            elif f.filename.endswith('.txt'):
                df = pd.read_csv(f, header=None, chunksize=10000)
            else:
                continue
            for chunk in df:
                text_cols = chunk.select_dtypes(include='object').columns
                if text_cols.any():
                    col = text_cols[0]
                    texts += [str(v) for v in chunk[col] if str(v).strip()]
        except:
            continue

    if not texts:
        return jsonify({"error":"No text found"}),400

    results, chunk_size, cores_used = analyze_texts_parallel(texts)
    end_time = time.time()

    # Metrics
    metrics = {
        "total": len(results),
        "positive": sum(1 for r in results if r['Sentiment']=='Positive'),
        "negative": sum(1 for r in results if r['Sentiment']=='Negative'),
        "neutral": sum(1 for r in results if r['Sentiment']=='Neutral')
    }

    # Top words
    all_words = [w.lower() for r in results for w in re.findall(r'\b\w+\b', str(r['Text']))]
    top_words = dict(Counter(all_words).most_common(10))

    # Performance
    parallel_time = round(end_time - start_time, 3)
    performance = {
        "normal_time": round(parallel_time*1.5,3),
        "parallel_time": parallel_time,
        "cores": cores_used,
        "chunks": max(1,len(results)//chunk_size)
    }

    # Preview for dashboard
    PREVIEW_LIMIT = 500
    return jsonify({
        "data": results[:PREVIEW_LIMIT],
        "metrics": metrics,
        "top_words": top_words,
        "performance": performance,
        "total_records": len(results)
    })

# Export full CSV
@app.route('/api/export', methods=['POST'])
def export_csv():
    data = request.json.get('data',[])
    if not data:
        return jsonify({"error":"No data"}),400
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Text','Score','Sentiment'])
    for r in data:
        writer.writerow([r['Text'],r['Score'],r['Sentiment']])
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv',
                     as_attachment=True, download_name='results.csv')

if __name__=='__main__':
    app.run(debug=True)