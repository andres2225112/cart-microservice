import pytest
import pytest_asyncio 
from unittest.mock import AsyncMock, patch
from app.repositories.cart_repository import CartRepository

@pytest.mark.asyncio
async def test_add_or_update_item_calls_hset_and_expire():
    mock_redis = AsyncMock()

    with patch("app.repositories.cart_repository.get_redis", return_value=mock_redis):
        repo = CartRepository()
        await repo.add_or_update_item("user_123", "producto_101", 2)

        mock_redis.hset.assert_called_once_with("cart:user_123", "producto_101", "2")
        mock_redis.expire.assert_called_once_with("cart:user_123", 86400)
