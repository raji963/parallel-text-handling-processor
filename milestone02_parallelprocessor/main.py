from text_loader import load_reviews
from database import create_table, create_index, insert_bulk
from benchmark import single_processing, threading_processing, multiprocessing_processing
from scalability_test import run_scalability_test, generate_reviews


FILE_PATH = "sample_texts/feedback.txt"


def run_benchmark(reviews):
    print("\n--- Performance Comparison ---")

    _, t1 = single_processing(reviews)
    print(f"Single Processing: {t1:.4f} sec")

    _, t2 = threading_processing(reviews)
    print(f"Threading: {t2:.4f} sec")

    _, t3 = multiprocessing_processing(reviews)
    print(f"Multiprocessing: {t3:.4f} sec")


if __name__ == "__main__":

    # Create database table and index
    create_table()
    create_index()

    # Load real file reviews
    reviews = load_reviews(FILE_PATH)

    # Run performance benchmark
    run_benchmark(reviews)

    # Run scalability tests
    run_scalability_test(100)
    run_scalability_test(10000)
    run_scalability_test(100000)