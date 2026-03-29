import sqlite3
import csv

def export_to_csv():
    # 1. Connect to the database
    conn = sqlite3.connect('sentiment_data.db')
    cursor = conn.cursor()
    
    # 2. Get all records
    cursor.execute("SELECT * FROM processed_reviews")
    rows = cursor.fetchall()
    
    # 3. Create a new CSV file and write the data
    with open('database_backup.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write the header row first
        writer.writerow(['ID', 'Original Text', 'Positive Words', 'Negative Words', 'Sentiment'])
        # Write all the data rows
        writer.writerows(rows)
        
    conn.close()
    print(f"✅ Successfully exported {len(rows)} records to 'database_backup.csv'!")

if __name__ == "__main__":
    export_to_csv()