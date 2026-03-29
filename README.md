# 📊 Python Parallel Text Handling Processor
*Enterprise-Level Customer Review Analyzer & Sentiment Engine*

## 1. Project Overview
The **Python Parallel Text Handling Processor** is a high-performance web application built with Flask and JavaScript. It is designed to perform large-scale sentiment analysis on massive datasets (50,000+ records) using **Multi-core Parallel Processing** and **Persistent Database Storage**. The system accurately classifies unstructured text as Positive, Negative, or Neutral, providing actionable business intelligence through an interactive dashboard.

---

## 2. Milestone 4 Enhancements (Latest Updates)
To meet the requirements for "Text Storage Improver" and "Performance Validation," the following production-level features were implemented:

* **🗄️ Text Storage Improver (SQLite):** Replaced temporary memory storage with a persistent SQLite database. All processed results are indexed and saved to `sentiment_data.db`, ensuring data reliability and long-term storage.
* **📧 Automated Reporting System:** Integrated an SMTP Simulation-based notification module (for safe testing without external dependencies. After large-scale processing, the system generates a summary report including total records, sentiment distribution, and execution metrics.
* **⚡ Speed Optimization (Sets vs. Lists):** Optimized the NLP scoring engine by utilizing **Python Sets** for word lookups. This achieves **O(1) Time Complexity**, significantly outperforming standard list-based iterations for large lexicons.
* **🛡️ Reliability & Error Handling:** Implemented robust `try-except` blocks to ensure that even if a sub-module (like email) faces connection issues, the core analysis and database storage remain unaffected.

---

## 3. Core Functionality
* **Multi-Format Upload:** Supports `.csv`, `.txt`, and `.xlsx` files with automatic data cleaning.
* **Parallel Execution:** Uses `ThreadPoolExecutor` to divide heavy workloads across all available CPU cores, preventing server blocking.
* **Interactive Dashboard:** Features a live data table, sentiment counters, and a "Reset" function for fresh analysis.
* **Data Visualizations:** Implements **Chart.js** for:
    * Sentiment Distribution (Doughnut Chart)
    * Score Frequency (Bar Chart)
    * Top 10 Sentiment Words (Dynamic Word Frequency Chart)

---

## 4. How Sentiment Analysis Works
The application utilizes a custom Rule-Based NLP engine.
* **Negation Handling:** Dynamically flips context (e.g., "not good" → Negative).
* **Intensifiers:** Gauges emotional strength (e.g., "very good" → Strong Positive +2).
* **Business Lexicon:** Includes expanded vocabulary for financial and professional contexts (e.g., "profitable", "deficit", "growth").

---

## 5. Performance Benchmarks
*Performance metrics recorded on an 8-Core CPU processing 50,000 records:*

| Mode | Execution Time | Speedup / Observation |
| :--- | :--- | :--- |
| **Sequential (Normal)** | ~6.44s | High CPU bottleneck |
| **Parallel (Threaded)** | **~2.51s** | **2.5x Faster** (Optimal core utilization) |

---

## 6. System Architecture & Internal Flow
1.  **Ingestion:** Data is loaded via Pandas and cleaned of null values.
2.  **Chunking:** The dataset is divided into equal segments based on the system's CPU core count.
3.  **Analysis:** Parallel threads process chunks using the optimized **Set-based** lookup engine.
4.  **Persistence:** Results are saved to the **SQLite Storage Improver**.
5.  **Reporting:** The **Notification Module** triggers an automated summary report for the user.

---

## 7. Tech Stack
* **Backend:** Python 3.x, Flask
* **Database:** SQLite3 (High-speed indexing)
* **Parallelism:** `concurrent.futures.ThreadPoolExecutor`
* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript
* **Charts:** Chart.js
* **Data Processing:** Pandas, Regular Expressions (Regex)

---

## 8. Steps to Run the Project
1.  **Install Dependencies:**
    ```bash
    pip install flask pandas openpyxl
    ```
2.  **Run Application:**
    ```bash
    python app.py
    ```
3.  **Access Dashboard:**
    Open `http://127.0.0.1:5000/` in your browser.

---

## 9. Conclusion
The Python Parallel Text Handling Processor efficiently bridges the gap between raw data and business intelligence. By combining **Parallel Computing**, **Optimized Data Structures (Sets)**, and **Persistent Storage (SQL)**, it provides a scalable, fast, and reliable solution for enterprise-level sentiment analysis.
