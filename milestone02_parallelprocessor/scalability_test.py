import time
from benchmark import single_processing
from database import insert_bulk, query_by_sentiment


def generate_reviews(n):
    base = "This product is amazing but has minor error"
    return [base for _ in range(n)]


def run_scalability_test(n):
    reviews = generate_reviews(n)

    # Processing time
    results, process_time = single_processing(reviews)

    # Insert time
    start_insert = time.time()
    insert_bulk(results)
    insert_time = time.time() - start_insert

    # Query time
    start_query = time.time()
    query_by_sentiment("Positive")
    query_time = time.time() - start_query

    print(f"\nRecords: {n}")
    print(f"Processing time: {process_time:.4f} sec")
    print(f"Insert time: {insert_time:.4f} sec")
    print(f"Query time: {query_time:.4f} sec")