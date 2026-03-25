**Milestone 02**
Parallel Text Processing System
Advanced NLP Sentiment Analysis & Performance Benchmarking

**Project Objective**
This milestone enhances the text processing system developed in Milestone 01 by introducing parallel processing techniques and advanced sentiment analysis. The system analyzes customer feedback using a rule-based sentiment engine combined with NLP libraries, and compares the performance of single processing, threading, and multiprocessing.

**Project Description**
This project processes customer feedback text and performs the following tasks:
•	Rule-based sentiment analysis with weighted scoring
•	Enhanced NLP sentiment analysis using TextBlob polarity and NLTK VADER compound scores
•	Detection of issue-related keywords
•	Storage of results in a SQLite database
•	Performance comparison between different processing methods
•	Scalability evaluation for increasing dataset sizes

**Processing Methods**
1. Single Processing
All text data is processed sequentially using a single CPU core. This serves as the baseline for performance comparison.
2. Threading
Multiple threads process text chunks simultaneously to improve efficiency, leveraging Python's threading module for I/O-bound concurrency.
3. Multiprocessing
Multiple processes run in parallel using different CPU cores, improving performance for large datasets through true parallelism.

**Processing Workflow**
The system follows a structured pipeline:

Read Text → Split Text → Process Each Chunk → Rule-Based Sentiment Scoring
→ NLP Sentiment Scoring → Keyword Detection → Database Insert → Performance Benchmarking

Weighted Sentiment Rule Engine
The system calculates sentiment scores based on weighted rules, enhanced with NLP analysis.

Word Weights
Type	Word	Score
Positive	excellent	+3
Positive	amazing	+2
Positive	good / happy / love / great	+1 / +2 / +2 / +2
Negative	terrible / hate	-3
Negative	worst / error / poor	-2
Negative	bad	-1

**Score Calculation Example**
Review: "This product is amazing but has one minor error"
amazing = +2
error  = -2
Total Score = 0  →  Neutral

**Sentiment Classification**
Score Condition	Classification
Score > 0	Positive
Score < 0	Negative
Score = 0	Neutral

**Enhancements in Milestone 02**
•	NLP-based sentiment scoring using TextBlob and NLTK VADER
•	Handling negations: not, never, didn't
•	Handling intensity modifiers: very, extremely, really

**Performance Results**
Example output from the system benchmark:

Processing Method Comparison
Method	Time (sec)
Single Processing	0.0649
Threading	0.0000
Multiprocessing	5.9278

Scalability Test Results
Records	     Processing Time	        Insert Time	       Query Time
100	          0.0702 sec	             0.0088 sec	        0.0010 sec
10,000	      2.8658 sec	             0.0427 sec       	0.0000 sec
100,000	      25.9873 sec	             0.3667 sec	        0.0000 sec

**Scalability Testing**
The system was tested with three dataset sizes — 100, 10,000, and 100,000 records — measuring the following metrics for each:
•	Processing time
•	Database insertion time
•	Query execution time

This evaluation ensures the system can handle large-scale text data efficiently and provides a foundation for further optimization.

**Database Optimization**
The project uses SQLite with the following optimizations:
•	Bulk insertion of records for reduced I/O overhead
•	Indexed queries for fast retrieval
•	Structured storage for large datasets

These optimizations improve data handling speed and query performance at scale.

**Project Structure**
Milestone02_ParallelProcessor/
├─ main.py
├─ text_loader.py
├─ rule_engine.py
├─ parallel_processor.py
├─ database.py
├─ performance_test.py
├─ search_export.py
├─ README.md
├─ requirements.txt
└─ .gitignore

**Technologies Used**
Technology	Purpose
Python 3	Core programming language
SQLite3	Lightweight database storage
Threading module	Concurrent processing via threads
Multiprocessing module	True parallel processing via CPU cores
TextBlob	NLP sentiment polarity scoring
NLTK VADER	Rule-based NLP compound sentiment scores

**Key Features**
•	Rule-based sentiment analysis with configurable word weights
•	NLP-enhanced sentiment analysis using TextBlob + NLTK VADER
•	Handling of negations and intensity modifiers
•	Parallel processing: single, threading, multiprocessing
•	Performance benchmarking and scalability testing
•	SQLite database storage with bulk insert and indexing
•	Keyword detection for issue identification

**Conclusion**
Milestone 02 strengthens the text processing system by implementing parallel processing for faster performance and NLP-enhanced sentiment analysis for more accurate insights. The system supports keyword detection, scalability testing, and optimized database operations for efficient handling of large datasets. Its modular design provides a solid foundation for future improvements, including advanced NLP techniques or distributed processing.
