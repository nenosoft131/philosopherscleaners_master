import pytest
from httpx import AsyncClient
from fastapi import FastAPI
import logging

# Import your middleware
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
        import asyncio

        await asyncio.sleep(0.6)
        return {"message": "slow"}

    return app


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# =========================
# TESTS
# =========================


@pytest.mark.asyncio
async def test_request_success(client):
    response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

    # headers added by middleware
    assert "X-Request-ID" in response.headers
    assert "X-Trace-ID" in response.headers


@pytest.mark.asyncio
async def test_request_id_propagation(client):
    headers = {"X-Request-ID": "test-id-123"}

    response = await client.get("/", headers=headers)

    assert response.headers["X-Request-ID"] == "test-id-123"
    assert response.headers["X-Trace-ID"] == "test-id-123"


@pytest.mark.asyncio
async def test_error_handling(client):
    response = await client.get("/error")

    assert response.status_code == 500
    body = response.json()

    assert "error" in body
    assert body["error"] == "Internal Server Error"
    assert "request_id" in body


@pytest.mark.asyncio
async def test_slow_request_logging(client, caplog):
    caplog.set_level(logging.WARNING)

    await client.get("/slow")

    logs = [record.message for record in caplog.records]

    assert any("slow_request" in str(log) for log in logs)


@pytest.mark.asyncio
async def test_logging_request_start(client, caplog):
    caplog.set_level(logging.INFO)

    await client.get("/")

    logs = [record.message for record in caplog.records]

    assert any("request_start" in str(log) for log in logs)
    assert any("request_end" in str(log) for log in logs)


@pytest.mark.asyncio
async def test_security_headers(client):
    response = await client.get("/")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"
