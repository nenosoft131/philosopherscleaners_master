from fastapi import Request
from starlette.responses import JSONResponse
from collections import defaultdict, deque
import time
import asyncio

# Config
ROUTE_LIMITS = {
    "/login": {"max": 5, "window": 60},     # 5 requests per 60 seconds
    "/data": {"max": 100, "window": 60},    # 100 requests per 60 seconds
}
DEFAULT_LIMIT = {"max": 10, "window": 60}

requests_store = defaultdict(lambda: defaultdict(deque))  # user/ip -> route -> timestamps
lock = asyncio.Lock()

async def rate_limiter_middleware(request: Request, call_next):
    ip = request.client.host
    route = request.url.path
    current_time = time.time()
    
    limit = ROUTE_LIMITS.get(route, DEFAULT_LIMIT)
    max_requests = limit["max"]
    window = limit["window"]

    async with lock:
        timestamps = requests_store[ip][route]

        # Remove expired requests
        while timestamps and current_time - timestamps[0] > window:
            timestamps.popleft()

        if len(timestamps) >= max_requests:
            retry_after = window - (current_time - timestamps[0])
            headers = {
                "X-RateLimit-Limit": str(max_requests),
                "X-RateLimit-Remaining": "0",
                "Retry-After": str(round(retry_after, 1))
            }
            return JSONResponse(
                status_code=429,
                content={"error": "Too Many Requests"},
                headers=headers
            )

        timestamps.append(current_time)
        remaining = max_requests - len(timestamps)

    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(max_requests)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    return response
