# view_data.py
import sqlite3

def retrieve_all_data():
    conn = sqlite3.connect('sentiment_data.db')
    cursor = conn.cursor()
    
    # Retrieve the first 10 records just to check
    cursor.execute("SELECT * FROM processed_reviews LIMIT 10")
    rows = cursor.fetchall()
    
    print("\n--- 🗄️ Checking Stored Database Data ---")
    for row in rows:
        print(f"ID: {row[0]} | Sentiment: {row[4]} | Words: {row[2]} Pos, {row[3]} Neg")
        
    conn.close()

if __name__ == "__main__":
    retrieve_all_data()