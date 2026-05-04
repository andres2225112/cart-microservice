import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from app.main import app


@pytest.mark.asyncio
async def test_update_item_returns_200_with_valid_quantity():
    with patch("app.services.cart_service.cart_repository") as mock_repo:
        mock_repo.item_exists = AsyncMock(return_value=True)
        mock_repo.update_item_quantity = AsyncMock(return_value=None)

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.put(
                "/api/cart/user_123/items/producto_101",
                json={"quantity": 5}
            )

        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "user_123"
        assert data["product_id"] == "producto_101"
        assert data["quantity"] == 5


@pytest.mark.asyncio
async def test_update_item_returns_422_when_quantity_is_zero():
    with patch("app.services.cart_service.cart_repository") as mock_repo:
        mock_repo.add_or_update_item = AsyncMock(return_value=None)

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.put(
                "/api/cart/user_123/items/producto_101",
                json={"quantity": 0}
            )

        assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_item_returns_422_when_quantity_is_negative():
    with patch("app.services.cart_service.cart_repository") as mock_repo:
        mock_repo.add_or_update_item = AsyncMock(return_value=None)

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.put(
                "/api/cart/user_123/items/producto_101",
                json={"quantity": -3}
            )

        assert response.status_code == 422