import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from app.main import app


@pytest.mark.asyncio
async def test_delete_item_returns_404_when_item_not_found():
    with patch("app.controllers.cart_controller.cart_service") as mock_service:
        mock_service.remove_item = AsyncMock(
            side_effect=LookupError("Producto producto_101 no encontrado en el carrito")
        )

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.delete("/api/cart/user_123/items/producto_101")

        assert response.status_code == 404
        assert "producto_101" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_item_returns_404_when_item_not_found():
    with patch("app.controllers.cart_controller.cart_service") as mock_service:
        mock_service.update_item = AsyncMock(
            side_effect=LookupError("Producto producto_101 no encontrado en el carrito")
        )

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.put(
                "/api/cart/user_123/items/producto_101",
                json={"quantity": 5}
            )

        assert response.status_code == 404
        assert "producto_101" in response.json()["detail"]