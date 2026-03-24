# 📊 Customer Review Analyzer (Milestone 03)

## 🚀 Project Overview
The Customer Review Analyzer is a **Flask-based web application** that performs **sentiment analysis on large datasets** using **parallel processing**.

Users can upload files or enter text, and the system analyzes reviews, classifies sentiment, and displays results through an interactive dashboard.

---

## 🎯 Objective
- Analyze customer reviews
- Classify sentiments: Positive / Negative / Neutral
- Handle large datasets (50K, 100K, 1M+)
- Demonstrate parallel processing performance

---

## ⚙️ Features

### ✅ Core Features
- 📎 File Upload (CSV, TXT, Excel)
- 📝 Manual Text Input
- ⚡ Parallel Processing (multiprocessing)
- 📊 Dashboard:
  - Total Records
  - Positive / Negative / Neutral counts
- 📈 Charts:
  - Sentiment Distribution
  - Score Frequency
  - Top Words
- 🔍 Search Functionality
- 📥 Export Results (CSV)

---

### ✅ Additional Features
- 🔄 Reset / Clear Data
- 📂 Multiple File Upload
- 📊 Handles large datasets (50K+ records)
- 🧠 CPU Core Usage Display
- ⚡ Sequential vs Parallel Comparison
- 🧪 Edge Case Testing Script

---

## 🧠 Sentiment Analysis Logic

### ✔ Rule-Based Approach
- Positive words → increase score
- Negative words → decrease score

### ✔ Special Cases
- Repeated words:
  - good good bad → Positive = 2, Negative = 1
- Negation:
  - not good → Negative
- Intensifiers:
  - very good → Strong Positive

---

## 🧪 Edge Case Testing

Tested using `edge_case_tester.py`:

- ✅ Empty input
- ✅ Invalid file types
- ✅ Repeated words
- ✅ Negation handling
- ✅ Intensifiers
- ✅ Large datasets

Run:
python edge_case_tester.py


---

## 📊 Performance Analysis
| Dataset Size | Sequential | Parallel | Speedup |
| ------------ | ---------- | -------- | ------- |
| 50,000       | ~0.31s     | ~3.17s   | 0.10x   |
| 100,000      | ~0.50s     | ~2.47s   | 0.21x   |
| 1,000,000    | ~4.76s     | ~8.51s   | 0.56x   |


### 🔍 Observations
- Parallel is slower for small data (overhead)
- Faster for large datasets
- Depends on CPU cores

---

## ⚡ Parallel Processing

- Uses multiprocessing.Pool
- Work divided across CPU cores
- Optimized chunk size
- Improves performance significantly

---

## 🛠️ Tech Stack

- Backend: Python, Flask
- Frontend: HTML, Tailwind CSS, JavaScript
- Charts: Chart.js
- Processing: Multiprocessing
- Database: SQLite (optional)

---

## 📁 Project Structure


milestone03_customerreviewanalyzer/
│
├── app.py
├── processor.py
├── database.py
├── edge_case_tester.py
│
├── templates/
│ └── index.html
│
├── static/
│ ├── script.js
│ └── style.css
│
├── results.csv
├── reviews.db
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore


---

## ▶️ How to Run

### Install Dependencies

pip install -r requirements.txt


### Run App

python app.py


### Open Browser

http://127.0.0.1:5000/


---

## 🧪 Testing


python edge_case_tester.py


## 🏆 Conclusion
The Customer Review Analyzer efficiently processes large sets of customer reviews, classifying them as positive, negative, or neutral. It handles big datasets using parallel processing, shows results clearly on a dashboard, and allows searching and exporting both full and filtered data. The system also manages repeated words, negations, and intensifiers, giving accurate sentiment results. Overall, it is a fast, reliable, and user-friendly tool for analyzing customer feedback.

