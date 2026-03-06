# Milestone 02 – Parallel Text Processing System

## Project Objective

The objective of this milestone is to enhance the text processing system developed in Milestone 01 by introducing **parallel processing techniques**.  
The system analyzes customer feedback using rule-based sentiment scoring and compares the performance of **single processing, threading, and multiprocessing**.

---

## Project Description

This project processes **customer feedback text** and performs the following tasks:

- Rule-based sentiment analysis using weighted scoring
- Detection of issue-related keywords
- Storage of results in a SQLite database
- Performance comparison between different processing methods

The system also evaluates how processing time changes when the dataset size increases.

---

## Processing Methods

### 1. Single Processing
All text data is processed sequentially using a single CPU core.

### 2. Threading
Multiple threads are used to process text chunks simultaneously.

### 3. Multiprocessing
Multiple processes run in parallel using different CPU cores to improve performance for larger datasets.

---

## Processing Workflow

The system follows a structured processing pipeline:

Read Text  
→ Split Text into Chunks  
→ Process Each Chunk  
→ Apply Rule-Based Sentiment Scoring  
→ Detect Keywords  
→ Store Results in SQLite Database  
→ Compare Processing Performance

---

## Weighted Sentiment Rule Engine

The system uses weighted rules to calculate sentiment scores.

Example rules:

Positive words:
```
excellent = +3
amazing = +2
good = +1
happy = +2
```

Negative words:
```
terrible = -3
bad = -1
worst = -2
error = -2
```

Example review:

```
"This product is amazing but has one minor error"
```

Score calculation:

```
amazing = +2
error = -2
Total score = 0
```

Sentiment classification:

```
Score > 0 → Positive  
Score < 0 → Negative  
Score = 0 → Neutral
```

---

## Performance Results

Example output from the system:

```
--- Performance Comparison ---

Single Processing: 0.0000 sec
Threading: 0.0000 sec
Multiprocessing: 0.2521 sec

Records: 100
Processing time: 0.0000 sec
Insert time: 0.0070 sec
Query time: 0.0000 sec

Records: 10000
Processing time: 0.0463 sec
Insert time: 0.0485 sec
Query time: 0.0028 sec

Records: 100000
Processing time: 0.4182 sec
Insert time: 0.2888 sec
Query time: 0.0000 sec
```

These results show how the system performs when the dataset size increases.

---

## Scalability Testing

The system was tested with different dataset sizes:

- 100 records
- 10,000 records
- 100,000 records

For each dataset, the following metrics were measured:

- Processing time
- Database insert time
- Query execution time

This helps evaluate the scalability of the system.

---

## Database Optimization

The project includes basic database optimizations such as:

- Bulk insertion of records
- Efficient database queries
- Structured data storage using SQLite

These optimizations improve performance when handling larger datasets.

---

## Project Structure

```
Milestone02_ParallelProcessor/

main.py
text_loader.py
rule_engine.py
parallel_processor.py
database.py
performance_test.py
search_export.py
README.md
requirements.txt
.gitignore
```

---

## Technologies Used

- Python 3
- SQLite3
- Threading module
- Multiprocessing module
- Modular Python programming

---

## Key Features

- Rule-based sentiment analysis
- Weighted scoring system
- Keyword detection
- Parallel processing implementation
- Performance benchmarking
- SQLite database storage

---

## Conclusion

Milestone 02 enhances the text processing system by introducing **parallel processing and performance analysis**.  
The project demonstrates how different processing methods affect execution time and scalability when working with large text datasets.

The modular design allows further improvements such as advanced natural language processing or distributed computing in future versions.