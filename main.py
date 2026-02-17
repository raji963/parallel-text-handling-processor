# main.py

from text_loader import read_text, chunk_text
from rule_engine import score_text, detect_patterns
from database import create_table, insert_result, get_summary


def process_text(file_path):
    print("Reading text...")
    text = read_text(file_path)

    print("Chunking text...")
    chunks = chunk_text(text, chunk_size=40)

    create_table()

    for chunk in chunks:
        score = score_text(chunk)
        keywords = detect_patterns(chunk)
        insert_result(chunk, score, keywords)

    total_chunks, average_score = get_summary()

    print("\nProcessing Complete")
    print("Total Chunks:", total_chunks)
    print("Average Score:", average_score)


if __name__ == "__main__":
    process_text("sample_texts/feedback.txt")
