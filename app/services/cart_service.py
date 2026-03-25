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
