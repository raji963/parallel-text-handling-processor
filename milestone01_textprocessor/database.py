# database.py

import sqlite3

DB_NAME = "text_analysis.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chunk TEXT,
            score INTEGER,
            keywords TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_result(chunk, score, keywords):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO results (chunk, score, keywords)
        VALUES (?, ?, ?)
    """, (chunk, score, ",".join(keywords)))

    conn.commit()
    conn.close()


def get_summary():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*), AVG(score) FROM results")
    count, avg_score = cursor.fetchone()

    conn.close()

    return count, avg_score