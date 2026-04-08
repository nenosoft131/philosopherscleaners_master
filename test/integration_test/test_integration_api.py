import pytest
from httpx import AsyncClient
from fastapi import FastAPI
import asyncio
import logging

from your_module import AdvancedMiddleware


@pytest.fixture
def app():
    app = FastAPI()
    app.add_middleware(AdvancedMiddleware)

    @app.get("/ok")
    async def ok():
        return {"status": "ok"}

    @app.get("/fail")
    async def fail():
        raise RuntimeError("failure")

    @app.get("/slow")
    async def slow():
        await asyncio.sleep(0.6)
        return {"status": "slow"}

    return app


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# ==========================================
# FULL REQUEST LIFECYCLE TEST
# ==========================================
@pytest.mark.asyncio
async def test_full_request_lifecycle(client, caplog):
    caplog.set_level(logging.INFO)

    response = await client.get("/ok")

    # --- Response correctness ---
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    # --- Headers injected ---
    assert "X-Request-ID" in response.headers
    assert "X-Trace-ID" in response.headers

    # --- Security headers ---
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"

    # --- Logging lifecycle ---
    logs = [r.message for r in caplog.records]
    assert any("request_start" in log for log in logs)
    assert any("request_end" in log for log in logs)


# ==========================================
# ERROR FLOW INTEGRATION
# ==========================================
@pytest.mark.asyncio
async def test_error_flow_integration(client, caplog):
    caplog.set_level(logging.ERROR)

    response = await client.get("/fail")

    # --- HTTP layer ---
    assert response.status_code == 500

    # --- Body structure ---
    body = response.json()
    assert body["error"] == "Internal Server Error"
    assert "request_id" in body

    # --- Headers preserved even on failure ---
    assert "X-Request-ID" in response.headers

    # --- Logging captured ---
    logs = [r.message for r in caplog.records]
    assert any("exception" in log.lower() for log in logs)


# ==========================================
# TRACE PROPAGATION ACROSS CALLS
# ==========================================
@pytest.mark.asyncio
async def test_trace_propagation_chain(client):
    trace_id = "trace-abc-123"

    r1 = await client.get("/ok", headers={"X-Request-ID": trace_id})
    r2 = await client.get("/ok", headers={"X-Request-ID": trace_id})

    assert r1.headers["X-Trace-ID"] == trace_id
    assert r2.headers["X-Trace-ID"] == trace_id


# ==========================================
# CONCURRENT SYSTEM BEHAVIOR
# ==========================================
@pytest.mark.asyncio
async def test_system_under_concurrency(client):
    async def call():
        return await client.get("/ok")

    responses = await asyncio.gather(*[call() for _ in range(10)])

    ids = [r.headers["X-Request-ID"] for r in responses]

    # Ensure isolation between requests
    assert len(set(ids)) == len(ids)

    # All responses valid
    assert all(r.status_code == 200 for r in responses)


# ==========================================
# SLOW REQUEST + LOGGING INTEGRATION
# ==========================================
@pytest.mark.asyncio
async def test_slow_request_triggers_warning(client, caplog):
    caplog.set_level(logging.WARNING)

    response = await client.get("/slow")

    assert response.status_code == 200

    logs = [r.message for r in caplog.records]
    assert any("slow_request" in log for log in logs)


# ==========================================
# MIXED TRAFFIC SCENARIO (REALISTIC LOAD)
# ==========================================
@pytest.mark.asyncio
async def test_mixed_traffic(client):
    async def ok():
        return await client.get("/ok")

    async def fail():
        return await client.get("/fail")

    async def slow():
        return await client.get("/slow")

    responses = await asyncio.gather(ok(), ok(), fail(), slow(), ok(), fail())

    status_codes = [r.status_code for r in responses]

    assert 200 in status_codes
    assert 500 in status_codes

    # Ensure every response has request id
    for r in responses:
        assert "X-Request-ID" in r.headers
