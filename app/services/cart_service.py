from app.repositories.cart_repository import CartRepository
from app.logger import get_logger

logger = get_logger(__name__)
cart_repository = CartRepository()


class CartService:

    async def add_item(self, user_id: str, product_id: str, quantity: int) -> dict:
        """
        Valida los datos y llama al repositorio para guardar el producto.
        """
        try:
            if quantity <= 0:
                logger.warning(f'add_item rejected: quantity={quantity} for user={user_id}')
                raise ValueError("La cantidad debe ser mayor a 0")
            if not product_id or not product_id.strip():
                logger.warning(f'add_item rejected: empty product_id for user={user_id}')
                raise ValueError("El product_id no puede estar vacío")

            await cart_repository.add_or_update_item(user_id, product_id, quantity)
            
            logger.info(f'add_item ok: user={user_id} product={product_id} qty={quantity}')

            return {
                "user_id": user_id,
                "product_id": product_id,
                "quantity": quantity
            }
        except Exception as e:
            if not isinstance(e, (ValueError, LookupError)):
                logger.error(f'unexpected error in add_item: user={user_id} err={str(e)}')
            raise

    async def get_cart(self, user_id: str) -> dict:
        try:
            cart_data = await cart_repository.get_cart(user_id)

            if not cart_data:
                logger.info(f'get_cart: empty or not found for user={user_id}')
                raise ValueError("Carrito no encontrado o vacío")

            items = {
                product_id: int(quantity)
                for product_id, quantity in cart_data.items()
            }

            total_items = sum(items.values())
            logger.info(f'get_cart ok: user={user_id} items={len(items)} total={total_items}')

            return {
                "user_id": user_id,
                "items": items,
                "total_items": total_items
            }
        except Exception as e:
            if not isinstance(e, (ValueError, LookupError)):
                logger.error(f'unexpected error in get_cart: user={user_id} err={str(e)}')
            raise
    async def remove_item(self, user_id: str, product_id: str) -> dict:
        try:
            if not product_id or not product_id.strip():
                logger.warning(f'remove_item rejected: empty product_id for user={user_id}')
                raise ValueError("El product_id no puede estar vacío")

            exists = await cart_repository.item_exists(user_id, product_id)
            if not exists:
                raise LookupError(f"Producto {product_id} no encontrado en el carrito")

            await cart_repository.remove_item(user_id, product_id)
            
            logger.info(f'remove_item ok: user={user_id} product={product_id}')

            return {
                "user_id": user_id,
                "product_id": product_id
            }
        except Exception as e:
            if not isinstance(e, (ValueError, LookupError)):
                logger.error(f'unexpected error in remove_item: user={user_id} err={str(e)}')
            raise





    async def update_item(self, user_id: str, product_id: str, quantity: int) -> dict:
        try:
            if quantity <= 0:
                logger.warning(f'update_item rejected: quantity={quantity} for user={user_id}')
                raise ValueError("La cantidad debe ser mayor a 0")
            if not product_id or not product_id.strip():
                logger.warning(f'update_item rejected: empty product_id for user={user_id}')
                raise ValueError("El product_id no puede estar vacío")

            exists = await cart_repository.item_exists(user_id, product_id)
            if not exists:
                raise LookupError(f"Producto {product_id} no encontrado en el carrito")

            await cart_repository.update_item_quantity(user_id, product_id, quantity)
            
            logger.info(f'update_item ok: user={user_id} product={product_id} qty={quantity}')

            return {
                "user_id": user_id,
                "product_id": product_id,
                "quantity": quantity
            }
        except Exception as e:
            if not isinstance(e, (ValueError, LookupError)):
                logger.error(f'unexpected error in update_item: user={user_id} err={str(e)}')
            raise





    async def clear_cart(self, user_id: str) -> dict:
        try:
            await cart_repository.clear_cart(user_id)
            logger.info(f'clear_cart ok: user={user_id}')
            return {
                "user_id": user_id,
                "message": "Carrito eliminado exitosamente"
            }
        except Exception as e:
            if not isinstance(e, (ValueError, LookupError)):
                logger.error(f'unexpected error in clear_cart: user={user_id} err={str(e)}')
            raise
