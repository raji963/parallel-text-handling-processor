import sqlite3

def create_connection():
    """Establish connection to the SQLite database."""
    return sqlite3.connect("reviews.db")

def create_table():
    """Create the table and optimize it with Indexes."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            score INTEGER,
            sentiment TEXT
        )
    """)

    # --- ADVANCED FEATURE: Database Optimization (Indexing) ---
    # This speeds up the search functionality significantly when dealing with thousands of rows
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sentiment ON reviews(sentiment)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_score ON reviews(score)")

    conn.commit()
    conn.close()

def insert_data(data):
    """Insert a large batch of processed reviews at once."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.executemany(
        "INSERT INTO reviews (text, score, sentiment) VALUES (?, ?, ?)",
        data
    )

    conn.commit()
    conn.close()

def fetch_all():
    """Fetch all historical processed reviews."""
    conn = create_connection()
    cursor = conn.cursor()
    
    # Fetch the newest reviews first
    cursor.execute("SELECT text, score, sentiment FROM reviews ORDER BY id DESC")
    rows = cursor.fetchall()
    
    conn.close()
    return rows