import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count
from rule_engine import analyze_sentiment


def single_processing(reviews):
    start = time.time()
    results = [analyze_sentiment(r) for r in reviews]
    end = time.time()
    return results, end - start


def threading_processing(reviews):
    start = time.time()
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(analyze_sentiment, reviews))
    end = time.time()
    return results, end - start


def multiprocessing_processing(reviews):
    start = time.time()
    with Pool(cpu_count()) as pool:
        results = pool.map(analyze_sentiment, reviews)
    end = time.time()
    return results, end - start