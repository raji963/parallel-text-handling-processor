import sqlite3

DB_NAME = "text_analysis.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review TEXT,
            sentiment TEXT,
            score INTEGER
        )
    """)

    conn.commit()
    conn.close()


def create_index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sentiment ON reviews(sentiment)")
    conn.commit()
    conn.close()


def insert_bulk(results):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.executemany(
        "INSERT INTO reviews (review, sentiment, score) VALUES (?, ?, ?)",
        results
    )

    conn.commit()
    conn.close()


def query_by_sentiment(sentiment):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reviews WHERE sentiment = ?", (sentiment,))
    rows = cursor.fetchall()

    conn.close()
    return rows