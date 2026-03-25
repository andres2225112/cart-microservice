import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from app.main import app


@pytest.mark.asyncio
async def test_get_cart_returns_cart_data():
    mock_cart = {"producto_101": "2", "producto_205": "1"}

    with patch("app.services.cart_service.cart_repository") as mock_repo:
        mock_repo.get_cart = AsyncMock(return_value=mock_cart)

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/cart/user_123")

        assert response.status_code == 200
        data = response.json()
        assert data["items"]["producto_101"] == 2
        assert data["total_items"] == 3


@pytest.mark.asyncio
async def test_get_cart_returns_404_when_empty():
    with patch("app.services.cart_service.cart_repository") as mock_repo:
        mock_repo.get_cart = AsyncMock(return_value={})

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/cart/user_inexistente")

        assert response.status_code == 404
