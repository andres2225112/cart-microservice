import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from app.main import app

@pytest.mark.asyncio
async def test_add_item_returns_201():
    with patch("app.services.cart_service.cart_repository") as mock_repo:
        mock_repo.add_or_update_item = AsyncMock(return_value=None)
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/cart/user_123/items",
                json={"product_id": "producto_101", "quantity": 2}
            )

            assert response.status_code == 201
            data = response.json()
            assert data["product_id"] == "producto_101"
            assert data["quantity"] == 2

@pytest.mark.asyncio
async def test_add_item_returns_422_when_quantity_is_zero():
    with patch("app.services.cart_service.cart_repository") as mock_repo:
        mock_repo.add_or_update_item = AsyncMock(return_value=None)
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/cart/user_123/items",
                json={"product_id": "producto_101", "quantity": 0}
            )

            assert response.status_code == 422
