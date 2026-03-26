
# Customer Review Analyzer (Milestone 03)

## 1. Project Overview
The Customer Review Analyzer is a complete, end-to-end web application built with Python (Flask) and JavaScript. It is designed to perform large-scale sentiment analysis on massive datasets (50,000+ records) using parallel processing. The system accurately classifies unstructured text as Positive, Negative, or Neutral, providing business intelligence through an interactive and visual dashboard.

---

## 2. Features Implemented

**Core Functionality:**
* **File Upload:** Supports multi-file uploads across `.csv`, `.txt`, and `.xlsx` formats.
* **Manual Text Input:** Allows direct text evaluation via the user interface.
* **Parallel Processing:** Handles massive datasets (50,000+ records) efficiently without causing server timeouts.
* **Interactive Dashboard:** Displays Total Records, alongside Positive, Negative, and Neutral metrics.
* **Data Visualizations:** Implements Chart.js for Sentiment Distribution (Doughnut Chart), Score Frequency (Bar Chart), and Top 10 Words (Filtered NLP Chart).

**Data Management:**
* **Search Functionality:** Live keyword search that filters the data table instantly without throwing "No match found" errors for valid inputs.
* **Export Results:** Users can download the fully processed dataset, or download a filtered CSV based exclusively on their active search queries.
* **UI Enhancements:** Includes a Reset/Clear Data function, file upload counters, and live execution time/CPU core metrics.

---

## 3. Dataset Details
* **Type of Data:** Unstructured customer feedback, product reviews, and business news.
* **Format:** Tested using real-world `.csv` and `.xlsx` files containing variable row lengths.
* **Volume:** Optimized and stress-tested specifically for enterprise-level datasets ranging from 50,000 to 1,000,000 rows.

---

## 4. How Sentiment Analysis is Implemented

The application utilizes a custom Natural Language Processing (NLP) scoring engine. The exact Positive and Negative word counts are visibly displayed on the frontend table for every evaluated review. The vocabulary has been expanded to handle business, financial, and news contexts (e.g., "profitable", "deficit", "growth", "crash").

**Rule-Based Approach & Special Cases:**
* **Direct Matches:** Positive words increase the score (+1), and negative words decrease the score (-1).
* **Repeated Words:** The system accurately parses and counts multiple instances of the same sentiment word. (Example: *"good good bad"* → Positive = 2, Negative = 1. Total Score = +1).
* **Negation Handling:** Dynamically flips sentiment context. (Example: *"not good"* → Evaluated as Negative).
* **Intensifiers:** Acts as a score multiplier to gauge emotional intensity. (Example: *"very good"* → Evaluated as Strong Positive +2).

---

## 5. Explanation of Parallel Processing & Internal Flow
To process 50,000+ records without crashing the application, the system uses a **Chunking and Aggregation** architecture via `concurrent.futures.ThreadPoolExecutor`.

* **How Chunks are Created:** The backend mathematically divides the dataset. For example, 50,000 records processed on an 8-core CPU are sliced into 8 equal arrays (chunks) of 6,250 records each.
* **Thread Dispatch:** Each CPU core takes one chunk and independently runs the sentiment analysis loop in an isolated thread, preventing Flask server blocking.
* **How Merging Happens:** Once threads finish, they return lists of dictionary objects. The main thread aggregates these sub-lists back into a single, sequential array using list extension, ensuring the original data order is preserved before sending the JSON response to the frontend.

---

## 6. Performance Comparison (Sequential vs Parallel)

*Performance metrics based on an 8-Core CPU setup processing real data:*

| Dataset Size | Sequential (Normal) | Parallel (Threaded) | Speedup / Observation |
| ------------ | ------------------- | ------------------- | --------------------- |
| 100 Records  | ~0.05s              | ~0.15s              | Slower (Due to thread-creation overhead) |
| 50,000 Records| ~6.44s             | **~4.29s** | **1.5x Faster** (Optimal CPU utilization) |

**Detailed Performance Reasoning:**
* **Why it is slower for small data:** Spawning threads, allocating memory, and context-switching creates "overhead." For 100 rows, the CPU spends more time setting up the threads than it does calculating the sentiment.
* **Why it is faster for large data:** For massive datasets, the actual mathematical calculation time heavily outweighs the thread-setup overhead. By dividing the workload, the system bypasses the single-thread bottleneck, resulting in a massive speedup.

---

## 7. System Limitations & Future Scope
While the expanded rule-based lexicon handles negations, intensifiers, and business contexts effectively, rule-based systems have inherent limitations in complex, real-world environments:
* **Sarcasm Detection:** A phrase like *"Oh great, another broken feature"* contains the positive word "great" but is contextually negative. Rule-based engines struggle with implied sarcasm.
* **Context-Based Meaning:** The word "unpredictable" is positive in a movie review (*"an unpredictable thriller"*) but negative in a software review (*"unpredictable server crashes"*). 
* **Future Enhancements:** To make the system completely robust for complex sentences and sarcasm, the next iteration would involve replacing the manual lexicon with a pre-trained contextual Machine Learning model (such as VADER or a BERT Transformer) which understands deep sentence structures rather than just exact keyword matching.

---

## 8. Edge Cases Handled
* **Empty Input:** The UI prevents submission of empty text/files and alerts the user gracefully.
* **Invalid File Types / Corrupted Data:** The backend safely skips blank rows, null values, or unreadable characters without causing application crashes.
* **Browser Freezing (Memory Management):** The frontend strictly limits DOM table rendering to the top 500 rows. This prevents the browser from crashing when evaluating 50,000+ rows, while still allowing the user to export the entirety of the processed data to a CSV file.

---

## 9. Tech Stack
* **Backend:** Python, Flask, `concurrent.futures`
* **Frontend:** HTML, Tailwind CSS, Vanilla JavaScript
* **Data Visualization:** Chart.js
* **Data Processing:** Pandas, Regular Expressions (Regex)

---

## 10. Steps to Run the Project

**1. Install Dependencies**

Bash
pip install -r requirements.txt

**2. Run the Application**

Bash
python app.py

**3. Access the Dashboard**
Open your web browser and navigate to:
http://127.0.0.1:5000/


## 11.conclusion
The Customer Review Analyzer efficiently processes large sets of customer reviews, classifying them as positive, negative, or neutral. It handles big datasets using parallel processing, shows results clearly on an interactive dashboard, and allows searching and exporting both full and filtered data. The system safely manages repeated words, negations, and intensifiers to provide accurate sentiment intelligence. Overall, it is a fast, reliable, and user-friendly tool for enterprise data analysis.