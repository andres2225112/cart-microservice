from app.repositories.cart_repository import CartRepository

cart_repository = CartRepository()


class CartService:

    async def add_item(self, user_id: str, product_id: str, quantity: int) -> dict:
        """
        Valida los datos y llama al repositorio para guardar el producto.
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        if not product_id or not product_id.strip():
            raise ValueError("El product_id no puede estar vacío")

        await cart_repository.add_or_update_item(user_id, product_id, quantity)

        return {
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity
        }

    async def get_cart(self, user_id: str) -> dict:
        cart_data = await cart_repository.get_cart(user_id)

        if not cart_data:
            raise ValueError("Carrito no encontrado o vacío")

        items = {
            product_id: int(quantity)
            for product_id, quantity in cart_data.items()
        }

        total_items = sum(items.values())

        return {
            "user_id": user_id,
            "items": items,
            "total_items": total_items
        }

    async def remove_item(self, user_id: str, product_id: str) -> dict:
        if not product_id or not product_id.strip():
            raise ValueError("El product_id no puede estar vacío")

        try:
            exists = await cart_repository.item_exists(user_id, product_id)
            if exists is False:
                raise LookupError(f"Producto {product_id} no encontrado en el carrito")
        except Exception:
            pass

        await cart_repository.remove_item(user_id, product_id)

        return {
            "user_id": user_id,
            "product_id": product_id
        }





    async def update_item(self, user_id: str, product_id: str, quantity: int) -> dict:
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        if not product_id or not product_id.strip():
            raise ValueError("El product_id no puede estar vacío")

        try:
            exists = await cart_repository.item_exists(user_id, product_id)
            if exists is False:
                raise LookupError(f"Producto {product_id} no encontrado en el carrito")
        except Exception:
            pass

        await cart_repository.update_item_quantity(user_id, product_id, quantity)

        return {
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity
        }





    async def clear_cart(self, user_id: str) -> dict:
        await cart_repository.clear_cart(user_id)

        return {
            "user_id": user_id,
            "message": "Carrito eliminado exitosamente"
        }