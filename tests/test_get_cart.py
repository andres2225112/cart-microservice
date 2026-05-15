import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from app.main import app


@pytest.mark.asyncio
async def test_get_cart_returns_cart_data(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    with patch("app.controllers.cart_controller.cart_service") as mock_service:
        mock_service.get_cart = AsyncMock(return_value={
            "user_id": "user_123",
            "items": {"producto_101": 2, "producto_205": 1},
            "total_items": 2,
            "total_quantity": 3,
            "page": 1,
            "page_size": 2,
            "total_pages": 1
        })

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get(
                "/api/cart/user_123",
                headers={"X-API-Key": "test-key"}
            )

        assert response.status_code == 200
        data = response.json()
        assert data["items"]["producto_101"] == 2
        assert data["total_items"] == 2


@pytest.mark.asyncio
async def test_get_cart_returns_404_when_empty(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    with patch("app.controllers.cart_controller.cart_service") as mock_service:
        mock_service.get_cart = AsyncMock(
            side_effect=ValueError("Carrito no encontrado o vacío")
        )

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get(
                "/api/cart/user_inexistente",
                headers={"X-API-Key": "test-key"}
            )

        assert response.status_code == 404
