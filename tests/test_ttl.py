import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from app.main import app


@pytest.mark.asyncio
async def test_get_ttl_returns_200_with_active_ttl():
    mock_result = {
        "user_id": "user_123",
        "ttl_seconds": 82400,
        "ttl_hours": 22.89,
        "warning": None,
    }

    with patch("app.controllers.cart_controller.cart_service") as mock_svc:
        mock_svc.get_ttl = AsyncMock(return_value=mock_result)

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.get("/api/cart/user_123/ttl")

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user_123"
    assert data["ttl_seconds"] == 82400
    assert data["ttl_hours"] == 22.89
    assert data["warning"] is None


@pytest.mark.asyncio
async def test_get_ttl_returns_200_with_warning_when_no_ttl_set():
    mock_result = {
        "user_id": "user_123",
        "ttl_seconds": -1,
        "ttl_hours": None,
        "warning": "Cart has no expiration set",
    }

    with patch("app.controllers.cart_controller.cart_service") as mock_svc:
        mock_svc.get_ttl = AsyncMock(return_value=mock_result)

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.get("/api/cart/user_123/ttl")

    assert response.status_code == 200
    data = response.json()
    assert data["ttl_seconds"] == -1
    assert data["ttl_hours"] is None
    assert data["warning"] == "Cart has no expiration set"


@pytest.mark.asyncio
async def test_get_ttl_returns_404_when_cart_not_found():
    with patch("app.controllers.cart_controller.cart_service") as mock_svc:
        mock_svc.get_ttl = AsyncMock(
            side_effect=LookupError("Carrito no encontrado o expirado")
        )

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.get("/api/cart/usuario_fantasma/ttl")

    assert response.status_code == 404
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_get_ttl_returns_500_on_unexpected_error():
    with patch("app.controllers.cart_controller.cart_service") as mock_svc:
        mock_svc.get_ttl = AsyncMock(
            side_effect=Exception("Redis down")
        )

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.get("/api/cart/user_123/ttl")

    assert response.status_code == 500