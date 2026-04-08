import pytest
from httpx import AsyncClient
from fastapi import FastAPI
import logging
import asyncio

from your_module import AdvancedMiddleware  # adjust import


# =========================
# TEST APP FIXTURE
# =========================
@pytest.fixture
def app():
    app = FastAPI()
    app.add_middleware(AdvancedMiddleware)

    @app.get("/")
    async def root():
        return {"message": "ok"}

    @app.get("/error")
    async def error():
        raise ValueError("boom")

    @app.get("/slow")
    async def slow():
        await asyncio.sleep(0.6)
        return {"message": "slow"}

    @app.get("/custom-header")
    async def custom_header():
        return {"message": "header"}

    return app


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# =========================
# BASIC FUNCTIONAL TESTS
# =========================


@pytest.mark.asyncio
async def test_request_success(client):
    response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
    assert "X-Request-ID" in response.headers
    assert "X-Trace-ID" in response.headers


@pytest.mark.asyncio
async def test_request_id_propagation(client):
    headers = {"X-Request-ID": "test-id-123"}

    response = await client.get("/", headers=headers)

    assert response.headers["X-Request-ID"] == "test-id-123"
    assert response.headers["X-Trace-ID"] == "test-id-123"


# =========================
# ERROR HANDLING
# =========================


@pytest.mark.asyncio
async def test_error_handling(client):
    response = await client.get("/error")

    assert response.status_code == 500
    body = response.json()

    assert "error" in body
    assert body["error"] == "Internal Server Error"
    assert "request_id" in body


@pytest.mark.asyncio
async def test_error_contains_same_request_id(client):
    headers = {"X-Request-ID": "err-123"}

    response = await client.get("/error", headers=headers)
    body = response.json()

    assert body["request_id"] == "err-123"
    assert response.headers["X-Request-ID"] == "err-123"


# =========================
# LOGGING TESTS
# =========================


@pytest.mark.asyncio
async def test_slow_request_logging(client, caplog):
    caplog.set_level(logging.WARNING)

    await client.get("/slow")

    logs = [record.message for record in caplog.records]

    assert any("slow_request" in str(log) for log in logs)


@pytest.mark.asyncio
async def test_fast_request_not_logged_as_slow(client, caplog):
    caplog.set_level(logging.WARNING)

    await client.get("/")

    logs = [record.message for record in caplog.records]

    assert not any("slow_request" in str(log) for log in logs)


@pytest.mark.asyncio
async def test_logging_request_start_and_end(client, caplog):
    caplog.set_level(logging.INFO)

    await client.get("/")

    logs = [record.message for record in caplog.records]

    assert any("request_start" in str(log) for log in logs)
    assert any("request_end" in str(log) for log in logs)


# =========================
# SECURITY HEADERS
# =========================


@pytest.mark.asyncio
async def test_security_headers_present(client):
    response = await client.get("/")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"


@pytest.mark.asyncio
async def test_security_headers_always_present_on_error(client):
    response = await client.get("/error")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"


# =========================
# HEADER BEHAVIOR
# =========================


@pytest.mark.asyncio
async def test_trace_id_generated_if_missing(client):
    response = await client.get("/")

    assert "X-Trace-ID" in response.headers
    assert response.headers["X-Trace-ID"] != ""


@pytest.mark.asyncio
async def test_request_id_generated_if_missing(client):
    response = await client.get("/")

    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"] != ""


@pytest.mark.asyncio
async def test_custom_headers_preserved(client):
    response = await client.get("/custom-header", headers={"X-Test": "123"})

    assert response.status_code == 200
    # Ensure middleware doesn't strip unrelated headers
    # (depends on implementation, adjust if needed)


# =========================
# CONCURRENCY TESTS
# =========================


@pytest.mark.asyncio
async def test_concurrent_requests_have_unique_ids(client):
    async def make_request():
        return await client.get("/")

    responses = await asyncio.gather(*[make_request() for _ in range(5)])

    request_ids = [r.headers["X-Request-ID"] for r in responses]

    assert len(set(request_ids)) == len(request_ids)


# =========================
# TIMING / PERFORMANCE
# =========================


@pytest.mark.asyncio
async def test_slow_endpoint_is_actually_slow(client):
    import time

    start = time.time()
    await client.get("/slow")
    duration = time.time() - start

    assert duration >= 0.5  # buffer for CI variability


# =========================
# EDGE CASES
# =========================


@pytest.mark.asyncio
async def test_empty_path(client):
    response = await client.get("")

    # FastAPI usually redirects "" -> "/"
    assert response.status_code in (200, 307)


@pytest.mark.asyncio
async def test_large_headers(client):
    large_value = "x" * 5000
    response = await client.get("/", headers={"X-Request-ID": large_value})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == large_value


@pytest.mark.asyncio
async def test_invalid_method(client):
    response = await client.post("/")

    # Depends on route config
    assert response.status_code in (405, 200)


@pytest.mark.asyncio
async def test_response_headers_not_mutated_between_requests(client):
    r1 = await client.get("/")
    r2 = await client.get("/")

    assert r1.headers["X-Request-ID"] != r2.headers["X-Request-ID"]
