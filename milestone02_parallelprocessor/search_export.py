# search_export.py

import csv
from database import fetch_all


def export_to_csv():
    rows = fetch_all()

    with open("customer_feedback_results.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(["ID", "Review", "Score", "Sentiment", "Tags", "Keywords"])

        for row in rows:
            writer.writerow(row)

    print("CSV file 'customer_feedback_results.csv' created successfully!")