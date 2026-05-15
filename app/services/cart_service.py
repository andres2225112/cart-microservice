from app.repositories.cart_repository import CartRepository
from app.logger import get_logger

logger = get_logger(__name__)
cart_repository = CartRepository()


class CartService:

    async def add_item(self, user_id: str, product_id: str, quantity: int) -> dict:
        """
        Valida los datos y llama al repositorio para guardar el producto.

        Args:
            user_id: Identificador del usuario propietario del carrito.
            product_id: Identificador del producto a agregar.
            quantity: Cantidad del producto (debe ser mayor a 0).

        Returns:
            Diccionario con user_id, product_id y quantity guardados.

        Raises:
            ValueError: Si quantity <= 0 o product_id esta vacio.
        """
        try:
            if quantity <= 0:
                logger.warning(f'add_item rejected: quantity={quantity} for user={user_id}')
                raise ValueError("La cantidad debe ser mayor a 0")
            if not product_id or not product_id.strip():
                logger.warning(f'add_item rejected: empty product_id for user={user_id}')
                raise ValueError("El product_id no puede estar vacio")

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

    async def get_cart(self, user_id: str, page: int = 1, page_size: int = None) -> dict:
        """
        Retorna el contenido del carrito con soporte de paginacion opcional.

        Args:
            user_id: Identificador del usuario propietario del carrito.
            page: Numero de pagina (default 1).
            page_size: Cantidad de items por pagina. Si es None retorna todos.

        Returns:
            Diccionario con items, totales y datos de paginacion.

        Raises:
            ValueError: Si el carrito no existe o esta vacio.
        """
        try:
            cart_data = await cart_repository.get_cart(user_id)

            if not cart_data:
                logger.info(f'get_cart: empty or not found for user={user_id}')
                raise ValueError("Carrito no encontrado o vacio")

            all_items = {
                product_id: int(quantity)
                for product_id, quantity in cart_data.items()
            }
            total_items = len(all_items)
            total_quantity = sum(all_items.values())

            if page_size is not None:
                if page < 1:
                    raise ValueError("El numero de pagina debe ser mayor a 0")
                if page_size < 1:
                    raise ValueError("El tamano de pagina debe ser mayor a 0")

                items_list = list(all_items.items())
                start = (page - 1) * page_size
                end = start + page_size
                page_items = dict(items_list[start:end])
                total_pages = -(-total_items // page_size)  # ceil division
            else:
                page_items = all_items
                page = 1
                page_size = total_items
                total_pages = 1

            logger.info(
                f'get_cart ok: user={user_id} items={total_items} '
                f'page={page} page_size={page_size}'
            )
            return {
                "user_id": user_id,
                "items": page_items,
                "total_items": total_items,
                "total_quantity": total_quantity,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages
            }
        except Exception as e:
            if not isinstance(e, (ValueError, LookupError)):
                logger.error(f'unexpected error in get_cart: user={user_id} err={str(e)}')
            raise

    async def remove_item(self, user_id: str, product_id: str) -> dict:
        """
        Elimina un producto del carrito del usuario.

        Args:
            user_id: Identificador del usuario propietario del carrito.
            product_id: Identificador del producto a eliminar.

        Returns:
            Diccionario de confirmacion con user_id y product_id eliminado.

        Raises:
            ValueError: Si product_id esta vacio.
            LookupError: Si el producto no existe en el carrito.
        """
        try:
            if not product_id or not product_id.strip():
                logger.warning(f'remove_item rejected: empty product_id for user={user_id}')
                raise ValueError("El product_id no puede estar vacio")

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
        """
        Valida los datos y actualiza la cantidad de un producto existente en el carrito.

        Args:
            user_id: Identificador del usuario propietario del carrito.
            product_id: Identificador del producto a actualizar.
            quantity: Nueva cantidad (debe ser mayor a 0).

        Returns:
            Diccionario con user_id, product_id y quantity actualizados.

        Raises:
            ValueError: Si quantity <= 0 o product_id esta vacio.
            LookupError: Si el producto no existe en el carrito.
        """
        try:
            if quantity <= 0:
                logger.warning(f'update_item rejected: quantity={quantity} for user={user_id}')
                raise ValueError("La cantidad debe ser mayor a 0")
            if not product_id or not product_id.strip():
                logger.warning(f'update_item rejected: empty product_id for user={user_id}')
                raise ValueError("El product_id no puede estar vacio")

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

    async def get_ttl(self, user_id: str) -> dict:
        """
        Retorna el TTL del carrito con interpretacion semantica.

        Args:
            user_id: Identificador del usuario cuyo TTL se consultara.

        Returns:
            Diccionario con ttl_seconds, ttl_hours y warning.

        Raises:
            LookupError: Si el carrito no existe o ya expiro (TTL == -2).
        """
        try:
            ttl = await cart_repository.get_ttl(user_id)

            if ttl == -2:
                logger.info(f'get_ttl: cart not found for user={user_id}')
                raise LookupError("Carrito no encontrado o expirado")

            if ttl == -1:
                logger.warning(f'get_ttl: cart has no expiration for user={user_id}')
                return {
                    "user_id": user_id,
                    "ttl_seconds": -1,
                    "ttl_hours": None,
                    "warning": "Cart has no expiration set"
                }

            ttl_hours = round(ttl / 3600, 2)
            logger.info(f'get_ttl ok: user={user_id} ttl_seconds={ttl}')
            return {
                "user_id": user_id,
                "ttl_seconds": ttl,
                "ttl_hours": ttl_hours,
                "warning": None
            }
        except Exception as e:
            if not isinstance(e, (ValueError, LookupError)):
                logger.error(f'unexpected error in get_ttl: user={user_id} err={str(e)}')
            raise

    async def clear_cart(self, user_id: str) -> dict:
        """
        Vacia el carrito completo del usuario.

        Args:
            user_id: Identificador del usuario cuyo carrito se vaciara.

        Returns:
            Diccionario de confirmacion con user_id y mensaje.
        """
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

    async def get_summary(self, user_id: str) -> dict:
        """
        Retorna un resumen estadistico del carrito del usuario.

        Args:
            user_id: Identificador del usuario cuyo resumen se consultara.

        Returns:
            Diccionario con distinct_products, total_units, top_product,
            ttl_seconds y expiring_soon.

        Raises:
            LookupError: Si el carrito no existe o esta vacio.
        """
        try:
            cart_data = await cart_repository.get_cart(user_id)
            if not cart_data:
                raise LookupError("Carrito no encontrado o vacio")

            items = {pid: int(qty) for pid, qty in cart_data.items()}
            distinct_products = len(items)
            total_units = sum(items.values())

            top_product = max(items, key=lambda k: items[k])
            top_product_quantity = items[top_product]
            ttl_seconds = await cart_repository.get_ttl(user_id)
            expiring_soon = (0 < ttl_seconds < 3600)

            logger.info(
                f'get_summary ok: user={user_id} products={distinct_products} '
                f'units={total_units}'
            )
            return {
                "user_id": user_id,
                "distinct_products": distinct_products,
                "total_units": total_units,
                "top_product": {
                    "product_id": top_product,
                    "quantity": top_product_quantity
                },
                "ttl_seconds": ttl_seconds,
                "expiring_soon": expiring_soon
            }
        except Exception as e:
            if not isinstance(e, (ValueError, LookupError)):
                logger.error(f'unexpected error in get_summary: user={user_id} err={str(e)}')
            raise
