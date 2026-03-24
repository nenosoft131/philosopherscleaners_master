from fastapi import Request
from starlette.responses import JSONResponse
import time
import logging
import uuid

logger = logging.getLogger("middleware")
logging.basicConfig(level=logging.INFO)


async def http_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    client_ip = request.client.host if request.client else "unknown"

    logger.info(
        f"[{request_id}] Incoming request | "
        f"{request.method} {request.url.path} | "
        f"Client: {client_ip}"
    )

    try:
        response = await call_next(request)

    except Exception as ex:
        process_time = (time.perf_counter() - start_time) * 1000

        logger.exception(
            f"[{request_id}] Error | "
            f"{request.method} {request.url.path} | "
            f"Time: {process_time:.2f}ms"
        )

        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "request_id": request_id,
                # avoid exposing details in prod
                "details": str(ex),
            },
        )

    process_time = (time.perf_counter() - start_time) * 1000

    # Add request ID to response headers
    response.headers["X-Request-ID"] = request_id

    # Estimate response size if possible
    content_length = response.headers.get("content-length", "unknown")

    log_message = (
        f"[{request_id}] Response | "
        f"Status: {response.status_code} | "
        f"Time: {process_time:.2f}ms | "
        f"Size: {content_length}"
    )

    # Highlight slow requests (>500ms)
    if process_time > 500:
        logger.warning(log_message + " ⚠️ Slow request")
    else:
        logger.info(log_message)

    return response
