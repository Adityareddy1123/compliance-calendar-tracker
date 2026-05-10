import requests
import time
import statistics

URLS = [
    "http://localhost:5000/health"
]

results = {}

for url in URLS:

    response_times = []

    print(f"\nTesting: {url}")

    for i in range(50):

        start = time.time()

        response = requests.get(url)

        end = time.time()

        response_time_ms = (end - start) * 1000

        response_times.append(response_time_ms)

        print(f"Request {i+1}: {round(response_time_ms, 2)} ms")

    response_times.sort()

    p50 = statistics.median(response_times)
    p95 = response_times[int(0.95 * len(response_times)) - 1]
    p99 = response_times[int(0.99 * len(response_times)) - 1]

    results[url] = {
        "p50": round(p50, 2),
        "p95": round(p95, 2),
        "p99": round(p99, 2)
    }

print("\nPerformance Benchmark Results\n")

for url, data in results.items():

    print(f"Endpoint: {url}")

    print(f"P50: {data['p50']} ms")
    print(f"P95: {data['p95']} ms")
    print(f"P99: {data['p99']} ms")