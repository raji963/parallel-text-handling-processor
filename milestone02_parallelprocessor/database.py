import sqlite3

# Connect to the database
conn = sqlite3.connect("reviews.db")
cursor = conn.cursor()

# Create table function
def create_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        sentiment TEXT,
        score REAL
    )
    """)
    conn.commit()

# Create index function
def create_index():
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sentiment ON reviews(sentiment)")
    conn.commit()

# Insert bulk reviews
def insert_bulk(results):
    for text, sentiment, score in results:
        cursor.execute(
            "INSERT INTO reviews (text, sentiment, score) VALUES (?, ?, ?)",
            (text, sentiment, score)
        )
    conn.commit()

# Query by sentiment
def query_by_sentiment(sentiment_label):
    cursor.execute("SELECT * FROM reviews WHERE sentiment=?", (sentiment_label,))
    return cursor.fetchall()