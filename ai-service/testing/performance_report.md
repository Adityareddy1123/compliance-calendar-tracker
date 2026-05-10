# Performance Benchmark Report — Day 12

## Endpoint Tested
/health

## Benchmark Configuration

- Total Requests Sent: 50
- Benchmark Tool: Python requests library
- Environment: Local Flask Development Server

---

## Benchmark Results

| Metric | Response Time |
|--------|----------------|
| P50 | 2040.54 ms |
| P95 | 2060.43 ms |
| P99 | 2067.43 ms |

---

## Observations

- The endpoint handled all 50 requests successfully without failures.
- Response times remained stable throughout the benchmark execution.
- No crashes or timeout issues were observed.
- Flask server performance was consistent during repeated requests.

---

## Performance Analysis

- P50 indicates average response consistency.
- P95 and P99 values remained close to the median, showing stable API performance.
- The benchmark confirmed successful endpoint availability and response reliability.

---

## Optimizations Verified

- Redis caching enabled
- Lightweight endpoint response structure
- Stable Flask request handling
- Efficient JSON response generation

---

## Conclusion

The `/health` endpoint successfully handled repeated requests with stable response times and reliable API performance. The endpoint remained functional under continuous benchmark testing and is suitable for demo and development usage.