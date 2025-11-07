import asyncio
import time
from statistics import (
    mean,
    median,
    stdev,
)
from typing import List

import httpx


async def make_request(
    client: httpx.AsyncClient,
    url: str,
    short_url: str,
) -> tuple[float, int]:
    start_time = time.time()
    try:
        response = await client.get(f"{url}/urls/{short_url}")
        elapsed = time.time() - start_time
        return elapsed, response.status_code
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"Error: {e}")
        return elapsed, 0


async def run_load_test(
    base_url: str,
    short_url: str,
    total_requests: int,
    concurrent_requests: int,
):
    print("Starting load test:")
    print(f"  URL: {base_url}/urls/{short_url}")
    print(f"  Total requests: {total_requests}")
    print(f"  Concurrent requests: {concurrent_requests}")
    print()

    semaphore = asyncio.Semaphore(concurrent_requests)
    results: List[tuple[float, int]] = []
    completed = 0
    lock = asyncio.Lock()

    async def worker():
        nonlocal completed
        async with httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=1000, max_connections=1000),
        ) as client:
            while True:
                async with lock:
                    if completed >= total_requests:
                        break
                    completed += 1

                async with semaphore:
                    result = await make_request(client, base_url, short_url)
                    async with lock:
                        results.append(result)
                        if len(results) % 1000 == 0:
                            print(
                                f"Completed {len(results)}/{total_requests} requests...",
                            )

    start_total = time.time()

    workers = [asyncio.create_task(worker()) for _ in range(concurrent_requests)]
    await asyncio.gather(*workers)

    total_time = time.time() - start_total

    response_times = [r[0] for r in results]
    status_codes = [r[1] for r in results]

    successful = sum(1 for code in status_codes if code == 200)
    failed = len(status_codes) - successful

    print("\n" + "=" * 60)
    print("LOAD TEST RESULTS")
    print("=" * 60)
    print(f"Total requests: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Requests per second: {len(results) / total_time:.2f}")
    print()
    print("Response time statistics:")
    print(f"  Min: {min(response_times) * 1000:.2f}ms")
    print(f"  Max: {max(response_times) * 1000:.2f}ms")
    print(f"  Mean: {mean(response_times) * 1000:.2f}ms")
    print(f"  Median: {median(response_times) * 1000:.2f}ms")
    if len(response_times) > 1:
        print(f"  Std Dev: {stdev(response_times) * 1000:.2f}ms")
    print()
    print("Status codes:")
    status_counts = {}
    for code in status_codes:
        status_counts[code] = status_counts.get(code, 0) + 1
    for code, count in sorted(status_counts.items()):
        print(f"  {code}: {count}")


if __name__ == "__main__":
    import sys

    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    short_url = sys.argv[2] if len(sys.argv) > 2 else "1hRHjOFZYsp4J3jXIIvNtt"
    total_requests = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
    concurrent = int(sys.argv[4]) if len(sys.argv) > 4 else 500

    asyncio.run(
        run_load_test(
            base_url=base_url,
            short_url=short_url,
            total_requests=total_requests,
            concurrent_requests=concurrent,
        ),
    )
