import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from app.main import app


@pytest.mark.asyncio
async def test_health_returns_ok_when_redis_responds():
    with patch("app.main.get_redis") as mock_get:
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock(return_value=True)
        mock_get.return_value = mock_redis
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["redis"] == "ok"
        assert data["detail"] is None


@pytest.mark.asyncio
async def test_health_returns_degraded_when_redis_fails():
    with patch("app.main.get_redis") as mock_get:
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock(side_effect=Exception("Connection refused"))
        mock_get.return_value = mock_redis
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "degraded"
        assert data["redis"] == "error"
        assert data["detail"] is not None


@pytest.mark.asyncio
async def test_health_returns_degraded_when_client_not_initialized():
    with patch("app.main.get_redis", return_value=None):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "degraded"
        assert data["detail"] == "client not initialized"
