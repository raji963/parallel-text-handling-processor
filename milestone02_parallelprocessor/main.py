import os
from text_loader import load_reviews
from database import create_table, create_index, insert_bulk
from benchmark import single_processing, threading_processing, multiprocessing_processing
from scalability_test import run_scalability_test, generate_reviews

# ==============================
# File path configuration
# ==============================
BASE_DIR = os.path.dirname(__file__)  # folder where main.py is
FILE_PATH = os.path.join(BASE_DIR, "sample_texts", "feedback.txt")

# Ensure sample_texts folder exists
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

# Create dummy feedback.txt if missing
if not os.path.exists(FILE_PATH):
    print(f"❌ File not found: {FILE_PATH}")
    print("Creating a dummy feedback.txt file...")
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write("This is a sample review.\n")
    print(f"✅ Dummy file created at: {FILE_PATH}")

# ==============================
# Benchmark function
# ==============================
def run_benchmark(reviews):
    print("\n--- Performance Comparison ---")
    _, t1 = single_processing(reviews)
    print(f"Single Processing: {t1:.4f} sec")

    _, t2 = threading_processing(reviews)
    print(f"Threading: {t2:.4f} sec")

    _, t3 = multiprocessing_processing(reviews)
    print(f"Multiprocessing: {t3:.4f} sec")


# ==============================
# Main execution
# ==============================
if __name__ == "__main__":

    # Create database table and index
    create_table()
    create_index()

    # Load reviews (real or dummy)
    reviews = load_reviews(FILE_PATH)
    print(f"Loaded {len(reviews)} reviews.")

    # Run performance benchmark
    run_benchmark(reviews)

    # Run scalability tests
    run_scalability_test(100)
    run_scalability_test(10000)
    run_scalability_test(100000)