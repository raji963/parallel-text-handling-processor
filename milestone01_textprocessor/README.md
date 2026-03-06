# Milestone 01 – Text Processing System

## Project Objective

The objective of this project is to build a structured text processing system that analyzes customer feedback text files.

The system performs rule-based sentiment analysis and detects issue-related keywords. The processed results are stored in a SQLite database and summarized for analysis.

---

## Text Domain

This project processes **customer feedback text**.

The input consists of customer reviews or feedback statements that may contain:

- Positive opinions (e.g., good, excellent, happy)
- Negative opinions (e.g., bad, problem, hate)
- Issue-related keywords (e.g., error, fail, issue)

---

## Processing Flow (Architecture Flow)

The system follows a clear modular processing pipeline:

Read Text  
→ Break into Chunks  
→ Process Each Chunk  
→ Apply Rule-Based Scoring  
→ Detect Keyword Patterns  
→ Store Results in SQLite Database  
→ Display Summary Statistics  

---

## Step-by-Step Flow Explanation

### 1. Read Text
The system reads a text file containing customer feedback.

### 2. Break into Chunks
The text is divided into smaller word-based chunks for structured processing.

### 3. Process
Each chunk is processed individually.

### 4. Apply Scoring
Positive and negative word counts are calculated.

Sentiment Score = **(Positive Count − Negative Count)**

### 5. Pattern Detection
Keywords like **"error", "issue", and "fail"** are detected.

### 6. Store in Database
Each processed chunk along with score and detected keywords is stored in **SQLite**.

### 7. Display Summary
The system displays:

- Total number of processed chunks
- Average sentiment score

---

## Project Structure
Milestone01_TextProcessor/
│
├── main.py
├── text_loader.py
├── rule_engine.py
├── database.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── sample_texts/
└── feedback.txt

---

## Technologies Used

- Python 3
- SQLite3 (built-in database)
- Modular programming design

No heavy external libraries are used.

---

## Key Features

- Text file reading
- Word-based text chunking
- Rule-based sentiment scoring
- Keyword pattern detection
- SQLite database storage
- Clean modular architecture

---

## Technical Observations

- The repository contains only milestone-related files.
- No unnecessary experimental code is included.
- `.gitignore` prevents pushing cache files and database files.
- `requirements.txt` does not include unused heavy libraries.
- The system is structured for future extension (e.g., parallel processing in Milestone 02).

---

## Conclusion

Milestone 01 successfully implements a structured text processing pipeline for customer feedback analysis using rule-based sentiment scoring, keyword detection, and SQLite database storage. The modular design ensures clarity, maintainability, and readiness for future enhancements.