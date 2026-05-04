from app.redis_client import get_redis

CART_TTL_SECONDS = 86400  # 24 horas


class CartRepository:
    async def add_or_update_item(self, user_id: str, product_id: str, quantity: int) -> None:
        """
        Guarda o actualiza un producto en el carrito del usuario.
        Reinicia el TTL a 24 horas en cada interacción.
        """
        redis = get_redis()
        cart_key = f"cart:{user_id}"

        await redis.hset(cart_key, product_id, str(quantity))
        await redis.expire(cart_key, CART_TTL_SECONDS)

    async def get_cart(self, user_id: str) -> dict:
        """
        Retorna todos los productos del carrito.
        Retorna dict vacío si el carrito no existe.
        """
        redis = get_redis()
        cart_key = f"cart:{user_id}"
        return await redis.hgetall(cart_key)

    async def remove_item(self, user_id: str, product_id: str) -> None:
        redis = get_redis()
        cart_key = f"cart:{user_id}"

        await redis.hdel(cart_key, product_id)
        return None

    async def update_item_quantity(self, user_id: str, product_id: str, quantity: int) -> None:
        redis = get_redis()
        cart_key = f"cart:{user_id}"

        await redis.hset(cart_key, product_id, str(quantity))
        await redis.expire(cart_key, CART_TTL_SECONDS)
        return None

    async def clear_cart(self, user_id: str) -> None:
        redis = get_redis()
        cart_key = f"cart:{user_id}"

        await redis.delete(cart_key)
        return None
    
    async def cart_exists(self, user_id: str) -> bool:
        redis = get_redis()
        return bool(await redis.exists(f"cart:{user_id}"))

    async def item_exists(self, user_id: str, product_id: str) -> bool:
        redis = get_redis()
        return bool(await redis.hexists(f"cart:{user_id}", product_id))

    async def get_ttl(self, user_id: str) -> int:
        """
        Consulta el TTL de la clave cart:{user_id} en Redis.
        Retorna entero positivo (segundos restantes), -1 (sin TTL) o -2 (no existe).
        El Repository no interpreta el valor: esa responsabilidad es del Service.
        """
        redis = get_redis()
        cart_key = f"cart:{user_id}"
        return await redis.ttl(cart_key)
