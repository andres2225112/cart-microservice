import os
os.environ["API_KEY"] = "test-key"

import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport

from app.main import app


MOCK_SUMMARY = {
    "user_id": "user_123",
    "total_products": 3,
    "total_quantity": 10,
    "top_product": {
        "product_id": "producto_101",
        "quantity": 5
    },
    "ttl_seconds": 7200,
    "expiring_soon": False
}


@pytest.mark.asyncio
async def test_get_summary_returns_200_with_correct_fields():
    with patch("app.controllers.cart_controller.cart_service") as mock_svc:
        mock_svc.get_summary = AsyncMock(return_value=MOCK_SUMMARY)

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:

            response = await client.get(
                "/api/cart/user_123/summary",
                headers={"x-api-key": "test-key"}
            )

        assert response.status_code == 200

        data = response.json()

        assert data["user_id"] == "user_123"
        assert data["total_products"] == 3
        assert data["total_quantity"] == 10
        assert data["ttl_seconds"] == 7200
        assert data["expiring_soon"] is False


@pytest.mark.asyncio
async def test_get_summary_returns_404_when_cart_not_found():
    with patch("app.controllers.cart_controller.cart_service") as mock_svc:

        mock_svc.get_summary = AsyncMock(
            side_effect=LookupError("Carrito no encontrado o vacío")
        )

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:

            response = await client.get(
                "/api/cart/fantasma/summary",
                headers={"x-api-key": "test-key"}
            )

        assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_summary_returns_500_on_unexpected_error():
    with patch("app.controllers.cart_controller.cart_service") as mock_svc:

        mock_svc.get_summary = AsyncMock(
            side_effect=Exception("Redis down")
        )

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:

            response = await client.get(
                "/api/cart/user_123/summary",
                headers={"x-api-key": "test-key"}
            )

        assert response.status_code == 500


@pytest.mark.asyncio
async def test_get_summary_expiring_soon_flag_is_true_when_ttl_low():

    mock_expiring = {
        **MOCK_SUMMARY,
        "ttl_seconds": 1800,
        "expiring_soon": True
    }

    with patch("app.controllers.cart_controller.cart_service") as mock_svc:

        mock_svc.get_summary = AsyncMock(
            return_value=mock_expiring
        )

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:

            response = await client.get(
                "/api/cart/user_123/summary",
                headers={"x-api-key": "test-key"}
            )

        assert response.status_code == 200

        data = response.json()

        assert data["expiring_soon"] is True
        assert data["ttl_seconds"] == 1800


@pytest.mark.asyncio
async def test_get_summary_top_product_has_correct_structure():

    with patch("app.controllers.cart_controller.cart_service") as mock_svc:

        mock_svc.get_summary = AsyncMock(
            return_value=MOCK_SUMMARY
        )

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:

            response = await client.get(
                "/api/cart/user_123/summary",
                headers={"x-api-key": "test-key"}
            )

        data = response.json()

        assert "product_id" in data["top_product"]
        assert "quantity" in data["top_product"]