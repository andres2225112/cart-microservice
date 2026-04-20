import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock
from app.main import app


@pytest.mark.asyncio
async def test_delete_item_success():
    with patch("app.controllers.cart_controller.cart_service") as mock_service:
        mock_service.remove_item = AsyncMock(return_value={
            "user_id": "user_123",
            "product_id": "producto_101"
        })

        transport = ASGITransport(app=app)

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete(
                "/api/cart/user_123/items/producto_101"
            )

        assert response.status_code == 200
        data = response.json()

        assert data["user_id"] == "user_123"
        assert data["product_id"] == "producto_101"

        mock_service.remove_item.assert_called_once_with(
            "user_123", "producto_101"
        )


@pytest.mark.asyncio
async def test_delete_item_calls_service():
    with patch("app.controllers.cart_controller.cart_service") as mock_service:
        mock_service.remove_item = AsyncMock(return_value={
            "user_id": "user_123",
            "product_id": "producto_101"
        })

        transport = ASGITransport(app=app)

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            await client.delete("/api/cart/user_123/items/producto_101")

        mock_service.remove_item.assert_called_once()
