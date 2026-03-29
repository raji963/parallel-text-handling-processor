import sqlite3

def init_db():
    # Connects to (or creates) the database file
    conn = sqlite3.connect('sentiment_data.db')
    cursor = conn.cursor()
    
    # 1. Create the table to store the processed text
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_text TEXT,
            positive_words INTEGER,
            negative_words INTEGER,
            final_sentiment TEXT
        )
    ''')
    
    # 2. Create an Index for lightning-fast retrieval of large datasets
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_sentiment 
        ON processed_reviews (final_sentiment)
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database successfully initialized with high-speed indexing.")

def save_results_to_db(results_list):
    # This function saves all your processed chunk data at once
    conn = sqlite3.connect('sentiment_data.db')
    cursor = conn.cursor()
    
    # Format the data for bulk insertion
    data_to_insert = [(item['text'], item['positive_count'], item['negative_count'], item['sentiment']) for item in results_list]
    
    # executemany inserts all records simultaneously (crucial for 50,000+ rows)
    cursor.executemany('''
        INSERT INTO processed_reviews (original_text, positive_words, negative_words, final_sentiment)
        VALUES (?, ?, ?, ?)
    ''', data_to_insert)
        
    conn.commit()
    conn.close()
    print(f"✅ Successfully saved {len(results_list)} records to the database.")

# Quick test to create the file if run directly
if __name__ == "__main__":
    init_db()