import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from app.main import app


@pytest.mark.asyncio
async def test_update_item_returns_200_with_valid_quantity(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    with patch("app.controllers.cart_controller.cart_service") as mock_service:
        mock_service.update_item = AsyncMock(return_value={
            "user_id": "user_123",
            "product_id": "producto_101",
            "quantity": 5
        })

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.put(
                "/api/cart/user_123/items/producto_101",
                json={"quantity": 5},
                headers={"X-API-Key": "test-key"}
            )

        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "user_123"
        assert data["product_id"] == "producto_101"
        assert data["quantity"] == 5


@pytest.mark.asyncio
async def test_update_item_returns_422_when_quantity_is_zero(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    with patch("app.controllers.cart_controller.cart_service") as mock_service:
        mock_service.update_item = AsyncMock(
            side_effect=ValueError("La cantidad debe ser mayor a 0")
        )

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.put(
                "/api/cart/user_123/items/producto_101",
                json={"quantity": 0},
                headers={"X-API-Key": "test-key"}
            )

        assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_item_returns_422_when_quantity_is_negative(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    with patch("app.controllers.cart_controller.cart_service") as mock_service:
        mock_service.update_item = AsyncMock(
            side_effect=ValueError("La cantidad debe ser mayor a 0")
        )

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.put(
                "/api/cart/user_123/items/producto_101",
                json={"quantity": -3},
                headers={"X-API-Key": "test-key"}
            )

        assert response.status_code == 422
