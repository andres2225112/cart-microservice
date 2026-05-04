import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from app.main import app


@pytest.mark.asyncio
async def test_clear_cart_returns_200():
    with patch("app.controllers.cart_controller.cart_service") as mock_service:
        mock_service.clear_cart = AsyncMock(return_value={
            "user_id": "user_123",
            "message": "Carrito eliminado exitosamente"
        })

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.delete("/api/cart/user_123")

        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "user_123"
        assert "message" in data


@pytest.mark.asyncio
async def test_get_cart_returns_404_after_clear():
    with patch("app.controllers.cart_controller.cart_service") as mock_service:
        mock_service.clear_cart = AsyncMock(return_value={
            "user_id": "user_123",
            "message": "Carrito eliminado exitosamente"
        })
        mock_service.get_cart = AsyncMock(side_effect=ValueError("Carrito no encontrado"))

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            await client.delete("/api/cart/user_123")
            response = await client.get("/api/cart/user_123")

        assert response.status_code == 404