from app.redis_client import get_redis

CART_TTL_SECONDS = 86400  # 24 horas


class CartRepository:
    async def add_or_update_item(self, user_id: str, product_id: str, quantity: int) -> None:
        """
        Guarda o actualiza un producto en el carrito del usuario.

        Args:
            user_id: Identificador del usuario propietario del carrito.
            product_id: Identificador del producto a guardar o actualizar.
            quantity: Cantidad del producto.

        Returns:
            None. Reinicia el TTL a 24 horas en cada interaccion.
        """
        redis = get_redis()
        cart_key = f"cart:{user_id}"

        await redis.hset(cart_key, product_id, str(quantity))
        await redis.expire(cart_key, CART_TTL_SECONDS)

    async def get_cart(self, user_id: str) -> dict:
        """
        Retorna todos los productos del carrito.

        Args:
            user_id: Identificador del usuario propietario del carrito.

        Returns:
            Diccionario con los productos y cantidades. Retorna dict
            vacio si el carrito no existe.
        """
        redis = get_redis()
        cart_key = f"cart:{user_id}"
        return await redis.hgetall(cart_key)

    async def remove_item(self, user_id: str, product_id: str) -> None:
        """
        Elimina un producto especifico del carrito del usuario.

        Args:
            user_id: Identificador del usuario propietario del carrito.
            product_id: Identificador del producto a eliminar.

        Returns:
            None. Si el producto no existe, Redis no lanza error.
        """
        redis = get_redis()
        cart_key = f"cart:{user_id}"

        await redis.hdel(cart_key, product_id)
        return None

    async def update_item_quantity(self, user_id: str, product_id: str, quantity: int) -> None:
        """
        Actualiza la cantidad de un producto existente en el carrito.

        Args:
            user_id: Identificador del usuario propietario del carrito.
            product_id: Identificador del producto a actualizar.
            quantity: Nueva cantidad del producto (debe ser > 0, validado en el Service).

        Returns:
            None. Reinicia el TTL a 24 horas tras la actualizacion.
        """
        redis = get_redis()
        cart_key = f"cart:{user_id}"

        await redis.hset(cart_key, product_id, str(quantity))
        await redis.expire(cart_key, CART_TTL_SECONDS)
        return None

    async def clear_cart(self, user_id: str) -> None:
        """
        Elimina el carrito completo del usuario de Redis.

        Args:
            user_id: Identificador del usuario cuyo carrito se vaciara.

        Returns:
            None. Si el carrito no existe, Redis no lanza error.
        """
        redis = get_redis()
        cart_key = f"cart:{user_id}"
        await redis.delete(cart_key)
        return None

    async def cart_exists(self, user_id: str) -> bool:
        """
        Verifica si existe una clave de carrito para el usuario en Redis.

        Args:
            user_id: Identificador del usuario a verificar.

        Returns:
            True si la clave cart:{user_id} existe en Redis, False en caso contrario.
        """
        redis = get_redis()
        return bool(await redis.exists(f"cart:{user_id}"))

    async def item_exists(self, user_id: str, product_id: str) -> bool:
        """
        Verifica si un producto especifico existe en el carrito del usuario.

        Args:
            user_id: Identificador del usuario propietario del carrito.
            product_id: Identificador del producto a verificar.

        Returns:
            True si el campo product_id existe en el hash cart:{user_id}, False si no.
        """
        redis = get_redis()
        return bool(await redis.hexists(f"cart:{user_id}", product_id))

    async def get_ttl(self, user_id: str) -> int:
        """
        Consulta el tiempo de vida restante (TTL) del carrito en Redis.

        Args:
            user_id: Identificador del usuario cuyo TTL se consultara.

        Returns:
            Entero con los segundos restantes (> 0), -1 si no tiene TTL asignado,
            o -2 si la clave no existe en Redis.
        """
        redis = get_redis()
        cart_key = f"cart:{user_id}"
        return await redis.ttl(cart_key)
